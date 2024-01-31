
from rich import print as rp
from getpass import getpass

Username = input('Username: ')
Password = getpass('Password: ')
Secret   = getpass('Secret: ')

while True:
    if Username == 'Automation' and Password == 'cisco123' and Secret == 'cisco123':
        rp('[bold green] Login successful!!\n')
        break
    else:
        rp('[bold red] Incorrect Username and/or Password!\n')
        Username = input('Username: ')
        Password = getpass('Password: ')
        Secret   = getpass('Secret: ')

