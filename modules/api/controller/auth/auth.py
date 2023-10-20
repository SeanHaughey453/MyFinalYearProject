from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from api.controller.logic.user_logic import StaffUserLogic, UserLogic
from api.models.users import User


class Signup(Resource):
    DEFAULT_ROLE = 'user'
    ROLE_MAPPING = {
        'user': 'User',
        'staff' : 'Staff'
    }

    def __init__(self):
        self.resource = 'users'
        self.user = User(request.json.get('username'), request.json.get('password'))
        self.user.role = self._get_role()
        self.user_logic = UserLogic(self.resource, self.user)
    
    def _get_role(self):
        return request.json.get('role', self.DEFAULT_ROLE)
    
    def post(self):
        response = self.user_logic.create(request.json)
        created_user = response['username']
                # Use the mapping to get the human-readable role
        user_role_name = self.ROLE_MAPPING.get(self.user.role, 'Unknown')
        return {'message': f'{user_role_name} {created_user} created successfully'}, 201
    
class Login(Resource):
    def __init__(self):
        self.resource = "users"
        self.user = User(request.json.get('username'), request.json.get('password'))
        self.user_logic = UserLogic(self.resource, self.user)

    def post(self):
        access_token = self.user_logic.get()
        return {'access_token': access_token}, 200


class Account(Resource):
    def __init__(self):
        self.resource = "users"
        self.user = User('', '') 
        self.user_logic = UserLogic(self.resource, self.user)

    @jwt_required()
    def get(self, username: str):
        current_user = get_jwt_identity()
        current_user = self.user_logic.jwt_get_user_details(current_user['user_id'], username)
        return {'message': f'Hi, {current_user["username"]}!', 'details': current_user}, 200

    @jwt_required()
    def patch(self, username: str):
        current_user = get_jwt_identity()
        print('current_user_id', current_user)
        updated_data = request.json
        updated_user = self.user_logic.jwt_update_user_details(current_user['user_id'], username, updated_data)
        return {'message': f'Your details have been updated successfully', 'details': updated_user}, 200

    @jwt_required()
    def delete(self, username: str):
        current_user = get_jwt_identity()
        print(current_user)
        self.user_logic.jwt_delete_user(current_user['user_id'], username)
        return {'message': 'User deleted'}, 204

class StaffSignup(Signup):
    DEFAULT_ROLE = 'staff'
    def __init__(self):
        super().__init__()
        self.resource = "staff_users"
        self.user_logic = StaffUserLogic(self.resource, self.user)

class StaffLogin(Login):
    def __init__(self):
        super().__init__()
        self.resource = "staff_users"
        self.user_logic = StaffUserLogic(self.resource, self.user)

class StaffAccount(Account):
    def __init__(self):
        super().__init__()
        self.resource = "staff_users"
        self.user_logic = StaffUserLogic(self.resource, self.user)