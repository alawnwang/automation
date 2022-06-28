import pypinyin

#拼音首字母大写
def get_acronym(str_data):
    return ''.join([i[0][0] for i in pypinyin.pinyin(str_data,style=pypinyin.NORMAL)])

#生成设备名称前缀，exp:SZ-BH
def device_prefix(city,building_name):
    device_prefix = '-'.join((get_acronym(city).upper(),get_acronym(building_name).upper()))
    return device_prefix