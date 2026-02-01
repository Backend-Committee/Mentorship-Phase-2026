import sqlite3


class DatabaseManager:
    def __init__(self, db_name="expense_star.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        sql_schema = """
                        -- 1. Authentication Info (Credentials)
                        CREATE TABLE IF NOT EXISTS AuthInfo (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT UNIQUE NOT NULL,
                            email TEXT UNIQUE NOT NULL,
                            hashed_password TEXT NOT NULL
                        );

                        -- 2. User Profile (Linked to Auth)
                        CREATE TABLE IF NOT EXISTS User (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            display_name TEXT NOT NULL,
                            auth_id INTEGER NOT NULL,
                            FOREIGN KEY (auth_id) REFERENCES AuthInfo(id) ON DELETE CASCADE
                        );

                        -- 3. Password Reset Tokens
                        -- CREATE TABLE IF NOT EXISTS ResetTokens (
                            -- token_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            -- user_id INTEGER NOT NULL,
                            -- token TEXT NOT NULL,
                            -- FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
                        -- );

                        -- 4. Bank Accounts (Owned by User)
                        CREATE TABLE IF NOT EXISTS BankAcc (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            title TEXT NOT NULL,
                            balance REAL DEFAULT 0.0,
                            user_id INTEGER NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
                        );

                        -- 5. Transactions (Income/Expense on an account)
                        CREATE TABLE IF NOT EXISTS [Transaction] (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            description TEXT,
                            amount REAL NOT NULL,
                            type TEXT NOT NULL CHECK (type IN ('income', 'expense')),
                            bank_account_id INTEGER NOT NULL,
                            FOREIGN KEY (bank_account_id) REFERENCES BankAcc(id) ON DELETE CASCADE
                        );

                        -- 6. Transfers (Moving money between accounts)
                        CREATE TABLE IF NOT EXISTS Transfer (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            description TEXT,
                            src_bank_account_id INTEGER NOT NULL,
                            dst_bank_account_id INTEGER NOT NULL,
                            amount REAL NOT NULL,
                            FOREIGN KEY (src_bank_account_id) REFERENCES BankAcc(id),
                            FOREIGN KEY (dst_bank_account_id) REFERENCES BankAcc(id)
                        );
                    """

        with self.conn:
            self.conn.executescript(sql_schema)
