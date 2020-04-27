from chat.views import Index, WS, Chat, RoomCreate, ChatTo, SecretRoomCreate
from auth.views import Login, Signin, Logout

# Rooms replace by chat

routes = [
    ('GET', '/index', Index, 'index'),
    ('GET', '/chat', Chat, 'chat'),
    ('GET', '/create_room', RoomCreate, 'create_room'),
    ('POST', '/create_room', RoomCreate, 'create_room'),

    ('GET', '/create_secret_room', SecretRoomCreate, 'create_secret_room'),
    ('POST', '/create_secret_room', SecretRoomCreate, 'create_secret_room'),
    
    ('GET', '/chat/{room}', ChatTo, 'to_chat'),
    ('GET', '/ws/{room}', WS, 'ws'),
    ('GET', '/login', Login, 'login'),
    ('POST', '/login', Login, 'login'),
    ('GET', '/signin', Signin, 'signin'),
    ('POST', '/signin', Signin, 'signin'),
    ('GET', '/logout', Logout, 'logout'),
]

def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2], name = route[3])

