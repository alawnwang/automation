import pymysql
from sqlalchemy import create_engine,Table,MetaData
from sqlalchemy.orm import sessionmaker

#
def link_db():
    engine = create_engine('mysql+pymysql://root:uz8954UZN@119.91.102.106:3306/building_information')
    return engine
#

#
# def db_query():
#     metadata = MetaData()
#     table = Table('ip_planning',metadata,autoload=True,autoload_with=link_db())
#     Session = sessionmaker(bind=link_db())
#     session = Session()
#     res = session.query(table).first()






def workplace_info(project):
    db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')

    cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
    workplace_info = "select * from workplace_information where project = '%s'" %project
    cursor1.execute(workplace_info)
    info_data = cursor1.fetchall()
    return info_data

def ip_planning(project):
    db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')

    cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
    ip_planning = "select * from ip_planning where project = '%s'" %project
    cursor1.execute(ip_planning)
    ip_data = cursor1.fetchall()
    return ip_data

def endpoint(project):
    db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')

    cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
    endpoint = "select * from endpoint where project = '%s'" %project
    cursor1.execute(endpoint)
    endpoint_data = cursor1.fetchall()
    return endpoint_data

def equipment_type(project):
    db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')

    cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
    equipment_type = "select * from equipment_type_version where project = '%s'" %project
    cursor1.execute(equipment_type)
    equipment_data = cursor1.fetchall()
    return equipment_data

def core_ip():
    db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')

    cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
    ip_info = "select * from ip_planning where func = '核心网段'"
    cursor1.execute(ip_info)
    info_data = cursor1.fetchall()
    return info_data

# def parameter(project):
#     db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')
#     cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
#     parameter = "select * from parameter where project = '%s'" %project
#     cursor1.execute(parameter)
#     parameter_data = cursor1.fetchall()
#     return parameter_data