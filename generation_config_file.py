import mysql_table_query
import config_template


def generation_lay3_vlan(project):
    network_info = mysql_table_query.ip_planning(project)
    device_info = mysql_table_query.deivce_ip(project)
    for dev in device_info:
        print(dev)
        # dev_bdr = str(dev['floor'])+str(dev['bdr'])
        # for net in network_info:
        #     print(net)
            # net_bdr = str(net['floor'])+str(net['bdr'])
            # if dev_bdr == net_bdr:
            #     print(dev['network'])

