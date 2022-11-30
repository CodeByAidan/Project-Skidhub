<h1 align="center">Project-Skidhub</h1>

<p align="center">
<br>
<a href="https://github.com/livxy/Project-Skidhub
/issues/new?assignees=&labels=&template=bug_report.md&title=">Report bug</a>
·
<a href="https://github.com/livxy/Project-Skidhub/issues/new?assignees=&labels=&template=feature_request.md&title=">Request feature</a>
<br><br>
<a href="https://github.com/livxy/Project-Skidhub"><img alt="Repo Size" src="https://img.shields.io/github/repo-size/livxy/Project-Skidhub" /></a>
<a href="https://github.com/livxy/Project-Skidhub"><img alt="File Count" src="https://img.shields.io/github/directory-file-count/livxy/Project-Skidhub" /></a>
<a href="https://github.com/livxy/Project-Skidhub"><img alt="Code Size" src="https://tokei.ekzhang.com/b1/github/livxy/Project-Skidhub" /></a>
</p>

Introducing **_Project-Skidhub_**! The simple user-friendly python script/application that does the hard Git operations through ease!

## What is it?

Simple CLI program that is extremely easy to use and user-friendly. It downloads specific files, specific file extensions, specific repos, etc. It also has search abilities to find those specific files that you have been looking for. No need to search for that needle in the haystack anymore! :smile:

## Current Features

- [x] Download All Repos from a User
- [x] Download Specific Named Repo from a User
- [x] Download File Extension from a User and Repo
- [x] Download File Extension from a User (All Repos)
- [x] Download/Find specific file name from a User and Repo
- [x] Download/Find specific file name from a User (All Repos)
- [x] Proxy Scraper (Scrapes Proxies from a website, and saves them to a file - This will be used in the future for the application)
- [x] Authorization Token (Allows you to use your own GitHub token to increase the rate limit of the application 60 -> 5000 requests per hour)
- [x] Help menu (Displays all the commands and their usage)
- [x] Settings menu (Allows you to change the settings of the application)
- [x] Easy CLI (Easy to use!)
- [x] Automation (Download with ease, no need to type in the commands every time! Just run the application and it will do the rest! 1 click and you're done!)
- [ ] Error Handling (Currently working on this, will be added soon)  
- [ ] Repost (Currently working on this, will be added soon)

## How to install

1. Install requirements:

  If you have pip installed go into the folder where all of the source code is located and run a command-prompt/terminal and run the following code:
  
  ```python
  pip install -r requirements.txt
  ```

 _If you do not have pip installed go into the folder, and run a terminal/command-prompt with the following lines of code:_
  
  ```python
  curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
  python get-pip.py
  ```

1. Run the python script:
  
  Type in your terminal/command-prompt:

  ```python
  python skidgithub.py
  ```

1. Get a GitHub token:
  (If you do not want to use a token, you can skip this step)
  (Skip this step if you downloaded v2.1 or higher, and the auto-token feature was used to get a token for you.)

- Go to [GitHub then Settings then Tokens](https://github.com/settings/tokens)
- Click on "Generate new token" then click "Generate new token (classic)"
- Give it a name (I recommend "Project Skidhub")
- Make sure to check the box that says "repo"
- Click on "Generate token"
- Copy the token
- Paste the token into the application on the first start-up (or go to /settings/config.yml and paste it into the "authorization_token" section. No quotes needed)
- Click "Save"
- Restart the application

## Agreement

You agree not to (and not to attempt to) (i) use the Service for any use or purpose other than as expressly permitted by these Terms;(ii) copy, adapt, modify, prepare derivative works based upon, distribute, license, sell, transfer, publicly display, publicly perform, transmit, stream, broadcast, attempt to discover any source code, reverse engineer, decompile, disassemble, or otherwise exploit the Service or any portion of the Service, except as expressly permitted in these Terms; or (iii) use data mining, robots, spiders, or similar data gathering and extraction tools on the Service.

This in short means that Github prohibits any form of bots and automation, which means that skidding is prohibited by ToS, and lawfully. This is for educational purposes only, if you want to use it use it at your own risk. We do not take any responsibility for you.
