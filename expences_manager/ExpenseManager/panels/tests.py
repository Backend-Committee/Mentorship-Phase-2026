from django.test import TestCase

from expenses.models import Panel, Category, PanelUser, User


class PanelsModelsTest(TestCase):
    def test_panel_meta_and_owner_relation(self):
        self.assertEqual(Panel._meta.db_table, "panels")
        owner_field = Panel._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, User)

    def test_category_constraints(self):
        constraint_names = [c.name for c in Category._meta.constraints]
        self.assertIn("uq_category_name_panel_ci", constraint_names)

    def test_paneluser_unique_constraint(self):
        constraint_names = [c.name for c in PanelUser._meta.constraints]
        self.assertIn("uq_panel_user", constraint_names)
