from aiohttp import web, WSMsgType
from aiohttp_session import get_session
from time import time
import aiohttp_jinja2
import json 

from auth.models import User


# wrong_enter = False
# wrong_signin = False

def set_session(session, user_id, request):
    session['user'] = str(user_id)
    session['last_visit'] = time()
    print(f'SRV: new session {session}')
    redirect(request, 'chat')

def redirect(request, router_name):
    url = request.app.router[router_name].url_for()
    raise web.HTTPFound(url)

class Login(web.View):

    @aiohttp_jinja2.template('login.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'chat')
        # global wrong_enter
        # if wrong_enter == True:
        #     return {'message': 'Wrong Login/Password'}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app['db_cursor'], data)
        result = await user.log_in()
        # global wrong_enter
        if result:
            print(f'SRV: {data["login"]} logged in')
            # wrong_enter = False
            session = await get_session(self.request)
            set_session(session, str(data['login']), self.request)
        else: 
            # wrong_enter = True
            redirect(self.request, 'login')



class Signin(web.View):

    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'chat')
        # global wrong_signin
        # if wrong_signin:
        #     return {'message': 'User with this login already exist!'}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app['db_cursor'], data)
        result = await user.create_user()
        # global wrong_signin
        if not result:
            # wrong_signin = True
            redirect(self.request, 'signin')
        else:
            print(f'SRV: new user created {data["login"]} {data["password"]}')
            # wrong_signin = False
            self.request.app['users'].append(data('login'))
            session = await get_session(self.request)
            set_session(session, str(data['login']), self.request)
            

class Logout(web.View):

    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'index')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')