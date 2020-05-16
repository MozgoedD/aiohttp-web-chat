from aiohttp import web, WSMsgType
from aiohttp_session import get_session
from time import time
import aiohttp_jinja2
import json 


from auth.models import User



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
        if session.get('enter_problems'):
            del session['enter_problems']
            return {'message': 'Wrong Login/Password'}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app['db_cursor'], data)
        result = await user.log_in()
        session = await get_session(self.request)
        if result:
            print(f'SRV: {data["login"]} logged in')
            if session.get('enter_problems'):
                del session['enter_problems']
            set_session(session, str(data['login']), self.request)
        else: 
            session['enter_problems'] = True
            redirect(self.request, 'login')



class Signin(web.View):

    @aiohttp_jinja2.template('signin.html')
    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            redirect(self.request, 'chat')
        if session.get('enter_problems'):
            del session['enter_problems']
            return {'message': 'User with this login already exist!'}

    async def post(self):
        data = await self.request.post()
        user = User(self.request.app['db_cursor'], data)
        result = await user.create_user()
        session = await get_session(self.request)
        if not result:
            session['enter_problems'] = True
            redirect(self.request, 'signin')
        else:
            user_login = str(data["login"])
            print(f'SRV: new user created {data["login"]}')
            if session.get('enter_problems'):
                del session['enter_problems']
            self.request.app['users'].append(user_login)
            set_session(session, str(data['login']), self.request)
            

class Logout(web.View):

    async def get(self):
        session = await get_session(self.request)
        if session.get('user'):
            del session['user']
            redirect(self.request, 'index')
        else:
            raise web.HTTPForbidden(body=b'Forbidden')