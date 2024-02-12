from flask_restful import Resource, request,reqparse
from flask_jwt_extended import jwt_required
from api.controller.common import role_required
from api.controller.logic.plan_logic import PlanLogic

class Plan(Resource):

    def __init__(self):
        self.resource = "plan"
        self.logic = PlanLogic(self.resource)

    def get(self, planId: str = None):
        response = self.logic.get(planId)
        return response, 200

    @jwt_required()
    @role_required('staff')
    def post(self):
        response = self.logic.post(request.json)
        return response, 201

    @jwt_required()
    @role_required('staff')
    def patch(self, planId: str):
        response = self.logic.patch(planId, request.json)
        return response, 200

    @jwt_required()
    @role_required('staff')
    def delete(self, planId: str):
        response = self.logic.delete(planId)
        return response, 204
    
    
class Plans(Resource):
    def __init__(self):
        self.resource = "plan"
        self.logic = PlanLogic(self.resource)

    @jwt_required()
    @role_required('staff')
    def get(self):
        response = self.logic.get()
        return response, 200
    
# class Plans(Resource):
#     def __init__(self):
#         self.resource = "booking_credit"
#         self.logic = Plan(self.resource)
        
#     @jwt_required()
#     @role_required('staff')
#     def get(self):
#         response = self.logic.get()
#         return response, 200
