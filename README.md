mssql-proc-compare
==================

This repository contains code to compare the results of previous and new stored procedures after the modifications.


Usage Instructions:

Install low level dependencies:
sudo apt-get install unixodbc unixodbc-dev freetds-dev tdsodbc python-dev

Install Python Odbc drivers.
Download the source (https://code.google.com/p/pyodbc/downloads/detail?name=pyodbc-3.0.7.zip)
Extract and run:
  sudo python setup.py build
  sudo python setup.py install
  
Install pymssql (Driver on top of odbc, with easy to use API)
sudo pip install pymssql

Once dependencies are installed, you can clone this repository and,
1. add connection parameters to conf.json
2. Input details like name of the stored proc to compare etc in input.json (You can change it by command line argument).
3. Run python compare.py. This should generate output.json to display the results. You can pass --output to change the location.



