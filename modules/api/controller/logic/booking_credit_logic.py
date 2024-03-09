from typing import Any, Dict

from flask_jwt_extended import jwt_required
from api.controller.common import role_required
from api.controller.logic.base_logic import BaseLogic
from api.resource_managers.booking_credit_resource_manager import BookingCreditRsrcManager


class BookingCreditLogic(BaseLogic):

    def __init__(self, resource):
        self.resource = resource
        super().__init__(resource)
        self.resource_manager = BookingCreditRsrcManager(resource)

    @jwt_required()
    @role_required('staff', 'admin')
    def get(self, id: str = None):
        response = self.resource_manager.get_rsrc(id)
        return response
    
    @jwt_required()
    @role_required('staff')
    def get_all_active(self):
        response = self.resource_manager.get_active_rsrcs()
        return response
    
    @jwt_required()
    @role_required('staff')
    def post(self, data: Any, **kwargs):
        data['active'] = True
        data['assigned'] = False
        self._validate_json(data, **kwargs)
        resource = data
        response = self.resource_manager.create_rsrc(resource)
        return response
     
    @jwt_required()
    @role_required('staff')
    def patch(self, schedule_id: str, change_set: Dict[str, Any], **kwargs):
        self._validate_json(change_set, **kwargs) 
        response = self.resource_manager.update_rsrc(change_set, schedule_id)
        return response
    
    @jwt_required()
    @role_required('staff', 'admin')
    def delete(self, schedule_id: str):
        response = self.resource_manager.delete_rsrc(schedule_id)
        return response 
        