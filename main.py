import coa_info
import doa_info

project = input('项目名称: ')
print(coa_info.get_coa_info(project,device_type='4500-16'))
for entry in doa_info.get_doa_info(project,device_type='9300'):
    print(entry)