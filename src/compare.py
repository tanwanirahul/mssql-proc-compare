'''
Created on 04-May-2014

@author: Rahul
'''
from mssqlwrapper import MSSQLWrapper
from utils import load_json_file, dump_json_file
import argparse

DS_WRAPPER_MAPPING = {"mssql": MSSQLWrapper}

DB_CONFIG = {}
DB_CONNECTIONS = {}
PROC_DETAILS = []
OUTPUT_STATUS = []


def load_details(conf, proc_details):
    '''
        loads the json specification for configuration and
        proc_details parameters.
    '''
    DB_CONFIG.update(load_json_file(conf))
    PROC_DETAILS.extend(load_json_file(proc_details))


def dict_compare(expected, under_test):
    '''
        Given the two dicts, checks if the dict under test is same as expected.
    '''
    for key, value in expected.items():
        if not value == under_test.get(key):
            raise Exception("Value mismatch for column {0}".format(key))


def compare_resultsets(original, under_test):
    '''
        Compares the two result sets for all the records.
    '''
    for index, original_record in enumerate(original):
        dict_compare(original_record, under_test[index])


def compare_procs(procs):
    '''
        Given the list of stored procedures, gets their data one by one
        and compares the output of original with modified one.
    '''
    for proc in procs:

        db = proc.get("db")

        if db is None:
            raise Exception("DB parameter for {0}".format(proc)
             + "stored procedure is missing in input file")

        wrapper = DB_CONNECTIONS.get(db)

        if wrapper is None:
            raise Exception("Connection parameters for {0}".format(db)
             + "DB are missing.")

        params = proc.get("parameters") or []
        old = str(proc.get("old"))
        modified = str(proc.get("new"))
        key_attribute = str(proc.get("keyAttribute"))

        original_result = wrapper.call_stored_proc(old, *params)
        under_test_result = wrapper.call_stored_proc(modified, *params)

        original_result = sorted(original_result,
                             key=lambda k: k.get(key_attribute))
        under_test_result = sorted(under_test_result,
                             key=lambda k: k.get(key_attribute))
        status = "PASS"
        error = "None"
        try:
            compare_resultsets(original_result, under_test_result)
        except Exception as e:
            status = "FAILED"
            error = e.message

        OUTPUT_STATUS.append({"old": old, "new": modified, "status": status,
                              "error": error})

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
    parser.add_argument('--datasource', nargs='?',
                        default="mssql")
    options = parser.parse_args()

    # load the config and procedures details
    load_details(options.conf, options.input)

    #Get DB Wrapper
    ds_wrapper = DS_WRAPPER_MAPPING.get(options.datasource)
    if ds_wrapper is None:
        raise Exception("Implementation for this datasource is not"
                            + " yet available.")

    # Add connections for all the different databases specified in conf.json
    for db, details in DB_CONFIG.items():
        conn_details = details
        conn_details.update({"db": db})
        DB_CONNECTIONS.update({db: ds_wrapper(**conn_details)})

    compare_procs(PROC_DETAILS)
    dump_json_file(OUTPUT_STATUS, options.output)
