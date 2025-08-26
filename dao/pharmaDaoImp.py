from typing import List
from dao.absatractDaoPharma import medecineDaoService
from db.db_connection import DBConnection
from models.medicine import Medicine

class medicineDaoImp(medecineDaoService):
    '''implementation of abstract class methods'''
    #sql queries
    DISPLAY_ALL_MEDICINE ="SELECT*FROM clinicdb "