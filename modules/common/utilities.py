import json
from decimal import Decimal
from datetime import date, datetime
import uuid

from api.error_handling import InvalidFormatException

class JsonSerialiser(json.JSONEncoder):
    def default(self, obj):
        #If passed in object is instance of Decimal convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)

        #If passed in object is instance of Date convert it to a isodate
        if isinstance(obj, date):
            return str(obj)

        #Otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
        
def format_json(logger, json_data):
    if is_jsonable(json_data) == True:
        return json_data
    else:
        logger.warning("Json contains unserializable data, returning string-ified version")
        serialised_json = json.dumps(json_data, sort_keys=True, indent=4, separators=(',', ': '), cls=JsonSerialiser)
        return json.loads(serialised_json)

def is_jsonable(data):
    try:
        json.dumps(data)
        return True
    except (TypeError, OverflowError):
        return False

def is_valid_uuid(string):
    try:
        uuid.UUID(string)
        return True
    except ValueError:
        raise InvalidFormatException("{} is not a valid UUID".format(string))

def is_valid_date_format(date_str: str) -> bool:
    """Checks if the date string is in the format 'dd-mm-yyyy'."""
    try:
        datetime.strptime(date_str, '%d-%m-%Y')
        return True
    except ValueError:
        raise InvalidFormatException("Dates should be in the format 'dd-mm-yyyy'")
    
def is_valid_dates_format(date_ary: [str]) -> bool:
    """Checks if the date string is in the format 'dd-mm-yyyy'."""
    try:
        for date in date_ary:
            datetime.strptime(date, '%d-%m-%Y')
        return True
    except ValueError:
        raise InvalidFormatException("Dates should be in the format 'dd-mm-yyyy'")