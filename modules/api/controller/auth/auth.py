from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from api.controller.logic.user_logic import AdminUserLogic, ClientsAvailableBookingsLogic, ClientsPlansLogic, StaffUserLogic, UserLogic
from api.models.users import User
from api.controller.common import role_required


class Signup(Resource):
    DEFAULT_ROLE = 'user'
    ROLE_MAPPING = {
        'user': 'User',
        'staff' : 'Staff',
        'admin': 'Admin' 
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
        updated_data = request.json
        updated_user = self.user_logic.jwt_update_user_details(current_user['user_id'], username, updated_data)
        return {'message': f'Your details have been updated successfully', 'details': updated_user}, 200

    @jwt_required()
    @role_required('admin')
    def delete(self,id):
        current_user = get_jwt_identity()
        self.user_logic.delete_user(id)
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

class AdminSignup(Signup):
    DEFAULT_ROLE = 'admin'
    def __init__(self):
        super().__init__()
        self.resource = "admin"
        self.user_logic = AdminUserLogic(self.resource, self.user)

class AdminLogin(Login):
    def __init__(self):
        super().__init__()
        self.resource = "admin"
        self.user_logic = StaffUserLogic(self.resource, self.user)

class AdminAccount(Account):
    def __init__(self):
        super().__init__()
        self.resource = "admin"
        self.user_logic = StaffUserLogic(self.resource, self.user)

class StaffAmmendCoWorker(Resource):
    TYPE_OF_LIST = "coworkers"
    MY_ACTIONS= ["append", "remove"]

    def __init__(self):
        self.resource = "staff_users"
        self.user = User('', '') 
        self.user_logic = StaffUserLogic(self.resource, self.user)

    @jwt_required()
    @role_required('staff')
    def patch(self):
        
        current_user = get_jwt_identity()
        data_to_add = request.json
       
        updated_user = self.user_logic.action_user_list(current_user, data_to_add[self.TYPE_OF_LIST][0], self.MY_ACTIONS[0], self.TYPE_OF_LIST)
        return {'message': f'Your details have been updated successfully', 'details': updated_user}, 200

    @jwt_required()
    @role_required('staff')
    def delete(self):
        current_user = get_jwt_identity()
        data_to_add = request.json
       
        updated_user = self.user_logic.action_user_list(current_user, data_to_add[self.TYPE_OF_LIST][0], self.MY_ACTIONS[1], self.TYPE_OF_LIST)
        return {'message': f'Your details have been updated successfully', 'details': updated_user}, 200

class StaffAmmendClient(StaffAmmendCoWorker):
    TYPE_OF_LIST = "clients"

    def __init__(self):
        super().__init__()
        

class StaffAmmendClientsCredits(Resource):

    def __init__(self):
        self.resource = "staff_users"
        self.user = User('', '') 
        self.user_logic = StaffUserLogic(self.resource, self.user)
    
    @jwt_required()
    @role_required('staff')
    def patch(self, clientId,bookingId):# need to test
        credit_assignment = {'clientId': clientId, 'bookingId': bookingId}
        updated_user = self.user_logic.giveCredit(credit_assignment)
        return {'message': f'you have given a credit to {updated_user}'}, 200

class StaffAmmendClientsPlans(Resource):

    def __init__(self):
        self.resource = "staff_users"
        self.user = User('', '') 
        self.user_logic = StaffUserLogic(self.resource, self.user)
    
    @jwt_required()
    @role_required('staff')
    def patch(self, clientId, planId):# need to test
        plan_assignment = {'clientId': clientId, 'planId': planId}
        updated_user = self.user_logic.givePlan(plan_assignment)
        return {'message': f'you have given a credit to {updated_user}'}, 200
    
class StaffRetreiveAllClients(Resource):
    
    def __init__(self):
        self.resource = "staff_users"
        self.user = User('', '') 
        self.user_logic = StaffUserLogic(self.resource, self.user)

    @jwt_required()
    @role_required('staff')
    def get(self):
        response = self.user_logic.get_all_clients()
        return response

class Users(Resource):

    def __init__(self):
        self.resource = "users"
        self.user = User('', '') 
        self.user_logic = UserLogic(self.resource, self.user)

    @jwt_required()
    @role_required('staff', 'admin')
    def get(self):
        response = self.user_logic.get_all_users()
        return response
    
class NonClientUsers(Resource):

    def __init__(self):
        self.resource = "staff_users"
        self.user = User('', '') 
        self.logic = StaffUserLogic(self.resource, self.user)

    @jwt_required()
    @role_required('staff')
    def get(self):
        response = self.logic.get_all_non_clients()
        return response
    
class AllStaffMembersProtected(Resource):
    
    def __init__(self):
        self.resource = "staff_users"
        self.user = User('', '') 
        self.logic = StaffUserLogic(self.resource, self.user)

    def get(self):
        response = self.logic.get_all_staff_protected()
        return response

class ClientPlans(Resource):
    def __init__(self):
        self.resource = "users"
        self.user = User('', '') 
        self.user_logic = ClientsPlansLogic(self.resource, self.user)

    @jwt_required()
    @role_required('user')
    def get(self):
        response = self.user_logic.get()
        return response, 200
    
class ClientsAvailableBookings(Resource):
    def __init__(self):
        self.resource = "users"
        self.user = User('', '') 
        self.user_logic = ClientsAvailableBookingsLogic(self.resource, self.user)

    @jwt_required()
    @role_required('user')
    def get(self):
        response = self.user_logic.get()
        return response, 200

