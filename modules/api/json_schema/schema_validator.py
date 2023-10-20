import os
import json
import jsonschema
from jsonschema import validate
from flask import request

from api.error_handling import DataModelException
from common.logger import ScheduleLogger

class SchemaValidator():
    __slots__ = (
        "_logger"
    )

    def __init__(self) -> None:
        self._logger = ScheduleLogger('Json Schema Validator')

    def resolve_schema_refs(self, schema, base_path):
        for key, value in schema.items():
            if isinstance(value, dict):
                if "$ref" in value and value["$ref"].startswith("file:"):
                    rel_path = value["$ref"].replace("file:", "")
                    abs_path = os.path.join(base_path, rel_path)
                    value["$ref"] = f"file:{abs_path}"
                self.resolve_schema_refs(value, base_path)

    def validate_request(self, resource_type, request_data, subresource_type=None, subresource_type2=None):
        request_type = request.method.lower()
        if subresource_type is not None:
            #if subresource_type2 is not None:
               # schema_path = "/app/api/json_schema/{0}/{1}.schema.{2}.json".format(resource_type, subresource_type, request_type)
            #else:
                schema_path = "/app/api/json_schema/{0}/{1}.schema.{2}.json".format(resource_type, subresource_type, request_type)
        else:
            if request_type == "patch":
                schema_path = "/app/api/json_schema/{0}/{0}.schema.{1}.json".format(resource_type, request_type)
            else:
                schema_path = "/app/api/json_schema/{0}/{0}.schema.json".format(resource_type)
        msg = "Trying to validate {} {} request with data: {}".format(resource_type, request_type, request_data)
        self._logger.info(msg)
        self._logger.debug("Schema path: {}".format(schema_path))
        try:
            with open(schema_path) as file:
                schema = json.load(file)
        except:
            msg = "Error loading json schema resource_type {} for request with this info: {}".format(resource_type, request_data)
            self._logger.error(msg)
            raise DataModelException(msg)

        # Resolve the $ref paths
        base_path = os.path.dirname(schema_path)
        self.resolve_schema_refs(schema, base_path)

        try:
            #json schema validation library function
            validate(instance=request_data, schema=schema)
            self._logger.info("Schema validated successfully")
            return request_data
        except jsonschema.exceptions.ValidationError as err:
            raise DataModelException("Data Model Schema Validation has failed: {}".format(err))
