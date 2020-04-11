from aiohttp import web, WSMsgType
from aiohttp_session import get_session
import aiohttp_jinja2
import json


class Index(web.View):
    @aiohttp_jinja2.template('chat.html')
    async def get(self):
        pass

class WS(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        session = await get_session(self.request)

        for _ws in self.request.app['websockets']:
            await _ws.send_str(f'{session["user"]} has connected:')

        self.request.app['websockets'].append(ws)

        print(f'SRV: connection from {session["user"]}')
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str('[ Your message has been delivered successfully ]')

                    for _ws in self.request.app['websockets']:
                        if _ws == ws:
                            pass
                        else:
                            await _ws.send_str(f'{session["user"]}: {msg.data}')

            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())

        for _ws in self.request.app['websockets']:
            await _ws.send_str(f'{session["user"]} has left')
        self.request.app['websockets'].remove(ws)
        print('websocket connection closed')
        return ws
