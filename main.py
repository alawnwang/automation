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

def generation_ip_planning(network,project):
    ip_planning_list = []
    # #IP规划
    core_ipaddress = ip_assign.network_class(network,project)['mgt']
    core_ip_dict = {'network':[core_ipaddress],'status':None,'domain':None,'vlan':None,'func':'核心网段','description':'interconnection','project':project,'building_name':None,'floor':None,'bdr':None,'type_of_workplace':None}
    ip_planning_list.append(core_ip_dict)

    for n, m in zip(ip_assign.mgt_num(project),ip_assign.network_class(network,project)['public']):
        n['network'] = str(m)
        ip_planning_sheet.append([n['vlan'],n['network'],n['fun'],n['desc'],n['floor'],n['bdr']])
        public_ip = {'network':[n['network']],'status':None,'domain':None,'vlan':[n['vlan']],'func':[n['fun']],'description':[n['desc']],'project':project,'building_name':None,'floor':[n['floor']],'bdr':[n['bdr']],'type_of_workplace':None}
        ip_planning_list.append(public_ip)

    network_list = ip_assign.network_class(network,project)['normal']
    for o in ip_assign.network_assign.oa_network_assign(network_list,project):
        ip_planning_sheet.append([o['vlan'], str(o['network']), o['fun'],o['desc'],o['floor'],o['bdr']])
        oa_ip = {'network': [o['network']], 'status': None, 'domain': None, 'vlan': [o['vlan']], 'func': [o['fun']],
                     'description': [o['desc']], 'project': project, 'building_name': None, 'floor': [o['floor']],
                     'bdr': [o['bdr']], 'type_of_workplace': None}
        ip_planning_list.append(oa_ip)

    for t in ip_assign.network_assign.ty_network_assign(network_list,project):
        ip_planning_sheet.append([t['vlan'], str(t['network']), t['fun'], t['desc'],t['floor'],t['bdr']])
        ty_ip = {'network': [t['network']], 'status': None, 'domain': None, 'vlan': [t['vlan']], 'func': [t['fun']],
                     'description': [t['desc']], 'project': project, 'building_name': None, 'floor': [t['floor']],
                     'bdr': [t['bdr']], 'type_of_workplace': None}
        ip_planning_list.append(ty_ip)

    for v in ip_assign.network_assign.voip_network_assign(network_list,project):
        ip_planning_sheet.append([v['vlan'], str(v['network']), v['fun'], v['desc'],v['floor'],v['bdr']])
        voip_ip = {'network': [v['network']], 'status': None, 'domain': None, 'vlan': [v['vlan']], 'func': [v['fun']],
                     'description': [v['desc']], 'project': project, 'building_name': None, 'floor': [v['floor']],
                     'bdr': [v['bdr']], 'type_of_workplace': None}
        ip_planning_list.append(voip_ip)
    return ip_planning_list

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




#
for i in generation_ip_planning(network,project):
    ip = pd.DataFrame.from_dict(i,orient='columns')
    ip.to_sql(con=mysql_table_query.link_db(), name='ip_planning',if_exists='append', index=False)

print('IP规划已生成完毕')

core_link()
core_doa_link()
doa_access_link()
print('建设规划已生成完毕')
planning_workbook.save('/Users/alawn/Desktop/%s.xlsx'%project)



