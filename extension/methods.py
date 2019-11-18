from benedict import benedict
from flask import Flask

from extension.mediums import Slack, Email

DEFAULT_MESSAGES = {
    'opened': "New PR #{number} with `{title}` on {repo} is received by {by} to {base} from {head}. Assigns {assignees}. Asks {requested_reviewers} to review the PR. {url}",
    'commented': "PR #{number} on {repo} by {by} receives a comment from {actor} - `{comment}`.",
    'assigned': "PR #{number} on {repo} by {by} - {actor} assigns assignees {assignees}.",
    'labeled': "PR #{number} on {repo}, {actor} labels with `{labels}`.",
    'review_requested': "PR #{number} on {repo} by {by} - {actor} asks {requested_reviewers} to review the PR.",
    'review_request_removed': "PR #{number} on {repo} by {by} - {actor} removes {removed_reviewer} as a reviewer.",
    'approved': ":tada: - PR #{number} on {repo} by {by} is now approved by {actor}. {assignees}, go on!",
    'changes_requested': "PR #{number} on {repo} by {by} - {actor} commented {comment} to make some changes.",
    'merged': "PR #{number} on {repo} is merged on {base} by {actor} at {at}. :cherries:.",
    'closed': "PR #{number} on {repo} is closed by {actor} and not merged. :cry:.",
}


def get_app_configuration():
    try:
        # load configuration from yaml
        conf = benedict.from_yaml('configuration.yaml')
    except ValueError:
        raise Exception("Invalid yaml/yml file")
    except Exception:
        raise Exception("'configuration.yaml' file missing")

    host = conf['host'] if 'host' in conf else '0.0.0.0'
    port = conf['port'] if 'port' in conf else 80
    debug = bool(conf['debug'] if 'debug' in conf else False)

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

    app_env = conf['app-env'] if 'app-env' in conf else 'production'

    if len(unsupported_medium):
        raise Exception('Unsupported mediums: {}'.format(", ".join(unsupported_medium)))

    slack_users = conf['users.slack'] if ['users', 'slack'] in conf and conf['users.slack'] else {}
    email_users = conf['users.email'] if ['users', 'email'] in conf and conf['users.email'] else {}

    custom_messages = conf['messages'] if 'messages' in conf else {}
    messages = {**DEFAULT_MESSAGES, **custom_messages}

    return {
        'app_env': app_env,
        'host': host,
        'port': port,
        'debug': debug,
        'name': name,
        'path': path,
        'methods': method,
        'secret': secret,
        'mediums': mediums,
        'available_mediums': available_mediums,
        'slack_users': slack_users,
        'email_users': email_users,
        'messages': messages,
    }


def get_flask_instance(name) -> Flask:
    return Flask(name)
