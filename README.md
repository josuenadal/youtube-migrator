# Youtube-migrator

This app opens your firefox profile within a selenium browser window, therefore gaining acces to your logged in youtube account, and extracts your subscribed youtube channels into a file or subscribes your account to youtube channels from links within a given file.

## How to use

- First log into your youtube account in your firefox browser.
- Then get the path to your firefox profile (go to about:profiles and get the Root Directory path).
- If you want to extract channels from a youtube account use the "-a extract" and the -f flag to provide your output file.
- If you want to subscribe the account to a list of channel urls use "-a set" and the -f flag to provide a file with channel urls.

For a migration you'd run the app with the extract action on one account, after that is done you'd then log in to the other account and run the app again with the set action.

This basically works by opening your firefox session within a selenium browser window and automating the extraction or subscription process.

Call the program with -h flag to see this menu.

```
usage: Youtube_Migrator [-h] -a {extract,set} -p PROFILE -f FILEPATH [-v] [-s]

This program takes in a firefox profile with an open youtube account and can subscribe you to a list of youtube channels or extract them from the
account.

options:
  -h, --help            show this help message and exit
  -a {extract,set}, --action {extract,set}
                        The action you would like to perform on your youtube account. Extract subscribers or set them.
  -p PROFILE, --profile PROFILE
                        Path to your firefox profile with an actively logged in youtube account..
  -f FILEPATH, --filepath FILEPATH
                        Path to output or take list of subscriber channel links.
  -v, --verbose         Print all status messages.
  -s, --saveprogress    Save progress when setting subscribers in a tmp file within the same directory of the given file.

```

When setting, the file with channel urls must contain one valid url per line.