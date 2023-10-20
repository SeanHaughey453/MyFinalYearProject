class GeneralException(Exception):
    '''General Exception please extend for other types'''
    __slots__ = ()
  
class ArangoException(Exception):
    '''General Exception please extend for other types'''
    pass

class ResourceConflictException(Exception):
    '''General Exception please extend for other types'''
    pass

class ResourceNotFoundException(Exception):
    '''General Exception please extend for other types'''
    pass

class DataModelException(Exception):
    '''General Exception please extend for other types'''
    pass

class MissingQueryParameterException(Exception):
    '''General Exception please extend for other types'''
    pass

class InvalidCredentials(Exception):
    '''General Exception please extend for other types'''
    pass

class InvalidFormatException(Exception):
    '''Raised when the provided format is incorrect.'''
    pass

class UnauthorizedException(Exception):
    '''Raised when the provided format is incorrect.'''
    pass

