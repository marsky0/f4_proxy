import requests
import time
import subprocess
import asyncio

# ANSI color codes
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
RESET = '\033[0m'

def ping(ip):
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True)
        if result.returncode == 0:
            time_ms = float(result.stdout.split('time=')[-1].split(' ms')[0])
            return time_ms
    except Exception as e:
        print(f'{RED}Error pinging {ip}: {e}{RESET}')
    return None

async def get_ping(count, ip):
    accumulated_ping = 0
    loop = asyncio.get_running_loop()
    
    for _ in range(count):
        result = await loop.run_in_executor(None, ping, ip)
        if result is None:
            return None
        accumulated_ping += result
        await asyncio.sleep(1)
    return accumulated_ping / count

def update_hosts(new_ip):
    HOSTS_FILE = '/etc/hosts'
    DOMAIN_SPOT = 'api.binance.com'
    DOMAIN_FUTURES = 'fapi.binance.com'
    try:
        with open(HOSTS_FILE, 'r') as file:
            lines = file.readlines()
        
        with open(HOSTS_FILE, 'w') as file:
            for line in lines:
                if DOMAIN_FUTURES not in line:
                    file.write(line)
            #file.write(f'{new_ip} {DOMAIN_SPOT}\n')
            file.write(f'{new_ip} {DOMAIN_FUTURES}\n')
        
        print(f'{GREEN}File {HOSTS_FILE} updated: {new_ip} -> {DOMAIN_FUTURES}{RESET}')
    except Exception as e:
        print(f'{RED}Error updating {HOSTS_FILE}: {e}{RESET}')

ip_lists = [
    '13.225.164.218', 
    '13.227.61.59', 
    '143.204.127.42', 
    '13.35.51.41', 
    '99.84.58.138', 
    '18.65.193.131', 
    '18.65.176.132', 
    '99.84.140.147', 
    '13.225.173.96', 
    '54.240.188.143', 
    '13.35.55.41',
    '13.35.57.207',
    '18.65.207.131', 
    '143.204.79.125', 
    '65.9.40.137', 
    '99.84.137.147', 
    '18.65.212.131',
    '108.138.23.14',
]

async def loop():
    best_ip = None
    best_ping = float('inf')
    tasks = {ip: get_ping(3, ip) for ip in ip_lists}
    results = await asyncio.gather(*tasks.values())
    
    for ip, ping_result in zip(tasks.keys(), results):
        if ping_result is not None:
            ping_result = int(ping_result)
            
            if ping_result > 500:
                color = RED
            elif ping_result > 50:
                color = YELLOW
            else:
                color = GREEN
            
            print(f'{color}{ip}: {ping_result}ms{RESET}')
            
            if ping_result < best_ping:
                best_ping = ping_result
                best_ip = ip
        else:
            print(f'{RED}{ip}: Error{RESET}')
    
    if best_ip:
        print(f'Best IP: {GREEN}{best_ip}{RESET}')
        update_hosts(best_ip)

async def main():
    while True:
        try:
            await loop()
            await asyncio.sleep(60)
        except Exception as e:
            print(f'{RED}Error: {e}{RESET}')

asyncio.run(main())

