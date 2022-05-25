import itertools
from math import ceil
import ipaddress
import mysql_table_query


# project = input('项目名称: ')
# #
# network = input('IP地址：')

def num_of_network(project):
    num_network = []
    for network in mysql_table_query.endpoint(project):
        floor_network_oa = ceil((network['dpoint'] + network['epoint']) / 240)
        floor_network_ty = ceil(floor_network_oa * 0.5)
        floor_network_voip = ceil(network['vpoint'] / 240)
        floor_network_num_dict = {'floor':network['floor'],'bdr':network['bdr'],'mgt':0.25,'ap_mgt':0.25,'video':0.25,
                                  'oa_device':0.25,'geli':0.25,'oa':floor_network_oa,'ty':floor_network_ty,
                                  'voip':floor_network_voip}
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

def network_class(network,project):
    pubilc_network_list = []
    pubilc_subnetwork_list = []
    core_ip_list = []
    loopback = []
    mgt_network = []
    ip_address = ipaddress.ip_network(network).subnets(new_prefix=24)
    connect_ip = (len(cacl_floor_bdr_num(project)))*8/224
    print(connect_ip)
    if connect_ip < 1:
        core_network = ip_address.__next__()
        mgt_network.append(core_network)
        for ip in core_network.subnets(new_prefix=30):
            core_ip_list.append(ip)
    else:
        numbers_of_connect_ip = ceil(connect_ip)
        while numbers_of_connect_ip != 0:
            core_network = ip_address.__next__()
            mgt_network.append(core_network)
            for ip in core_network.subnets(new_prefix=30):
                core_ip_list.append(ip)
            numbers_of_connect_ip = numbers_of_connect_ip - 1
    core_ip = itertools.product(core_ip_list)
    loopbackip = 0
    while loopbackip <= 7:
        loopback.append(core_ip.__next__())
        loopbackip = loopbackip + 1
    network_class_dict = {'mgt':mgt_network,'connection_ip':core_ip,'public':None,'normal':None}
    print(network_class_dict)
    n = cacl_public(project)
    while n != 0:
        n = n - 1
        pubilc_network_list.append(ip_address.__next__())

    for pu in pubilc_network_list:
        for ip in ipaddress.ip_network(pu).subnets(new_prefix=26):
            pubilc_subnetwork_list.append(ip)
    network_class_dict['public'] = (publicip for publicip in pubilc_subnetwork_list)
    normal_network_list = []
    for i in ip_address:
        normal_network_list.append(i)
    network_class_dict['normal'] = (ip for ip in normal_network_list)
    return network_class_dict
#
def mgt_num(project):
    public_dict_list = []
    function_list = ['网络设备管理', 'AP网', '会议设备网', '行政设备网', '隔离VLAN']
    description_list = ['MGT', 'AP-MGT', 'Video', 'OA-Device', 'GELI']
    for fun,des in zip(function_list,description_list):
        for floor_bdr in cacl_floor_bdr_num(project):
            if des == 'MGT':
                vlan = 10
            elif des == 'AP-MGT':
                vlan = 11
            elif des == 'Video':
                vlan = 44
            elif des == 'OA-Device':
                vlan = 600
            elif des == 'GELI':
                vlan = 666
            floor_bdr_split = floor_bdr.split('-')
            public_dict = {'vlan': vlan, 'floor': str(floor_bdr_split[0]),'bdr':str(floor_bdr_split[1]),'network':'','fun':fun,'desc':des}
            public_dict_list.append(public_dict)
    public_dict_generation = (p for p in public_dict_list)
    return public_dict_generation

def generation_netwrok_dict(project):
    return {'public': cacl_public(project), 'oa': cacl_oa(project), 'ty': cacl_ty(project), 'voip': cacl_voip(project)}

def network_assign(project):
    normal_network_list = []
    for floor in num_of_network(project):
        vlan_oa = 19
        num = 0
        while floor['oa'] != 0:
            floor['oa'] = floor['oa'] - 1
            vlan_oa = vlan_oa + 1
            num = num + 1
            normal_network_list.append(
                {'vlan': vlan_oa, 'floor': str(floor['floor']),'bdr':str(floor['bdr']), 'network':None, 'fun': '有线办公网','desc':('OA-'+str(num))})

    for floor in num_of_network(project):
        vlan_oa = 29
        num = 0
        while floor['ty'] != 0:
            floor['ty'] = floor['ty'] - 1
            vlan_oa = vlan_oa + 1
            num = num + 1
            normal_network_list.append(
                {'vlan': vlan_oa, 'floor': str(floor['floor']),'bdr':str(floor['bdr']), 'network': None, 'fun': '有线体验网','desc':('TY-'+str(num))})

    for floor in num_of_network(project):
        vlan_oa = 99
        num = 0
        while floor['voip'] != 0:
            floor['voip'] = floor['voip'] - 1
            vlan_oa = vlan_oa + 1
            num = num + 1
            normal_network_list.append(
                {'vlan': vlan_oa, 'floor': str(floor['floor']),'bdr':str(floor['bdr']), 'network': None, 'fun': 'VOIP网','desc':('VOIP-'+str(num))})

    normal_network_info = (i for i in normal_network_list)
    return normal_network_info



def acl(ipinfo):
    acl = ''
    if ipinfo == 'AP网':
        acl = 'AP'
    elif ipinfo == '会议设备网':
        acl = 'Video'
    elif ipinfo == '行政设备网':
        acl = 'OA-Device'
    elif ipinfo == '隔离VLAN':
        acl = 'GELI'
    elif ipinfo == '有线办公网':
        acl = 'OA'
    elif ipinfo == '有线体验网':
        acl = 'TY'
    elif ipinfo == 'VOIP网':
        acl = 'VOIP'
    return acl
#
def generation_ip_planning(network,project):
    ip_planning_list = []
    # #IP规划
    core_ipaddress = network_class(network,project)['mgt']
    core_network = len(core_ipaddress)
    core_bdr_floor = mysql_table_query.workplace_info(project).pop(0)['core_bdr_floor']
    if core_network <= 1:
        ip_planning_list.append({'network':[core_ipaddress],'status':'启用','domain':None,'vlan':None,'func':['核心网段'],'description':['interconnection'],'acl':None,'project':project,'building_name':None,'floor':[core_bdr_floor],'bdr':[1]})
    else:
        for n in core_ipaddress:
            core_ip_dict = {'network': [n], 'status': '启用', 'domain': None, 'vlan': None, 'func': ['核心网段'],
                            'description': ['interconnection'], 'acl': None, 'project': project, 'building_name': None,
                            'floor': [core_bdr_floor], 'bdr': [1]}
            ip_planning_list.append(core_ip_dict)


    public_dic = mgt_num(project)
    public_network_list = network_class(network, project)['public']
    for n in public_network_list:
        try:
            public_network_basic_info = public_dic.__next__()
            public_ip = {'network': [ipaddress.ip_network(n)], 'status': '启用', 'domain': None,
                         'vlan': [public_network_basic_info['vlan']], 'func': [public_network_basic_info['fun']], 'description': [public_network_basic_info['desc']], 'acl': acl(public_network_basic_info['fun']),
                         'project': project, 'building_name': None, 'floor': [public_network_basic_info['floor']], 'bdr': [public_network_basic_info['bdr']]}
            ip_planning_list.append(public_ip)
        except StopIteration:
            public_ip = {'network': [ipaddress.ip_network(n)], 'status': '未启用', 'domain': None,
                         'vlan': None, 'func': None, 'description':None, 'acl': None,
                         'project': project, 'building_name': None, 'floor':None, 'bdr': None}
            ip_planning_list.append(public_ip)
    normal_dic = network_assign(project)
    normal_network_list = network_class(network,project)['normal']
    for norip in normal_network_list:
        try:
            normal_network_basic_info = normal_dic.__next__()
            normal_ip = {'network': [ipaddress.ip_network(norip)], 'status': '启用', 'domain': None, 'vlan': [normal_network_basic_info['vlan']], 'func': [normal_network_basic_info['fun']],
                         'description': [normal_network_basic_info['desc']],'acl':acl(normal_network_basic_info['fun']),'project': project, 'building_name': None, 'floor': [normal_network_basic_info['floor']],
                         'bdr': [normal_network_basic_info['bdr']]}
            ip_planning_list.append(normal_ip)
        except StopIteration:
            pass
            normal_ip = {'network': [ipaddress.ip_network(norip)], 'status': '未启用', 'domain': None,
                         'vlan': None, 'func': None, 'description':None, 'acl': None,
                         'project': project, 'building_name': None, 'floor':None, 'bdr': None}

            ip_planning_list.append(normal_ip)
    return ip_planning_list

