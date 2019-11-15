import hashlib
from hmac import new as hmac_new, compare_digest

from benedict import benedict
from flask import Flask, make_response, jsonify, request

from extension.hook_processor import HookProcessor

# load configuration

try:
    conf = benedict.from_yaml('configuration.yaml')
except ValueError:
    raise Exception("Invalid yaml/yml file")
except Exception:
    raise Exception("'configuration.yaml' file missing")

# Get the webhook receiver path
path = "/{}".format((conf['webhook-path'] if 'webhook-path' in conf else 'hook').strip('/'))

# Get the webhook receiver method
method = conf['webhook-method'] if 'webhook-method' in conf else 'GET'
# Convert method to array if not
method = method if isinstance(method, list) else [method]
# app name
name = conf['app-name'] if 'app-name' in conf else __name__
# get the secret key for incoming requests to match
secret = conf['secret-key'] if 'secret-key' in conf else None

# Init flask app
app = Flask(name)
HTTP_METHODS = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


# index page
@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify({
        'error': False,
        'message': 'Peer Pressure up & running',
    }), 200)


# wildcard routes for catching all incoming calls
@app.route('/<path:u_path>', methods=HTTP_METHODS)
def exception(u_path):
    return make_response(jsonify({
        'error': True,
        'message': 'Invalid route.',
        'method': request.method,
        'path': u_path
    }), 404)


# Check the incoming requests to match the provided secret key
@app.before_request
def validate_signature():
    if not secret:
        return
    digest = 'sha1={}'.format(hmac_new(str.encode(secret), request.data, hashlib.sha1).hexdigest())

    if not compare_digest(digest, request.headers.get('X-Hub-Signature')):
        return make_response(jsonify({
            'error': True,
            'message': 'Unauthorized request'
        }), 401)


@app.route(path, methods=method)
def handler():
    if not request.is_json:
        return make_response(jsonify({
            'error': True,
            'message': 'Form is only accepted for application/json'
        }))

    try:
        data = request.get_json(silent=True)
        event = HookProcessor(data).process()
        pr = event.handle()
    except Exception as e:
        return make_response(jsonify({
            'error': True,
            'message': str(e)
        }), 400)

    return make_response(jsonify({
        'error': False,
        'message': 'Handled webhook successfully.'
    }), 202)
