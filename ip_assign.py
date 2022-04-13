from math import ceil
import ipaddress
import mysql_table_query

def num_of_network(project):
    num_network = []
    for network in mysql_table_query.endpoint(project):
        floor_network_oa = ceil((network['dpoint'] + network['epoint']) / 240)
        floor_network_ty = ceil(floor_network_oa * 0.5)
        floor_network_voip = ceil(network['vpoint'] / 240)
        floor_network_num_dict = {'floor': network['floor'], 'bdr':network['bdr'],'mgt': 0.25, 'ap_mgt': 0.25, 'video': 0.25,
                                  'oa_device': 0.25, 'geli': 0.25, 'oa': floor_network_oa, 'ty': floor_network_ty,
                                  'voip': floor_network_voip}
        num_network.append(floor_network_num_dict)
    return num_network

def cacl_public(project):
    public_num = 0
    for public in num_of_network(project):
        num = public['mgt'] + public['ap_mgt'] + public['video'] + public['oa_device'] + public['geli']
        public_num += num
    return ceil(public_num)

def cacl_floor_bdr_num(project):
    bdr_list = []
    for mgt in mysql_table_query.endpoint(project):
        bdr_list.append('-'.join((str(mgt['floor']), str(mgt['bdr']))))
    return bdr_list

def network_class(network,project):
    pubilc_network_list = []
    ip_address = ipaddress.ip_network(network).subnets(new_prefix=24)
    mgt_ip = ip_address.__next__()
    network_class_dict = {'mgt':mgt_ip,'public':[],'normal':None}
    n = cacl_public(project)
    while n != 0:
        n = n - 1
        pubilc_network_list.append(ip_address.__next__())
    for pu in pubilc_network_list:
        for ip in ipaddress.ip_network(pu).subnets(new_prefix=26):
            network_class_dict['public'].append(ip)
    normal_network_list = []
    m = cacl_oa(project) + cacl_oa(project) + cacl_voip(project)
    while m != 0:
        m = m - 1
        normal_network_list.append(ip_address.__next__())
    network_class_dict['normal'] = (ip for ip in normal_network_list)
    return network_class_dict

def mgt_num(project):
    public_dict_list = []
    function_list = ['网络设备管理', 'AP网', '会议设备网', '行政设备网', '隔离VLAN']
    description_list = ['MGT', 'AP_MGT', 'Video', 'OA_Device', 'GELI']
    for fun,des in zip(function_list,description_list):
        for floor_bdr in cacl_floor_bdr_num(project):
            if des == 'MGT':
                vlan = 10
            elif des == 'AP_MGT':
                vlan = 11
            elif des == 'Video':
                vlan = 44
            elif des == 'OA_Device':
                vlan = 600
            elif des == 'GELI':
                vlan = 666
            floor_bdr_split = floor_bdr.split('-')
            public_dict = {'vlan': vlan, 'floor': str(floor_bdr_split[0]),'bdr':str(floor_bdr_split[1]),'network':'','fun':fun,'desc':des}
            public_dict_list.append(public_dict)
    return public_dict_list


def cacl_oa(project):
    num_oa = 0
    for oa in num_of_network(project):
        num_oa += oa['oa']
    return ceil(num_oa)

def cacl_ty(project):
    num_ty = 0
    for ty in num_of_network(project):
        num_ty += ty['ty']
    return ceil(num_ty)

def cacl_voip(project):
    num_voip = 0
    for voip in num_of_network(project):
        num_voip += voip['voip']
    return ceil(num_voip)

def generation_netwrok_dict(project):
    return {'public': cacl_public(project), 'oa': cacl_oa(project), 'ty': cacl_ty(project), 'voip': cacl_voip(project)}

class network_assign:
    def oa_network_assign(func,project):
        oa_dict_list = []
        for floor in num_of_network(project):
            vlan_oa = 19
            num = 0
            while floor['oa'] != 0:
                floor['oa'] = floor['oa'] - 1
                vlan_oa = vlan_oa + 1
                num = num + 1
                oa_dict_list.append(
                    {'vlan': vlan_oa, 'floor': str(floor['floor']),'bdr':str(floor['bdr']), 'network': func.__next__(), 'fun': '有线办公网','desc':('OA_'+str(num))})
        return oa_dict_list

    def ty_network_assign(func,project):
        ty_dict_list = []
        for floor in num_of_network(project):
            vlan_oa = 29
            num = 0
            while floor['ty'] != 0:
                floor['ty'] = floor['ty'] - 1
                vlan_oa = vlan_oa + 1
                num = num + 1
                ty_dict_list.append(
                    {'vlan': vlan_oa, 'floor': str(floor['floor']),'bdr':str(floor['bdr']), 'network': func.__next__(), 'fun': '有线体验网','desc':('TY_'+str(num))})
        return ty_dict_list

    def voip_network_assign(func,project):
        ty_dict_list = []
        for floor in num_of_network(project):
            vlan_oa = 99
            num = 0
            while floor['voip'] != 0:
                floor['voip'] = floor['voip'] - 1
                vlan_oa = vlan_oa + 1
                num = num + 1
                ty_dict_list.append(
                    {'vlan': vlan_oa, 'floor': str(floor['floor']),'bdr':str(floor['bdr']), 'network': func.__next__(), 'fun': 'VOIP网','desc':('VOIP_'+str(num))})
        return ty_dict_list
