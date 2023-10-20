import time
from typing import Any, Dict
from requests.adapters import Retry
from pyArango.collection import Collection
from pyArango.connection import Connection
from pyArango.database import Database
from pyArango.connection import AikidoSession


''' PyArango doesn't handle timeouts correctly, and isn't reliable
    We want to force the call to connect to arango to have a timeout of 10 seconds,
    this way it will timeout and reconnect. This prevents hanging connections. 
    Probably only needed in a multinode configuration but good to have anyway'''

AikidoSession.Holder._base_call = AikidoSession.Holder.__call__
def _monkey_patch_call(self, *args, **kwargs):
  kwargs["timeout"] = 10
  return self._base_call(*args, **kwargs)

AikidoSession.Holder.__call__ = _monkey_patch_call


def open_connection(arango_url: str, logger: Any) -> Connection:
  conn = None
  attempt = 0
  retry_policy = Retry(total=10, connect=10, read=0,
                       other=0, backoff_factor=0.2)
  while conn == None:
    logger.info("Trying to connect to ArangoDB...")
    try:
      username = "root"
      password = "root"
      conn = Connection(arangoURL=arango_url, username=username, password=password,
                       max_retries=retry_policy)
    except Exception as e:
      msg = "Exception: {} while trying to connect to Arango DB {}. Perhaps Arango DB is not running. Please check!".format(
          e, arango_url)
      logger.error(msg)
      logger.warn("Trying to reconnect to Arango in 5 seconds")
      time.sleep(5)
      attempt = attempt + 1
      logger.warn("Now trying to connect to Arango DB {} with {} attempt".format(arango_url, str(attempt)))
      continue

  logger.info("Connected!")
  return conn


def open_database(conn: Connection, name: str, logger: Any) -> Database:
  '''Check if DB exists, if not then create it
    this works well for first app run with fresh db
  '''
  db = None
  if conn.hasDatabase(name):
    db = conn[name]
  else:
    logger.info('Creating database "{}"'.format(name))
    db = conn.createDatabase(name=name)
  logger.info('Opened database "{}"'.format(name))
  return db


def open_collection(db: Database, name: str, logger: Any) -> Collection:
  '''Check if DB collection exists, if not then create it
    this works well for first app run with fresh db
  '''
  collection = None
  if db.hasCollection(name):
    collection = db[name]
  else:
    # Collection does not exist - create it
    logger.info('Creating collection "{}"'.format(name))
    collection = db.createCollection(name=name,replicationFactor=2)
  logger.info('Opened collection "{}"'.format(name))
  return collection

def remove_arango_tags(doc: Dict[str, Any]) -> Dict[str, Any]:
  arango_keys = ['_key', '_id', '_rev']
  data = {k: v for k, v in doc.items() if k not in arango_keys}
  return data