import mysql_table_query
import device_name_prefix
import ipaddress
import device_port
from type_dict import type

def generation_doa_name(project):
    doa_prefix = '-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),'BDR'+str(mysql_table_query.workplace_info(project)[0]['core_bdr_floor'])+'01'))
    return doa_prefix

def get_doa_type(project):
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'doa':
            doa_type = entry['name']
            return doa_type

def get_doa_port(device_type):
    if device_type == '9300':
        doa_port = device_port.cisco.doa_c9300_port()
        return doa_port

def get_doa_info(project):
    all_mgt_list = []
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
            {'floor': entry['floor'],'hsrp':{'ip':str(mgt_ip_list[1][0]),'netmask':str(mgt_ip_list[1][1])},'DDOA':{'name':'-'.join((generation_doa_name(project),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'D',get_doa_type(project),'DOA','01')),'mgtip':str(d_doa_mgt[0]),'netmask':str(d_doa_mgt[1])}, 'EDOA':{'name':'-'.join((generation_doa_name(project),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'E',get_doa_type(project),'DOA','01')),'mgtip':str(e_doa_mgt[0]),'netmask':str(e_doa_mgt[1])},'prot_assign':device_port.cisco(type(project)['doa'])})
    return all_mgt_list


