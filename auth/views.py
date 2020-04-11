from aiohttp import web, WSMsgType
from aiohttp_session import get_session
from time import time
import aiohttp_jinja2
import json 


def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    print(session)
    redirect(request, 'index')

def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)

class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        pass

    async def post(self):
        data = await self.request.post()
        print(f'SRV: {data["login"]} logged in')
        session = await get_session(self.request)
        set_session(session, str(data['login']), self.request)