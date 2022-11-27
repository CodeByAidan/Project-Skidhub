import json
import logging, verboselogs
import os
import sys
import time

import colorama
import requests
import yaml
import textwrap


#TODO: add a help menu
#TODO: add a credits menu
#TODO: add a update menu (check for updates)
#TODO: add a search menu (search for users, repos, files, etc)
#TODO: add a "download" menu

# check if the user is running the most recent version of the script
def check_version():
    # get the latest version from the github api
    latest_version = requests.get("https://api.github.com/repos/livxy/skidgithub/releases/latest").json()["tag_name"]
    # check if the latest version is the same as the current version
    if latest_version != version:
        # if the versions are not the same, print a message
        print(f"{colorama.Fore.RED}You are not running the latest version of skidgithub!{colorama.Fore.RESET}

if not os.path.isdir("settings/"): os.makedirs("settings/");
if not os.path.isfile("settings/config.yml"):
    with open("settings/config.yml", "a+") as file:
        file.write(f'''
Settings:
    debug: false
    proxy: false
    save_to_path: {os.getcwd()}
    threads: 1
    timeout: 10
    user_agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2
    verbose: false                               
                ''')

config = yaml.safe_load(open("settings/config.yml"))
if config['Settings']["debug"] == True:
    logging.basicConfig(level=logging.DEBUG)

if config['Settings']["verbose"] == True:
    verboselogs.install()
    logging.basicConfig(level=verboselogs.VERBOSE)

def skidgithub():
    # clear the screen and make a blue title
    def logo():
        os.system('cls' if os.name == 'nt' else 'clear')
        print(colorama.Fore.LIGHTGREEN_EX + '''
            .oooooo..o oooo         o8o        .o8  oooo                     .o8       
            d8P'    `Y8 `888         `"'       "888  `888                    "888       
            Y88bo.       888  oooo  oooo   .oooo888   888 .oo.   oooo  oooo   888oooo.  
            `"Y8888o.   888 .8P'   `888  d88' `888   888P"Y88b  `888  `888   d88' `88b 
                `"Y88b  888888.     888  888   888   888   888   888   888   888   888 
            oo     .d8P  888 `88b.   888  888   888   888   888   888   888   888   888 
            8""88888P'  o888o o888o o888o `Y8bod88P" o888o o888o  `V88V"V8P'  `Y8bod8P'                                                                                                                                                         
        ''')
        colorama.deinit()

    logo()

    print(''' 
        [1] Download All Repos from a User
        [2] Download Specific Named Repo from a User
        [3] Download File Extension from a User and Repo 
        [4] Download File Extension from a User (All Repos)
        [5] Download/Find specific file name from a User and Repo
        [6] Download/Find specific file name from a User (All Repos)
        [7] Settings 
        [8] Exit
    ''')

    option = input('Choose an option: ')

    # download all repos
    def download_all(username):
        try:
            r = requests.get(f"https://api.github.com/users/{username}/repos")
            if r.status_code != 200:
                print(f"{colorama.Fore.RED}Error: {r.status_code}")
                sys.exit(1)

            repos = json.loads(r.text or r.content)

            for repo in repos:
                name = repo["name"]
                clone_url = repo["clone_url"]
                print(f"{name}: {clone_url}")
                os.system(f"git clone {clone_url}")

            next_page = r.links["next"]["url"]

            while next_page is not None:
                r = requests.get(next_page)
                if r.status_code != 200:
                    print(f"Error: {str(r.status_code)}")
                    sys.exit(1)
                repos = json.loads(r.text or r.content)
                for repo in repos:
                    name = repo["name"]
                    clone_url = repo["clone_url"]
                    print(f"{name}: {clone_url}")
                    os.system(f"git clone {clone_url}")
                next_page = r.links["next"]["url"] if "next" in r.links else None

        except KeyError:
            print(f"Completed!\nDownloaded: {len(repos)} Repositories\nPress Enter To Exit...")
            input("")
            sys.exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Press enter to exit...")
            sys.exit(1)

    # download a specific repo
    def download_specific(username, repo):
        try:
            r = requests.get(f"https://api.github.com/repos/{username}/{repo}")
            if r.status_code != 200:
                print(f"Error: {str(r.status_code)}")
                sys.exit(1)
            repo = json.loads(r.text or r.content)
            name = repo["name"]
            clone_url = repo["clone_url"]
            print(f"{name}: {clone_url}")
            os.system(f"git clone {clone_url}")
            print("Completed in !\nPress Enter To Exit...")
            input("")
            sys.exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Press enter to exit...")
            sys.exit(1)

    # Function to search for a file name in all repos
    def search_all_files(username, file):
        try:
            r = requests.get(f"https://api.github.com/users/{username}/repos")
            if r.status_code != 200:
                print(f"Error: {str(r.status_code)}")
                sys.exit(1)
            repos = json.loads(r.text or r.content)
            for repo in repos:
                name = repo["name"]
                clone_url = repo["clone_url"]
                print(f"{name}: {clone_url}")    
                os.system(f"git clone {clone_url}")
                for root, dirs, files in os.walk(f"{name}"):
                    if file in files:
                        print(f"{file} found in {name}")
                        print(f"Path: {root}")
                        print("")            
                os.system(f"rmdir /S /Q {name}")
            next_page = r.links["next"]["url"]
            while next_page is not None:
                r = requests.get(next_page)
                if r.status_code != 200:
                    print(f"Error: {str(r.status_code)}")
                    sys.exit(1)
                repos = json.loads(r.text or r.content)
                for repo in repos:
                    name = repo["name"]
                    clone_url = repo["clone_url"]
                    print(f"{name}: {clone_url}")
                    os.system(f"git clone {clone_url}")
                    for root, dirs, files in os.walk(f"{name}"):
                        if file in files:
                            print(f"Found {file} in {root}")
                    os.system(f"rmdir /S /Q {name}")
                next_page = r.links["next"]["url"] if "next" in r.links else None 
            print("Completed in !\nPress Enter To Exit...")
            input("")
            sys.exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)

    # Function to search for a file name in a specific repo
    def search_file(username, repo, file):
        try:
            r = requests.get(f"https://api.github.com/repos/{username}/{repo}/contents")
            if r.status_code != 200:
                print(f"Error: {str(r.status_code)}")
                sys.exit(1)
            repo = json.loads(r.text or r.content)
            for file in repo:
                if file["type"] == "file":
                    print(file["name"])
            print("Completed in !\nPress Enter To Exit...")
            input("")
            sys.exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Press enter to exit...")
            sys.exit(1)

    #! this should work? 
    # Search for a file extension in a specific repo
    def search_file_ext(username, repo, extension):
        try:
            r = requests.get(f"https://api.github.com/repos/{username}/{repo}/contents")
            if r.status_code != 200:
                print(f"Error: {str(r.status_code)}")
                sys.exit(1)
            repo = json.loads(r.text or r.content)
            for file in repo:
                if file["type"] == "file" and file["name"].endswith(extension):
                    print(file["name"])
            print("Completed in !\nPress Enter To Exit...")
            input("")
            sys.exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Press enter to exit...")
            sys.exit(1)     


    # Function that will check if the user's repos have already been downloaded and if they have KEEP THEM, if not download them. 
    def check_repos(username, repo=None):
        try:
            r = requests.get(f"https://api.github.com/users/{username}/repos")
            if r.status_code != 200:
                print(f"Error: {str(r.status_code)}")
                sys.exit(1)
            repos = json.loads(r.text or r.content)
            for repo in repos:
                name = repo["name"]
                clone_url = repo["clone_url"]
                print(f"{name}: {clone_url}")
                if os.path.exists(f"{name}"):
                    print(f"{name} already exists!")
                else:
                    os.system(f"git clone {clone_url}")
            next_page = r.links["next"]["url"]
            while next_page is not None:
                r = requests.get(next_page)
                if r.status_code != 200:
                    print(f"Error: {str(r.status_code)}")
                    sys.exit(1)
                repos = json.loads(r.text or r.content)
                for repo in repos:
                    name = repo["name"]
                    clone_url = repo["clone_url"]
                    print(f"{name}: {clone_url}")
                    if os.path.exists(f"{name}"):
                        print(f"{name} already exists!")
                    else:
                        os.system(f"git clone {clone_url}")
                next_page = r.links["next"]["url"] if "next" in r.links else None 
            print("Completed in !\nPress Enter To Exit...")
            input("")
            sys.exit(0)
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Press enter to exit...")
            sys.exit(1)

    def check_repos(username, repo):
        try:
            r = requests.get(f"https://api.github.com/users/{username}/repos")
            if r.status_code != 200:
                print(f"Error: {str(r.status_code)}")
                input("Press enter to exit...")
                sys.exit(1)
            repos = json.loads(r.text or r.content)
            for repo in repos:
                name = repo["name"]
                clone_url = repo["clone_url"]
                print(f"{name}: {clone_url}")
                if os.path.isdir(f"{name}"):
                    print(f"Skipping {name}...")
                else:
                    os.system(f"git clone {clone_url}")
            next_page = r.links["next"]["url"] if "next" in r.links else None
            while next_page is not None:
                r = requests.get(next_page)
                if r.status_code != 200:
                    print(f"Error: {str(r.status_code)}")
                    sys.exit(1)
                repos = json.loads(r.text or r.content)
                for repo in repos:
                    name = repo["name"]
                    clone_url = repo["clone_url"]
                    print(f"{name}: {clone_url}")
                    if os.path.isdir(f"{name}"):
                        print(f"Skipping {name}...")
                    else:
                        os.system(f"git clone {clone_url}")
        except KeyboardInterrupt:
            print("Exiting...")
            input("Press enter to exit...")
            sys.exit(0)
        except Exception as e:
            print(f"Error: {str(e)}")
            input("Press enter to exit...")
            sys.exit(1)

    def scrape_proxies(type): #proxies [http, https, socks4, socks5, all]
        if type == "http":
            if not os.path.isdir("settings/proxies/"): os.makedirs("settings/proxies/");
            with open("settings/proxies/http.txt", "a+") as file:
                request = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=5000")
                proxies = []
                for proxy in request.text.split("\n"):
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
                        file.write(str(proxy)+"\n")
            print(f"Scraped `{len(proxies)}` HTTP proxies.")
            input("Press enter to exit...")
            sys.exit(0)


        if type == "https":
            if not os.path.isdir("settings/proxies/"): os.makedirs("settings/proxies/");
            with open("settings/proxies/https.txt", "a+") as file:
                request = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=https&timeout=5000")
                proxies = []
                for proxy in request.text.split("\n"):
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
                        file.write(str(proxy)+"\n")
            print(f"Scraped `{len(proxies)}` HTTPS proxies.")
            input("Press enter to exit...")
            sys.exit(0)  

        if type == "socks4":
            if not os.path.isdir("settings/proxies/"): os.makedirs("settings/proxies/");
            with open("settings/proxies/socks4.txt", "a+") as file:
                request = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks4&timeout=5000")
                proxies = []
                for proxy in request.text.split("\n"):
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
                        file.write(str(proxy)+"\n")
            print(f"Scraped `{len(proxies)}` SOCKS4 proxies.")
            input("Press enter to exit...")
            sys.exit(0)   

        if type == "socks5":
            if not os.path.isdir("settings/proxies/"): os.makedirs("settings/proxies/");
            with open("settings/proxies/socks5.txt", "a+") as file:
                request = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=socks5&timeout=5000")
                proxies = []
                for proxy in request.text.split("\n"):
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
                        file.write(str(proxy)+"\n")
            print(f"Scraped `{len(proxies)}` SOCKS5 proxies.")
            input("Press enter to exit...")
            sys.exit(0)

        if type == "all":
            if not os.path.isdir("settings/proxies/"): os.makedirs("settings/proxies/");
            with open("settings/proxies/all.txt", "a+") as file:
                request = requests.get("https://api.proxyscrape.com/?request=displayproxies&proxytype=all&timeout=5000")
                proxies = []
                for proxy in request.text.split("\n"):
                    proxy = proxy.strip()
                    if proxy:
                        proxies.append(proxy)
                        file.write(str(proxy)+"\n")
            print(f"Scraped `{len(proxies)}` HTTP, HTTPS, SOCKS4 AND SOCKS5 proxies.")
            input("Press enter to exit...")
            sys.exit(0)

    if option == '1': # Download All Repos from a User
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        download_all(username)

    if option == "2": # Download Specific Named Repo from a User
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        download_specific(username, repo)

    if option == "3": # Download File Extension from a User and Repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        extension = input('Enter the file extension: ')
        search_file_ext(username, repo, extension)

    if option == "4": # Download File Extension from a User (All Repos)
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        extension = input('Enter the file extension: ')

    if option == "5": # Download/Find specific file name from a User and Repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        file_name = input('Enter the file name: ')

    if option == "6": #Download/Find specific file name from a User (All Repos)
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        file_name = input('Enter the file name: ')


    if option == "7": # Settings
        def settings():
            os.system('cls' if os.name == 'nt' else 'clear')
            logo()

            with open("settings/config.yml", "r") as ymlfile:
                cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)          
                
            print(textwrap.fill("Settings", width=50, initial_indent=' ' * 25, subsequent_indent=' ' * 25))
            print(opts := (f'''
                1. Proxy = {cfg['Settings']['proxy']}
                2. User-Agent = {cfg['Settings']['user_agent']}
                3. Threads = {cfg['Settings']['threads']}
                4. Timeout = {cfg['Settings']['timeout']}
                5. Verbose = {cfg['Settings']['verbose']}
                6. Save to path = {cfg['Settings']['save_to_path']}
                7. Debug = {cfg['Settings']['debug']}
                8. Back
            '''))

            option = input("Enter the option: ")

            if option == "1": # Proxy
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current Proxy: {cfg['Settings']['proxy']}\n\n1. Use Proxy (http, https, socks4, socks5, all), \n2. Don't Use Proxy\n3. Back")
                option = input("Enter the option: ")
                if option == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    proxy = input("Enter the proxy (http, https, socks4, socks5, all): ")
                    if proxy == "http":
                        scrape_proxies("http")
                    if proxy == "https":
                        scrape_proxies("https")
                    if proxy == "socks4":
                        scrape_proxies("socks4")
                    if proxy == "socks5":
                        scrape_proxies("socks5")
                    if proxy == "all":
                        scrape_proxies("all")
                    else:
                        print("Invalid proxy type. Please create an issue on github if you think this is a bug.")
                        input("Going back to settings...")
                        settings()
                    cfg['Settings']['proxy'] = proxy
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Proxy set to {proxy}")
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    cfg['Settings']['proxy'] = ""
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print("Proxy set to None")
                    time.sleep(0.5)
                    settings()
                if option == "3":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "2": # User-Agent
                os.system('cls' if os.name == 'nt' else 'clear')


            if option == "3": # Threads
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current Threads: {cfg['Settings']['threads']}\n\n1. Use Threads\n2. Don't Use Threads\n3. Edit Threads\n4. Go Back")
                option = input("Enter the option: ")
                if option == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    threads = input("Enter the threads: ")
                    cfg['Settings']['threads'] = threads
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Threads set to {threads}")
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    cfg['Settings']['threads'] = ""
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print("Threads set to None")
                    time.sleep(0.5)
                    settings()
                if option == "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    threads = input("Enter the threads: ")
                    cfg['Settings']['threads'] = threads
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Threads set to {threads}")
                    time.sleep(0.5)
                    settings()
                if option == "4":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "4": # Timeout
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current Timeout: {cfg['Settings']['timeout']}\n\n1. Use Timeout\n2. Don't Use Timeout\n3. Edit Timeout\n4. Go Back")
                option = input("Enter the option: ")
                if option == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    timeout = input("Enter the timeout: ")
                    cfg['Settings']['timeout'] = timeout
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Timeout set to {timeout}")
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    cfg['Settings']['timeout'] = ""
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print("Timeout set to None")
                    time.sleep(0.5)
                    settings()
                if option == "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    timeout = input("Enter the timeout: ")
                    cfg['Settings']['timeout'] = timeout
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Timeout set to {timeout}")
                    time.sleep(0.5)
                    settings()
                if option == "4":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "5": # Verbose
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current Verbose: {cfg['Settings']['verbose']}\n\n1. Use Verbose\n2. Don't Use Verbose\n3. Edit Verbose\n4. Go Back")
                option = input("Enter the option: ")
                if option == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    verbose = "True"
                    cfg['Settings']['verbose'] = True 
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    verboselogs
                    print(f"Verbose set to {verbose}")
                    verboselogs.install()
                    logging.basicConfig(level=verboselogs.VERBOSE)
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    
                    cfg['Settings']['verbose'] = "False"
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print("Verbose set to False")
                    time.sleep(0.5)
                    settings()
                if option == "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    verbose = input("Enter True/False: ")
                    if verbose != "True" or "False":
                        print("Invalid option")
                        time.sleep(0.5)
                        settings()
                    cfg['Settings']['verbose'] = verbose
                    with open("settings/config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Verbose set to {verbose}")
                    time.sleep(0.5)
                    settings()
                if option == "4":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "6": # Save to file
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current directory for saved files: {cfg['Settings']['save_to_path']}\n1. Edit Save to file\n2. Go Back")
                option = input("Enter the option: ")
                if option == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    save = input("Enter the directory for which you want your files to save in: ")
                    cfg['Settings']['save_to_path'] = save
                    with open("config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"New directory for saved files set to {save}")
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "7": # Debug
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current Debug: {cfg['Settings']['debug']}\n\n1. Use Debug\n2. Don't Use Debug\n3. Edit Debug\n4. Go Back")
                option = input("Enter the option: ")
                if option == "1":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    debug = "True"
                    cfg['Settings']['debug'] = debug
                    with open("config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Debug set to {debug}")
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    debug = "False"
                    cfg['Settings']['debug'] = debug
                    with open("config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print("Debug set to False")
                    time.sleep(0.5)
                    settings()
                if option == "3":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    debug = input("Enter True/False: ")
                    cfg['Settings']['debug'] = debug
                    with open("config.yml", "w") as ymlfile:
                        yaml.dump(cfg, ymlfile)
                    print(f"Debug set to {debug}")
                    time.sleep(0.5)
                    settings()
                if option == "4":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "8": # Back
                skidgithub()

            elif option not in len(enumerate(opts)):
                print("Invalid option")
                time.sleep(0.5)
                settings()                    

        settings()

    if option == "8": #Exit
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Exiting...")
        time.sleep(0.5)
        sys.exit(0)
        
if __name__ == "__main__":
   skidgithub()
