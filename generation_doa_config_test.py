import mysql_table_query
import ipaddress
import h3c_6520x_master_doa
import config_template

project = '深圳光启未来'
#
# network = input('IP地址：')

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



def ip_planning(project):
    return mysql_table_query.ip_planning(project)

def connect(project):
    return mysql_table_query.connection(project)

def mgtip(project):
    return mysql_table_query.mgtip(project)

def convert_interface_name(portname):
    interface_name = None
    if 'Ten-GigabitEthernet' in portname:
        interface_name = portname.replace('Ten-GigabitEthernet','Te')
    elif 'GigabitEthernet1' in portname:
        interface_name = portname.replace('GigabitEthernet','Gi')
    elif 'Smartrate-Ethernet' in portname:
        interface_name = portname.replace('Smartrate-Ethernet','SGE')
    elif 'Smartrate-Ethernet' in portname:
        interface_name = portname.replace('Smartrate-Ethernet','SGE')
    return interface_name



def generation_doa_config(project):
    core_network = mysql_table_query.core_ip(project)
    ospf_area = ipaddress.IPv4Network(core_network[0]['network']).network_address
    for entry in basic_device_info_dict(project):
        print(entry)
        if '-D-' in entry['device_name']:
            with open('/Users/wanghaoyu/Desktop/config/' + str(entry['mgtip'] + '_' + entry['device_name']) + '.cfg',
                      'a+') as config:
                def packet_filter():
                    packet_filter=[]
                    for n in entry['network']:
                        if n['vlan'] == '10' or n['acl'] == '' or n['acl'] == 'None':
                            pass
                        else:
                            packet_filter.append(config_template.h3c_port_config_template.gloabl_acl().render(acl_name=n['acl'],
                                                                                                      vlan_num=n['vlan']))
                    return ''.join(packet_filter)

                def undo_slicent_interface():
                    undo_slicent_interface = []
                    for n in entry['network']:
                        if n['desc'] == 'MGT':
                            undo_slicent_interface.append(config_template.route_config.undo_silcent().render(
                                interconnect_interface=entry['layer3connection']['Z_port'],
                                mgt_vlan_num='vlan' + str(n['vlan'])))
                    return ''.join(undo_slicent_interface)

                def ospf_network():
                    ospf_netowrk = []
                    for n in entry['network']:
                        network = config_template.route_config.network().render(
                            ipaddress=str(ipaddress.ip_network(n['network'])[2]))
                        ospf_netowrk.append(network)
                    return ''.join(ospf_netowrk)
                config.write(h3c_6520x_master_doa.h3c_6520x_master_doa().render(sysname=entry['device_name'],packet_filter=packet_filter(),router_id=entry['mgtip'],undo_silent_interface=undo_slicent_interface(),area_id=ospf_area,
                                                                                ospf_network=ospf_network()))

generation_doa_config(project)