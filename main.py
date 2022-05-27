import coa_info
import doa_info
import access_info
import openpyxl
import time
import ip_assign
import pandas as pd
import mysql_table_query
import connection_relation



project = input('项目名称: ')
#
network = input('IP地址：')



def ip_planning_intser_sql(network,project):
    for net in ip_assign.generation_ip_planning(network,project):
        ip = pd.DataFrame.from_dict(net, orient='columns')
        ip.to_sql(con=mysql_table_query.link_db(), name='ip_planning', if_exists='append', index=False)
ip_planning_intser_sql(network,project)
print('IP规划已生成完毕')

# def connection_intser_sql(network,project):
#     connect = connection_relation.connection_relation(network,project)['connect']
#     con = pd.DataFrame.from_dict(connect, orient='columns')
#     con.to_sql(con=mysql_table_query.link_db(), name='connection_relation', if_exists='append', index=False)
#     mgtip = connection_relation.connection_relation(network,project)['mgtip']
#     mgt = pd.DataFrame.from_dict(mgtip, orient='columns')
#     mgt.to_sql(con=mysql_table_query.link_db(), name='manage_ip_assignments', if_exists='append', index=False)
# connection_intser_sql(network,project)
# print('链接关系已生成完毕')


