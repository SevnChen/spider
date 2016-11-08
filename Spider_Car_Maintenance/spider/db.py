# -*- coding: utf-8
import mysql.connector
from config import *

class ConnectDB(object):
    def __init__(self):
        config_db={'host':DB_HOST,
                   'user':DB_USER,
                   'password':PASSWORD,
                   'port':PORT,
                   'database':DB_NAME,
                   'charset':'utf8'}
        self.db=mysql.connector.connect(**config_db)
        self.cursor = self.db.cursor()
    def insert(self,table_name	="",
                    manufacturer ="",
                    brand ="",
                    series ="",
                    car_id_souhu ="",
                    name ="",
                    year ="",
                    table1_head ="",
                    table1_content ="",
                    table2_head ="",
                    table2_content ="",
                    url_car =""):
        sql='''insert into %s  
               (manufacturer,brand,series,car_id_souhu,name,year,table1_head,table1_content, table2_head, table2_content,url_car)
               VALUES(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\', \'%s\',\'%s\') ''' %(table_name, manufacturer, brand, 
               series, car_id_souhu, name, year, table1_head, table1_content, table2_head, table2_content, url_car)
        #print sql
        self.cursor.execute(sql)
        self.db.commit()
    def select(self,table_name="",field="",value=""):
        sql=''' select %s from %s where %s = \'%s\' ''' % (field,table_name,field,value)
        result=self.cursor.execute(sql)
        return result
    def dbclose(self):
        self.db.close()
    def dbcreate(self):
        sql = ''' DROP TABLE IF EXISTS `car_maintenance`; '''
        self.cursor.execute(sql)
        self.db.commit()
        sql =''' CREATE TABLE `car_maintenance` (
                `car_maintenance_id` int(11) NOT NULL AUTO_INCREMENT,
                `manufacturer` varchar(255) DEFAULT NULL,
                `brand` varchar(255) DEFAULT NULL,
                `series` varchar(255) DEFAULT NULL,
                `car_id_souhu` varchar(255) DEFAULT NULL,
                `name` varchar(255) DEFAULT NULL,
                `year` varchar(255) DEFAULT NULL,
                `table1_head` longtext DEFAULT NULL,
                `table1_content` longtext DEFAULT NULL,
                `table2_head` longtext DEFAULT NULL,
                `table2_content` longtext DEFAULT NULL,
                `url_car` varchar(255) DEFAULT NULL,
                PRIMARY KEY (`car_maintenance_id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8 '''
        self.cursor.execute(sql)
        self.db.commit()





