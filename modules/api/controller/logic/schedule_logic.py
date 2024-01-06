

from typing import Any, Dict
from flask_jwt_extended import get_jwt_identity
from api.controller.logic.base_logic import BaseLogic
from api.error_handling import ResourceConflictException, ResourceNotFoundException, UnauthorizedException
from api.schedule_resource_manager import ScheduleResourceManager
from api.user_rsrc_manager import StaffUserRsrcManager


class ScheduleLogic(BaseLogic):
    def __init__(self, resource):
        self.resource = resource
        super().__init__(resource)
        self.resource_manager = ScheduleResourceManager(resource)
        self.staff_rsrc_mngr = StaffUserRsrcManager('staff_users')

    def get(self, id: str = None):
        response = self.resource_manager.get_rsrc(id)
        return response
    
    def post(self, data: Any, **kwargs):
        self._validate_json(data, **kwargs)
        resource = self._init_default_values(data)
        current_user = get_jwt_identity()
        staff_ids = self._get_list_of_coworkers(current_user['user_id'])
        staff_ids.append(current_user['user_id'])
        resource['staff_ids'] = staff_ids
        response = self.resource_manager.create_rsrc(resource)
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