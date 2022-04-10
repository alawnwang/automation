import ipaddress
import coa_info
import config_template
import doa_info
import access_info
import jinja2
import openpyxl
import ip_planning
import pymysql
import type_dict
planning_workbook = openpyxl.Workbook()
mgt_sheet  = planning_workbook.create_sheet('mgt_ip')
mgt_sheet.append(['hostname','mgtip','netmask'])
connect_sheet = planning_workbook.create_sheet('connect_sheet')
connect_sheet.append(['主端设备','端口','对端设备','端口'])
ip_planning_sheet = planning_workbook.create_sheet('ip_planning')
ip_planning_sheet.append(['vlan','network','function','floor'])
project = input('项目名称: ')

# #IP规划
for n, m in zip(ip_planning.mgt_num(project),ip_planning.network_class(project)['public']):
    n['network'] = str(m)
    ip_planning_sheet.append([n['vlan'],n['network'],n['fun'],n['bdr']])
network_list = ip_planning.network_class(project)['normal']
for o in ip_planning.network_assign.oa_network_assign(network_list,project):
    ip_planning_sheet.append([o['vlan'], str(o['network']), o['fun'], o['floor']])
for t in ip_planning.network_assign.ty_network_assign(network_list,project):
    ip_planning_sheet.append([t['vlan'], str(t['network']), t['fun'], t['floor']])
for v in ip_planning.network_assign.voip_network_assign(network_list,project):
    ip_planning_sheet.append([v['vlan'], str(v['network']), v['fun'], v['floor']])

#
# 核心链接关系
connect_sheet.append([coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0]])
connect_sheet.append([coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1]])
print(coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0])
print(coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1])

print(coa_info.get_coa_type(project))
print(coa_info.get_coa_info(project))
#汇聚到核心互联/汇聚互联
for coa,doa in zip(coa_info.get_coa_info(project)['port_assign']['downlink'],doa_info.get_doa_info(project)):
    connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['MCOA'],coa])
    connect_sheet.append([doa['EDOA']['name'],doa['EDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['SCOA'],coa])
    connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][0],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][0]])
    connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][1],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][1]])
#
# #接入到汇聚互联/管理IP
for doa,xoa in zip(doa_info.get_doa_info(project), access_info.get_access_info(project)):
    mgt_sheet.append([doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask']])
    mgt_sheet.append([doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask']])
    for dname in xoa['DXOA']:
        print(dname)
        mgt_sheet.append([dname['name'], dname['ip'], dname['netmask']])
        connect_sheet.append([dname['name'],dname['port_assign'][0],doa['DDOA']['name'],(doa['DDOA']['port_assign']['ddownlink']).pop(0)])
        connect_sheet.append([dname['name'], dname['port_assign'][1], doa['EDOA']['name'],
                              (doa['EDOA']['port_assign']['ddownlink']).pop(0)])
    for ename in xoa['EXOA']:
        mgt_sheet.append([ename['name'], ename['ip'], ename['netmask']])
        connect_sheet.append([ename['name'], ename['port_assign'][0], doa['DDOA']['name'],
              (doa['DDOA']['port_assign']['edownlink']).pop(0)])
        connect_sheet.append([ename['name'], ename['port_assign'][1], doa['EDOA']['name'],
              (doa['EDOA']['port_assign']['edownlink']).pop(0)])
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
#
planning_workbook.save('/Users/wanghaoyu/Desktop/%s.xlsx'%project)

#
# for network in ip_planning.num_of_network(project):
#     print(network)
#
# ip_planning.ip_assign(project)


