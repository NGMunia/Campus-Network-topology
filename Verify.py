
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from Network.Devices import Area_0, Spokes, Firewalls, Edge_Routers, Switches


# RUNNING CONFIGS
rp('[cyan]----------Backing Up configurations---------[/cyan]')
filepath = input('Running-configs filepath: ')
for devices in chain(Area_0.values(), Firewalls.values(), 
                     Edge_Routers.values(), Spokes.values(), Switches.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host   = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show run')

    with open(f'{filepath}/{host}', 'w')as f:
        f.write(output)
    rp(f'The running confiuration of {host} has been backed up!!')



#VERIFYING SPANNING-TREE SUMMARY
for devices in Area_0.values():
    c = ConnectHandler(**devices)
    c.enable()
    rp(c.send_command('show spanning-tree summary totals'),'\n')



# VERIFYING ETHERCHANNELS
for devices in Area_0.values():
    c = ConnectHandler(**devices)
    c.enable()
    rp(c.send_command('show etherchannel summary'),'\n')



#VERIFYING HSRPv2 and VRRP
rp('\n[cyan]----------Verifying HSRP on CORE switches and EDGE Routers---------[/cyan]')   
for devices in chain(Area_0.values(),Edge_Routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show standby brief')
    rp(host,output, sep='\n')
rp('\n[cyan]----------Verifying VRRP on Spoke routers---------[/cyan]')
for devices in Spokes.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show vrrp brief')
    rp(host,output, sep='\n')



#VERIFYING OSPF ON CORE ROUTERS:
rp('\n[cyan]----------Verifying OSPF on CORE ROUTERS---------[/cyan]')
for devices in Area_0.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip route ospf')
    rp(host,output, sep='\n')



#VERIFYING BGP NLRI ON EDGE ROUTERS:
rp('\n[cyan]----------Verifying BGP NLRI on EDGE ROUTERS---------[/cyan]')
for devices in Edge_Routers.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show ip bgp')
    rp(host,output, sep='\n')
