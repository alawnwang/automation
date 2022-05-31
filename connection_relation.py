import coa_info
import doa_info
import cwl_info
import access_info
import ccs_info
import ccs_fw
import xl_info
import ip_assign
#
project = input('项目名称: ')
#
network = input('IP地址：')


def connection_relation(network,project):
    coa_info_summary = coa_info.get_coa_info(network,project)
    cwl_info_summary = cwl_info.get_cwl_info(network,project)
    doa_info_summary = doa_info.get_doa_info(project)
    access_info_summary = access_info.get_access_info(project)
    ccs_info_summary = ccs_info.get_ccs_info(network,project)
    ccs_fw_summary = ccs_fw.get_ccs_fw_info(network,project)

    connection_dict ={'mgtip':{'project':[],'floor':[],'bdr':[],'device_name':[],'mgtip':[],'mgtmask':[],'gateway':[]},'connect':{'project':[],'A_floor':[],'A_bdr':[],'A_device':[],'A_port':[],'A_ip':[],'Z_floor':[],'Z_bdr':[],'Z_device':[],'Z_port':[],'Z_ip':[]}}
#
#核心链接关系

    # 核心互联-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['interconnect'][0])
    connection_dict['connect']['A_ip'].append('Trunk')
    connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['Z_port'].append(coa_info_summary['port_assign']['interconnect'][0])
    connection_dict['connect']['Z_ip'].append('Trunk')
    # 核心互联-2
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['A_ip'].append('Trunk')
    connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['Z_port'].append(coa_info_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['Z_ip'].append('Trunk')
    # 核心互联-聚合口
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['A_ip'].append('Bridge-Aggregation1')
    connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['Z_port'].append(coa_info_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation1')
    # 核心area0
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append('500')
    connection_dict['connect']['A_ip'].append(coa_info_summary['MMGTIP']['area0_ip'])
    connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['Z_port'].append('500')
    connection_dict['connect']['Z_ip'].append(coa_info_summary['SMGTIP']['area0_ip'])
    # 核心localarea
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append('501')
    connection_dict['connect']['A_ip'].append(coa_info_summary['MMGTIP']['localarea'])
    connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['Z_port'].append('501')
    connection_dict['connect']['Z_ip'].append(coa_info_summary['SMGTIP']['localarea'])
    # 无线核心互联-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['A_port'].append(cwl_info_summary['port_assign']['interconnect'][0])
    connection_dict['connect']['A_ip'].append('Trunk')
    connection_dict['connect']['Z_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['SCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['port_assign']['interconnect'][0])
    connection_dict['connect']['Z_ip'].append('Trunk')
    # 无线核心互联-2
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['A_port'].append(cwl_info_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['A_ip'].append('Trunk')
    connection_dict['connect']['Z_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['Z_ip'].append('Trunk')
    # 无线核心互联-聚合口
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['A_port'].append(cwl_info_summary['MMGTIP']['ip'])
    connection_dict['connect']['A_ip'].append('Trunk')
    connection_dict['connect']['Z_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['SCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['SMGTIP']['ip'])
    connection_dict['connect']['Z_ip'].append('Trunk')
    # 大厦核心-无线核心-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['cwl'][0])
    connection_dict['connect']['A_ip'].append('Bridge-Aggregation6')
    connection_dict['connect']['Z_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['port_assign']['uplink'][0])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation6')
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['cwl'][1])
    connection_dict['connect']['A_ip'].append('Bridge-Aggregation6')
    connection_dict['connect']['Z_floor'].append(str(cwl_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['port_assign']['uplink'][1])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation6')
    # 大厦核心-无线核心-2
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['cwl'][0])
    connection_dict['connect']['A_ip'].append('Bridge-Aggregation6')
    connection_dict['connect']['Z_floor'].append(cwl_info_summary['floor'])
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['SCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['port_assign']['uplink'][0])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation6')
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['cwl'][1])
    connection_dict['connect']['A_ip'].append('Bridge-Aggregation6')
    connection_dict['connect']['Z_floor'].append(cwl_info_summary['floor'])
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['SCW'])
    connection_dict['connect']['Z_port'].append(cwl_info_summary['port_assign']['uplink'][1])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation6')
    #大厦核心-无线核心-聚合口-ip-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append('Bridge-Aggregation6')
    connection_dict['connect']['A_ip'].append(coa_info_summary['MMGTIP']['cwl'])
    connection_dict['connect']['Z_floor'].append(cwl_info_summary['floor'])
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['MCW'])
    connection_dict['connect']['Z_port'].append('Bridge-Aggregation6')
    connection_dict['connect']['Z_ip'].append(cwl_info_summary['MMGTIP']['uplink'])
    #大厦核心-无线核心-聚合口-ip-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['A_port'].append('Bridge-Aggregation6')
    connection_dict['connect']['A_ip'].append(coa_info_summary['SMGTIP']['cwl'])
    connection_dict['connect']['Z_floor'].append(cwl_info_summary['floor'])
    connection_dict['connect']['Z_bdr'].append(cwl_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(cwl_info_summary['SCW'])
    connection_dict['connect']['Z_port'].append('Bridge-Aggregation6')
    connection_dict['connect']['Z_ip'].append(cwl_info_summary['SMGTIP']['uplink'])
    # 大厦核心-控制网防火墙-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['ccs'][0])
    connection_dict['connect']['A_ip'].append('vlan 550'+'/'+str(coa_info_summary['MMGTIP']['ccsip'])+'/'+str(coa_info_summary['MMGTIP']['vlan_gateway']))
    connection_dict['connect']['Z_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['Z_device'].append(ccs_fw_summary['MCW'])
    connection_dict['connect']['Z_port'].append(ccs_fw_summary['port_assign']['uplink'])
    connection_dict['connect']['Z_ip'].append(str(ccs_fw_summary['up_phycial'])+str(ccs_fw_summary['MMGTIP']['up_link_manage_ip']))
    # 大厦核心-控制网防火墙-2
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    connection_dict['connect']['A_device'].append(coa_info_summary['SCOA'])
    connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['ccs'][0])
    connection_dict['connect']['A_ip'].append(str(coa_info_summary['SMGTIP']['ccsip']) + '/' + str(
        coa_info_summary['MMGTIP']['vlan_gateway']))
    connection_dict['connect']['Z_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['Z_device'].append(ccs_fw_summary['SCW'])
    connection_dict['connect']['Z_port'].append(ccs_fw_summary['port_assign']['uplink'])
    connection_dict['connect']['Z_ip'].append(str(ccs_fw_summary['up_phycial'])+str(ccs_fw_summary['SMGTIP']['up_link_manage_ip']))
    # 防火墙互联-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['A_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['A_device'].append(ccs_fw_summary['MCW'])
    connection_dict['connect']['A_port'].append(ccs_fw_summary['port_assign']['interconnect'][0])
    connection_dict['connect']['A_ip'].append('HA')
    connection_dict['connect']['Z_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['Z_device'].append(ccs_fw_summary['SCW'])
    connection_dict['connect']['Z_port'].append(ccs_fw_summary['port_assign']['interconnect'][0])
    connection_dict['connect']['Z_ip'].append('HA')
    # 防火墙互联-2
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['A_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['A_device'].append(ccs_fw_summary['MCW'])
    connection_dict['connect']['A_port'].append(ccs_fw_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['A_ip'].append('HA')
    connection_dict['connect']['Z_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['Z_device'].append(ccs_fw_summary['SCW'])
    connection_dict['connect']['Z_port'].append(ccs_fw_summary['port_assign']['interconnect'][1])
    connection_dict['connect']['Z_ip'].append('HA')
    # 防火墙-控制网核心-1
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['A_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['A_device'].append(ccs_fw_summary['MCW'])
    connection_dict['connect']['A_port'].append(ccs_fw_summary['port_assign']['downlink'])
    connection_dict['connect']['A_ip'].append(str(ccs_fw_summary['down_phycial'])+str(ccs_fw_summary['MMGTIP']['down_link_manage_ip']))
    connection_dict['connect']['Z_floor'].append(str(ccs_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(ccs_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(ccs_info_summary['MCCS'])
    connection_dict['connect']['Z_port'].append(ccs_info_summary['port_assign']['uplink'])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation6')
    # 防火墙-控制网核心-2
    connection_dict['connect']['project'].append(project)
    connection_dict['connect']['A_floor'].append(str(ccs_fw_summary['floor']))
    connection_dict['connect']['A_bdr'].append(ccs_fw_summary['bdr'])
    connection_dict['connect']['A_device'].append(ccs_fw_summary['SCW'])
    connection_dict['connect']['A_port'].append(ccs_fw_summary['port_assign']['downlink'])
    connection_dict['connect']['A_ip'].append(str(ccs_fw_summary['down_phycial'])+str(ccs_fw_summary['SMGTIP']['down_link_manage_ip']))
    connection_dict['connect']['Z_floor'].append(str(ccs_info_summary['floor']))
    connection_dict['connect']['Z_bdr'].append(ccs_info_summary['bdr'])
    connection_dict['connect']['Z_device'].append(ccs_info_summary['SCCS'])
    connection_dict['connect']['Z_port'].append(ccs_info_summary['port_assign']['uplink'])
    connection_dict['connect']['Z_ip'].append('Bridge-Aggregation6')
    # # 控制网核心互联-1
    # connection_dict['connect']['project'].append(project)
    # connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    # connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    # connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    # connection_dict['connect']['A_port'].append('Bridge-Aggregation6')
    # connection_dict['connect']['A_ip'].append(coa_info_summary['MMGTIP']['cwl'])
    # connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    # connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    # connection_dict['connect']['Z_device'].append(cwl_info_summary['MCW'])
    # connection_dict['connect']['Z_port'].append('Bridge-Aggregation6')
    # connection_dict['connect']['Z_ip'].append(cwl_info_summary['MMGTIP']['uplink'])
    # # 控制网核心互联-2
    # connection_dict['connect']['project'].append(project)
    # connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    # connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    # connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    # connection_dict['connect']['A_port'].append('Bridge-Aggregation6')
    # connection_dict['connect']['A_ip'].append(coa_info_summary['SMGTIP']['cwl'])
    # connection_dict['connect']['Z_floor'].append(str(coa_info_summary['floor']))
    # connection_dict['connect']['Z_bdr'].append(coa_info_summary['bdr'])
    # connection_dict['connect']['Z_device'].append(cwl_info_summary['MCW'])
    # connection_dict['connect']['Z_port'].append('Bridge-Aggregation6')
    # connection_dict['connect']['Z_ip'].append(cwl_info_summary['SMGTIP']['uplink'])
    # # 控制网核心互联-聚合口
    # connection_dict['connect']['project'].append(project)
    # connection_dict['connect']['A_floor'].append(str(coa_info_summary['floor']))
    # connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    # connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    # connection_dict['connect']['A_port'].append(coa_info_summary['port_assign']['ccs'])
    # connection_dict['connect']['A_ip'].append(coa_info_summary['MMGTIP']['ccsip'])
    # connection_dict['connect']['Z_floor'].append(str(ccs_fw['floor']))
    # connection_dict['connect']['Z_bdr'].append(ccs_fw['bdr'])
    # connection_dict['connect']['Z_device'].append(ccs_fw['MCW'])
    # connection_dict['connect']['Z_port'].append('Bridge-Aggregation6')
    # connection_dict['connect']['Z_ip'].append(cwl_info_summary['SMGTIP']['uplink'])
    # func = ip_assign.network_class(network,project)
    #
    # connect_ip = (i for i in func['connection_ip'])


    # for coa,doa in zip(coa_info_summary['port_assign']['downlink'],doa_info_summary):
    #     try:
    #         d_a_z_ip = connect_ip.__next__()[0]
    #         connection_dict['connect']['project'].append(project)
    #         connection_dict['connect']['A_floor'].append(coa_info_summary['floor'])
    #         connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    #         connection_dict['connect']['A_device'].append(coa_info_summary['MCOA'])
    #         connection_dict['connect']['A_port'].append(coa)
    #         connection_dict['connect']['A_ip'].append(str(d_a_z_ip[1])+'/'+str(d_a_z_ip.prefixlen))
    #         connection_dict['connect']['Z_floor'].append(doa['DDOA']['floor'])
    #         connection_dict['connect']['Z_bdr'].append(doa['DDOA']['bdr'])
    #         connection_dict['connect']['Z_device'].append(doa['DDOA']['name'])
    #         connection_dict['connect']['Z_port'].append(doa['DDOA']['port_assign']['uplink'][0])
    #         connection_dict['connect']['Z_ip'].append(str(d_a_z_ip[2])+'/'+str(d_a_z_ip.prefixlen))
    #
    #         e_a_z_ip = connect_ip.__next__()[0]
    #         connection_dict['connect']['project'].append(project)
    #         connection_dict['connect']['A_floor'].append(coa_info_summary['floor'])
    #         connection_dict['connect']['A_bdr'].append(coa_info_summary['bdr'])
    #         connection_dict['connect']['A_device'].append(coa_info_summary['SCOA'])
    #         connection_dict['connect']['A_port'].append(coa)
    #         connection_dict['connect']['A_ip'].append(str(e_a_z_ip[1])+'/'+str(e_a_z_ip.prefixlen))
    #         connection_dict['connect']['Z_floor'].append(doa['EDOA']['floor'])
    #         connection_dict['connect']['Z_bdr'].append(doa['EDOA']['bdr'])
    #         connection_dict['connect']['Z_device'].append(doa['EDOA']['name'])
    #         connection_dict['connect']['Z_port'].append(doa['EDOA']['port_assign']['uplink'][0])
    #         connection_dict['connect']['Z_ip'].append(str(e_a_z_ip[2])+'/'+str(e_a_z_ip.prefixlen))
    #     except StopIteration:pass
    #
    # for coa, doa in zip(coa_info_summary['port_assign']['downlink'], doa_info_summary):
    #     connection_dict['connect']['project'].append(project)
    #     connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #     connection_dict['connect']['A_bdr'].append(doa['DDOA']['bdr'])
    #     connection_dict['connect']['A_device'].append(doa['DDOA']['name'])
    #     connection_dict['connect']['A_port'].append(doa['DDOA']['port_assign']['interconnect'][0])
    #     connection_dict['connect']['A_ip'].append('Trunk')
    #     connection_dict['connect']['Z_floor'].append(doa['EDOA']['floor'])
    #     connection_dict['connect']['Z_bdr'].append(doa['EDOA']['bdr'])
    #     connection_dict['connect']['Z_device'].append(doa['EDOA']['name'])
    #     connection_dict['connect']['Z_port'].append(doa['EDOA']['port_assign']['interconnect'][0])
    #     connection_dict['connect']['Z_ip'].append('Trunk')
    #     connection_dict['connect']['project'].append(project)
    #     connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #     connection_dict['connect']['A_bdr'].append(doa['DDOA']['bdr'])
    #     connection_dict['connect']['A_device'].append(doa['DDOA']['name'])
    #     connection_dict['connect']['A_port'].append(doa['DDOA']['port_assign']['interconnect'][1])
    #     connection_dict['connect']['A_ip'].append('Trunk')
    #     connection_dict['connect']['Z_floor'].append(doa['EDOA']['floor'])
    #     connection_dict['connect']['Z_bdr'].append(doa['EDOA']['bdr'])
    #     connection_dict['connect']['Z_device'].append(doa['EDOA']['name'])
    #     connection_dict['connect']['Z_port'].append(doa['EDOA']['port_assign']['interconnect'][1])
    #     connection_dict['connect']['Z_ip'].append('Trunk')

#接入到汇聚互联/管理IP
    # for doa in doa_info_summary:
    #
    #     connection_dict['mgtip']['project'].append(project)
    #     connection_dict['mgtip']['floor'].append(doa['DDOA']['floor'])
    #     connection_dict['mgtip']['bdr'].append(doa['DDOA']['bdr'])
    #     connection_dict['mgtip']['device_name'].append(doa['DDOA']['name'])
    #     connection_dict['mgtip']['mgtip'].append(doa['DDOA']['mgtip'])
    #     connection_dict['mgtip']['mgtmask'].append(doa['DDOA']['netmask'])
    #     connection_dict['mgtip']['gateway'].append(None)
    #     connection_dict['mgtip']['project'].append(project)
    #     connection_dict['mgtip']['floor'].append(doa['EDOA']['floor'])
    #     connection_dict['mgtip']['bdr'].append(doa['EDOA']['bdr'])
    #     connection_dict['mgtip']['device_name'].append(doa['EDOA']['name'])
    #     connection_dict['mgtip']['mgtip'].append(doa['EDOA']['mgtip'])
    #     connection_dict['mgtip']['mgtmask'].append(doa['EDOA']['netmask'])
    #     connection_dict['mgtip']['gateway'].append(None)
    #     for xoa in access_info_summary:
    #         if str(doa['DDOA']['floor'])+str(doa['DDOA']['bdr']) == str(xoa['floor'])+str(xoa['bdr']):
    #             for dx in xoa['DXOA']:
    #
    #                 connection_dict['mgtip']['project'].append(project)
    #                 connection_dict['mgtip']['floor'].append(dx['floor'])
    #                 connection_dict['mgtip']['bdr'].append(dx['bdr'])
    #                 connection_dict['mgtip']['device_name'].append(dx['name'])
    #                 connection_dict['mgtip']['mgtip'].append(dx['ip'])
    #                 connection_dict['mgtip']['mgtmask'].append(dx['netmask'])
    #                 connection_dict['mgtip']['gateway'].append(dx['gateway'])
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['DDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['DDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['DDOA']['port_assign']['ddownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(dx['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(dx['bdr'])
    #                 connection_dict['connect']['Z_device'].append(dx['name'])
    #                 connection_dict['connect']['Z_port'].append(dx['port_assign'][0])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['EDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['EDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['EDOA']['port_assign']['ddownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(dx['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(dx['bdr'])
    #                 connection_dict['connect']['Z_device'].append(dx['name'])
    #                 connection_dict['connect']['Z_port'].append(dx['port_assign'][1])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #             for ex in xoa['EXOA']:
    #                 connection_dict['mgtip']['project'].append(project)
    #                 connection_dict['mgtip']['floor'].append(ex['floor'])
    #                 connection_dict['mgtip']['bdr'].append(ex['bdr'])
    #                 connection_dict['mgtip']['device_name'].append(ex['name'])
    #                 connection_dict['mgtip']['mgtip'].append(ex['ip'])
    #                 connection_dict['mgtip']['mgtmask'].append(ex['netmask'])
    #                 connection_dict['mgtip']['gateway'].append(ex['gateway'])
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['DDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['DDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['DDOA']['port_assign']['edownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(ex['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(ex['bdr'])
    #                 connection_dict['connect']['Z_device'].append(ex['name'])
    #                 connection_dict['connect']['Z_port'].append(ex['port_assign'][0])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['EDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['EDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['EDOA']['port_assign']['edownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(ex['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(ex['bdr'])
    #                 connection_dict['connect']['Z_device'].append(ex['name'])
    #                 connection_dict['connect']['Z_port'].append(ex['port_assign'][1])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #             for ve in xoa['VEVP']:
    #                 connection_dict['mgtip']['project'].append(project)
    #                 connection_dict['mgtip']['floor'].append(ve['floor'])
    #                 connection_dict['mgtip']['bdr'].append(ve['bdr'])
    #                 connection_dict['mgtip']['device_name'].append(ve['name'])
    #                 connection_dict['mgtip']['mgtip'].append(ve['ip'])
    #                 connection_dict['mgtip']['mgtmask'].append(ve['netmask'])
    #                 connection_dict['mgtip']['gateway'].append(ve['gateway'])
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['DDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['DDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['DDOA']['port_assign']['vdownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(ve['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(ve['bdr'])
    #                 connection_dict['connect']['Z_device'].append(ve['name'])
    #                 connection_dict['connect']['Z_port'].append(ve['port_assign'][0])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['EDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['EDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['EDOA']['port_assign']['vdownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(ve['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(ve['bdr'])
    #                 connection_dict['connect']['Z_device'].append(ve['name'])
    #                 connection_dict['connect']['Z_port'].append(ve['port_assign'][1])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #             for ew in xoa['VEWL']:
    #                 connection_dict['mgtip']['project'].append(project)
    #                 connection_dict['mgtip']['floor'].append(ew['floor'])
    #                 connection_dict['mgtip']['bdr'].append(ew['bdr'])
    #                 connection_dict['mgtip']['device_name'].append(ew['name'])
    #                 connection_dict['mgtip']['mgtip'].append(ew['ip'])
    #                 connection_dict['mgtip']['mgtmask'].append(ew['netmask'])
    #                 connection_dict['mgtip']['gateway'].append(ew['gateway'])
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['DDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['DDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['DDOA']['port_assign']['wdownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(ew['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(ew['bdr'])
    #                 connection_dict['connect']['Z_device'].append(ew['name'])
    #                 connection_dict['connect']['Z_port'].append(ew['port_assign'][0])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    #                 connection_dict['connect']['project'].append(project)
    #                 connection_dict['connect']['A_floor'].append(doa['DDOA']['floor'])
    #                 connection_dict['connect']['A_bdr'].append(doa['EDOA']['bdr'])
    #                 connection_dict['connect']['A_device'].append(doa['EDOA']['name'])
    #                 connection_dict['connect']['A_port'].append(doa['EDOA']['port_assign']['wdownlink'].pop(0))
    #                 connection_dict['connect']['A_ip'].append('Trunk')
    #                 connection_dict['connect']['Z_floor'].append(ew['floor'])
    #                 connection_dict['connect']['Z_bdr'].append(ew['bdr'])
    #                 connection_dict['connect']['Z_device'].append(ew['name'])
    #                 connection_dict['connect']['Z_port'].append(ew['port_assign'][1])
    #                 connection_dict['connect']['Z_ip'].append('Trunk')
    #
    # return connection_dict



# n = (connection_relation(network,project)['mgtip'])
# for i in n:
#     print(i)
    for p,af,ab,ad,ap,ai,zf,zb,zd,zp,zi in zip(connection_dict['connect']['project'],connection_dict['connect']['A_floor'],connection_dict['connect']['A_bdr'],connection_dict['connect']['A_device'],connection_dict['connect']['A_port'],connection_dict['connect']['A_ip'],connection_dict['connect']['Z_floor'],connection_dict['connect']['Z_bdr'],connection_dict['connect']['Z_device'],connection_dict['connect']['Z_port'],connection_dict['connect']['Z_ip']):
        print(p,af,ab,ad,ap,ai,zf,zb,zd,zp,zi)
    #

    print(connection_dict['mgtip']['device_name'],connection_dict['mgtip']['mgtip'],connection_dict['mgtip']['mgtmask'],connection_dict['mgtip']['gateway'])
    for p,df,db,dd,di,dn,dg in zip(connection_dict['mgtip']['project'],connection_dict['mgtip']['floor'],connection_dict['mgtip']['bdr'],connection_dict['mgtip']['device_name'],connection_dict['mgtip']['mgtip'],connection_dict['mgtip']['mgtmask'],connection_dict['mgtip']['gateway']):
        print(p,df,db,dd,di,dn,dg)
    # print(len(connection_dict['connect']['project']),len(connection_dict['connect']['A_floor']),len(connection_dict['connect']['A_bdr']),len(connection_dict['connect']['A_device']),len(connection_dict['connect']['A_port']),len(connection_dict['connect']['A_ip']),len(connection_dict['connect']['Z_floor']),len(connection_dict['connect']['Z_bdr']),len(connection_dict['connect']['Z_device']),len(connection_dict['connect']['Z_port']),len(connection_dict['connect']['Z_ip']))
    print(len(connection_dict['mgtip']['project']),len(connection_dict['mgtip']['floor']),len(connection_dict['mgtip']['bdr']),len(connection_dict['mgtip']['device_name']),len(connection_dict['mgtip']['mgtip']),len(connection_dict['mgtip']['mgtmask']),len(connection_dict['mgtip']['gateway']))
connection_relation(network,project)