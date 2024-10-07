import sys
import argparse
from urllib.parse import urlparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def verbose_print(msg):
    """Print verbose messages if verbose flag is set.""" 
    if args.verbose:
        print(msg)

def validate_args(args):
    """Validate that minimum arguments are set, else quit"""
    valid = True

    if args.action is None:
        print("Please provide an action such as \"extract\" or \"set\" to either export subscribed channels into a list or subscribe to a list of channel links.")
        quit()

    if args.profile is None or Path(args.profile).is_dir() == False:
        print("Please provide the path to your firefox profile with the -p flag.\nYour profile can be found in the about:profiles page in the firefox browser.")
        valid = False

    if args.action.upper() == "SET":
        if args.filepath is None or Path(args.filepath).is_file() == False:
            print("Please provide a file with channel links with the -f.")
            valid = False

    if args.action.upper() == "EXTRACT":
        if args.filepath is None or Path(args.filepath).resolve == False:
            print("Please provide a good filepath location for outputting channel links with the -f.")
            valid = False
            
    if valid == False:
        quit()

def get_array_from_file(filepath):
    """Get list from a file, return an array."""
    if Path(filepath).is_file():
        file_array = []
        with open(filepath, "r", encoding="utf-8") as f:
            file_array = f.read().splitlines()
        return file_array
    else:
        raise RuntimeError(filepath + " is not a valid file.")

def write_array_to_file(filepath, array):
    """Write an array to a file, like channel links"""
    with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(array))

def is_valid_link(url):
    """Return bool if url is valid."""
    parsed_url = urlparse(url)
    return bool(parsed_url.scheme and parsed_url.netloc)

def get_valid_link_array(unchecked_links):
    """Returns a list of valid links"""
    checked_links = []
    for link in unchecked_links:
        if is_valid_link(link):
            checked_links.append(link)
        else:
            verbose_print("Bad link: " + link)

    if len(checked_links) > 0:
        return checked_links
    else:
        return []

def get_links_from_file(filepath):
    """Check if temp file exist, load and clean links and return link array"""
    verbose_print("Filepath: " + filepath)

    tmp_filepath = filepath + ".tmp"
    file_lines = []

    if Path(tmp_filepath).exists():
        verbose_print("Found tmp file " + tmp_filepath)
        print("Continuing from tmp file")
        file_lines = get_file_contents_as_array(tmp_filepath)
    else:
        verbose_print("Opening file " + filepath)
        file_lines = get_file_contents_as_array(filepath)

    if len(file_lines) > 0:
        return get_valid_link_array(file_lines)
    else:
        print("No lines found in file")
        quit()

def get_driver_with_profile(profile_path):
    """Load given profile, and allow user to confirm it has been loaded correctly, else input a new profile path"""
    print("Going to load profile at " + profile_path)
    try:
        user_input = profile_path
        msg = ""
        while True:
            if Path(user_input).is_dir():
                browser_options = Options()
                print("If selenium browser takes more than 2 mins to load, the path to the profile may be wrong. Exit and make sure your profile path is correct (look in the about:profiles page.")
                browser_options.profile = user_input
                driver = webdriver.Firefox(browser_options)
                driver.implicitly_wait(10)
                driver.get("https://youtube.com/")
                msg = "Please check your profile has loaded your youtube account into selenium browser window\nIf loaded correctly enter y, if not enter path to firefox profile: "
            else:
                msg = "Not a valid profile directory. Enter a valid firefox profile directory (look it up in the about:profiles page): "
                
            user_input = input(msg)

            if user_input == "y" or user_input == "Y":
                return driver
            else:
                driver.quit()
    except KeyboardInterrupt:
        print("\nStopping program")
        quit()

def subscribe_to_channels(channels_array):
    """Takes a list of subscribers channels and subscribes to each one of em"""
    print("Going to subscribe")
    try:
        for link in channels_array:
            driver.get(link)
            print(link + " -> ", end="")
            try:
                if driver.find_element(By.CSS_SELECTOR, 'yt-subscribe-button-view-model .yt-spec-button-shape-next__button-text-content').text == "Subscribe":
                    driver.find_element(By.CSS_SELECTOR, 'yt-subscribe-button-view-model').click()
                    print("subscribed")
                elif driver.find_element(By.CSS_SELECTOR, 'yt-subscribe-button-view-model .yt-spec-button-shape-next__button-text-content').text == "Subscribed":
                    print("already subscribed")
            except NoSuchElementException:
                print("Element not found")
            channels_array.remove(link)
    except:
        if args.saveprogress:
            print("Saving progress in tmp file")
            with open(args.filepath+".tmp", "w", encoding="utf-8") as f:
                for links in channel_links:
                    f.write(links + "\n")
    driver.quit()

def get_channel_links_from_youtube():
    """Get a list of subscribed channel links from youtube"""
    
    print("Going to extract channels you're subscribed to")

    SUBSCRIBER_LINK_CSS_SELECTOR =  'a#main-link'
    
    array = []
    try:
        driver.get("https://www.youtube.com/feed/channels")
        try:
            for sub in driver.find_elements(By.CSS_SELECTOR, SUBSCRIBER_LINK_CSS_SELECTOR):
                print(sub.get_attribute('href'))
                array.append(sub.get_attribute('href'))
        except:
            print("No such element or attribute found.")
    except:
        print("Could not find page.")

    return array
            
#
#
# Main
#
#

parser = argparse.ArgumentParser(prog="Youtube_Migrator",
                                 description="This program takes in a firefox profile with an open youtube account and can subscribe you to a list of youtube channels or extract them from the account.")

parser.add_argument("-a", "--action",
                    choices=["extract", "set"],
                    required=True,
                    help="The action you would like to perform on your youtube account. Extract subscribers or set them.")

parser.add_argument("-p","--profile",
                    action="store",
                    required=True,
                    help="Path to your firefox profile with an actively logged in youtube account..")

parser.add_argument("-f","--filepath",
                    action="store",
                    required=True,
                    help="Path to output channel urls or to take channel urls from.")

parser.add_argument("-v", "--verbose",
                    action="store_true",
                    help="Print all status messages.")

parser.add_argument("-s", "--saveprogress",
                    action="store_true",
                    help="Save progress when setting subscribers in a tmp file within the same directory of the given file.")

args = parser.parse_args()

verbose_print(args)

# Check if required arguments are set, else quit.
validate_args(args)

try:
    if args.action.upper() == "EXTRACT":
        # Get driver with firefox profile loaded and validate correct profile.
        driver = get_driver_with_profile(args.profile)

        channel_links_array = get_channel_links_from_youtube()

        if len(channel_links_array) > 0:
            write_array_to_file(args.filepath, channel_links_array)
            print("Done")
        else:
            print("No channel links to write to file")

        driver.quit()

    elif args.action.upper() == "SET":
        # Get channel links from file or resume from temporary file.
        channel_links_array = get_links_from_file(args.filepath)

        # Get driver with firefox profile loaded and validate correct profile.
        driver = get_driver_with_profile(args.profile)

        # One by one visit and click subscribe on each channel.
        subscribe_to_channels(channel_links_array)

        driver.quit()
except:
    driver.quit()
