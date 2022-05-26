import pymysql
import openpyxl



#
# def ip_planning(project):
#     db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')
#
#     cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
#     ip_planning = "select * from ip_planning where project = '%s' ORDER BY floor*1" %project
#     cursor1.execute(ip_planning)
#     ip_data = cursor1.fetchall()
#     return ip_data
#
# def connection(project):
#     db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')
#
#     cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
#     info = "select * from connection_relation where project = '%s'" % project
#     cursor1.execute(info)
#     connection = cursor1.fetchall()
#     return connection
#
# def deivce_ip(project):
#     db = pymysql.connect(host='119.91.102.106', user='root', password='uz8954UZN', database='building_information')
#
#     cursor1 = db.cursor(cursor=pymysql.cursors.DictCursor, )
#     info = "select * from Manage_IP_assignments where project = '%s'" % project
#     cursor1.execute(info)
#     device_ip = cursor1.fetchall()
#     return device_ip
#
# def write_excel(project):
#     workbook = openpyxl.Workbook()
#     ip_sheet = workbook.create_sheet('ip_planning')
#     ip_sheet.append(['network','status','domain','vlan','func','description','acl','project','building_name','floor','bdr','type_of_workplace'])
#     mgt_sheet = workbook.create_sheet('mgt_ip')
#     mgt_sheet.append([''])
#     connect = workbook.create_sheet('connect')
#     for info in ip_planning(project):


# import  mysql_table_query
# def basic_device_info_dict(project):
#     doa_config_info = []
#     manage_ip_list = mysql_table_query.deivce_ip(project)
#     network = mysql_table_query.ip_planning(project)
#     connect = mysql_table_query.connection(project)
#     interconnection_list = []
#     downlinkconnection_list = []
#     uplinkconnection_list = []
#     for c in connect:
#         connection = {'floor': None, 'A_device': None, 'A_port': None, 'Z_device': None, 'Z_port': None}
#         if '-DOA-' in c['A_device'] and '-DOA-' in c['Z_device'] :
#             connection['floor'] = c['Z_floor']
#             connection['A_device'] = c['A_device']
#             connection['A_port'] = c['A_port']
#             connection['Z_device'] = c['Z_device']
#             connection['Z_port'] = c['Z_port']
#             interconnection_list.append(connection)
#
#         if '-DOA-' in c['A_device'] and '-DOA-' not in c['Z_device'] :
#             connection['floor'] = c['Z_floor']
#             connection['A_device'] = c['A_device']
#             connection['A_port'] = c['A_port']
#             connection['Z_device'] = c['Z_device']
#             connection['Z_port'] = c['Z_port']
#             downlinkconnection_list.append(connection)
#
#         layer3connection = {'layer3connection':{'floor': None, 'A_device': None, 'A_port': None,'A_ipaddress':None,'Z_device': None, 'Z_port': None,'Z_ipaddress':None}}
#         if '-COA' in c['A_device'] and '-DOA-' in c['Z_device']:
#             layer3connection['layer3connection']['floor'] = c['Z_floor']
#             layer3connection['layer3connection']['A_device'] = c['A_device']
#             layer3connection['layer3connection']['A_port'] = c['A_port']
#             layer3connection['layer3connection']['A_ipaddress'] = c['A_ip']
#             layer3connection['layer3connection']['Z_device'] = c['Z_device']
#             layer3connection['layer3connection']['Z_port'] = c['Z_port']
#             layer3connection['layer3connection']['Z_ipaddress'] = c['Z_ip']
#             uplinkconnection_list.append(layer3connection)
#     for ip in manage_ip_list:
#         interconnect = {'interconnect':[]}
#         for n in interconnection_list:
#             if ip['device_name'] == n['A_device'] or ip['device_name'] == n['Z_device']:
#                 interconnect['interconnect'].append(n)
#             if ip['floor'] == n['floor'] and '-DOA' in ip['device_name']:
#                 ip.update(interconnect)
#
#
#         d_downlinkconnect = {'downlinkconnect': []}
#         e_downlinkconnect = {'downlinkconnect': []}
#         for m in downlinkconnection_list:
#             if '-DOA-' in ip['device_name'] and  '-D-' in ip['device_name'] and '-D-' in m['A_device'] and ip['floor'] == m['floor'] :
#                 d_downlinkconnect['downlinkconnect'].append(m)
#                 ip.update(d_downlinkconnect)
#             if '-DOA-' in ip['device_name'] and  '-E-' in ip['device_name'] and '-E-' in m['A_device'] and ip['floor'] == m['floor'] :
#                 e_downlinkconnect['downlinkconnect'].append(m)
#                 ip.update(e_downlinkconnect)
#
#         for u in uplinkconnection_list:
#             if ip['device_name'] == u['layer3connection']['Z_device']:
#                 ip.update(u)
#
#
#         networklist = []
#
#         for n in network:
#             interface_vlan = {'vlan': None, 'network': None,'desc':None,'acl':None}
#             if str(n['floor'])+str(n['bdr']) == str(ip['floor'])+str(ip['bdr']):
#                 interface_vlan['vlan'] = n['vlan']
#                 interface_vlan['network'] = n['network']
#                 interface_vlan['desc'] = n['description']
#                 interface_vlan['acl'] = n['acl']
#
#
#                 networklist.append(interface_vlan)
#         if '-DOA-' not in ip['device_name']:
#             pass
#         else:
#             ip.update({'network':networklist})
#             doa_config_info.append(ip)
#
#     return doa_config_info
#
# doa = basic_device_info_dict(project)
# for d in doa:
#     print(d)






import mysql_table_query
from math import ceil
from math import floor
project = input('项目名称: ')
#
network = input('IP地址：')


endpoint = mysql_table_query.endpoint(project)

def calc_num_oa(num_oa_point):
    num_oa_network = None
    num = num_oa_point / 240
    if num < 1:
        num_oa_network = 1
    else:
        numsplit = '{:.2}'.format(num_oa_point / 240)
        decimals = numsplit.split('.')
        if int(decimals[1]) < 2:
            num_oa_network = floor(num)
        if int(decimals[1]) > 2:
            num_oa_network = ceil(num)
    return num_oa_network

def calc_num_ty(num_oa_point):
    num_oa_network = None
    num = num_oa_point / 240 * 0.5
    if num < 1:
        num_oa_network = 1
    else:
        numsplit = '{:.2}'.format(num_oa_point / 240)
        decimals = numsplit.split('.')
        if int(decimals[1]) < 2:
            num_oa_network = floor(num)
        if int(decimals[1]) > 2:
            num_oa_network = ceil(num)
    return num_oa_network


def num_of_network(project):
    num_network = []
    for network in mysql_table_query.endpoint(project):
        if network['convergence'] =='N':
            pass
        else:
            floor_network_oa = (network['dpoint'] + network['epoint'])
            floor_network_ty = floor_network_oa * 0.5
            floor_network_voip = ceil(network['vpoint'] / 240)


            floor_network_num_dict = {'floor':network['floor'],'bdr':network['bdr'],'mgt':0.25,'ap_mgt':0.25,'video':0.25,
                                      'oa_device':0.25,'geli':0.25,'oa':calc_num_oa(floor_network_oa),'ty':calc_num_ty(floor_network_ty),
                                      'voip':floor_network_voip}
            num_network.append(floor_network_num_dict)
    return num_network