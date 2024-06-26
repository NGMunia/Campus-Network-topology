
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from rich.prompt import Prompt
from Network.Devices import Area_0, Firewalls, Edge_Routers, Spokes, Switches, ISP_Routers
from csv import writer



# RUNNING CONFIGS
rp('[bold cyan]----------Backing Up configurations---------[/bold cyan]')
filepath = Prompt.ask('[bright_magenta]Running-configs filepath [/]')
for devices in chain(Area_0.values(), Firewalls.values(), 
                     Edge_Routers.values(), Spokes.values(), Switches.values(),ISP_Routers.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host   = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show run')

    with open(f'{filepath}/{host}', 'w')as f:
        f.write(output)
    rp(f'The running configuration of {host} has been backed up!!')



# DEVICES' INVENTORY
rp('\n[bold cyan]----------Device Inventory----------[/bold cyan]')
filepath = Prompt.ask('[bright_magenta]Inventory filepath [/]')
with open (f'{filepath}/Data.csv', 'w')as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP address','Software Image','Version','Serial number'])
    for devices in chain(Area_0.values(), Edge_Routers.values(), Firewalls.values(), 
                         Spokes.values(),  Switches.values(), ISP_Routers.values()):
        c = ConnectHandler(**devices)
        c.enable()
        output = c.send_command('show version',use_textfsm=True)[0]

        hostname = output['hostname']
        ip_addr  = devices['ip']
        image    = output['software_image']
        version  = output['version']
        serial   = output['serial']

        write_data.writerow([hostname,ip_addr,image,version,serial])
        rp(f'Finished taking {hostname} Inventory')
        c.disconnect()