from flask_restful import Resource, request,reqparse
from flask_jwt_extended import jwt_required
from api.controller.common import role_required

from api.controller.logic.schedule_logic import ModifyScheduleStaffLogic, ScheduleLogic
from api.controller.logic.booking_credit_logic import BookingCreditLogic


class BookingCredit(Resource):

    def __init__(self):
        self.resource = "booking_credit"
        self.logic = BookingCreditLogic(self.resource)

    def get(self, bookingCreditId: str):
        response = self.logic.get(bookingCreditId)
        return response, 200

    @jwt_required()
    @role_required('staff')
    def post(self):
        response = self.logic.post(request.json)
        return response, 201

    @jwt_required()
    @role_required('staff')
    def patch(self, bookingCreditId: str):
        response = self.logic.patch(bookingCreditId, request.json)
        return response, 200

    @jwt_required()
    @role_required('admin')
    def delete(self, bookingCreditId: str):
        response = self.logic.delete(bookingCreditId)
        return response, 204
    
    
class BookingCredits(Resource):
    def __init__(self):
        self.resource = "booking_credit"
        self.logic = BookingCreditLogic(self.resource)
    @jwt_required()
    @role_required('staff', 'admin')
    def get(self):
        response = self.logic.get()
        return response, 200
    
class ActiveBookingCredits(BookingCredits):

    @jwt_required()
    @role_required('staff')
    def get(self):
        response = self.logic.get_all_active()
        return response, 200
