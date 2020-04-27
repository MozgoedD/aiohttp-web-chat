


class User():
    
    def __init__(self, db, data):
        self.db_cursor = db
        self.login = data.get('login')
        self.password = data.get('password')

    async def check_user(self):
        sql_query = f"""SELECT login FROM users WHERE login='{str(self.login)}';"""
        await self.db_cursor.execute(sql_query)
        user = await self.db_cursor.fetchall()
        if user:
            return True
        else:
            return False

    async def create_user(self):
        is_user_in = await self.check_user()
        if not is_user_in:
            sql_query = f"""INSERT INTO users (login, password)
                                VALUES ('{self.login}', '{self.password}');"""

            await self.db_cursor.execute(sql_query)
            print(f'DB: new user {self.login} with password {self.password}')
            return True
        else:
            print(f'DB: user {self.login} already exist!')
            return False

    async def log_in(self):
        is_user_in = await self.check_user()
        if is_user_in:
            sql_query = f"""SELECT password FROM users WHERE login='{str(self.login)}'"""
            await self.db_cursor.execute(sql_query)
            password = await self.db_cursor.fetchall()
            password = password[0][0]
            if self.password == password:
                return True
            else:
                print(f'DB: wrong password for user {self.login}!')
                return False
            return True
        else:
            print(f'DB: user {self.login} not exist!')
            return False

