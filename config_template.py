from jinja2 import Template
class config_template:

    def doa_uplink(self):
        self.DOA_UP_LINK_PORT = Template('''
interface {{port_num}}
description {{uplink_descr}}
ip address {{ip_address}} {{netmask}}
no ip redric
no ip unreachable
        ''')
        return self.DOA_UP_LINK_PORT

    def doa_downlink():
        DOA_DOWN_LINK_PROT=Template('''
interface {{port_num}}
description {{downlink_descr}}
switchport mode trunk
        ''')
        return DOA_DOWN_LINK_PROT

    def time_zone():
        return 'clock timezone CST add 08:00:00'

    def dldp_lldp():
        return '''
lldp global enable
dldp global enable
        '''

    def ssh_acl():
        return '''
ssh server enable
ssh server acl acl_number
        '''

    def aaa_tacacs():
        return Template('''
hwtacacs scheme tencent_scheme
 primary authentication 10.42.3.75
 primary authorization 10.42.3.75
 primary accounting 10.42.3.75
 secondary authentication  10.14.160.75
 secondary authorization  10.14.160.75
 secondary accounting  10.14.160.75
 key authentication cipher {{tacacs_key}}
 key authorization cipher {{tacacs_key}}
 key accounting cipher {{tacacs_key}}
 user-name-format without-domain
 nas-ip {{nas_ip}}
    ''')

    def login_acl_use():
        return '''
telnet server enable
telnet server acl 2000

ssh server enable
ssh server acl 2000
'''

    def login_acl():
        return Template('''
acl number 2000
 rule 0 permit source 10.99.204.0 0.0.0.255
 rule 5 permit source 10.14.90.0 0.0.0.255
 rule 10 permit source 10.14.67.0 0.0.0.255
 rule 15 permit source 10.14.34.0 0.0.0.255
 rule 20 permit source 10.14.70.0 0.0.0.255
 rule 25 permit source 10.14.64.0 0.0.0.255
 rule 30 permit source 10.80.15.192 0.0.0.63
 rule 35 permit source 10.76.83.0 0.0.0.255
 rule 40 permit source 10.76.1.0 0.0.0.15
 rule 45 permit source 10.6.0.0 0.0.0.15
 rule 50 permit source 10.6.3.0 0.0.0.3
 rule 55 permit source 10.39.0.0 0.0.1.255
 rule 60 permit source 10.39.1.0 0.0.0.255
 rule 65 permit source 10.99.204.0 0.0.0.255
 {{login_acl}}
 ''')

    def snmp_acl():
        return Template('''
acl basic 2010
 rule 0 permit source 10.14.0.0 0.0.0.255
 rule 5 permit source 10.14.34.0 0.0.0.255
 rule 10 permit source 10.14.67.0 0.0.0.255
 rule 15 permit source 10.14.203.0 0.0.0.255
 rule 20 permit source 10.34.27.0 0.0.0.255
 rule 25 permit source 10.99.130.0 0.0.0.255
 rule 30 permit source 10.99.204.0 0.0.0.255
 ''')

    def snmp_config():
        return '''
 snmp-agent
 snmp-agent community read simple tencent acl 2010
 snmp-agent sys-info version v2c
'''

    def ntp_config():
        return '''
 ntp-service enable
 ntp-service unicast-server 10.14.0.136
 ntp-service unicast-server 10.14.198.20
'''

    def domain_lookup():
        return '''
domain tencent
 authentication lan-access radius-scheme tencent
 authorization lan-access radius-scheme tencent
 accounting lan-access radius-scheme tencent
#
domain tencent_domain
 authentication login hwtacacs-scheme tencent_scheme local
 authorization login hwtacacs-scheme tencent_scheme local
 accounting login hwtacacs-scheme tencent_scheme local
 authorization command hwtacacs-scheme tencent_scheme none
 accounting command hwtacacs-scheme tencent_scheme
#
 domain default enable tencent_domain
'''

    def local_user():
        return '''
local-user netman class manage
 password simple tencent@123
 service-type telnet ssh terminal
 authorization-attribute user-role network-admin
'''

class h3c_port_config_template:
    def loopback0():
        return Template('''
interface LoopBack0
 ip address {{ipaddress}} {{netmask}}
''')

    def lay3_phy_interface_config():
        return Template('''
interface {{phy_interface}}
 port link-mode route
 description {{description}}
 ip address {{ipaddress}} {{netmask}}
''')

    def lay2_phy_interface_config():
        return Template('''
interface {{phy_interface}}
 port link-mode bridge
 description {{description}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 dldp enable
''')

    def interconnect_phy_interface_config():
        return Template('''
interface {{phy_interface}}
 port link-mode bridge
 description {{description}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 dldp enable
 port link-aggregation group 1
    ''')

    def port_channel_interface_config():
        return Template('''
interface {{port_channel}}
 description {{description}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 link-aggregation mode dynamic
''')


    def vlan_config():
        return Template('''
vlan {{vlan_num}}
 name {{vlan_des}}
''')

    def mater_interface_vlan_config():
        return Template('''
interface {{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vlan_num}} {{vrrp_ip}}
 vrrp vrid {{vlan_num}} priority 120
 packet-filter name {{acl_name}} inbound
 dhcp select relay
 dhcp relay server-address {{master_dhcp}}
 dhcp relay server-address {{slave_dhcp}}
''')

    def slaver_interface_vlan_config():
        return Template('''
interface {{interface_vlan}}
 description {{vlan_des}}
 ip address {{slaver_vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vlan_num}} {{vrrp_ip}}
 packet-filter name {{acl_name}} inbound
 dhcp select relay
 dhcp relay server-address {{master_dhcp}}
 dhcp relay server-address {{slave_dhcp}}
''')


class route_config:
    def undo_silcent():
        return Template('''
 undo silent-interface {{interconnect_interface}}
 undo silent-interface {{mgt_vlan_num}}
        ''')

    def network_area():
        return Template('''
 area {{core_network}}
  network {{ipaddress}} 0.0.0.0
  stub
        ''')
    def ospf_config():
        return Template('''
router ospf 100
 silent-interface all
''')

