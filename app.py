import os

from flask import request, make_response, jsonify

from extension.hook_processor import HookProcessor
from extension.methods import get_app_configuration, get_flask_instance
from extension.middlewares import validate_signature, expects_json

configuration = get_app_configuration()

app = get_flask_instance(configuration['name'])
http_methods = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH']


# index page
@app.route('/', methods=['GET'], )
def index():
    return make_response(jsonify({
        'error': False,
        'message': 'Peer Pressure up & running',
    }), 200)


# wildcard routes for catching all incoming calls
@app.route('/<path:u_path>', methods=http_methods)
def exception(u_path):
    return make_response(jsonify({
        'error': True,
        'message': 'Invalid route.',
        'method': request.method,
        'path': u_path
    }), 404)


@app.route(configuration['path'], methods=configuration['methods'])
@validate_signature(configuration['secret'])
@expects_json
def handler():
    try:
        data = request.get_json(silent=True)
        event = HookProcessor(data).process()
        pr = event.handle()

        # for medium in configuration['mediums']:
        #     configuration['available_mediums'][medium](configuration['users'], pr).notify()
    except Exception as e:
        return make_response(jsonify({
            'error': True,
            'message': str(e)
        }), 400)

    return make_response(jsonify({
        'error': False,
        'message': 'Handled webhook successfully.'
    }), 202)


if __name__ == '__main__':
    environment = configuration['app_env'] if 'app_env' in configuration else "development" if \
        configuration['debug'] else "production"

    os.environ['FLASK_ENV'] = environment

    if environment == 'production':
        from waitress import serve

        serve(app, host=configuration['host'], port=configuration['port'])
    else:
        app.run(host=configuration['host'], port=configuration['port'], debug=configuration['debug'])
