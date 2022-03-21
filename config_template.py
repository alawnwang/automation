from jinja2 import Template
def doa_uplink():
    DOA_UP_LINK_PORT = Template('''
    interface {{port_num}}
    description {{uplink_descr}}
    ip address {{ip_address}} {{netmask}}
    no ip redric
    no ip unreachable
    ''')
    return DOA_UP_LINK_PORT

def doa_downlink():
    DOA_DOWN_LINK_PROT=Template('''
    interface {{port_num}}
    description {{downlink_descr}}
    switchport mode trunk
    ''')
    return DOA_DOWN_LINK_PROT
