from typing import Any, Dict
from api.json_schema.schema_validator import SchemaValidator
from api.rsrc_manager import ResourceManager
from common.logger import ScheduleLogger


class BaseLogic():
    ''' Base business logic, where we decide how we want to progress, validate and process a http request
        Complete validation, implement logic and pass to the resource manager to svae to data stores

        This base class will be extended by child classes to implement functionality based on specific resource needs '''
    
    def __init__(self, resource):
        self.resource = resource

        logger_name = "Buisness Logic {}".format(self.resource)
        self._logger = ScheduleLogger(logger_name)
        self.schema_validate = SchemaValidator()
        self.resource_manager = ResourceManager(self.resource)

    #general post functions
    #these functions are placeholders to be overwritten by child classes
    def get(self, id: str = None):
        pass

    def post(self, data: Any, **kwargs):
        pass

    def patch(self, id: str, change_set: Dict[str, Any], **kwargs):
        pass

    def delete(self, id: str):
        pass

    def validate_request(self, data: Any, **kwargs):
        pass

    def _validate_json(self, data: Dict[str, Any])  -> None:
        self.schema_validate.validate_request(self.resource, data)

    def _init_default_values(self, data: Dict[str, Any]):
        optionalKeys = []
        if data is not None:
            for key in optionalKeys:
                if not data.get(key):
                    data[key] = None
        return data
