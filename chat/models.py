

class Message():

    def __init__(self, db, user, room_id):
        self.db_cursor = db
        self.user = user
        self.room_id = int(room_id)

    async def save_message(self, text, datetime):
        sql_query = f"""INSERT INTO messages (user_login, room, text, datetime)
                    VALUES ('{self.user}', '{self.room_id}', '{text}', '{datetime}');"""
        await self.db_cursor.execute(sql_query)

    async def get_messages(self):
        sql_query = f"""SELECT user_login, text FROM messages WHERE room = {self.room_id} ORDER BY datetime;"""
        await self.db_cursor.execute(sql_query)
        messages = await self.db_cursor.fetchall()
        print(messages, type(messages))
        return messages

class Room():
    
    def __init__(self, db, name):
        self.db_cursor = db
        self.name = name
        self.websockets = []

    def get_name(self):
        return f'{self.name}'

    def get_ws_list(self):
        return self.websockets

    async def check_room(self):
        sql_query = f"""SELECT name FROM rooms WHERE name='{str(self.name)}';"""
        await self.db_cursor.execute(sql_query)
        room = await self.db_cursor.fetchall()
        if room:
            return True
        else:
            return False

    async def create_room(self):
        is_room_in = await self.check_room()
        if not is_room_in:
            sql_query = f"""INSERT INTO rooms (name)
                    VALUES ('{self.name}');"""
            await self.db_cursor.execute(sql_query)
            print('DB: room has been created')
            return True
        else: 
            print('DB: room exist!')
            return False

    async def get_room_id(self):
        sql_query = f"""SELECT id FROM rooms WHERE name='{str(self.name)}';"""
        await self.db_cursor.execute(sql_query)
        room_id = await self.db_cursor.fetchall()
        return room_id[0][0]

    def append_ws(self, ws):
        self.websockets.append(ws)

    def remove_ws(self, ws):
        self.websockets.remove(ws)