import coa_info
import config_template
import doa_info
import xoa_info
import jinja2
import openpyxl

planning_workbook = openpyxl.Workbook()
mgt_sheet  = planning_workbook.create_sheet('mgt_ip')
mgt_sheet.append(['hostname','mgtip','netmask'])
connect_sheet = planning_workbook.create_sheet('connect_sheet')
connect_sheet.append(['主端设备','端口','对端设备','端口'])

project = input('项目名称: ')
# print(coa_info.get_coa_info(project))



for doa,xoa in zip(doa_info.get_doa_info(project),xoa_info.generation_access_info(project)):
    mgt_sheet.append([doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask']])
    mgt_sheet.append([doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask']])
    for dname in xoa['DXOA']:
        mgt_sheet.append([dname['name'],dname['ip'],dname['netmask']])
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


planning_workbook.save('/Users/alawn/Desktop/合肥中安一期.xlsx')




