from flask_jwt_extended import create_access_token
from api.error_handling import InvalidCredentials, ResourceConflictException, ResourceNotFoundException
from api.models.users import User
from api.rsrc_manager import ResourceManager
from flask import current_app as app

from werkzeug.security import generate_password_hash, check_password_hash

class UserRsrcManager(ResourceManager):
    def __init__(self, resource: str):
        self._resource = resource
        self.data_store = app.data_store_users
        super().__init__(resource)
    
    def create_rsrc(self, json, id: str = None):
        if self._data_manager.check_username_available(json['username']):
            raise ResourceConflictException('username already taken')
        hashed_pswrd = generate_password_hash(json['password'])
        json['password'] = hashed_pswrd
        return super().create_rsrc(json)

    def get_rsrc(self, id: str):
        response = self._data_manager.get_from_resource(id)
        return response
    
    def update_rsrc(self, json, id):
        return super().update_rsrc(json, id)
    
    def delete_rsrc(self, id):
        return super().delete_rsrc(id)
    
    def verify_login(self, username: str, password: str):
        user = self._get_login_details(username)
        if not user:
            raise ResourceNotFoundException("User not found")
        return self._get_access_token(user, password)
    
    def _get_login_details(self, username: str):
        #returns user object
        user = self._data_manager.find_by_username(username)
        self._logger.info("User login details: {}".format(user))
        return user     

    def _get_access_token(self, user: User, raw_password: str):
        if user and check_password_hash(user.password, raw_password):
            role_claims = {"role": user.role}
            self._logger.info("User role: {}".format(role_claims))
            identity_data = {
                'user_id': user._id,
                'username': user.username
            }
            access_token = create_access_token(identity=identity_data, additional_claims=role_claims)
            return access_token
        raise InvalidCredentials("The provided login details were not valid")   
    
class StaffUserRsrcManager(UserRsrcManager):
    def __init__(self, resource:str):
        super().__init__(resource)
        self.data_store = app.data_store_staff
