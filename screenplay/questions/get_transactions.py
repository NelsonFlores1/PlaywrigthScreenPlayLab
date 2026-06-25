import allure


class GetTransactions:
    """Question: What transactions are displayed?"""

    TRANSACTION_ROWS = "#transactionTable tbody tr"

    def answered_by(self, actor) -> list[dict]:
        with allure.step("Get list of transactions"):
            page = actor.ability.page
            page.wait_for_selector("#transactionTable", timeout=10000)
            rows = page.query_selector_all(self.TRANSACTION_ROWS)
            transactions = []
            for row in rows:
                cells = row.query_selector_all("td")
                if not cells:
                    continue
                date = cells[0].inner_text().strip() if len(cells) > 0 else ""
                description = cells[1].inner_text().strip() if len(cells) > 1 else ""
                debit = cells[2].inner_text().strip() or None if len(cells) > 2 else None
                credit = cells[3].inner_text().strip() or None if len(cells) > 3 else None
                transactions.append({
                    "date": date,
                    "description": description,
                    "debit": debit,
                    "credit": credit,
                })
            return transactions
