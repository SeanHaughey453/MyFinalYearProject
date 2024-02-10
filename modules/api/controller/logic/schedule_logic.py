

from typing import Any, Dict
from flask_jwt_extended import get_jwt_identity
from api.controller.logic.base_logic import BaseLogic
from api.error_handling import ResourceConflictException, ResourceNotFoundException, UnauthorizedException
from api.schedule_resource_manager import ScheduleResourceManager
from api.user_rsrc_manager import StaffUserRsrcManager, UserRsrcManager


class ScheduleLogic(BaseLogic):
    def __init__(self, resource):
        self.resource = resource
        super().__init__(resource)
        self.resource_manager = ScheduleResourceManager(resource)
        self.staff_rsrc_mngr = StaffUserRsrcManager('staff_users')
        self.user_rsrc_mngr = UserRsrcManager('users')

    def get(self, id: str = None):
        current_user = get_jwt_identity()
        resource = self.resource_manager.get_rsrc(id)
        owner = self.staff_rsrc_mngr.get_rsrc(resource['createdBy'])
        if current_user['role'] == 'staff':
            if current_user['user_id'] != resource['createdBy']:
                if current_user['user_id'] not in owner['coworkers']:
                    raise UnauthorizedException('This staff memeber is not a coworker with the schedule owner')
            return resource
        else:
            if current_user['user_id'] not in owner['clients']:
                raise UnauthorizedException('This user is not a client of the schedule owner')
            return self._hide_other_client_bookings(resource, current_user)
    
    def get_dashboard_data(self):
        current_user_jwt = get_jwt_identity()
        current_user = self.staff_rsrc_mngr.get_rsrc(current_user_jwt['user_id']) if current_user_jwt['role']== 'staff' else self.user_rsrc_mngr.get_rsrc(current_user_jwt['user_id'])

        if current_user_jwt['role'] == 'staff':
            resources = self.resource_manager.get_by_user(current_user['id'])
        else:
            if current_user['trainer'] != '':
                resources = self.resource_manager.get_active_schedule(current_user['trainer'])
        return resources



    def post(self, data: Any, **kwargs):
        self._validate_json(data, **kwargs)
        resource = self._init_default_values(data)
        current_user = get_jwt_identity()
        staff_ids = self._get_list_of_coworkers(current_user['user_id'])
        staff_ids.append(current_user['user_id'])
        resource['staff_ids'] = staff_ids
        resource['createdBy'] = current_user['user_id']
        resource['active'] = True
        response = self.resource_manager.create_rsrc(resource)
        self._update_owner_data(current_user['user_id'], response['id'] )
        return response
     
    def patch(self, schedule_id: str, change_set: Dict[str, Any], **kwargs):
        self._check_ownership(schedule_id)
        self._validate_json(change_set, **kwargs) 
        response = self.resource_manager.update_rsrc(change_set, schedule_id)
        return response
    
    def delete(self, schedule_id: str):
        self._check_ownership(schedule_id)
        response = self.resource_manager.delete_rsrc(schedule_id)
        return response
    
    def _init_default_values(self, data: Dict[str, Any]):
        optionalKeys = []
        if data is not None:
            for key in optionalKeys:
                if not data.get(key):
                    data[key] = None
        return data

    def _check_ownership(self, schedule_id: str):
        '''check if user is staff of the schedule'''
        current_user = get_jwt_identity()
        print('current user', current_user)
        
        my_current_schedule = self.resource_manager.get_rsrc(schedule_id)
        print("my_current_schedule['staff_ids']", my_current_schedule['staff_ids'])
        if current_user['user_id'] not in my_current_schedule['staff_ids']:
            raise UnauthorizedException('You are not authorized to edit this schedule')
        
    def _get_list_of_coworkers(self, current_user_id :str):
        user = self.staff_rsrc_mngr.get_rsrc(current_user_id)
        return user['coworkers']

    def _hide_other_client_bookings(self, resource: Dict[str, Any], user:Dict[str, Any]):
            weekdays= ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

            for weekday in resource.keys():
                if weekday in weekdays:
                    for hour in resource[weekday].keys():
                        if 'user_id' in resource[weekday][hour]:
                            if resource[weekday][hour]['user_id'] != user['user_id']:
                                resource[weekday][hour] = {'booked': 'booked'}
            return resource
    
    def _update_owner_data(self,user_id, schedule_id ):
#this works aslong as the list(being seen a stack) for the owner/staff resource stays in the same order, if i needed to change the order of the list then it will wreck
# this could change through targetiong the arango save function so REMEBER this if i do need to target save instead of patch as it could change
        owner = self.staff_rsrc_mngr.get_rsrc(user_id)
        changeset_owner = {}
        changeset_schedule = {}
        previous_schedules = owner['ownedSchedules'].copy()
        if previous_schedules != []:
            previous_schedule_id = previous_schedules.pop()
            previous_schedule = self.resource_manager.get_rsrc(previous_schedule_id)
            previous_schedule['active'] = False
            changeset_schedule['active'] = previous_schedule['active']
            updated_previous_schedule = self.resource_manager.update_rsrc(previous_schedule, previous_schedule_id)
        owner['ownedSchedules'].append(schedule_id)
        changeset_owner['ownedSchedules'] = owner['ownedSchedules']
        updated_owner = self.staff_rsrc_mngr.update_rsrc(changeset_owner, user_id)


        

class ModifyScheduleStaffLogic(ScheduleLogic):

    def __init__(self, resource):
        super().__init__(resource)

    def add_staff_to_schedule(self, user_id_json, schedule_id):#need to test
        change_set = {"staff_ids": []}
        self._check_ownership(schedule_id)
        self._check_add_staff(user_id_json)
        my_current_schedule = self.resource_manager.get_rsrc(schedule_id)
        user_to_add_json = self.staff_rsrc_mngr.get_rsrc(user_id_json['adduserid'])
        if user_to_add_json is None:
            raise ResourceNotFoundException('this user does not exist')
        my_current_schedule['staff_ids'].append(user_to_add_json['id'])
        change_set['staff_ids'].append( my_current_schedule['staff_ids'])
        response = self.resource_manager.update_rsrc(change_set, schedule_id)
        return response
    
    def delete_staff_from_schedule(self, change_set, schedule_id):
        pass
    
    
        
    def _check_add_staff(self, change_set: dict):

        expected_key = {"adduserid"}
        print('change_set',change_set)
        extra_keys = set(change_set.keys()) - expected_key
        if extra_keys:
            raise ResourceConflictException('There should not be extra keys in the data when adding staff to a Schedule')
        if 'adduserid' not in change_set:
            raise ResourceNotFoundException('No add user id parameter was found when adding staff to a schedule')
        
