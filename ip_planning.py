from math import ceil

import ipaddress
import mysql_table_query

def num_of_network(project):
    num_network = []
    for network in mysql_table_query.endpoint(project):
        floor_network_oa = ceil((network['dpoint']+network['epoint'])/240)
        floor_network_ty = ceil(floor_network_oa*0.5)
        floor_network_voip = ceil(network['vpoint']/240)
        floor_network_num_dict = {'floor':network['floor'],'mgt':0.25,'ap_mgt':0.25,'video':0.25,'oa_device':0.25,'geli':0.25,'oa':floor_network_oa,'ty':floor_network_ty,'voip':floor_network_voip}
        num_network.append(floor_network_num_dict)
    return num_network

def ip_assign(project):
    b_class_network = '10.0.0.0/8'
    for network in num_of_network(project):
        mgt = sum(network['mgt'])
        print(mgt)


