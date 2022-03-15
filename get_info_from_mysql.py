import pymysql
import ipaddress
import pypinyin
from math import ceil

db = pymysql.connect(host='119.91.102.106',user='root',password='uz8954UZN',database='building_information')
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
                mgt_ip_list.append(ip)
                doa_mgt = mgt_ip_list[1:4]
                d_xoa_mgt = mgt_ip_list[4:18]
                e_xoa_mgt = mgt_ip_list[18:32]
                v_evp_mgt = mgt_ip_list[32:46]
                w_ewl_mgt = mgt_ip_list[59:63]
            mgt_dict = {'floor':entry['floor'],'doa_mgt':doa_mgt,'d_xoa_mgt':d_xoa_mgt,'e_xoa_mgt':e_xoa_mgt,'v_evp_mgt':v_evp_mgt,'w_ewl_mgt':w_ewl_mgt}
            all_mgt_list.append(mgt_dict)
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
            # .update(device_number(entry['dpoint'],entry['epoint'],entry['vpoint'],entry['area']))
        device_number_dict_list.append(device_number_dict)
    return device_number_dict_list





def get_equipment_type():
    # for di in device_number_dict():
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
        floor_device_dict = {'DDOA':d_doa_name,'EDOA':e_doa_name,'DXOA':d_xoa_name,'EXOA':e_xoa_name,'VEVP':v_evp_name,'VEWL':v_ewl_name}
        devicelist.append(floor_device_dict)
    return devicelist


