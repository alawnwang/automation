import coa_info
import config_template
import doa_info
import xoa_info
import jinja2

project = input('项目名称: ')
# print(coa_info.get_coa_info(project))
for doa,xoa in zip(doa_info.get_doa_info(project=project),xoa_info.generation_access_info(project)):
    print(doa,xoa)




