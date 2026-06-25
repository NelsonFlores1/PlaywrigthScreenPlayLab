from __future__ import annotations
from typing import Any

from screenplay.actors.browse_the_web import BrowseTheWeb


class Actor:
    """Represents a user interacting with the system under test."""

    def __init__(self, browse_the_web: BrowseTheWeb):
        self._browse_the_web = browse_the_web

    @property
    def ability(self) -> BrowseTheWeb:
        """Return the BrowseTheWeb ability."""
        return self._browse_the_web

    def attempts_to(self, *tasks) -> None:
        """Execute one or more Tasks sequentially."""
        for task in tasks:
            task.perform_as(self)

    def asks_about(self, question) -> Any:
        """Evaluate a Question and return the result."""
        return question.answered_by(self)
