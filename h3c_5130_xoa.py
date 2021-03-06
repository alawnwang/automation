from jinja2 import Template

def h3c_5130_xoa():
    return Template('''#
 version 7.1.070, Release 6328
#
 sysname {{sysname}}
#
 clock timezone CST add 08:00:00
#
 telnet server enable
 telnet server acl 2000
#
 irf mac-address persistent timer
 irf auto-update enable
 undo irf link-delay
 irf member 1 priority 1
#
 dot1x authentication-method eap
 dot1x timer tx-period 5
#
 mac-authentication domain tencent 
 mac-authentication user-name-format mac-address with-hyphen lowercase 
#
 port-security enable
#
 dhcp enable   
#
 dhcp snooping enable
#
 lldp global enable
#
 dldp global enable
#
 password-recovery enable
#
vlan 1
{{layer2_vlan}}
#
stp region-configuration
 region-name RG
 instance 1 vlan 1 to 99 110 to 679 690 to 4094 
 instance 2 vlan 100 to 109 680 to 689  
 active region-configuration
#
 stp bpdu-protection
 stp global enable
#
interface NULL0
#
interface Vlan-interface10
 ip address {{mgt_ip}} {{mgt_netmask}}
#
interface GigabitEthernet1/0/1
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/2
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/3
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/4
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/5
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/6
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/7
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/8
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#              
interface GigabitEthernet1/0/9
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/10
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/11
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/12
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/13
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/14
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/15
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/16
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/17
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/18
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/19
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/20
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/21
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/22
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/23
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/24
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/25
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/26
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/27
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/28
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/29
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/30
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/31
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#              
interface GigabitEthernet1/0/32
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/33
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/34
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/35
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/36
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/37
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/38
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/39
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/40
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/41
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/42
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/43
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/44
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/45
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/46
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/47
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/48
 port link-type hybrid
 undo port hybrid vlan 1
 port hybrid vlan {{vlan}} untagged
 port hybrid pvid vlan {{vlan}}
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
#
interface GigabitEthernet1/0/51
#
interface GigabitEthernet1/0/52
#
interface Smartrate-Ethernet1/0/49
 description {{uplink_device1}}-{{uplink_port1}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 speed 2500 
 stp loop-protection
 dldp enable   
 arp detection trust
 dhcp snooping trust
#
interface Smartrate-Ethernet1/0/50
 description {{uplink_device2}}-{{uplink_port2}}
 port link-type trunk
 undo port trunk permit vlan 1
 port trunk permit vlan 2 to 4094
 speed 2500 
 stp loop-protection
 dldp enable
 arp detection trust
 dhcp snooping trust
#
 scheduler logfile size 16
#
line class aux
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
line vty 0 15
 authentication-mode scheme
 user-role network-admin
 user-role network-operator
 command authorization
 command accounting
#
line vty 16 63
 user-role network-operator
#
 ip route-static 0.0.0.0 0 {{default_gateway}}
#
 info-center logbuffer size 1024
 info-center loghost source Vlan-interface10
 info-center loghost 10.34.27.26 facility local2
 info-center loghost 10.99.130.23
 info-center loghost 10.99.204.32
 info-center loghost 10.99.204.82
#              
 snmp-agent
 snmp-agent community read simple {{snmp_password}} acl 2010
 snmp-agent sys-info version v2c v3 
#
 ssh server enable
 ssh server acl 2000
#
 arp detection validate src-mac
 arp detection log enable
#
 ntp-service enable
 ntp-service unicast-server 10.28.0.20
 ntp-service unicast-server 10.14.198.20
#
acl number 2000 name CL
 rule 0 permit source 10.12.220.0 0.0.0.255
 rule 5 permit source 10.123.127.0 0.0.0.255
 rule 10 permit source 10.14.90.0 0.0.0.255
 rule 15 permit source 10.14.67.0 0.0.0.255
 rule 20 permit source 10.14.34.0 0.0.0.255
 rule 25 permit source 10.14.70.0 0.0.0.255
 rule 30 permit source 10.14.64.0 0.0.0.255
 rule 35 permit source 10.80.15.192 0.0.0.63
 rule 40 permit source 10.76.83.0 0.0.0.255
 rule 45 permit source 10.76.1.0 0.0.0.15
 rule 50 permit source 10.6.0.0 0.0.0.15
 rule 55 permit source 10.6.3.0 0.0.0.3
 rule 65 permit source 10.99.130.0 0.0.0.255
 rule 70 permit source 10.99.204.0 0.0.0.255
 rule 75 permit source 10.39.1.0 0.0.0.255
 rule 80 permit source 10.39.0.0 0.0.0.255
 rule 85 permit source 10.99.196.224 0.0.0.31
 {{local_manage_network}}
#
acl basic 2010
 rule 0 permit source 10.14.0.0 0.0.0.255
 rule 5 permit source 10.14.34.0 0.0.0.255
 rule 10 permit source 10.14.67.0 0.0.0.255
 rule 15 permit source 10.14.203.0 0.0.0.255
 rule 20 permit source 10.34.27.0 0.0.0.255
 rule 25 permit source 10.99.130.0 0.0.0.255
 rule 30 permit source 10.99.204.0 0.0.0.255
#
hwtacacs scheme tencent_scheme
 primary authentication 10.42.3.75
 primary authorization 10.42.3.75
 primary accounting 10.42.3.75
 secondary authentication 10.14.160.75
 secondary authorization 10.14.160.75
 secondary accounting 10.14.160.75
 key authentication simple {{tacacs_password}}
 key authorization simple {{tacacs_password}}
 key accounting simple {{tacacs_password}}
 user-name-format without-domain
 nas-ip {{mgt_ip}}
#
radius scheme system
 user-name-format without-domain
#
radius scheme tencent
 primary authentication 10.99.220.200 28882
 secondary authentication 10.99.145.4 28882
 key authentication simple {{radius_password}}
 user-name-format without-domain
 attribute 31 mac-format section six separator - lowercase 
#
domain system
#
domain tencent 
 authentication lan-access radius-scheme tencent
 authorization lan-access radius-scheme tencent
 accounting lan-access none
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
 password simple {{local_password}}
 service-type telnet ssh terminal
 authorization-attribute user-role network-admin
 authorization-attribute user-role network-operator
#
return
''')