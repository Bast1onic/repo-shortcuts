import sys
import os
import requests

# get API token
try:
    with open(f'./data/input.txt') as inputf:
        token = inputf.read().strip()
except(FileNotFoundError):
    print('Could not find input file. Make sure you spelled it correctly as "input.txt", \
          and that it is in the /data folder.')
    exit(0)

# get repos from API
url = 'https://api.github.com/user/repos'
headers = {'accept': 'application/vnd.github+json',
           'authorization': f'bearer {token}',
           'x-github-api-version': '2022-11-28',
           'affiliation': 'owner'}

r = requests.get(url, headers=headers)
if(r.status_code != 200):
    if(r.json()['message'] != None and r.json()['message'] == 'Bad credentials'):
        print('Error: invalid token')
    else:
        print("Error: Could not access GitHub API")
    exit(0)

# parse response
urls = {repo['full_name'] for repo in r.json()}
# open storage file
try:
    links = open('./data/links.txt', 'r+')
    # compare against fetched result to determine new links and dead links
    storedLinks = {line.strip() for line in links.readlines()}
    newurls = urls - storedLinks
    deadurls = storedLinks - urls
    links.truncate(0)
    links.seek(0)
except(FileNotFoundError):
    links = open('./data/links.txt', 'w')
finally:
    # overwrite with fetched results
    links.write('\n'.join(urls))
    links.close()

# create only new shortcuts
for url in newurls:
    with open(f'./links/{url.split("/")[1]}.url', 'w') as sc:
        sc.write(f'[InternetShortcut]\rURL=https://github.com/{url}')

print("Shortcuts have been created. Check the /links folder.")

# attempt to prune dead links
linksPath = sys.argv[1] if len(sys.argv) > 1 else None
choice = None

if(linksPath):
    while(choice not in ['y', 'n']):
        choice = input("It looks like you specified a path for the directory in which your links are stored. Do you wish to attempt to remove all dead links? (y/n)\n")

if(choice == 'y'):
    if(not os.path.isdir(linksPath)):
        print("Invalid path specified, aborting.")
        exit(0)
    
    unexplored = [linksPath]
    # iteratively explores directory tree rooted at linkPath
    while(len(unexplored)>0):
        curdir = unexplored.pop()
        os.chdir(curdir)
        
        for item in os.listdir():
            if(os.path.isdir(item)):
                unexplored.append(os.path.abspath(item))
            elif(os.path.splitext(item)[-1]=='.url'):
                with open(item, 'r') as sc:
                    url = sc.readlines()[1][23:]
                if(url in deadurls):
                    os.remove(item)
                    print(f"Removed {item}")

