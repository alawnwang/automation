import coa_info
import doa_info
import access_info
import ip_assign



def connection_relation(network,project):
    connection_list = []
    connection_dict = {'A_device':[],'A_port':[],'A_ip':[],'Z_device':[],'Z_port':[],'Z_ip':[]}

#核心链接关系
    connection_dict['A_device'].append(coa_info.get_coa_info(project)['MCOA'])
    connection_dict['A_device'].append(coa_info.get_coa_info(project)['MCOA'])
    connection_dict['A_port'].append(coa_info.get_coa_info(project)['port_assign']['interconnect'][0])
    connection_dict['A_port'].append(coa_info.get_coa_info(project)['port_assign']['interconnect'][1])
    connection_dict['A_ip'].append('Trunk')
    connection_dict['A_ip'].append('Trunk')
    connection_dict['Z_device'].append(coa_info.get_coa_info(project)['SCOA'])
    connection_dict['Z_device'].append(coa_info.get_coa_info(project)['SCOA'])
    connection_dict['Z_port'].append(coa_info.get_coa_info(project)['port_assign']['interconnect'][0])
    connection_dict['Z_port'].append(coa_info.get_coa_info(project)['port_assign']['interconnect'][1])
    connection_dict['Z_ip'].append('Trunk')
    connection_dict['Z_ip'].append('Trunk')

    func = ip_assign.network_class(network,project)
    connect_ip = func['connection_ip']
    for coa,doa in zip(coa_info.get_coa_info(project)['port_assign']['downlink'],doa_info.get_doa_info(project)):
        d_a_z_ip = connect_ip.__next__()[0]
        connection_dict['A_device'].append(coa_info.get_coa_info(project)['MCOA'])
        connection_dict['A_port'].append(coa)
        connection_dict['A_ip'].append(d_a_z_ip[1])
        connection_dict['Z_device'].append(doa['DDOA']['name'])
        connection_dict['Z_port'].append(doa['DDOA']['port_assign']['uplink'][0])
        connection_dict['Z_ip'].append(d_a_z_ip[2])
        e_a_z_ip = connect_ip.__next__()[0]
        connection_dict['A_device'].append(coa_info.get_coa_info(project)['SCOA'])
        connection_dict['A_port'].append(coa)
        connection_dict['A_ip'].append(e_a_z_ip[1])
        connection_dict['Z_device'].append(doa['EDOA']['name'])
        connection_dict['Z_port'].append(doa['EDOA']['port_assign']['uplink'][0])
        connection_dict['Z_ip'].append(e_a_z_ip[2])
        connection_dict['A_device'].append(doa['DDOA']['name'])
        connection_dict['A_port'].append(doa['DDOA']['port_assign']['interconnect'][0])
        connection_dict['A_ip'].append('Trunk')
        connection_dict['Z_device'].append(doa['EDOA']['name'])
        connection_dict['Z_port'].append(doa['EDOA']['port_assign']['interconnect'][0])
        connection_dict['Z_ip'].append('Trunk')
        connection_dict['A_device'].append(doa['DDOA']['name'])
        connection_dict['A_port'].append(doa['DDOA']['port_assign']['interconnect'][1])
        connection_dict['A_ip'].append('Trunk')
        connection_dict['Z_device'].append(doa['EDOA']['name'])
        connection_dict['Z_port'].append(doa['EDOA']['port_assign']['interconnect'][1])
        connection_dict['Z_ip'].append('Trunk')

#接入到汇聚互联/管理IP
    for doa,xoa in zip(doa_info.get_doa_info(project), access_info.get_access_info(project)):
        # mgt_sheet.append([doa['DDOA']['name'],doa['DDOA']['mgtip'],doa['DDOA']['netmask']])
        # mgt_sheet.append([doa['EDOA']['name'],doa['EDOA']['mgtip'],doa['EDOA']['netmask']])
        for dname in xoa['DXOA']:
            # mgt_sheet.append([dname['name'], dname['ip'], dname['netmask']])
            connection_dict['A_device'].append(doa['DDOA']['name'])
            connection_dict['A_port'].append((doa['DDOA']['port_assign']['ddownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(dname['name'])
            connection_dict['Z_port'].append(dname['port_assign'][0])
            connection_dict['Z_ip'].append('Trunk')
            connection_dict['A_device'].append(doa['EDOA']['name'])
            connection_dict['A_port'].append((doa['EDOA']['port_assign']['ddownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(dname['name'])
            connection_dict['Z_port'].append(dname['port_assign'][1])
            connection_dict['Z_ip'].append('Trunk')
        for ename in xoa['EXOA']:
            # mgt_sheet.append([ename['name'], ename['ip'], ename['netmask']])
            connection_dict['A_device'].append(doa['DDOA']['name'])
            connection_dict['A_port'].append((doa['DDOA']['port_assign']['edownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(ename['name'])
            connection_dict['Z_port'].append(ename['port_assign'][0])
            connection_dict['Z_ip'].append('Trunk')
            connection_dict['A_device'].append(doa['EDOA']['name'])
            connection_dict['A_port'].append((doa['EDOA']['port_assign']['edownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(ename['name'])
            connection_dict['Z_port'].append(ename['port_assign'][1])
            connection_dict['Z_ip'].append('Trunk')
        for vname in xoa['VEVP']:
            # mgt_sheet.append([vname['name'], vname['ip'], vname['netmask']])
            connection_dict['A_device'].append(doa['DDOA']['name'])
            connection_dict['A_port'].append((doa['DDOA']['port_assign']['vdownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(vname['name'])
            connection_dict['Z_port'].append(vname['port_assign'][0])
            connection_dict['Z_ip'].append('Trunk')
            connection_dict['A_device'].append(doa['EDOA']['name'])
            connection_dict['A_port'].append((doa['EDOA']['port_assign']['vdownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(vname['name'])
            connection_dict['Z_port'].append(vname['port_assign'][1])
            connection_dict['Z_ip'].append('Trunk')
        for wname in xoa['VEWL']:
            # mgt_sheet.append([wname['name'], wname['ip'], wname['netmask']])
            connection_dict['A_device'].append(doa['DDOA']['name'])
            connection_dict['A_port'].append((doa['DDOA']['port_assign']['wdownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(wname['name'])
            connection_dict['Z_port'].append(wname['port_assign'][0])
            connection_dict['Z_ip'].append('Trunk')
            connection_dict['A_device'].append(doa['EDOA']['name'])
            connection_dict['A_port'].append((doa['EDOA']['port_assign']['wdownlink']).pop(0))
            connection_dict['A_ip'].append('Trunk')
            connection_dict['Z_device'].append(wname['name'])
            connection_dict['Z_port'].append(wname['port_assign'][1])
            connection_dict['Z_ip'].append('Trunk')

    return connection_dict