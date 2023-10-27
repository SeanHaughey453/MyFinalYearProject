from flask_restful import Resource, request, reqparse
from flask_jwt_extended import jwt_required

from common.logger import ScheduleLogger
from api.controller.common import role_required

from api.controller.logic.sub_logic.schedule_sub_logic import ScheduleSubresourceLogic 

class BaseSubResource(Resource):

    def __init__(self):
        self.resource = "schedule"
        self.subresource = "Filled in at Child Classes"
        self.logic = ScheduleSubresourceLogic(self.resource, self.subresource)

    def get(self, schedule_id: str):
        response = self.logic.get(schedule_id)
        return response, 200

    '''No Post request - Services initial post will be as part of the schedule resource, 
        if it's not provided at that stage service object will be defaulted to None, 
        so we can simply patch at this stage'''

    @jwt_required()
    @role_required('staff')
    def patch(self, schedule_id: str):
        response = self.logic.patch(schedule_id, request.json)
        return response, 200

    @jwt_required()
    @role_required('staff')
    def delete(self, schedule_id: str):
        response = self.logic.delete(schedule_id)
        return response, 204

class Day(BaseSubResource):
    def __init__(self):
        super().__init__()
        self.subresource = "day"

class Booking(BaseSubResource):
    def __init__(self):
        super().__init__()
        self.subresource = "booking"

class Break(BaseSubResource):
    def __init__(self):
        super().__init__()
        self.subresource = "break"

class Placeholder(BaseSubResource):
    def __init__(self):
        super().__init__()
        self.subresource = "placeholder"