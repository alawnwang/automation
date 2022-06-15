import mysql_table_query
import ipaddress
import h3c_6520x_master_doa
import h3c_5130_xoa
import h3c_5130_evp
import h3c_5560_ewl
import config_template

project = '深圳金地威新'
#
# network = input('IP地址：')
manage_ip_list = mysql_table_query.deivce_ip(project)
network = mysql_table_query.ip_planning(project)
connect = mysql_table_query.connection(project)
endpoint = mysql_table_query.endpoint(project)



def convert_interface_name(portname):
    interface_name = None
    if 'Ten-GigabitEthernet' in portname:
        interface_name = portname.replace('Ten-GigabitEthernet','Te')
    elif 'GigabitEthernet1' in portname:
        interface_name = portname.replace('GigabitEthernet','Gi')
    elif 'Smartrate-Ethernet' in portname:
        interface_name = portname.replace('Smartrate-Ethernet','SGE')
    elif 'Bridge-Aggregation' in portname:
        interface_name = portname.replace('Bridge-Aggregation','BAGG')
    return interface_name

def basic_device_info_dict(project):
    doa_config_info = []
    manage_ip_list = mysql_table_query.deivce_ip(project)
    network = mysql_table_query.ip_planning(project)
    connect = mysql_table_query.connection(project)
    interconnection_list = []
    downlinkconnection_list = []
    uplinkconnection_list = []
    for c in connect:
        connection = {'floor': None, 'A_device': None, 'A_port': None, 'Z_device': None, 'Z_port': None}
        if '-DOA-' in c['A_device'] and '-DOA-' in c['Z_device'] :
            connection['floor'] = c['Z_floor']
            connection['A_device'] = c['A_device']
            connection['A_port'] = c['A_port']
            connection['Z_device'] = c['Z_device']
            connection['Z_port'] = c['Z_port']
            interconnection_list.append(connection)

        if '-DOA-' in c['A_device'] and '-DOA-' not in c['Z_device'] :
            connection['floor'] = c['Z_floor']
            connection['A_device'] = c['A_device']
            connection['A_port'] = c['A_port']
            connection['Z_device'] = c['Z_device']
            connection['Z_port'] = c['Z_port']
            downlinkconnection_list.append(connection)

        layer3connection = {'layer3connection':{'floor': None, 'A_device': None, 'A_port': None,'A_ipaddress':None,'Z_device': None, 'Z_port': None,'Z_ipaddress':None}}
        if '-COA' in c['A_device'] and '-DOA-' in c['Z_device']:
            layer3connection['layer3connection']['floor'] = c['Z_floor']
            layer3connection['layer3connection']['A_device'] = c['A_device']
            layer3connection['layer3connection']['A_port'] = c['A_port']
            layer3connection['layer3connection']['A_ipaddress'] = c['A_ip']
            layer3connection['layer3connection']['Z_device'] = c['Z_device']
            layer3connection['layer3connection']['Z_port'] = c['Z_port']
            layer3connection['layer3connection']['Z_ipaddress'] = c['Z_ip']
            uplinkconnection_list.append(layer3connection)

    for ip in manage_ip_list:
        interconnect = {'interconnect':[]}
        for n in interconnection_list:
            if ip['device_name'] == n['A_device'] or ip['device_name'] == n['Z_device']:
                interconnect['interconnect'].append(n)
            if ip['floor'] == n['floor'] and '-DOA' in ip['device_name']:
                ip.update(interconnect)

        d_downlinkconnect = {'downlinkconnect': []}
        e_downlinkconnect = {'downlinkconnect': []}
        for m in downlinkconnection_list:
            if '-DOA-' in ip['device_name'] and  '-D-' in ip['device_name'] and '-D-' in m['A_device'] and ip['floor'] == m['floor'] :
                d_downlinkconnect['downlinkconnect'].append(m)
                ip.update(d_downlinkconnect)
            if '-DOA-' in ip['device_name'] and  '-E-' in ip['device_name'] and '-E-' in m['A_device']  and ip['floor'] == m['floor'] :
                e_downlinkconnect['downlinkconnect'].append(m)
                ip.update(e_downlinkconnect)

        for u in uplinkconnection_list:
            if ip['device_name'] == u['layer3connection']['Z_device']:
                ip.update(u)
        networklist = []

        for n in network:
            interface_vlan = {'vlan': None, 'network': None,'func':None,'desc':None,'acl':None}
            if str(n['floor'])+str(n['bdr']) == str(ip['floor'])+str(ip['bdr']):
                interface_vlan['vlan'] = n['vlan']
                interface_vlan['network'] = n['network']
                interface_vlan['func'] = n['func']
                interface_vlan['desc'] = n['description']
                interface_vlan['acl'] = n['acl']
                networklist.append(interface_vlan)

        if '-DOA-' not in ip['device_name']:
            pass
        else:
            ip.update({'network':networklist})
            doa_config_info.append(ip)
    return doa_config_info


def floor_doa_list (project):
    for i in basic_device_info_dict(project):



def access_vlan():
    access_vlan = {'oa_access_vlan':[],'evp_access_vlan':[]}
    for i in endpoint:
        oa_device_list = []
        evp_device_list = []
        oa_vlan_list=[]
        evp_vlan_list =[]
        for entry in manage_ip_list:
            if str(entry['floor'])+str(entry['floor']) == str(i['floor'])+str(i['floor']) and 'XOA' in entry['device_name']:
                oa_device_list.append(entry['device_name'])
            if str(entry['floor']) + str(entry['floor']) == str(i['floor']) + str(i['floor']) and 'EVP' in entry['device_name']:
                evp_device_list.append(entry['device_name'])
        for entry in network:
            if str(entry['floor']) + str(entry['floor']) == str(i['floor']) + str(i['floor']):
                if entry['func'] == '有线办公网':
                    oa_vlan_list.append(entry['vlan'])
                if entry['func'] == 'VOIP网':
                    evp_vlan_list.append(entry['vlan'])


        n = len(oa_device_list)
        while n != 0:
            try:
                n = n - 1
                for i in oa_vlan_list:
                    oa_access_vlan = {'device_name': oa_device_list.pop(0), 'access_vlan': i}
                    access_vlan['oa_access_vlan'].append(oa_access_vlan)
            except IndexError:
                break



        n = len(evp_device_list)
        while n != 0:
            try:
                n = n - 1
                for i in evp_vlan_list:
                    evp_access_vlan = {'device_name': evp_device_list.pop(0), 'access_vlan': i}
                    access_vlan['evp_access_vlan'].append(evp_access_vlan)
            except IndexError:
                break
    return access_vlan

def access_device_config_info(project):

    access_config_list = []
    uplinkconnection_list = []

    for c in connect:
        connection = {'floor': None, 'A_device': None, 'A_port': None, 'Z_device': None, 'Z_port': None}
        if '-DOA-' not in c['Z_device'] and '-COA-' not in c['Z_device'] :
            connection['floor'] = c['Z_floor']
            connection['A_device'] = c['A_device']
            connection['A_port'] = c['A_port']
            connection['Z_device'] = c['Z_device']
            connection['Z_port'] = c['Z_port']
            uplinkconnection_list.append(connection)
#
    for entry in manage_ip_list:
        uplink = {'uplink': []}
        for ul in uplinkconnection_list:
            if ul['Z_device'] == entry['device_name']:
                uplink['uplink'].append(ul)
        entry.update(uplink)


    for entry in manage_ip_list:
        xoa_vlan_list = []
        evp_vlan_list = []
        ewl_vlan_list = []

        for n in network:
            lay2vlan = {'vlan': None,'func':None,'desc':None}
            if str(n['floor'])+str(n['bdr']) == str(entry['floor'])+str(entry['bdr']) and n['func'] != 'VOIP网' and n['func'] != 'AP网' and n['func'] != '核心网段':
                lay2vlan['vlan'] = n['vlan']
                lay2vlan['func'] = n['func']
                lay2vlan['desc'] = n['description']
                xoa_vlan_list.append(lay2vlan)

            if str(n['floor'])+str(n['bdr']) == str(entry['floor'])+str(entry['bdr']) and (n['func'] == '网络设备管理' or n['func'] == 'VOIP网'):
                lay2vlan['vlan'] = n['vlan']
                lay2vlan['func'] = n['func']
                lay2vlan['desc'] = n['description']
                evp_vlan_list.append(lay2vlan)

            if str(n['floor'])+str(n['bdr']) == str(entry['floor'])+str(entry['bdr'])  and (n['func'] == '网络设备管理' or n['func'] == 'AP网'):
                lay2vlan['vlan'] = n['vlan']
                lay2vlan['func'] = n['func']
                lay2vlan['desc'] = n['description']
                ewl_vlan_list.append(lay2vlan)

        if 'XOA' in entry['device_name']:
            entry.update({'vlan': xoa_vlan_list})
            for access in access_vlan()['oa_access_vlan']:
                if entry['device_name'] == access['device_name']:
                    entry.update(access)
    #
    #
    #     if 'EVP' in entry['device_name']:
    #         entry.update({'vlan':evp_vlan_list})
    #         for access in access_vlan()['evp_access_vlan']:
    #             if entry['device_name'] == access['device_name']:
    #                 entry.update(access)
    #
    #     if 'EWL' in entry['device_name']:
    #         entry.update({'vlan':ewl_vlan_list})
    #
    #     if 'COA' in entry['device_name'] or 'DOA' in entry['device_name']:
    #         pass
    #     else:
    #         access_config_list.append(entry)
    return access_config_list
access_device_config_info(project)

# for d in basic_device_info_dict(project):

