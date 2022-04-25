import mysql_table_query
import config_template
import ipaddress
project = input('项目名称: ')

def basic_device_info_dict(func):
    doa_config_info = []
    manage_ip_list = func
    network = mysql_table_query.ip_planning(project)
    connect = mysql_table_query.connection(project)

    for ip in manage_ip_list:
        networklist = []
        mcon = []
        scon = []
        for n in network:
            interface_vlan = {'vlan': None, 'network': None,'desc':None,'acl':None}
            if str(n['floor'])+str(n['bdr']) == str(ip['floor'])+str(ip['bdr']):
                interface_vlan['vlan'] = n['vlan']
                interface_vlan['network'] = n['network']
                interface_vlan['desc'] = n['description']
                interface_vlan['acl'] = n['acl']
                # if :
                # print(ip['floor'],ip['bdr'],interface_vlan)
                networklist.append(interface_vlan)
        if '-DOA-' not in ip['device_name']:
            pass
        else:
            ip.update({'network':networklist})
            doa_config_info.append(ip)

        for c in connect:
            connection = {'local_interface':None,'Z_device':None,'Z_interface':None}
            if str(c['A_floor']) + str(c['A_bdr']) == str(ip['floor']) + str(ip['bdr']):
                if '-D-' in ip['device_name'] and '-DOA-' in ip['device_name'] and '-D-' in c['A_device']:
                    connection['local_interface'] = c['A_port']
                    connection['Z_device'] = c['Z_device']
                    connection['Z_interface'] = c['Z_port']
                    mcon.append(connection)
                    ip.update({'mconnect':mcon})
                if '-E-' in ip['device_name'] and '-DOA-' in ip['device_name'] and '-E-' in c['A_device']:
                    connection['local_interface'] = c['A_port']
                    connection['Z_device'] = c['Z_device']
                    connection['Z_interface'] = c['Z_port']
                    scon.append(connection)
                    ip.update({'sconnect': scon})
    return doa_config_info


        # print(vlan_config)
        # for con in mysql_table_query.connection(project):
        #     print(con)


doa = basic_device_info_dict(mysql_table_query.deivce_ip(project))
for d in doa:
    if '-D-' in d['device_name']:
        with open('/Users/wanghaoyu/Desktop/config/'+d['device_name']+'.cfg','a+') as config:
            for n in d['network']:
                config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))

            for n in d['network']:
                config.write(config_template.h3c_port_config_template.mater_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
                                                                                                           vlan_ipaddress=ipaddress.ip_network(n['network'])[2],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                                                                                           vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1],acl_name=n['acl']))
            for c in d['mconnect']:
                config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['local_interface'],description=(c['Z_device']+'-'+c['Z_interface'])))
        config.close()

    if '-E-' in d['device_name']:
        with open('/Users/wanghaoyu/Desktop/config/'+d['device_name']+'.cfg','a+') as config:
            for n in d['network']:
                config.write(config_template.h3c_port_config_template.vlan_config().render(vlan_num=n['vlan'],vlan_des=n['desc']))

            for n in d['network']:
                config.write(config_template.h3c_port_config_template.slaver_interface_vlan_config().render(interface_vlan=n['vlan'],vlan_des=n['desc'],
                                                                                                           vlan_ipaddress=ipaddress.ip_network(n['network'])[3],vlan_netmask=ipaddress.ip_network(n['network']).netmask,
                                                                                                           vlan_num=n['vlan'],vrrp_ip=ipaddress.ip_network(n['network'])[1],acl_name=n['acl']))
            for c in d['sconnect']:
                config.write(config_template.h3c_port_config_template.lay2_phy_interface_config().render(phy_interface=c['local_interface'],description=(c['Z_device']+'-'+c['Z_interface'])))
        config.close()
# def generation_lay3_vlan(project):
#     network_info = mysql_table_query.ip_planning(project)
#     device_info = mysql_table_query.deivce_ip(project)
#     for dev in device_info:
#         print(dev)
#         dev_bdr = str(dev['floor'])+str(dev['bdr'])
#         for net in network_info:
#             print(net)
#             net_bdr = str(net['floor'])+str(net['bdr'])
#             if dev_bdr == net_bdr:
#                 print(dev['network'])

