class cisco:
    def coa_c4500x_16_port():
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
    def doa_c9300_port():
        down_link = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (1,47)]
        up_link = ['TenGigabitEthernet1/1/'+str(portnum) for portnum in range (1,9)]
        interconnect = ['FiveGigabitEthernet1/0/'+str(portnum) for portnum in range (47,49)]
        return {'downlink':down_link,'uplink':up_link,'interconnect':interconnect}
    def xoa_c9300_port():
        up_link = ['TenGigabitEthernet1/1/'+str(portnum) for portnum in range (1,9)]
        return up_link
    def evp_c2960_port():
        uplink =['GigabitEthernet0/'+str(portnum) for portnum in range (3,5)]
        return uplink
    def ewl_c3650_fs_port():
        uplink = ['GigabitEthernet1/0/' + str(portnum) for portnum in range(45, 49)]
        return uplink
    def ewl_c3650_fd_port():
        uplink = ['TenGigabitEthernet1/1/' + str(portnum) for portnum in range(3, 5)]
        return uplink
    # def normal_config(self):
    #     normal_config = '''
    #     '''