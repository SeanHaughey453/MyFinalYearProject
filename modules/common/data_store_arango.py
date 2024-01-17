import time
from typing import Any, Dict, Optional, List
from copy import deepcopy
from pyArango.collection import BulkOperation
from pyArango.theExceptions import DocumentNotFoundError
from pyArango.document import Document
from pyArango.query import Query

from common.arango_utils import open_collection, open_connection, open_database, remove_arango_tags

from api.error_handling import ArangoException
from common.logger import ScheduleLogger

class DataStoreArangoDb:

  'Data Store using arangodb as the backing store.'
  __slots__ = ("_logger", "_conn", "_db", "_collection")

  def __init__(self, arango_url: str, db_name: str, collection_name: str) -> None:
    self._logger = ScheduleLogger('Datastore Arango')
    self._conn = open_connection(arango_url, self._logger)
    self._db = open_database(self._conn, db_name, self._logger)
    self._collection = open_collection(self._db, collection_name, self._logger)

  def overwrite(self, key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    try:
      self.__setitem__(key, data)
    except:
      raise ArangoException("Error writing to Arango")
    response = self.__getitem__(key)
    return response

  def get_item(self, key: str) -> Optional[Dict[str, Any]]:
    return self.__getitem__(key)

  def __setitem__(self, key: str, data: Dict[str, Any]):
    doc = self._collection.createDocument(data)
    #the _key will also set the _id of the document to be "collectionName/_keyUUID"
    doc._key = str(key)
    doc.save(waitForSync=True)

  def __getitem__(self, key: str) -> Dict[str, Any]:
    try:
      doc = self._collection.fetchDocument(key, rawResults=True)
    except (KeyError, DocumentNotFoundError):
      raise DocumentNotFoundError("The document with key '{}' does not exist".format(key))
    return remove_arango_tags(doc)
    
  def get_all(self) -> List[Dict[str, Any]]:
    #Return all documents in a collection as a list of dictionaries
    all_documents = []
    for doc in self._collection.fetchAll(rawResults=True):
      all_documents.append(remove_arango_tags(doc))
    return all_documents

  def patch_item(self, key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    doc = None
    #Check if document actually exists
    try:
      doc = self._collection.fetchDocument(key)
    except DocumentNotFoundError:
      raise DocumentNotFoundError("Document with key of {} was not found during patch".format(key))

    #Patch document with new data
    try:
      #work around as pyArango won't update a dict with a none value, so delete item first then patch
      for dictKey, value in data.items():
        if value == None:
         del doc[dictKey]

      doc.set(data)
      doc.patch(waitForSync=True)
    except:
      raise ArangoException("Error writing to Arango")
    
    return self.__getitem__(key)

  def delete_item(self, key: str) -> None:
    try:
      doc = self._collection.fetchDocument(key)
      doc.delete()
    except DocumentNotFoundError:
      raise DocumentNotFoundError("Document with key of {} was not found during delete".format(key))

  def check_existance(self, key: str) -> bool:
    '''Returns true if a collection with that id exists, otherwise returns false'''
    try:
      doc = self._collection.fetchDocument(key, rawResults=True)
      return True
    except:
      return False

  def run_query(self, query: str) -> List[Dict[str, Any]]:
    """Executes an AQL query and returns the results as a list of dictionaries."""
    results = []
    try:
        aql_query = self._db.AQLQuery(query, rawResults=True)
        for doc in aql_query:
            results.append(remove_arango_tags(doc))
    except Exception as e:
        raise ArangoException(f"Error executing AQL query: {e}")
    return results
  
  def put_item(self, key: str, data: Dict[str, Any]) -> Dict[str, Any]:
    doc = None
    print('data', data)
    #Check if document actually exists
    try:
      doc = self._collection.fetchDocument(key)
    except DocumentNotFoundError:
      raise DocumentNotFoundError("Document with key of {} was not found during patch".format(key))
    
    if doc is None:
      raise ArangoException("Document is None")
    #Patch document with new data
    try:
      #work around as pyArango won't update a dict with a none value, so delete item first then patch
      for dictKey, value in data.items():
        if value == None:
         del doc[dictKey]

      doc.set(data)
      print('doc',doc)
      doc.save(waitForSync=True)
    except Exception as e:
      print(f"Error updating document: {e}")
      raise ArangoException("Error writing to Arango")
    
    return self.__getitem__(key)
