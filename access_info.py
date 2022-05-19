import mysql_table_query
import device_name_prefix
import ipaddress
import device_port
from math import ceil


#计算每层楼接入设备数量
def device_number(dpoint,epoint,vpoint,area):
    d_xoa = ceil(dpoint/48)
    e_xoa = ceil(epoint/48)
    v_evp = ceil(vpoint/48)
    ap = ceil(area/62*0.85)
    if ap > 48:
        w_ewl = ceil(ap/48)
    else:
        w_ewl = 1
    return {'d_xoa':d_xoa,'e_xoa':e_xoa,'v_evp':v_evp,'w_ewl':w_ewl}
#
def device_number_dict(project):
    device_number_dict_list = []
    for entry in mysql_table_query.endpoint(project):
        device_number_dict = {'floor':entry['floor'],'bdr':entry['bdr']}
        device_number_dict.update(device_number(entry['dpoint'],entry['epoint'],entry['vpoint'],entry['area']))
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
def access_manage_ip(project):
    all_mgt_list = []
    for entry in mysql_table_query.ip_planning(project):
        mgt_ip_list = []
        if entry['description'] == 'MGT':
            for ip in ipaddress.IPv4Network(entry['network']):

                mgt_ip_list.append((ip,ipaddress.IPv4Network(entry['network']).netmask))
        else:
            continue
        if len(mgt_ip_list) == 64:
            default_gw = mgt_ip_list[1]
            d_xoa_mgt = mgt_ip_list[4:18]
            e_xoa_mgt = mgt_ip_list[18:32]
            v_evp_mgt = mgt_ip_list[32:46]
            w_ewl_mgt = mgt_ip_list[59:63]
        elif len(mgt_ip_list) == 32:
            default_gw = mgt_ip_list[1]
            d_xoa_mgt = mgt_ip_list[4:11]
            e_xoa_mgt = mgt_ip_list[12:19]
            v_evp_mgt = mgt_ip_list[20:27]
            w_ewl_mgt = mgt_ip_list[28:31]

        all_mgt_list.append(
            {'floor': entry['floor'],'bdr':entry['bdr'],'gw':default_gw,'DXOA': d_xoa_mgt, 'EXOA': e_xoa_mgt,
             'VEVP': v_evp_mgt, 'VEWL': w_ewl_mgt})
    return all_mgt_list

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
    for entry in generation_device_info_dict(project):
        d_xoa_name = ['-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'D',entry['xoa'],str(num).rjust(2,'0'))) for num in range (1,entry['d_xoa']+1)]
        e_xoa_name = ['-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'E',entry['xoa'],str(num).rjust(2,'0'))) for num in range (1,entry['e_xoa']+1)]
        v_evp_name = ['-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'V',entry['evp'],str(num).rjust(2,'0'))) for num in range (1,entry['v_evp']+1)]
        v_ewl_name = ['-'.join((device_name_prefix.device_prefix(mysql_table_query.workplace_info(project)[0]['city'],mysql_table_query.workplace_info(project)[0]['building_name']),('BDR'+str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'V',entry['ewl'],str(num).rjust(2,'0'))) for num in range (1,entry['w_ewl']+1)]
        floor_device_dict = {'floor':entry['floor'],'bdr':entry['bdr'],'DXOA':d_xoa_name,'EXOA':e_xoa_name,'VEVP':v_evp_name,'VEWL':v_ewl_name}
        devicelist.append(floor_device_dict)
    return devicelist

# #
def get_xoa_type(project):
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

def get_evp_type(project):
    port_assign = {'name': None, 'port_assign': None}
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'evp':
            access_type = {'supplier':entry['supplier'],'type':entry['equipment_type']}
            if access_type['supplier'] == 'cisco':
                port_assign['name'] = 'C'+str(entry['name'])
                port_assign['port_assign'] = device_port.cisco(access_type['type'])
            elif access_type['supplier'] == 'h3c':
                port_assign['name'] = 'H'+str(entry['name'])
                port_assign['port_assign'] = device_port.h3c(access_type['type'])
    return port_assign


def get_ewl_type(project):
    port_assign = {'name': None, 'port_assign': None}
    for entry in mysql_table_query.equipment_type(project):
        if entry['function'] == 'ewl':
            access_type = {'supplier':entry['supplier'],'type':entry['equipment_type']}
            if access_type['supplier'] == 'cisco':
                port_assign['name'] = 'C'+str(entry['name'])
                port_assign['port_assign'] = device_port.cisco(access_type['type'])
            elif access_type['supplier'] == 'h3c':
                port_assign['name'] = 'H'+str(entry['name'])
                port_assign['port_assign'] = device_port.h3c(access_type['type'])
    return port_assign

def get_access_info(project):
    access_list = []
    for n,m in zip(generation_floor_device_name(project),access_manage_ip(project)):
        access_dict = {'floor':n['floor'],'bdr':n['bdr'],'DXOA':[],'EXOA':[],'VEVP':[],'VEWL':[]}
        for name in n['DXOA']:
            ip_address = m['DXOA'].pop(0)
            dxoa = {'floor':n['floor'],'bdr':n['bdr'],'name':name,'ip':str(ip_address[0]),'netmask':str(ip_address[1]),'gateway':str(m['gw'][0]),'port_assign':get_xoa_type(project)['port_assign']}
            if access_dict['floor'] == dxoa['floor']:
                access_dict['DXOA'].append(dxoa)
        for name in n['EXOA']:
            ip_address = m['EXOA'].pop(0)
            exoa = {'floor': n['floor'],'bdr':n['bdr'],'name': name, 'ip': str(ip_address[0]),
                    'netmask': str(ip_address[1]),'gateway':str(m['gw'][0]), 'port_assign': get_xoa_type(project)['port_assign']}
            if access_dict['floor'] == exoa['floor']:
                access_dict['EXOA'].append(exoa)
        for name in n['VEVP']:
            ip_address = m['VEVP'].pop(0)
            vevp = {'floor': n['floor'],'bdr':n['bdr'],'name': name, 'ip': str(ip_address[0]),
                    'netmask': str(ip_address[1]),'gateway':str(m['gw'][0]), 'port_assign':get_evp_type(project)['port_assign']}
            if access_dict['floor'] == vevp['floor']:
                access_dict['VEVP'].append(vevp)
        for name in n['VEWL']:
            ip_address = m['VEWL'].pop(0)
            vewl = {'floor': n['floor'],'bdr':n['bdr'],'name': name, 'ip': str(ip_address[0]),
                    'netmask': str(ip_address[1]),'gateway':str(m['gw'][0]), 'port_assign':get_ewl_type(project)['port_assign']}
            if access_dict['floor'] == vewl['floor']:
                access_dict['VEWL'].append(vewl)
        access_list.append(access_dict)

    return access_list


