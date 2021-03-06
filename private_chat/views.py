from aiohttp import web, WSMsgType
from aiohttp_session import get_session
from time import strftime
import aiohttp_jinja2
import json

from private_chat.models import PrivateRoom


class PrivateChats(web.View):
    @aiohttp_jinja2.template('private_chats.html')
    async def get(self):
        session = await get_session(self.request)
        return {'user_name': str(session["user"]), 'user_list': self.request.app['users'], 'conversation': ''}

class PrivateChatTo(web.View):
    @aiohttp_jinja2.template('private_chats.html')
    async def get(self):
        conversation = str(self.request.match_info['conversation'])
        session = await get_session(self.request)

        if self.request.app['private_rooms']:
            is_exist = False
            for active_private_chat in self.request.app['private_rooms']:
                if (active_private_chat.user_2 == str(session["user"]) and active_private_chat.user_1 == conversation) or (active_private_chat.user_1 == str(session["user"]) and active_private_chat.user_2 == conversation):
                    is_exist = True
                    break
            if not is_exist:
                private_chat = PrivateRoom(str(session["user"]), conversation)
                self.request.app['private_rooms'].append(private_chat)
        else:
            private_chat = PrivateRoom(str(session["user"]), conversation)
            self.request.app['private_rooms'].append(private_chat)

        return {'user_name': str(session["user"]), 'user_list': self.request.app['users'], 'conversation': conversation}

class Private_WS(web.View):
    async def get(self):
        conversation = str(self.request.match_info['conversation'])
        session = await get_session(self.request)

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        await ws.send_str(f'Private chat with user {conversation}! You entered as: {session["user"]}')

        for active_private_chat in self.request.app['private_rooms']:
            if (active_private_chat.user_2 == str(session["user"]) and active_private_chat.user_1 == conversation) or (active_private_chat.user_1 == str(session["user"]) and active_private_chat.user_2 == conversation):
                private_chat = active_private_chat

        for _ws in private_chat.get_ws_list():
            await _ws.send_str(f'{str(session["user"])} has connected to private chat {private_chat.get_name()}')

        private_chat.append_ws(ws)
        if str(session["user"]) == private_chat.user_2:
            if private_chat.user_1_public_key:
                await ws.send_str(f'{private_chat.user_1_public_key}')

        elif str(session["user"]) == private_chat.user_1:
            if private_chat.user_2_public_key:
                await ws.send_str(f'{private_chat.user_2_public_key}')
        
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                print(msg.data)
                if msg.data == 'close':
                    await ws.close()
                elif msg.data.startswith('PublicKey:'):
                    if str(session["user"]) == private_chat.user_1:
                        private_chat.user_1_public_key = msg.data
                        for _ws in private_chat.get_ws_list():
                            if _ws != ws:
                                await _ws.send_str(f'{private_chat.user_1_public_key}')

                    elif str(session["user"]) == private_chat.user_2:
                        private_chat.user_2_public_key = msg.data
                        for _ws in private_chat.get_ws_list():
                            if _ws != ws:
                                await _ws.send_str(f'{private_chat.user_2_public_key}')
                else:
                    print(f'SRV: from user {str(session["user"])}: {msg.data}')
                    for _ws in private_chat.get_ws_list():
                        if _ws != ws:
                            await _ws.send_str(f'{msg.data}')

            elif msg.type == WSMsgType.ERROR:
                print('SRV: ws connection closed with exception %s' %ws.exception())

        for _ws in private_chat.get_ws_list():
            await _ws.send_str(f'{session["user"]} has left from private chat {private_chat.get_name()}')

        private_chat.remove_ws(ws)

