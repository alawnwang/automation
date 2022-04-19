import coa_info
import doa_info
import access_info
import ip_assign

connection_list = []

def connection_relation(project):


#核心链接关系
    # master_connection= {[coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][0]])
    # connect_sheet.append([coa_info.get_coa_info(project)['MCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1],coa_info.get_coa_info(project)['SCOA'],coa_info.get_coa_info(project)['port_assign']['interconnect'][1]])
    connection_list.append({'A_device':coa_info.get_coa_info(project)['MCOA'],'A_port':coa_info.get_coa_info(project)['port_assign']['interconnect'][0],'A_ip':None,'Z_device':coa_info.get_coa_info(project)['SCOA'],'Z_port':coa_info.get_coa_info(project)['port_assign']['interconnect'][0],'Z_ip':None})
    connection_list.append({'A_device':coa_info.get_coa_info(project)['MCOA'],'A_port':coa_info.get_coa_info(project)['port_assign']['interconnect'][1],'A_ip':None,'Z_device':coa_info.get_coa_info(project)['SCOA'],'Z_port':coa_info.get_coa_info(project)['port_assign']['interconnect'][1],'Z_ip':None})

def core_doa_link(network,project):
#汇聚到核心互联/汇聚互联
    func = ip_assign.network_class(network,project)
    connect_ip = func['connection_ip']
    # print(connect_ip)
    for coa,doa in zip(coa_info.get_coa_info(project)['port_assign']['downlink'],doa_info.get_doa_info(project)):
        a_z_ip = connect_ip.__next__()
        # connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['MCOA'],coa])
        # connect_sheet.append([doa['EDOA']['name'],doa['EDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['SCOA'],coa])
        # connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][0],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][0]])
        # connect_sheet.append([doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][1],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][1]])
        doa_up_connection_relation = {'A_device':doa['DDOA']['name'], 'A_port':doa['DDOA']['port_assign']['uplink'][0], 'A_ip':a_z_ip[1],'Z_device':coa_info.get_coa_info(project)['MCOA'], 'Z_port':coa, 'Z_ip':a_z_ip[2]}
        doa_inter_connection_relation = {'A_device':doa['DDOA']['name'], 'A_port':doa['DDOA']['port_assign']['uplink'][0], 'A_ip':None, 'Z_device':coa_info.get_coa_info(project)['MCOA'], 'Z_port':coa, 'Z_ip':None}
        connection_list.append(doa_up_connection_relation)
        connection_list.append(doa_inter_connection_relation)
        # print(doa['DDOA']['name'],doa['DDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['MCOA'],coa)
        # print(doa['EDOA']['name'],doa['EDOA']['port_assign']['uplink'][0],coa_info.get_coa_info(project)['SCOA'],coa)
        # print(doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][0],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][0])
        # print(doa['DDOA']['name'],doa['DDOA']['port_assign']['interconnect'][1],doa['EDOA']['name'],doa['EDOA']['port_assign']['interconnect'][1])

# def doa_access_link(project):
#接入到汇聚互联/管理IP
    for doa,xoa in zip(doa_info.get_doa_info(project), access_info.get_access_info(project)):
        # mgt_sheet.append([doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask']])
        # mgt_sheet.append([doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask']])
        print(doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask'])
        print(doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask'])
        for dname in xoa['DXOA']:
            # print(dname)
            # mgt_sheet.append([dname['name'], dname['ip'], dname['netmask']])
            # connect_sheet.append([dname['name'],dname['port_assign'][0],doa['DDOA']['name'],(doa['DDOA']['port_assign']['ddownlink']).pop(0)])
            # connect_sheet.append([dname['name'], dname['port_assign'][1], doa['EDOA']['name'],
            #                       (doa['EDOA']['port_assign']['ddownlink']).pop(0)])
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