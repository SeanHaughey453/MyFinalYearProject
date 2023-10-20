

from typing import Any, Dict
from flask_jwt_extended import get_jwt_identity
from api.controller.logic.base_logic import BaseLogic
from api.error_handling import ResourceConflictException, ResourceNotFoundException, UnauthorizedException
from api.schedule_resource_manager import ScheduleResourceManager


class ScheduleLogic(BaseLogic):
    def __init__(self, resource):
        self.resource = resource
        super().__init__(resource)
        self.resource_manager = ScheduleResourceManager(resource)

    def get(self, id: str = None):
        response = self.resource_manager.get_rsrc(id)
        return response
    
    def post(self, data: Any, **kwargs):
        self._validate_json(data, **kwargs)
        resource = self._init_default_values(data)
        current_user = get_jwt_identity()
        resource['staff_ids'] = [current_user]
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
        my_current_schedule = self.resource_manager.get_rsrc(schedule_id)
        if current_user not in my_current_schedule['staff_ids']:
            raise UnauthorizedException('You are not authorized to edit this schedule')
        

class ModifyScheduleStaffLogic(ScheduleLogic):

    def __init__(self, resource):
        super().__init__(resource)

    def add_staff_to_schedule(self, change_set, schedule_id):#need to test
        self._check_ownership(schedule_id)
        self._check_add_staff(change_set)
        my_current_schedule = self.resource_manager.get_rsrc(schedule_id)
        user_to_add_json = self.resource_manager.get_by_username(change_set["addusername"])
        if user_to_add_json is not None:
            my_current_schedule['staff_ids'].append(user_to_add_json)
        response = self.resource_manager.update_rsrc(my_current_schedule['staff_ids'], schedule_id)
        return response
    
    def delete_staff_from_schedule(self, change_set, schedule_id):
        pass
    
    
        
    def _check_add_staff(self, change_set: dict):
        expected_key = {"addusername"}
        extra_keys = set(change_set.keys()) - expected_key
        if extra_keys:
            raise ResourceConflictException('There should not be extra keys in the data when adding staff to a Schedule')
        if 'addusername' not in change_set:
            raise ResourceNotFoundException('No add username parameter was found when adding staff to a schedule')