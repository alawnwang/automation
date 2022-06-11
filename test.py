import ipaddress
iplist = [ipaddress.IPv4Network('30.22.0.0/24'),ipaddress.IPv4Network('30.22.1.0/24'),ipaddress.IPv4Network('30.22.2.0/24')]
print(list(ipaddress.collapse_addresses(iplist)))
