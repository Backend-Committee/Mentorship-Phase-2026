from django.test import TestCase

from .models import Expense, Budget


class TransactionsModelsTest(TestCase):
    def test_expense_table_and_indexes(self):
        self.assertEqual(Expense._meta.db_table, "expenses")
        index_fields = {tuple(idx.fields) for idx in Expense._meta.indexes}
        self.assertIn(("panel", "date"), index_fields)
        self.assertIn(("panel", "category"), index_fields)
        self.assertIn(("panel", "created_by"), index_fields)

    def test_budget_constraints(self):
        self.assertEqual(Budget._meta.db_table, "budgets")
        constraint_names = [c.name for c in Budget._meta.constraints]
        self.assertIn("uq_budget_period_scope", constraint_names)
