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
core_network = mysql_table_query.core_ip(project)
ospf_area = ipaddress.IPv4Network(core_network[0]['network']).network_address
def login_acl():
    login_acl = []
    rule_num = 65

    for acl in core_network:
        rule_num = rule_num+5
        logacl = ' rule '+str(rule_num)+' permit soure '+str(ipaddress.IPv4Network(acl['network']).network_address)+' '+str(ipaddress.IPv4Network(acl['network']).hostmask)
        login_acl.append(logacl)
    return login_acl


ap_dhcp = str(mysql_table_query.dhcp(project)[0]['AP_dhcp']).split(';')
video_dhcp = str(mysql_table_query.dhcp(project)[0]['Video_dhcp']).split(';')
oadevice_dhcp = str(mysql_table_query.dhcp(project)[0]['OA-Device_dhcp']).split(';')
geli_dhcp =str(mysql_table_query.dhcp(project)[0]['GELI_dhcp']).split(';')
oa_dhcp = str(mysql_table_query.dhcp(project)[0]['OA_dhcp']).split(';')
ty_dhcp = str(mysql_table_query.dhcp(project)[0]['TY_dhcp']).split(';')
voip_dhcp = str(mysql_table_query.dhcp(project)[0]['VOIP_dhcp']).split(';')

def convert_interface_name(portname):
    interface_name = None
    if 'Ten-GigabitEthernet' in portname:
        interface_name = portname.replace('Ten-GigabitEthernet','Te')
    elif 'GigabitEthernet1' in portname:
        interface_name = portname.replace('GigabitEthernet','Gi')
    elif 'Smartrate-Ethernet' in portname:
        interface_name = portname.replace('Smartrate-Ethernet','SGE')
    return interface_name

def generation_doa_config_file():
    for d in doa:
        print(d)
        if '-D-' in d['device_name']:
            with open('/Users/alawn/Desktop/config/'+d['device_name']+'.cfg','a+') as config:
                config.write(config_template.config_template.sysname().render(sysname=d['device_name']))
                config.write('\n'+'#')
                config.write(config_template.config_template.time_zone())
                config.write('#')
                config.write(config_template.config_template.login_acl_use())
                config.write('#')
                config.write(config_template.config_template.dldp_lldp())
                config.write('#')
                config.write(config_template.config_template.line_aux())
                config.write('#')
                config.write(config_template.config_template.vty())
                config.write('#')
                config.write(config_template.config_template.logging())
                config.write('#')
                config.write(config_template.config_template.ntp())
                def geneneration_ospf():
                    unslicent = None
                    for n in d['network']:
                        if n['desc'] == 'MGT':
                            unslicent = config_template.route_config.undo_silcent().render(
                                interconnect_interface=d['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan']))
                    return unslicent
                for n in d['network']:
                    config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))

                for n in d['network']:
                    if n['desc'] == 'MGT':
                        config.write(config_template.h3c_port_config_template.vlan10_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'],vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                    elif 'AP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in ap_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'Video' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in video_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'OA_Device' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in oadevice_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'GELI' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in geli_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'OA' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in oa_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'TY' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in ty_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'VOIP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.voip_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in voip_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')


                for i in d['interconnect']:
                    config.write(config_template.h3c_port_config_template.interconnect_phy_interface_config().render(phy_interface=i['A_port'],description=(i['Z_device']+'-'+convert_interface_name(i['Z_port']))))
                    config.write('\n'+'#')
                    config.write(config_template.h3c_port_config_template.port_channel_interface_config().render(description=i['Z_device']))
                for c in d['downlinkconnect']:
                    config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['A_port'],description=(c['Z_device']+'-'+convert_interface_name(c['Z_port']))))
                config.write(config_template.h3c_port_config_template.lay3_phy_interface_config().render(
                    phy_interface=d['layer3connection']['Z_port'],
                    description=d['layer3connection']['A_device'] + '-' + convert_interface_name(d['layer3connection']['A_port']),
                    ipaddress=d['layer3connection']['Z_ipaddress'], netmask=' 255.255.255.252'))

                config.write(config_template.route_config.ospf_config())
                config.write(geneneration_ospf())
                config.write(config_template.route_config.network_area().render(core_network=str(ospf_area)))
                for n in d['network']:
                    network = config_template.route_config.network().render(ipaddress=str(ipaddress.ip_network(n['network'])[2]))
                    config.write(network)
                config.write('\n'+'  stub')
                config.write('\n'+'#')
                config.write(config_template.config_template.advance_acl())
                config.write(config_template.config_template.aaa_tacacs().render(nas_ip=str(ipaddress.ip_network(n['network'])[2])))
                config.write('\n'+'#')
                config.write(config_template.config_template.snmp_acl())
                config.write('#')
                config.write(config_template.config_template.snmp_config())
                config.write('#')
                config.write(config_template.config_template.stand_login_acl())
                for acl_cotent in login_acl():
                    config.write(config_template.config_template.floor_login_acl().render(login_acl=acl_cotent))
                config.write(config_template.config_template.domain_lookup())
            config.close()
    #     #
        if '-E-' in d['device_name']:
            with open('/Users/alawn/Desktop/config/'+d['device_name']+'.cfg','a+') as config:
                config.write(config_template.config_template.sysname().render(sysname=d['device_name']))
                config.write('\n'+'#')
                config.write(config_template.config_template.time_zone())
                config.write('#')
                config.write(config_template.config_template.login_acl_use())
                config.write('#')
                config.write(config_template.config_template.dldp_lldp())
                config.write('#')
                config.write(config_template.config_template.line_aux())
                config.write('#')
                config.write(config_template.config_template.vty())
                config.write('#')
                config.write(config_template.config_template.logging())
                config.write('#')
                config.write(config_template.config_template.ntp())
                def geneneration_ospf():
                    unslicent = None
                    for n in d['network']:
                        if n['desc'] == 'MGT':
                            unslicent = config_template.route_config.undo_silcent().render(
                                interconnect_interface=d['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan']))
                    return unslicent
                for n in d['network']:
                    config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))

                for n in d['network']:
                    if n['desc'] == 'MGT':
                        config.write(config_template.h3c_port_config_template.vlan10_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                    elif 'AP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in ap_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'Video' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in video_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'OA_Device' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in oadevice_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'GELI' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in geli_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'OA' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in oa_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'TY' in n['desc']:
                        config.write(config_template.h3c_port_config_template.normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in ty_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'VOIP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.voip_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
                        for dhcp in voip_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                for i in d['interconnect']:
                    config.write(config_template.h3c_port_config_template.interconnect_phy_interface_config().render(phy_interface=i['Z_port'],description=(i['A_device']+'-'+convert_interface_name(i['A_port']))))
                    config.write('\n'+'#')
                    config.write(config_template.h3c_port_config_template.port_channel_interface_config().render(description=i['A_device']))
                for c in d['downlinkconnect']:
                    config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['A_port'],description=(c['Z_device']+'-'+convert_interface_name(c['Z_port']))))
                config.write(config_template.h3c_port_config_template.lay3_phy_interface_config().render(phy_interface=d['layer3connection']['Z_port'],description=d['layer3connection']['A_device']+'-'+convert_interface_name(d['layer3connection']['A_port']),ipaddress=d['layer3connection']['Z_ipaddress'],netmask=' 255.255.255.252'))
                config.write(config_template.route_config.ospf_config())
                config.write(geneneration_ospf())
                config.write(config_template.route_config.network_area().render(core_network=str(ospf_area)))
                for n in d['network']:
                    network = config_template.route_config.network().render(ipaddress=str(ipaddress.ip_network(n['network'])[3]))
                    config.write(network)
                config.write('\n'+'  stub')
                config.write('\n' + '#')
                config.write(config_template.config_template.advance_acl())
                config.write(
                    config_template.config_template.aaa_tacacs().render(nas_ip=str(ipaddress.ip_network(n['network'])[3])))
                config.write('\n' + '#')
                config.write(config_template.config_template.snmp_acl())
                config.write('#')
                config.write(config_template.config_template.snmp_config())
                config.write('#')
                config.write(config_template.config_template.stand_login_acl())
                for acl_cotent in login_acl():
                    config.write(config_template.config_template.floor_login_acl().render(login_acl=acl_cotent))
                config.write(config_template.config_template.domain_lookup())
            config.close()

generation_doa_config_file()
