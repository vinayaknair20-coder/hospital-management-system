# importing multiple libraries to run mysql connectors

import pymysql
from configparser import ConfigParser
from pymysql.err import MySQLError
import os
from pymysql import cursors

# creating  connection class
class DBConnection:
    '''singleton connection implementation,ie,
    it only create one instance and use it everytime'''
    # creating class variable to store created instance,by default set none
    __instance=None 
    # overriding new(dunder method) to check if instance created or not
    def __new__(cls):
        # creating new instance if not already existing
        if cls.__instance is None:
            cls.__instance=super(DBConnection,cls).__new__(cls)
            cls.__instance.initialize()
        # if existing then return existing object
        return cls.__instance
    def initialize(self):

        '''initializing database using credentials in db_config.ini file'''

        try:
            # loading the config file
            config=ConfigParser()
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            config_path = os.path.join(project_root,'db_config.ini')
            config.read(config_path) #extracted datas frm file into a dictionary format
            # establishing mysql connetion
            self.connection=pymysql.connect(
                host=config.get('mysql','host'),
                user=config.get('mysql','username'),
                password=config.get('mysql','password'),
                database=config.get('mysql','database')
            )
            print('connected to mysql database')
        except MySQLError as e:
            print(f'error while connecting to mysql:{e}')
            self.connection=None

    def get_connection(self):
        return self.connection
