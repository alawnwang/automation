import mysql_table_query
import device_name_prefix
import ipaddress
import device_port
import ip_assign

# project = input('项目名称: ')
# #
# network = input('IP地址：')

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


def get_coa_info(network,project):
    mgt_ip = ip_assign.network_class(network, project)['loopback']
    entry = (mysql_table_query.core_ip(project))[0]
    ccs_connect_ip = [ip for ip in ipaddress.collapse_addresses([mgt_ip[6][0],mgt_ip[7][0]])]
    mgt_dict = {'floor': entry['floor'],'bdr':entry['bdr'],'MCOA': ('-'.join((generation_coa_name(project), 'A01', str(get_coa_type(project)['name']), 'COA', '01'))),
                'MMGTIP': {'ip': mgt_ip[0][0][1], 'netmask': '255.255.255.255','area0_ip':str(mgt_ip[1][0][1])+'/'+str((mgt_ip[1][0]).prefixlen),'localarea':str(mgt_ip[2][0][1])+'/'+str((mgt_ip[1][0]).prefixlen),
                     'cwl':str(mgt_ip[3][0][1])+'/'+str((mgt_ip[1][0]).prefixlen),'ccsvlan':'550','ccsip':str(ccs_connect_ip[0][1])+'/'+str((mgt_ip[1][0]).prefixlen),'vlan_gateway':str(ccs_connect_ip[0][3])+'/'+str((mgt_ip[1][0]).prefixlen)},'SCOA': (
            '-'.join((generation_coa_name(project), 'A02', get_coa_type(project)['name'], 'COA', '01'))),
                'SMGTIP': {'ip':str(mgt_ip[0][0][2])+'/'+str((mgt_ip[0][0]).prefixlen), 'netmask': '255.255.255.255','area0_ip':str(mgt_ip[1][0][2])+'/'+str((mgt_ip[1][0]).prefixlen),'localarea':str(mgt_ip[2][0][2])+'/'+str((mgt_ip[2][0]).prefixlen),
                     'cwl':str(mgt_ip[4][0][1])+'/'+str((mgt_ip[4][0]).prefixlen),'ccsvlan':'550','ccsip':str(ccs_connect_ip[0][2])+'/'+str((mgt_ip[0][0]).prefixlen),'vlan_gateway':str(ccs_connect_ip[0][3])+'/'+str((mgt_ip[0][0]).prefixlen)},
                'port_assign': get_coa_type(project)['port_assign']}
    return mgt_dict



# get_coa_info(network,project)