'''
The script serves as a login mechanism before initiating any automated tasks. 
This ensures that only authorized personnel with the correct credentials can execute automation scripts, 
preventing unauthorized access and potential misuse.

'''

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

