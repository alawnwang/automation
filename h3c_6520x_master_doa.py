from jinja2 import Template

def h3c_6520x_master_doa():
    return Template('''#
 version 7.1.070, Release 6533
#
 sysname {{sysname}}
 #
 clock timezone CST add 08:00:00
#
 telnet server enable
 telnet server acl 2000
 telnet server ipv6 acl ipv6 3000
#
 irf mac-address persistent timer
 irf auto-update enable
 undo irf link-delay
 irf member 1 priority 1
#
{{packet_filter}}
#
 link-aggregation global load-sharing mode dåestination-ip source-ip
#
ospf 100 router-id {{router_id}}
 silent-interface all
 {{undo_silent_interface}}
 area {{area_id}}
  {{ospf_network}}
  stub
#
 dhcp enable
#
 lldp global enable
#
 dldp global enable
#
 password-recovery enable
#
{{layer2_vlan}}
stp region-configuration
 region-name RG
 instance 1 vlan 1 to 99 110 to 679 690 to 4094
 instance 2 vlan 100 to 109 680 to 689
 active region-configuration
#
 stp instance 0 to 1 priority 8192
 stp instance 2 priority 16384
 stp bpdu-protection
 stp global enable
#
interface Bridge-Aggregation1
 description {{interconnect_device}}-{{interconnect_bagg_port}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 link-aggregation mode dynamic
#
interface NULL0
{{layer3_interface_vlan}}
#
interface M-GigabitEthernet0/0/0
#
interface Ten-GigabitEthernet1/0/49:1
 port link-mode route
 description {{uplink_device_name}}-{{uplink_port_num}}
 ip address {{uplink_address}} {{uplink_netmask}}
#

#
 scheduler logfile size 16
#
line class aux
 user-role network-admin
#
line class usb
 user-role network-admin
#
line class vty
 user-role network-operator
#
line aux 0
 authentication-mode password
 user-role network-admin
 set authentication password simple {{console_password}}
#
line vty 0 4
 authentication-mode scheme
 user-role network-admin
 user-role network-operator
 command authorization
 command accounting
#
line vty 5 63
 user-role network-operator
#
 info-center logbuffer size 1024
 info-center loghost source Vlan-interface10
 info-center loghost 10.34.27.26
 info-center loghost 10.99.130.23
 info-center loghost 10.99.204.32
 info-center loghost 10.99.204.82
 info-center source SHELL loghost deny
#
 snmp-agent
 snmp-agent community read simple tencent acl 2010
 snmp-agent sys-info version v2c v3
#
 ssh server enable
 ssh server acl 2000
 ssh server ipv6 acl ipv6 3000
#
 ntp-service enable
 ntp-service unicast-server 10.28.0.20
 ntp-service unicast-server 10.14.198.20
#
acl number 2000 name CL
 rule permit source 10.12.220.0 0.0.0.255
 rule permit source 10.123.127.0 0.0.0.255
 rule permit source 10.14.90.0 0.0.0.255
 rule permit source 10.99.130.0 0.0.0.255
 rule permit source 10.99.204.0 0.0.0.255
 rule permit source 10.99.196.224 0.0.0.31
 rule permit source 10.14.67.0 0.0.0.255
 rule permit source 10.14.34.0 0.0.0.255
 rule permit source 10.14.70.0 0.0.0.255
 rule permit source 10.14.64.0 0.0.0.255
 rule permit source 10.80.15.192 0.0.0.63
 rule permit source 10.76.83.0 0.0.0.255
 rule permit source 10.76.1.0 0.0.0.3
 rule permit source 10.6.3.0 0.0.0.3
 {{local_manage_network}}

#
acl basic 2010
 rule permit source 10.14.0.0 0.0.0.255
 rule permit source 10.14.34.0 0.0.0.255
 rule permit source 10.14.67.0 0.0.0.255
 rule permit source 10.14.203.0 0.0.0.255
 rule permit source 10.34.27.0 0.0.0.255
 rule permit source 10.99.130.0 0.0.0.255
 rule permit source 10.99.204.0 0.0.0.255
#
acl advanced name AP
 rule permit icmp
 rule permit ip destination 224.0.0.18 0
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp destination-port eq ntp
 rule permit udp destination-port range 5246 5248
 rule permit udp destination-port range 12222 12224
 rule permit ip destination 10.123.127.0 0.0.0.255
 rule permit ip destination 10.12.220.0 0.0.0.255
 rule permit ip destination 10.6.5.0 0.0.0.255
 rule permit ip destination 10.14.32.0 0.0.0.255
 rule permit ip destination 10.80.224.0 0.0.0.255
 rule permit ip destination 10.99.204.0 0.0.0.255
 rule permit ip destination 10.32.1.0 0.0.0.255
 rule permit ip destination 10.64.0.0 0.0.0.255
 rule permit ip destination 10.68.0.0 0.0.0.255
 rule permit ip destination 10.43.0.0 0.0.0.255
 rule permit ip destination 10.44.0.0 0.0.0.255
 rule permit ip destination 10.45.0.0 0.0.0.255
 rule permit ip destination 10.45.128.0 0.0.0.255
 rule permit ip destination 10.72.0.0 0.0.0.255
 rule permit ip destination 10.73.0.0 0.0.0.255
 rule permit ip destination 10.78.0.0 0.0.0.255
 rule permit ip destination 10.79.0.0 0.0.0.255
 rule permit ip destination 10.9.160.0 0.0.0.255
 rule permit ip destination 10.35.0.0 0.0.0.255
 rule permit ip destination 10.7.0.128 0.0.0.127
 rule permit ip destination 10.36.0.128 0.0.0.127
 rule permit ip destination 10.94.49.208 0.0.0.15
 rule permit ip destination 10.93.0.108 0
 rule permit ip destination 10.93.128.0 0.0.0.31
 rule permit ip destination 10.93.136.30 0
 rule permit ip destination 10.93.144.68 0
 rule permit ip destination 10.98.200.62 0
 rule deny ip
#
acl advanced name GELI
 rule permit icmp
 rule permit ip destination 224.0.0.18 0
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp source-port eq ntp
 rule permit ip destination 10.14.128.17 0
 rule permit ip destination 10.28.64.100 0
 rule permit tcp destination 10.28.43.0 0.0.0.255
 rule permit tcp destination 10.28.70.0 0.0.0.255
 rule permit tcp destination 10.99.65.128 0.0.0.127
 rule permit tcp destination 10.99.196.224 0.0.0.31
 rule permit tcp destination 10.99.245.192 0.0.0.63
 rule permit tcp destination 17.249.0.0 0.0.255.255
 rule permit tcp destination 17.252.0.0 0.0.255.255
 rule permit tcp destination 17.57.144.0 0.0.3.255
 rule permit tcp destination 17.188.128.0 0.0.63.255
 rule permit tcp destination 17.188.20.0 0.0.1.255
 rule deny ip
#
acl advanced name OA
 rule permit icmp
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp source-port eq ntp
 rule deny tcp source-port range 1 1024
 rule deny udp source-port range 1 1024
 rule permit tcp destination 10.99.3.192 0.0.0.63 source-port eq 5900
 rule permit tcp destination 10.99.16.0 0.0.1.255 source-port eq 5900
 rule permit tcp destination 10.99.131.0 0.0.0.255 source-port eq 5900
 rule permit tcp destination 10.99.139.0 0.0.0.255 source-port eq 5900
 rule permit tcp destination 10.99.156.0 0.0.0.255 source-port eq 5900
 rule permit tcp destination 10.99.162.160 0.0.0.31 source-port eq 5900
 rule permit tcp destination 10.99.169.160 0.0.0.31 source-port eq 5900
 rule permit tcp destination 10.99.195.0 0.0.0.63 source-port eq 5900
 rule permit tcp destination 10.99.212.0 0.0.1.255 source-port eq 5900
 rule permit tcp destination 10.14.87.128 0.0.0.127 source-port eq 5900
 rule permit tcp destination 10.14.211.0 0.0.0.63 source-port eq 5900
 rule permit tcp destination 10.96.208.0 0.0.1.255 source-port eq 5900
 rule permit tcp destination 10.96.252.0 0.0.1.255 source-port eq 5900
 rule permit tcp destination 10.96.154.0 0.0.1.255 source-port eq 5900
 rule permit tcp destination 10.97.32.0 0.0.3.255 source-port eq 5900
 rule permit tcp destination 10.90.0.0 0.0.127.255 source-port eq 5900
 rule permit tcp destination 10.3.240.0 0.0.7.255 source-port eq 5900
 rule deny tcp source-port eq 5900
 rule permit tcp destination 10.99.3.192 0.0.0.63 source-port eq 3389
 rule permit tcp destination 10.99.16.0 0.0.1.255 source-port eq 3389
 rule permit tcp destination 10.99.131.0 0.0.0.255 source-port eq 3389
 rule permit tcp destination 10.99.139.0 0.0.0.255 source-port eq 3389
 rule permit tcp destination 10.99.156.0 0.0.0.255 source-port eq 3389
 rule permit tcp destination 10.99.162.160 0.0.0.31 source-port eq 3389
 rule permit tcp destination 10.99.169.160 0.0.0.31 source-port eq 3389
 rule permit tcp destination 10.99.195.0 0.0.0.63 source-port eq 3389
 rule permit tcp destination 10.99.212.0 0.0.1.255 source-port eq 3389
 rule permit tcp destination 10.14.87.128 0.0.0.127 source-port eq 3389
 rule permit tcp destination 10.14.211.0 0.0.0.63 source-port eq 3389
 rule permit tcp destination 10.96.208.0 0.0.1.255 source-port eq 3389
 rule permit tcp destination 10.96.252.0 0.0.1.255 source-port eq 3389
 rule permit tcp destination 10.96.154.0 0.0.1.255 source-port eq 3389
 rule permit tcp destination 10.97.32.0 0.0.3.255 source-port eq 3389
 rule permit tcp destination 10.90.0.0 0.0.127.255 source-port eq 3389
 rule permit tcp destination 10.3.240.0 0.0.7.255 source-port eq 3389
 rule deny tcp source-port eq 3389
 rule permit ip
#
acl advanced name OA-Device
 rule permit icmp
 rule permit ip destination 224.0.0.18 0
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp destination-port eq ntp
 rule permit udp source-port eq ntp
 rule permit udp source-port eq snmp
 rule permit tcp source-port range 9000 9100 destination-port range 9000 9100
 rule permit udp source-port range 9000 9100 destination-port range 9000 9100
 rule permit tcp source-port eq 9100
 rule permit ip destination 10.6.210.77 0
 rule permit ip destination 10.6.210.78 0.0.0.1
 rule permit ip destination 10.14.8.50 0
 rule permit ip destination 10.99.195.131 0
 rule permit ip destination 10.99.195.167 0
 rule permit ip destination 10.99.195.168 0
 rule permit ip destination 10.99.195.172 0
 rule permit ip destination 10.99.195.128 0.0.0.15
 rule permit ip destination 10.28.9.93 0
 rule permit ip destination 10.99.204.23 0
 rule permit ip destination 10.99.204.44 0
 rule permit ip destination 10.99.204.47 0
 rule permit ip destination 10.99.220.80 0
 rule permit tcp destination 10.14.12.28 0 destination-port eq www
 rule permit tcp destination 10.14.12.115 0 destination-port eq www
 rule permit tcp destination 10.14.12.165 0 destination-port eq www
 rule permit tcp destination 10.99.224.30 0
 rule permit tcp destination 10.99.224.229 0
 rule permit tcp destination 10.99.224.248 0
 rule permit tcp destination 10.14.12.62 0 destination-port eq www
 rule permit tcp destination 10.14.12.171 0 destination-port eq www
 rule permit tcp destination 10.99.249.41 0 destination-port eq www
 rule permit tcp destination 10.99.249.20 0
 rule permit tcp destination 10.99.249.44 0
 rule permit tcp destination 10.99.249.221 0
 rule permit tcp destination 10.99.249.233 0
 rule permit ip destination 10.99.210.73 0
 rule permit ip destination 10.99.210.74 0
 rule permit ip destination 10.97.154.0 0.0.0.127
 rule permit ip destination 10.99.6.176 0.0.0.15
 rule permit ip destination 10.99.6.192 0.0.0.63
 rule permit ip destination 10.99.8.0 0.0.0.15
 rule permit ip destination 10.99.8.112 0.0.0.15
 rule permit ip destination 10.99.8.128 0.0.0.31
 rule permit ip destination 10.99.128.16 0.0.0.15
 rule permit ip destination 10.99.128.32 0.0.0.15
 rule permit ip destination 10.99.13.64 0.0.0.15
 rule permit ip destination 10.99.137.0 0.0.0.31
 rule permit ip destination 10.99.153.0 0.0.0.31
 rule permit ip destination 10.99.198.48 0.0.0.15
 rule permit ip destination 10.99.198.64 0.0.0.15
 rule permit ip destination 10.99.137.192 0.0.0.15
 rule permit ip destination 10.99.137.240 0.0.0.15
 rule permit ip destination 10.99.153.96 0.0.0.15
 rule permit ip destination 10.99.153.112 0.0.0.15
 rule permit ip destination 10.99.128.64 0.0.0.63
 rule permit ip destination 10.99.129.0 0.0.0.31
 rule permit ip destination 10.99.198.176 0.0.0.15
 rule permit ip destination 10.99.209.0 0.0.0.127
 rule permit ip destination 10.14.87.0 0.0.0.63
 rule permit ip destination 10.14.102.0 0.0.0.255
 rule permit ip destination 10.14.212.0 0.0.0.255
 rule permit ip destination 10.28.70.128 0.0.0.127
 rule permit ip destination 10.28.86.0 0.0.0.63
 rule permit ip destination 10.24.33.0 0.0.0.255
 rule permit ip destination 10.33.27.0 0.0.0.63
 rule permit ip destination 10.34.28.64 0.0.0.63
 rule permit ip destination 10.76.2.0 0.0.0.127
 rule permit tcp destination 10.28.6.13 0 destination-port eq smtp
 rule permit tcp destination 10.123.118.211 0 destination-port eq smtp
 rule permit tcp destination 10.28.6.13 0 source-port eq smtp
 rule permit tcp destination 10.123.118.211 0 source-port eq smtp
 rule permit tcp destination 10.123.118.214 0 destination-port eq smtp
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 843
 rule deny udp destination 10.0.0.0 0.255.255.255 destination-port eq 8000
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 15000
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 843
 rule deny udp destination 11.0.0.0 0.255.255.255 destination-port eq 8000
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 15000
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 843
 rule deny udp destination 30.0.0.0 0.255.255.255 destination-port eq 8000
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 15000
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 843
 rule deny udp destination 9.0.0.0 0.255.255.255 destination-port eq 8000
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 15000
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq www
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 443
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 843
 rule deny udp destination 172.16.0.0 0.15.255.255 destination-port eq 8000
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 15000
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq www
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 443
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 843
 rule deny udp destination 100.64.0.0 0.63.255.255 destination-port eq 8000
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 15000
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq www
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 443
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 843
 rule deny udp destination 192.168.0.0 0.0.255.255 destination-port eq 8000
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 15000
 rule permit tcp destination-port eq www
 rule permit tcp destination-port eq 443
 rule permit tcp destination-port eq 843
 rule permit udp destination-port eq 8000
 rule permit tcp destination-port eq 15000
 rule deny ip
#
acl advanced name TY
 rule deny icmp destination 10.14.0.0 0.0.255.255
 rule deny icmp destination 10.28.0.0 0.0.255.255
 rule deny icmp destination 10.88.0.0 0.0.255.255
 rule deny icmp destination 10.99.0.0 0.0.255.255
 rule permit icmp
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp source-port eq ntp
 rule deny ip destination 10.0.0.0 0.255.255.255
 rule deny ip destination 11.0.0.0 0.255.255.255
 rule deny ip destination 30.0.0.0 0.255.255.255
 rule deny ip destination 172.16.0.0 0.15.255.255
 rule deny ip destination 192.168.0.0 0.0.255.255
 rule deny ip destination 9.0.0.0 0.255.255.255
 rule deny ip destination 100.64.0.0 0.63.255.255
 rule permit ip
#
acl advanced name VOIP
 rule permit icmp
 rule permit ip destination 224.0.0.18 0
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp destination-port eq ntp
 rule permit ip destination 10.99.204.161 0
 rule permit ip destination 10.99.205.57 0
 rule permit ip destination 10.99.205.85 0
 rule permit ip destination 10.28.33.0 0.0.0.255
 rule permit ip destination 10.28.35.0 0.0.0.255
 rule permit ip destination 10.41.105.0 0.0.0.255
 rule permit ip destination 10.41.106.0 0.0.0.255
 rule permit ip destination 10.11.6.0 0.0.0.255
 rule permit ip destination 10.14.160.0 0.0.1.255
 rule permit ip destination 10.1.138.0 0.0.0.255
 rule permit ip destination 192.168.75.0 0.0.0.255
 rule permit ip destination 10.6.100.0 0.0.0.255
 rule permit ip destination 10.41.190.0 0.0.0.255
 rule permit udp destination-port range 16384 32767
 rule permit udp source-port range 16384 32767
 rule deny ip
#
acl advanced name Video
 rule permit icmp
 rule permit ip destination 224.0.0.18 0
 rule permit udp source-port eq bootpc
 rule permit udp destination-port eq bootps
 rule permit udp destination-port eq dns
 rule permit udp destination-port eq ntp
 rule deny tcp destination-port eq 3389
 rule deny tcp destination-port eq 3306
 rule deny tcp destination-port eq 5800
 rule deny tcp destination-port eq 5900
 rule deny tcp destination-port eq 36000
 rule deny tcp destination-port eq 56000
 rule permit tcp destination-port gt 2325
 rule permit udp destination-port gt 2325
 rule permit tcp destination-port eq 1719
 rule permit udp destination-port eq 1720
 rule permit tcp destination 10.12.220.0 0.0.1.255 source-port eq 22
 rule permit tcp destination 10.12.220.0 0.0.1.255 source-port eq telnet
 rule permit tcp destination 10.12.220.0 0.0.1.255 source-port eq www
 rule permit tcp destination 10.12.220.0 0.0.1.255 source-port eq 443
 rule permit tcp destination 10.123.127.0 0.0.0.255 source-port eq 22
 rule permit tcp destination 10.123.127.0 0.0.0.255 source-port eq telnet
 rule permit tcp destination 10.123.127.0 0.0.0.255 source-port eq www
 rule permit tcp destination 10.123.127.0 0.0.0.255 source-port eq 443
 rule permit tcp destination 10.123.129.0 0.0.0.255 source-port eq 22
 rule permit tcp destination 10.123.129.0 0.0.0.255 source-port eq telnet
 rule permit tcp destination 10.123.129.0 0.0.0.255 source-port eq www
 rule permit tcp destination 10.123.129.0 0.0.0.255 source-port eq 443
 rule permit tcp destination 10.123.138.0 0.0.0.255 source-port eq 22
 rule permit tcp destination 10.123.138.0 0.0.0.255 source-port eq telnet
 rule permit tcp destination 10.123.138.0 0.0.0.255 source-port eq www
 rule permit tcp destination 10.123.138.0 0.0.0.255 source-port eq 443
 rule permit ip destination 10.99.195.88 0
 rule permit ip destination 10.99.204.143 0
 rule permit ip destination 10.14.83.102 0.0.0.1
 rule permit ip destination 10.14.83.126 0
 rule permit ip destination 10.14.13.63 0
 rule permit ip destination 10.14.83.25 0
 rule permit ip destination 10.14.85.51 0
 rule permit ip destination 10.14.86.100 0
 rule permit ip destination 10.93.0.136 0
 rule permit ip destination 10.93.0.134 0
 rule permit ip destination 10.11.16.91 0
 rule permit ip destination 10.14.32.101 0
 rule permit ip destination 10.14.32.102 0.0.0.1
 rule permit ip destination 10.14.32.104 0
 rule permit ip destination 10.11.16.102 0
 rule permit ip destination 10.11.16.105 0
 rule permit ip destination 10.11.16.106 0
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 843
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 843
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 843
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq www
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 443
 rule deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 843
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq www
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 443
 rule deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 843
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq www
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 443
 rule deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 843
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq www
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 443
 rule deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 843
 rule permit tcp destination-port eq www
 rule permit tcp destination-port eq 443
 rule permit tcp destination-port eq 843
 rule deny ip
#
acl ipv6 advanced 3000
 rule 10 deny ipv6
#
hwtacacs scheme tencent_scheme
 primary authentication 10.42.3.75
 primary authorization 10.42.3.75
 primary accounting 10.42.3.75
 secondary authentication 10.14.160.75
 secondary authorization 10.14.160.75
 secondary accounting 10.14.160.75
 key authentication simple tencent
 key authorization simple tencent
 key accounting simple tencent
 user-name-format without-domain
 nas-ip {{manage_ip}}
#
radius scheme system
 user-name-format without-domain
#
domain system
#
domain tencent_domain
 authentication login hwtacacs-scheme tencent_scheme local
 authorization login hwtacacs-scheme tencent_scheme local
 accounting login hwtacacs-scheme tencent_scheme local
 authorization command hwtacacs-scheme tencent_scheme none
 accounting command hwtacacs-scheme tencent_scheme
#
 domain default enable tencent_domain
#
role name level-0
 description Predefined level-0 role
#
role name level-1
 description Predefined level-1 role
#
role name level-2
 description Predefined level-2 role
#
role name level-3
 description Predefined level-3 role
#
role name level-4
 description Predefined level-4 role
#
role name level-5
 description Predefined level-5 role
#
role name level-6
 description Predefined level-6 role
#
role name level-7
 description Predefined level-7 role
#
role name level-8
 description Predefined level-8 role
#
role name level-9
 description Predefined level-9 role
#
role name level-10
 description Predefined level-10 role
#
role name level-11
 description Predefined level-11 role
#
role name level-12
 description Predefined level-12 role
#
role name level-13
 description Predefined level-13 role
#
role name level-14
 description Predefined level-14 role
#
user-group system
#
local-user netman class manage
 password {{local_user_password}}
 service-type telnet ssh terminal
 authorization-attribute user-role network-admin
 authorization-attribute user-role network-operator
#
return''')
