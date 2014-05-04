mssql-proc-compare
==================

This repository contains code to compare the results of previous and new stored procedures after the modifications.


##Usage Instructions:


1. Install low level dependencies:
    
    **_sudo apt-get install unixodbc unixodbc-dev freetds-dev tdsodbc python-dev_**


2. Install Python Odbc drivers.
    
    Download the source (https://code.google.com/p/pyodbc/downloads/detail?name=pyodbc-3.0.7.zip)


3. Extract and run:
    1. sudo python setup.py build
    2. sudo python setup.py install
  

4. Install pymssql (Driver on top of odbc, with easy to use API)
    sudo pip install pymssql


5. Once dependencies are installed, you can clone this repository and,
    1. add connection parameters to conf.json
    
    2. Input details like name of the stored proc to compare etc in input.json (You can change it by command line argument).
  
    3. Run python compare.py. This should generate output.json to display the results. You can pass --output to change the location.



