# -----------------------------------------------------------------------------
# ----------------------------------DECORATORS---------------------------------
# -----------------------------------------------------------------------------
def disabled(f):
    """
    Decorator that returns an HTTP 503 (Service Unavailable) error code when a
    route is invoked.

    Because of the order of decorator execution, this decorator should come
    immediatly after registering the route and before any other decorators.

    As an example:
        @app.route("/account/")
        @disabled
        @...(other decorators)
        def account():
            pass
    """
    @wraps(f)
    def _wrapper(*args, **kwargs):
        return abort(503)
    return _wrapper

def user_allowed(user_name):
    """ Allows only a given user access to a route.  """
    def _decorator(f):
        @wraps(f)
        def _wrapper(*args, **kwargs):
            if current_user.is_anonymous:
                pass
            elif current_user.username == user_name:
                return f(*args, **kwargs)
            return abort(403)
        return _wrapper
    return _decorator
