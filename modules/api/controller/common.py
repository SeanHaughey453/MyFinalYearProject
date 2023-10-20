from flask_jwt_extended import get_jwt
from functools import wraps

from api.error_handling import MissingQueryParameterException

'''Common functions to be used by any part of the domain controller'''

def _check_if_request_arg_present(parser, arg, enforce=True, strict=False) -> str:
    '''Checks if a given argument was provided in the request
       If enforce is false, then the request is not required to have the argument
       If strict is false does not inforce all rules, which allows empty payload for requests '''
    args = parser.parse_args(strict=strict)
    argument = args.get(arg)
    if not argument and enforce == True:
        raise MissingQueryParameterException("This request requires a {} query parameter".format(arg))
    return argument

def role_required(required_role):
    '''Decorator to check if the user has the required role to access the endpoint,
       If the user does not have the required role, a 403 error is returned,
       If the user has the required role, the endpoint is called,
       Should be used as @role_required("role") where role is the required role,
       Can only be used on endpoints with JWT protection: @jwt_required'''
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_role = get_jwt().get("role", None)
            if current_role != required_role:
                return {"message": "Access forbidden: Requires role {}".format(required_role)}, 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
