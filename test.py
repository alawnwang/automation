# import pandas as pd
#
# list = [{'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-ft25cjfv', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名2', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-htc2rnzh', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-p6q98hl3', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.5'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:36Z', 'ExpiredTime': '2022-05-06T09:54:36Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['sg-fp0nuocq', 'sg-p98zzw10','33333'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '22399c02-5955-4125-8dde-7241928b4c77', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None},
#         {'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-n8ph9sdj', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名1', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-dszjcemn', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-blmv80pb', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.6'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:38Z', 'ExpiredTime': '2022-05-06T09:54:38Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['111111', 'sg-fp0nuocq'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '5db08c92-3e67-4b33-8564-d0806f258a6a', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None},
#         {'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-ft25cjfv', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名2', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-htc2rnzh', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-p6q98hl3', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.7'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:36Z', 'ExpiredTime': '2022-05-06T09:54:36Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['sg-p98zzw10','sg-fp0nuocq'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '22399c02-5955-4125-8dde-7241928b4c77', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None},
#         {'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-ft25cjfv', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名2', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-htc2rnzh', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-p6q98hl3', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.8'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:36Z', 'ExpiredTime': '2022-05-06T09:54:36Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['sg-fp0nuocq'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '22399c02-5955-4125-8dde-7241928b4c77', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None},
#         {'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-ft25cjfv', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名2', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-htc2rnzh', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-p6q98hl3', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.8'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:36Z', 'ExpiredTime': '2022-05-06T09:54:36Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['1111','2222'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '22399c02-5955-4125-8dde-7241928b4c77', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None},
#        {'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-ft25cjfv', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名2', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-htc2rnzh', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-p6q98hl3', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.8'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:36Z', 'ExpiredTime': '2022-05-06T09:54:36Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['sg-fp0nuocq','sg-p98zzw10'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '22399c02-5955-4125-8dde-7241928b4c77', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None}]
#
# standard_SG = ['sg-p98zzw10','sg-fp0nuocq']
#
# new_dict = {'InstanceId':[], 'PrivateIpAddresses':[], 'SecurityGroupIds':[],'Standard_SG':[],'Result':[]}
#
# for n in list:
#     new_dict['InstanceId'].append(n['InstanceId'])
#     new_dict['PrivateIpAddresses'].append(n['PrivateIpAddresses'][0])
#     new_dict['SecurityGroupIds'].append(n['SecurityGroupIds'])
#     new_dict['Standard_SG'].append(standard_SG)
#     if len(n['SecurityGroupIds']) > len(standard_SG):
#         match = [s for s in n['SecurityGroupIds'] if s not in standard_SG]
#         new_dict['Result'].append('多余安全组：'+str(match))
#     elif len(n['SecurityGroupIds']) < len(standard_SG):
#         match = [s for s in standard_SG if s not in n['SecurityGroupIds']]
#         new_dict['Result'].append('缺少安全组：'+str(match))
#     elif len(n['SecurityGroupIds']) == len(standard_SG):
#         match = [s for s in n['SecurityGroupIds'] if s not in standard_SG]
#         if match == []:
#             new_dict['Result'].append('安全组完全匹配')
#         elif len(match) < len(standard_SG):
#             lost = [s for s in standard_SG if s not in n['SecurityGroupIds']  ]
#             new_dict['Result'].append('部分错误安全组:'+str(match)+' 缺少安全组'+str(lost))
#         elif len(match) == len(standard_SG):
#             new_dict['Result'].append('错误安全组:' + str(match))

    
# df = pd.DataFrame(new_dict)
# df.to_excel('/Users/wanghaoyu/Desktop/test.xlsx',sheet_name='test',)

# import mysql_table_query
# project = input('项目名称: ')
# print(mysql_table_query.dhcp(project))
import re
def convert_interface_name(portname):
    interface_name = None
    if 'Ten-GigabitEthernet' in portname:
        interface_name = portname.replace('Ten-GigabitEthernet','Te')
    elif 'GigabitEthernet1' in portname:
        interface_name = portname.replace('GigabitEthernet','Gi')
    elif 'Smartrate-Ethernet' in portname:
        interface_name = portname.replace('Smartrate-Ethernet','SGE')
    return interface_name
