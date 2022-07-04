import socket

import sqlalchemy.exc
from sqlalchemy import create_engine
from urllib.parse import quote_plus as urlquote
import pandas as pd

project = input('项目名称：')




def link_db():
    try:
        username = 'root'
        password = '87654321'
        host = '12345678'
        port = '3306'
        dbname = 'building_information'
        engine = create_engine(f'mysql+pymysql://{username}:{urlquote(password)}@{host}:{port}/{dbname}')
        return engine
    except socket.gaierror:
        print('数据库无法连接')

def ip_planning_tables(project):
    return "select * from ip_planning where project = '%s' ORDER BY network*1" %project

def connection(project):
    return "select * from connection_relation where project = '%s'" % project

def manageip(project):
    return  "select * from manage_ip_assignments where project = '%s'" % project

def mysql_inquire(sql_statement,engine):
    sql_res = pd.read_sql(sql_statement,engine)
    return sql_res

def write_excel():
    excel_file = pd.ExcelWriter('/Users/alawn/Desktop/config/' + project + '规划.xlsx')
    ip_planning = mysql_inquire(ip_planning_tables(project), link_db())
    ip_planning.to_excel(excel_file,sheet_name='ip_planning_sheet')
    connect = mysql_inquire(connection(project), link_db())
    connect.to_excel(excel_file,sheet_name='connection_sheet')
    mgtip =  mysql_inquire(manageip(project), link_db())
    mgtip.to_excel(excel_file,sheet_name='mgtip_sheet')
    excel_file.save()


write_excel()