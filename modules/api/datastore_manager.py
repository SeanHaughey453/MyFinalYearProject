from typing import Any, Dict, List
from flask import current_app as app
from api.models.users import User
from common.logger import ScheduleLogger


class DatastoreManager:
    __slots__ = ("_logger", "_resource", "_collection_name", "_data_store_schedules", "_data_store_users", "_data_store_booking_credit", "_data_store_plan")

    def __init__(self, resource: str):

        self._resource = resource
        self._collection_name = self._resource
        self._logger = ScheduleLogger("Datastore Manager {}".format(self._resource))
        self._data_store_schedules = app.data_store_schedules
        self._data_store_users = app.data_store_users
        self._data_store_booking_credit = app.data_store_booking_credit
        self._data_store_plan = app.data_store_plan

        if self._resource == "staff_users":
            self._collection_name = "staff"
            self._data_store_users = app.data_store_staff
            self._resource = "users"
            
        if self._resource == "admin":
            self._collection_name = "admin"
            self._data_store_users = app.data_store_admin
            self._resource = "users"


        ###### GENERIC METHODS #######

    def get_all_from_resource(self):
        print('self.resource', self._resource)
        method_name = "get_all_from_resource_{}".format(self._resource)
        method = getattr(self, method_name)
        return method()
    
    def get_from_resource(self, id: str, key=None):
        method_name = "get_from_resource_{}".format(self._resource)
        method = getattr(self, method_name)
        return method(id)

    def post_resource(self, data: Dict[str, Any], id: str = None, **kwargs):
        method_name = "post_resource_{}".format(self._resource)
        method = getattr(self, method_name)
        return method(data, id, **kwargs)

    def patch_resource(self, data: Any, id: str = None, **kwargs):
        method_name = "patch_resource_{}".format(self._resource)
        method = getattr(self, method_name)
        return method(data, id, **kwargs)

    def delete_rsrc(self, id: str):
        method_name = "delete_rsrc_{}".format(self._resource)
        method = getattr(self, method_name)
        return method(id)

    def check_if_resource(self, id: str, key=None):
        method_name = "check_if_resource_{}".format(self._resource)
        method = getattr(self, method_name)
        return method(id)
    
    ######## USER METHODS ######
    def get_from_resource_users(self, id: str):
        resource = self._data_store_users.get_item(id)
        return resource

    def get_from_resource_staff_users(self, id: str):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        resource = self._data_store_users.get_item(id)
        return resource 
    
    def get_all_from_resource_users(self):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        resource = self._data_store_users.get_all()
        return resource
    
    def get_all_from_resource_staff_users(self):
        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        resource = self._data_store_users.get_all()
        return resource
    
    def post_resource_users(self, data: Dict[str, Any], id: str = None, **kwargs):
        resource = self._data_store_users.overwrite(data["id"], data)
        return resource
    
    def patch_resource_users(self, data: Dict[str, Any], user_id: str, **kwargs):
        resource = self._data_store_users.patch_item(user_id, data)
        return resource

    def delete_rsrc_users(self, id: str, **kwargs):
        resource = self._data_store_users.delete_item(id)
        return resource

    def check_username_available(self, username: str):
        return self._data_store_users._collection.fetchFirstExample({'username': username})

    def find_by_username(self, username: str):
        query = 'FOR u IN {collection} FILTER u.username == @username RETURN u'.format(collection=self._collection_name)
        cursor = self._data_store_users._db.AQLQuery(query, bindVars={'username': username})
        results = list(cursor)
        if len(results) == 0:
            return None
        user = results[0]
        return User(username=user['username'], password=user['password'], role=user['role'], _id=user['id'],firstname=user['firstName'],surname=user['surname'],email=user['email'], )
    
    def get_user_list(self, ids: List[str] ):

        if not ids:
            raise ValueError("The 'ids' parameter is empty.")
        
        #ids_str = ', '.join(f"'{id}'" for id in ids)
        query = f'''FOR u IN users
                   FILTER u.id IN @ids
                   RETURN {{"username": u.username, "email": u.email, "id": u.id, goals: u.goals}}
                '''
        return self._data_store_users.run_query(query, bindVars={"ids": ids})

###### SCHEDULE METHODS #####
    def get_from_resource_schedule(self, id: str):
        resource = self._data_store_schedules.get_item(id)
        return resource

    def get_all_from_resource_schedule(self):
        resource = self._data_store_schedules.get_all()
        return resource

    def get_active_schedules_by_user(self, id: str):
        #resource = self._data_store_schedules.get_all()
        #returns the list of all active schedules
        query = f"""
                FOR s IN {self._collection_name}
                FILTER s.active == true && s.createdBy == "{id}"
                RETURN s
                """
        return self._data_store_schedules.run_query(query) #resource

    def get_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetches all documents in the collection owned by the given user_id."""
        query = f"""
                FOR s IN {self._collection_name}
                FILTER s.createdBy == "{user_id}"
                RETURN s
                """
        return self._data_store_schedules.run_query(query)
    
    def get_by_username(self, username: str):#
        query = 'FOR u IN {collection} FILTER u.username == @username RETURN u'.format(collection=self._collection_name)
        cursor = self._data_store_users._db.AQLQuery(query, bindVars={'username': username})
        results = list(cursor)
        if len(results) == 0:
            return None
        user = results[0]
        return {'user_id': str(user['id']), 'username': str(user['username'])}#only returns userid and username for now because the only thing we need it for is adding a new staff member to a schedule

    def post_resource_schedule(self, data: Dict[str, Any], id: str = None, **kwargs):
        resource = self._data_store_schedules.overwrite(data["id"], data)
        return resource

    def patch_resource_schedule(self, data: Any, id: str = None, **kwargs):
        resource = self._data_store_schedules.patch_item(id, data)
        return resource

    def delete_rsrc_schedule(self, id: str, **kwargs):
        resource = self._data_store_schedules.delete_item(id)
        return resource

    def check_if_resource_schedule(self, schedule_id: str, **kwargs):
        resource = self._data_store_schedules.check_existance(schedule_id)
        return resource
    
    def put_rsrc_schedule(self, data: Any, id: str, **kwargs):
        resource = self._data_store_schedules.put_item(id, data)
        return resource
    
    ##############BOOKING CREDIT METHODS#############################

    def get_from_resource_booking_credit(self, id: str):
        resource = self._data_store_booking_credit.get_item(id)
        return resource

    def get_all_from_resource_booking_credit(self, id = None):
        resource = self._data_store_booking_credit.get_all()
        return resource
    
    def get_all_active_booking_credit(self):
        query = f"""FOR b in {self._collection_name}
                    FILTER b.active == true && b.assigned == false
                    return b
                """
        return self._data_store_booking_credit.run_query(query)
    
    def post_resource_booking_credit(self, data: Dict[str, Any], id: str = None, **kwargs):
        resource = self._data_store_booking_credit.overwrite(data["id"], data)
        return resource

    def patch_resource_booking_credit(self, data: Any, id: str = None, **kwargs):
        resource = self._data_store_booking_credit.patch_item(id, data)
        return resource

    def delete_rsrc_booking_credit(self, id: str, **kwargs):
        resource = self._data_store_booking_credit.delete_item(id)
        return resource

    def check_if_resource_booking_credit(self, schedule_id: str, **kwargs):
        resource = self._data_store_booking_credit.check_existance(schedule_id)
        return resource
    
        ##############PLAN METHODS#############################

    def get_from_resource_plan(self, id: str):
        resource = self._data_store_plan.get_item(id)
        return resource

    def get_all_from_resource_plan(self):
        resource = self._data_store_plan.get_all()
        return resource
    
    def get_list_from_resource_plan(self, ids: List[str] ):
        if not ids:
            raise ValueError("The 'ids' parameter is empty.")
        
        query = f'''FOR p IN plan
                   FILTER p.id IN @ids
                   RETURN p
                '''
        return self._data_store_plan.run_query(query, bindVars={"ids": ids})
    
    def post_resource_plan(self, data: Dict[str, Any], id: str = None, **kwargs):
        resource = self._data_store_plan.overwrite(data["id"], data)
        return resource

    def patch_resource_plan(self, data: Any, id: str = None, **kwargs):
        resource = self._data_store_plan.patch_item(id, data)
        return resource

    def delete_rsrc_plan(self, id: str, **kwargs):
        resource = self._data_store_plan.delete_item(id)
        return resource

    def check_if_resource_plan(self, schedule_id: str, **kwargs):
        resource = self._data_store_plan.check_existance(schedule_id)
        return resource
    

