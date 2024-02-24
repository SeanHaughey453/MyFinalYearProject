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
        new_temp = templates.schedule_template
        response = self.logic.post(new_temp)
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

class templates():

    schedule_template={
    "monday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                },
    "tuesday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                },
    "wednesday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                },
    "thursday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                },
    "friday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                },
    "saturday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                },
    "sunday": {
        
            "0800":{
                "placeholder": "placeholder"
            },
            "0900":{
                "placeholder": "placeholder"
            },
            "1000":{
                "placeholder": "placeholder"
                },
            "1100":{
                "placeholder": "placeholder"
                }, 
            "1200":{
                "placeholder": "placeholder"
                }, 
            "1300":{
                "placeholder": "placeholder"
                }, 
            "1400":{
                "placeholder": "placeholder"
                }, 
            "1500":{
                "placeholder": "placeholder"
            }, 
            "1600":{
                "placeholder": "placeholder"
                }, 
            "1700":{
                "placeholder": "placeholder"
                }, 
            "1800":{
                "placeholder": "placeholder"
                }
                }
}
