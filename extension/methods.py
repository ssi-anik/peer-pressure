from benedict import benedict
from flask import Flask

from extension.mediums import Slack, Email


def get_app_configuration():
    try:
        # load configuration from yaml
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
    # get the notification mediums
    mediums = conf['notification-medium'] if 'notification-medium' in conf else 'slack'
    mediums = mediums if isinstance(mediums, list) else [mediums]

    available_mediums = {
        'slack': Slack, 'email': Email
    }

    unsupported_medium = [item for item in mediums if item not in available_mediums.keys()]

    if len(unsupported_medium):
        raise Exception('Unsupported mediums: {}'.format(", ".join(unsupported_medium)))

    return {
        'name': name,
        'path': path,
        'methods': method,
        'secret': secret,
        'mediums': mediums,
        'available_mediums': available_mediums,
    }


def get_flask_instance(name) -> Flask:
    return Flask(name)
