from typing import Any, Dict
from copy import deepcopy
from deepmerge import always_merger
from flask_jwt_extended import get_jwt_identity
from api.error_handling import UnauthorizedException
from api.controller.logic.base_logic import BaseLogic
from api.schedule_resource_manager import ScheduleResourceManager

class ScheduleSubresourceLogic(BaseLogic):
    def __init__(self, resource, subresource):
        self.resource = resource
        self.subresource = subresource
        super().__init__(resource)
        #overwrite resource manager for scheduler resource manager
        self.resource_manager = ScheduleResourceManager(resource)


    def get(self, id: str = None, **kwargs):
        '''Could've called datastore directly from http request but use base logic for continuity'''
        resource = self._get_resource(id)
        services = self._get_services(resource)
        return services

    def patch(self, id: str, change_set: Dict[str, Any] = None, **kwargs):
        self._check_ownership(id)
        self._validate_request(change_set)
        update = self._wrap_subresouce_in_resource(id, change_set)
        response = self.resource_manager.update_resource(update, id)
        return response[self.subresource]

    def delete(self, id: str, **kwargs):
        self._check_ownership(id)
        update = self._wrap_subresouce_in_resource(id, None)
        response = self.resource_manager.update_resource(update, id)
        return response

    def _validate_request(self, data: Dict[str, Any], **kwargs):
        self._validate_json(data, **kwargs)

    def _validate_json(self, data: Dict[str, Any], **kwargs):
        ##Add all validation - schema + logic etc
        response = self.schema_validate.validate_request(self.resource, data, self.subresource)
        return response

    def _get_services(self, data: Dict[str, Any]) -> Any:
        if data.get(self.subresource) and data[self.subresource] is not None:
            return data[self.subresource]
        else:
            return None

    def _get_resource(self, id: str):
        return self.resource_manager.get_resource(id)

    def _wrap_subresouce_in_resource(self, id: str, data: Dict[str, Any], **kwargs):
        ''' We can't directly update a subresource so we grab the ensure resource
            make any changes programmatically and push the entire resource back in'''
        schedule_resource = self._get_resource(id)
        services_subresource = self._get_services(schedule_resource)

        existing_services = deepcopy(services_subresource)
        
        combined = always_merger.merge(existing_services, data) 
        schedule_resource[self.subresource] = combined

        return schedule_resource

    def _check_ownership(self, schedule_id: str):
        '''Check if user is owner of schedule'''
        current_user_id = get_jwt_identity()
        owned_weekly_schedules = self.resource_manager.get_by_user(current_user_id)
        
        owned_schedule_ids = [schedule['id'] for schedule in owned_weekly_schedules]
        if schedule_id not in owned_schedule_ids:
            raise UnauthorizedException('You are not authorized to edit this schedule')
