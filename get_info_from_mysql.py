import ipaddr
import pymysql
import ipaddress
import pypinyin
import config_template
from math import ceil

db = pymysql.connect(host='111',user='222',password='333',database='building_information')
cursor = db.cursor(cursor=pymysql.cursors.DictCursor,)

sql = 'show tables'
cursor.execute(sql)

rs = cursor.fetchall()

project = input('项目名称:')

def get_acronym(str_data):
    return ''.join([i[0][0] for i in pypinyin.pinyin(str_data,style=pypinyin.NORMAL)])


def workplace_info(project):
    workplace_info = "select * from workplace_information where project = '%s'" %project
    cursor.execute(workplace_info)
    info_data = cursor.fetchall()
    return info_data

def ip_planning(project):
    ip_planning = "select * from ip_planning where project = '%s'" %project
    cursor.execute(ip_planning)
    ip_data = cursor.fetchall()
    return ip_data

def endpoint(project):
    endpoint = "select * from endpoint where project = '%s'" %project
    cursor.execute(endpoint)
    endpoint_data = cursor.fetchall()
    return endpoint_data

def equipment_type(project):
    equipment_type = "select * from equipment_type_version where project = '%s'" %project
    cursor.execute(equipment_type)
    equipment_data = cursor.fetchall()
    return equipment_data

def manage_ip():
    all_mgt_list = []
    for entry in ip_planning(project):
        mgt_ip_list = []
        if entry['function'] == '网络设备管理':
            mgt_network = ipaddress.IPv4Network(entry['network'])
            for ip in mgt_network:
                mgt_ip_list.append((ip,mgt_network.netmask))
                doa_mgt = mgt_ip_list[1:4]
                d_xoa_mgt = mgt_ip_list[4:18]
                e_xoa_mgt = mgt_ip_list[18:32]
                v_evp_mgt = mgt_ip_list[32:46]
                w_ewl_mgt = mgt_ip_list[59:63]
            mgt_dict = {'floor':entry['floor'],'doa_mgt':doa_mgt,'d_xoa_mgt':d_xoa_mgt,'e_xoa_mgt':e_xoa_mgt,'v_evp_mgt':v_evp_mgt,'w_ewl_mgt':w_ewl_mgt}
            all_mgt_list.append(mgt_dict)
    print(all_mgt_list)
    return all_mgt_list

def device_prefix(city,building_name):
    device_prefix = '-'.join((get_acronym(city).upper(),get_acronym(building_name).upper()))
    return device_prefix

def generation_prefix():
    for entry in workplace_info(project):
        prefix = device_prefix(entry['city'],entry['building_name'])
        return prefix

def device_number(dpoint,epoint,vpoint,area):
    doa = 2
    d_xoa = ceil(dpoint/48)
    e_xoa = ceil(epoint/48)
    v_evp = ceil(vpoint/48)
    ap = ceil(area/62*0.85)
    if ap > 48:
        w_ewl = ceil(ap/48)
    else:
        w_ewl = 1
    return {'doa':doa,'d_xoa':d_xoa,'e_xoa':e_xoa,'v_evp':v_evp,'w_ewl':w_ewl}

def device_number_dict():
    device_number_dict_list = []
    for entry in endpoint(project):
        device_number_dict = {'floor':entry['floor'],'bdr':entry['bdr']}
        device_number_dict.update(device_number(entry['dpoint'],entry['epoint'],entry['vpoint'],entry['area']))
        device_number_dict_list.append(device_number_dict)
    return device_number_dict_list





def get_equipment_type():
    type_list = []
    for entry in equipment_type(project):
        if entry['supplier'] == 'cisco':
            equipment_type_acronym = 'C'
        elif entry['supplier'] == 'hillstone':
            equipment_type_acronym = 'S'
        elif entry['supplier'] == 'h3c':
            equipment_type_acronym = 'H'
        elif entry['supplier'] == 'aruba':
            equipment_type_acronym = 'A'
        type_function = equipment_type_acronym+entry['equipment_type']+'-'+str(entry['function']).upper()
        type_dict = {entry['function']:type_function}
        type_list.append(type_dict)
    return type_list

def generation_device_info_dict():
    device_info_list = []
    for entry in device_number_dict():
        for type in get_equipment_type():
            entry.update(type)
        device_info_list.append(entry)
    return device_info_list


def generation_device_name():
    devicelist = []
    for entry in generation_device_info_dict():
        d_doa_name = '-'.join((generation_prefix(),(str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'D',entry['doa'],'01'))
        e_doa_name = '-'.join((generation_prefix(),(str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'E',entry['doa'],'01'))
        d_xoa_name = ['-'.join((generation_prefix(),(str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'D',entry['xoa'],str(num).rjust(2,'0'))) for num in range (1,entry['d_xoa']+1)]
        e_xoa_name = ['-'.join((generation_prefix(),(str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'E',entry['xoa'],str(num).rjust(2,'0'))) for num in range (1,entry['e_xoa']+1)]
        v_evp_name = ['-'.join((generation_prefix(),(str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'V',entry['evp'],str(num).rjust(2,'0'))) for num in range (1,entry['v_evp']+1)]
        v_ewl_name = ['-'.join((generation_prefix(),(str(entry['floor'])+str(entry['bdr']).rjust(2,'0')),'V',entry['ewl'],str(num).rjust(2,'0'))) for num in range (1,entry['w_ewl']+1)]
        floor_device_dict = {'floor':entry['floor'],'DDOA':d_doa_name,'EDOA':e_doa_name,'DXOA':d_xoa_name,'EXOA':e_xoa_name,'VEVP':v_evp_name,'VEWL':v_ewl_name}
        devicelist.append(floor_device_dict)
    return devicelist

def get_ip_planning_info():
    device_mgt_list = []
    for entry in ip_planning(project):
        if entry['description'] == 'MGT':
            ip_list = [ip for ip in ipaddr.IPv4Network(entry['network'])]
            d_doa_mgt = ip_list[2]
            e_doa_mgt = ip_list[3]
            d_xoa_mgt = ip_list[4:18]
            e_xoa_mgt = ip_list[18:32]
            v_evp_mgt = ip_list[32:46]
            w_ewl_mgt = ip_list[59:63]
            device_mgt_list.append({'floor':entry['floor'],'DDOA':d_doa_mgt,'EDOA':e_doa_mgt,'DXOA':d_xoa_mgt,'EXOA':e_xoa_mgt,'VEVP':v_evp_mgt,'VEWL':w_ewl_mgt})
        else:
            pass
    return device_mgt_list


for n,m in zip(get_ip_planning_info(),generation_device_name()):
    print(n['DDOA'],m['DDOA'])
    print(n['EDOA'], m['EDOA'])
    # for D in list(zip((n['DXOA']),m['DXOA'])):
    #     print(D)
    #     print(D[0],D[1],config_template.cisco.xoa_c9300_port()[0],config_template.cisco.xoa_c9300_port()[1])
    # for E in list(zip((n['EXOA']), m['EXOA'])):
    #     print(E[0],E[1],config_template.cisco.xoa_c9300_port()[0],config_template.cisco.xoa_c9300_port()[1])
    # for V in list(zip((n['VEVP']), m['VEVP'])):
    #     print(V[0],V[1],config_template.cisco.evp_c2960_port()[0],config_template.cisco.evp_c2960_port()[1])
    # for W in list(zip((n['VEWL']), m['VEWL'])):
    #     print(W[0],W[1],config_template.cisco.ewl_c3650_fd_port()[0],config_template.cisco.ewl_c3650_fd_port()[1])


    # EXOA = [EXOA for E in list(zip((n['EXOA']),m['EXOA'])) for EXOA in E]
    # VEVP = [VEVP for V in list(zip((n['VEVP']),m['VEVP'])) for VEVP in V]
    # VEWL = [VEWL for W in list(zip((n['VEWL']),m['VEWL'])) for VEWL in W]

    # print(EXOA)
    # print(VEVP)
    # print(VEWL)