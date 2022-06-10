import mysql_table_query
import ipaddress
import h3c_6520x_master_doa
import config_template

project = '深圳光启未来'
#
# network = input('IP地址：')


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



def ip_planning(project):
    return mysql_table_query.ip_planning(project)

def connect(project):
    return mysql_table_query.connection(project)

def mgtip(project):
    return mysql_table_query.mgtip(project)


def generation_doa_config(project):
    core_network = mysql_table_query.core_ip(project)
    ospf_area = ipaddress.IPv4Network(core_network[0]['network']).network_address
    for entry in basic_device_info_dict(project):
        if '-D-' in entry['device_name']:
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
                    return ''.join(packet_filter).lstrip()
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
                        network = config_template.route_config.network().render(
                            ipaddress=str(ipaddress.ip_network(n['network'])[2]))
                        ospf_netowrk.append(network)
                    return ''.join(ospf_netowrk).lstrip()

                def layer2_vlan():
                    layer2vlan=[]
                    for n in entry['network']:
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
                            mgt_vlan = config_template.h3c_port_config_template.vlan10_mater_interface_vlan_config().render(interface_vlan=n['vlan'], vlan_des=n['desc'],vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1])
                            layer3_vlan.append(mgt_vlan)
                        elif n['func'] == 'AP网':
                            ap_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                                    interface_vlan=n['vlan'], vlan_des=n['desc'],
                                    vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                                    vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                    vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1],
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
                            oa_device_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
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
                            geli_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
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
                            oa_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
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
                            ty_vlan = config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
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
                            voip_vlan = config_template.h3c_port_config_template.global_voip_mater_interface_vlan_config().render(
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
                # def downlink_d_port(entry):
                #     h6520x_d_down_link_port_list = ['Ten-GigabitEthernet1/0/1', 'Ten-GigabitEthernet1/0/2',
                #                                     'Ten-GigabitEthernet1/0/3', 'Ten-GigabitEthernet1/0/4',
                #                                     'Ten-GigabitEthernet1/0/5', 'Ten-GigabitEthernet1/0/6',
                #                                     'Ten-GigabitEthernet1/0/7', 'Ten-GigabitEthernet1/0/8',
                #                                     'Ten-GigabitEthernet1/0/9', 'Ten-GigabitEthernet1/0/10',
                #                                     'Ten-GigabitEthernet1/0/11', 'Ten-GigabitEthernet1/0/12',
                #                                     'Ten-GigabitEthernet1/0/13', 'Ten-GigabitEthernet1/0/14']
                #     d_layer2_interface = []
                #     print(entry['device_name'])
                #     for adp in entry['downlinkconnect']:
                #         print(adp)
                #         for dp in h6520x_d_down_link_port_list:
                #             if adp['A_port'] == dp and '-XOA-' in adp['Z_device']:
                #                 pass
                                # interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(phy_interface=adp['A_port'],description= adp['Z_device']+'-'+convert_interface_name(adp['Z_port']))
                                # d_layer2_interface.append(interface)

                            # else:
                            #     print(dp)
                                # interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(phy_interface=dp)
                                # d_layer2_interface.append(interface)


                #     return ''.join(d_layer2_interface).lstrip()
                # downlink_d_port(entry)
                # def downlink_e_port(entry):
                #     h6520x_e_down_link_port_list = ['Ten-GigabitEthernet1/0/15', 'Ten-GigabitEthernet1/0/16',
                #                                     'Ten-GigabitEthernet1/0/17', 'Ten-GigabitEthernet1/0/18',
                #                                     'Ten-GigabitEthernet1/0/19', 'Ten-GigabitEthernet1/0/20',
                #                                     'Ten-GigabitEthernet1/0/21', 'Ten-GigabitEthernet1/0/22',
                #                                     'Ten-GigabitEthernet1/0/23', 'Ten-GigabitEthernet1/0/24',
                #                                     'Ten-GigabitEthernet1/0/25', 'Ten-GigabitEthernet1/0/26',
                #                                     'Ten-GigabitEthernet1/0/27', 'Ten-GigabitEthernet1/0/28']
                #     e_layer2_interface = []
                #     for adp in entry['downlinkconnect']:
                #         for dp in h6520x_e_down_link_port_list:
                #             if adp['A_port'] == dp and '-XOA-' in adp['Z_device']:
                #                 interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(
                #                     phy_interface=adp['A_port'],
                #                     description=adp['Z_device'] + '-' + convert_interface_name(adp['Z_port']))
                #                 e_layer2_interface.append(interface)
                #             else:
                #                 interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                #                     phy_interface=dp)
                #                 e_layer2_interface.append(interface)
                #
                #     return ''.join(e_layer2_interface).lstrip()
                #
                # def downlink_v_port(entry):
                #     h6520x_v_down_link_port_list = ['Ten-GigabitEthernet1/0/29', 'Ten-GigabitEthernet1/0/30',
                #                                     'Ten-GigabitEthernet1/0/31', 'Ten-GigabitEthernet1/0/32',
                #                                     'Ten-GigabitEthernet1/0/33', 'Ten-GigabitEthernet1/0/34',
                #                                     'Ten-GigabitEthernet1/0/35', 'Ten-GigabitEthernet1/0/36',
                #                                     'Ten-GigabitEthernet1/0/37', 'Ten-GigabitEthernet1/0/38',
                #                                     'Ten-GigabitEthernet1/0/39', 'Ten-GigabitEthernet1/0/40',
                #                                     'Ten-GigabitEthernet1/0/41', 'Ten-GigabitEthernet1/0/42']
                #     v_layer2_interface = []
                #     for adp in entry['downlinkconnect']:
                #         for dp in h6520x_v_down_link_port_list:
                #             if adp['A_port'] == dp and '-XOA-' in adp['Z_device']:
                #                 interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(
                #                     phy_interface=adp['A_port'],
                #                     description=adp['Z_device'] + '-' + convert_interface_name(adp['Z_port']))
                #                 v_layer2_interface.append(interface)
                #             else:
                #                 interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                #                     phy_interface=dp)
                #                 v_layer2_interface.append(interface)
                #
                #     return ''.join(v_layer2_interface).lstrip()
                #
                # def downlink_w_port(entry):
                #     h6520x_w_down_link_port_list = ['Ten-GigabitEthernet1/0/49:2', 'Ten-GigabitEthernet1/0/49:3',
                #                                     'Ten-GigabitEthernet1/0/49:4', 'Ten-GigabitEthernet1/0/50:1',
                #                                     'Ten-GigabitEthernet1/0/50:2', 'Ten-GigabitEthernet1/0/50:3',
                #                                     'Ten-GigabitEthernet1/0/50:4', 'Ten-GigabitEthernet1/0/51:1',
                #                                     'Ten-GigabitEthernet1/0/51:2', 'Ten-GigabitEthernet1/0/51:3',
                #                                     'Ten-GigabitEthernet1/0/51:4', 'Ten-GigabitEthernet1/0/52:1',
                #                                     'Ten-GigabitEthernet1/0/52:2', 'Ten-GigabitEthernet1/0/52:3',
                #                                     'Ten-GigabitEthernet1/0/52:4']
                #     w_layer2_interface = []
                #     for adp in entry['downlinkconnect']:
                #         for dp in h6520x_w_down_link_port_list:
                #             if adp['A_port'] == dp and '-XOA-' in adp['Z_device']:
                #                 interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(
                #                     phy_interface=adp['A_port'],
                #                     description=adp['Z_device'] + '-' + convert_interface_name(adp['Z_port']))
                #                 w_layer2_interface.append(interface)
                #
                #             else:
                #                 interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(
                #                     phy_interface=dp)
                #                 w_layer2_interface.append(interface)
                #
                #     return ''.join(w_layer2_interface).lstrip()
                # print(entry['layer3connection']['A_ipaddress'],convert_interface_name(entry['layer3connection']['A_port']))
                # config.write(h3c_6520x_master_doa.h3c_6520x_master_doa().render(sysname=entry['device_name'],packet_filter=packet_filter(),router_id=entry['mgtip'],undo_silent_interface=undo_slicent_interface(),area_id=ospf_area,
                #                                                                 ospf_network=ospf_network(),layer2_vlan=layer2_vlan(),interconnect_device=entry['interconnect'][0]['Z_device'],interconnect_bagg_port=convert_interface_name(interconnect_port()[0]),layer3_interface_vlan=layer3_interface_vlan(),
                #                                                                 uplink_device_name=entry['layer3connection']['A_device'],uplink_port_num=convert_interface_name(entry['layer3connection']['A_port']),uplink_address=ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).ip,uplink_netmask=ipaddress.IPv4Interface(entry['layer3connection']['Z_ipaddress']).netmask))
                def layer2_interface():
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
                        downlink_list.append(n['A_port'])
                        Z_device.append(n['Z_device'])
                        Z_port.append(n['Z_port'])
                    for i in h6520x_d_down_link_port_list:
                        if i in downlink_list:
                            # try:
                            interface = config_template.h3c_port_config_template.oa_lay2_phy_interface_config().render(phy_interface=i,description=str(Z_device_gener.__next__())+'-'+convert_interface_name(str(Z_port_gener.__next__())))
                            d_down_link_config.append(interface)
                            # except InterruptedError:
                            #     interface = config_template.h3c_port_config_template.normal_lay2_phy_interface_config().render(phy_interface=i)
                            #     d_down_link_config.append(interface)
                    return ''.join(d_down_link_config).lstrip()
                layer2_interface()
                print(entry['device_name'])1
                print(layer2_interface())
generation_doa_config(project)