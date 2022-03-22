import coa_info
import doa_info
import xoa_info


project = input('项目名称: ')
print(coa_info.get_coa_info(project))
for entry in doa_info.get_doa_info(project=project):
    print(entry)
for entry in xoa_info.generation_access_info(project=project):
    print(entry)