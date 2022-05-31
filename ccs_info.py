import mysql_table_query
import device_name_prefix
import ipaddress
import ip_assign
import device_port

def generation_ccs_name(project):
    ccs_prefix = '-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),'BDR'+str(mysql_table_query.workplace_info(project)[0]['core_bdr_floor'])+'01'))
    return ccs_prefix

def get_ccs_type(project):
    port_assign = {'name':'','port_assign':None}
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'ccs':
            coa_type = {'supplier':entry['supplier'],'type':entry['equipment_type']}
            if coa_type['supplier'] == 'cisco':
                port_assign['name'] = 'C'+str(entry['name'])
                port_assign['port_assign'] = device_port.cisco(coa_type['type'])
            elif coa_type['supplier'] == 'h3c':
                port_assign['name'] = 'H'+str(entry['name'])
                port_assign['port_assign'] = device_port.h3c(coa_type['type'])
    return port_assign


def get_ccs_info(network,project):
    entry = mysql_table_query.ccs_ip(project)[0]
    mgt_ip = ipaddress.IPv4Network((entry)['network'])
    connect_ip = ip_assign.network_class(network, project)['loopback']
    ccs_fw_connect_ip = [ip for ip in ipaddress.collapse_addresses([connect_ip[6][0],connect_ip[7][0]])][0]
    ccs_connect_ip = [ip for ip in ipaddress.collapse_addresses([connect_ip[8][0],connect_ip[9][0]])][0]
    mgt_dict = {'floor': entry['floor'],'bdr':entry['bdr'],'MCCS': ('-'.join((generation_ccs_name(project), 'A01', str(get_ccs_type(project)['name']), 'CCS', '01')))
        , 'MMGTIP': {'vlan':entry['vlan'],'ip': mgt_ip[2],'hsrp':mgt_ip[1],'uplink':str(ccs_connect_ip[5])+'/'+str(ccs_connect_ip.prefixlen),'vlan_gateway':str(ccs_connect_ip[4])+'/'+str(ccs_connect_ip.prefixlen)}, 'SCCS': (
            '-'.join((generation_ccs_name(project), 'A02', get_ccs_type(project)['name'], 'CCS', '01'))),
                'SMGTIP': {'vlan':entry['vlan'],'ip': mgt_ip[3],'hsrp':mgt_ip[1],'uplink':str(ccs_connect_ip[6])+'/'+str(ccs_connect_ip.prefixlen),'vlan_gateway':str(ccs_connect_ip[4])+'/'+str(ccs_connect_ip.prefixlen)},'port_assign': get_ccs_type(project)['port_assign']}

    return mgt_dict


