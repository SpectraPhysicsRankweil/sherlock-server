from collections import defaultdict
from aiohttp import web


def get_remote_ip(request):
    return request.headers.get('X-Real-IP', request.remote)


async def index(request):
    return web.FileResponse('./static/index.html')


async def register(request):
    database = request.app['database']
    request_data = await request.json()

    if 'ip_list' not in request_data or not isinstance(request_data['ip_list'], list):
        return web.Response(status=400)  # Bad Request
    if 'identifier' not in request_data or not isinstance(request_data['identifier'], str):
        return web.Response(status=400)  # Bad Request
    database[get_remote_ip(request)][request_data['identifier']] = request_data
    return web.Response()


async def query(request):
    database = request.app['database']
    devices = list(database[get_remote_ip(request)].values())
    return web.json_response(devices)

app = web.Application()

app['database'] = defaultdict(lambda: defaultdict(dict))

# database is a dict with remote_ip as key and a dict as value.
# that dict uses an identifier as key and a dict with device info as values.
# device info dict contains
#  - "ip_list": list with ip adresses (as strings)

app.add_routes([web.get('/', index),
                web.get('/api/query', query),
                web.post('/api/register', register)])
app.router.add_static('/', path='static', name='static')

web.run_app(app, port=80)