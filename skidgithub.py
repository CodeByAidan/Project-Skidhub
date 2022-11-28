import json  
import logging, verboselogs
import shutil
import os
import sys
import time

import colorama
import requests
import yaml
import textwrap



def skidgithub():
    global version

    #TODO: add a help menu
    #TODO: add a credits menu
    #TODO: add a update menu (check for updates)
    #TODO: add a search menu (search for users, repos, files, etc)
    #TODO: add a "download" menu
    #TODO: MOVE FUNCTIONS OUT OF THE OPTIONS MENU (╯°□°）╯︵ ┻━┻
    #TODO: check OS and use the correct path separator
 
    def check_version():
        global version
        try:
            latest_version = requests.get("https://api.github.com/repos/livxy/Project-Skidhub/releases/latest").json()["tag_name"]
            latest_version_link = requests.get("https://api.github.com/repos/livxy/Project-Skidhub/releases/latest").json()["html_url"]
            if latest_version != version:
                print(f"{colorama.Fore.RED}You are not running the latest version of Project-Skidhub!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}Please update to the latest version!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}v{latest_version} -> {latest_version_link}{colorama.Fore.RESET}")
                sys.exit()
        except Exception as e:
            print(f"{colorama.Fore.RED}Failed to check for updates!{colorama.Fore.RESET}")
            print(f"{colorama.Fore.RED}Error: {e}{colorama.Fore.RESET}")
            # check if it's because of the rate limit
            if requests.get("https://api.github.com/rate_limit").json()["resources"]["core"]["remaining"] == 0:
                print(f"{colorama.Fore.RED}You have reached the GitHub API rate limit!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}You can check your rate limit here: https://api.github.com/rate_limit{colorama.Fore.RESET}")
                # convert line above to minutes
                print(f"{colorama.Fore.RED}Try again in: {round((requests.get('https://api.github.com/rate_limit').json()['resources']['core']['reset'] - time.time()) / 60)} minutes{colorama.Fore.RESET}")
                input("Press enter to exit...")
                sys.exit()
            else:
                print(f"{colorama.Fore.RED}Please try again later!{colorama.Fore.RESET}")
                input("Press enter to exit...")
                sys.exit()
                
    if not os.path.isdir("settings/"): os.makedirs("settings/");
    if not os.path.isfile("settings/config.yml"):
        with open("settings/config.yml", "a+") as file:
            file.write(f'''
    Settings:
        debug: false
        proxy: false
        save_to_path: {os.getcwd()}
        save_to_path_automatic: true # If true, the save_to_path will be automatically set to the current directory, even if the save_to_path is set manually.
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
    
    if config['Settings']["save_to_path_automatic"] == True:
        config["Settings"]["save_to_path"] = os.getcwd()
        with open("settings/config.yml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)
    
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
    
    check_version()
   
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

    def download_all_repos(username): #               (Option 1) - Download All Repos from a User
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

    def download_specific(username, repo): #          (Option 2) - Download Specific Named Repo from a User
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

    def search_file_ext(username, repo, extension): # (Option 3) - Download File Extension from a User and Repo
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

    def download_all(username, extension): #          (Option 4) Download File Extension from a User (All Repos)
        with open("settings/config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader) 
        r = requests.get(f"https://api.github.com/users/{username}/repos")
        if r.status_code != 200:
            print(f"Error: {str(r.status_code)} - {str(r.text)}")
            sys.exit(1)
        repos = json.loads(r.text or r.content)
        for repo in repos: 
            name = repo["name"]
            clone_url = repo["clone_url"]
            os.system(f"git clone {clone_url} {name}")
            found_name = []
            foundpath = []
            found_repo = []

            for root, dirs, files in os.walk(name):
                for file in files:
                    if file.endswith(extension):
                        found_name.append(file)
                        found_repo.append(name)
                        print(f"Found {file}")
                        if os.name == 'nt':
                            os.system(f"move .\\{name}\{file} {cfg['Settings']['save_to_path']}")
                        else:
                            os.system(f"mv ./{name}/{file} {cfg['Settings']['save_to_path']}")
                        # remove the directory
                        print(f"Moved {file} to {cfg['Settings']['save_to_path']}!")
                        foundpath.append(os.path.join(root, file))
                        if os.name == 'nt':
                            os.system(f"rmdir /s /q {name}")
                        else:
                            os.system(f"rm -rf {name}")
                        print(f"Removed {name}!")
            print(f"Found {len(found_name)} files with the extension {extension} in {len(found_repo)} repos!")
            print(f"Moved {len(found_name)} files to {cfg['Settings']['save_to_path']}!")
            print(f"Removed {len(found_repo)} repos!")
            print(f"Done!")

    def search_file_name(username, repo, file_name): #(Option 5) - Download/Find specific file name from a User and Repo
        with open("settings/config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader) 
        r = requests.get(f"https://api.github.com/repos/{username}/{repo}/contents/")
        if r.status_code != 200:
            print(f"Error: {str(r.status_code)} - {str(r.text)}")
            sys.exit(1)
        files = json.loads(r.text or r.content)
        for file in files:
            name = file["name"]
            if name == file_name:
                print(f"Found {file_name}!")
                download_url = file["download_url"]
                if os.name == 'nt':
                    os.system(f"curl -o {cfg['Settings']['save_to_path']}\{file_name} {download_url}")
                else:
                    os.system(f"curl -o {cfg['Settings']['save_to_path']}/{file_name} {download_url}")
                print(f"Downloaded {file_name} to {cfg['Settings']['save_to_path']}!")
                print(f"Moved {file_name} to {cfg['Settings']['save_to_path']}!")
                print(f"Done!")
                input("")
                sys.exit(0)
        print(f"Could not find {file_name}!")
        input("")
        sys.exit(1)
    
    def search_file_name_all(username, file_name): #  (Option 6) - Download/Find specific file name from a User (All Repos)
        with open("settings/config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader) 
        r = requests.get(f"https://api.github.com/users/{username}/repos")
        if r.status_code != 200:
            print(f"Error: {str(r.status_code)} - {str(r.text)}")
            sys.exit(1)
        repos = json.loads(r.text or r.content)
        for repo in repos:
            name = repo["name"]
            clone_url = repo["clone_url"]
            os.system(f"git clone {clone_url} {name}")
            found_name = []
            foundpath = []
            found_repo = []
            for root, dirs, files in os.walk(name):
                for file in files:
                    if file == file_name:
                        found_name.append(file)
                        found_repo.append(name)
                        print(f"Found {file}!")
                        if os.name == 'nt':
                            os.system(f"move .\\{name}\{file} {cfg['Settings']['save_to_path']}")
                        else:
                            os.system(f"mv ./{name}/{file} {cfg['Settings']['save_to_path']}")
                        # remove the directory
                        if os.name == 'nt':
                            os.system(f"rmdir /s /q {name}")
                        else:
                            os.system(f"rm -rf {name}")
                        print(f"Moved {file} to {cfg['Settings']['save_to_path']}!")
                        print(f"Removed {name}!")
                        foundpath.append(os.path.join(root, file))
            print(f"Found {len(found_name)} files with the name {file_name} in {len(found_repo)} repos!")
            print(f"Moved {len(found_name)} files to {cfg['Settings']['save_to_path']}!")
            print(f"Removed {len(found_repo)} repos!")
            print(f"Done!")
            input("")
            sys.exit(0)
        print(f"Could not find {file_name}!")
        input("")
        sys.exit(1)

    def scrape_proxies(type): #                       (In Option 7 - Settings) - proxies [http, https, socks4, socks5, all]
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

    def settings(): #                                 (Option 7) - Settings
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

    if option == '1': # Download All Repos from a User
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        download_all_repos(username)

    if option == "2": # Download Specific Named Repo from a User - download_specific(username, repo)
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        download_specific(username, repo)

    if option == "3": # Download File Extension from a User and Repo - search_file_ext(username, repo, extension)
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        extension = input('Enter the file extension: ')
        search_file_ext(username, repo, extension)

    if option == "4": # Download File Extension from a User (All Repos)
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        extension = input('Enter the file extension: ')
    
        download_all(username, extension)
                    
    if option == "5": # Download/Find specific file name from a User and Repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        file_name = input('Enter the file name (including extension i.e. "index.html"): ')

            
        search_file_name(username, repo, file_name)

    if option == "6": #Download/Find specific file name from a User (All Repos)
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        file_name = input('Enter the file name (including extension i.e. "index.html"): ')

        search_file_name_all(username, file_name)

    if option == "7": # Settings                
        settings()

    if option == "8": # Repost :troll:
        os.system('cls' if os.name == 'nt' else 'clear')
        logo()
        print("")

    if option == "8": #Exit
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Exiting...")
        time.sleep(0.5)
        sys.exit(0)
        
if __name__ == "__main__":
   version = "1.0"
   skidgithub()
