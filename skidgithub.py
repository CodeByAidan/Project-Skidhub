
import json
import os
import sys
import time

import colorama
import requests

#!TODO: Search for "file"
#!TODO: Search by file extension
#!TODO: Create a "settings"
#!TODO: 

#!TODO: proxy support

#!TODO: auto-post
#!TODO: auto-rat
#!TODO: auto ℝ𝕠𝕓𝕝𝕠𝕩𝕤𝕖𝕔𝕦𝕣𝕚𝕥𝕪𝕊𝕥𝕖𝕒𝕝𝕖𝕣.𝕔𝕝𝕒𝕤𝕤

def skidgithub():
    # clear the screen and make a blue title
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

    print(''' 
        [1] Download All
        [2] Download Specific Repo
        [3] Search for a file name in
        [3] Exit
    ''')

    option = input('Choose an option: ')

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

    if option == '1': # Download All Repos
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        download_all(username)

    if option == "2": # Download Specific Repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        download_specific(username, repo)

    if option == '3': # Exit
        sys.exit()


        
skidgithub()
