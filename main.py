import time
from datetime import datetime

from flask import Flask, render_template, request

from model import networks, Device, Network


def get_remote_ip(request):
    return request.headers.get('X-Real-IP', request.remote_addr)


app = Flask(__name__)

@app.template_filter()
def fmttime(value):
    return datetime.fromtimestamp(value).strftime('%H:%M')

@app.template_filter()
def ago(value):
    difference = int(time.time() - value)
    if difference < 180:
        return str(difference) + ' seconds ago'
    return str(difference // 60) + ' minutes ago'

@app.route('/')
def index():
    remote_ip = get_remote_ip(request)
    network = networks.get(remote_ip, Network(remote_ip))
    print(network.devices)
    return render_template('./index.html', network=network)


@app.route('/api/register', methods=['POST'])
def register():
    request_data = request.get_json()

    try:
        ip_list = tuple(request_data['ip_list'])
        hostname = request_data['hostname']
    except TypeError:
        return '"ip_list" or "hostname" key is missing or wrong datatype', 400  # Bad Request

    unique_id = request_data.get('unique_id', None)

    remote_ip = get_remote_ip(request)
    network = networks.get(remote_ip, Network(remote_ip))
    key = unique_id if unique_id else hostname

    if key in network:
        network[key].update_timestamp()
        network[key].ip_list = ip_list
        network[key].hostname = hostname
    else:
        network[key] = Device(ip_list, hostname, unique_id)

    networks[remote_ip] = network

    return ''

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)