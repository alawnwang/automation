import pypinyin
def get_acronym(str_data):
    return ''.join([i[0][0] for i in pypinyin.pinyin(str_data,style=pypinyin.NORMAL)])

def device_prefix(city,building_name):
    device_prefix = '-'.join((get_acronym(city).upper(),get_acronym(building_name).upper()))
    return device_prefix