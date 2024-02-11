from typing import Any, Dict

from flask_jwt_extended import get_jwt_identity
from api.controller.logic.base_logic import BaseLogic
from api.error_handling import GeneralException, InvalidCredentials, ResourceConflictException, ResourceNotFoundException, UnauthorizedException
from api.models.users import User
from api.user_rsrc_manager import StaffUserRsrcManager, UserRsrcManager
from api.resource_managers.booking_credit_resource_manager import BookingCreditRsrcManager
from api.resource_managers.plan_rsrc_manager import PlanRsrcManager


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
            self._init_default_values(data)#need to test
            if not data.get("role"):
                data["role"] = self.role
            data['trainer'] = ''
            response = self.rsrc_manager.create_rsrc(data)
            return response

        def get(self):
            response = self.rsrc_manager.verify_login(self.username, self.password)
            return response  

        def get_all_users(self):
            all_users = self.rsrc_manager.get_rsrc()
            for user in all_users:
                user.pop('password', None)
            return all_users      
        
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
        
        def _init_default_values(self, data: Dict[str, Any]):
            optionalKeys = ['bookingCredits', 'usedBookingCredits', 'assignedPlans']
            if data is not None:
                for key in optionalKeys:
                    if not data.get(key):
                        data[key] = []
            return data
        
class StaffUserLogic(UserLogic):
    def __init__(self, resource: str, user: User):
        super().__init__(resource, user)
        self.rsrc_manager = StaffUserRsrcManager(self.resource)
        self.client_rsrc_manager = UserRsrcManager('users')
        self.booking_rsrc_manager = BookingCreditRsrcManager('booking_credit')
        self.plan_rsrc_manager = PlanRsrcManager('plan')
        
    def _init_default_values(self, data: Dict[str, Any]):
        optionalKeys = ['coworkers', 'clients', 'ownedSchedules']
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
        client_change_set = {
            'trainer': ''
        }
        self._is_current_user(username, current_user_jwt['user_id'])
        current_user = self.rsrc_manager.get_rsrc(current_user_jwt['user_id'])#if these users dont exist the validation will be handled in get_rsrc()
        other_user = self.client_rsrc_manager.get_rsrc(other_user_id) if type_of_list == 'clients' \
            else self.rsrc_manager.get_rsrc(other_user_id)
        
        if action == 'append' and type_of_list == 'clients':
            if other_user['trainer'] != '':
                raise GeneralException('This client already has a trainer. You must remove them first')
            client_change_set['trainer'] = current_user['id']   

        if action == 'remove' and type_of_list == 'clients':
            client_change_set['trainer'] = ''

        #if these users dont exist the validation will be handled in get_rsrc()
        self._check_if_user_in_list(action, other_user['id'], current_user[type_of_list])
        self._check_if_user_canbe_coworker(other_user['role'], type_of_list)
        
        eval(a_or_r_from_current_user_str)
        change_set[type_of_list] = current_user[type_of_list]

        client_response = self.client_rsrc_manager.update_rsrc(client_change_set,other_user['id'] )
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
         
    def giveCredit(self, credit_assingment_json):
        current_user_jwt = get_jwt_identity()
        self._validate_give_credit(current_user_jwt, credit_assingment_json)
        current_user = self.rsrc_manager.get_rsrc(current_user_jwt['user_id'])

        if credit_assingment_json['clientId'] in current_user['clients']:
            change_set, booking_credit_change_set = {}, {}
            booking_credit = self.booking_rsrc_manager.get_rsrc(credit_assingment_json['bookingId'])#if the credit doesnt exisit it will be handled in get_rsrc()
            if booking_credit['assigned'] == True:
                raise ResourceConflictException('This Booking credit resource has already been assigned to somone')
            client = self.client_rsrc_manager.get_rsrc(credit_assingment_json['clientId'])
            client['bookingCredits'].append(booking_credit['id'])
            change_set['bookingCredits'] = client['bookingCredits']
            response = self.client_rsrc_manager.update_rsrc(change_set, credit_assingment_json['clientId'])
            booking_credit_change_set['assigned'] = True
            booking_credit = self.booking_rsrc_manager.update_rsrc(booking_credit_change_set, booking_credit['id'] )
            return response
        else:
            raise GeneralException('This client is not parts of your Client list!')
    
    def givePlan(self, plan_assignment_json):
        current_user_jwt = get_jwt_identity()
        self._validate_give_plan(current_user_jwt, plan_assignment_json)
        current_user = self.rsrc_manager.get_rsrc(current_user_jwt['user_id'])

        if plan_assignment_json['clientId'] in current_user['clients']:
            change_set = {}
            plan = self.plan_rsrc_manager.get_rsrc(plan_assignment_json['planId'])#if the credit doesnt exisit it will be handled in get_rsrc()
            client = self.client_rsrc_manager.get_rsrc(plan_assignment_json['clientId'])
            client['assignedPlans'].append(plan['id'])
            change_set['assignedPlans'] = client['assignedPlans']
            response = self.client_rsrc_manager.update_rsrc(change_set, plan_assignment_json['clientId'])
            return response
        else:
            raise GeneralException('This client is not parts of your Client list!')
        

    def _validate_give_credit(self, current_user_jwt, credit_assingment_json):
        if current_user_jwt == None or credit_assingment_json == None:
            raise ResourceNotFoundException('current user or the credit assignment was not found')
        if 'clientId' not in credit_assingment_json:
            raise ResourceNotFoundException('a client ID was not found in the credit assignment')
        if 'bookingId' not in credit_assingment_json:
            raise ResourceNotFoundException('a booking ID was not found in the credit assignment')
        
    def _validate_give_plan(self, current_user_jwt, plan_assignment_json):
        if current_user_jwt == None or plan_assignment_json == None:
            raise ResourceNotFoundException('current user or the credit assignment was not found')
        if 'clientId' not in plan_assignment_json:
            raise ResourceNotFoundException('a client ID was not found in the plan assignment')
        if 'planId' not in plan_assignment_json:
            raise ResourceNotFoundException('a plan ID was not found in the plan assignment')
    
    def get_all_clients(self):
        current_user_jwt = get_jwt_identity()
        print('current_user_jwt', current_user_jwt)
        current_user = self.rsrc_manager.get_rsrc(current_user_jwt['user_id'])
        print('current_user', current_user)
        client_list = self.client_rsrc_manager.get_clients_list(current_user['clients'])
 
        return client_list













        


