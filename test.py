# import ipaddress
# iplist = [ipaddress.IPv4Network('30.22.0.0/24'),ipaddress.IPv4Network('30.22.1.0/24'),ipaddress.IPv4Network('30.22.2.0/24')]
# print(list(ipaddress.collapse_addresses(iplist)))
project = '深圳光启未来'
import mysql_table_query
connect = mysql_table_query.connection(project)
print(type(connect))
for i in connect:
    print(i)
