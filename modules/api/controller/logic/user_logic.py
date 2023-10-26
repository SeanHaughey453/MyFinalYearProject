from typing import Any, Dict
from api.controller.logic.base_logic import BaseLogic
from api.error_handling import InvalidCredentials, ResourceConflictException, ResourceNotFoundException, UnauthorizedException
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
            user = self.rsrc_manager.get_rsrc(user_id)
            if user.get('id') == user_id and user.get('username') == username:
                return True
            return False
        
class StaffUserLogic(UserLogic):
    def __init__(self, resource: str, user: User):
        super().__init__(resource, user)
        self.rsrc_manager = StaffUserRsrcManager(self.resource)
        self.client_rsrc_manager = UserRsrcManager('users')
        
    def _init_default_values(self, data: Dict[str, Any]):
        optionalKeys = ['coworkers', 'clients']
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
    
    def action_user_list(self, current_user_jwt, username, other_user_id, action, type_of_list ):
        ''' this is a fairly complicated function it handles 4 different endpoints and deals with them all 
            dynamically and reuses code
            
            a_or_r_from_current_user_str stores the executions that will be getting called inside the eval() function
            it also formats the variables used within it to handle the type of list (client or coworker) 
            
            because of how i have built out the resource managers to get the client resource i then needed to target the
            user resource manager as oppose to staff one which i have defined both in __init__

            can be used for both StaffAmmendClient and StaffAmmendCoWorker classes

            NOTE TO SELF - i used eval because when i tried using get_attr it bombed out
              as get_attr searches at a class level
            '''
        
        a_or_r_from_current_user_str = f"current_user['{type_of_list}'].{action}(other_user['id'])"
        change_set = {type_of_list: None}
        self._is_current_user(username, current_user_jwt['user_id'])
        current_user = self.rsrc_manager.get_rsrc(current_user_jwt['user_id'])#if these users dont exist the validation will be handled in get_rsrc()
        other_user = self.client_rsrc_manager.get_rsrc(other_user_id) if type_of_list == 'clients' \
            else self.rsrc_manager.get_rsrc(other_user_id)
        #if these users dont exist the validation will be handled in get_rsrc()
        self._check_if_user_in_list(action, other_user['id'], current_user[type_of_list])
        self._check_if_user_canbe_coworker(other_user['role'], type_of_list)
        
        eval(a_or_r_from_current_user_str)
        change_set[type_of_list] = current_user[type_of_list]
        response = self.rsrc_manager.update_rsrc(change_set, current_user['id'])
        return response
    
    def _is_current_user(self, username, current_user_id):
        if not self.check_matching_id_and_username(username,current_user_id):
            raise InvalidCredentials('User details do not match this account')
        
    def _check_if_user_in_list(self, action, other_user_id, list_of_users):
        if action == 'append' and other_user_id in list_of_users:
           raise ResourceConflictException('this user is already in the list')
        
    def _check_if_user_canbe_coworker(self, other_user_id, type_of_list):
         if other_user_id != 'staff' and type_of_list == 'coworkers':
            raise UnauthorizedException('This user is not authorised to become a coworker')

        


