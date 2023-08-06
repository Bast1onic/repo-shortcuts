import sys
import subprocess
import re
import os

# get API token
try:
    with open(f'./data/input.txt') as inputf:
        token = inputf.read().strip()
except(FileNotFoundError):
    print('Could not find input file. Make sure you spelled it correctly as "input.txt", \
          and that it is in the /data folder.')
    exit(0)

# get repos from API
fetchCmd = f'curl -s -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer {token}" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -H "affiliation: owner" \
  https://api.github.com/user/repos'

repoLines = subprocess.check_output(["grep", "full_name"], input = subprocess.check_output(fetchCmd)).decode()

# parse response
urls = set(re.findall(': "([^"]*)",', repoLines))

# open storage file
# compare against fetched result to determine new links and dead links
with open('./data/links.txt', 'r+') as links:
    storedLinks = {line.strip() for line in links.readlines()}
    newurls = urls - storedLinks
    deadurls = storedLinks - urls

    # overwrite with fetched results
    links.truncate(0)
    links.seek(0)
    links.write('\n'.join(urls))

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
                unexplored.append(item)
            elif(os.path.splitext(item)[-1]=='.url'):
                with open(item, 'r') as sc:
                    url = sc.readlines()[1][23:]
                    print(url)
                if(url in deadurls):
                    os.remove(item)
                    print(f"Removed {item}")



