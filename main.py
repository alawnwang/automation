import test
import coa_info
import doa_info
import access_info
import openpyxl
import time
import ip_assign
import pandas as pd
import mysql_table_query

planning_workbook = openpyxl.Workbook()
mgt_sheet  = planning_workbook.create_sheet('mgt_ip')
mgt_sheet.append(['hostname','mgtip','netmask'])
connect_sheet = planning_workbook.create_sheet('connect_sheet')
connect_sheet.append(['主端设备','端口','对端设备','端口'])
ip_planning_sheet = planning_workbook.create_sheet('ip_planning')
ip_planning_sheet.append(['vlan','network','function','desctiption','floor','bdr'])

project = input('项目名称: ')

network = input('IP地址：')




# print(ip_assign.num_of_network(project))
# paramete = mysql_table_query.parameter(project)
#
# print((paramete['AP_dhcp']).split(';'))

def intser_sql():
    for net in ip_assign.generation_ip_planning(network,project):
        ip = pd.DataFrame.from_dict(net, orient='columns')
        ip.to_sql(con=mysql_table_query.link_db(), name='ip_planning', if_exists='append', index=False)
        ip.to_excel(planning_workbook,sheet_name='ip_planning',index=False)

def core_link():
#核心链接关系
    connect_sheet.append([coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0]])
    connect_sheet.append([coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1]])
    print(coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0])
    print(coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1])

def core_doa_link():
#汇聚到核心互联/汇聚互联
    for coa,doa in zip(coa_info.get_coa_info(project)['port_assign']['downlink'],doa_info.get_doa_info(project)):
        connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['MCOA'],coa])
        connect_sheet.append([doa['EDOA']['name'],doa['EDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['SCOA'],coa])
        connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][0],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][0]])
        connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][1],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][1]])
        print(doa['DDOA']['name'],doa['DDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['MCOA'],coa)
        print(doa['EDOA']['name'],doa['EDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['SCOA'],coa)
        print(doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][0],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][0])
        print(doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][1],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][1])

def doa_access_link():
#接入到汇聚互联/管理IP
    for doa,xoa in zip(doa_info.get_doa_info(project), access_info.get_access_info(project)):
        mgt_sheet.append([doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask']])
        mgt_sheet.append([doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask']])
        print(doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask'])
        print(doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask'])
        for dname in xoa['DXOA']:
            # print(dname)
            mgt_sheet.append([dname['name'], dname['ip'], dname['netmask']])
            connect_sheet.append([dname['name'],dname['port_assign'][0],doa['DDOA']['name'],(doa['DDOA']['port_assign']['ddownlink']).pop(0)])
            connect_sheet.append([dname['name'], dname['port_assign'][1], doa['EDOA']['name'],
                                  (doa['EDOA']['port_assign']['ddownlink']).pop(0)])
            print(dname['name'], dname['ip'], dname['netmask'])
            print(dname['name'],dname['port_assign'][0],doa['DDOA']['name'],(doa['DDOA']['port_assign']['ddownlink']).pop(0))
            print(dname['name'], dname['port_assign'][1], doa['EDOA']['name'],
                                  (doa['EDOA']['port_assign']['ddownlink']).pop(0))
        for ename in xoa['EXOA']:
            mgt_sheet.append([ename['name'], ename['ip'], ename['netmask']])
            connect_sheet.append([ename['name'], ename['port_assign'][0], doa['DDOA']['name'],
                  (doa['DDOA']['port_assign']['edownlink']).pop(0)])
            connect_sheet.append([ename['name'], ename['port_assign'][1], doa['EDOA']['name'],
                  (doa['EDOA']['port_assign']['edownlink']).pop(0)])
            print(ename['name'], ename['ip'], ename['netmask'])
            print(ename['name'], ename['port_assign'][0], doa['DDOA']['name'],
                  (doa['DDOA']['port_assign']['edownlink']).pop(0))
            print(ename['name'], ename['port_assign'][1], doa['EDOA']['name'],
                  (doa['EDOA']['port_assign']['edownlink']).pop(0))
        for vname in xoa['VEVP']:
            mgt_sheet.append([vname['name'], vname['ip'], vname['netmask']])
            connect_sheet.append([vname['name'], vname['port_assign'][0], doa['DDOA']['name'],
                  (doa['DDOA']['port_assign']['vdownlink']).pop(0)])
            connect_sheet.append([vname['name'], vname['port_assign'][1], doa['EDOA']['name'],
                  (doa['EDOA']['port_assign']['vdownlink']).pop(0)])
        for wname in xoa['VEWL']:
            mgt_sheet.append([wname['name'], wname['ip'], wname['netmask']])
            connect_sheet.append([wname['name'], wname['port_assign'][0], doa['DDOA']['name'],
                  (doa['DDOA']['port_assign']['wdownlink']).pop(0)])
            connect_sheet.append([wname['name'], wname['port_assign'][1], doa['EDOA']['name'],
                  (doa['EDOA']['port_assign']['wdownlink']).pop(0)])
        print(wname['name'], wname['ip'], wname['netmask'])
        print(wname['name'], wname['port_assign'][0], doa['DDOA']['name'],
              (doa['DDOA']['port_assign']['wdownlink']).pop(0))
        print(wname['name'], wname['port_assign'][1], doa['EDOA']['name'],
              (doa['EDOA']['port_assign']['wdownlink']).pop(0))






print('IP规划已生成完毕')

core_link()
core_doa_link()
doa_access_link()
print('建设规划已生成完毕')
planning_workbook.save(planning_workbook.save('/Users/alawn/Desktop/%s.xlsx'%project))



