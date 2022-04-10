import mysql_table_query
import device_name_prefix
import ipaddress
import device_port
from type_dict import type
def generation_doa_name(project):
    doa_prefix = device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name'])
    return doa_prefix

def get_doa_type(project):
    port_assign = {'name':None,'port_assign':None}
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'doa':
            doa_type = {'supplier':entry['supplier'],'type':entry['equipment_type']}
            if doa_type['supplier'] == 'cisco':
                port_assign['name'] = 'C'+str(entry['name'])
                port_assign['port_assign'] = device_port.cisco(doa_type['type'])
            elif doa_type['supplier'] == 'h3c':
                port_assign['name'] = 'H'+str(entry['name'])
                port_assign['port_assign'] = device_port.h3c(doa_type['type'])
    return port_assign

def get_doa_info(project):
    all_mgt_list = []
    try:
        for entry in mysql_table_query.ip_planning(project):
            mgt_ip_list = []
            if entry['description'] == 'MGT':
                for ip in ipaddress.IPv4Network(entry['network']):
                    mgt_ip_list.append((ip, ipaddress.IPv4Network(entry['network']).netmask))
            else:
                continue
            d_doa_mgt = mgt_ip_list[2]
            e_doa_mgt = mgt_ip_list[3]
            all_mgt_list.append(
                {'floor': entry['floor'],'hsrp':{'ip':str(mgt_ip_list[1][0]),'netmask':str(mgt_ip_list[1][1])},
                 'DDOA':{'name':'-'.join((generation_doa_name(project),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'D',get_doa_type(project)['name'],'DOA','01')),'mgtip':str(d_doa_mgt[0]),'netmask':str(d_doa_mgt[1]),'port_assign':get_doa_type(project)['port_assign']},
                 'EDOA':{'name':'-'.join((generation_doa_name(project),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'E',get_doa_type(project)['name'],'DOA','01')),'mgtip':str(e_doa_mgt[0]),'netmask':str(e_doa_mgt[1]),'port_assign':get_doa_type(project)['port_assign']}})
    except EOFError:
        print('无法查询数据')
    return all_mgt_list
