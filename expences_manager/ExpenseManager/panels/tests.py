from django.test import TestCase
from django.apps import apps
from django.conf import settings

from .models import Panel, Category, PanelUser


class PanelsModelsTest(TestCase):
    def test_panel_meta_and_owner_relation(self):
        self.assertEqual(Panel._meta.db_table, "panels")
        user_model = apps.get_model(settings.AUTH_USER_MODEL)
        owner_field = Panel._meta.get_field("owner")
        self.assertEqual(owner_field.related_model, user_model)

    def test_category_constraints(self):
        constraint_names = [c.name for c in Category._meta.constraints]
        self.assertIn("uq_category_name_panel_ci", constraint_names)

    def test_paneluser_unique_constraint(self):
        constraint_names = [c.name for c in PanelUser._meta.constraints]
        self.assertIn("uq_panel_user", constraint_names)
