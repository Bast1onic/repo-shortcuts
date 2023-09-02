# repo-shortcuts
A simple Python script to fetch the links of all repositories you have owner affiliation over and create shortcuts on your local machine.

This is a work-around to being unable to organize your repositories in any sort of grouping on GitHub. The shortcuts on your local machine, on the other hand, can be organized however you like.

## Dependencies
Make sure to install the `requests` module before attempting to run this script.

## How to use
1. Clone this repository to your local machine: `git clone https://github.com/Bast1onic/repo-shortcuts`
2. [Create](https://github.com/settings/tokens/new) a GitHub API [token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with repository access. The script will use this token to fetch your repository links. Make sure to copy it as soon as you create it, or you will need to regenerate it.
3. Create `/data` and `/links` directories if they are not already present.
4. Copy the token into a file named "input.txt" in the /data directory of the repository; make sure there is no trailing whitespace or newline. The token will need to be in this file whenever you want to run the script.
5. Run the script via command line: `python mklinks.py` on Windows or `python3 mklinks.py` on MacOS/Linux.
6. The script will populate the /links folder with shortcuts. You can now organize these shortcuts however you like.

If you create or gain access to other repositories afterwards, you can repeat step 5 to get new shortcuts. The script stores links it has already fetched in /data/links.txt so that duplicate shortcuts are not created.

If you want to additionally remove dead shortcuts (i.e. to repositories you have either deleted or no longer have access to), you can specify the path of the root directory in which your shortcuts are stored so the script can find and delete them. Run the script as `python mklinks.py [root]`, where `[root]` is the path to the root directory. You must specify the absolute path unless the directory is stored within the repository.

## Notes
* The token is read from a file instead of being passed as a command-line argument so that it is not stored in console history.
* If you discover a bug or want to suggest a change, please feel free to open a new issue and/or pull request.