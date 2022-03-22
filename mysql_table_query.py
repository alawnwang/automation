import pymysql

db = pymysql.connect(host='111',user='222',password='333',database='444')


cursor = db.cursor(cursor=pymysql.cursors.DictCursor,)

sql = 'show tables'
cursor.execute(sql)

rs = cursor.fetchall()


def workplace_info(project):
    workplace_info = "select * from workplace_information where project = '%s'" %project
    cursor.execute(workplace_info)
    info_data = cursor.fetchall()
    return info_data

def ip_planning(project):
    ip_planning = "select * from ip_planning where project = '%s'" %project
    cursor.execute(ip_planning)
    ip_data = cursor.fetchall()
    return ip_data

def endpoint(project):
    endpoint = "select * from endpoint where project = '%s'" %project
    cursor.execute(endpoint)
    endpoint_data = cursor.fetchall()
    return endpoint_data

def equipment_type(project):
    equipment_type = "select * from equipment_type_version where project = '%s'" %project
    cursor.execute(equipment_type)
    equipment_data = cursor.fetchall()
    return equipment_data