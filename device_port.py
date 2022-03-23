def cisco(type):
    if type == '4500_16':
        down_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (1,11)]
        cvp = 'TenGigabitEthernet1/1/12'
        up_link = 'TenGigabitEthernet1/1/11'
        cwl = ['FiveGigabitEthernet1/0/13', 'FiveGigabitEthernet1/0/14']
        interconnect = ['FiveGigabitEthernet1/0/15','FiveGigabitEthernet1/0/16']
        return {'downlink': down_link,'uplink': up_link,'cvp':cvp,'cwl':cwl,'interconnect': interconnect}
    # def coa_c4500x_32_port():
    #     down_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (1,47)]
    #     up_link = ['TenGigabitEthernet1/1/'+str(portnum) for portnum in range (1,9)]
    #     interconnect = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (47,49)]
    # def coa_c4500x_40_port():
    #     down_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (1,47)]
    #     up_link = ['TenGigabitEthernet1/1/'+str(portnum) for portnum in range (1,9)]
    #     interconnect = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (47,49)]
    elif type == '9300_48un':
        ddown_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (1,15)]
        edown_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (15,29)]
        vdown_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (29,43)]
        wdown_link = ['TenGigabitEthernet1/1/' + str(portnum) for portnum in range(5, 9)]
        up_link = ['TenGigabitEthernet1/1/'+str(portnum) for portnum in range (1,5)]
        interconnect = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (47,49)]
        return {'ddownlink':ddown_link,'edownlink':edown_link,'vdownlink':vdown_link,'wdownlink':wdown_link,'uplink':up_link,'interconnect':interconnect}
    elif type == '9300_48t':
        up_link = ['TenGigabitEthernet1/1/'+str(portnum) for portnum in range (1,3)]
        return up_link
    elif type ==  '2960_pst':
        uplink =['GigabitEthernet0/'+str(portnum) for portnum in range (3,5)]
        return uplink
    elif type == '3650_fs':
        uplink = ['GigabitEthernet1/0/' + str(portnum) for portnum in range(45, 49)]
        return uplink
    elif type == '3650_fd':
        uplink = ['TenGigabitEthernet1/1/' + str(portnum) for portnum in range(3, 5)]
        return uplink
    # def normal_config(self):
    #     normal_config = '''
    #     '''