import mysql_table_query
import device_name_prefix
import ipaddress
import device_port
# from type_dict import type
def generation_coa_name(project):
    coa_prefix = '-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),'BDR'+str(mysql_table_query.workplace_info(project)[0]['core_bdr_floor'])+'01'))
    return coa_prefix

def get_coa_type(project):
    port_assign = {'name':'','port_assign':None}
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'coa':
            coa_type = {'supplier':entry['supplier'],'type':entry['equipment_type']}
            if coa_type['supplier'] == 'cisco':
                port_assign['name'] = 'C'+str(entry['name'])
                port_assign['port_assign'] = device_port.cisco(coa_type['type'])
            elif coa_type['supplier'] == 'h3c':
                port_assign['name'] = 'H'+str(entry['name'])
                port_assign['port_assign'] = device_port.h3c(coa_type['type'])
    return port_assign

def get_coa_info(project):
    for enrty in mysql_table_query.ip_planning(project):
        if enrty['function'] == '核心网段':
            mcoa_ip = ipaddress.IPv4Network(enrty['network'])[1]
            scoa_ip = ipaddress.IPv4Network(enrty['network'])[2]
            mgt_dict = {'floor': enrty['floor'], 'MCOA': (
                '-'.join((generation_coa_name(project), 'A01', str(get_coa_type(project)['name']), 'COA', '01')))
                , 'MMGTIP': {'ip': str(mcoa_ip), 'netmask': '255.255.255.255'}, 'SCOA': (
                    '-'.join((generation_coa_name(project), 'A02', get_coa_type(project)['name'], 'COA', '01'))),
                        'SMGTIP': {'ip': str(scoa_ip), 'netmask': '255.255.255.255'},
                        'port_assign': get_coa_type(project)['port_assign']}
            return mgt_dict

