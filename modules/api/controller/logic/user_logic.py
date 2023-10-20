from typing import Any, Dict
from api.controller.logic.base_logic import BaseLogic
from api.error_handling import InvalidCredentials
from api.models.users import User
from api.user_rsrc_manager import StaffUserRsrcManager, UserRsrcManager


class UserLogic(BaseLogic):
        def __init__(self, resource: str, user: User):
            self.resource = resource
            self.username = user.username
            self.password = user.password
            self._id = user._id
            self.role = user.role
            super().__init__(resource)
            self.rsrc_manager = UserRsrcManager(self.resource)

        def create(self, data):
            self._validate_json(data) 
            if not data.get("role"):
                data["role"] = self.role
            response = self.rsrc_manager.create_rsrc(data)
            return response

        def get(self):
            response = self.rsrc_manager.verify_login(self.username, self.password)
            return response        
        
        def jwt_get_user_details(self, user_id: str, username: str):
            #When already jwt verfiied
            if not self.check_matching_id_and_username(username, user_id):
                raise InvalidCredentials('User details do not match this account')
            response = self.rsrc_manager.get_rsrc(user_id)
            return response

        def jwt_update_user_details(self, user_id: str, username: str, data: Dict[str, Any]):
            if not self.check_matching_id_and_username(username, user_id):
                raise InvalidCredentials('User details do not match this account')
            self._validate_json(data)
            response = self.rsrc_manager.update_rsrc(data, user_id)
            return response

        def jwt_delete_user(self, user_id: str, username: str):
            if not self.check_matching_id_and_username(username, user_id):
                raise InvalidCredentials('User details do not match this account')
            response = self.rsrc_manager.delete_rsrc(user_id)
            return response

        def check_matching_id_and_username(self, username: str, user_id: str) -> bool:
            print('user_id', user_id)
            user = self.rsrc_manager.get_rsrc(user_id)
            if user.get('id') == user_id and user.get('username') == username:
                return True
            return False
        
class StaffUserLogic(UserLogic):
    def __init__(self, resource: str, user: User):
        super().__init__(resource, user)
        self.resource_manager = StaffUserRsrcManager(self.resource)
        
    def _init_default_values(self, data: Dict[str, Any]):
        optionalKeys = ['coworker', 'clients']
        if data is not None:
            for key in optionalKeys:
                if not data.get(key):
                   data[key] = []
        return data

    def create(self, data):
        self._validate_json(data) 
        self._init_default_values(data)
        if not data.get("role"):
            data["role"] = self.role
        response = self.rsrc_manager.create_rsrc(data)
        return response
