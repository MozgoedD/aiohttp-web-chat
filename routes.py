from chat.views import Index, WS
from auth.views import Login


routes = [
    ('GET', '/', Index, 'index'),
    ('GET', '/ws', WS, 'ws'),
    ('GET', '/login', Login, 'login'),
    ('POST', '/login', Login, 'plogin'),
]

def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name = route[3])
