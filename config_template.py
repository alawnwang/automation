from jinja2 import Template
class config_template:
#

    def sysname():
        return Template('''sysname {{sysname}}
''')

    def time_zone():
        return '\n'+'''clock timezone CST add 08:00:00
'''

    def login_acl_use():
        return '''
telnet server enable
telnet server acl 2000
#
ssh server enable
ssh server acl 2000
'''
    def dldp_lldp():
        return '''
dhcp enable
#
lldp global enable
#
dldp global enable
'''

    def line_aux():
        return '''
 line aux 0
 authentication-mode password
 user-role network-admin
 set authentication password simple 11111
'''

    def vty():
        return '''
line vty 0 4
 authentication-mode scheme
 user-role network-admin
 user-role network-operator
 command authorization
 command accounting
'''

    def logging():
        return '''
 info-center logbuffer size 1024
 info-center loghost source Vlan-interface10
 info-center loghost 10.34.27.26
 info-center loghost 10.99.130.23
 info-center loghost 10.99.204.32
 info-center loghost 10.99.204.82
 info-center source SHELL loghost deny
'''

    def ntp():
        return '''
 ntp-service enable
 ntp-service unicast-server 10.28.0.20
 ntp-service unicast-server 10.14.198.20
'''
    def stp_config():
        return '''
stp region-configuration
 region-name RG
 instance 1 vlan 1 to 99 110 to 4094 
 instance 2 vlan 100 to 109 
 active region-configuration
'''

    def advance_acl():
        return '''
acl advanced name AP
 rule 5 permit icmp
 rule 10 permit udp source-port eq 1985
 rule 15 permit udp source-port eq bootpc
 rule 20 permit udp destination-port eq bootps
 rule 25 permit udp destination-port eq dns
 rule 30 permit udp destination-port eq ntp
 rule 35 permit udp destination-port range 5246 5248
 rule 40 permit udp destination-port range 12222 12224
 rule 45 permit ip destination 10.123.127.0 0.0.0.255
 rule 50 permit ip destination 10.12.220.0 0.0.0.255
 rule 55 permit ip destination 10.6.5.0 0.0.0.255
 rule 60 permit ip destination 10.14.32.0 0.0.0.255
 rule 65 permit ip destination 10.80.224.0 0.0.0.255
 rule 70 permit ip destination 10.99.204.0 0.0.0.255
 rule 75 permit ip destination 10.32.1.0 0.0.0.255
 rule 80 permit ip destination 10.64.0.0 0.0.0.255
 rule 85 permit ip destination 10.68.0.0 0.0.0.255
 rule 90 permit ip destination 10.43.0.0 0.0.0.255
 rule 95 permit ip destination 10.44.0.0 0.0.0.255
 rule 100 permit ip destination 10.45.0.0 0.0.0.255
 rule 105 permit ip destination 10.45.128.0 0.0.0.255
 rule 110 permit ip destination 10.72.0.0 0.0.0.255
 rule 115 permit ip destination 10.73.0.0 0.0.0.255
 rule 120 permit ip destination 10.78.0.0 0.0.0.255
 rule 125 permit ip destination 10.79.0.0 0.0.0.255
 rule 130 permit ip destination 10.9.160.0 0.0.0.255
 rule 135 permit ip destination 10.7.0.128 0.0.0.127
 rule 140 permit ip destination 10.36.0.128 0.0.0.127
 rule 145 permit ip destination 10.94.49.208 0.0.0.15
 rule 150 permit ip destination 10.93.0.108 0
 rule 155 permit ip destination 10.93.128.0 0.0.0.31
 rule 160 permit ip destination 10.93.136.30 0
 rule 165 permit ip destination 10.93.144.68 0
 rule 170 permit ip destination 10.98.200.62 0
 rule 171 permit ip destination 10.39.0.128 0.0.0.63
 rule 175 deny ip
#
acl advanced name GELI
 rule 0 permit icmp
 rule 5 permit ip destination 224.0.0.18 0
 rule 10 permit udp source-port eq bootpc
 rule 15 permit udp destination-port eq bootps
 rule 20 permit udp destination-port eq dns
 rule 25 permit udp source-port eq ntp
 rule 30 permit ip destination 10.14.128.17 0
 rule 35 permit ip destination 10.28.64.100 0
 rule 40 permit tcp destination 10.28.43.0 0.0.0.255
 rule 45 permit tcp destination 10.28.70.0 0.0.0.255
 rule 50 permit tcp destination 10.99.65.128 0.0.0.127
 rule 55 permit tcp destination 10.99.196.224 0.0.0.31
 rule 60 permit tcp destination 10.99.245.192 0.0.0.63
 rule 65 permit tcp destination 17.249.0.0 0.0.255.255
 rule 70 permit tcp destination 17.252.0.0 0.0.255.255
 rule 75 permit tcp destination 17.57.144.0 0.0.3.255
 rule 80 permit tcp destination 17.188.128.0 0.0.63.255
 rule 85 permit tcp destination 17.188.20.0 0.0.1.255
 rule 90 deny ip
#
acl advanced name OA
 rule 0 permit icmp
 rule 5 permit udp source-port eq bootpc
 rule 10 permit udp destination-port eq bootps
 rule 15 permit udp destination-port eq dns
 rule 20 permit udp source-port eq ntp
 rule 25 deny tcp source-port range 1 1024
 rule 30 deny udp source-port range 1 1024
 rule 35 permit tcp destination 10.99.3.192 0.0.0.63 source-port eq 5900
 rule 40 permit tcp destination 10.99.16.0 0.0.1.255 source-port eq 5900
 rule 45 permit tcp destination 10.99.131.0 0.0.0.255 source-port eq 5900
 rule 50 permit tcp destination 10.99.139.0 0.0.0.255 source-port eq 5900
 rule 55 permit tcp destination 10.99.156.0 0.0.0.255 source-port eq 5900
 rule 60 permit tcp destination 10.99.162.160 0.0.0.31 source-port eq 5900
 rule 65 permit tcp destination 10.99.169.160 0.0.0.31 source-port eq 5900
 rule 70 permit tcp destination 10.99.195.0 0.0.0.63 source-port eq 5900
 rule 75 permit tcp destination 10.99.212.0 0.0.1.255 source-port eq 5900
 rule 80 permit tcp destination 10.14.87.128 0.0.0.127 source-port eq 5900
 rule 85 permit tcp destination 10.14.211.0 0.0.0.63 source-port eq 5900
 rule 90 permit tcp destination 10.96.208.0 0.0.1.255 source-port eq 5900
 rule 95 permit tcp destination 10.96.252.0 0.0.1.255 source-port eq 5900
 rule 100 permit tcp destination 10.96.154.0 0.0.1.255 source-port eq 5900
 rule 105 permit tcp destination 10.97.32.0 0.0.3.255 source-port eq 5900
 rule 110 permit tcp destination 10.90.0.0 0.0.127.255 source-port eq 5900
 rule 115 permit tcp destination 10.3.240.0 0.0.7.255 source-port eq 5900
 rule 120 deny tcp source-port eq 5900
 rule 125 permit tcp destination 10.99.3.192 0.0.0.63 source-port eq 3389
 rule 130 permit tcp destination 10.99.16.0 0.0.1.255 source-port eq 3389
 rule 135 permit tcp destination 10.99.131.0 0.0.0.255 source-port eq 3389
 rule 140 permit tcp destination 10.99.139.0 0.0.0.255 source-port eq 3389
 rule 145 permit tcp destination 10.99.156.0 0.0.0.255 source-port eq 3389
 rule 150 permit tcp destination 10.99.162.160 0.0.0.31 source-port eq 3389
 rule 155 permit tcp destination 10.99.169.160 0.0.0.31 source-port eq 3389
 rule 160 permit tcp destination 10.99.195.0 0.0.0.63 source-port eq 3389
 rule 165 permit tcp destination 10.99.212.0 0.0.1.255 source-port eq 3389
 rule 170 permit tcp destination 10.14.87.128 0.0.0.127 source-port eq 3389
 rule 175 permit tcp destination 10.14.211.0 0.0.0.63 source-port eq 3389
 rule 180 permit tcp destination 10.96.208.0 0.0.1.255 source-port eq 3389
 rule 185 permit tcp destination 10.96.252.0 0.0.1.255 source-port eq 3389
 rule 190 permit tcp destination 10.96.154.0 0.0.1.255 source-port eq 3389
 rule 195 permit tcp destination 10.97.32.0 0.0.3.255 source-port eq 3389
 rule 200 permit tcp destination 10.90.0.0 0.0.127.255 source-port eq 3389
 rule 205 permit tcp destination 10.3.240.0 0.0.7.255 source-port eq 3389
 rule 210 deny tcp source-port eq 3389
 rule 215 permit ip
#
acl advanced name OA-Device
 rule 0 permit icmp
 rule 5 permit ip destination 224.0.0.18 0
 rule 10 permit udp source-port eq bootpc
 rule 15 permit udp destination-port eq bootps
 rule 20 permit udp destination-port eq dns
 rule 25 permit udp destination-port eq ntp
 rule 30 permit udp source-port eq ntp
 rule 35 permit udp source-port eq snmp
 rule 40 permit tcp source-port range 9000 9100 destination-port range 9000 9100
 rule 45 permit udp source-port range 9000 9100 destination-port range 9000 9100
 rule 50 permit tcp source-port eq 9100
 rule 51 permit ip destination 10.6.210.77 0
 rule 52 permit ip destination 10.6.210.78 0.0.0.1
 rule 55 permit ip destination 10.14.8.50 0
 rule 60 permit ip destination 10.99.195.131 0
 rule 65 permit ip destination 10.99.195.167 0
 rule 70 permit ip destination 10.99.195.168 0
 rule 75 permit ip destination 10.99.195.172 0
 rule 80 permit ip destination 10.99.195.128 0.0.0.15
 rule 85 permit ip destination 10.28.9.93 0
 rule 90 permit ip destination 10.99.204.23 0
 rule 95 permit ip destination 10.99.204.44 0
 rule 100 permit ip destination 10.99.210.73 0
 rule 105 permit ip destination 10.99.210.74 0
 rule 110 permit ip destination 10.99.204.47 0
 rule 115 permit tcp destination 10.14.12.28 0 destination-port eq www
 rule 120 permit tcp destination 10.14.12.115 0 destination-port eq www
 rule 125 permit tcp destination 10.14.12.165 0 destination-port eq www
 rule 126 permit tcp destination 10.99.224.30 0
 rule 127 permit tcp destination 10.99.224.229 0
 rule 128 permit tcp destination 10.99.224.248 0
 rule 130 permit ip destination 10.99.6.176 0.0.0.15
 rule 135 permit ip destination 10.99.6.192 0.0.0.63
 rule 140 permit ip destination 10.99.8.0 0.0.0.15
 rule 145 permit ip destination 10.99.8.112 0.0.0.15
 rule 150 permit ip destination 10.99.8.128 0.0.0.31
 rule 155 permit ip destination 10.99.128.16 0.0.0.15
 rule 160 permit ip destination 10.99.128.32 0.0.0.15
 rule 165 permit ip destination 10.99.13.64 0.0.0.15
 rule 170 permit ip destination 10.99.137.0 0.0.0.31
 rule 175 permit ip destination 10.99.153.0 0.0.0.31
 rule 180 permit ip destination 10.99.198.48 0.0.0.15
 rule 185 permit ip destination 10.99.198.64 0.0.0.15
 rule 190 permit ip destination 10.99.137.192 0.0.0.15
 rule 195 permit ip destination 10.99.137.240 0.0.0.15
 rule 200 permit ip destination 10.99.153.96 0.0.0.15
 rule 205 permit ip destination 10.99.153.112 0.0.0.15
 rule 210 permit ip destination 10.99.128.64 0.0.0.63
 rule 215 permit ip destination 10.99.129.0 0.0.0.31
 rule 220 permit ip destination 10.99.198.176 0.0.0.15
 rule 225 permit ip destination 10.99.209.0 0.0.0.127
 rule 230 permit ip destination 10.14.87.0 0.0.0.63
 rule 235 permit ip destination 10.14.102.0 0.0.0.255
 rule 240 permit ip destination 10.14.212.0 0.0.0.255
 rule 245 permit ip destination 10.28.70.128 0.0.0.127
 rule 250 permit ip destination 10.28.86.0 0.0.0.63
 rule 255 permit ip destination 10.24.33.0 0.0.0.255
 rule 260 permit ip destination 10.33.27.0 0.0.0.63
 rule 265 permit ip destination 10.34.28.64 0.0.0.63
 rule 270 permit ip destination 10.76.2.0 0.0.0.127
 rule 275 permit tcp destination 10.28.6.13 0 destination-port eq smtp
 rule 280 permit tcp destination 10.123.118.211 0 destination-port eq smtp
 rule 285 permit tcp destination 10.28.6.13 0 source-port eq smtp
 rule 290 permit tcp destination 10.123.118.211 0 source-port eq smtp
 rule 295 permit tcp destination 10.123.118.214 0 destination-port eq smtp
 rule 300 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq www
 rule 305 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 443
 rule 310 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 843
 rule 315 deny udp destination 10.0.0.0 0.255.255.255 destination-port eq 8000
 rule 320 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 15000
 rule 325 deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq www
 rule 330 deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 443
 rule 335 deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 843
 rule 340 deny udp destination 11.0.0.0 0.255.255.255 destination-port eq 8000
 rule 345 deny tcp destination 11.0.0.0 0.255.255.255 destination-port eq 15000
 rule 350 deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq www
 rule 355 deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 443
 rule 360 deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 843
 rule 365 deny udp destination 30.0.0.0 0.255.255.255 destination-port eq 8000
 rule 370 deny tcp destination 30.0.0.0 0.255.255.255 destination-port eq 15000
 rule 375 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq www
 rule 380 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 443
 rule 385 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 843
 rule 390 deny udp destination 9.0.0.0 0.255.255.255 destination-port eq 8000
 rule 395 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 15000
 rule 400 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq www
 rule 405 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 443
 rule 410 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 843
 rule 415 deny udp destination 172.16.0.0 0.15.255.255 destination-port eq 8000
 rule 420 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 15000
 rule 425 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq www
 rule 430 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 443
 rule 435 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 843
 rule 440 deny udp destination 100.64.0.0 0.63.255.255 destination-port eq 8000
 rule 445 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 15000
 rule 450 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq www
 rule 455 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 443
 rule 460 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 843
 rule 465 deny udp destination 192.168.0.0 0.0.255.255 destination-port eq 8000
 rule 470 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 15000
 rule 475 permit tcp destination-port eq www
 rule 480 permit tcp destination-port eq 443
 rule 485 permit tcp destination-port eq 843
 rule 490 permit udp destination-port eq 8000
 rule 495 permit tcp destination-port eq 15000
 rule 500 deny ip
#
acl advanced name TY
 rule 0 deny icmp destination 10.14.0.0 0.0.255.255
 rule 5 deny icmp destination 10.28.0.0 0.0.255.255
 rule 10 deny icmp destination 10.88.0.0 0.0.255.255
 rule 15 deny icmp destination 10.99.0.0 0.0.255.255
 rule 20 permit icmp
 rule 25 permit udp source-port eq bootpc
 rule 30 permit udp destination-port eq bootps
 rule 35 permit udp destination-port eq dns
 rule 40 permit udp source-port eq ntp
 rule 45 deny ip destination 10.0.0.0 0.255.255.255
 rule 50 deny ip destination 11.0.0.0 0.255.255.255
 rule 55 deny ip destination 30.0.0.0 0.255.255.255
 rule 60 deny ip destination 172.16.0.0 0.15.255.255
 rule 65 deny ip destination 192.168.0.0 0.0.255.255
 rule 70 deny ip destination 9.0.0.0 0.255.255.255
 rule 75 deny ip destination 100.64.0.0 0.63.255.255
 rule 80 permit ip
#
acl advanced name VOIP
 rule 0 permit icmp
 rule 5 permit ip destination 224.0.0.18 0
 rule 10 permit udp source-port eq bootpc
 rule 15 permit udp destination-port eq bootps
 rule 20 permit udp destination-port eq dns
 rule 25 permit udp destination-port eq ntp
 rule 30 permit ip destination 10.11.6.0 0.0.0.255
 rule 35 permit ip destination 10.14.160.0 0.0.1.255
 rule 40 permit ip destination 10.1.138.0 0.0.0.255
 rule 45 permit ip destination 192.168.75.0 0.0.0.255
 rule 50 permit ip destination 10.6.100.0 0.0.0.255
 rule 51 permit ip destination 10.28.35.0 0.0.0.255
 rule 52 permit ip destination 10.41.106.0 0.0.0.255
 rule 55 permit ip destination 10.41.190.0 0.0.0.255
 rule 56 permit ip destination 10.99.204.161 0
 rule 57 permit ip destination 10.99.205.57 0
 rule 58 permit ip destination 10.99.205.85 0
 rule 60 permit udp destination-port range 16384 32767
 rule 65 permit udp source-port range 16384 32767
 rule 70 deny ip
#
acl advanced name Video
 rule 0 permit icmp
 rule 5 permit ip destination 224.0.0.18 0
 rule 10 permit udp source-port eq bootpc
 rule 15 permit udp destination-port eq bootps
 rule 20 permit udp destination-port eq dns
 rule 25 permit udp destination-port eq ntp
 rule 30 permit tcp destination-port eq 1719
 rule 35 deny tcp destination-port eq 3389
 rule 40 deny tcp destination-port eq 3306
 rule 45 deny tcp destination-port eq 5800
 rule 50 deny tcp destination-port eq 5900
 rule 55 deny tcp destination-port eq 36000
 rule 60 deny tcp destination-port eq 56000
 rule 65 permit tcp destination-port gt 2325
 rule 70 permit udp destination-port eq 1720
 rule 75 permit udp destination-port gt 2325
 rule 80 permit tcp destination 10.12.220.0 0.0.1.255 source-port eq 22
 rule 85 permit tcp destination 10.12.220.0 0.0.1.255 source-port eq telnet
 rule 90 permit tcp destination 10.12.220.0 0.0.1.255 source-port eq www
 rule 95 permit tcp destination 10.12.220.0 0.0.1.255 source-port eq 443
 rule 100 permit tcp destination 10.123.127.0 0.0.0.255 source-port eq 22
 rule 105 permit tcp destination 10.123.127.0 0.0.0.255 source-port eq telnet
 rule 110 permit tcp destination 10.123.127.0 0.0.0.255 source-port eq www
 rule 115 permit tcp destination 10.123.127.0 0.0.0.255 source-port eq 443
 rule 120 permit tcp destination 10.123.129.0 0.0.0.255 source-port eq 22
 rule 125 permit tcp destination 10.123.129.0 0.0.0.255 source-port eq telnet
 rule 130 permit tcp destination 10.123.129.0 0.0.0.255 source-port eq www
 rule 135 permit tcp destination 10.123.129.0 0.0.0.255 source-port eq 443
 rule 140 permit tcp destination 10.123.138.0 0.0.0.255 source-port eq 22
 rule 145 permit tcp destination 10.123.138.0 0.0.0.255 source-port eq telnet
 rule 150 permit tcp destination 10.123.138.0 0.0.0.255 source-port eq www
 rule 155 permit tcp destination 10.123.138.0 0.0.0.255 source-port eq 443
 rule 160 permit ip destination 10.99.204.143 0
 rule 165 permit ip destination 10.14.83.102 0.0.0.1
 rule 170 permit ip destination 10.99.195.88 0
 rule 175 permit ip destination 10.14.83.126 0
 rule 180 permit ip destination 10.14.13.63 0
 rule 185 permit ip destination 10.14.83.25 0
 rule 190 permit ip destination 10.14.85.51 0
 rule 195 permit ip destination 10.14.86.100 0
 rule 200 permit ip destination 10.93.0.136 0
 rule 205 permit ip destination 10.93.0.134 0
 rule 210 permit ip destination 10.11.16.91 0
 rule 215 permit ip destination 10.14.32.101 0
 rule 220 permit ip destination 10.14.32.102 0.0.0.1
 rule 225 permit ip destination 10.14.32.104 0
 rule 230 permit ip destination 10.11.16.102 0
 rule 235 permit ip destination 10.11.16.105 0
 rule 240 permit ip destination 10.11.16.106 0
 rule 245 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq www
 rule 250 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 443
 rule 255 deny tcp destination 10.0.0.0 0.255.255.255 destination-port eq 843
 rule 260 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq www
 rule 265 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 443
 rule 270 deny tcp destination 9.0.0.0 0.255.255.255 destination-port eq 843
 rule 275 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq www
 rule 280 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 443
 rule 285 deny tcp destination 172.16.0.0 0.15.255.255 destination-port eq 843
 rule 290 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq www
 rule 295 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 443
 rule 300 deny tcp destination 100.64.0.0 0.63.255.255 destination-port eq 843
 rule 305 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq www
 rule 310 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 443
 rule 315 deny tcp destination 192.168.0.0 0.0.255.255 destination-port eq 843
 rule 320 permit tcp destination-port eq www
 rule 325 permit tcp destination-port eq 443
 rule 330 permit tcp destination-port eq 843
 rule 335 deny ip
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
 key authentication simple tencent
 key authorization simple tencent
 key accounting simple tencent
 user-name-format without-domain
 nas-ip {{nas_ip}}
''')

    def stand_login_acl():
        return '''
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
 rule 65 permit source 10.99.204.0 0.0.0.255'''

    def floor_login_acl():
        return Template('''
{{login_acl}}
''')

    def snmp_acl():
        return'''
acl basic 2010
 rule 0 permit source 10.14.0.0 0.0.0.255
 rule 5 permit source 10.14.34.0 0.0.0.255
 rule 10 permit source 10.14.67.0 0.0.0.255
 rule 15 permit source 10.14.203.0 0.0.0.255
 rule 20 permit source 10.34.27.0 0.0.0.255
 rule 25 permit source 10.99.130.0 0.0.0.255
 rule 30 permit source 10.99.204.0 0.0.0.255
'''

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
#
radius scheme system
 user-name-format without-domain
#
domain system
#
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
 password simple 1111111
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
#
''')

    def oa_lay2_phy_interface_config():
        return Template('''
interface {{phy_interface}}
 port link-mode bridge
 description {{description}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 speed 2500
 dldp enable
#''')

    def normal_lay2_phy_interface_config():
        return Template('''
interface {{phy_interface}}
 port link-mode bridge
#''')

    def voip_lay2_phy_interface_config():
        return Template('''
interface {{phy_interface}}
 port link-mode bridge
 description {{description}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 dldp enable
#''')

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
#
''')

    def port_channel_interface_config():
        return Template('''
interface Bridge-Aggregation1
 description {{description}}-Agg1
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 link-aggregation mode dynamic
''')


    def vlan_config():
        return Template('''
#
vlan {{vlan_num}}
 name {{vlan_des}}
 {{arp_detection}}
''')





    def gloabl_acl():
        return Template('\n'+''' packet-filter name {{acl_name}} vlan-interface {{vlan_num}} inbound
''')

    def master_stp():
        return '''
#
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
#'''


    def slaver_stp():
        return '''
#
stp region-configuration
 region-name RG
 instance 1 vlan 1 to 99 110 to 679 690 to 4094 
 instance 2 vlan 100 to 109 680 to 689 
 active region-configuration
#
 stp instance 0 to 1 priority 16384
 stp instance 2 priority 8192
 stp bpdu-protection
 stp global enable
#'''


    def vlan10_mater_interface_vlan_config():
        return Template('''
#
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vlan_num}} virtual-ip  {{vrrp_ip}}
 vrrp vrid {{vlan_num}} priority 120
''')

    def vlan10_slaver_interface_vlan_config():
        return Template('''
#
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vlan_num}} virtual-ip {{vrrp_ip}}
''')

    def normal_mater_interface_vlan_config():
        return Template('''
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip  {{vrrp_ip}}
 vrrp vrid {{vrrp_num}} priority 120
 packet-filter name {{acl_name}} inbound
 dhcp select relay
''')

    def normal_slaver_interface_vlan_config():
        return Template('''
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip {{vrrp_ip}}
 packet-filter name {{acl_name}} inbound
 dhcp select relay
''')

    def voip_mater_interface_vlan_config():
        return Template('''
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip  {{vrrp_ip}}
 packet-filter name {{acl_name}} inbound
 dhcp select relay
''')

    def voip_slaver_interface_vlan_config():
        return Template('''
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vlan_num}} virtual-ip {{vrrp_ip}}
 vrrp vrid {{vrrp_num}} priority 120
 packet-filter name {{acl_name}} inbound
 dhcp select relay
''')

    def global_normal_mater_interface_vlan_config():
        return Template('''
#
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip {{vrrp_ip}}
 vrrp vrid {{vrrp_num}} priority 120
 dhcp select relay
''')

    def global_normal_slaver_interface_vlan_config():
        return Template('''
#
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip {{vrrp_ip}}
 dhcp select relay
''')

    def global_voip_mater_interface_vlan_config():
        return Template('''
#
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip  {{vrrp_ip}}
 dhcp select relay
''')

    def global_voip_slaver_interface_vlan_config():
        return Template('''
#
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
 vrrp vrid {{vrrp_num}} virtual-ip  {{vrrp_ip}}
 vrrp vrid {{vrrp_num}} priority 120
 dhcp select relay
''')
    def dhcp_relay():
        return Template('\n'+''' dhcp relay server-address {{dhcp_relay}}
''')

    def access_mgt_interface_vlan_config():
        return Template('''
interface Vlan-interface{{interface_vlan}}
 description {{vlan_des}}
 ip address {{vlan_ipaddress}} {{vlan_netmask}}
''')

    def access_default_gateway():
        return Template('''
ip route-static 0.0.0.0 0 {{gateway}}
''' )

    def oa_access_interface():
        return Template('''
interface range GigabitEthernet1/0/1 to GigabitEthernet1/0/48
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan_num}} untagged
 port hybrid pvid vlan {{vlan_num}}
 mac-vlan enable
 storm-constrain broadcast pps 300 300
 storm-constrain control block
 stp edged-port
 arp rate-limit 200
 undo dot1x handshake
 dot1x mandatory-domain tencent
 dot1x max-user 1
 undo dot1x multicast-trigger
 dot1x unicast-trigger
 dot1x guest-vlan 666
 dot1x auth-fail vlan 666
 dot1x critical vlan 666
 port-security intrusion-mode blockmac
 port-security max-mac-count 1
 port-security port-mode mac-else-userlogin-secure
 dhcp snooping rate-limit 300
 dhcp snooping binding record
 dhcp snooping check request-message
''')

    def evp_access_interface():
        return Template('''
interface range GigabitEthernet1/0/1 to GigabitEthernet1/0/48
 port access vlan {{vlan_num}}
 stp edged-port
 poe enable
 undo dot1x handshake
 dot1x mandatory-domain tencent
 dot1x max-user 1
 undo dot1x multicast-trigger
 dot1x unicast-trigger
 port-security intrusion-mode blockmac
 port-security max-mac-count 1
 port-security port-mode userlogin-secure
 ''')


    def ewl_access_interface():
        return '''
interface range GigabitEthernet1/0/1 to GigabitEthernet1/0/48
 port link-mode bridge
 description To_AP
 port access vlan 11
 speed 1000 
 duplex full
 stp edged-port
 poe enable
'''
    def access_uplink():
        return Template('''
interface {{port_num}}
 description {{A_devicename}}-{{A_port}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 speed 2500 
 stp loop-protection
 dldp enable   
 arp detection trust
 dhcp snooping trust
#''')

    def xoa_radius():
        return '''
radius scheme tencent
 primary authentication 10.99.220.200 28882
 secondary authentication 10.99.145.4 28882
 key authentication simple 11111
 user-name-format without-domain
 attribute 31 mac-format section six separator - lowercase 
'''

    def evp_radius():
        return '''
radius scheme tencent
 primary authentication 10.14.32.81
 primary accounting 10.14.32.81
 secondary authentication 10.14.160.81
 secondary accounting 10.14.160.81
 key authentication simple 11111
 key accounting simple 11111
 user-name-format without-domain
 attribute 31 mac-format section six separator - lowercase 
'''


class route_config:
    def ospf_config():
        return Template('\n'+''' ospf 100 route-id {{mgt_ip}}
 silent-interface all'''+'\n')
    def undo_silcent():
        return Template('\n'+''' undo silent-interface {{interconnect_interface}}
 undo silent-interface {{mgt_vlan_num}}'''+'\n')
    def network_area():
        return Template('\n'+''' area {{core_network}}'''+'\n')
    def network():
        return Template('\n'+'''  network {{ipaddress}} 0.0.0.0'''+'\n')



