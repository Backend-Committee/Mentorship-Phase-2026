from decimal import Decimal
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from rest_framework.test import APIRequestFactory

from expenses.models import User, Panel, Category, Expense, Budget
from expenses.serializers import ExpenseSerializer, BudgetSerializer


class ExpenseModelSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", email="alice@example.com", password="pass")
        self.panel = Panel.objects.create(name="Household", owner=self.user)
        self.other_panel = Panel.objects.create(name="Work", owner=self.user)
        self.category = Category.objects.create(panel=self.panel, name="Groceries")
        self.other_category = Category.objects.create(panel=self.other_panel, name="Travel")
        self.today = date.today()

    def test_model_rejects_non_positive_amount(self):
        e = Expense(panel=self.panel, category=self.category, created_by=self.user, amount=Decimal("0"), date=self.today)
        with self.assertRaises(ValidationError) as cm:
            e.full_clean()
        self.assertIn("Amount must be greater than zero", str(cm.exception))

    def test_model_rejects_category_panel_mismatch(self):
        e = Expense(panel=self.panel, category=self.other_category, created_by=self.user, amount=Decimal("10"), date=self.today)
        with self.assertRaises(ValidationError) as cm:
            e.full_clean()
        self.assertIn("Category must belong to the same panel", str(cm.exception))

    def test_serializer_validates_decimal_places_and_positive(self):
        factory = APIRequestFactory()
        request = factory.post("/", {}, format="json")
        request.user = self.user

        data = {
            "panel": str(self.panel.id),
            "category": str(self.category.id),
            "amount": "10.123",  # more than 2 decimals
            "date": self.today.isoformat(),
        }
        serializer = ExpenseSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("no more than 2 decimal places", str(serializer.errors))

        data["amount"] = "0"
        serializer = ExpenseSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Amount must be greater than zero", str(serializer.errors))

    def test_serializer_create_sets_created_by_and_persists(self):
        factory = APIRequestFactory()
        request = factory.post("/", {}, format="json")
        request.user = self.user

        data = {
            "panel": str(self.panel.id),
            "category": str(self.category.id),
            "amount": "12.50",
            "date": self.today.isoformat(),
            "description": "Weekly groceries",
        }
        serializer = ExpenseSerializer(data=data, context={"request": request})
        self.assertTrue(serializer.is_valid(), msg=str(serializer.errors))
        expense = serializer.save(created_by=self.user)
        self.assertIsNotNone(expense.id)
        self.assertEqual(expense.created_by, self.user)
        self.assertEqual(expense.amount, Decimal("12.50"))

    def test_serializer_rejects_category_panel_mismatch(self):
        factory = APIRequestFactory()
        request = factory.post("/", {}, format="json")
        request.user = self.user

        data = {
            "panel": str(self.panel.id),
            "category": str(self.other_category.id),
            "amount": "15.00",
            "date": self.today.isoformat(),
        }
        serializer = ExpenseSerializer(data=data, context={"request": request})
        self.assertFalse(serializer.is_valid())
        self.assertIn("Category must belong to the same panel", str(serializer.errors))


class BudgetModelSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="bob", email="bob@example.com", password="pass")
        self.panel = Panel.objects.create(name="Team", owner=self.user)
        self.category = Category.objects.create(panel=self.panel, name="Ops")

    def test_budget_limit_must_be_positive(self):
        b = Budget(panel=self.panel, category=self.category, limit_amount=Decimal("0"), period=Budget.Period.MONTHLY)
        with self.assertRaises(ValidationError):
            b.full_clean()

    def test_custom_period_requires_dates_and_date_order(self):
        b = Budget(panel=self.panel, category=None, limit_amount=Decimal("1000"), period=Budget.Period.CUSTOM)
        with self.assertRaises(ValidationError):
            b.full_clean()

        b.start_date = date.today()
        b.end_date = date.today() - timedelta(days=1)
        with self.assertRaises(ValidationError):
            b.full_clean()

    def test_category_panel_mismatch_rejected(self):
        other_panel = Panel.objects.create(name="OtherTeam", owner=self.user)
        other_cat = Category.objects.create(panel=other_panel, name="SpecialTravel")
        b = Budget(panel=self.panel, category=other_cat, limit_amount=Decimal("100"), period=Budget.Period.MONTHLY)
        with self.assertRaises(ValidationError):
            b.full_clean()
