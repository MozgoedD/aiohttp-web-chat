from aiohttp import web
from aiohttp_session import get_session

async def authorize(app, handler):
    async def middleware(request):
        def check_path(path):
            result = True
            for r in ['/login', '/static/', '/signin', '/signout', '/_debugtoolbar/']:
                if path.startswith(r):
                    result = False
            return result

        session = await get_session(request)
        if session.get("user"):
            return await handler(request)
        elif check_path(request.path):
            url = request.app.router['login'].url_for()
            raise web.HTTPFound(url)
            return handler(request)
        else:
            return await handler(request)

    return middleware