from robot.libraries.BuiltIn import BuiltIn
import logging


class MongoConnectionManager(object):
    """
    Connection Manager handles the connection & disconnection to the database.
    """

    def __init__(self):
        """
        Initializes _dbconnection to None.
        """
        self._dbconnection = None
        self._builtin = BuiltIn()

    def connect_to_mongodb(self, dbHost='localhost', dbPort=27017, dbMaxPoolSize=10, dbNetworkTimeout=None,
                           dbDocClass=dict, dbTZAware=False):
        """
        Loads pymongo and connects to the MongoDB host using parameters submitted.

        Example usage:
        | # To connect to foo.bar.org's MongoDB service on port 27017 |
        | Connect To MongoDB | foo.bar.org | ${27017} |
        | # Or for an authenticated connection |
        | Connect To MongoDB | admin:admin@foo.bar.org | ${27017} |

        """
        dbapiModuleName = 'pymongo'
        db_api_2 = __import__(dbapiModuleName)

        dbPort = int(dbPort)
        # print "host is               [ %s ]" % dbHost
        # print "port is               [ %s ]" % dbPort
        # print "pool_size is          [ %s ]" % dbPoolSize
        # print "timeout is            [ %s ]" % dbTimeout
        # print "slave_okay is         [ %s ]" % dbSlaveOkay
        # print "document_class is     [ %s ]" % dbDocClass
        # print "tz_aware is           [ %s ]" % dbTZAware
        logging.debug(
            "| Connect To MondoDB | dbHost | dbPort | dbMaxPoolSize | dbNetworktimeout | dbDocClass | dbTZAware |")
        logging.debug(
            "| Connect To MondoDB | %s | %s | %s | %s | %s | %s |" % (dbHost, dbPort, dbMaxPoolSize, dbNetworkTimeout,
                                                                      dbDocClass, dbTZAware))

        self._dbconnection = db_api_2.MongoClient(host=dbHost, port=dbPort, socketTimeoutMS=dbNetworkTimeout,
                                                  document_class=dbDocClass, tz_aware=dbTZAware,
                                                  maxPoolSize=dbMaxPoolSize)

    def disconnect_from_mongodb(self):
        """
        Disconnects from the MongoDB server.

        For example:
        | Disconnect From MongoDB | # disconnects from current connection to the MongoDB server | 
        """
        logging.debug("| Disconnect From MongoDB |")
        self._dbconnection.close()

    def retrieve_mongodb_records_by_id(self, dbName, dbCollName, objectid, fields=[], returnDocuments=False):
        """
        Retrieve the record from a given MongoDB database collection by _id
        Returned value must be single quoted for comparison, otherwise you will
        get a TypeError error.

        Usage is:
        | ${Result} | Retrieve MongoDB Records By ID | DBName | CollectionName | ObjectId |
        | Log | ${Result} |
        """
        dbName = str(dbName)
        dbCollName = str(dbCollName)
        try:
            db = self._dbconnection['%s' % (dbName,)]
        except TypeError:
            self._builtin.fail("Connection failed, please make sure you have run 'Connect To Mongodb' first.")
        coll = db['%s' % dbCollName]
        if fields:
            results = coll.find_one({'_id': ObjectId(objectid)}, fields)
        else:
            results = coll.find_one({'_id': ObjectId(objectid)})
        if returnDocuments:
            return list(results)
        else:
            response = ''
            for d in results:
                response = '%s%s' % (response, d.items())
            return response