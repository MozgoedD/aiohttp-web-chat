from aiohttp import web, WSMsgType
from aiohttp_session import get_session
from time import strftime
import aiohttp_jinja2
import json

from chat.models import Message, Room, UserInChat
from auth.models import User

def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)

def redirect_to_room(request, room_name):
    url = request.app.router['to_chat'].url_for(room=room_name)
    raise web.HTTPFound(url)


class Index(web.View):
    @aiohttp_jinja2.template('index.html')
    async def get(self):
        pass

class Chat(web.View):
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        session = await get_session(self.request)
        return {'room_name': '', 'rooms': self.request.app['rooms'], 'user_name': str(session["user"])}

class RoomCreate(web.View):
    @aiohttp_jinja2.template('create_room.html')
    async def get(self):
        session = await get_session(self.request)
        # return {'room_name': '', 'rooms': self.request.app['rooms'], 'user_name': str(session["user"])}

    async def post(self):
        data = await self.request.post()
        name = str(data.get('room_name'))
        room = Room(self.request.app['db_cursor'], name)
        result = await room.create_room()
        if not result:
            redirect(self.request, 'chat')
        else:
            if room not in self.request.app['rooms']:
                self.request.app['rooms'].append(room)

            redirect_to_room(self.request, f"{data.get('room_name')}")

class ChatTo(web.View):
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        room_name = self.request.match_info['room'].lower()
        room = Room(self.request.app['db_cursor'], room_name)
        is_room_in = await room.check_room()
        if not is_room_in:
            redirect(self.request, 'chat')
        else:
            session = await get_session(self.request)
            return {'room_name': str(room_name), 'rooms': self.request.app['rooms'], 'user_name': str(session["user"])}

class WS(web.View):
    async def get(self):
        room_name = self.request.match_info['room'].lower()
        for room_in_chat in self.request.app['rooms']:
            if room_in_chat.get_name() == room_name:
                room = room_in_chat
        # just checking, after delete!
        if not room:
            redirect(self.request, 'index')

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        session = await get_session(self.request)
        await ws.send_str(f'Welcome to the room {room.get_name()}! You entered as: {session["user"]} ')
        room_id = await room.get_room_id()
        user = UserInChat(self.request.app['db_cursor'], session['user'])
        user_id = await user.get_user_id()
        message = Message(self.request.app['db_cursor'], user_id, room_id)

        messages_list = await message.get_messages()
        print(messages_list)
        if messages_list:
            for message_in_db in messages_list:
                await ws.send_str(f'{message_in_db[0]}: {message_in_db[1]}')

        for _ws in room.get_ws_list():
            await _ws.send_str(f'{session["user"]} has connected:')

        self.request.app['websockets'].append(ws)
        room.append_ws(ws)

        print(f'SRV: connection from {session["user"]} to the room {room.get_name()}')
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await message.save_message(f'{msg.data}', f'{str(strftime("%Y-%m-%d %H:%M"))}')
                    for _ws in room.get_ws_list():
                            if _ws != ws:
                                await _ws.send_str(f'{session["user"]}: {msg.data}')

            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %ws.exception())

        for _ws in room.get_ws_list():
            await _ws.send_str(f'{session["user"]} has left from the room {room.get_name()}')
        room.remove_ws(ws)
        self.request.app['websockets'].remove(ws)
        print('websocket connection closed')
        return ws

