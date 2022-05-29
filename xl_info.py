import mysql_table_query
import device_name_prefix
import ipaddress
import device_port
from math import ceil


# project = input('项目名称: ')
#
#计算每层楼接入设备数量
def device_number(iot):
    if iot > 48:
        xl = ceil(iot/48)
    else:
        xl = 1
    return {'num_xl':xl}
#
def device_number_dict(project):
    device_number_dict_list = []
    for entry in mysql_table_query.endpoint(project):
        device_number_dict = {'floor':entry['floor'],'bdr':entry['bdr']}
        device_number_dict.update(device_number(entry['iot']))
        device_number_dict_list.append(device_number_dict)
    return device_number_dict_list

def get_equipment_type(project):
    type_list = []
    for entry in mysql_table_query.equipment_type(project):
        if entry['supplier'] == 'cisco':
            equipment_type_acronym = 'C'
        elif entry['supplier'] == 'hillstone':
            equipment_type_acronym = 'S'
        elif entry['supplier'] == 'h3c':
            equipment_type_acronym = 'H'
        elif entry['supplier'] == 'aruba':
            equipment_type_acronym = 'A'
        type_function = equipment_type_acronym+entry['name']+'-'+str(entry['function']).upper()
        type_dict = {entry['function']:type_function}
        type_list.append(type_dict)
    return type_list
# # #

#
#     # return all_mgt_list

# #
def generation_device_info_dict(project):
    device_info_list = []
    for entry in device_number_dict(project):
        for type in get_equipment_type(project):
            entry.update(type)
        device_info_list.append(entry)
    return device_info_list



# #
#
def generation_floor_device_name(project):
    devicelist = []
    ccs_mgt_ip = ipaddress.IPv4Network(mysql_table_query.ccs_ip(project)[0]['network'])
    # xl_mgt_ip = (ip for ip in ccs_mgt_ip[4:])
    for entry in generation_device_info_dict(project):
        xl_name = ['-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'K',entry['xl'],str(num).rjust(2,'0'))) for num in range (1,entry['num_xl']+1)]
        floor_device_dict = {'floor':entry['floor'],'bdr':entry['bdr'],'xl':xl_name}
        devicelist.append(floor_device_dict)
    return devicelist

# #
def get_xl_type(project):
    port_assign = {'name': None, 'port_assign': None}
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'xoa':
            access_type = {'supplier':entry['supplier'],'type':entry['equipment_type']}
            if access_type['supplier'] == 'cisco':
                port_assign['name'] = 'C'+str(entry['name'])
                port_assign['port_assign'] = device_port.cisco(access_type['type'])
            elif access_type['supplier'] == 'h3c':
                port_assign['name'] = 'H'+str(entry['name'])
                port_assign['port_assign'] = device_port.h3c(access_type['type'])
    return port_assign

def get_access_info(project):
    xl_list = []
    ccs_mgt_ip = ipaddress.IPv4Network(mysql_table_query.ccs_ip(project)[0]['network'])
    xl_mgt_ip = (ip for ip in list(ccs_mgt_ip)[4:-2])
    for n in generation_floor_device_name(project):
        access_dict = {'floor':n['floor'],'bdr':n['bdr'],'xl':[]}
        for name in n['xl']:
            xl = {'floor':n['floor'],'bdr':n['bdr'],'name':name,'ip':xl_mgt_ip.__next__(),'netmask':ccs_mgt_ip.prefixlen,'gateway':ccs_mgt_ip[1],'port_assign':get_xl_type(project)['port_assign']}
            if access_dict['floor'] == xl['floor']:
                access_dict['xl'].append(xl)
        xl_list.append(access_dict)
    return xl_list


# for i in get_access_info(project):
#     print(i)