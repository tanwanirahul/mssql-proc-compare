'''
Created on 04-May-2014

@author: Rahul
'''
import pymssql


class MSSQLWrapper(object):
    '''
        Wraps the sql server connections and commands/calls.
    '''
    def __init__(self, server="localhost", port=1433, user="root",
                 password="password", db="test"):
        '''
            Given the connection details, tries to make a connection to the
            target server.
        '''
        self.conn = None
        self.cursor = None
        try:
            self.conn = pymssql.connect(server=server, user=user,
                                        password=password, database=db,
                                        port=str(port), as_dict=True)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise Exception("Unable to connect to target host: {0}".format(
                                                               e.message))

    def call_stored_proc(self, proc_name, *args):
        '''
           Given the stored proc name and list of arguments to pass to
           the same, returns the result of stored proc execution.
        '''
        self.cursor.callproc(proc_name, args)
        for row in self.cursor:
            yield row
