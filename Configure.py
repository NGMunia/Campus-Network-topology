
from netmiko import ConnectHandler
from itertools import chain
from rich import print as rp
from jinja2 import FileSystemLoader, Environment
from Network.Devices import Area_0, Firewalls, Edge_Routers, Spokes, Switches


# Configuring Netflow on Branch routers:
Template_dir =input('Jinja Templates Directory filepath: ')
rp(f'[bold cyan]----------Configuring NetFlow----------[/cyan]')
for devices in Spokes.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']

    server = input('IP address of the Flow Collector: ')
    interface = input(f'{host} Netflow source interface: ')
    Port = input(f'{host} Netflow UDP-Port: ')

    data = {
            'Flow_Interface': interface,
            'UDP_Port': Port,
            'Server_IP': server  
           }
    env = Environment(loader=FileSystemLoader(Template_dir))
    template = env.get_template('NetFlow.j2')
    commands = template.render(data)
    rp(c.send_config_set(commands.splitlines()),'\n')
    c.save_config()
    c.disconnect()


# Configuring NTP
rp(f'\n[bold cyan]----------Configuring NTP on Routers, Firewalls and Core switches----------[/bold cyan]')
for devices in chain(Area_0.values(), Firewalls.values(), Edge_Routers.values(),
                     Spokes.values(),Switches.values()):
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']
    ntp = input(f'NTP server IP for host  {host}: ')
    source = input(f'{host} NTP source interface: ')

    data = {
            'ntp_server': ntp,
            'source_intf': source
           }
    env = Environment(loader=FileSystemLoader(Template_dir))
    template = env.get_template('NTP.j2')
    commands = template.render(data)
    rp(c.send_config_set(commands.splitlines()),'\n')
    c.save_config()
    c.disconnect()

