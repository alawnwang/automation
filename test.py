# import mysql_table_query
#
#
# class generation_network:
#     def __init__(self,vlan,description,hsrpip,masterip,backupip,netmask,acl,function,floor):
#         self.floor = floor
#         self.vlan = vlan
#         self.description = description
#         self.hsrpip = hsrpip
#         self.masterip = masterip
#         self.backupip = backupip
#         self.netmask = netmask
#         self.acl = acl
#         self.function = function
#
#     def query_ip_planning(self,project):
#         for n in mysql_table_query.ip_planning(project):
#             print(n)


import config_template

print(config_template.h3c_port_config_template.vlan_config().render(vlan_num='10',vlan_des='name'))