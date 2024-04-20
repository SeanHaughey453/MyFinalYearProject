from flask_jwt_extended import get_jwt
from functools import wraps



def role_required(*required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_role = get_jwt().get("role", None)
            if current_role not in  required_roles:
                return {"message": "Access forbidden: Requires role {}".format(required_roles)}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
