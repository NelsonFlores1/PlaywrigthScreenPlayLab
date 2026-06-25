"""
Shared test configuration and fixtures for ParaBank Playwright test automation.

Provides browser lifecycle management, Actor fixture with BrowseTheWeb ability,
and Allure screenshot attachment on test failure.
"""

import os
import logging

import pytest
import allure
import urllib.request
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext

from screenplay.actors.actor import Actor
from screenplay.actors.browse_the_web import BrowseTheWeb


logger = logging.getLogger(__name__)

# Default timeout configuration
NAVIGATION_TIMEOUT_MS = 30_000  # 30 seconds
ELEMENT_VISIBILITY_TIMEOUT_MS = 10_000  # 10 seconds

# ParaBank configuration
PARABANK_BASE_URL = "https://parabank.parasoft.com/parabank"


def pytest_configure(config):
    """Initialize ParaBank database at session start to ensure default users exist."""
    try:
        req = urllib.request.Request(
            f"{PARABANK_BASE_URL}/services/bank/initializeDB",
            method="POST",
        )
        urllib.request.urlopen(req, timeout=10)
        logger.info("ParaBank database initialized successfully.")
    except Exception as e:
        logger.warning("Could not initialize ParaBank database: %s", e)


def pytest_addoption(parser):
    """Add custom CLI options for browser configuration.

    Note: If pytest-playwright is installed, it already registers --headed.
    We guard against duplicate registration.
    """
    known_options = set()
    for group in parser._groups:
        for opt in group.options:
            known_options.update(opt.names())

    if "--headed" not in known_options:
        parser.addoption(
            "--headed",
            action="store_true",
            default=False,
            help="Run browser in headed mode (visible window).",
        )

    parser.addoption(
        "--screenshot-mode",
        action="store",
        default="always",
        choices=["always", "on-failure"],
        help="When to capture screenshots: 'always' (default) or 'on-failure'.",
    )


@pytest.fixture(scope="session")
def browser(request):
    """
    Session-scoped fixture that launches a Chromium browser instance.

    Headless by default. Override with:
      - --headed CLI flag
      - HEADED=1 environment variable
    """
    headed_cli = request.config.getoption("--headed", default=False)
    headed_env = os.environ.get("HEADED", "").strip() in ("1", "true", "True", "yes")
    headless = not (headed_cli or headed_env)

    playwright = sync_playwright().start()
    browser_instance = playwright.chromium.launch(headless=headless)

    yield browser_instance

    # Session teardown: close browser and stop Playwright engine
    browser_instance.close()
    playwright.stop()


@pytest.fixture(scope="function")
def page(browser: Browser):
    """
    Function-scoped fixture that creates a new browser context and page per test.

    Each test gets an isolated context (no shared cookies, storage, or session data).
    Configures default timeouts for navigation and element visibility.
    """
    context: BrowserContext = browser.new_context()
    context.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
    context.set_default_timeout(ELEMENT_VISIBILITY_TIMEOUT_MS)

    page_instance: Page = context.new_page()

    yield page_instance

    # Teardown: close context after each test function
    page_instance.close()
    context.close()


@pytest.fixture
def actor(page: Page) -> Actor:
    """Provide an Actor with BrowseTheWeb ability for the current test."""
    return Actor(BrowseTheWeb(page))


# --- Screenshot Evidence ---


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshots and attach to the Allure report.

    Behavior controlled by --screenshot option:
      - 'always' (default): captures screenshot at end of every test (pass or fail)
      - 'on-failure': captures screenshot only when a test fails

    Can also be set via environment variable: SCREENSHOT_MODE=on-failure
    """
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    # Determine screenshot mode
    screenshot_mode = os.environ.get("SCREENSHOT_MODE", "").strip()
    if not screenshot_mode:
        screenshot_mode = item.config.getoption("--screenshot-mode", default="always")

    # Decide whether to capture
    should_capture = False
    if screenshot_mode == "always":
        should_capture = True
    elif screenshot_mode == "on-failure" and report.failed:
        should_capture = True

    if not should_capture:
        return

    # Attempt to get the page fixture from the test item
    page_instance = item.funcargs.get("page")
    if page_instance is None:
        return

    # Determine attachment name based on result
    status = "FAILED" if report.failed else "PASSED"
    attachment_name = f"screenshot_{item.name}_{status}"

    try:
        screenshot = page_instance.screenshot()
        allure.attach(
            screenshot,
            name=attachment_name,
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as screenshot_error:
        # Log screenshot failure gracefully; do not mask the original error
        logger.warning(
            "Failed to capture screenshot for '%s': %s",
            item.nodeid,
            screenshot_error,
        )
