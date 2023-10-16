import sqlite3


class BDBConnector:
    def __init__(self):

        self.db = sqlite3.connect('users.db')
        self.sql = self.db.cursor()

        self.sql.execute("""CREATE TABLE IF NOT EXISTS users (
            id BIGINT,
            name TEXT,
            balance BIGFLOAT,
            amount BIGINT,
            amount_trx BIGINT,
            amount_usd BIGINT,
            last_invoice_id BIGINT,
            total_amount BIGINT,
            suc_transactions BIGINT)""")

        self.db.commit()

    async def add_user(self, user_id, name):
        self.sql.execute(f"SELECT id FROM users WHERE id={user_id}")
        if self.sql.fetchone() is None:
            self.sql.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, name, 0, 0, 0, 0, 0, 0, 0))
            self.db.commit()
            print('Пользователь добавлен!')
        else:
            print('Пользователь уже зарегистрирован!')

    async def add_test_user(self):
        user_id = 1123134
        name = 'TEST'
        self.sql.execute(f"SELECT id FROM users WHERE id={user_id}")

        if self.sql.fetchone() is None:
            self.sql.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", (user_id, name, 0, 0, 0, 0, 0, 0, 0))
            self.db.commit()
            print('Пользователь добавлен!')
        else:
            print('Пользователь уже зарегистрирован!')

    async def pay_balance(self, user_id, amount):
        self.sql.execute(f"UPDATE users SET balance=balance+{amount} WHERE id={user_id}")
        self.db.commit()

    async def sub_balance(self, user_id, amount):
        self.sql.execute(f"UPDATE users SET balance=balance-{amount} WHERE id={user_id}")
        self.db.commit()

    async def set_total_balance(self, user_id, amount):
        self.sql.execute(f"UPDATE users SET total_amount={amount}+total_amount WHERE id={user_id}")
        self.db.commit()
        
    async def get_info(self, user_id):
        self.sql.execute(f"SELECT * FROM users WHERE id={user_id}")
        user_info = self.sql.fetchone()[0]
        return user_info

    async def get_name(self, user_id):
        self.sql.execute(f"SELECT name FROM users WHERE id={user_id}")
        user_name = self.sql.fetchone()[0]
        return user_name

    async def get_balance(self, user_id):
        self.sql.execute(f"SELECT balance FROM users WHERE id={user_id}")
        user_balance = self.sql.fetchone()[0]
        print(user_balance)
        return user_balance

    async def get_amount(self, user_id):
        self.sql.execute(f"SELECT amount FROM users WHERE id={user_id}")
        user_amount = self.sql.fetchone()[0]
        print(user_amount)
        return user_amount

    async def get_amount_trx(self, user_id):
        self.sql.execute(f"SELECT amount_trx FROM users WHERE id={user_id}")
        user_amount_trx = self.sql.fetchone()[0]
        print(user_amount_trx)
        return user_amount_trx

    async def get_amount_usd(self, user_id):
        self.sql.execute(f"SELECT amount_usd FROM users WHERE id={user_id}")
        user_amount_usd = self.sql.fetchone()[0]
        return user_amount_usd

    async def get_last_invoice_id(self, user_id):
        self.sql.execute(f"SELECT last_invoice_id FROM users WHERE id={user_id}")
        user_last_invoice_id = self.sql.fetchone()[0]
        return user_last_invoice_id

    async def get_total_amount(self, user_id):
        self.sql.execute(f"SELECT total_amount FROM users WHERE id={user_id}")
        user_total_amount = self.sql.fetchone()[0]
        return user_total_amount

    async def get_suc_transactions(self, user_id):
        self.sql.execute(f"SELECT suc_transactions FROM users WHERE id={user_id}")
        user_suc_transactions = self.sql.fetchone()[0]
        return user_suc_transactions

    async def set_amount(self, user_id, new_amount):
        self.sql.execute(f"UPDATE users SET amount={new_amount} WHERE id={user_id}")
        self.db.commit()

    async def set_amount_trx(self, user_id, new_amount_trx):
        self.sql.execute(f"UPDATE users SET amount_trx={new_amount_trx} WHERE id={user_id}")
        self.db.commit()

    async def set_amount_usd(self, user_id, new_amount_usd):
        self.sql.execute(f"UPDATE users SET amount_usd={new_amount_usd} WHERE id={user_id}")
        self.db.commit()

    async def set_invoice_id(self, user_id, new_invoice_id):
        self.sql.execute(f"UPDATE users SET last_invoice_id={new_invoice_id} WHERE id={user_id}")
        self.db.commit()

    async def set_suc_transactions(self, user_id):
        self.sql.execute(f"UPDATE users SET suc_transactions=suc_transactions+1 WHERE id={user_id}")
        self.db.commit()
