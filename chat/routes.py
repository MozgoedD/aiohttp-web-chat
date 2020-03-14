from views import Index, WS


routes = [
    ('GET', '/', Index),
    ('GET', '/ws', WS),
]

def setup_routes(app):
    for route in routes:
        app.router.add_route(route[0], route[1], route[2])
