import mysql_table_query
import config_template
import ipaddress
project = input('项目名称: ')

def basic_device_info_dict(func):
    doa_config_info = []
    manage_ip_list = func
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
            if '-DOA-' in ip['device_name'] and  '-E-' in ip['device_name'] and '-E-' in m['A_device'] and ip['floor'] == m['floor'] :
                e_downlinkconnect['downlinkconnect'].append(m)
                ip.update(e_downlinkconnect)

        for u in uplinkconnection_list:
            if ip['device_name'] == u['layer3connection']['Z_device']:
                ip.update(u)


        networklist = []

        for n in network:
            interface_vlan = {'vlan': None, 'network': None,'desc':None,'acl':None}
            if str(n['floor'])+str(n['bdr']) == str(ip['floor'])+str(ip['bdr']):
                interface_vlan['vlan'] = n['vlan']
                interface_vlan['network'] = n['network']
                interface_vlan['desc'] = n['description']
                interface_vlan['acl'] = n['acl']


                networklist.append(interface_vlan)
        if '-DOA-' not in ip['device_name']:
            pass
        else:
            ip.update({'network':networklist})
            doa_config_info.append(ip)

    return doa_config_info
#
#
#
doa = basic_device_info_dict(mysql_table_query.deivce_ip(project))
core_network = mysql_table_query.core_ip()
ospf_area = ipaddress.IPv4Network(core_network[0]['network']).network_address
for d in doa:
    if '-D-' in d['device_name']:
        def geneneration_ospf():
            for n in d['network']:
                if n['desc'] == 'MGT':
                    unslicent= config_template.route_config.undo_silcent().render(
                        interconnect_interface=d['layer3connection']['Z_port'], mgt_vlan_num='vlan' + str(n['vlan']))

            # area = config_template.route_config.network_area().render(core_network=str(ospf_area))
            #     network = config_template.route_config.network().render(ipaddress=ipaddress.ip_network(n['network'])[1])


                # print(area)
                # print(network)

        geneneration_ospf()
    #     with open('/Users/alawn/Desktop/config/'+d['device_name']+'.cfg','a+') as config:
    #
    #         for n in d['network']:
    #             print(n)
    #             config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))
    #             if n['desc'] == 'MGT':
    #                 config.write(config_template.h3c_port_config_template.vlan10_mater_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
    #                                                                                                        vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
    #                                                                                                        vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1]))
    #             elif 'VOIP' in n['desc']:
    #                 config.write(config_template.h3c_port_config_template.voip_mater_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
    #                                                                                                        vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
    #                                                                                                        vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1],acl_name=n['acl']))
    #             else:
    #                 config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
    #                                                                                                        vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
    #                                                                                                        vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1],acl_name=n['acl']))
    #
    #
    #         for i in d['interconnect']:
    #             config.write(config_template.h3c_port_config_template.interconnect_phy_interface_config().render(phy_interface=i['A_port'],description=(i['Z_device']+'-'+i['Z_port'])))
    #         for c in d['downlinkconnect']:
    #             config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['A_port'],description=(c['Z_device']+'-'+c['Z_port'])))
    #         config.write(config_template.h3c_port_config_template.lay3_phy_interface_config().render(
    #             phy_interface=d['layer3connection']['Z_port'],
    #             description=d['layer3connection']['A_device'] + '-' + d['layer3connection']['A_port'],
    #             ipaddress=d['layer3connection']['Z_ipaddress'], netmask=' 255.255.255.252'))
    #     config.close()
    #
    # if '-E-' in d['device_name']:
    #     with open('/Users/alawn/Desktop/config/'+d['device_name']+'.cfg','a+') as config:
    #         for n in d['network']:
    #             print(n)
    #             config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))
    #
    #             if n['desc'] == 'MGT':
    #                 config.write(config_template.h3c_port_config_template.vlan10_slaver_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
    #                                                                                                        vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
    #                                                                                                        vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1]))
    #             elif 'VOIP' in n['desc']:
    #                 config.write(config_template.h3c_port_config_template.voip_slaver_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
    #                                                                                                        vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
    #                                                                                                        vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1],acl_name=n['acl']))
    #             else:
    #                 config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
    #                                                                                                        vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
    #                                                                                                        vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1],acl_name=n['acl']))
    #             config.write(config_template.route_config.ospf_config())
    #             if n['desc'] == 'MGT':
    #                 config.write(config_template.route_config.undo_silcent().render(interconnect_interface = d['layer3connection']['Z_port'],mgt_vlan_num= 'vlan'+n['vlan']))
    #             config.write(config_template.route_config.network_area().render(core_network=str(ospf_area)))
    #             config.write(config_template.route_config.network().render(ipaddress=n['network'])[1])
    #             config.write(' stub')
    #         for i in d['interconnect']:
    #             config.write(config_template.h3c_port_config_template.interconnect_phy_interface_config().render(phy_interface=i['Z_port'],description=(i['A_device']+'-'+i['A_port'])))
    #         for c in d['downlinkconnect']:
    #             config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['A_port'],description=(c['Z_device']+'-'+c['Z_port'])))
    #         config.write(config_template.h3c_port_config_template.lay3_phy_interface_config().render(phy_interface=d['layer3connection']['Z_port'],description=d['layer3connection']['A_device']+'-'+d['layer3connection']['A_port'],ipaddress=d['layer3connection']['Z_ipaddress'],netmask=' 255.255.255.252'))
    #     config.close()
    #
    #
