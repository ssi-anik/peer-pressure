import os

from flask import request, make_response, jsonify

from extension.methods import get_app_configuration, get_flask_instance
from extension.middlewares import validate_signature, expects_json, excepted_events
from extension.processors import HookProcessor, SlackProcessor

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
@excepted_events(['pull_request', 'pull_request_review', 'ping'])
@validate_signature(configuration['secret'])
@expects_json
def handler():
    try:
        data = request.get_json(silent=True)
        event = HookProcessor(data).process()
        pull_request = event.handle()

        if pull_request.action not in configuration['active_events']:
            return make_response(jsonify({
                'error': False,
                'message': 'Not listening to event',
                'event': pull_request.action
            }), 200)

        processed_pull_request = SlackProcessor(pull_request, configuration['slack_users']).process()

        if 'slack' in configuration['mediums']:
            slack_medium = configuration['available_mediums']['slack']
            slack_conf = {
                'url': configuration['slack_url'],
                'channel': configuration['slack_channel'],
                'username': configuration['slack_username'],
                'emoji': configuration['slack_emoji'],
            }
            slack_medium(processed_pull_request, configuration['messages'], slack_conf).notify()
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
