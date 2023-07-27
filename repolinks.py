import sys
import subprocess
import re

# get API token
inputFile = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
try:
    with open(f'./data/{inputFile}') as inputf:
        token = inputf.read().strip()
except(FileNotFoundError):
    print('Could not find input file. Make sure you spelled it correctly when specifying it or rename the file to "input.txt", \
          and make sure it is in the /data folder.')
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
urls = re.findall(': "([^"]*)",', repoLines)

# check already created links
# if file is empty, skip this step
# else see which incoming links are not in file, and create those only
with open('./data/links.txt', 'w+') as links:
    storedLinks = links.readlines()
    if(len(storedLinks)>0):
        urls = set(urls) - set(storedLinks)

# create shortcuts
for url in urls:
    with open(f'./links/{url.split("/")[1]}.url', 'w') as sc:
        sc.write(f'[InternetShortcut]\rURL=https://github.com/{url}')

# record newly created links in file
with open('./data/links.txt', 'a') as links:
    if(len(storedLinks)>0 and len(urls)>0):
        links.write('\n')
    links.write('\n'.join(urls))

print("Shortcuts have been created. Check the /links folder.")
