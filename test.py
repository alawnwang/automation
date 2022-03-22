import mysql_table_query
project = input('项目名称: ')
def test():
    for type in mysql_table_query.equipment_type(project=project):
        if type['function'] == 'xoa':
            xoa = type['equipment_type']
        elif type['function'] == 'evp':
            evp = type['equipment_type']
        elif type['function'] == 'ewl':
            ewl = type['equipment_type']
    return {'xoa':xoa,'evp':evp,'ewl':ewl}
print(test())