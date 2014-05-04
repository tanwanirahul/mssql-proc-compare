'''
Created on 04-May-2014

@author: Rahul
'''
from mssqlwrapper import MSSQLWrapper
import argparse
import json

DS_WRAPPER_MAPPING = {"mssql": MSSQLWrapper}

DB_CONFIG = {}
PROC_DETAILS = []
OUTPUT_STATUS = []


def load_json_file(file_handle):
    '''
        Attempts to load the JSON deta form specified file.
    '''
    try:
        return json.load(file_handle)
    except Exception:
        raise Exception("Data not in proper JSON format for file : {0}".format(
                                                                file_handle))


def load_details(conf, proc_details):
    '''
        loads the json specification for configuration and
        proc_details parameters.
    '''
    DB_CONFIG.update(load_json_file(conf))
    PROC_DETAILS.extend(load_json_file(proc_details))


if __name__ == "__main__":
    '''
        Accepts command line options for configuration, input and output
        details.
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', nargs='?', type=argparse.FileType('r'),
                            default="conf.json")
    parser.add_argument('--input', nargs='?', type=argparse.FileType('r'),
                            default="input.json")
    parser.add_argument('--output', nargs='?', type=argparse.FileType('w'),
                        default="output.json")
    parser.add_argument('--datasource', nargs='?', type=argparse.FileType('w'),
                        default="mssql")
    options = parser.parse_args()

    # load the config and procedures details
    load_details(options.conf, options.input)

    #Get DB Wrapper
    wrapper = DS_WRAPPER_MAPPING.get(options.datasource)
    if wrapper is None:
        raise Exception("Implementation for this datasource is not"
                            + "yet available.")
