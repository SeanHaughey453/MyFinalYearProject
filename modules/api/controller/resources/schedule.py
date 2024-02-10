from flask_restful import Resource, request,reqparse
from flask_jwt_extended import jwt_required
from api.controller.common import role_required

from api.controller.logic.schedule_logic import ModifyScheduleStaffLogic, ScheduleLogic


class Schedule(Resource):

    def __init__(self):
        self.resource = "schedule"
        self.logic = ScheduleLogic(self.resource)
    
    @jwt_required()
    def get(self, scheduleId: str):
        response = self.logic.get(scheduleId)
        return response, 200

    @jwt_required()
    @role_required('staff')
    def post(self):
        response = self.logic.post(request.json)
        return response, 201

    @jwt_required()
    @role_required('staff')
    def patch(self, scheduleId: str):
        response = self.logic.patch(scheduleId, request.json)
        return response, 200

    @jwt_required()
    @role_required('staff')
    def delete(self, scheduleId: str):
        response = self.logic.delete(scheduleId)
        return response, 204
    
class ModifyScheduleStaff(Schedule):

    def __init__(self):
        super().__init__()
        self.logic = ModifyScheduleStaffLogic(self.resource)
    
    @jwt_required()
    @role_required('staff')
    def patch(self, scheduleId: str):
        print('scheduleId', scheduleId)
        print('request.json', request.json)
        response = self.logic.add_staff_to_schedule(request.json, scheduleId)
        return response
    
    @jwt_required()
    @role_required('staff')
    def delete(self, scheduleId: str):
        response = self.logic.delete_staff_from_schedule(scheduleId)
        return response, 204
    
class Schedules(Resource):
    def __init__(self):
        self.resource = "schedule"
        self.logic = ScheduleLogic(self.resource)
    @jwt_required()
    def get(self):
        response = self.logic.get_dashboard_data()
        return response, 200
    
