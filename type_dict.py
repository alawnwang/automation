import mysql_table_query
def type(project):
    for type in mysql_table_query.equipment_type(project):
        if type['function'] == 'coa':
            coa = type['equipment_type']
        if type['function'] == 'doa':
            doa = type['equipment_type']
        if type['function'] == 'xoa':
            xoa = type['equipment_type']
        elif type['function'] == 'evp':
            evp = type['equipment_type']
        elif type['function'] == 'ewl':
            ewl = type['equipment_type']
    type_dict = {'coa':coa,'doa':doa,'xoa':xoa,'evp':evp,'ewl':ewl}
    return type_dict

