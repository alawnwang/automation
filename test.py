import mysql_table_query
import ipaddress
import h3c_6520x_master_doa
import h3c_5130_xoa
import h3c_5130_evp
import h3c_5560_ewl
import config_template
import queue
import threading

project = '深圳光启未来'
#
# network = input('IP地址：')
manage_ip_list = mysql_table_query.deivce_ip(project)
network = mysql_table_query.ip_planning(project)
connect = mysql_table_query.connection(project)
endpoint = mysql_table_query.endpoint(project)



def convert_interface_name(portname):
    interface_name = None
    if 'Ten-GigabitEthernet' in portname:
        interface_name = portname.replace('Ten-GigabitEthernet','T')
    elif 'GigabitEthernet1' in portname:
        interface_name = portname.replace('GigabitEthernet','G')
    elif 'Smartrate-Ethernet' in portname:
        interface_name = portname.replace('Smartrate-Ethernet','SGE')
    elif 'Bridge-Aggregation' in portname:
        interface_name = portname.replace('Bridge-Aggregation','BAGG')
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

basic_device_info_dict(project)


def generation_doa_config(project):
    core_network = mysql_table_query.core_ip(project)
    ospf_area = ipaddress.IPv4Network(core_network[0]['network']).network_address
    for entry in basic_device_info_dict(project):
        print(entry)
        if '-D-' in entry['device_name']:
            with open('/Users/alawn/Desktop/config/' + str(entry['mgtip'] + '_' + entry['device_name']) + '.cfg',
                      'a+') as config:
                config.seek(0,0)
                def packet_filter():
                    packet_filter=[]
                    for n in entry['network']:
                        if n['func'] == '核心网段' or n['vlan'] == '10' or n['acl'] == '' or n['acl'] == 'None':
                            pass
                        else:
                            packet_filter.append(config_template.h3c_port_config_template.gloabl_acl().render(acl_name=n['acl'],
                                                                                                      vlan_num=n['vlan']))
                    return ''.join(packet_filter).lstrip('\n')
                def undo_slicent_interface():
                    undo_slicent_interface = []
                    for n in entry['network']:
                        if n['desc'] == 'MGT':
                            undo_slicent_interface.append(config_template.route_config.undo_silcent().render(
                                interconnect_interface=entry['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan'])))
                    return ''.join(undo_slicent_interface).lstrip()
                def ospf_network():
                    ospf_netowrk = []
                    for n in entry['network']:
                        if n['func'] == '核心网段' or n['func'] == '智能控制管理网' or n['func'] == '无线核心管理段' or n['func'] == '智能控制网':
                            pass
                        else:
                            network = config_template.route_config.network().render(
                                ipaddress=str(ipaddress.ip_network(n['network'])[2]))
                            ospf_netowrk.append(network)
                    ospf_netowrk.append(config_template.route_config.network().render(ipaddress=str(ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).ip)))
                    return ''.join(ospf_netowrk).lstrip()

                def layer2_vlan():
                    layer2vlan=[]
                    for n in entry['network']:
                        if n['func'] == '核心网段' or n['func'] == '智能控制管理网' or n['func'] == '无线核心管理段' or n['func'] == '智能控制网':
                            pass
                        else:
                            vlan = config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc'])
                            layer2vlan.append(vlan)
                    return ''.join(layer2vlan).lstrip()

                def interconnect_port():
                    interconnect_port = []
                    for n in entry['interconnect']:
                        interconnect_port.append(n['Z_port'])
                    return interconnect_port


                def layer3_interface_vlan():
                    all_ap_dhcp = str(mysql_table_query.dhcp(project)[0]['AP_dhcp']).split(';')
                    all_video_dhcp = str(mysql_table_query.dhcp(project)[0]['Video_dhcp']).split(';')
                    all_oadevice_dhcp = str(mysql_table_query.dhcp(project)[0]['OA-Device_dhcp']).split(';')
                    all_geli_dhcp = str(mysql_table_query.dhcp(project)[0]['GELI_dhcp']).split(';')
                    all_oa_dhcp = str(mysql_table_query.dhcp(project)[0]['OA_dhcp']).split(';')
                    all_ty_dhcp = str(mysql_table_query.dhcp(project)[0]['TY_dhcp']).split(';')
                    all_voip_dhcp = str(mysql_table_query.dhcp(project)[0]['VOIP_dhcp']).split(';')
                    layer3_vlan = []
                    for n in entry['network']:
                        if n['func'] == '网络设备管理':
                            mgt_vlan = config_template.h3c_port_config_template.vlan10_mater_interface_vlan_config().render(interface_vlan=n['vlan'], vlan_des=n['desc'],vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,vlan_num=str(n['vlan']),vrrp_ip=ipaddress.ip_network(n['network'])[1])
                            layer3_vlan.append(mgt_vlan)
                        elif n['func'] == 'AP网':
                            ap_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=str(n['vlan']),vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(ap_vlan)
                            for dhcp in all_ap_dhcp:
                                ap_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(ap_dhcp)
                        elif n['func'] == '会议设备网':
                            video_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=str(n['vlan']),vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(video_vlan)
                            for dhcp in all_video_dhcp:
                                video_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(video_dhcp)
                        elif n['func'] == '行政设备网':
                            if int(n['vlan']) > 254:
                                vrrp_num = n['vlan'][0:2]
                            else:
                                vrrp_num = n['vlan']
                            oa_device_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=vrrp_num,
                                    vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl'])
                            layer3_vlan.append(oa_device_vlan)
                            for dhcp in all_oadevice_dhcp:
                                oa_device_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(oa_device_dhcp)
                        elif n['func'] == '隔离VLAN':
                            if int(n['vlan']) > 254:
                                vrrp_num = n['vlan'][0:2]
                            else:
                                vrrp_num = n['vlan']
                            geli_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=vrrp_num,vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(geli_vlan)
                            for dhcp in all_geli_dhcp:
                                geli_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(geli_dhcp)
                        elif n['func'] == '有线办公网':
                            oa_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=str(n['vlan']),vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(oa_vlan)

                            for dhcp in all_oa_dhcp:
                                oa_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(oa_dhcp)


                        elif n['func'] == '有线体验网':
                            ty_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=str(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(ty_vlan)
                            for dhcp in all_ty_dhcp:
                                ty_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(ty_dhcp)
                        elif n['func'] == 'VOIP网':
                            voip_vlan = config_template.h3c_port_config_template.global_voip_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vrrp_num=str(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(voip_vlan)
                            for dhcp in all_voip_dhcp:
                                voip_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(voip_dhcp)
                        else:
                            pass
                    return ''.join(layer3_vlan).lstrip()

                def d_downlink_layer2_interface():
                    h6520x_d_down_link_port_list = ['Ten-GigabitEthernet1/0/1', 'Ten-GigabitEthernet1/0/2',
                                                    'Ten-GigabitEthernet1/0/3', 'Ten-GigabitEthernet1/0/4',
                                                    'Ten-GigabitEthernet1/0/5', 'Ten-GigabitEthernet1/0/6',
                                                    'Ten-GigabitEthernet1/0/7', 'Ten-GigabitEthernet1/0/8',
                                                    'Ten-GigabitEthernet1/0/9', 'Ten-GigabitEthernet1/0/10',
                                                    'Ten-GigabitEthernet1/0/11', 'Ten-GigabitEthernet1/0/12',
                                                    'Ten-GigabitEthernet1/0/13', 'Ten-GigabitEthernet1/0/14']
                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    d_down_link_config = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    for n in entry['downlinkconnect']:
                        if '-D-' in n['Z_device'] and '-XOA-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])

                    for i in h6520x_d_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(phy_interface=i,description=str(Z_device_gener.__next__())+'-'+convert_interface_name(str(Z_port_gener.__next__())))
                            d_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(phy_interface=i)
                            d_down_link_config.append(interface)
                    return ''.join(d_down_link_config).lstrip()
                d_downlink_layer2_interface()

                def e_downlink_layer2_interface():
                    h6520x_e_down_link_port_list = ['Ten-GigabitEthernet1/0/15', 'Ten-GigabitEthernet1/0/16',
                                                    'Ten-GigabitEthernet1/0/17', 'Ten-GigabitEthernet1/0/18',
                                                    'Ten-GigabitEthernet1/0/19', 'Ten-GigabitEthernet1/0/20',
                                                    'Ten-GigabitEthernet1/0/21', 'Ten-GigabitEthernet1/0/22',
                                                    'Ten-GigabitEthernet1/0/23', 'Ten-GigabitEthernet1/0/24',
                                                    'Ten-GigabitEthernet1/0/25', 'Ten-GigabitEthernet1/0/26',
                                                    'Ten-GigabitEthernet1/0/27', 'Ten-GigabitEthernet1/0/28']
                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    e_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-E-' in n['Z_device'] and '-XOA-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_e_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(
                                phy_interface=i,
                                description=str(Z_device_gener.__next__()) + '-' + convert_interface_name(
                                    str(Z_port_gener.__next__())))
                            e_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                                phy_interface=i)
                            e_down_link_config.append(interface)
                    return ''.join(e_down_link_config).lstrip()

                def v_downlink_layer2_interface():
                    h6520x_v_down_link_port_list = ['Ten-GigabitEthernet1/0/29', 'Ten-GigabitEthernet1/0/30',
                                                    'Ten-GigabitEthernet1/0/31', 'Ten-GigabitEthernet1/0/32',
                                                    'Ten-GigabitEthernet1/0/33', 'Ten-GigabitEthernet1/0/34',
                                                    'Ten-GigabitEthernet1/0/35', 'Ten-GigabitEthernet1/0/36',
                                                    'Ten-GigabitEthernet1/0/37', 'Ten-GigabitEthernet1/0/38',
                                                    'Ten-GigabitEthernet1/0/39', 'Ten-GigabitEthernet1/0/40',
                                                    'Ten-GigabitEthernet1/0/41', 'Ten-GigabitEthernet1/0/42']

                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    v_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-V-' in n['Z_device'] and '-EVP-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_v_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.voip_lay2_phy_interface_config().render(
                                phy_interface=i,
                                description=str(Z_device_gener.__next__()) + '-' + convert_interface_name(
                                    str(Z_port_gener.__next__())))
                            v_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                                phy_interface=i)
                            v_down_link_config.append(interface)
                    return ''.join(v_down_link_config).lstrip()

                def w_downlink_layer2_interface():
                    h6520x_w_down_link_port_list = ['Ten-GigabitEthernet1/0/49:2', 'Ten-GigabitEthernet1/0/49:3',
                                                    'Ten-GigabitEthernet1/0/49:4', 'Ten-GigabitEthernet1/0/50:1',
                                                    'Ten-GigabitEthernet1/0/50:2', 'Ten-GigabitEthernet1/0/50:3',
                                                    'Ten-GigabitEthernet1/0/50:4', 'Ten-GigabitEthernet1/0/51:1',
                                                    'Ten-GigabitEthernet1/0/51:2', 'Ten-GigabitEthernet1/0/51:3',
                                                    'Ten-GigabitEthernet1/0/51:4', 'Ten-GigabitEthernet1/0/52:1',
                                                    'Ten-GigabitEthernet1/0/52:2', 'Ten-GigabitEthernet1/0/52:3',
                                                    'Ten-GigabitEthernet1/0/52:4']

                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    w_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-V-' in n['Z_device'] and '-EWL-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_w_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.voip_lay2_phy_interface_config().render(
                                phy_interface=i,
                                description=str(Z_device_gener.__next__()) + '-' + convert_interface_name(
                                    str(Z_port_gener.__next__())))
                            w_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                                phy_interface=i)
                            w_down_link_config.append(interface)
                    return ''.join(w_down_link_config).lstrip()

                def login_acl(project):
                    core_network = mysql_table_query.core_ip(project)
                    core_ipaddress_list = []
                    login_acl = []
                    for acl in core_network:
                        core_ipaddress_list.append(ipaddress.IPv4Network(acl['network']))
                    for network in ipaddress.collapse_addresses(core_ipaddress_list):
                        logacl = '\n'+' rule permit soure ' + str(
                            network.network_address) + ' ' + str(
                            network.hostmask)
                        login_acl.append(logacl)
                    return ''.join(login_acl).lstrip()

                config.write(h3c_6520x_master_doa.h3c_6520x_master_doa().render(sysname=entry['device_name'],packet_filter=packet_filter(),
                                                                                router_id=entry['mgtip'],undo_silent_interface=undo_slicent_interface(),
                                                                                area_id=ospf_area,ospf_network=ospf_network(),layer2_vlan=layer2_vlan(),
                                                                                interconnect_device=entry['interconnect'][0]['Z_device'],
                                                                                interconnect_bagg_port=convert_interface_name(interconnect_port()[0]),
                                                                                layer3_interface_vlan=layer3_interface_vlan(),
                                                                                uplink_device_name=entry['layer3connection']['A_device'],
                                                                                uplink_port_num=convert_interface_name(entry['layer3connection']['A_port']),
                                                                                uplink_address=ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).ip,
                                                                                uplink_netmask=ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).netmask,
                                                                                d_downlink_layer2_interface=d_downlink_layer2_interface(),
                                                                                e_downlink_layer2_interafce=e_downlink_layer2_interface(),
                                                                                v_downlink_layer2_interafce=v_downlink_layer2_interface(),
                                                                                w_downlink_layer2_interafce=w_downlink_layer2_interface(),
                                                                                interconnect_phyical_port1=convert_interface_name(interconnect_port()[1]),
                                                                                interconnect_phyical_port2=convert_interface_name(interconnect_port()[2]),
                                                                                console_password='123456',local_manage_network=login_acl(project),
                                                                                manage_ip=entry['mgtip'],local_user_password='123456'))
        if '-E-' in entry['device_name']:
            with open('/Users/alawn/Desktop/config/' + str(entry['mgtip'] + '_' + entry['device_name']) + '.cfg',
                      'a+') as config:
                def packet_filter():
                    packet_filter=[]
                    for n in entry['network']:
                        if n['func'] == '核心网段' or n['vlan'] == '10' or n['acl'] == '' or n['acl'] == 'None':
                            pass
                        else:
                            packet_filter.append(config_template.h3c_port_config_template.gloabl_acl().render(acl_name=n['acl'],
                                                                                                      vlan_num=n['vlan']))
                    return ''.join(packet_filter).lstrip('\n')
                def undo_slicent_interface():
                    undo_slicent_interface = []
                    for n in entry['network']:
                        if n['desc'] == 'MGT':
                            undo_slicent_interface.append(config_template.route_config.undo_silcent().render(
                                interconnect_interface=entry['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan'])))
                    return ''.join(undo_slicent_interface).lstrip()
                def ospf_network():
                    ospf_netowrk = []
                    for n in entry['network']:
                        if n['func'] == '核心网段' or n['func'] == '智能控制管理网' or n['func'] == '无线核心管理段' or n['func'] == '智能控制网':
                            pass
                        else:
                            network = config_template.route_config.network().render(
                                ipaddress=str(ipaddress.ip_network(n['network'])[3]))
                            ospf_netowrk.append(network)
                    ospf_netowrk.append(config_template.route_config.network().render(ipaddress=str(ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).ip)))
                    return ''.join(ospf_netowrk).lstrip()

                def layer2_vlan():
                    layer2vlan=[]
                    for n in entry['network']:
                        if n['func'] == '核心网段' or n['func'] == '智能控制管理网' or n['func'] == '无线核心管理段' or n['func'] == '智能控制网':
                            pass
                        else:
                            vlan = config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc'])
                            layer2vlan.append(vlan)
                    return ''.join(layer2vlan).lstrip()

                def interconnect_port():
                    interconnect_port = []
                    for n in entry['interconnect']:
                        interconnect_port.append(n['Z_port'])
                    return interconnect_port

                def layer3_interface_vlan():
                    all_ap_dhcp = str(mysql_table_query.dhcp(project)[0]['AP_dhcp']).split(';')
                    all_video_dhcp = str(mysql_table_query.dhcp(project)[0]['Video_dhcp']).split(';')
                    all_oadevice_dhcp = str(mysql_table_query.dhcp(project)[0]['OA-Device_dhcp']).split(';')
                    all_geli_dhcp = str(mysql_table_query.dhcp(project)[0]['GELI_dhcp']).split(';')
                    all_oa_dhcp = str(mysql_table_query.dhcp(project)[0]['OA_dhcp']).split(';')
                    all_ty_dhcp = str(mysql_table_query.dhcp(project)[0]['TY_dhcp']).split(';')
                    all_voip_dhcp = str(mysql_table_query.dhcp(project)[0]['VOIP_dhcp']).split(';')
                    layer3_vlan = []
                    for n in entry['network']:
                        if n['func'] == '网络设备管理':
                            mgt_vlan = config_template.h3c_port_config_template.vlan10_slaver_interface_vlan_config().render(interface_vlan=n['vlan'], vlan_des=n['desc'],vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1])
                            layer3_vlan.append(mgt_vlan)
                        elif n['func'] == 'AP网':
                            ap_vlan = config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(ap_vlan)
                            for dhcp in all_ap_dhcp:
                                ap_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(ap_dhcp)
                        elif n['func'] == '会议设备网':
                            video_vlan = config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(video_vlan)
                            for dhcp in all_video_dhcp:
                                video_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(video_dhcp)
                        elif n['func'] == '行政设备网':
                            if int(n['vlan']) > 254:
                                vrrp_num = n['vlan'][0:2]
                            else:
                                vrrp_num = n['vlan']
                            oa_device_vlan = config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_num=vrrp_num,
                                    vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl'])
                            layer3_vlan.append(oa_device_vlan)
                            for dhcp in all_oadevice_dhcp:
                                oa_device_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(oa_device_dhcp)
                        elif n['func'] == '隔离VLAN':
                            geli_vlan = config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(geli_vlan)
                            for dhcp in all_geli_dhcp:
                                geli_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(geli_dhcp)
                        elif n['func'] == '有线办公网':
                            oa_vlan = config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(oa_vlan)

                            for dhcp in all_oa_dhcp:
                                oa_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(oa_dhcp)


                        elif n['func'] == '有线体验网':
                            ty_vlan = config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(ty_vlan)
                            for dhcp in all_ty_dhcp:
                                ty_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(ty_dhcp)
                        elif n['func'] == 'VOIP网':
                            voip_vlan = config_template.h3c_port_config_template.global_voip_slaver_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
                                    acl_name=n['acl'])
                            layer3_vlan.append(voip_vlan)
                            for dhcp in all_voip_dhcp:
                                voip_dhcp = config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp)
                                layer3_vlan.append(voip_dhcp)
                        else:
                            pass
                    return ''.join(layer3_vlan).lstrip()

                def d_downlink_layer2_interface():
                    h6520x_d_down_link_port_list = ['Ten-GigabitEthernet1/0/1', 'Ten-GigabitEthernet1/0/2',
                                                    'Ten-GigabitEthernet1/0/3', 'Ten-GigabitEthernet1/0/4',
                                                    'Ten-GigabitEthernet1/0/5', 'Ten-GigabitEthernet1/0/6',
                                                    'Ten-GigabitEthernet1/0/7', 'Ten-GigabitEthernet1/0/8',
                                                    'Ten-GigabitEthernet1/0/9', 'Ten-GigabitEthernet1/0/10',
                                                    'Ten-GigabitEthernet1/0/11', 'Ten-GigabitEthernet1/0/12',
                                                    'Ten-GigabitEthernet1/0/13', 'Ten-GigabitEthernet1/0/14']

                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    d_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-D-' in n['Z_device'] and '-XOA-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_d_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(phy_interface=i,description=str(Z_device_gener.__next__())+'-'+convert_interface_name(str(Z_port_gener.__next__())))
                            d_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(phy_interface=i)
                            d_down_link_config.append(interface)
                    return ''.join(d_down_link_config).lstrip()


                def e_downlink_layer2_interface():
                    h6520x_e_down_link_port_list = ['Ten-GigabitEthernet1/0/15', 'Ten-GigabitEthernet1/0/16',
                                                    'Ten-GigabitEthernet1/0/17', 'Ten-GigabitEthernet1/0/18',
                                                    'Ten-GigabitEthernet1/0/19', 'Ten-GigabitEthernet1/0/20',
                                                    'Ten-GigabitEthernet1/0/21', 'Ten-GigabitEthernet1/0/22',
                                                    'Ten-GigabitEthernet1/0/23', 'Ten-GigabitEthernet1/0/24',
                                                    'Ten-GigabitEthernet1/0/25', 'Ten-GigabitEthernet1/0/26',
                                                    'Ten-GigabitEthernet1/0/27', 'Ten-GigabitEthernet1/0/28']
                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    e_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-E-' in n['Z_device'] and '-XOA-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_e_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(
                                phy_interface=i,
                                description=str(Z_device_gener.__next__()) + '-' + convert_interface_name(
                                    str(Z_port_gener.__next__())))
                            e_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                                phy_interface=i)
                            e_down_link_config.append(interface)
                    return ''.join(e_down_link_config).lstrip()

                def v_downlink_layer2_interface():
                    h6520x_v_down_link_port_list = ['Ten-GigabitEthernet1/0/29', 'Ten-GigabitEthernet1/0/30',
                                                    'Ten-GigabitEthernet1/0/31', 'Ten-GigabitEthernet1/0/32',
                                                    'Ten-GigabitEthernet1/0/33', 'Ten-GigabitEthernet1/0/34',
                                                    'Ten-GigabitEthernet1/0/35', 'Ten-GigabitEthernet1/0/36',
                                                    'Ten-GigabitEthernet1/0/37', 'Ten-GigabitEthernet1/0/38',
                                                    'Ten-GigabitEthernet1/0/39', 'Ten-GigabitEthernet1/0/40',
                                                    'Ten-GigabitEthernet1/0/41', 'Ten-GigabitEthernet1/0/42']
                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    v_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-V-' in n['Z_device'] and '-EVP-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_v_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.voip_lay2_phy_interface_config().render(
                                phy_interface=i,
                                description=str(Z_device_gener.__next__()) + '-' + convert_interface_name(
                                    str(Z_port_gener.__next__())))
                            v_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                                phy_interface=i)
                            v_down_link_config.append(interface)
                    return ''.join(v_down_link_config).lstrip()

                def w_downlink_layer2_interface():
                    h6520x_w_down_link_port_list = ['Ten-GigabitEthernet1/0/49:2', 'Ten-GigabitEthernet1/0/49:3',
                                                    'Ten-GigabitEthernet1/0/49:4', 'Ten-GigabitEthernet1/0/50:1',
                                                    'Ten-GigabitEthernet1/0/50:2', 'Ten-GigabitEthernet1/0/50:3',
                                                    'Ten-GigabitEthernet1/0/50:4', 'Ten-GigabitEthernet1/0/51:1',
                                                    'Ten-GigabitEthernet1/0/51:2', 'Ten-GigabitEthernet1/0/51:3',
                                                    'Ten-GigabitEthernet1/0/51:4', 'Ten-GigabitEthernet1/0/52:1',
                                                    'Ten-GigabitEthernet1/0/52:2', 'Ten-GigabitEthernet1/0/52:3',
                                                    'Ten-GigabitEthernet1/0/52:4']

                    downlink_list = []
                    Z_device = []
                    Z_port = []
                    Z_device_gener = (g for g in Z_device)
                    Z_port_gener = (p for p in Z_port)
                    w_down_link_config = []
                    for n in entry['downlinkconnect']:
                        if '-V-' in n['Z_device'] and '-EWL-' in n['Z_device']:
                            downlink_list.append(n['A_port'])
                            Z_device.append(n['Z_device'])
                            Z_port.append(n['Z_port'])
                    for i in h6520x_w_down_link_port_list:
                        if i in downlink_list:
                            interface = config_template.h3c_port_config_template.voip_lay2_phy_interface_config().render(
                                phy_interface=i,
                                description=str(Z_device_gener.__next__()) + '-' + convert_interface_name(
                                    str(Z_port_gener.__next__())))
                            w_down_link_config.append(interface)
                        else:
                            interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                                phy_interface=i)
                            w_down_link_config.append(interface)
                    return ''.join(w_down_link_config).lstrip()

                def login_acl(project):
                    core_network = mysql_table_query.core_ip(project)
                    core_ipaddress_list = []
                    login_acl = []
                    for acl in core_network:
                        core_ipaddress_list.append(ipaddress.IPv4Network(acl['network']))
                    for network in ipaddress.collapse_addresses(core_ipaddress_list):
                        logacl = '\n'+' rule permit soure ' + str(
                            network.network_address) + ' ' + str(
                            network.hostmask)
                        login_acl.append(logacl)
                    return ''.join(login_acl).lstrip()

                config.write(h3c_6520x_master_doa.h3c_6520x_master_doa().render(sysname=entry['device_name'],packet_filter=packet_filter(),
                                                                                router_id=entry['mgtip'],undo_silent_interface=undo_slicent_interface(),
                                                                                area_id=ospf_area,ospf_network=ospf_network(),layer2_vlan=layer2_vlan(),
                                                                                interconnect_device=entry['interconnect'][0]['A_device'],
                                                                                interconnect_bagg_port=convert_interface_name(interconnect_port()[0]),
                                                                                layer3_interface_vlan=layer3_interface_vlan(),
                                                                                uplink_device_name=entry['layer3connection']['A_device'],
                                                                                uplink_port_num=convert_interface_name(entry['layer3connection']['A_port']),
                                                                                uplink_address=ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).ip,
                                                                                uplink_netmask=ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).netmask,
                                                                                d_downlink_layer2_interface=d_downlink_layer2_interface(),
                                                                                e_downlink_layer2_interafce=e_downlink_layer2_interface(),
                                                                                v_downlink_layer2_interafce=v_downlink_layer2_interface(),
                                                                                w_downlink_layer2_interafce=w_downlink_layer2_interface(),
                                                                                interconnect_phyical_port1=convert_interface_name(interconnect_port()[1]),
                                                                                interconnect_phyical_port2=convert_interface_name(interconnect_port()[2]),
                                                                                console_password='123456',local_manage_network=login_acl(project),
                                                                                manage_ip=entry['mgtip'],local_user_password='123456'))





def doa_config():
    doa_config_list = []
    for network in basic_device_info_dict(project):
        doa_config_list.append(network)
    return doa_config_list

def access_uplink():
    access_uplink = []
    uplinkconnection_list = []
    for c in connect:
        connection = {'floor': None, 'A_device': None, 'A_port': None, 'Z_device': None, 'Z_port': None}
        if '-DOA-' not in c['Z_device'] and '-COA-' not in c['Z_device']:
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
        access_uplink.append(entry)
    return access_uplink



def access_vlan():
    doa_config_list = doa_config()
    access_uplink_list = access_uplink()
    access_vlan = {'oa_access_vlan':[],'evp_access_vlan':[]}
    for i in endpoint:
        oa_device_list = []
        evp_device_list = []
        oa_vlan_list=[]
        evp_vlan_list =[]
        for entry in access_uplink_list:
            uplink = None
            for device in doa_config_list:
                if entry['uplink'] != []:
                    uplink = entry['uplink'][0]['A_device']
                else:
                    pass
                if uplink == device['device_name'] and 'XOA' in entry['device_name']:
                    oa_device_list.append(entry['device_name'])
                if uplink == device['device_name'] and 'EVP' in entry['device_name']:
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


def access_device_config_info():
    doa_config_list = doa_config()

    access_config_list = []
    access_uplink_list = access_uplink()
    for entry in access_uplink_list:
        xoa_vlan_list = []
        evp_vlan_list = []
        ewl_vlan_list = []

        uplink = None
        for network in doa_config_list:
            if entry['uplink'] != []:
                uplink = entry['uplink'][0]['A_device']
            else:
                pass
            if uplink == network['device_name']:
                for vlan in network['network']:
                    lay2vlan = {'vlan': None,'func':None,'desc':None}
                    if vlan['func'] != 'VOIP网' and vlan['func'] != 'AP网' and vlan['func'] != '核心网段':
                        lay2vlan['vlan'] = vlan['vlan']
                        lay2vlan['func'] = vlan['func']
                        lay2vlan['desc'] = vlan['desc']
                        xoa_vlan_list.append(lay2vlan)

                    if vlan['func'] == '网络设备管理' or vlan['func'] == 'VOIP网':
                        lay2vlan['vlan'] = vlan['vlan']
                        lay2vlan['func'] = vlan['func']
                        lay2vlan['desc'] = vlan['desc']
                        evp_vlan_list.append(lay2vlan)

                    if vlan['func'] == '网络设备管理' or vlan['func'] == 'AP网':
                        lay2vlan['vlan'] = vlan['vlan']
                        lay2vlan['func'] = vlan['func']
                        lay2vlan['desc'] = vlan['desc']
                        ewl_vlan_list.append(lay2vlan)

        if 'XOA' in entry['device_name']:
            entry.update({'vlan': xoa_vlan_list})
            for access in access_vlan()['oa_access_vlan']:
                if entry['device_name'] == access['device_name']:
                    entry.update(access)

        if 'EVP' in entry['device_name']:
            entry.update({'vlan':evp_vlan_list})
            for access in access_vlan()['evp_access_vlan']:
                if entry['device_name'] == access['device_name']:
                    entry.update(access)

        if 'EWL' in entry['device_name']:
            entry.update({'vlan':ewl_vlan_list})

        if 'COA' in entry['device_name'] or 'DOA' in entry['device_name']:
            pass
        else:
            access_config_list.append(entry)
    return access_config_list

def generation_access_config_file(project):
    access_config = access_device_config_info()
    for a in access_config:
        if '-XL-' in a['device_name'] or '-CCS-' in a['device_name']:
            pass
        else:
            with open('/Users/alawn/Desktop/config/'+str(a['mgtip']+'_'+a['device_name'])+'.cfg','a+') as config:
                def login_acl(project):
                    core_network = mysql_table_query.core_ip(project)
                    core_ipaddress_list = []
                    login_acl = []
                    for acl in core_network:
                        core_ipaddress_list.append(ipaddress.IPv4Network(acl['network']))
                    for network in ipaddress.collapse_addresses(core_ipaddress_list):
                        logacl = '\n'+' rule permit soure ' + str(
                            network.network_address) + ' ' + str(
                            network.hostmask)
                        login_acl.append(logacl)
                    return ''.join(login_acl).lstrip()

                def layer2_vlan():
                    layer2_vlan_list = []
                    for vlan in a['vlan']:
                        if vlan['func'] == '有线办公网' or vlan['func'] == '有线体验网':
                            vlan_config = config_template.h3c_port_config_template.vlan_config().render(vlan_num=vlan['vlan'],
                                                                                               vlan_des=vlan['desc'],arp_detection='arp detection enable')
                        else:
                            vlan_config = config_template.h3c_port_config_template.vlan_config().render(
                                vlan_num=vlan['vlan'],
                                vlan_des=vlan['desc'])
                        layer2_vlan_list.append(vlan_config)
                    return ''.join(layer2_vlan_list).lstrip()

                def uplink_device():
                    uplink_device = []
                    for uplink in a['uplink']:
                        uplink_device.append(uplink['A_device'])
                    return uplink_device

                def uplink_port():
                    uplink_port = []
                    for uplink in a['uplink']:
                        uplink_port.append(convert_interface_name(uplink['A_port']))
                    return uplink_port





                if 'XOA' in a['device_name']:
                    config.write(h3c_5130_xoa.h3c_5130_xoa().render(sysname=a['device_name'],layer2_vlan=layer2_vlan(),mgt_ip=a['mgtip'],
                                                                    mgt_netmask=a['mgtmask'],vlan=a['access_vlan'],uplink_device1=uplink_device()[0],uplink_device2=uplink_device()[1],uplink_port1=uplink_port()[0],uplink_port2=uplink_port()[1],console_password='123456',default_gateway=a['gateway'],snmp_password='123456',local_manage_network=login_acl(project),tacacs_password='123456',radius_password='123456',local_password='123456'))
                elif 'EVP' in a['device_name']:
                    config.write(h3c_5130_evp.h3c_5130_evp().render(sysname=a['device_name'],layer2_vlan=layer2_vlan(),mgt_ip=a['mgtip'],
                                                                    mgt_netmask=a['mgtmask'],vlan=a['access_vlan'],uplink_device1=uplink_device()[0],uplink_device2=uplink_device()[1],uplink_port1=uplink_port()[0],uplink_port2=uplink_port()[1],console_password='123456',default_gateway=a['gateway'],snmp_password='123456',local_manage_network=login_acl(project),tacacs_password='123456',radius_password='123456',local_password='123456'))
                elif 'EWL' in a['device_name']:
                    config.write(h3c_5560_ewl.h3c_5560_ewl().render(sysname=a['device_name'], layer2_vlan=layer2_vlan(),mgt_ip=a['mgtip'],
                                                                    mgt_netmask=a['mgtmask'],uplink_device1=uplink_device()[0],uplink_device2=uplink_device()[1],uplink_port1=uplink_port()[0],uplink_port2=uplink_port()[1],console_password='123456',default_gateway=a['gateway'],snmp_password='123456',local_manage_network=login_acl(project),tacacs_password='123456',local_password='123456'))

#
generation_doa_config(project)
generation_access_config_file(project)