from flask_jwt_extended import get_jwt
from functools import wraps

from api.error_handling import MissingQueryParameterException

'''Common functions to be used by any part of the domain controller'''

def role_required(*required_roles):
    '''Decorator to check if the user has the required role to access the endpoint,
       If the user does not have the required role, a 403 error is returned,
       If the user has the required role, the endpoint is called,
       Should be used as @role_required("role") where role is the required role,
       Can only be used on endpoints with JWT protection: @jwt_required'''
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_role = get_jwt().get("role", None)
            if current_role not in  required_roles:
                return {"message": "Access forbidden: Requires role {}".format(required_roles)}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
