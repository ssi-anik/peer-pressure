import hashlib
from functools import wraps
from hmac import new as hmac_new, compare_digest

from flask import request, abort, make_response, jsonify


def validate_signature(secret):
    def check_secret(f):
        @wraps(f)
        def compare_secret(*args, **kwargs):
            if secret:
                digest = 'sha1={}'.format(
                    hmac_new(str.encode(secret), request.data, hashlib.sha1).hexdigest()
                )

                if not compare_digest(digest, request.headers.get('X-Hub-Signature', '')):
                    return abort(make_response(jsonify({
                        'error': True,
                        'message': 'Unauthorized request'
                    }), 401))

            return f(*args, **kwargs)

        return compare_secret

    return check_secret


def excepted_events(events):
    def check_event(f):
        @wraps(f)
        def compare_event(*args, **kwargs):
            if events:
                sent_event = request.headers.get('X-GitHub-Event', '').strip()
                if not hasattr(events, '__iter__'):
                    raise Exception('Invalid events list. expects __iter__ object')
                if sent_event not in events:
                    return abort(make_response(jsonify({
                        'error': True,
                        'message': 'Unauthorized events',
                        'event': sent_event
                    }), 401))

            return f(*args, **kwargs)

        return compare_event

    return check_event


def expects_json(f):
    @wraps(f)
    def check_if_json(*args, **kwargs):
        if not request.is_json:
            return abort(make_response(jsonify({
                'error': True,
                'message': 'Form is only accepted for application/json'
            }), 400))

        return f(*args, *kwargs)

    return check_if_json
