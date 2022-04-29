# import mysql_table_query
#
#
# class generation_network:
#     def __init__(self,vlan,description,hsrpip,masterip,backupip,netmask,acl,function,floor):
#         self.floor = floor
#         self.vlan = vlan
#         self.description = description
#         self.hsrpip = hsrpip
#         self.masterip = masterip
#         self.backupip = backupip
#         self.netmask = netmask
#         self.acl = acl
#         self.function = function
#
#     def query_ip_planning(self,project):
#         for n in mysql_table_query.ip_planning(project):
#             print(n)
import pandas as pd

list = [{'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-ft25cjfv', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名2', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-htc2rnzh', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-p6q98hl3', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.70'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:36Z', 'ExpiredTime': '2022-05-06T09:54:36Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['sg-rjxkijxg', 'sg-p98zzw10', 'sg-fp0nuocq'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '22399c02-5955-4125-8dde-7241928b4c77', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None}, {'Placement': {'Zone': 'ap-shanghai-7', 'ProjectId': 0, 'HostIds': None, 'HostIps': None, 'HostId': None}, 'InstanceId': 'ins-n8ph9sdj', 'InstanceType': 'SN3ne.19XLARGE256', 'CPU': 76, 'Memory': 256, 'RestrictState': 'NORMAL', 'InstanceName': '未命名1', 'InstanceChargeType': 'PREPAID', 'SystemDisk': {'DiskType': 'CLOUD_PREMIUM', 'DiskId': 'disk-dszjcemn', 'DiskSize': 100, 'CdcId': None}, 'DataDisks': [{'DiskSize': 200, 'DiskType': 'CLOUD_SSD', 'DiskId': 'disk-blmv80pb', 'DeleteWithInstance': True, 'SnapshotId': None, 'Encrypt': False, 'KmsKeyId': None, 'ThroughputPerformance': 0, 'CdcId': None}], 'PrivateIpAddresses': ['10.88.160.77'], 'PublicIpAddresses': None, 'InternetAccessible': {'InternetChargeType': None, 'InternetMaxBandwidthOut': 0, 'PublicIpAssigned': None, 'BandwidthPackageId': None}, 'VirtualPrivateCloud': {'VpcId': 'vpc-f4hagklo', 'SubnetId': 'subnet-8tz9fh6l', 'AsVpcGateway': False, 'PrivateIpAddresses': None, 'Ipv6AddressCount': None}, 'ImageId': 'img-2lr9q49h', 'RenewFlag': 'NOTIFY_AND_AUTO_RENEW', 'CreatedTime': '2021-12-06T09:54:38Z', 'ExpiredTime': '2022-05-06T09:54:38Z', 'OsName': 'TencentOS Server 2.2 (tkernel3)', 'SecurityGroupIds': ['sg-rjxkijxg', 'sg-p98zzw10', 'sg-fp0nuocq'], 'LoginSettings': {'Password': None, 'KeyIds': None, 'KeepImageLogin': None}, 'InstanceState': 'RUNNING', 'Tags': [{'Key': '一级业务', 'Value': 'TKEX_1372246'}, {'Key': '三级业务', 'Value': '控制节点_1372251'}, {'Key': '二级业务', 'Value': 'OA_1372249'}, {'Key': '备份负责人', 'Value': 'jonasun'}, {'Key': '负责人', 'Value': 'pinepeng'}, {'Key': '运营产品', 'Value': 'TKEx-TEG-OA-IT_3272'}, {'Key': '运营部门', 'Value': '企业IT部部门级资源_1091'}], 'StopChargingMode': 'NOT_APPLICABLE', 'Uuid': '5db08c92-3e67-4b33-8564-d0806f258a6a', 'LatestOperation': 'RenewInstances', 'LatestOperationState': 'SUCCESS', 'LatestOperationRequestId': 'b483ed43-c06c-4b1f-92b4-989418e4a3c8', 'DisasterRecoverGroupId': '', 'IPv6Addresses': None, 'CamRoleName': '', 'HpcClusterId': '', 'RdmaIpAddresses': None, 'IsolatedSource': 'NOTISOLATED', 'GPUInfo': None}]




new_dict = {'InstanceId':[], 'PrivateIpAddresses':[], 'SecurityGroupIds':[]}

for n in list:
    print(n['InstanceId'],n['PrivateIpAddresses'],n['SecurityGroupIds'])
    new_dict['InstanceId'].append(n['InstanceId'])
    new_dict['PrivateIpAddresses'].append(n['PrivateIpAddresses'])
    new_dict['SecurityGroupIds'].append(n['SecurityGroupIds'])

