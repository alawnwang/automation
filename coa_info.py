import mysql_table_query
import device_name_prefix
import ipaddress
import device_port

def generation_coa_name(project):
    coa_prefix = '-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),'BDR'+str(mysql_table_query.workplace_info(project)[0]['core_bdr_floor'])+'01'))
    return coa_prefix

def get_coa_type(project):
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'coa':
            coa_type = entry['equipment_type']
            return coa_type

def get_coa_port(device_type):
    if device_type == '4500-16':
        coa_port = device_port.cisco.coa_c4500x_16_port()
        return coa_port

def get_coa_info(project,device_type):
    for enrty in mysql_table_query.ip_planning(project):
        if enrty['function'] == '核心网段':
            mcoa_ip = ipaddress.IPv4Network(enrty['network'])[1]
            scoa_ip = ipaddress.IPv4Network(enrty['network'])[2]
            mgt_dict = {'floor':enrty['floor'],'MCOA':('-'.join((generation_coa_name(project),'A01',get_coa_type(project),'COA','01')))
                ,'MMGTIP':str(mcoa_ip),'SCOA':('-'.join((generation_coa_name(project),'A02',get_coa_type(project),'COA','01'))),'SMGTIP':str(scoa_ip),'port_assign':get_coa_port(device_type)}
            return mgt_dict
