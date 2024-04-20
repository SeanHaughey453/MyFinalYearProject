from typing import Any, Dict
from api.datastore_manager import DatastoreManager
from common.logger import ScheduleLogger
import uuid



class ResourceManager:
    '''Abstraction layer, to make any changes to resource after http request and validation but before saving data'''
    __slots__ = ("_logger", "_data_manager", "_resource")

    def __init__(self, resource: str):
        self._resource = resource
        self._logger = ScheduleLogger("Resource Manager {}".format(self._resource))
        self._data_manager = DatastoreManager(self._resource)

    def create_rsrc(self, json, id: str = None):
        '''creates a new resource with no id'''
        resource = ResourceManager.create_uuid(json)
        response = self._data_manager.post_resource(resource, id)
        return response

    def get_rsrc(self, resource_id: str = None, linked_resource_id: str = None,):
        ''' Implemented differently per resource, see child '''
        pass


    def update_rsrc(self, json, id = None):
        '''Used when patching a resource that already has an id'''
        response = self._data_manager.patch_resource(json, id)
        return response

    def delete_rsrc(self, id):
        '''Used to delete an existing resource'''
        response = self._data_manager.delete_rsrc(id)
        return response
         
    @staticmethod
    def create_uuid(json): 
        '''Generate a unique uuid for resource'''
        json['id'] = str(uuid.uuid4())
        return json
