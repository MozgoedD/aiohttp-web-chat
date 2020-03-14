from aiohttp import web, WSMsgType
import aiohttp_jinja2
import json


class Index(web.View):
    @aiohttp_jinja2.template('main.html')
    async def get(self):
        pass

class WS(web.View):
    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        for _ws in self.request.app['websockets']:
            await _ws.send_str(f'New connection:')

        self.request.app['websockets'].append(ws)

        print(f'SRV: connection from ?')
        async for msg in ws:
            if msg.type == WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str('[ Your message has been delivered successfully ]')

                    for _ws in self.request.app['websockets']:
                        await _ws.send_str(f'{msg.data}')

            elif msg.type == WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())

        for _ws in self.request.app['websockets']:
            await _ws.send_str('One left')
        self.request.app['websockets'].remove(ws)
        print('websocket connection closed')
        return ws

# async def index(request):
#     responce_obj = {'status': 'succed'}
#     return web.Response(text=json.dumps(responce_obj), status=200)

# async def create_user(request):
#     try:
#         user_name = request.query['name']
#         print(f'SRV: created a new user. name: {user_name}')
#         responce_obj = {'status': 'succed', 'message': 'user succesfully created'}
#         return web.Response(text=json.dumps(responce_obj), status=200)

#     except Exception as e:
#         responce_obj = {'status': 'failed', 'message': str(e)}
#         return web.Response(text=json.dumps(responce_obj), status=500)