import mysql_table_query


class generation_network:
    def __init__(self,vlan,description,hsrpip,masterip,backupip,netmask,acl,function,floor):
        self.floor = floor
        self.vlan = vlan
        self.description = description
        self.hsrpip = hsrpip
        self.masterip = masterip
        self.backupip = backupip
        self.netmask = netmask
        self.acl = acl
        self.function = function

    def query_ip_planning(self,project):
        for n in mysql_table_query.ip_planning(project):
            print(n)
