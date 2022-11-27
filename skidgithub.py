
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
        [3] Search for a file name in all repos
        [4] Search for a file name in a specific repo
        [5] Search for a file extension in a specific repo
        [6] Exit
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
                        print(f"Found {file} in {root}")
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


    # Create a function that will check if the user's repos have already been downloaded and if they have KEEP THEM, if not download them. 
    def check_repos(username):
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

    if option == '1': # Download All Repos
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        check_repos(username)
        download_all(username)

    if option == "2": # Download Specific Repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input('Enter the username: ')
        repo = input('Enter the repo name: ')
        check_repos(username)
        download_specific(username, repo)

    #TODO: Fix this by adding a check to see if the repo has already been downloaded
    if option == "3": # Search for a file name in all repos
        os.system('cls' if os.name == 'nt' else 'clear')    
        username = input("Enter the username: ")
        file = input("Enter the file name: ")
        check_repos(username)
        search_all_files(username, file)

    #TODO: Fix this by adding a check to see if the repo has already been downloaded
    if option == "4": # Search for a file name in a specific repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input("Enter the username: ")
        repo = input("Enter the repo name: ")
        file = input("Enter the file name: ")
        check_repos(username)
        search_file(username, repo, file)

    #TODO: Fix this by adding a check to see if the repo has already been downloaded
    if option == "5": # Search for a file extension in a specific repo
        os.system('cls' if os.name == 'nt' else 'clear')
        username = input("Enter the username: ")
        repo = input("Enter the repo name: ")
        extension = input("Enter the file extension: ")
        check_repos(username)
        search_file_ext(username, repo, extension)

    if option == '6': # Exit
        sys.exit()


        
if __name__ == "__main__":
   skidgithub()
