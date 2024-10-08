import traceback
from typing import Any, Optional, Type, cast
from flask import current_app
from flask_restful import Api
from werkzeug.exceptions import HTTPException

class Scedule_API_Errors(list):
    def __init__(self, default_error=500):
        super().__init__()
        self.default_error = default_error
    
    def add_error(self, exception: Type[Exception], status_code: int):
        error = {"exception": exception, "status_code": status_code}
        super(Scedule_API_Errors, self).append(error)
    
    def get_default_error(self):
        return self.default_error

class Scedule_API(Api):
    def __init__(self, error_list: Optional["Scedule_API_Errors"] = None, *args, **kwargs) -> None:
        self.error_list = error_list
        super().__init__(*args, **kwargs)
    
    def check_errors(self, e: Exception):
        if self.error_list is not None:
            for error in self.error_list:
                if isinstance(e, error['exception']):
                    return error
        return None
    
    def handle_error(self, e: Exception):
        current_app.logger.error("Caught Exception: %s\n%s", str(e), traceback.format_exc())
        error = self.check_errors(e)

        if error is not None:
            return http_response(e, cast(int, error['status_code']))
        
        if isinstance(e, HTTPException):
            return http_response(e, e.code or 500)

        if self.error_list:
            return http_response(e, self.error_list.get_default_error())
        
        return http_response(e, 900)
    
def http_response(msg: Any, status_code: int):
        response = {"message": "{}".format(msg)}

        if hasattr(msg, 'error_list') and msg.error_list is not None:
            response['error_list'] = msg.error_list

        return response, status_code