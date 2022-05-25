down_link = {'module1':['Ten-GigabitEthernet1/1/' + str(portnum) for portnum in range(1,25)],'moudle2':['Ten-GigabitEthernet1/2/' + str(portnum) for portnum in range(1,25)],'module2':['Ten-GigabitEthernet1/2/' + str(portnum) for portnum in range(1,25)],'module3':['Ten-GigabitEthernet1/2/' + str(portnum) for portnum in range(1,25)],'module4':['Ten-GigabitEthernet1/2/' + str(portnum) for portnum in range(1,25)]}
down_link['module1'].append('FortyGigE1/1/25')
down_link['module1'].append('FortyGigE1/1/26')
down_link['module2'].append('FortyGigE1/1/25')
down_link['module2'].append('FortyGigE1/1/26')
down_link['module3'].append('FortyGigE1/1/25')
down_link['module3'].append('FortyGigE1/1/26')
down_link['module4'].append('FortyGigE1/1/25')
down_link['module4'].append('FortyGigE1/1/26')


print(down_link)