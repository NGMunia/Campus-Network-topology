
from login import Username, Password, Secret


Spokes  =  {
            'BR-A1':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.10.1',
                      'ip':'10.1.11.1'
                    },
            'BR-A2':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.10.2',
                      'ip':'10.1.11.2'
                    },
            'BR-B1':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.20.1',
                      'ip':'10.1.21.1'
                    },
            'BR-B2':{
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'10.1.20.2',
                      'ip':'10.1.21.2'
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
                      'ip':'10.0.0.2',
                      'ip':'10.0.0.6'
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
          'ACC-SW': {
                      'device_type':'cisco_ios',
                      'username': Username,
                      'secret': Secret,
                      'password': Password,
                      'ip':'192.168.12.10'
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
          }