
from login import Username, Password, Secret


Spokes  =  {
            'BR-A1':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.20.0.2'
                    },
            'BR-A2':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.20.0.3'
                    },
            'BR-B1':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.20.0.4'
                    },
            'BR-B2':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.20.0.5'
                    },
            
             'BR-C':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.20.0.7'
                    }         
            }
Area_0 =  {
          'CORE-1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.0.0.1'
                    },
          'CORE-2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.0.0.5'
                    },
             'HUB': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'172.20.0.1'
                    }
          }

Firewalls=    {
          'FW-1':  {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'32.19.86.253',
                   },
        'FW-mgt':  {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.20.1'
                   },
        'FW-DMZ':  {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.50.1'
                   }
          }

Edge_Routers = {
          'Edge-1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'32.19.86.1',
                    },
          'Edge-2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'32.19.86.2'
                    }
          }
Switches= {
          'MGT-SW': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.20.10'
                    },
        'SW-BLD-1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.12.10'
                    },
        'SW-BLD-2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.12.11'
                    },
          'SW-BR1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.10.10'
                    },
          'SW-BR2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.20.10'
                    },
         'SW-SERV': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.12.253'
                    },
        'SW1-Edge': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.0.50.10'
                    },
        'SW2-Edge': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.0.50.11'
                    }               
          }
ISP_Routers = {
          'ISP-1': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'44.67.28.1',
                    },
          'ISP-2': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'72.73.74.1'
                    }
          }