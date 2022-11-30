import json  
import logging, verboselogs
import os
import sys
import time

import colorama
from colorama import Fore, Style
import requests
import yaml
import textwrap

def skidgithub():

    #TODO: add a search menu (search for users, repos, files, etc)
    #TODO: add a "download" menu
    #TODO: Convert to tkinker GUI - Use pyinstaller to make an executable file

    def check_version():
        global version
        
        try:
            print(f"{colorama.Fore.YELLOW}Checking for updates...{colorama.Style.RESET_ALL}")
            latest_version = requests.get("https://api.github.com/repos/livxy/Project-Skidhub/releases/latest", headers={"authorization": f"token {config['Settings']['authorization_token']}"}).json()["tag_name"]
            latest_version_link = requests.get("https://api.github.com/repos/livxy/Project-Skidhub/releases/latest", headers={"authorization": f"token {config['Settings']['authorization_token']}"}).json()["html_url"]
            if latest_version != version:
                print(f"{colorama.Fore.RED}You are not running the latest version of Project-Skidhub!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}Please update to the latest version!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}v{latest_version} -> {latest_version_link}{colorama.Fore.RESET}")
                sys.exit()
            else:
                print(f"{colorama.Fore.GREEN}You are running the latest version of Project-Skidhub!{colorama.Fore.RESET}")          
                time.sleep(0.5)
                os.system("cls" if os.name == "nt" else "clear")  
        except Exception as e:
            print(f"{colorama.Fore.RED}Failed to check for updates!{colorama.Fore.RESET}")
            print(f"{colorama.Fore.RED}Error: {e}{colorama.Fore.RESET}")
            # check if it's because of the rate limit
            if requests.get("https://api.github.com/rate_limit", headers={"authorization": f"token {config['Settings']['authorization_token']}"}).json()["resources"]["core"]["remaining"] == 0:
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
            # The path is to a folder inside the current directory called "Downloads"
            # Create a folder in current directory called "Downloads" if it doesn't exist
            if not os.path.isdir("Downloads/"): os.makedirs("Downloads/");
            path = os.path.join(os.getcwd(), "Downloads")
            file.write(f'''
Settings:
  debug: false
  # proxy: false
  save_to_path: {path}
  save_to_path_automatic: true
  # threads: 1
  # timeout: 10
  # user_agent: Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.2) Gecko/20100101 Firefox/10.0.2
  verbose: true
  authorization_token: "" # Visit https://github.com/settings/tokens to generate a token                               
                    ''')

    config = yaml.safe_load(open("settings/config.yml"))
    if config['Settings']["debug"] == True:
        logging.basicConfig(level=logging.DEBUG)

    if config['Settings']["verbose"] == True:
        verboselogs.install()
        logging.basicConfig(level=verboselogs.VERBOSE)

    if config['Settings']["save_to_path_automatic"] == True:
        config["Settings"]["save_to_path"] = os.path.join(os.getcwd(), "Downloads")
        with open("settings/config.yml", "w") as file:
            yaml.dump(config, file, default_flow_style=False)


    def auth_checker():
        if config['Settings']['authorization_token'] in ["", "null", " "]:
            link = "https://github.com/settings/tokens/new?scopes=repo&description=Project-Skidhub"

            # Based on their OS open the link in the browser - supported OS: Windows, Linux, Mac
            if sys.platform == "win32":
                os.startfile(link)
            elif sys.platform == "darwin":
                os.system(f"open {link}")
            elif sys.platform == "linux":
                os.system(f"xdg-open {link}")        
            else:
                print(f"{colorama.Fore.RED}Your OS is not supported!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}Please generate a token here: {link}!{colorama.Fore.RESET}")

            print(f"{colorama.Fore.RED}Please enter your GitHub authorization token!{colorama.Fore.RESET}")
            print(f"{colorama.Fore.RED}Read the instructions in the README.md file!{colorama.Fore.RESET}")
            token = input("Token: ")
            config["Settings"]["authorization_token"] = token
            with open("settings/config.yml", "w") as file:
                yaml.dump(config, file, default_flow_style=False)
            if requests.get("https://api.github.com/user", headers={"authorization": f"token {config['Settings']['authorization_token']}"}).status_code == 200:
                print(f"{colorama.Fore.GREEN}Your token is valid!{colorama.Fore.RESET}")
            else:
                print(f"{colorama.Fore.RED}Your token: '{config['Settings']['authorization_token']}' is invalid!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}Please generate a new token!{colorama.Fore.RESET}")
                auth_checker()
                sys.exit()
        #? Should I get rid of lines 113-130 and just make it so that if the token is invalid it will just generate a new one? 
        else:
            if requests.get("https://api.github.com/user", headers={"authorization": f"token {config['Settings']['authorization_token']}"}).status_code == 200:
                print(f"{colorama.Fore.GREEN}Your token is valid!{colorama.Fore.RESET}")
            else:
                print(f"{colorama.Fore.RED}Your token: '{config['Settings']['authorization_token']}' is invalid!{colorama.Fore.RESET}")
                print(f"{colorama.Fore.RED}Please generate a new token!{colorama.Fore.RESET}")
                token = input("Token: ")
                config["Settings"]["authorization_token"] = token
                with open("settings/config.yml", "w") as file:
                    yaml.dump(config, file, default_flow_style=False)
                if requests.get("https://api.github.com/user", headers={"authorization": f"token {config['Settings']['authorization_token']}"}).status_code == 200:
                    print(f"{colorama.Fore.GREEN}Your token is valid!{colorama.Fore.RESET}")
                else:
                    print(f"{colorama.Fore.RED}Your token: '{config['Settings']['authorization_token']}' is invalid!{colorama.Fore.RESET}")
                    print(f"{colorama.Fore.RED}Please generate a new token!{colorama.Fore.RESET}")
                    auth_checker()
                    sys.exit()
    
    auth_checker()
    check_version()
    # End of startup

    def after_startup():
        
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
            [8] Help
            [9] Exit
            [0] Credits
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
                    os.system(f"git clone {clone_url} {config['Settings']['save_to_path']}")

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
                        os.system(f"git clone {clone_url} {config['Settings']['save_to_path']}")
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
                os.system(f"git clone {clone_url} {config['Settings']['save_to_path']}")
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
                os.system(f"git clone {clone_url} {name} {config['Settings']['save_to_path']}")

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
                os.system(f"git clone {clone_url} {name} {cfg['Settings']['save_to_path']}")
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
                1. Proxy Scrapper = {cfg['Settings']['proxy']}
                2. Verbose = {cfg['Settings']['verbose']}
                3. Save to path = {cfg['Settings']['save_to_path']}
                4. Debug = {cfg['Settings']['debug']}
                5. Back
            '''))

            option = input("Enter the option: ")

            if option == "1": # Proxy
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"Current Proxy: {cfg['Settings']['proxy']}\n\n1. Scrape Proxy (http, https, socks4, socks5, all), \n2. Don't Use Proxy [FUTURE FEATURE]\n3. Back")
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
                    # print(f"Proxy set to {proxy}")
                    time.sleep(0.5)
                    settings()
                if option == "2":
                    os.system('cls' if os.name == 'nt' else 'clear')
                    logo()
                    print("This feature is not available yet.")
                    # cfg['Settings']['proxy'] = ""
                    # with open("settings/config.yml", "w") as ymlfile:
                    #     yaml.dump(cfg, ymlfile)
                    # print("Proxy set to None")
                    time.sleep(1.5)
                    settings()
                if option == "3":
                    settings()
                else:
                    print("Invalid option")
                    time.sleep(0.5)
                    settings()

            if option == "2": # Verbose
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

            if option == "3": # Save to path
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

            if option == "4": # Debug
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

            if option == "5": # Back
                skidgithub()

            elif option not in len(enumerate(opts)):
                print("Invalid option")
                time.sleep(0.5)
                settings()    

        def help(): #                                     (Option 8) - Help
            os.system('cls' if os.name == 'nt' else 'clear')
            logo()
            print("1. What is Skid Github?\n2. How to use Skid Github?\n3. Go Back")
            option = input("Enter the option: ")
            if option == "1":
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print("Skid Github is a tool that can be used to find sensitive files on github.")
                time.sleep(0.5)
                help()
            if option == "2":
                os.system('cls' if os.name == 'nt' else 'clear')
                logo()
                print(f"""
                1. Download All Repos from a User (This will download all the repos from a user)
                2. Download a Specific Repo from a User (This will download a specific repo from a user)
                3. Download File Extension from a User and Repo (This will search for files with a file extension in a repo from a user)
                4. Download File Extension from a User (This will search for files with a file extension in all the repos from a user)
                5. Download File Name from a User and Repo (This will search for a file with a name in a repo from a user)
                6. Download File Name from a User (This will search for a file with a name in all the repos from a user)
                """)
                input("Press enter to go back")
                help()
            if option == "3":
                skidgithub()        

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

        if option == "6": # Download/Find specific file name from a User (All Repos)
            os.system('cls' if os.name == 'nt' else 'clear')
            username = input('Enter the username: ')
            file_name = input('Enter the file name (including extension i.e. "index.html"): ')

            search_file_name_all(username, file_name)

        if option == "7": # Settings                
            settings()

        if option == "8": # Help
            help()

        if option == "9": # Exit
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Exiting...{Fore.RESET}{Style.RESET_ALL}")
            time.sleep(0.5)
            sys.exit(0)
            
        if option == "0": # Credits
            os.system('cls' if os.name == 'nt' else 'clear')
            logo()
            # In the print statement-line below-use colorama to make the text colorful
            print(f"""
            {Fore.RED}{Style.BRIGHT}Skidhub
            {Fore.GREEN}{Style.BRIGHT}Version: 2.1
            {Fore.YELLOW}{Style.BRIGHT}Author: {Fore.RED}{Style.BRIGHT}livxy
            {Fore.MAGENTA}{Style.BRIGHT}Github: {Fore.RED}{Style.BRIGHT}https://github.com/livxy
            {Fore.CYAN}{Style.BRIGHT}Discord: {Fore.RED}{Style.BRIGHT}bruhs#7404
            
            {Fore.YELLOW}{Style.BRIGHT}Special Thanks to:
            - {Fore.RED}{Style.BRIGHT}timof121{Fore.YELLOW}{Style.BRIGHT}{Fore.RED}{Style.BRIGHT}: {Fore.YELLOW}{Style.BRIGHT}For helping me with the code, and for being a great friend. :)
            - {Fore.MAGENTA}{Style.BRIGHT}Github: {Fore.RED}{Style.BRIGHT}https://github.com/timof121
            {Fore.RESET}{Style.RESET_ALL}
            
            
            {Fore.RED}{Style.BRIGHT}Press enter to go back{Fore.RESET}{Style.RESET_ALL}
            """)
            input(); os.system("cls" if os.name == "nt" else "clear"); after_startup() 
    after_startup()
            
if __name__ == "__main__":
    version = "3.0"
    try: 
        skidgithub()
    except KeyboardInterrupt:
        print(f"\n\n\n{colorama.Fore.RED}{logging.getLevelName(logging.ERROR)}: Keyboard Interrupt{Fore.RESET}{Style.RESET_ALL}")
        colorama.deinit()
        time.sleep(0.5)
        sys.exit(0)
