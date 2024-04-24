from typing import Any, Dict

from flask_jwt_extended import jwt_required
from api.controller.common import role_required
from api.controller.logic.base_logic import BaseLogic
from api.resource_managers.booking_credit_rsrc_manager import BookingCreditRsrcManager
from api.resource_managers.plan_rsrc_manager import PlanRsrcManager


class PlanLogic(BaseLogic):

    def __init__(self, resource):
        self.resource = resource
        super().__init__(resource)
        self.resource_manager = PlanRsrcManager(resource)

    @jwt_required()
    def get(self, id: str = None):
        response = self.resource_manager.get_rsrc(id)
        return response
    
    @jwt_required()
    @role_required('staff')
    def post(self, data: Any, **kwargs):
        self._validate_json(data, **kwargs)
        resource = data
        response = self.resource_manager.create_rsrc(resource)
        return response
     
    @jwt_required()
    @role_required('staff')
    def patch(self, plan_id: str, change_set: Dict[str, Any], **kwargs):
        self._validate_json(change_set, **kwargs) 
        response = self.resource_manager.update_rsrc(change_set, plan_id)
        return response
    
    @jwt_required()
    @role_required('staff')
    def delete(self, plan_id: str):
        response = self.resource_manager.delete_rsrc(plan_id)
        return response 
    
        