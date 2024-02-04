
from netmiko import ConnectHandler
from rich import print as rp
from jinja2 import FileSystemLoader, Environment
from Network.Devices import Area_0, Firewalls, Edge_Routers, Spokes


# Configuring Netflow on Branch routers:
Template_dir =input('Jinja Templates Directory filepath: ')
for devices in Spokes.values():
    c = ConnectHandler(**devices)
    c.enable()
    host  = c.send_command('show version', use_textfsm=True)[0]['hostname']

    server = input('IP address of the Flow Collector: ')
    interface = input(f'{host} Netflow source interface: ')
    Port = input(f'{host} Netflow UDP-Port: ')

# Data to be used in placeholders
    data = {
            'Flow_Interface': interface,
            'UDP_Port': Port,
            'Server_IP': server  
           }

# Loading the Template directory and Template itself
    env = Environment(loader=FileSystemLoader(Template_dir))
    template = env.get_template('NetFlow.j2')

# Placing the actual data on the template
    commands = template.render(data)

# Sending the commands to devices
    rp(c.send_config_set(commands.splitlines()),'\n')
    c.save_config()
    c.disconnect()

