

from api.rsrc_manager import ResourceManager


class ScheduleResourceManager(ResourceManager):
    def __init__(self, resource):
        self.resource = resource
        super().__init__(resource)
    
    def create_rsrc(self, json, id: str = None):
        ''' Used when creating a fresh resource with no id'''
        return super().create_rsrc(json)
    
    def get_rsrc(self, resource_id: str = None):
        #if an id was specified get item, otherwise it's a get all request
        if resource_id is not None:
            response = self._data_manager.get_from_resource(resource_id)
        else:
            response = self._data_manager.get_all_from_resource()
            
        self._logger.info("Resource: {}".format(response))
        return response

    def get_by_user(self, user_id: str):
        response = self._data_manager.get_by_user(user_id)
        self._logger.info("Resource: {}".format(response))
        return response
    
    def get_by_username(self, username):
        res = self._data_manager.get_by_username(username)
        print(res)
        self._logger.info("Resource: {}".format(res))
        return res

    
    def update_rsrc(self, json, id=None):
        return super().update_rsrc(json, id)
    
    def delete_rsrc(self, id):
        return super().delete_rsrc(id)
