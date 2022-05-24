import mysql_table_query
import config_template
import ipaddress

project = input('项目名称: ')

manage_ip_list = mysql_table_query.deivce_ip(project)
network = mysql_table_query.ip_planning(project)
connect = mysql_table_query.connection(project)
endpoint = mysql_table_query.endpoint(project)


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




doa = basic_device_info_dict(project)
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
#

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
        if '-D-' in d['device_name']:
            with open('/Users/alawn/Desktop/config/'+str(d['mgtip']+'_'+d['device_name'])+'.cfg','a+') as config:
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
                    if n['desc'] == 'interconnect':
                        pass
                    else:
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
                        if int(n['vlan']) > 254:
                            vrrp_num = n['vlan'][0:2]
                        else:
                            vrrp_num = n['vlan']
                        config.write(config_template.h3c_port_config_template.normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_num=vrrp_num,vrrp_ip=ipaddress.ip_network(n['network'])[1], acl_name=n['acl']))
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
                    else:
                        pass

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
            with open('/Users/alawn/Desktop/config/'+str(d['mgtip']+'_'+d['device_name'])+'.cfg','a+') as config:
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

def global_generation_doa_config_file():
    for d in doa:
        if '-D-' in d['device_name']:
            with open('C:/Users/Alawn/Desktop/config/'+str(d['mgtip']+'_'+d['device_name'])+'.cfg','a+') as config:
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
                config.write(config_template.h3c_port_config_template.master_stp())
                def geneneration_ospf():
                    unslicent = None
                    for n in d['network']:
                        if n['desc'] == 'MGT':
                            unslicent = config_template.route_config.undo_silcent().render(
                                interconnect_interface=d['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan']))
                    return unslicent

                def vrrp(vlan):
                    if int(vlan) > 254:
                        vrrp = vlan[0:2]
                    else:
                        vrrp = vlan
                    return vrrp

                for n in d['network']:
                    # if n['desc'] == 'interconnection':
                    #     pass
                    # else:
                    config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))
                for n in d['network']:
                    if n['desc'] == 'MGT':
                        config.write(config_template.h3c_port_config_template.vlan10_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'],vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                    elif 'AP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in ap_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'Video' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in video_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'OA_Device' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']),  vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in oadevice_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'GELI' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']),  vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in geli_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'OA' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']),  vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in oa_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'TY' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']),  vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in ty_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    elif 'VOIP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_voip_mater_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[2],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']),  vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in voip_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n'+'#')
                    else:pass

                for n in d['network']:
                    if n['vlan'] == '10' or n['acl'] == '' or n['acl'] == 'None':
                        pass
                    else:
                        config.write(config_template.h3c_port_config_template.gloabl_acl().render(acl_name=n['acl'],vlan_num=n['vlan']))
                config.write('\n'+'#')
                for i in d['interconnect']:
                    config.write(config_template.h3c_port_config_template.interconnect_phy_interface_config().render(phy_interface=i['A_port'],description=(i['Z_device']+'-'+convert_interface_name(i['Z_port']))))
                config.write('\n'+'#')

                config.write(config_template.h3c_port_config_template.port_channel_interface_config().render(description=d['interconnect'][0]['Z_device']))
                config.write('\n' + '#')

                for c in d['downlinkconnect']:
                    config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['A_port'],description=(c['Z_device']+'-'+convert_interface_name(c['Z_port']))))
                config.write(config_template.h3c_port_config_template.lay3_phy_interface_config().render(
                    phy_interface=d['layer3connection']['Z_port'],
                    description=d['layer3connection']['A_device'] + '-' + convert_interface_name(d['layer3connection']['A_port']),
                    ipaddress=(d['layer3connection']['Z_ipaddress']).split('/')[0], netmask=' 255.255.255.252'))

                config.write(config_template.route_config.ospf_config().render(mgt_ip=d['mgtip']))
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
            with open('C:/Users/Alawn/Desktop/config/'+str(d['mgtip']+'_'+d['device_name'])+'.cfg','a+') as config:
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
                config.write(config_template.h3c_port_config_template.slaver_stp())
                def geneneration_ospf():
                    unslicent = None
                    for n in d['network']:
                        if n['desc'] == 'MGT':
                            unslicent = config_template.route_config.undo_silcent().render(
                                interconnect_interface=d['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan']))
                    return unslicent


                for n in d['network']:
                    if n['desc'] == 'interconnection':
                        pass
                    else:
                        config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))

                for n in d['network']:
                    if n['desc'] == 'MGT':
                        config.write(config_template.h3c_port_config_template.vlan10_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vlan_num=n['vlan'], vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                    elif 'AP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in ap_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'Video' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in video_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'OA_Device' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in oadevice_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'GELI' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in geli_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'OA' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in oa_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'TY' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_normal_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in ty_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    elif 'VOIP' in n['desc']:
                        config.write(config_template.h3c_port_config_template.global_voip_slaver_interface_vlan_config().render(
                            interface_vlan=n['vlan'], vlan_des=n['desc'],
                            vlan_ipaddress=ipaddress.ip_network(n['network'])[3],
                            vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                            vrrp_num=vrrp(n['vlan']), vrrp_ip=ipaddress.ip_network(n['network'])[1]))
                        for dhcp in voip_dhcp:
                            config.write(config_template.h3c_port_config_template.dhcp_relay().render(dhcp_relay=dhcp))
                        config.write('\n' + '#')
                    else:pass

                for n in d['network']:
                    if n['vlan'] == '10' or n['acl'] == '' or n['acl'] == 'None':
                        pass
                    else:
                        config.write(config_template.h3c_port_config_template.gloabl_acl().render(acl_name=n['acl'],vlan_num=n['vlan']))
                config.write('\n'+'#')

                for i in d['interconnect']:
                    config.write(config_template.h3c_port_config_template.interconnect_phy_interface_config().render(phy_interface=i['Z_port'],description=(i['A_device']+'-'+convert_interface_name(i['A_port']))))
                config.write('\n'+'#')
                config.write(config_template.h3c_port_config_template.port_channel_interface_config().render(
                    description=d['interconnect'][0]['A_device']))
                config.write('\n' + '#')

                for c in d['downlinkconnect']:
                    config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['A_port'],description=(c['Z_device']+'-'+convert_interface_name(c['Z_port']))))
                config.write(config_template.h3c_port_config_template.lay3_phy_interface_config().render(phy_interface=d['layer3connection']['Z_port'],description=d['layer3connection']['A_device']+'-'+convert_interface_name(d['layer3connection']['A_port']),ipaddress=(d['layer3connection']['Z_ipaddress']).split('/')[0],netmask=' 255.255.255.252'))
                config.write(config_template.route_config.ospf_config().render(mgt_ip=d['mgtip']))
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

#
def access_device_config_info():

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




def generation_access_config_file():
    for a in access_device_config_info():
        with open('C:/Users/Alawn/Desktop/config/'+str(a['mgtip']+'_'+a['device_name'])+'.cfg','a+') as config:
            config.write(config_template.config_template.sysname().render(sysname=a['device_name']))
            config.write('\n' + '#')
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
            config.write('#')
            config.write(config_template.config_template.stp_config())
            for vlan in a['vlan']:
                config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=vlan['vlan'],
                                                                                           vlan_des=vlan['desc']))
            config.write('#')

            for vlan in a['vlan']:
                if vlan['desc'] == 'MGT':
                    config.write(config_template.h3c_port_config_template.access_mgt_interface_vlan_config().render(interface_vlan = vlan['vlan'],vlan_des=vlan['desc'],vlan_ipaddress=a['mgtip'],vlan_netmask=a['mgtmask']))
            config.write('\n' + '#')
            config.write(config_template.h3c_port_config_template.access_default_gateway().render(gateway=a['gateway']))
            config.write('\n'+'#')
            if 'XOA' in a['device_name']:
                config.write(config_template.h3c_port_config_template.oa_access_interface().render(vlan_num=a['access_vlan']))
                config.write('\n' + '#')
                config.write(config_template.h3c_port_config_template.xoa_radius())
            if 'EVP' in a['device_name']:
                config.write(config_template.h3c_port_config_template.evp_access_interface().render(vlan_num=a['access_vlan']))
                config.write('\n' + '#')
                config.write(config_template.h3c_port_config_template.evp_radius())
            if 'EWL' in a['device_name']:
                config.write(
                    config_template.h3c_port_config_template.ewl_access_interface())
                config.write('\n' + '#')

            for ul in a['uplink']:
                config.write(config_template.h3c_port_config_template.access_uplink().render(port_num=ul['Z_port'],A_devicename=ul['A_device'],A_port=convert_interface_name(ul['A_port'])))
            config.write(
                config_template.config_template.aaa_tacacs().render(nas_ip=str(a['mgtip'])))
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

global_generation_doa_config_file()
generation_access_config_file()