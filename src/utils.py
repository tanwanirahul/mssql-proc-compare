'''
Created on 04-May-2014

@author: Rahul
'''
import json


def load_json_file(file_handle):
    '''
        Attempts to load the JSON deta form specified file.
    '''
    try:
        return json.load(file_handle)
    except Exception:
        raise Exception("Data not in proper JSON format for file : {0}".format(
                                                                file_handle))


def dump_json_file(data, file_handle):
    '''
        Dumps the JSON data into file.
    '''
    try:
        return json.dump(data, file_handle)
    except Exception:
        raise Exception("Data not in proper JSON format for file : {0}".format(
                                                                file_handle))
