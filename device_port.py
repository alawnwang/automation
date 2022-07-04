def cisco(type):
    if type == '4500_16':
        down_link = ['TenGigabitEthernet1/'+str(portnum) for portnum in range (1,11)]
        cvp = 'TenGigabitEthernet1/12'
        up_link = 'TenGigabitEthernet1/11'
        cwl = ['TenGigabitEthernet1/13', 'TenGigabitEthernet1/14']
        interconnect = ['TenGigabitEthernet1/15','TenGigabitEthernet1/16']
        return {'downlink': down_link,'uplink': up_link,'cvp':cvp,'cwl':cwl,'interconnect': interconnect}
    elif type == '4500_32':
        down_link = ['TenGigabitEthernet1/'+str(portnum) for portnum in range (1,27)]
        cvp = 'TenGigabitEthernet1/28'
        up_link = 'TenGigabitEthernet1/27'
        cwl = ['TenGigabitEthernet1/29', 'TenGigabitEthernet1/30']
        interconnect = ['TenGigabitEthernet1/31','TenGigabitEthernet1/32']
        return {'downlink': down_link,'uplink': up_link,'cvp':cvp,'cwl':cwl,'interconnect': interconnect}
    elif type == '4500_40':
        down_link = ['TenGigabitEthernet1/'+str(portnum) for portnum in range (1,33)]
        cvp = 'TenGigabitEthernet2/4'
        up_link = 'TenGigabitEthernet2/3'
        cwl = ['TenGigabitEthernet2/5', 'TenGigabitEthernet2/6']
        interconnect = ['TenGigabitEthernet2/7','TenGigabitEthernet2/8']
        return {'downlink': down_link,'uplink': up_link,'cvp':cvp,'cwl':cwl,'interconnect': interconnect}
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

def h3c(type):
    if type == '9850_4c':
        down_link = ['Ten-GigabitEthernet1/1/1', 'Ten-GigabitEthernet1/1/2', 'Ten-GigabitEthernet1/1/3', 'Ten-GigabitEthernet1/1/4', 'Ten-GigabitEthernet1/1/5', 'Ten-GigabitEthernet1/1/6', 'Ten-GigabitEthernet1/1/7', 'Ten-GigabitEthernet1/1/8', 'Ten-GigabitEthernet1/1/9', 'Ten-GigabitEthernet1/1/10', 'Ten-GigabitEthernet1/1/11', 'Ten-GigabitEthernet1/1/12', 'Ten-GigabitEthernet1/1/13', 'Ten-GigabitEthernet1/1/14', 'Ten-GigabitEthernet1/1/15', 'Ten-GigabitEthernet1/1/16', 'Ten-GigabitEthernet1/1/17', 'Ten-GigabitEthernet1/1/18', 'Ten-GigabitEthernet1/1/19', 'Ten-GigabitEthernet1/1/20', 'Ten-GigabitEthernet1/1/21', 'Ten-GigabitEthernet1/1/22', 'Ten-GigabitEthernet1/1/23', 'Ten-GigabitEthernet1/1/24', 'Ten-GigabitEthernet1/2/1', 'Ten-GigabitEthernet1/2/2', 'Ten-GigabitEthernet1/2/3', 'Ten-GigabitEthernet1/2/4', 'Ten-GigabitEthernet1/2/5', 'Ten-GigabitEthernet1/2/6', 'Ten-GigabitEthernet1/2/7', 'Ten-GigabitEthernet1/2/8', 'Ten-GigabitEthernet1/2/9', 'Ten-GigabitEthernet1/2/10', 'Ten-GigabitEthernet1/2/11', 'Ten-GigabitEthernet1/2/12', 'Ten-GigabitEthernet1/2/13', 'Ten-GigabitEthernet1/2/14', 'Ten-GigabitEthernet1/2/15', 'Ten-GigabitEthernet1/2/16', 'Ten-GigabitEthernet1/2/17', 'Ten-GigabitEthernet1/2/18', 'Ten-GigabitEthernet1/2/19', 'Ten-GigabitEthernet1/2/20', 'Ten-GigabitEthernet1/2/21', 'Ten-GigabitEthernet1/2/22', 'Ten-GigabitEthernet1/2/23', 'Ten-GigabitEthernet1/2/24']
        cvp = 'Ten-GigabitEthernet1/0/44'
        up_link = 'Ten-GigabitEthernet1/4/1'
        cwl = ['Ten-GigabitEthernet1/3/1', 'Ten-GigabitEthernet1/3/2','Ten-GigabitEthernet1/3/3','Ten-GigabitEthernet1/3/4']
        ccs = 'Ten-GigabitEthernet1/3/5'
        interconnect = ['Ten-GigabitEthernet1/1/25','Ten-GigabitEthernet1/2/25']
        return {'downlink': down_link,'uplink': up_link,'cvp':cvp,'cwl':cwl,'ccs':ccs,'interconnect': interconnect}
    elif type == '6520_54qc':
        down_link = ['Ten-GigabitEthernet1/0/'+str(portnum) for portnum in range (1,41)]
        cvp = 'Ten-GigabitEthernet1/0/44'
        up_link = 'Ten-GigabitEthernet1/0/43'
        cwl = ['Ten-GigabitEthernet1/0/45', 'Ten-GigabitEthernet1/0/46']
        interconnect = ['Ten-GigabitEthernet1/0/47','Ten-GigabitEthernet1/0/48']
        return {'downlink': down_link,'uplink': up_link,'cvp':cvp,'cwl':cwl,'interconnect': interconnect}
    elif type == '6520_54qc_cwl':
        up_link = ['Ten-GigabitEthernet1/0/1','Ten-GigabitEthernet1/0/2']
        down_link = ['Ten-GigabitEthernet1/0/3', 'Ten-GigabitEthernet1/0/4']
        interconnect = ['Ten-GigabitEthernet1/0/47','Ten-GigabitEthernet1/0/48']
        return {'downlink': down_link,'uplink': up_link,'interconnect': interconnect}
    elif type == '6520_54qc_ccs':
        down_link = ('Ten-GigabitEthernet1/0/'+str(portnum) for portnum in range (1,46))
        up_link = ['Ten-GigabitEthernet1/0/46']
        interconnect = ['Ten-GigabitEthernet1/0/47','Ten-GigabitEthernet1/0/48']
        return {'downlink': down_link,'uplink': up_link,'interconnect': interconnect}
    elif type == '6520_54xc':
        ddown_link = ['Ten-GigabitEthernet1/0/'+str(portnum) for portnum in range (1,15)]
        edown_link = ['Ten-GigabitEthernet1/0/'+str(portnum) for portnum in range (15,29)]
        vdown_link = ['Ten-GigabitEthernet1/0/'+str(portnum) for portnum in range (29,43)]
        wdown_link = ['Ten-GigabitEthernet1/0/50:1','Ten-GigabitEthernet1/0/51:1','Ten-GigabitEthernet1/0/52:1']
        up_link = ['Ten-GigabitEthernet1/0/49:'+str(portnum) for portnum in range (1,5)]
        interconnect = ['Ten-GigabitEthernet1/0/'+str(portnum) for portnum in range (47,49)]
        return {'ddownlink':ddown_link,'edownlink':edown_link,'vdownlink':vdown_link,'wdownlink':wdown_link,'uplink':up_link,'interconnect':interconnect}
    elif type == '5130_52mp':
        up_link = ['Smartrate-Ethernet1/0/' + str(portnum) for portnum in range(49,51)]
        return up_link
    elif type == '5130_52p':
        uplink = ['GigabitEthernet1/0/' + str(portnum) for portnum in range(49,51)]
        return uplink
    elif type == '5560_54c':
        uplink = ['Ten-GigabitEthernet1/0/' + str(portnum) for portnum in range(49,51)]
        return uplink



def hillstone(type):
    if type == 'E1700':
        down_link = 'ethernet0/2'
        up_link = 'ethernet0/1'
        interconnect = ['ethernet0/7','ethernet0/8']
        return {'downlink': down_link,'uplink': up_link,'interconnect': interconnect}
