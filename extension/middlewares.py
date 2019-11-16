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
