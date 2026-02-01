from typing import Callable

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from prompt_toolkit.validation import Validator

from features.account.model import Account
from features.account.service import AccountService


class AccountsMenuScreen:
    """Menu for the currently logged-in user's accounts"""

    def __init__(self, service: AccountService, current_user):
        self.service = service
        self.current_user = current_user
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def _refresh_accounts(self):
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def show_accounts(self):
        self._refresh_accounts()
        for account in self.accounts:
            print(account)

    def render(self) -> str:
        self.show_accounts()
        return inquirer.select(
            message="Accounts",
            choices=[
                Choice("transaction", name="Transaction"),
                Choice("create_account", name="Create account"),
                # Choice("edit_account", name="Edit Account"),
                # Choice("delete_an_account", name="Delete An Account"),
                Choice("back", name="Back"),
            ],
        ).execute()


class TransactionScreen:
    """Displays Screen in which you can add(expenses, incomes, transfers)."""

    def __init__(self, service: AccountService, current_user):
        self.service = service
        self.current_user = current_user
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def _refresh_accounts(self):
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)
        pass

    def show_accounts(self):
        self._refresh_accounts()
        for account in self.accounts:
            print(account)

    def render(self) -> str:
        self.show_accounts()

        return inquirer.select(
            message="Choose a transaction",
            choices=[
                Choice("expense", name="Expense"),
                Choice("income", name="Income"),
                Choice("trasnfer", name="Transfer"),
                Choice("back", name="Back"),
            ],
        ).execute()


class ExpenseScreen:
    """Displays Screen in which you can add expenses"""

    def __init__(self, service: AccountService, current_user, send_message: Callable):
        self.service = service
        self.current_user = current_user
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)
        self.send_message = send_message

    def _refresh_accounts(self):
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def show_accounts(self):
        self._refresh_accounts()
        for account in self.accounts:
            print(account)

    def render(self) -> str:
        self.show_accounts()

        account_choice = inquirer.select(
            message="Choose an account",
            choices=[
                Choice(account.id, name=account.title) for account in self.accounts
            ],
        ).execute()

        from InquirerPy.validator import NumberValidator

        amount: int = inquirer.text(
            message="amount",
            validate=NumberValidator(message="Input must be a number"),
        ).execute()

        try:
            self.service.add_transaction(
                id=account_choice, tx_type="expense", amount=int(amount)
            )
            self.send_message("\nExpense added successfully!\n")
        except (ValueError, LookupError) as e:
            self.send_message(f"\nError: {e}\n")

        return "transaction"


class IncomeScreen:
    """Displays Screen in which you can add income"""

    def __init__(self, service: AccountService, current_user, send_message: Callable):
        self.service = service
        self.current_user = current_user
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)
        self.send_message = send_message

    def _refresh_accounts(self):
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def show_accounts(self):
        self._refresh_accounts()
        for account in self.accounts:
            print(account)

    def render(self) -> str:
        self.show_accounts()

        account_choice = inquirer.select(
            message="Choose an account",
            choices=[
                Choice(account.id, name=account.title) for account in self.accounts
            ],
        ).execute()

        from InquirerPy.validator import NumberValidator

        amount: int = inquirer.text(
            message="amount",
            validate=NumberValidator(message="Input must be a number"),
        ).execute()

        try:
            self.service.add_transaction(account_choice, "income", int(amount))
            self.send_message("\n✔ Income added successfully!\n")
        except (ValueError, LookupError) as e:
            self.send_message(f"\n✘ Error: {e}\n")

        return "transaction"


class TransferScreen:
    """Displays Screen in which you can make a transfer"""

    def __init__(self, service: AccountService, current_user, send_message: Callable):
        self.service = service
        self.current_user = current_user
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)
        self.send_message = send_message

    def _refresh_accounts(self):
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def show_accounts(self):
        self._refresh_accounts()
        for account in self.accounts:
            print(account)

    def render(self) -> str:
        self.show_accounts()

        if len(self.accounts) < 2:
            self.send_message("\nYou need at least 2 accounts to make a transfer.\n")
            return "transaction"

        src_account_choice = inquirer.select(
            message="Choose a source account",
            choices=[
                Choice(account.id, name=account.title) for account in self.accounts
            ],
        ).execute()

        dst_account_choice = inquirer.select(
            message="Choose a destination account",
            choices=[
                Choice(account.id, name=account.title)
                for account in self.accounts
                if src_account_choice != account.id
            ],
        ).execute()

        from InquirerPy.validator import NumberValidator

        amount: int = inquirer.text(
            message="amount",
            validate=NumberValidator(),
        ).execute()

        description = inquirer.text(
            message="Description",
        ).execute()

        src_account = self.service.get_account(src_account_choice)

        if src_account.balance < float(amount):
            self.send_message(
                f"Rejected!, Insufficent Funds, Your balance is {src_account.balance} and you are trying to send {amount}"
            )
            return "transaction"

        try:
            self.service.add_transfer(
                src_account_choice, dst_account_choice, amount, description
            )
            self.send_message("\n✔ Transfer done successfully!\n")
        except (ValueError, LookupError) as e:
            self.send_message(f"\n✘ Error: {e}\n")

        return "transaction"


class CreateAccountScreen:
    """Displays Screen in which you can create account"""

    def __init__(self, service: AccountService, current_user):
        self.service = service
        self.current_user = current_user
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def _refresh_accounts(self):
        self.accounts = self.service.get_all_user_accounts(self.current_user.id)

    def render(self) -> str:
        account_title = inquirer.text(
            message="Title",
        ).execute()

        from InquirerPy.validator import NumberValidator

        initial_balance = inquirer.text(
            message="Title",
            validate=NumberValidator(message="Input must be a number"),
        ).execute()

        self.service.create_account(
            title=account_title, user_id=self.current_user.id, balance=initial_balance
        )

        print("Account Created successfully")

        return "Back"
