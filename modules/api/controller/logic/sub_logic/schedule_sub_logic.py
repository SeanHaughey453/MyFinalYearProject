from typing import Any, Dict
from copy import deepcopy
from deepmerge import always_merger
from flask_jwt_extended import get_jwt_identity
from api.error_handling import ResourceConflictException, UnauthorizedException
from api.controller.logic.base_logic import BaseLogic
from api.schedule_resource_manager import ScheduleResourceManager
from api.user_rsrc_manager import StaffUserRsrcManager, UserRsrcManager
from api.resource_managers.booking_credit_resource_manager import BookingCreditRsrcManager

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
        return self.resource_manager.get_rsrc(id)

    def _wrap_subresouce_in_resource(self, id: str, day:str ,hour:str , data: Dict[str, Any], **kwargs):

        schedule_resource = self._get_resource(id)
        schedule_resource[day][hour] = {}
        schedule_resource[day][hour] = data
        return schedule_resource

    def _check_ownership(self, schedule_id: str):
        '''Check if user is owner of schedule'''
        current_user = get_jwt_identity()
        owned_weekly_schedules = self.resource_manager.get_by_user(current_user['user_id'])
        
        owned_schedule_ids = [schedule['id'] for schedule in owned_weekly_schedules]
        if schedule_id not in owned_schedule_ids:
            raise UnauthorizedException('You are not authorized to edit this schedule')

class SubBookingSubresourceLogic(ScheduleSubresourceLogic):

    def __init__(self, resource, subresource):
        super().__init__(resource, subresource)
        self.user_rsrc_manager = UserRsrcManager('users')
        self.staff_rsrc_manager = StaffUserRsrcManager('staff_users')
        self.booking_credit_rsrc_manager = BookingCreditRsrcManager('booking_credit')
        
    def patch(self, id: str, day: str, hour: str, change_set: Dict[str, Any] = None):
        schedule_slot = {'id': id, 'day': day, 'hour': hour, 'change_set': change_set}
        self._validate_request(change_set) if change_set != {} else None
        schedule_resource,current_user_jwt = self._get_resource(id), get_jwt_identity()
        current_user, schedule_owner = self.user_rsrc_manager.get_rsrc(current_user_jwt['user_id']), self.staff_rsrc_manager.get_rsrc(schedule_resource['createdBy'])
        self.add_booking_validation(current_user, schedule_owner['clients'], schedule_resource ,schedule_slot )
        
        return self.process_booking_from_client(schedule_resource, current_user, schedule_slot)
    
    def process_booking_from_client(self, schedule_resource, current_user, schedule_slot):
        response_list = []
        change_set = schedule_slot['change_set']
        current_credit_id = current_user['bookingCredits'].pop()
        current_credit = self.booking_credit_rsrc_manager.get_rsrc(current_credit_id)
        current_credit['active'] = False
        current_user['usedBookingCredits'].append(current_credit_id)

        response_list.append(self.user_rsrc_manager.update_rsrc(current_user,current_user['id']))
        response_list.append(self.booking_credit_rsrc_manager.update_rsrc(current_credit, current_credit_id))

        change_set['user_id'],change_set['name'] = current_user['id'], current_user['username']
        update = self._wrap_subresouce_in_resource(schedule_slot['day'] ,schedule_slot['hour'], change_set, schedule_resource)
        response_list.append(self.resource_manager.update_full_rsrc(update, schedule_slot['id']))
        return response_list
    
    def add_booking_validation(self,current_user,schedule_owner_lists, schedule_resource, schedule_slot):
        day, hour = schedule_slot['day'], schedule_slot['hour']
        if current_user['id'] not in schedule_owner_lists:
            raise UnauthorizedException('This client is not authorized to book into this schedule')
        
        if current_user['bookingCredits'] == []:
            raise UnauthorizedException('You have insuffecent credits to book')
        
        if 'user_id' in schedule_resource[day][hour] or 'name' in schedule_resource[day][hour]:
            raise ResourceConflictException('This booking has already been taken')
        
    def _wrap_subresouce_in_resource(self, day:str ,hour:str , data: Dict[str, Any], schedule_resource:Dict[str,Any], **kwargs):
        '''we needed to overwrite this function to prevent duplicate calls to the schedule resource'''
        schedule_resource[day][hour] = {}
        schedule_resource[day][hour] = data
        return schedule_resource
