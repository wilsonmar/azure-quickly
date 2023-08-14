#!/usr/bin/env python3
# Copyright (c) JetBloom LLC
# SPDX-License-Identifier: MPL-2.0
"""az-status.py within https://github.com/wilsonmar/az-status/blob/master/az-status/
   Explained at https://wilsonmar.github.io/azure-quickly ???
   This is sample code to provide a feature-rich base for new Python 3.9+ programs run from CLI.
   It implements advice at https://www.linkedin.com/pulse/how-shine-coding-challenges-wilson-mar-/
   
   Examples also include feature flags, and various ways of calling APIs.
   Use this code to avoid wasting time "reinventing the wheel" and getting various coding working together,
   especially important due to the heightened security needed in today's world of ransomware.

   Includes built-in testing.

   Security features here include calls to various cloud secret key managers and file encryption,
   all in one program so data can be passed between different clouds.
   Here we use a minimum of 3rd-party library dependencies (to avoid transitive vulnerabilities).

   NO  Text Internationalization (English only)
   NOT Using Azure Secrets API https://developer.hashicorp.com/vault/api-docs/secret/azure

   This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS
   OF ANY KIND, either express or implied. See the License for the specific
   language governing permissions and limitations under the License.
"""

#### SECTION 01. Set Default Global Variables:

__repository__ = "https://github.com/wilsonmar/azure-quickly"
__author__ = "Wilson Mar"
__copyright__ = "See the file LICENSE for copyright and license info"
__license__ = "See the file LICENSE for copyright and license info"
__linkedin__ = "https://linkedin.com/in/WilsonMar"
__version__ = "0.3.2"  # Initial based on https://github.com/wilsonmar/az-status/blob/master/api-sample.py
    # Using semver.org format per PEP440: change on every commit:


#### SECTION 02. Import libraries (in alphabetical order)

# The first of several external dependencies, and will error if not installed:
# (preferrably within a conda enviornment):
# requirements.txt
# pip install azure  # https://pypi.org/project/azure/
import argparse   # for cmd parameters using ArgumentParser in 3.6+
#import azure    # FIXME
#import azure-cli
#from azure.cli.core import get_default_cli as azcli

import base64  # encoding
# import boto3   # for aws
# from botocore.exceptions import ClientError  # for aws
# from cryptography.fernet import Fernet
import _datetime  # because "datetime" doesn't work.
from _datetime import timedelta

from dateutil import tz
   # See https://bobbyhadz.com/blog/python-no-module-named-dateutil

from datetime import datetime
from datetime import timezone
from decimal import Decimal

# FIXME: ModuleNotFoundError: No module named 'dotenv'
# from dotenv import load_dotenv
   # Based on: pip3 install python-dotenv
   # load_dotenv()  # Retrieve from .env into Python global variables.
   # See https://www.python-engineer.com/posts/dotenv-python/
   # See https://pypi.org/project/python-dotenv/

# from google.cloud import secretmanager

import hashlib  # https://docs.python.org/3/library/hashlib.html
# Based on: pip install hvac 
import hvac     # Hashicorp Vault Python lib
   # HashiCorp Vault Python Client v23.1.2 from https://pypi.org/project/hvac/
import json
# import jwt
# import keyring   # used by use_keyring 
# import keyring.util.platform_ as keyring_platform
import locale  # https://phrase.com/blog/posts/beginners-guide-to-locale-in-python/
import logging    # see https://realpython.com/python-logging/
import os   # only on unix-like systems
            # for os.getenv(),  os.uname, os.getpid(), os.environ, os.import, os.path
from os import path

# ~/.local/lib/python3.8/site-packages (2.3.0)
from pathlib import Path  # python3 only
import pathlib
# import pickle      # for serialization and deserialization of objects,
   # is denylisted
import platform    # built-in for mac_ver()
import pytz        # pytz-2021.3 for time zone handling 
import pwd
# import pyjwt  #  pyjwt-2.7.0 

import random   # built-in lib
from random import SystemRandom

import re  # regular expression
# import redis
import requests
from requests.auth import HTTPDigestAuth
import shutil
import site
import smtplib  # to send email
import socket
from stat import *
# import subprocess  # Blacklisted -
# https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess
import sys        # for sys.argv[0], sys.exit(), sys.version
#from sys import platform
# from textblob import TextBlob
import time       # for sleep(secs)
from timeit import default_timer as timer

import unittest
import urllib.request
import uuid       # https://docs.python.org/3/library/uuid.html
import webbrowser


#### SECTION 03: Capture pgm start date/time 

# Obtain pgm start to obtain run duration at end:
pgm_start_timestamp = time.monotonic()  # for wall-clock time (includes any sleep).
pgm_start_epoch_timestamp = time.time()  # TODO: Display Z (UTC/GMT) instead of local time
pgm_start_local_timestamp = time.localtime()
    # See https://www.geeksforgeeks.org/get-current-time-in-different-timezone-using-python/


#### SECTION 04: Default Feature flag settings (in order of code):

run_mode = "dev"   # vs. "prod"
clear_cli = True   # Clear Console so output always appears at top of screen.

show_print_samples = True
show_warning = True    # -wx  Don't display warning
show_info = True       # -qq  Display app's informational status and results for end-users
show_heading = True    # -q  Don't display step headings before attempting actions
show_verbose = True    # -v  Display technical program run conditions
show_trace = True     # -vv Display responses from API calls for debugging code
show_fail = True       # Always show
show_secrets = True       # Never show

show_pgm_init = True   # Display pgm init date/time and env info

verify_manually = True

# 6. Obtain run control data from .env file in the user's $HOME folder
#    to obtain the desired cloud region, zip code, and other variable specs.
use_env_file = False  # until load is fixed.
show_env = True
remove_env_line = False

# 6. Define Localization (to translate text to the specified locale)
localize_text = False

# 7. Display run conditions: datetime, OS, Python version, etc. = show_pgminfo
show_pgminfo = True

   # Load Country SQLite in-memory database for date-time formats = load_country_db
load_country_db = False

# 8. Define utilities for managing local data storage folders and files
use_pytz_datetime = True
show_dates = True

show_logging = True

show_aws_init = True
# Vault defaults if parameters are not provided:
VAULT_URL_PORT='http://127.0.0.1:8200'
VAULT_TOKEN='dev-only-token'
VAULT_USER='default_user'

login_to_azure = True

# 9. Generate various calculations for hashing, encryption, etc.

# 9.1. Generate Hash (UUID/GUID) from a file    = gen_hash
gen_hash = False
# 9.2. Generate a random salt                   = gen_salt
gen_salt = False
# 9.3. Generate a random percent of 100         = gen_1_in_100
gen_1_in_100 = False
# 9.4. Convert between Roman numerals & decimal = process_romans
process_romans = False
# 9.5. Generate JWT (Json Web Token)            = gen_jwt
gen_jwt = False
# 9.6. Generate Lotto America Numbers           = gen_lotto
gen_lotto = False
# 9.7. Make a decision                          = magic_8ball
gen_magic_8ball = False

# 10. Retrieve client IP address                  = get_ipaddr
get_ipaddr = False
# 11. Lookup geolocation info from IP Address     = lookup_ipaddr
lookup_ipaddr = False

# 12. Obtain Zip Code to retrieve Weather info    = lookup_zipinfo
lookup_zipinfo = False
# 13. Retrieve Weather info using API             = show_weather
show_weather = True
email_weather = False

##  14. Retrieve secrets from local OS Keyring  = use_keyring
use_keyring = False

# 14. Retrieve secrets from Azure Key Vault  = use_azure
use_azure = False
use_azure_redis = False

# 14.1 Generate a fibonacci number recursion    = gen_fibonacci
# (write and read to Azure Redis)
gen_fibonacci = False

# 9.9 Make change using Dynamic Programming     = make_change
make_change = False

# 9.10 "Knapsack"
fill_knapsack = False

# 15. Retrieve secrets from AWS KMS         = use_aws
# https://cloudacademy.com/course/get-started-with-aws-cloudhsm/what-is-cloudhsm/
use_aws = False

# 16. Retrieve secrets from GCP Secret Manager = use_gcp
use_gcp = False

# 17. Retrieve secrets from Hashicorp Vault = use_hvac
use_hvac = False

# 18. Create/Reuse container folder for img app to use

# 18.1 Get proof on Blockchain  = add_blockchain
add_blockchain = True

# 19. Download img application files           = download_imgs
download_imgs = False     # feature flag
img_set = "small_ico"      # or others
img_file_name = None

cleanup_img_files = False
remove_img_dir_at_beg = False
remove_img_dir_at_end = False    # to clean up folder
remove_img_file_at_beg = False
remove_img_file_at_end = False   # to clean up file in folder

# 20. Manipulate image (OpenCV OCR extract)    = process_img
process_img = False

img_file_naming_method = "uuid4time"  # or "uuid4hex" or "uuid4"

# 21. Send message to Slack                    = send_slack_msgs  (TODO:)
send_slack = False

# 22. Send email thru Gmail         = email_via_gmail
email_via_gmail = False
verify_email = False
email_file_path = ""

# 23. Calculate Hash and View Gravatar on Web Browser   = view_gravatar
# (use MD5 Hash)
view_gravatar = False

# 24. Calculte BMI using units of measure  = categorize_bmi
# (Metric vs English conversoin based on country code)
categorize_bmi = False
email_weather = False

# 97. Play text to sound:
gen_sound_for_text = False
remove_sound_file_generated = False

# 98. Remove (clean-up) folder/files created   = cleanup_img_files
cleanup_img_files = False
# 99. Display run time stats at end of program = display_run_stats
display_run_stats = False



#### SECTION 05. Parse arguments that control program operation

# https://towardsdatascience.com/a-simple-guide-to-command-line-arguments-with-argparse-6824c30ab1c3
# Assumes: pip install argparse
# import argparse
parser = argparse.ArgumentParser(
    description="A Python3 console (CLI) program to call APIs storing secrets.")
# -h (for help) is by default.
parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='Verbose messages')
parser.add_argument(
    '-q',
    '--quiet',
    action='store_true',
    help='Quiet headers/footers')

# Based on https://docs.python.org/3/library/argparse.html
args = parser.parse_args()
# if show_verbose == True:
#    print(f'*** args.v={args.v}')


#### SECTION 06. Define utilities for printing (in color with emojis)

# QUESTION: How to pull in text_in containing {}.

if clear_cli:
    import os
    # QUESTION: What's the output variable?
    lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')

class bcolors:  # ANSI escape sequences:
    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[37m'   # [37 white
    FAIL = '\033[91m'      # [91 red
    WARNING = '\033[93m'   # [93 yellow
    INFO = '\033[92m'      # [92 green
    VERBOSE = '\033[95m'   # [95 purple
    TRACE = '\033[96m'     # [96 blue/green

                 # [94 blue (bad on black background)
    CVIOLET = '\033[35m'
    CBEIGE = '\033[36m'
    CWHITE = '\033[37m'

    RESET = '\033[0m'      # switch back to default color

def print_separator():
    """ A function to put a blank line in CLI output. Used in case the technique changes throughout this code. """
    print(" ")

def print_heading(text_in):
    if show_heading:
        print('\n***', bcolors.HEADING+bcolors.UNDERLINE, f'{text_in}', bcolors.RESET)

def print_fail(text_in):
    if show_fail:
        print('***', bcolors.FAIL, "FAIL:", f'{text_in}', bcolors.RESET)

def print_warning(text_in):
    if show_warning:
        print('***', bcolors.WARNING, "WARNING:", f'{text_in}', bcolors.RESET)

def print_info(text_in):
    if show_info:
        print('***', bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)

def print_verbose(text_in):
    if show_verbose:
        print('***', bcolors.VERBOSE, f'{text_in}', bcolors.RESET)

def print_trace(text_in):  # displayed as each object is created in pgm:
    if show_trace:
        print('***', bcolors.TRACE, f'{text_in}', bcolors.RESET)

def print_secret(secret_in):
    """ Outputs only the first few characters (like Git) plus dots replacing the rest """
    secret_len = 32  # same length regardless of secret length to reduce ability to guess:
    if len(secret_in) >= 20 :  # slice 
       secret_out = secret_in[0:4] + "."*(secret_len-4)
    else:
       secret_out = secret_in[0:1] + "."*(secret_len-1)
    print('***', bcolors.CBEIGE, "SECRET: ", f'{secret_out}', bcolors.RESET)

if show_print_samples:
    print_heading("show_print_samples")
    print_fail("sample fail")
    print_warning("sample warning")
    print_info("sample info")
    print_verbose("sample verbose")
    print_trace("sample trace")
    print_secret("1234567890123456789")

# From here on:
print_heading("show during construction")


#### SECTION 07. Utilities for managing data storage folders and files

def dir_remove(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)  # deletes a directory and all its contents.
        # os.remove(img_file_path)  # single file
    # Alternative: Path objects from the Python 3.4+ pathlib module also expose these instance methods:
        # pathlib.Path.unlink()  # removes a file or symbolic link.
        # pathlib.Path.rmdir()   # removes an empty directory.

def dir_tree(startpath):
    # Thanks to
    # https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


    # TODO: Hint that this returns list data type:
def about_disk_space():
    statvfs = os.statvfs(".")
    # Convert to bytes, multiply by statvfs.f_frsize and divide for Gigabyte
    # representation:
    GB = 1000000
    disk_total = ((statvfs.f_frsize * statvfs.f_blocks) /
                  statvfs.f_frsize) / GB
    disk_free = ((statvfs.f_frsize * statvfs.f_bfree) / statvfs.f_frsize) / GB
    # disk_available = ((statvfs.f_frsize * statvfs.f_bavail ) / statvfs.f_frsize ) / GB
    disk_list = [disk_total, disk_free]
    return disk_list


    # This returns date object:
def file_creation_date(path_to_file, my_os_platform):
    """
    Get the datetime stamp that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    WARNING: Use of epoch time means resolution is to the seconds (not microseconds)
    """
    if path_to_file is None:
        if show_trace:
            print_trace("path_to_file="+path_to_file)
    print_trace("platform.system="+platform.system())
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def file_remove(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)  # deletes a directory and all its contents.

# TODO: Create, navigate to, and remove local working folders:


#### SECTION 08. Get pgm run env data:

def os_platform():
    platform_system = platform.system()
    print_trace("platform_system="+platform_system)
    if platform_system == "Darwin":
        my_platform = "macOS"
    elif platform_system == "linux" or platform_system == "linux2":
        my_platform = "Linux"
    elif platform_system == "win32":
        my_platform = "Windows"
    else:
        print_fail("platform_system="+platform_system+" is unknown!")
        exit(1)
    return my_platform


def macos_version_name(release_in):
    """ Returns the marketing name of macOS versions which are not available
        from the running macOS operating system.
    """
    # NOTE: Return value is a list!
    # This has to be updated every year, so perhaps put this in an external library so updated
    # gets loaded during each run.
    # Apple has a way of forcing users to upgrade, so this is used as an
    # example of coding.
    # FIXME: https://github.com/nexB/scancode-plugins/blob/main/etc/scripts/homebrew.py
    MACOS_VERSIONS = {
        '22.7': ['Next2024', 2024, '22'],
        '22.6': ['Next2023', 2023, '22'],
        '22.5': ['After Monterey', 2022, '22'],
        '21.1': ['Monterey', 2021, '21'],
        '11.1': ['Big Sur', 2020, '20'],
        '19.6': ['Catalina', 2019, '19'],
        '10.14': ['Mojave', 2018, '18'],
        '10.13': ['High Sierra', 2017, '17'],
        '10.12': ['Sierra', 2016, '16'],
        '10.11': ['El Capitan', 2015, '15'],
        '10.10': ['Yosemite', 2014, '14'],
        '10.0': ['Mavericks', 2013, '13'],
        '10.8': ['Mountain Lion', 2012, '12'],
        '10.7': ['Lion', 2011, '11'],
        '10.6': ['Snow Leopard', 2008, '10'],
        '10.5': ['Leopard', 2007, '10.5'],
        '10.4': ['Tiger', 2005, '10.4'],
        '10.3': ['Panther', 2004, '10.3'],
        '10.2': ['Jaguar', 2003, '10.2'],
        '10.1': ['Puma', 2002, '10.1'],
        '10.0': ['Cheetah', 2001, '10.0'],
    }
    # WRONG: On macOS Monterey, platform.mac_ver()[0]) returns "10.16", which is Big Sur and thus wrong.
    # See https://eclecticlight.co/2020/08/13/macos-version-numbering-isnt-so-simple/
    # and https://stackoverflow.com/questions/65290242/pythons-platform-mac-ver-reports-incorrect-macos-version/65402241
    # and https://docs.python.org/3/library/platform.html
    # So that is not a reliable way, especialy for Big Sur
    # import subprocess
    # p = subprocess.Popen("sw_vers", stdout=subprocess.PIPE)
    #result = p.communicate()[0]
    macos_platform_release=platform.release()
    # Alternately:
    release = '.'.join(release_in.split(".")[:2])  # ['10', '15', '7']
    macos_info = MACOS_VERSIONS[release]  # lookup for ['Monterey', 2021]
    print_trace("macos_info="+str(macos_info))
    print_trace("macos_platform_release="+macos_platform_release)
    return macos_platform_release

my_os_platform = os_platform()  # defined above.
print_trace("my_os_platform="+my_os_platform)

#my_os_platform=localize_blob("version")
my_os_version = platform.release()  # platform.mac_ver()[0] can be wrong
print_trace("my_os_version="+my_os_version)
#Alternately:
# my_os_version_name = macos_version_name(my_os_version)
# print_info("my_os_version_name="+my_os_version_name)

my_os_process = str(os.getpid())
print_trace("my_os_process="+my_os_process)

    #print("*** %s %s=%s" % (my_os_platform, localize_blob("version"), platform.mac_ver()[0]),end=" ")
    #print("%s process ID=%s" % ( my_os_name, os.getpid() ))

    # or socket.gethostname()
my_platform_node = platform.node()
print_trace("my_platform_node="+my_platform_node)

my_os_uname = str(os.uname())
print_trace("my_os_uname="+my_os_uname)
    # MacOS version=%s 10.14.6 # posix.uname_result(sysname='Darwin',
    # nodename='NYC-192850-C02Z70CMLVDT', release='18.7.0', version='Darwin
    # Kernel Version 18.7.0: Thu Jan 23 06:52:12 PST 2020;
    # root:xnu-4903.278.25~1/RELEASE_X86_64', machine='x86_64')

pwuid_shell=pwd.getpwuid(os.getuid()).pw_shell     # like "/bin/zsh"
   # preferred over os.getuid())[0]
   # Instead of: import psutil
   # machine_uid_pw_name = psutil.Process().username()
print_trace("pwuid_shell="+pwuid_shell)

# Obtain machine login name:
# This handles situation when user is in su mode. 
   # See https://docs.python.org/3/library/pwd.html
pwuid_gid=pwd.getpwuid(os.getuid()).pw_gid         # Group number datatype
print_trace("pwuid_gid="+str(pwuid_gid)+" (group ID number)")

pwuid_uid=pwd.getpwuid(os.getuid()).pw_uid
print_trace("pwuid_uid="+str(pwuid_uid)+" (user ID number)")

pwuid_name=pwd.getpwuid(os.getuid()).pw_name
print_trace("pwuid_name="+pwuid_name)

pwuid_dir=pwd.getpwuid(os.getuid()).pw_dir         # like "/Users/johndoe"
print_trace("pwuid_dir="+pwuid_dir)

# See https://wilsonmar.github.io/python-samples#run_env
user_home_dir_path = str(Path.home())   # example: /users/wilson_mar
print_trace("user_home_dir_path="+user_home_dir_path)
   # the . in .secrets tells Linux that it should be a hidden file.

# Several ways to obtain:
# See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
# this_pgm_name = sys.argv[0]                     # = ./az-status.py
# this_pgm_name = os.path.basename(sys.argv[0])   # = az-status.py
# this_pgm_name = os.path.basename(__file__)      # = az-status.py
# this_pgm_path = os.path.realpath(sys.argv[0])   # = az-status.py
# Used by display_run_stats() at bottom:
this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
print_trace("this_pgm_name="+this_pgm_name)

this_pgm_version = __version__
    # Adapted from https://www.python-course.eu/python3_formatted_output.php
print_trace("this_pgm__version__="+this_pgm_version)

this_pgm_os_path = os.path.realpath(sys.argv[0])
print_trace("this_pgm_os_path="+this_pgm_os_path)
   # Example: "/Users/wilsonmar/github-wilsonmar/azure-quickly/az-status/az-status.py"

site_packages_path=site.getsitepackages()[0]
print_trace("site_packages_path="+site_packages_path)

this_pgm_last_modified_epoch=os.path.getmtime(this_pgm_os_path)
print_trace("this_pgm_last_modified_epoch="+str(this_pgm_last_modified_epoch))

this_pgm_last_modified_datetime = _datetime.datetime.fromtimestamp(this_pgm_last_modified_epoch)  
print_trace("this_pgm_last_modified_datetime="+str(this_pgm_last_modified_datetime)+" (UTC/GMT)")
    # Default like: 2021-11-20 07:59:44.412845  (with space between date & time)

python_ver=platform.python_version()
    # 3.9.16
print_trace("python_ver="+python_ver)

def no_newlines(in_string):
    """ Strip new line from in_string
    """
    return ''.join(in_string.splitlines())

python_version=no_newlines(sys.version) 
    # 3.9.16 (main, Dec  7 2022, 10:16:11) [Clang 14.0.0 (clang-1400.0.29.202)] 
    # 3.8.3 (default, Jul 2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
print_trace("python_version="+python_version)

print_trace("python_version_info="+str(sys.version_info))
    # Same as on command line: python -c "print(__import__('sys').version)"
    # 2.7.16 (default, Mar 25 2021, 03:11:28)
    # [GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc-
 
if sys.version_info.major == 3 and sys.version_info.minor <= 6:
        # major, minor, micro, release level, and serial: for sys.version_info.major, etc.
        # Version info sys.version_info(major=3, minor=7, micro=6,
        # releaselevel='final', serial=0)
    print_fail("Python 3.6 or higher is required for this program. Please upgrade.")
    sys.exit(1)

venv_base_prefix = sys.base_prefix 
venv_prefix = sys.prefix
if venv_base_prefix == venv_prefix :
    print_trace("venv at " + venv_base_prefix)
else:
    print_fail("venv is different from venv_prefix "+venv_prefix)
    
print_trace("__name__="+__name__)


# TODO: Make this function for call before & after run:
#    disk_list = about_disk_space()
#    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
#    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
    # left-to-right order of fields are re-arranged from the function's output.


#### SECTION 09.  Obtain run control data from .env file in the user's $HOME folder

def open_env_file(env_file) -> str:
    """
    Return a Boolean obtained from .env file based on key provided.
    """
    # TODO: Check to see if the file is available. Download sample file
    # IN CLI: pip install python-dotenv
    # from dotenv import load_dotenv
    # reference:
    print_info("env_file="+env_file)
    print_info("user_home_dir_path="+user_home_dir_path)
    global_env_path = user_home_dir_path +"/"+ env_file  # concatenate path
    print_info("global_env_path="+global_env_path)
    # "az-status.env" from GitHub to the user's $HOME folder for

    # text_to_print = "global_env_path=" + str(global_env_path)
    global_env_path_time = file_creation_date(global_env_path, my_os_platform)
    dt = _datetime.datetime.utcfromtimestamp( global_env_path_time )
    iso_format = dt.strftime('%A %d %b %Y %I:%M:%S %p Z')  # Z = UTC with no time zone
    print_verbose( "created " + iso_format )
    
    # FIXME: Check if library is loaded:
    # load_dotenv(global_env_path)

    # Get globals defined on every run: 
    # These should be listed in same order as in the .env file:

    # PROTIP: Don't change the system's locale setting within a Python program because
    # locale is global and affects other applications.
    return True

def get_from_env_file(key_in) -> str:
    """
    Return a string obtained from .env file based on key provided.
    Used instead of os.environ.get('SOME_URL')
    """
    # TODO: Check if file is available:
    value = os.environ.get(key_in)  # built-in function
    if not value:
        print_warning(key_in +" not found in .env file "+ env_file)
        return None
    else:
        # del os.environ[key_in]
        os.environ[key_in] = value
        # TODO: If key_in name contains "secret", print it as a secret:
        print_trace(key_in +"=\""+ value +"\"")
        return value

if True:  # always execute
    print_heading("show_env trace:")

    env_file = 'az-status.env'  # internal default if not provided in parms.
    if not use_env_file:
        print_warning("NOT use_env_file")
    else:
        use_env_file = open_env_file(env_file)

    # NOTE: Country code can come from IP Address lookup
    # "US"      # For use in whether to use metric
    my_country_from_env = get_from_env_file('MY_COUNTRY')
    if my_country_from_env:
        my_country = my_country_from_env
    else:
        my_country = "US"
    print_trace("my_country="+my_country)

    # CAUTION: PROTIP: LOCALE values are different on Windows than Linux/MacOS
    # "ar_EG", "ja_JP", "zh_CN", "zh_TW", "hi" (Hindi), "sv_SE" #swedish
    my_locale="en_US"
    locale_from_env = get_from_env_file('LOCALE')  # for translation
    if locale_from_env:
        my_locale = locale_from_env
    else:
        my_locale = "en_US"
    print_trace("my_locale="+my_locale)

    my_encoding_from_env = get_from_env_file('MY_ENCODING')  # "UTF-8"
    if my_encoding_from_env:
        my_encoding = my_encoding_from_env
    else:
        my_encoding = "UTF-8"
    print_trace("my_encoding="+my_encoding)

    my_tz_name_from_env = get_from_env_file('MY_TIMEZONE_NAME')
    if my_tz_name_from_env:
        my_tz_name = my_tz_name_from_env
    else:
        # Get time zone code from local operating system:
        # import datetime  # for Python 3.6+
        my_tz_name = str(_datetime.datetime.utcnow().astimezone().tzinfo)
            # _datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
            # = "MST" for U.S. Mountain Standard Time, or 'Asia/Kolkata'
    print_trace("my_tz_name="+my_tz_name)

    my_zip_code_from_env     = get_from_env_file('MY_ZIP_CODE')   # "90210"  # use to lookup country, US state, long/lat, etc.
    if my_zip_code_from_env: 
        my_zip_code = my_zip_code_from_env
    else: 
        my_zip_code = "90210"   # Beverly Hills, CA, for demo usage.
    print_trace("my_zip_code="+my_zip_code)

    my_longitude_from_env = get_from_env_file('MY_LONGITUDE')
    if my_longitude_from_env:
        my_longitude = my_longitude_from_env
    else:
        my_longitude = "104.322"
    print_trace("my_longitude="+my_longitude)

    my_latitude_from_env = get_from_env_file('MY_LATITUDE')
    if my_latitude_from_env:
        my_latitude = my_latitude_from_env
    else:
        my_latitude = "34.123"
    print_trace("my_latitude="+my_latitude)

    my_curency_from_env = get_from_env_file('MY_CURRENCY')
    if my_curency_from_env:
        my_currency = my_curency_from_env
    else:
        my_currency = "USD"
    print_trace("my_currency="+my_currency)

    my_date_format_from_env = get_from_env_file('MY_DATE_FORMAT')
    if my_date_format_from_env:
        my_date_format = my_date_format_from_env
    else:
        my_date_format = "%A %d %b %Y %I:%M:%S %p %Z %z"
        # TODO: Override default date format based on country
            # Swedish dates are like 2014-11-14 instead of 11/14/2014.
            # https://www.wikiwand.com/en/Date_format_by_country shows only 7 Order style formats
            # See https://wilsonmar.github.io/python-coding/#DurationCalcs
        if load_country_db:
            country_info_dict=get_data_from_country_db(my_country)
            if country_info_dict:  # TODO:
                print(country_info_dict)  # "D/M/Y" 
    print_trace("my_date_format="+my_date_format)
        

#### SECTION 10. Manage sqliteDB countryDB reference DB

# CAUTION: Avoid printing api_key value and other secrets to console or logs.

# CAUTION: Leaving secrets anywhere on a laptop is dangerous. One click on a malicious website and it can be stolen.
# It's safer to use a cloud vault such as Amazon KMS, Azure, Hashicorp Vault after signing in.
# https://blog.gruntwork.io/a-comprehensive-guide-to-managing-secrets-in-your-terraform-code-1d586955ace1#bebe
# https://vault-cli.readthedocs.io/en/latest/discussions.html#why-not-vault-hvac-or-hvac-cli

def check_sqlite_header(sqlite3_db_name):
    
    # Check if first 100 bytes of path identifies itself as sqlite3 in header:
    # From https://stackoverflow.com/questions/12932607/how-to-check-if-a-sqlite3-database-exists-in-python
    f = open(sqlite3_db_name, "rx")
    ima = f.read(16).encode('hex')
    f.close()
    #see http://www.sqlite.org/fileformat.html#database_header magic header string
    if ima != "53514c69746520666f726d6174203300": 
        return 3
    else:
        return None

def open_sqlite3_db(sqlite3_db_name):

    cwd = os.getcwd()  # Get current working directory
    print_verbose("Current working directory: {0}".format(cwd))

    import sqlite3
    try:
        # Try to see if db file exists (can be opened) in operating system:
        with open(cwd +"/"+ sqlite3_db_name): pass
        # WARNING: Use SQLite rather than operating system commands to delete db.
    except IOError:
        print_verbose("Create SQLite database "+ sqlite3_db_name)    

    try:  # Connect to SQLite: https://zetcode.com/db/sqlitepythontutorial/
        conn = sqlite3.connect(sqlite3_db_name)
        cursor = conn.cursor()

        sqlite_select_Query = "select sqlite_version();"
        cursor.execute(sqlite_select_Query)
        record = cursor.fetchall()
        print_verbose("SQLite database "+ sqlite3_db_name+" version: "+ str(record) )

        # See if table can be accessed by querying the built-in sqlite_master table within every db:
        cursor.execute('''SELECT name FROM sqlite_master 
            WHERE type='table' AND name='table_name';''')
        print(check_sqlite_header(sqlite3_db_name))
        print(cursor.fetchall())

        if cursor.fetchone()[0]==1 :  #if the count is 1, then table exists:
            print_trace('Table exists.')
            return cursor  # FIXME: TypeError: 'NoneType' object is not subscriptable
        else:
            print_trace('Table does not exist.')
            # Create db if not there:
            try:
                create_country_table_query = '''CREATE TABLE Country_data (
                                        country_name TEXT NOT NULL,
                                        country_id2 INTEGER PRIMARY KEY,
                                        country_id3 INTEGER SECONDARY KEY,
                                        country_population REAL,
                                        country_area_km2 REAL,
                                        country_gdp REAL);'''
                conn.execute(create_country_table_query)
                conn.commit()
                print_trace("SQLite table Country_data created.")
                return cursor
            except sqlite3 as error:
                print_fail("SQLite database "+ sqlite3_db_name+" error: " + str(error))
                return None
    except IOError as error:
        # FIXME: print_fail("SQLite database "+ sqlite3_db_name+" error: " + str(error))
        print_fail("SQLite database "+ sqlite3_db_name+" error")
        return None
    
# TODO: def get_dtformat_from_locale():

def get_data_from_country_db(country_id):
    # Load Country SQLite in-memory database for date-time formats = load_country_db
    # TODO: Delete database if requested.
    print_heading("load_country_db")

    sqlite3_db_name="SQLite3_country.db"
    conn = open_sqlite3_db(sqlite3_db_name)
    if load_country_db:
        try:
            cursor.execute('''SELECT name FROM sqlite_master 
                WHERE type='table' AND name='table_name';''')
            if cursor.fetchone()[0]==1 :  #if the count is 1, then table exists:
                print_trace('Table exists.')
                return cursor
            else:
                print_trace('Do main table tasks.')
                # https://towardsdatascience.com/python-sqlite-tutorial-the-ultimate-guide-fdcb8d7a4f30
                # https://datagy.io/sql-beginners-tutorial/

                # TODO: Load country data from csv file 
                # Alternately (Excel vis=a OpenPyXL):
                # more_users = [('00003', 'Peter', 'Parker', 'Male'), ('00004', 'Bruce', 'Wayne', 'male')]
                # cur.execute("INSERT INTO users VALUES(?, ?, ?, ?);", user)
                # conn.commit()

                # TODO: Create indexes
                # cur.execute("""SELECT *, users.fname, users.lname FROM orders LEFT JOIN users ON users.userid=orders.userid;""")
                # print(cur.fetchall())
            
                # TODO: Lookup index 1 - 2 char country for Linux (highest priority)
                # TODO: Lookup index 2 - 3 char country for Windows (medium priority)
                # TODO: Lookup index 3 - Phone code (low priority)

                # TODO: Retrieve date_time, phone, population, land, GDP

        except IOError as error:
            print_fail("SQLite database "+ sqlite3_db_name+" error: " + str(error))
            return None
        finally:
            if conn:
                conn.close()
                print_trace("SQLite database "+ sqlite3_db_name+" connection closed.")
        
        locale_dict = dict()
        locale_dict['en_US'] = 'D/M/Y'  # HARD-CODING FOR DEBUGGING
        return locale_dict   # {'en_US': 'D/M/Y'}


#### SECTION 11. Localization (to translate text to the specified locale)

# internationalization according to localization setting:
def format_epoch_datetime(date_in):
    return (time.strftime(my_date_format, time.localtime(date_in)))

# internationalization according to localization setting:
def format_number(number):
    return ("{:,}".format(number))

# Use user's default settings by setting as blank:
locale.setlocale(locale.LC_ALL, '')
# Use current setting:
locale.setlocale(locale.LC_ALL, None)

# TODO: if value from parsing command parameters, override value from env:
if my_locale: # locale_from_env:  # not empty:
    my_locale = locale_from_env
else:  # fall back # from operating system:
    my_locale = locale.getlocale()

if not my_locale:
    my_locale = "en_US"  # hard-coded default such as "en_US"

try:
    locale.setlocale(locale.LC_TIME, my_locale)
except BaseException:
    if show_fail:
        print(
            f'***{bcolors.FAIL} Ignoring error in setting OS LOCALE \"{my_locale}\"!{bcolors.RESET}')

# for lang in locale.locale_alias.values():  # print all locales with "UTF-8"
#    print(lang)

# Preparations for translation:
    # pip install textblob  # translates text using API calls to Google Translate.
    # python -m textblob.download_corpora


def localize_blob(byte_array_in):
    if not localize_text:
        return byte_array_in

    if type(byte_array_in) is not str:
        print(f'*** \"{byte_array_in}\"={type(byte_array_in)} ')
        return byte_array_in
    else:
        blob = TextBlob(byte_array_in)
    try:
        translated = blob.translate(to=my_locale)  # such as 'de_DE'
    except BaseException:
        translated = byte_array_in
    return translated
    # https://textblob.readthedocs.io/en/dev/ can also perform natural language processing (NLP) tasks such as
    # part-of-speech tagging, noun phrase extraction, sentiment analysis,
    # classification, translation, and more.


    # TODO: PROTIP: Provide hint that data type is a time object:
def creation_date(path_to_file):
    print("path_to_file type="+type(path_to_file))
    """
    Requires import platform, import os, from stat import *
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime


def part_of_day_greeting():
    from datetime import datetime
    current_hour = datetime.now().hour
    if current_hour < 12:
        part_of_day = localize_blob('Good morning!')
    elif 12 <= current_hour < 17:
        part_of_day = localize_blob('Good afternoon!')
    else:
        part_of_day = localize_blob('Good evening!')
    return part_of_day


def verify_yes_no_manually(question, default='no'):
    # Adapted from https://gist.github.com/garrettdreyfus/8153571
    if not verify_manually:  # global
        return default
    else:
        if default is None:
            prompt = " [y/n] "
        elif default == 'yes':
            prompt = " [Y/n] "
        elif default == 'no':
            prompt = " [y/N] "
        else:
            raise ValueError(
                f'*** {localize_blob("Unknown setting")} {localize_blob("default")} \"{default}\" ')
        while True:  # Keep asking:
            try:
                resp = input(question + prompt).strip().lower()
                if default is not None and resp == '':
                    return default == 'yes'
                else:
                    return distutils.util.strtobool(
                        resp)  # QUESTION: what is this?
            except ValueError:
                print(
                    f'*** {localize_blob("Please respond")}: "yes" or "y" or "no" or "n".\n')


if localize_text:

    # if env_locale != my_locale[0] : # 'en_US'
    #   print("error")
    if show_warning:
       print(f'***{bcolors.WARNING} global_env_path LOCALE \'{env_locale}\' {localize_blob("overrides")} OS LOCALE {my_locale}{bcolors.RESET}')

    # NOTE: print(f'*** Date: {locale.atof("32,824.23")} ')
    # File "/Users/wilsonmar/miniconda3/envs/py3k/lib/python3.8/locale.py", line 326, in atof
    # return func(delocalize(string))
    # ValueError: could not convert string to float: '32.824.23'

    if my_encoding_from_env:  # not empty:
       my_encoding = my_encoding_from_env
    else:  # fall back to hard-coded default:
       my_encoding = "utf-8"  # default: or "cp860" or "latin" or "ascii"


"""if show_trace == True:
    # Output all locales:
    # See https://docs.python.org/3/library/locale.html#locale.localeconv
    for key, value in locale.localeconv().items():
        print("*** %s: %s" % (key, value))
"""

if show_dates:  # TODO: Move this to the end of the program source code!
    print_heading("show_dates using localized format:")
    my_local_time = time.localtime()
    
    print_trace("pgm_start_timestamp="+str(pgm_start_timestamp))
    print_trace("pgm_start_epoch_timestamp="+str(pgm_start_epoch_timestamp))  # like 1685264269.421101
    time_val = time.localtime(pgm_start_epoch_timestamp)
    print_trace("pgm_start_epoch_timestruct=" + str( time_val ) )

    if my_date_format == "":  # variable contains a value:
        iso_format = '%A %Y-%b-%d %I:%M:%S %p'
        print_warning("Using default date format="+iso_format)
        my_date_format = iso_format

    # Local time with specified timezone name and offset:
    pgm_start_epoch_time = _datetime.datetime.fromtimestamp(pgm_start_epoch_timestamp)  
    dt = _datetime.datetime.utcfromtimestamp(pgm_start_epoch_timestamp)
    pgm_start_epoch_time=dt.strftime(my_date_format)  # Z = UTC with no time zone
    print_trace("pgm_start_epoch_time="+str(pgm_start_epoch_time))
    
    current_local_time = time.strftime(my_date_format, my_local_time)
    # See https://www.youtube.com/watch?v=r1Iv4d6CO2Q&list=PL98qAXLA6afuh50qD2MdAj3ofYjZR_Phn&t=50s
    print_trace("current_local_time=  "+current_local_time)  
    print_trace("my_local_time="+str(my_local_time))
    # Example: Friday 10 Dec 2021 11:59:25 PM MST -0600
    
    username_greeting = str( my_tz_name ) +" "+ part_of_day_greeting()   # +" by username: "+ global_username
    print_verbose(username_greeting)
    
    #    dt = _datetime.datetime.utcfromtimestamp(pgm_start_epoch_timestamp)
    #    # NOTE: ISO 8601 and RFC 3339 '%Y-%m-%d %H:%M:%S' or '%Y-%m-%dT%H:%M:%S'
    #    iso_format = '%A %Y-%b-%d %I:%M:%S %p Z(UTC/GMT)'
    #    current_local_time=dt.strftime(iso_format)  # Z = UTC with no time zone
    #    print_trace("current_local_time="+current_local_time)  
        
    if use_pytz_datetime:
        # import pytz
        start_UTC_time = pytz.utc   # get the standard UTC time
        datetime_utc = datetime.now(start_UTC_time)
        print_trace("pgm_start_time_pytz= "+datetime_utc.strftime(my_date_format))

        # Example of hard-coded time zone: 
        # IST = pytz.timezone('Asia/Kolkata')  # Specify a location in India:
        IST = pytz.timezone('Asia/Kolkata')  # Specify a location in India:
        datetime_utc = datetime.now(IST)   # from above
        print_trace("current time at IST= "+datetime_utc.strftime(my_date_format)+" ("+str(IST)+") India")
        # print(str(datetime_utc.strftime(my_date_format))+" India")

    """
    # Get a UTC tzinfo object – by calling tz.tzutc():
    # Based on: from dateutil import tz
    tz.tzutc()
    # Get offset 0 by calling the utcoffset() method with a UTC datetime object:

    #from datetime import timezone
    #import datetime
    dt = _datetime.datetime.now(timezone.utc)  # returns number of seconds since the epoch.
    #dt = datetime.datetime.now()  # returns number of seconds since the epoch.
    # use tzinfo class to convert datetime to UTC:
    utc_time = dt.replace(tzinfo=timezone.utc)
    print(utc_time)
    # Use the timestamp() to convert the datetime object, in UTC, to get the UTC timestamp:
    utc_timestamp = utc_time.timestamp()
    print_verbose("Epoch utc_timestamp now: "+ str(utc_timestamp))
    # Can't print(utc_timestamp.strftime(my_date_format))  # AttributeError: 'float' object has no attribute 'strftime'

    import datetime
    print("tz.tzutc now: "+ str(tz.tzutc().utcoffset(datetime.datetime.utcnow())) )
    # datetime.timedelta(0)
    """


#### SECTION 12. Generate Hash (UUID/GUID) from a file    = gen_hash

def gen_hash_text(gen_hash_method, byte_array_in):
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # import hashlib  # https://docs.python.org/3/library/hashlib.html
    # From among hashlib.algorithms_available
    if gen_hash_method == "SHA1":
        m = hashlib.sha1()
    elif gen_hash_method == "SHA224":
        m = hashlib.sha224()
    elif gen_hash_method == "SHA256":
        m = hashlib.sha256()
    elif gen_hash_method == "SHA384":
        m = hashlib.sha384()
    elif gen_hash_method == "SHA512":  # (defined in FIPS 180-2)
        m = hashlib.sha512()
    # See https://www.wikiwand.com/en/Cryptographic_hash_function#/Cryptographic_hash_algorithms
    # SHA224, 224 bits (28 bytes); SHA-256, 32 bytes; SHA-384, 48 bytes; and
    # SHA-512, 64 bytes.

    m.update(byte_array_in)
    if show_verbose:
        print(
            f'*** {gen_hash_method} {m.block_size}-bit {m.digest_size}-hexbytes {m.digest_size*2}-characters')
        # print(f'*** digest={m.digest()} ')

    return m.hexdigest()


# TODO: Merge into a single function by looking at the type of input.
def gen_hash_file(gen_hash_method, file_in):
    # A hash is a fixed length one way string from input data. Change of even one bit would change the hash.
    # A hash cannot be converted back to the input data (unlike encryption).
    # https://stackoverflow.com/questions/22058048/hashing-a-file-in-python

    # import hashlib  # https://docs.python.org/3/library/hashlib.html
    # From among hashlib.algorithms_available:
    if gen_hash_method == "SHA1":
        m = hashlib.sha1()
    elif gen_hash_method == "SHA224":
        m = hashlib.sha224()
    elif gen_hash_method == "SHA256":
        m = hashlib.sha256()
    elif gen_hash_method == "SHA384":
        m = hashlib.sha384()
    elif gen_hash_method == "SHA512":  # (defined in FIPS 180-2)
        m = hashlib.sha512()
    # See https://www.wikiwand.com/en/Cryptographic_hash_function#/Cryptographic_hash_algorithms
    # SHA224, 224 bits (28 bytes); SHA-256, 32 bytes; SHA-384, 48 bytes; and
    # SHA-512, 64 bytes.

    # See https://death.andgravity.com/hashlib-buffer-required
    # to read files in 64kb chunks rather than sucking the life out of your
    # memory.
    BUF_SIZE = 65536
    # https://www.quickprogrammingtips.com/python/how-to-calculate-sha256-hash-of-a-file-in-python.html
    with open(file_in, 'rb') as f:   # or sys.argv[1]
        for byte_block in iter(lambda: f.read(BUF_SIZE), b""):
            m.update(byte_block)
    if show_verbose:
        print(
            f'*** {gen_hash_method} {m.block_size}-bit {m.digest_size}-hexbytes {m.digest_size*2}-characters')
        # print(f'*** digest={m.digest()} ')

    return m.hexdigest()


class TestGenHash(unittest.TestCase):
    def test_gen_hash(self):

        if gen_hash:
            print_heading("gen_hash")

            # Making each image file name unique ensures that changes in the file resets cache of previous version.
            # UUID = Universally Unique Identifier, which Microsoft calls Globally Unique Identifier or GUID.
            # UUIDs are supposed to be unique in time (stamp) and space (IP address or MAC address).
            # UUIDs are always 128-bit, but can be formatted with dashes or into 32 hex bits.
            # Adapted from https://docs.python.org/3/library/uuid.html
            # CAUTION: uuid1() compromises privacy since it contains the computer’s
            # network IP address.

            # 87509061370279318 portion (sortable)
            if img_file_naming_method == "uuid4time":
                x = uuid.uuid4()
                # cbceb48b-7c97-4b46-b5f7-b55b3d09c2e4
                print(f'*** uuid.uuid4()={x} ')
                print(f'*** x.time={x.time} ')   # 87509061370279318
                # sorted(ss, key= lambda x: x[0].time)
                # CAUTION: Do not use the time portion by itself from
                # {uuid.uuid1().time} as it doesn't have place.

            elif img_file_naming_method == "uuid4":  # with dashes like 5ac79987-9654-4c0a-b70a-46d57cb0d4b9
                x = uuid.uuid4()
                # cbceb48b-7c97-4b46-b5f7-b55b3d09c2e4
                print(f'*** {uuid.uuid4()} ')

            # d42277a3bfcd4f019699d4094c457634 (not sortable)
            elif img_file_naming_method == "uuid4hex":
                x = uuid.uuid4()
                print(f'*** uuid.uuid1() -> x.hex={x.hex} ')

            # See
            # http://coders-errand.com/hash-functions-for-smart-contracts-part-3/


#### SECTION 12. Setup logging

if show_logging:
   print_heading("show_logging")

    # Confirm manually: https://portal.azure.com/#view/Microsoft_Azure_Billing/SubscriptionsBlade
    # https://azure.github.io/azure-sdk/releases/latest/mgmt/python.html
   logger = logging.getLogger(__name__)
   print_info("logger="+str(logger))



#### SECTION 9.2 Generate a random Salt

DEFAULT_ENTROPY = 32  # bytes in string to return, by default

def token_urlsafe(nbytes=None):
    tok = token_urlsafe(nbytes)
    # 'Drmhze6EPcv0fN_81Bj-nA'
    return base64.urlsafe_b64encode(tok).rstrip(b'=').decode('ascii')


if gen_salt:
    # “full entropy” (i.e. 128-bit uniformly random value)
    print_heading("gen_salt")

    # Based on https://github.com/python/cpython/blob/3.6/Lib/secrets.py
    #     tok=token_urlsafe(16)
    # tok=token_bytes(nbytes=None)
    # 'Drmhze6EPcv0fN_81Bj-nA'
    #print(f' *** tok{tok} ')

    from random import SystemRandom
    cryptogen = SystemRandom()
    x = [cryptogen.randrange(3) for i in range(20)]  # random ints in range(3)
    # [2, 2, 2, 2, 1, 2, 1, 2, 1, 0, 0, 1, 1, 0, 0, 2, 0, 0, 0, 0]
    print(f'    {x}')

    if show_heading:
        print(
            f'*** gen_salt: [cryptogen.random() for i in range(3)]  # random floats in [0., 1.)')
    y = [cryptogen.random() for i in range(3)]  # random floats in [0., 1.)
    # [0.2710009745425236, 0.016722063038868695, 0.8207742461236148]
    print(f'    {y}')

    #print(f'*** {salt_size} salt={password_salt} ')


#### SECTION 9.3 Generate random percent of 100:

if gen_1_in_100:
    print_heading("gen_1_in_100")

    print("*** 5 Random number between 1 and 100:")
    import random
    print(range(5))
    for x in range(5):
        # between 1 and 100 (1 less than 101)
        print(random.randint(1, 101), end=" ")
        # see
        # https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b311-random


#### SECTION 9.4 Convert Roman to Decimal for use of case

# From
# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch03s24.html
def int_to_roman(input):
    # Convert a input year to a Roman numeral

    if isinstance(input, str):
        input = int(input)

    # FIXME: if not isinstance(input, type(1)):
#        raise TypeError, "expected integer, got %s" % type(input)
#    if not 0 < input < 4000:
#        raise ValueError, "Argument must be between 1 and 3999"
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = (
        'M',
        'CM',
        'D',
        'CD',
        'C',
        'XC',
        'L',
        'XL',
        'X',
        'IX',
        'V',
        'IV',
        'I')
    result = []
    for i in range(len(ints)):
        # FIXME: TypeError: unsupported operand type(s) for /: 'str' and 'int'
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)


def roman_to_int(roman_str_in):
    # Convert a Roman numeral to an integer

    if not isinstance(roman_str_in, type("")):
        # FIXME: TypeError: unsupported operand type(s) for /: 'str' and 'int'
        #        raise TypeError, "expected string, got %s" % type(input)
        print(f'***FAIL: Input \"{roman_str_in}\" not a string')
        return
    roman_str_in = roman_str_in.upper()
    nums = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    sum = 0
    for i in range(len(roman_str_in)):
        try:
            value = nums[roman_str_in[i]]
            # If the next place holds a larger number, this value is negative
            if i + 1 < len(roman_str_in) and nums[roman_str_in[i + 1]] > value:
                sum -= value
            else:
                sum += value
        except KeyError:
            print("*** FIXME: whatever")
            # FIXME:         raise ValueError, 'input is not a valid Roman numeral: %s' % input
    # easiest test for validity...
    if int_to_roman(sum) == roman_str_in:
        return sum


if process_romans:
    mylist = ["2021", "xx"]
    my_number = mylist[0]  # "2021"
    my_roman = int_to_roman(my_number)
    print(f'*** {my_number} => {my_roman} ')

    # FIXME: my_roman=2021 #"MMXXI"  # = 2021
    # my_number=roman_to_int( my_roman )
    # print(f'*** {my_roman} => {my_number} ')


"""
# FIXME:
class RomanToDecimal(object):
    # Use the same dictionary for two-way conversion in one function
    # from https://www.tutorialspoint.com/roman-to-integer-in-python
    def romanToInt(self, s):
        # :type s: str
        # :rtype: int
        roman = {
            'I': 1,
            'V': 5,
            'X': 10,
            'L': 50,
            'C': 100,
            'D': 500,
            'M': 1000,
            'IV': 4,
            'IX': 9,
            'XL': 40,
            'XC': 90,
            'CD': 400,
            'CM': 900}
        i = 0
        num = 0
        while i < len(s):
            if i + 1 < len(s) and s[i:i + 2] in roman:
                num += roman[s[i:i + 2]]
                i += 2
            else:
                # print(i)
                num += roman[s[i]]
                i += 1
        return num
"""

if process_romans:
    print_heading("process_romans")

    my_roman = "MMXXI"  # "MMXXI" = 2021
    ob1 = roman_to_int(my_roman)
    # my_number = ob1.romanToInt(my_roman)
    print(f'*** process_romans: roman_to_int: {my_roman} => {my_number} ')

    my_roman_num = 2021  # = "MMXXI"
    ob1 = int_to_roman(my_roman_num)
    print(f'*** process_romans: int_to_roman: {my_number} ==> {my_roman} ')

    # Verify online at
    # https://www.calculatorsoup.com/calculators/conversions/roman-numeral-converter.php


#### SECTION 9.5 Generate JSON Web Token          = gen_jwt

if gen_jwt:
    print_heading("gen_jwt")
    # import jwt
    jwt_some = "something"
    jwt_payload = "my payload"
    encoded_jwt = jwt.encode({jwt_some: jwt_payload},
                             "secret", algorithm="HS256")
    print(f'*** encoded_jwt={encoded_jwt} ')
    # A
    # eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzb21lIjoicGF5bG9hZCJ9.Joh1R2dYzkRvDkqv3sygm5YyK8Gi4ShZqbhK2gxcs2U
    response = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    # {'some': 'payload'}
    print(f'*** response={response} ')


#### SECTION 9.6 Generate Lotto using random range    = gen_lotto_num

def gen_lotto_num():
    lotto_numbers = ""
    for x in range(5):
        # (1 more than 52 due to no 0)
        lotto_numbers = lotto_numbers + str(random.randint(1, 53)) + " "
    lotto_numbers = lotto_numbers + str(random.randint(1, 11))
    return lotto_numbers

    # set_val={"1","2","3","4","5"}
    # str_val = " ".join(set_val)  #
    # https://appdividend.com/2020/12/29/how-to-convert-python-set-to-string/


class TestGenLotto(unittest.TestCase):
    def test_gen_lotto_num(self):

        if gen_lotto:
            print_heading("gen_lotto")

            print_verbose(
                "Lotto America: 5 lucky numbers between 1 and 52 and 1 Star number between 1 and 10:")
            lotto_numbers = gen_lotto_num()
            # Based on https://www.lottoamerica.com/numbers/montana
            print_info(lotto_numbers)  # such as "17 45 40 34 15 4" (6 numbers)

    # https://www.calottery.com/draw-games/superlotto-plus#section-content-2-3


#### SECTION 9.7 Generate Lotto using random range    = gen_magic_8ball


def do_gen_magic_8ball():
    """This shows use of case statements to return a random number."""
    # Adapted from https://www.pythonforbeginners.com/code/magic-8-ball-written-in-python
    # import sys
    # import random
    while True:  # loop until Enter is pressed to quit.
        question = input(
            "Type a question for the magic 8-ball: (press enter to quit):")
        answer = random.randint(1, 8)  # Random number between 1 and 8
        if question == "":
            sys.exit()
        elif int(answer) == 1:
            print(localize_blob("1. It is certain"))
        elif int(answer) == 2:
            print(localize_blob("2. Outlook good"))
        elif int(answer) == 3:
            print(localize_blob("3. You may rely on it"))
        elif int(answer) == 4:
            print(localize_blob("4. Ask again later"))
        elif int(answer) == 5:
            print(localize_blob("5. Concentrate and ask again"))
        elif int(answer) == 6:
            print(localize_blob("6. Reply hazy, try again"))
        elif int(answer) == 7:
            print(localize_blob("7. My reply is no"))
        elif int(answer) == 8:
            print(localize_blob("8. My sources say no"))
        elif int(answer) == _:
            print("magic_8ball programming error.")
    """
        match str(answer):  # Wait until Python 3.10+ to use this
        case 1:
            print(localize_blob("It is certain"))
        case 2:
            print(localize_blob("Outlook good"))
        case 3:
            print(localize_blob("You may rely on it"))
        case 4:
            print(localize_blob("Ask again later"))
        case 5:
            print(localize_blob("Concentrate and ask again"))
        case 6:
            print(localize_blob("Reply hazy, try again"))
        case 7:
            print(localize_blob("My reply is no"))
        case 8:
            print(localize_blob("My sources say no"))
        case _:
            print("magic_8ball programming error.")
        # Loop
    """


class TestGen8Ball(unittest.TestCase):
    def test_gen_magic_8ball(self):

        if gen_magic_8ball:
            print_heading("gen_magic_8ball")

            do_gen_magic_8ball()

            # Extension TODO: Execute many times to see distribution of the
            # random number generated?



#### SECTION 9.8 Generate Fibonacci to compare recursion vs memoization locally and in Redis:

# alternative:
# https://github.com/samgh/DynamicProgrammingEbook/blob/master/python/Fibonacci.py

class Fibonacci(object):

    def fibonacci_recursive(n):
        """Calculate value of n-th Fibonacci sequence using brute-force across all - for O(n) time complexity
           This recursive approach is also called a "naive" implementation.
        """
        # if (n == 0) return 0;
        # if (n == 1) return 1;
        # if n in {0, 1, 2}:  # first 3 return values (0, 1, 2) are the same as
        # the request value.
        if n <= 3:
            return n
        # recursive means function calls itself.
        return Fibonacci.fibonacci_recursive(
            n - 1) + Fibonacci.fibonacci_recursive(n - 2)


    # Starting point in local cache:
    fibonacci_memoized_cache = {
        0: 0,
        1: 1,
        2: 2,
        3: 3,
        4: 5,
        5: 8,
        6: 13,
        7: 21,
        8: 34,
        9: 55,
        10: 89,
        11: 144,
        12: 233,
        13: 377,
        14: 610}
# 15: 987, 16: 1597, 17: 2584}


    def fibonacci_iterative(n):
        """Calculate value of n-th Fibonacci sequence using iterative approach for O(1) time complexity.
           This is considered a "bottom-up" dynamic programming.
           The memoized cache is generated.
        """
        if n in {
                0,
                1,
                2,
                3}:   # the first result values (0, 1, 2, 3) are the same as the request value.
            return n
        # Initialize cache:
        cache = list(range(n+1))
        cache[0:4] = [0,1,2,3]
        for i in range (4,n+1):
            cache[i] = cache[i-1] + cache[i-2]
        # TODO: Make use of hard-coded Fibonacci.fibonacci_memoized_cache
        Fibonacci.fibonacci_memoized_cache = {i:cache[i] for i in cache}
        return cache[n]


    def fibonacci_redis_connect():
            import redis
            azure_redis_hostname=get_from_env_file('AZURE_REDIS_HOSTNAME_FOR_FIBONACCI')
            
            azure_redis_port=get_from_env_file('AZURE_REDIS_PORT_FOR_FIBONACCI')
            azure_redis_password=get_from_env_file('AZURE_REDIS_ACCESS_KEY')
            reddis_connect_dict={
                'host': azure_redis_hostname,
                'port': azure_redis_port,
                'password': azure_redis_password,
                'ssl': False}
            try:
                # Retrieve fibonacci_memoized_cache from Redis:
                redis_fibonacci_connect = redis.StrictRedis(**reddis_connect_dict)  # PROTIP: ** means to unpack dictionary.

                # WARNING: Be off VPN for this to work:
                result = redis_fibonacci_connect.ping()
                print(f'*** Redis Host \"{azure_redis_hostname}\" established!" ')
                return redis_fibonacci_connect
            except Exception as e :
                print_fail(e)
                print_fail("fibonacci_redis_rw failed.")  # DEBGGING
                use_azure_redis = False
                return False

    # https://azure.microsoft.com/en-us/blog/view-your-azure-cache-for-redis-data-in-new-visual-studio-code-extension/
    # View your Azure Cache for Redis data in new Visual Studio Code extension

    def fibonacci_redis_rw(n):
        # see https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started
        # BEFORE ON TERMINAL: pip3 install -U redis  # to install package https://github.com/redis/redis-py
        # Check for availability of single n in the local fibonacci_memoized_cache:
        if n in Fibonacci.fibonacci_memoized_cache.keys():
            result_number = Fibonacci.fibonacci_memoized_cache[n] 
            print("*** Local returned : " + str(result_number) )
        else:  # If not, lookup from Redis:
            redis_fibonacci_connect = Fibonacci.fibonacci_redis_connect()
            if redis_fibonacci_connect:
                result = redis_fibonacci_connect.exists(n)  # single key/value.
                if result:  # found in Redis:
                    # Retrieve entire contents of Redis in fibonacci_memoized_cache (for future efficiency)
                    keys = list(redis_fibonacci_connect.scan_iter())
                    values = redis_fibonacci_connect.mget(keys)
                    cache = {k.decode("utf-8"):v.decode("utf-8") for k,v in zip(keys, values)}
                    # print(f'*** Redis cache={cache} ')
                    # return cache
                else:  # If not in Redis, create it and add to Redis:
                    result = Fibonacci.fibonacci_recursive(n)
                    if result: # Add to Redis:
                        true_false = redis_fibonacci_connect.set(n, result)
                        print(f'*** redis_fibonacci_connect.set returns {true_false} ')
                    else:
                        return None
                return result


    def fibonacci_redis_delete():
        """ Delete Redis cache, one key at a time : """
        redis_fibonacci_connect = Fibonacci.fibonacci_redis_connect()
        if redis_fibonacci_connect:
            for key in redis_fibonacci_connect.scan_iter():
                Fibonacci.redis_fibonacci_connect.delete(key)
            print("*** deleted : ")
        

    def fibonacci_memoized(n):
        """Calculate value of n-th Fibonacci sequence using recursive approach for O(1) time complexity.
           This is considered a "bottom-up" dynamic programming.
        """

        if n in Fibonacci.fibonacci_memoized_cache:  # Base case
            return Fibonacci.fibonacci_memoized_cache[n]

        Fibonacci.fibonacci_memoized_cache[n] = Fibonacci.fibonacci_memoized(
            n - 1) + Fibonacci.fibonacci_memoized(n - 2)

        new_num = Fibonacci.fibonacci_memoized(
            n - 1) + Fibonacci.fibonacci_memoized(n - 2)

        # FIXME: Add entry to Fibonacci.fibonacci_memoized_cache
            # see https://careerkarma.com/blog/python-add-to-dictionary/        
        Fibonacci.fibonacci_memoized_cache[n] = new_num
        print( Fibonacci.fibonacci_memoized_cache )

        return Fibonacci.fibonacci_memoized_cache[n]  # return whole cache?


class TestFibonacci(unittest.TestCase):
    def test_gen_fibonacci(self):

        if gen_fibonacci:
            """ Fibonacci numbers are recursive in design to generate sequence.
                But storing calculated values can reduce the time complexity to O(1).
            """
            print_heading("gen_fibonacci")

            #result = Fibonacci.fibonacci_redis_delete()
            #print(f'*** {result} from delete() ')

            # https://realpython.com/fibonacci-sequence-python/
            # hard-coded value (to go with hard-coded array above)
            n = 17  # For 14, n=610

            func_start_timer = timer()
            result = Fibonacci.fibonacci_recursive(n)
            func_end_timer = timer()
            recursive_time_duration = func_end_timer - func_start_timer
            if show_info:
                print(
                    f'*** fibonacci_recursive: {n} => {result} in {timedelta(seconds=recursive_time_duration)} seconds ')

            # For my next trick, replace local array with array from Redis:
            if use_azure_redis:
                redis_fibonacci = Fibonacci.fibonacci_redis_rw(n)
                if redis_fibonacci:
                    fibonacci_memoized_cache = redis_fibonacci
                print(Fibonacci.fibonacci_memoized_cache)  # DEBUGGIN

            # Having the array in Redis/Kafka cache service enables several instances of
            # this program to run at the same time.

            func_start_timer = timer()
            result=Fibonacci.fibonacci_memoized(n)
            if False:  # result:
                # Add new item to array in Redis cache:
                Fibonacci.fibonacci_redis_write(n, result)
            func_end_timer = timer()
            memoized_time_duration = func_end_timer - func_start_timer
            diff_order=( recursive_time_duration / memoized_time_duration )
            if show_info == True:
                print(f'*** fibonacci_memoized: {n} => {result} in {timedelta(seconds=memoized_time_duration)} seconds ({"%.2f" % diff_order}X faster).')

    

#### SECTION  9.9 Make change using Dynamic Programming     = make_change

# See https://wilsonmar.github.io/python-samples#make_change
# alternative:
# https://github.com/samgh/DynamicProgrammingEbook/blob/master/python/MakingChange.py


MAX_INT = 10  # the maximum number of individual bills/coins returned.


def make_change_plainly(k, C):
    # k is the amount you want back in bills/change
    # C is an array of each denomination value of the currency, such as [100,50,20,10,5,1]
    # (assuming there is an unlimited amount of each bill/coin available)
    n = len(C)  # the number of items in array C
    if show_verbose:
        print(f'*** make_change_plainly: C="{C}" n={n} ')

    turn = 0  # steps in making change
    print(f'*** turn={turn} k={k} to start ')
    compares = 0
    # list of individual bills/coins returned the number of different
    # denominations.
    change_returned = []
    # Mutable (can grow) with each turn to return a denomination
    while k > 0:  # Keep making change until no more
        for denom in C:  # Look thru the denominations where i=100, 50, etc....
            compares += 1
            # without float(), it won't calculate correctly.
            if float(k) >= denom:
                k = k - denom
                turn += 1  # increment
                if show_verbose:
                    print(f'*** turn={turn} k={k} after denom={denom} change ')
                # Add change made to output array [20, 10, 1, 1, 1, 1]
                change_returned.append(denom)
                break  # start a new scan of denominations
    print(f'*** After {turn} turns, k={k} remaining ...')
    # print(f'*** {change_returned} ')
    return change_returned


"""
MAX_INT=10  # the maximum number of individual bills/coins returned.

def make_change_dynamically(k,C):
   dp = [0] + [MAX_INT] * k  # array to hold output change made?
    print(f'*** dp={dp} ')

    # xrange (lazy) is no longer available?
    print(f'*** {list(range(1, n + 1))} ')
    for i in list(range(1, n + 1)):
       for j in list(range(C[i - 1], k + 1)):
           dp[j] = min(dp[j - C[i - 1]] + 1, dp[j])
    return dp
"""


class TestMakeChange(unittest.TestCase):
    def test_make_change(self):

        if make_change:
            print_heading("make_change")

            # TODO: Add timings
            change_for = 34
            denominations = [100, 50, 20, 10, 5, 1]
            change_back = make_change_plainly(change_for, denominations)
            if show_info:
                # print(f'*** change_for {change_for} in denominations {denominations} ')
                print(f'*** make_change: change_back=\"{change_back}\" ')
            self.assertEqual(change_back, [20, 10, 1, 1, 1, 1])


#### SECTION  9.10 Fill knapsack  = fill_knapsack

class TestFillKnapsack(unittest.TestCase):
    def test_fill_knapsack(self):

        if fill_knapsack:
            print_heading("fill_knapsack")

            print(f'*** fill_knapsack: ')

            def setUp(self):
                self.testcases = [
                    ([], 0, 0), ([
                        Item(
                            4, 5), Item(
                            1, 8), Item(
                            2, 4), Item(
                            3, 0), Item(
                            2, 5), Item(
                                2, 3)], 3, 13), ([
                                    Item(
                                        4, 5), Item(
                                            1, 8), Item(
                                                2, 4), Item(
                                                    3, 0), Item(
                                                        2, 5), Item(
                                                            2, 3)], 8, 20)]


#### SECTION 10. Retrieve client IP address    = get_ipaddr

my_ip_address=""  # Global

# class TestShowIpAddr(unittest.TestCase):

def find_ip_geodata(my_ip_address):

    ipfind_api_key = get_from_env_file('IPFIND_API_KEY')
    # Sample IPFIND_API_KEY="12345678-abcd-4460-a7d7-b5f6983a33c7"
    if ipfind_api_key and len(my_ip_address) > 0:
        print_verbose("Using IPFIND_API_KEY in .env file.")
    else:
        # remove key from memory others might peak at.
        # remove key from memory so others can't peak at it.
        del os.environ["IPFIND_API_KEY"]
        if show_verbose:
            print(
                f'***{bcolors.WARNING} Please remove secret \"IPFIND_API_KEY\" from .env file.{bcolors.RESET}')
    # TODO: Verify ipfind_api_key

    # Alternative: https://httpbin.org/ip returns JSON { "origin": "98.97.111.222" }
    url = 'https://ipfind.co/?auth=' + ipfind_api_key + '&ip=' + my_ip_address
    try:
        # import urllib, json # at top of this file.
        # https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html#b310-urllib-urlopen
        response = urllib.request.urlopen(url)
        # See https://docs.python.org/3/howto/urllib2.html
        try:
            ip_base = json.loads(response.read())
            # example='{"my_ip_address":"98.97.111.222","country":"United States","country_code":"US","continent":"North America","continent_code":"NA","city":null,"county":null,"region":null,"region_code":null,"postal_code":null,"timezone":"America\/Chicago","owner":null,"longitude":-97.822,"latitude":37.751,"currency":"USD","languages":["en-US","es-US","haw","fr"]}'
            # As of Python version 3.7, dictionaries are ordered. In Python 3.6
            # and earlier, dictionaries are unordered.
            if show_info:
                # print(f'***{bcolors.TRACE} country=\"{ip_base["timezone"]}\".{bcolors.RESET}')
                # "timezone":"America\/Chicago",
                # "longitude":-97.822,"latitude":37.751,
                # CAUTION: The client's true IP Address may be masked if a VPN is being used!
                # "currency":"USD",
                # "languages":["en-US","es-US","haw","fr"]}
                print(
                    f'*** {localize_blob("Longitude")}: {ip_base["longitude"]} {localize_blob("Latitude")}: {ip_base["latitude"]} in {ip_base["country_code"]} {ip_base["timezone"]} {ip_base["currency"]} (VPN IP).')
                return ip_base
        except Exception:
            print(
                f'***{bcolors.FAIL} ipfind.co {localize_blob("response not read")}.{bcolors.RESET}')
            # exit()
            return None
    except Exception:
        print(
            f'***{bcolors.FAIL} {url} {localize_blob("not operational")}.{bcolors.RESET}')
        # exit()
        return None


# def test_get_ipaddr(self):
if get_ipaddr:
    print_heading("get_ipaddr")

    import socket  # https://docs.python.org/3/library/socket.html
    print_verbose("IP address from socket.gethostname: "+socket.gethostbyname(socket.gethostname()))  # 192.168.0.118
        # 127.0.0.1
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_ipaddr = s.getsockname()[0]
    # FIXME: Close socket
    # s.close(fd)
    print_verbose("IP address from getsockname (default route): " + s.getsockname()[0])

    """
    # https://www.delftstack.com/howto/python/get-ip-address-python/
    from netifaces import interfaces, ifaddresses, AF_INET
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        print(' '.join(addresses))
    sys.exit()  # DEBUGGING
    """

    my_ipaddr_from_env = get_from_env_file('MY_IP_ADDRESS')
    if my_ipaddr_from_env and len(my_ipaddr_from_env) > 0:
        my_ip_address = my_ipaddr_from_env
    else:
        # print_warning("IP Address is blank in .env file.")
        # Lookup the ip address on the internet:
        url = "http://checkip.dyndns.org"
            # Alternative: https://ip-fast.com/api/ip/ is fast and not wrapped in HTML.
            # Alternative: https://api.ipify.org/?format=json

        # PROTIP: Close connection immediatelyto reduce man-in-the-middle attacks:
        #s = requests.session()
        #s.config['keep_alive'] = False
        request = requests.get(url, allow_redirects=False, headers={'Connection':'close'})
        # print( request.text )
        # <html><head><title>Current IP Check</title></head><body>Current IP Address: 98.97.94.96</body></html>
        clean = request.text.split(': ', 1)[1]  # split 1once, index [1]
        # [0] for first item.
        my_ip_address = clean.split('</body></html>', 1)[0]
        print_info( "My external IP Address: " + my_ip_address +" from "+ url )

    # NOTE: This is like curl ipinfo.io (which provides additional info associated with ip address)
    # IP Address is used for geolocation (zip & lat/long) for weather info.
    # List of geolocation APIs: https://www.formget.com/ip-to-zip-code/
    # Fastest is https://ipfind.com/ offering Developers - Free, 100
    # requests/day


# Lookup geolocation info from IP Address
if lookup_ipaddr:
    print_heading("lookup_ipaddr")
    print_trace("lookup_ipaddr for ip: " + my_ip_address)

    ip_base=find_ip_geodata(my_ip_address)
    if not ip_base:
        print_fail("ip_base not found: " + str(ip_base))
    else:
        print_verbose("ip_base found: " + str(ip_base))
        # Replace global defaults:
        # FIXME: TypeError: 'NoneType' object is not subscriptable
        if ip_base["country_code"]:
            my_country = ip_base["country_code"]
        if ip_base["longitude"]:
            my_longitude = ip_base["longitude"]
        if ip_base["latitude"]:
            my_latitude = ip_base["latitude"]
        if ip_base["timezone"]:
            my_timezone = ip_base["timezone"]
        if ip_base["currency"]:
            my_currency = ip_base["currency"]

        # TODO: my_country = ip_base["country_code"]


#### SECTION 12. Obtain Zip Code (used to retrieve Weather info)


def obtain_zip_code():

    # use to lookup country, US state, long/lat, etc.
    my_zip_code_from_env = get_from_env_file('MY_ZIP_CODE')    
    if my_zip_code_from_env:
        # Empty strings are "falsy" - considered false in a Boolean context:
        #text_msg="US Zip Code: "+ str(my_zip_code_from_env) +" obtained from file "+ str(global_env_path)
        #print_verbose(text_msg)
        return my_zip_code_from_env
    else:   # zip code NOT supplied from .env:
        ZIP_CODE_DEFAULT = "90210"  # Beverly Hills, CA, for demo usage.
        zip_code = ZIP_CODE_DEFAULT
        if show_warning:
            print(
                f'***{bcolors.WARNING} \"MY_ZIP_CODE\" not specified in .env file.{bcolors.RESET} ')
            print(
                f'***{bcolors.WARNING} Default US Zip Code = \"{ZIP_CODE_DEFAULT}\"{bcolors.RESET} ')
            return zip_code
        if verify_manually:
            while True:  # keep asking in loop:
                question = localize_blob("A.Enter 5-digit Zip Code: ")
                zip_code_input = input(question)
                if not zip_code_input:  # If empty input, use default:
                    zip_code = ZIP_CODE_DEFAULT
                    return zip_code
                zip_code = zip_code_input
                # zip_code_char_count = sum(c.isdigit() for c in zip_code)
                zip_code_char_count = len(zip_code)
                # Check if zip_code is 5 digits:
                if (zip_code_char_count != 5):
                    if show_warning:
                        print(
                            f'***{bcolors.WARNING} Zip Code \"{zip_code}\" should only be 5 characters.{bcolors.RESET} ')
                    # ask for zip_code
                    if not verify_manually:
                        zip_code = ZIP_CODE_DEFAULT
                        return zip_code
                    else:  # ask manually:
                        question = localize_blob("B.Enter 5-digit Zip Code: ")
                        zip_code_input = input(question)
                        if not zip_code_input:  # If empty input, use default:
                            zip_code = ZIP_CODE_DEFAULT
                            return zip_code
                        zip_code = zip_code_input
                else:
                    return zip_code
# Test cases:
# .env "59041" processed
# .env has "590" (too small) recognizing less then 5 digits.
# .env has no zip (question), answer "90222"
# .env has no zip (question), answer "902"


class TestLookupZipinfo(unittest.TestCase):
    def test_lookup_zipinfo(self):

        if lookup_zipinfo:
            print_heading("lookup_zipinfo")

            zip_code = obtain_zip_code()
            zippopotam_url = "https://api.zippopotam.us/us/" + zip_code
            # TODO: Do ICMP ping on api.zippopotam.us
            if show_trace:
                print(
                    f'***{bcolors.TRACE} lookup_zipinfo: zippopotam_url={zippopotam_url} {bcolors.RESET} ')
            try:
                response = requests.get(zippopotam_url, allow_redirects=False)
                x = response.json()
                print_trace(x)  # sample response:
                # {"post code": "59041", "country": "United States", "country abbreviation": "US", \
                # "places": [{"place name": "Joliet", "longitude": "-108.9922", "state": "Montana", "state abbreviation": "MT", "latitude": "45.4941"}]}
                y = x["places"]
                if show_info:
                    print(
                        f'***{bcolors.INFO} lookup_zipinfo: {zip_code} = {y[0]["place name"]}, {y[0]["state abbreviation"]} ({y[0]["state"]}), {x["country abbreviation"]} ({x["country"]}) {bcolors.RESET}')
                    print(
                        f'***{bcolors.INFO} {localize_blob("Longitude:")} {y[0]["longitude"]} {localize_blob("Latitude:")} {y[0]["latitude"]} {bcolors.RESET}')
                    # TODO: loop through zip_codes
            except BaseException as e:  # FIXME: Test with bad DNS name
                print(
                    f'***{bcolors.FAIL} zippopotam.us BaseException: \"{e}\".{bcolors.RESET} ')
                exit(1)
            except ConnectionError as e:
                print(
                    f'***{bcolors.FAIL} zippopotam.us connection error \"{e}\".{bcolors.RESET} ')
                exit(1)
            except Exception as e:  # Check on error on zip_code lookup:
                #        print('abcd')
                print(
                    f'***{bcolors.FAIL} zippopotam.us Exception: \"{e}\".{bcolors.RESET} ')
                exit(1)


#### SECTION 13. Retrieve Weather info using API

def compass_text_from_degrees(degrees):
    # adapted from https://www.campbellsci.com/blog/convert-wind-directions
    compass_sector = [
        "N",
        "NNE",
        "NE",
        "ENE",
        "E",
        "ESE",
        "SE",
        "SSE",
        "S",
        "SSW",
        "SW",
        "WSW",
        "W",
        "WNW",
        "NW",
        "NNW",
        "N"]  # 17 index values
    # graphic ![python-cardinal-point-compass-windrose-600x600-Brosen svg](https://user-images.githubusercontent.com/300046/142781379-addfa8f7-9394-4751-9ddd-65e681e4a49c.png)
    # graphic from https://www.wikiwand.com/en/Cardinal_direction
    remainder = degrees % 360  # modulo remainder of 270/360 = 196
    index = int(round(remainder / 22.5, 0) + 1)   # (17 values)
    return compass_sector[index]


if show_weather:
    print_heading("show_weather")

    # Commentary on this at
    # https://wilsonmar.github.io/python-samples#show_weather

    # See https://openweathermap.org/current for
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    # TODO: Ping host to verify reachability

    # Adapted from https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
    # From https://home.openweathermap.org/users/sign_up
    # then https://home.openweathermap.org/users/sign_in

    # Retrieve from .env file in case vault doesn't work:
    openweathermap_api_key = get_from_env_file('OPENWEATHERMAP_API_KEY')
    # OPENWEATHERMAP_API_KEY="12345678901234567890123456789012"
    # remove OPENWEATHERMAP_API_KEY value from memory.
    del os.environ["OPENWEATHERMAP_API_KEY"]
    print_verbose(
            f'***{bcolors.WARNING} WARNING: Please store \"OPENWEATHERMAP_API_KEY\" in a Vault instead of .env file.{bcolors.RESET}')
    # TODO: Verify openweathermap_api_key

    my_zip_code = obtain_zip_code()
    # api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    # weather_url = base_url + "appid=" + api_key + "&q=" + city_name
    weather_url = base_url + "appid=" + openweathermap_api_key + "&zip=" + my_zip_code
    if show_trace:
        print(f'***{bcolors.TRACE} weather_url={weather_url}.{bcolors.RESET}')

    # TODO: Format request encoding to remove spaces, etc.

    # return response object from get method of requests module:
    try:
        response = requests.get(weather_url, allow_redirects=False)
    except ConnectionError:
        print(f'*** Connection error \"{response}\".')

    # convert json format data into json method of response object:
    # python format data
    x = response.json()
    if show_trace:
        print(f'***{bcolors.TRACE} x = {response.json()}{bcolors.RESET}')
        # On-line JSON formatter: https://jsonformatter.curiousconcept.com/

    # x contains list of nested dictionaries.
    # x "cod" contains the HTTP response code - "404":
    if x["cod"] == "404":
        print(
            f'*** {x["cod"]} - U.S. Zip Code {bcolors.FAIL}\"{my_zip_code}\" Not Found!{bcolors.RESET}')
    else:
        # store the value of "main" key in variable y:
        y = x["main"]

        coord = x["coord"]
        system = x["sys"]
        text_weather_location = system["country"] + " " + my_zip_code + ": " + x["name"] + " " + localize_blob(
            "Longitude") + ": " + str(coord["lon"]) + " " + localize_blob("Latitude") + ": " + str(coord["lat"])
        # no  +","+ my_us_state
        print_info(text_weather_location)
# f'*** {localize_blob("Longitude")}: {coord["lon"]}
# {localize_blob("Latitude")}: {coord["lat"]} {localize_blob("in")}
# {system["country"]} {x["name"]} {my_zip_code} ')

        # store the value of "weather" key in variable z:
        z = x["weather"]
        # store the value corresponding to the "description" key at

        # store the value corresponding to the "temp" key of y:
        current_temp_kelvin = y["temp"]
        # Text to float conversion: celsius = (temp - 32) * 5/9
        current_temp_fahrenheit = (
            float(current_temp_kelvin) * 1.8) - float(459.67)
        current_temp_celsius = (float(current_temp_kelvin)) - float(273.15)

        sunrise = time.strftime(
            my_date_format, time.localtime(
                system["sunrise"]))
        sunset = time.strftime(
            my_date_format, time.localtime(
                system["sunset"]))
        min_fahrenheit = (float(y["temp_min"]) * 1.8) - float(459.67)
        max_fahrenheit = (float(y["temp_max"]) * 1.8) - float(459.67)
        min_celsius = (float(y["temp_min"])) - float(273.15)
        max_celsius = (float(y["temp_max"])) - float(273.15)
        if show_info:
            text_weather_min = localize_blob("Minimum temperature") + ": " + "{:.2f}".format(
                min_celsius) + "°C (" + "{:.2f}".format(min_fahrenheit) + "°F) " + localize_blob("Sunrise") + ": " + sunrise
            # print(f'*** {localize_blob("Minimum temperature")}: {"{:.2f}".format(min_celsius)}°C ({"{:.2f}".format(min_fahrenheit)}°F), {localize_blob("Sunrise")}: {sunrise} ')
            print_info(text_weather_min)

            text_weather_cur = localize_blob("Currently") + ": " + "{:.2f}".format(current_temp_celsius) + "°C (" + "{:.2f}".format(current_temp_fahrenheit) + "°F) " \
                + str(y["humidity"]) + "% " + localize_blob("humidity") + ", " + localize_blob(z[0]["description"]) + ", " + \
                localize_blob("visibility") + ": " + str(x["visibility"]) + " feet"
            # f'***{bcolors.INFO} {localize_blob("Currently")}:
            # {"{:.2f}".format(current_temp_celsius)}°C
            # ({"{:.2f}".format(current_temp_fahrenheit)}°F), {y["humidity"]}%
            # {localize_blob("humidity")},
            # {localize_blob(z[0]["description"])},
            # {localize_blob("visibility")}: {x["visibility"]}
            # feet{bcolors.RESET}')
            print_info(text_weather_cur)
            # f'***{bcolors.INFO} {localize_blob("Currently")}:
            # {"{:.2f}".format(current_temp_celsius)}°C
            # ({"{:.2f}".format(current_temp_fahrenheit)}°F), {y["humidity"]}%
            # {localize_blob("humidity")},
            # {localize_blob(z[0]["description"])},
            # {localize_blob("visibility")}: {x["visibility"]}
            # feet{bcolors.RESET}')

            text_weather_max = localize_blob("Maximum temperature") + ": " + "{:.2f}".format(
                max_celsius) + "°C (" + "{:.2f}".format(max_fahrenheit) + "°F) " + localize_blob("Sunset") + ": " + sunset
            # print(f'*** {localize_blob("Maximum temperature")}: {"{:.2f}".format(max_celsius)}°C ({"{:.2f}".format(max_fahrenheit)}°F),  {localize_blob("Sunset")}: {sunset} ')
            print_info(text_weather_max)

        wind = x["wind"]
        if show_info:
            if "gust" not in wind.keys():
                # if wind["gust"] == None :
                gust = ""
            else:
                gust = localize_blob("Gusts") + ": " + \
                    str(wind["gust"]) + " mph"
            text_wind = localize_blob("Wind Speed") + ": " + str(wind["speed"]) + " " + gust + " " + localize_blob(
                "from direction") + ": " + compass_text_from_degrees(wind["deg"]) + "(" + str(wind["deg"]) + "/360)"
            print_info(text_wind)
            # print(f'*** {localize_blob("Wind Speed")}: {wind["speed"]} {gust} {localize_blob("from direction")}: {compass_text_from_degrees(wind["deg"])} ({wind["deg"]}/360) ')
            # FIXME: y["grnd_level"]
            grnd_level = ""
            text_pressure = localize_blob("Atmospheric pressure") + ": " + grnd_level + ":" + str(
                y["pressure"]) + " hPa (hectopascals) or millibars (mb) " + localize_blob("at ground level")
            print_info(text_pressure)
            #    f'*** {localize_blob("Atmospheric pressure")}: {grnd_level} ({y["pressure"]}) hPa (hectopascals) or millibars (mb) {localize_blob("at ground level")}')
            # at Sea level: {y["sea_level"]} Ground: {y["grnd_level"]} '),
            # From a low of 1011 hPa in December and January, to a high of about 1016 in mid-summer,
            # 1013.25 hPa or millibars (mb) is the average pressure at mean sea-level (MSL) globally.
            # (101.325 kPa; 29.921 inHg; 760.00 mmHg).
            # In the International Standard Atmosphere (ISA) that is 1 atmosphere (atm).
            # In the continental US, San Diego CA has the smallest range (994.58 to 1033.86) hPa (29.37 to 30.53 inHg).
            # The boiling point of water is higher than 100 °C (212 °F) at
            # higher pressure (on mountains).

        # TODO: Save readings for historical comparisons.
        # TODO: Look up previous temp and pressure to compare whether they are rising or falling.
            # Air pressure rises and falls about 3 hP in daily cycles, regardless of weather.
            # A drop of 7 hP or more in 24 hours may indicate a tendency: high-pressure system is moving out and/or a low-pressure system is moving in.
            # Lows have a pressure of around 1,000 hPa/millibars.
            # Generally, high pressure means fair weather, and low pressure
            # means rain.

        if email_weather:
            message = text_weather_location + "\n" + text_weather_min + "\n" + \
                text_weather_cur + "\n" + text_weather_max + "\n" + text_wind + "\n" + text_pressure
            to_gmail_address = get_from_env_file("TO_EMAIL_ADDRESS")
            subject_text = "Current weather for " + x["name"]
            # FIXME: smtplib_sendmail_gmail(to_gmail_address,subject_text, message )
            # print("Emailed to ...")


##  14. Retrieve secrets from local OS Key Vault  = use_keyring

# Commentary on this at https://wilsonmar.github.io/python-samples#use_keyvault

def store_in_keyright(key_namespace_in, key_entry_in, key_text_in):
    # pip install -U keyring
    import keyring
    import keyring.util.platform_ as keyring_platform

    print("*** Keyring path:", keyring_platform.config_root())
        # /home/username/.config/python_keyring  # Might be different for you

    print("*** Keyring: ", keyring.get_keyring())
        # keyring.backends.SecretService.Keyring (priority: 5)

    keyring.set_password(key_namespace_in, key_entry_in, key_text_in)
    # print("*** text: ",keyring.get_password(key_namespace_in, key_entry_in))


def get_text_from_keyring(key_namespace_in, key_entry_in):
    # pip install -U keyring
    import keyring
    import keyring.util.platform_ as keyring_platform

    cred = keyring.get_credential(key_namespace_in, key_entry_in)
    # CAUTION: Don't print out {cred.password}
    # print(f"*** For username/key_namespace {cred.username} in namespace {key_namespace_in} ")
    return cred.password


# TODO: def remove_from_keyring(key_namespace_in, key_entry_in):

def rm_env_line( api_key_in , replace_str_in ):
    with open(global_env_path, 'r') as f:
        x = f.read()
        # Obtain line containing value of api_key_in:
        regex_pattern = api_key_in + r'="\w*"'
        matched_line = re.findall(regex_pattern, x)[0]
        print_trace(matched_line)
        
        # Substitute in an entire file:
        entire_file = re.sub(matched_line, replace_str_in, x)
        print_trace(entire_file)
        # t=input()    # DEBUGGING

    with open(global_env_path, 'w+') as f:
        f.write(entire_file)

    # Read again to confirm:
    with open(global_env_path, 'r') as f:
        print_trace( f.read() )


if remove_env_line:

    api_key_name="OPENWEATHERMAP_API_KEY"
    current_time = time.time()
    current_datetime = _datetime.datetime.fromtimestamp(current_time)  # Default: 2021-11-20 07:59:44.412845
    text_msg="# " + api_key_name +" removed " + str(current_datetime) +" by "+ global_username
    rm_env_line( api_key_name , text_msg )
    print_verbose(text_msg)

if use_keyring:
    print_heading("use_keyring")

    # TODO: Replace these hard-coded with real values:
    key_namespace = "my-app"
    key_entry = "OPENWEATHERMAP_API_KEY"  # = cred.username
    key_text="yackaty yack"
    print(f'*** username/key_namespace: \"{key_entry}\" in namespace \"{key_namespace}\" ')

    store_in_keyright(key_namespace, key_entry, key_text)
    key_text_back=get_text_from_keyring(key_namespace, key_entry)
    print_trace( key_text_back )

    # TODO: remove_from_keyring(key_namespace_in, key_entry_in)



#### SECTION 13. Login to Vault using Python hvac library

if login_to_azure:
   print_fail("QUESTION: Chris?")

   # Python equivalent of "az login" CLI command.


#### SECTION 14: Obtain Azure Subscription from Vault 

def azure_login():
    """
    > az --version
    azure-cli                         2.49.0
    core                              2.49.0
    telemetry                          1.0.8
    Extensions:
    azure-devops                      0.18.0
    azure-iot                        0.10.14
    timeseriesinsights                 0.2.1
    Dependencies:
    msal                              1.20.0
    azure-mgmt-resource               22.0.0
    Python location '/usr/local/Cellar/azure-cli/2.49.0/libexec/bin/python'
    Extensions directory '/Users/wilsonmar/.azure/cliextensions'
    """
    return False

if use_azure:
    print_fail("QUESTION: Chris?")


#### SECTION 15: Login to Azure

   # https://www.youtube.com/watch?v=unbzStG3IVY
   # In preview June, 2022.
   # Azure ML CLI v2 support python, R, Java, Julia, C#
   # Python SDK v2 build any workflow (simple to complex incrementally)

def azure_see():
    """
    az login --use-device-code
    pip install -r requirements.txt
    python provision_rg.py

    # https://github.com/RekhuGopal/PythonHacks/blob/main/AzureAutomationWithPython/requirements.txt
    # contains:
    azure-mgmt-resource
    azure-mgmt-storage
    azure-identity
    """
    # Based on: import os, random
    # from azure.identity import AzureCliCredential
    credential = AzureCliCredential()
   
    subscription_id = "285a9b29-43df-4ebf-85b1-61bbf7929871"   # replace with yours.
    resource_client = ResourceManagementClient(credential, subscription_id)
    RESOURCE_GROUP_NAME = "PythonAzureExample-Storage-rg"
    LOCATION = "centralus"

    return False

if login_to_azure:
    print_fail("QUESTION: Chris?")


# See https://www.youtube.com/watch?v=YAg6khewJiU
   # How to use Python SDK for Azure Automation by vrchinnarathod@gmail.com
   # https://www.linkedin.com/in/rekhu-chinnarathod-58b3a860/
   # which uses https://github.com/RekhuGopal/PythonHacks/tree/main/AzureAutomationWithPython
   # https://github.com/RekhuGopal/PythonHacks/blob/main/AzureAutomationWithPython/provision_rg.py

# Requires: pip install azure.identity # (2021.10.8) Azure Active Directory identity library
   # 1.13.0 https://docs.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python
   # https://pypi.org/project/azure-identity/
#from azure.identity import DefaultAzureCredential


    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.storage import StorageManagementClient

#from azure.common.credentials import ServicePrincipalCredentials

   # https://pypi.python.org/pypi/azure-keyvault-secrets
#from azure.keyvault.secrets import SecretClient

# azure-mgmt-storage  
   # https://pypi.python.org/pypi/azure-mgmt-storage
# azure-mgmt-compute  
   # https://pypi.python.org/pypi/azure-mgmt-compute) : Management of Virtual Machines, etc.

#from azure.mgmt.resource import ResourceManagementClient  
   # https://pypi.python.org/pypi/azure-mgmt-resource

#from azure.storage.blob import BlobServiceClient   #
   # https://pypi.python.org/pypi/azure-storage-blob



#### SECTION 16: In Azure, list resources for specific SubscriptionID

# See https://www.youtube.com/watch?v=we1pcMRQwD8 by Michael Levan of CBTNuggets.com
# See https://stackoverflow.com/questions/51546073/how-to-run-azure-cli-commands-using-python
from azure.cli.core import get_default_cli as azcli
# Run a CLI az command constructed as a Python struct:
# Replace 'Dev2' with your resource:
azcli().invoke(['vm', 'list', '-g', 'Dev2'])

def az_cli (args_str):
    args = args_str.split()
    cli = get_default_cli()
    cli.invoke(args)
    if cli.result.result:
        return cli.result.result
    elif cli.result.error:
        raise cli.result.error
    return True



#### SECTION 14. Retrieve secrets from Azure Key Vault

# Commentary on this at https://wilsonmar.github.io/python-samples#use_azure

def set_azure_secret_from_env(secretName):
    # TODO: Get from user prompt?
    # secretName  = input("Input a name for your secret > ")
    # secretValue = input("Input a value for your secret > ")

    secretValue = get_from_env_file(secretName)  # from .env file
    if not secretValue:
        print_fail("No " + secretName + " in .env")
        return None
    try:
        client.set_secret(secretName, secretValue)
        print_verbose("Secret " + secretName+ " saved.")
        print_info("Please store in a Vault instead of .env file.")
    except Exception:
        # FIXME: 
        print(
            f'***{bcolors.FAIL} client.set.secret of \"{secretName}\" failed.{bcolors.RESET}')
        return None

    # python3 wants to use your confidential
    # information stored in "VS Code Azure" in your
    # keychain
    # See https://github.com/microsoft/vscode-azurefunctions/issues/1759


def retrieve_azure_secret(secretName):
    try:
        retrieved_secret = client.get_secret(secretName)
        # Don't print secrets: print(f'*** Secret \"{secretName}\" = \"{retrieved_secret.value}\".')
        return retrieved_secret
    except Exception:
        print(
            f'***{bcolors.FAIL} client.get.secret of \"{secretName}\" failed.{bcolors.RESET}')


def delete_azure_secret(secretName):
    try:
        poller = client.begin_delete_secret(secretName)
        deleted_secret = poller.result()
        print(f'*** Secret \"{secretName}\" deleted.')
    except Exception:
        print(
            f'***{bcolors.FAIL} delete.secret of \"{secretName}\" failed.{bcolors.RESET}')
        exit()


if use_azure:

    # https://azuredevopslabs.com/labs/vstsextend/azurekeyvault/
    # Based on
    # https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-python

    # Before running this, in a Terminal type: "az login" for the default browser to enable you to login.
    # Return to the Terminal.  TODO: Service account login?

    # "eastus"  # aka LOCATION using the service.
    az_region_from_env = get_from_env_file('AZURE_REGION')
    if az_region_from_env:
        azure_region = az_region_from_env
    else:
        azure_region = "eastus"


    AZ_SUBSCRIPTION_ID = get_from_env_file('AZ_SUBSCRIPTION_ID')  # from .env file
    if not AZ_SUBSCRIPTION_ID:
        print_fail("No AZ_SUBSCRIPTION_ID.")
        exit

    azure_region = get_from_env_file('AZURE_REGION')  # from .env file
    if not azure_region:
        print_fail("No AZURE_REGION.")
        exit

    # ON A CLI TERMINAL:
    # pip install -U azure-keyvault-secrets
    # az account list --output table
    # az account set --subscription ...
    # az group create --name KeyVault-PythonQS-rg --location eastus
    # az keyvault create --name howdy-from-azure-eastus --resource-group KeyVault-PythonQS-rg
    # az keyvault set-policy --name howdy-from-azure-eastus --upn {email} --secret-permissions delete get list set
    # Message: Resource group 'devwow' could not be found.

    # Defined at top of this file:
    # import os
    # from azure.keyvault.secrets import SecretClient
    # from azure.identity import DefaultAzureCredential

    azure_keyVaultName = get_from_env_file('AZ_KEY_VAULT_NAME')  # from .env file
    if not azure_keyVaultName:
        print_fail("No AZ_KEY_VAULT_NAME.")
        exit

    KVUri = f"https://{azure_keyVaultName}.vault.azure.net"
    try:
        credential = DefaultAzureCredential()
        client = SecretClient(vault_url=KVUri, credential=credential)
        print(
            f'*** Using Azure secret Key Vault \"{azure_keyVaultName}\" in {azure_region} region.')
    except Exception:
        print(
            f'***{bcolors.FAIL} Azure Key Vault {azure_keyVaultName} auth failed.{bcolors.RESET}')
        # don't exit. Using .env file failure.
    
    # TODO: Encrypt/hash secret in transit and at rest!    
    result = set_azure_secret_from_env("OPENWEATHERMAP_API_KEY")
        # OPENWEATHERMAP_API_KEY="12345678901234567890123456789012"
    if not result:
        exit
    
    #retrieved_secret = retrieve_azure_secret("OPENWEATHERMAP_API_KEY")
    #print_trace("Secret retrieved: " + str(retrieved_secret) )  # please avoid printing out secret values.
    # TODO: Unencrypt/rehash secretValue?

    x=input("Press Enter to continue")  # DEBUGGING

    # set_azure_secret_from_env("IPFIND_API_KEY")
    # retrieve_azure_secret("IPFIND_API_KEY")
        # IPFIND_API_KEY="12345678-abcd-4460-a7d7-b5f6983a33c7"


#### SECTION 15. Retrieve secrets from AWS KMS

# Commentary on this at https://wilsonmar.github.io/python-samples#use_aws

# https://www.learnaws.org/2021/02/20/aws-kms-boto3-guide/
# https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/secrets-manager.html
# https://docs.aws.amazon.com/kms/latest/developerguide/
# https://docs.aws.amazon.com/code-samples/latest/catalog/python-kms-encrypt_decrypt_file.py.html

# In the Terminal running this program:
# Must first install : pip install boto3 -U
# Use the "cryptopgraphy" package to encrypt and decrypt data.
# Paste definitions of AWS keys to authenticate.

""" Boto3 has two ways to access objects within AWS services (such as kms):
    * boto3.client('kms') provide a low-level interface to all AWS service operations.
    Client whose methods map close to 1:1 with service APIs.
    Clients are generated from a JSON service definition file.

    * boto3.resources('kms') represent an object-oriented interface to AWS to provide
    a higher-level abstraction than the raw, low-level calls made by service clients.
"""


def create_aws_cmk(description="aws_cmk_description"):  # FIXME
    """Creates KMS Customer Master Keys (CMKs).
    AWS KMS supports two types of CMKs, using a Description to differentiate between them:
    1. By default, KMS creates a symmetric CMK 256-bit key. It never leaves AWS KMS unencrypted.
    2. Asymmetric CMKs are where AWS KMS generates a key pair. The private key never leaves AWS KMS unencrypted.
    """

    kms_client = boto3.client("kms")
    response = kms_client.create_key(Description=aws_cmk_description)

    # Return the key ID and ARN:
    return response["KeyMetadata"]["KeyId"], response["KeyMetadata"]["Arn"]
    # RESPONSE: ('c98e65ee-95a5-409e-8f25-6f6732578798',
    # 'arn:aws:kms:us-west-2:xxxx:key/c98e65ee-95a5-409e-8f25-6f6732578798')


def retrieve_aws_cmk(aws_cmk_description):
    """Retrieve an existing KMS CMK based on its description"""

    # Retrieve a list of existing CMKs
    # If more than 100 keys exist, retrieve and process them in batches
    kms_client = boto3.client("kms")
    response = kms_client.list_keys()

    for cmk in response["Keys"]:
        key_info = kms_client.describe_key(KeyId=cmk["KeyArn"])
        if key_info["KeyMetadata"]["Description"] == description:
            return cmk["KeyId"], cmk["KeyArn"]

    # No matching CMK found
    return None, None


def create_aws_data_key(cmk_id, key_spec="AES_256"):
    """Generate a data key to use when encrypting and decrypting data,
    so this returns both the encrypted CiphertextBlob as well as Plaintext of the key.
    A data key is a unique symmetric data key used to encrypt data outside of AWS KMS.
    AWS returns both an encrypted and a plaintext version of the data key.
    AWS recommends the following pattern to use the data key to encrypt data outside of AWS KMS:
    - Use the GenerateDataKey operation to get a data key.
    - Use the plaintext data key (in the Plaintext field of the response) to encrypt your data outside of AWS KMS. Then erase the plaintext data key from memory.
    - Store the encrypted data key (in the CiphertextBlob field of the response) with the encrypted data.
    """

    # Create data key:
    kms_client = boto3.client("kms")
    response = kms_client.generate_aws_data_key(KeyId=cmk_id, KeySpec=key_spec)

    # Return the encrypted and plaintext data key
    return response["CiphertextBlob"], base64.b64encode(response["Plaintext"])


def delete_aws_data_key(cmk_id):
    print("ha")


def decrypt_aws_data_key(data_key_encrypted):
    """Decrypt an encrypted data key"""

    # Decrypt the data key
    kms_client = boto3.client("kms")
    response = kms_client.decrypt(CiphertextBlob=data_key_encrypted)

    # Return plaintext base64-encoded binary data key:
    return base64.b64encode((response["Plaintext"]))



NUM_BYTES_FOR_LEN = 4


def encrypt_aws_file(filename, cmk_id):
    """Encrypt JSON data using an AWS KMS CMK
    Client-side, encrypt data using the generated data key along with the cryptography package in Python.
    Store the encrypted data key along with your encrypted data since that will be used to decrypt the data in the future.
    """

    with open(filename, "rb") as file:
        file_contents = file.read()

    data_key_encrypted, data_key_plaintext = create_aws_data_key(cmk_id)
    if data_key_encrypted is None:
        return

    # try: Encrypt the data:
    f = Fernet(data_key_plaintext)
    file_contents_encrypted = f.encrypt(file_contents)

    # Write the encrypted data key and encrypted file contents together:
    with open(filename + '.encrypted', 'wb') as file_encrypted:
        file_encrypted.write(
            len(data_key_encrypted).to_bytes(
                NUM_BYTES_FOR_LEN,
                byteorder='big'))
        file_encrypted.write(data_key_encrypted)
        file_encrypted.write(file_contents_encrypted)


def decrypt_aws_file(filename):
    """Decrypt a file encrypted by encrypt_aws_file()"""

    # Read the encrypted file into memory
    with open(filename + ".encrypted", "rb") as file:
        file_contents = file.read()

    # The first NUM_BYTES_FOR_LEN tells us the length of the encrypted data key
    # Bytes after that represent the encrypted file data
    data_key_encrypted_len = int.from_bytes(file_contents[:NUM_BYTES_FOR_LEN],
                                            byteorder="big") \
        + NUM_BYTES_FOR_LEN
    data_key_encrypted = file_contents[NUM_BYTES_FOR_LEN:data_key_encrypted_len]

    # Decrypt the data key before using it
    data_key_plaintext = decrypt_aws_data_key(data_key_encrypted)
    if data_key_plaintext is None:
        return False

    # Decrypt the rest of the file:
    f = Fernet(data_key_plaintext)
    file_contents_decrypted = f.decrypt(file_contents[data_key_encrypted_len:])

    # Write the decrypted file contents
    with open(filename + '.decrypted', 'wb') as file_decrypted:
        file_decrypted.write(file_contents_decrypted)


# The AWS Toolkit uses the AWS Serverless Application Model (AWS SAM) to
# create and manage AWS resources such as AWS Lambda Functions.
# It provides shorthand syntax to express functions, APIs, databases, and more in a declarative way.
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html
# https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html


if use_aws:
    print_heading("use_aws")

    aws_region_from_env = get_from_env_file('AWS_REGION')   # "us-east-1"
    if az_region_from_env:
        azure_region = az_region_from_env
    else:
        azure_region = "us-east-1"  # "Friends don't let friends use AWS us-east-1 in production"

    # Retrieve from .env file:
    aws_cmk_description = get_from_env_file('AWS_CMK_DESCRIPTION')
    if not aws_cmk_description:
        print_fail("AWS_CMK_DESCRIPTION not in .env")
        exit(1)
    else:
        if show_verbose:
            print(
                f'**** Creating AWS CMK with Description:\"{aws_cmk_description}\" ')

    # https://hands-on.cloud/working-with-kms-in-python-using-boto3/

    # create_aws_cmk(description=aws_cmk_description)

    # retrieve_aws_cmk(aws_cmk_description)
    # RESPONSE: ('c98e65ee-95a5-409e-8f25-6f6732578798',
    # 'arn:aws:kms:us-west-2:xxx:key/c98e65ee-95a5-409e-8f25-6f6732578798')
    # enable_aws_cmk()
    # disable_aws_cmk()
    # list_aws_cmk()

    # create_aws_data_key(cmk_id, key_spec="AES_256")
    # schedule_key_deletion()
    # option to specify a PendingDeletion period of 7-30 days.
    # cancel_key_deletion()

    # encrypt_aws_data_key(data_key_encrypted)
    # decrypt_aws_data_key(data_key_encrypted)

    # encrypt_aws_file(filename, cmk_id)
    # decrypt_aws_file(filename)
    #    cat test_file.decrypted
    # hello, world
    # this file will be encrypted


#### SECTION 16. Retrieve secrets from GCP Secret Manager = use_gcp

# Commentary on this at https://wilsonmar.github.io/python-samples#use_gcp
# https://wilsonmar.github.io/gcp

# Adapted from
# https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets

def create_gcp_secret(gcp_project_id_in, secret_id):
    """
    Create a new secret with the given name. A secret is a logical wrapper
    around a collection of secret versions. Secret versions hold the actual
    secret material.
    """
    from google.cloud import secretmanager

    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project:
    parent = f"projects/{gcp_project_id_in}"

    # Build a dict of settings for the secret:
    secret = {'replication': {'automatic': {}}}

    # Create the secret:
    response = client.create_secret(
        secret_id=secret_id,
        parent=parent,
        secret=secret)
    # request={
    #    "parent": parent,
    #    "secret_id": secret_id,
    #    "secret": {"replication": {"automatic": {}}},
    # }

    if show_verbose:
        print(f'*** Created GCP secret: {response.name}')
    return response.name


def add_gcp_secret_version(gcp_project_id_in, secret_id, payload):
    """
    Add a new secret version to the given secret with the provided payload.
    """

    # from google.cloud import secretmanager

    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent secret.
    parent = f"projects/{gcp_project_id_in}/secrets/{secret_id}"

    # Convert the string payload into a bytes. This step can be omitted if you
    # pass in bytes instead of a str for the payload argument.
    payload = payload.encode('UTF-8')

    # Add the secret version.
    response = client.add_secret_version(
        parent=parent, payload={'data': payload})

    if show_verbose:
        print(f'*** Added GCP secret version: {response.name}')
    return response.name


def access_gcp_secret_version(
        gcp_project_id_in,
        secret_id,
        version_id="latest"):
    """
    Access the payload for the given secret version if one exists. The version
    can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
    """

    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{gcp_project_id_in}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)
  # response = client.access_secret_version(request={"name": name})

    respone_payload = response.payload.data.decode('UTF-8')
    if show_verbose:
        print(f'*** Added GCP secret version: {respone_payload}')
    return respone_payload


def hash_gcp_secret(secret_value):
    return hashlib.sha224(bytes(secret_value, "utf-8")).hexdigest()


def list_gcp_secrets(gcp_project_id_in):
    """
    List all secrets in the given project.
    """

    # from google.cloud import secretmanager
    # Create the Secret Manager client:
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the parent project:
    parent = f"projects/{gcp_project_id_in}"

    for secret in client.list_secrets(request={"parent": parent}):
        print("*** Found secret: {}".format(secret.name))


# Based on https://cloud.google.com/secret-manager/docs/managing-secrets
# TODO: Getting details about a secret, Managing access to secrets,
# TODO: Updating a secret, Deleting a secret

if use_gcp:
    # Adapted from
    # https://codelabs.developers.google.com/codelabs/secret-manager-python#5
    # pip install -U google-cloud-secret-manager
    # from google.cloud import secretmanager  #
    # https://cloud.google.com/secret-manager/docs/reference/libraries
    # CAUTION: On FreeBSD and Mac OS X, putenv() setting environ may cause memory leaks. https://docs.python.org/2/library/os.html#os.environ

    gcp_project_id = get_from_env_file('GCP_PROJECT_ID')

    gcp_creds = get_from_env_file('GOOGLE_APPLICATION_CREDENTIALS')  # "path_to_json_credentials_file"
    
    my_secret_key="secret123a"  # format: [[a-zA-Z_0-9]+]
    my_secret_value="can't tell you"

    result = create_gcp_secret(gcp_project_id, my_secret_key)
    # Created secret: projects/<PROJECT_NUM>/secrets/my_secret_key

    # Each payload value of a secret key is a different version:
    result = add_gcp_secret_version(gcp_project_id,my_secret_key,my_secret_value)

    # Added secret version:
    result = add_gcp_secret_version(gcp_project_id, my_secret_key, my_secret_key)
        # google.api_core.exceptions.AlreadyExists: 409 Secret [projects/1070308975221/secrets/secret123] already exists.
    # projects/<PROJECT_NUM>/secrets/my_secret_key/versions/2

    result = hash_gcp_secret(access_secret_version(my_secret_key))
    # Example: 83f8a4edb555cde4271029354395c9f4b7d79706ffa90c746e021d11

    # Since previous call did not specify a version, the latest value is retrieved:
    result = hash_gcp_secret(access_secret_version(my_secret_key, version_id=2))

    # You should see the same output as the last command.
    # Call the function again, but this time specifying the first version:
    result = hash_gcp_secret(access_secret_version(my_secret_key, version_id=1))
    # You should see a different hash this time, indicating a different output:

    if show_verbose:
        list_gcp_secrets(gcp_project_id_in)


#### SECTION 17: Log into AWS using Pythong Boto3 library
 
aws_boto3_version = boto3.__version__
print_info("aws_boto3_version="+aws_boto3_version)  # example: 1.20.12



#### SECTION 17. Retrieve secrets from Hashicorp Vault

# Commentary on this at
# https://wilsonmar.github.io/python-samples#HashicorpVault

# After Add to python-samples.env

# Global static values (according to Security policies):
HASHICORP_VAULT_LEASE_DURATION = '1h'


def retrieve_secret():
    # Adapted from
    # https://fakrul.wordpress.com/2020/06/06/python-script-credentials-stored-in-hashicorp-vault/
    client = hvac.Client(VAULT_URL)
    read_response = client.secrets.kv.read_secret_version(path='meraki')

    url = 'https://api.meraki.com/api/v0/organizations/{}/inventory'.format(
        ORG_ID)
    MERAKI_API_KEY = 'X-Cisco-Meraki-API-Key'
    ORG_ID = '123456'  # TODO: Replace this hard coding.
    MERAKI_API_VALUE = read_response['data']['data']['MERAKI_API_VALUE']
    response = requests.get(
        url=url,
        headers={
            MERAKI_API_KEY: MERAKI_API_VALUE,
            'Content-type': 'application/json'})

    switch_list = response.json()
    switch_serial = []
    for i in switch_list:
        if i['model'][:2] in ('MS') and i['networkId'] is not None:
            switch_serial.append(i['serial'])

    print(switch_serial)


if use_hvac:
    # TODO: Make into function

    vault_url = get_from_env_file('VAULT_URL')
    vault_token = get_from_env_file('VAULT_TOKEN')

    hashicorp_vault_secret_path = "secret/snakes"

    # import os
    # import hvac  # https://github.com/hvac/hvac = Python client

    client = hvac.Client()
    client = hvac.Client(
        url=os.environ['VAULT_URL'],
        token=os.environ['VAULT_TOKEN'],
        cert=(client_cert_path, client_key_path),
        verify=server_cert_path
    )

    client.write(
        hashicorp_vault_secret_path,
        type='pythons',
        lease=HASHICORP_VAULT_LEASE_DURATION)

    if client.is_authenticated():
        print(client.read(hashicorp_vault_secret_path))
        # {u'lease_id': u'', u'warnings': None, u'wrap_info': None, u'auth': None, u'lease_duration': 3600, u'request_id': u'c383e53e-43da-d491-6c20-b0f5f7e4a33a', u'data': {u'type': u'pythons', u'lease': u'1h'}, u'renewable': False}


#### SECTION 18: Write secret to HashiCorp Vault per https://github.com/hashicorp/vault-examples/blob/main/examples/_quick-start/python/example.py


#### SECTION 19: Refresh certs crated by HashiCorp Vault

# Authentication
client = hvac.Client(
    url='http://127.0.0.1:8200',
    token='dev-only-token',
)
# Write a secret:
create_response = client.secrets.kv.v2.create_or_update_secret(
    path='my-secret-password',
    # secret=dict(password='Hashi123'),
)

print('Secret written successfully.')

# Reading a secret
read_response = client.secrets.kv.read_secret_version(path='my-secret-password')

password = read_response['data']['data']['password']

if password != 'Hashi123':
    sys.exit('unexpected password')

print('Access granted!')



#### SECTION 18. Create/Reuse folder for img app to put files:

img_directory = "Images"   # FIXME

if download_imgs:
    # Sets :

    if img_set == "small_ico":
        img_url = "http://google.com/favicon.ico"
        img_file_name = "google.ico"

    elif img_set == "big_mp4":
        # Big 7,376,089' byte mp4 file:
        img_url = 'https://aspb1.cdn.asset.aparat.com/aparat-video/a5e07b7f62ffaad0c104763c23d7393215613675-360p.mp4?wmsAuthSign=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbiI6IjUzMGU0Mzc3ZjRlZjVlYWU0OTFkMzdiOTZkODgwNGQ2IiwiZXhwIjoxNjExMzMzMDQxLCJpc3MiOiJTYWJhIElkZWEgR1NJRyJ9.FjMi_dkdLCUkt25dfGqPLcehpaC32dBBUNDC9cLNiu0'
        img_file_name = "play.mp4"

    elif img_set == "zen_txt":   # Used by paragraphs.py:
        img_url = "https://www.pythontutorial.net/wp-content/uploads/2020/10/the-zen-of-python.txt"
        img_file_name = "the-zen-of-python.txt"

    elif img_set == "lorem_5":
        # Website that obtain "Lorem Ipsum" placeholder text commonly used for
        # previewing layouts and visual mockups.
        img_url = "https://baconipsum.com/api/?type=meat-and-filler&sentences=3&start-with-lorem=1&format=text"
        img_file_name = "Lorem_ipson_5.txt"

        # type: all-meat for meat only or meat-and-filler for meat mixed with miscellaneous ‘lorem ipsum’ filler.
        # paras: optional number of paragraphs, defaults to 5. Blank line in between paragraphs
        # sentences: number of sentences (this overrides paragraphs)
        # start-with-lorem: optional pass 1 to start the first paragraph with ‘Bacon ipsum dolor sit amet’.
        # format: ‘json’ (default), ‘text’, or ‘html’

    # TODO: QR Code Generator https://www.qrcode-monkey.com/qr-code-api-with-logo/ for url to mobile authenticator app (Google) for MFA
        # import pyqrcode - https://github.com/mindninjaX/Python-Projects-for-Beginners/blob/master/QR%20code%20generator/QR%20code%20generator.py
    # TODO: Generate photo of people who don't exist.

    else:
        print(
            f'***{bcolors.FAIL} img_set \"{img_set}\" not recognized in coding!{bcolors.RESET}')
        exit(1)

    img_project_root = get_from_env_file('IMG_PROJECT_ROOT')  # $HOME (or ~) folder
    # FIXME: If it's blank, use hard-coded default

    # under user's $HOME (or ~) folder
    img_project_folder = get_from_env_file('IMG_PROJECT_FOLDER')
    # FIXME: If it's blank, use hard-coded default

    # Convert "$HOME" or "~" (tilde) in IMG_PROJECT_PATH to "/Users/wilsonmar":
    if "$HOME" in img_project_root:
        img_project_root = Path.home()
    elif "~" in img_project_root:
        img_project_root = expanduser("~")
    img_project_path = str(img_project_root) + "/" + img_project_folder
    if show_verbose:
        # macOS "$HOME/Projects" or on Windows: D:\\Projects
        print(f'*** {localize_blob("Path")}: \"{img_project_path}\" ')

    if path.exists(img_project_path):
        formatted_epoch_datetime = format_epoch_datetime(os.path.getmtime(img_project_path))
        if show_verbose:
            print(
                f'*** {localize_blob("Directory")} \"{img_directory}\" {localize_blob("created")} {formatted_epoch_datetime}')
        # FIXME: dir_tree( img_project_path )  # List first 10 folders
        # TODO: Get file creation dates, is platform-dependent, differing even
        # between the three big OSes.

        if remove_img_dir_at_beg:
            if verify_manually:  # Since this is dangerous, request manual confirmation:
                Join = input(
                    'Delete a folder used by several other programs?\n')
                if Join.lower() == 'yes' or Join.lower() == 'y':
                    dir_remove(img_project_path)
            else:
                dir_remove(img_project_path)

    try:
        # Create recursively, per
        # https://www.geeksforgeeks.org/create-a-directory-in-python/
        os.makedirs(img_project_path, exist_ok=True)
        # Alternative: os.mkdir(img_parent_path)
        os.chdir(img_project_path)  # change to directory.
    except OSError as error:
        print(f'***{bcolors.FAIL} {localize_blob("Directory path")} \"{img_file_name}\" {localize_blob("cannot be created")}.{bcolors.RESET}')
        print(error)

    # print (f'*** {localize_blob("Present Working Directory")}: \"{os.getcwd()}\" ')


#### SECTION 19. Download img application files  = download_imgs

# Commentary on this at
# https://wilsonmar.github.io/python-samples#download_imgs

if download_imgs:
    print_heading("download_imgs")

    # STEP: Get current path of the script being run:
    img_parent_path = pathlib.Path(
        __file__).parent.resolve()  # for Python 3 (not 2)
    # NOTE: The special variable _file_ contains the path to the current file.
    if show_verbose:
        print("*** Script executing at path: '% s' " % img_parent_path)
    # img_parent_path=os.path.dirname(os.path.abspath(__file__))  # for Python 2 & 3
    # print("*** Script executing at path: '% s' " % img_parent_path )

    # STEP: TODO: Create a Projects folder (to not clutter the source code
    # repository)

    # STEP: Show target directory path for download:

    img_project_path = os.path.join(img_parent_path, img_directory)

    if show_verbose:
        print("*** Downloading to directory: '% s' " % img_project_path)
    if path.exists(img_directory):
        formatted_epoch_datetime = format_epoch_datetime(
            os.path.getmtime(img_project_path))
        print(f'*** {localize_blob("Directory")} \"{img_directory}\" {localize_blob("created")} {formatted_epoch_datetime}')
        dir_tree(img_project_path)
        # NOTE: Getting file creation dates, is platform-dependent, differing
        # even between the three big OSes.
        if remove_img_dir_at_beg:
            dir_remove(img_project_path)
    try:
        # Create recursively, per
        # https://www.geeksforgeeks.org/create-a-directory-in-python/
        os.makedirs(img_project_path, exist_ok=True)
        # os.mkdir(img_parent_path)
    except OSError as error:
        print(
            f'***{bcolors.FAIL} Directory path \"{img_file_name}\" cannot be created.{bcolors.RESET}')
        print(error)

    # STEP: Show present working directory:
    # About Context Manager:
    # https://stackoverflow.com/questions/6194499/pushd-through-os-system
    os.chdir(img_project_path)
    # if show_verbose == True:
    #    print (f'*** {localize_blob("Present Working Directory")}: \"{os.getcwd()}\" ')

    # STEP: Download file from URL:

    img_file_path = os.path.join(img_project_path, img_file_name)
    if show_verbose:
        print("*** Downloading to file path: '% s' " % img_file_path)
    if path.exists(img_file_path) and os.access(img_file_path, os.R_OK):
        if remove_img_file_at_beg:
            if show_verbose:
                print(
                    f'*** {localize_blob("File being removed")}: {img_file_path} ')
            file_remove(img_file_path)
        else:
            if show_verbose:
                print(
                    f'***{bcolors.WARNING} No downloading as file can be accessed.{bcolors.RESET}')
    else:
        if show_verbose:
            print("*** Downloading from url: '% s' " % img_url)
        # Begin perf_counter_ns()  # the nanosecond version of perf_counter().
        tic = time.perf_counter()

        # urllib.urlretrieve(img_url, img_file_path)  # alternative.
        file_requested = requests.get(img_url, allow_redirects=True)
        headers = requests.head(img_url, allow_redirects=True).headers
        print("*** content_type: '% s' " % headers.get('content-type'))
        open(img_file_name, 'wb').write(file_requested.content)
        # NOTE: perf_counter_ns() is the nanosecond version of perf_counter().

    # STEP: Show file size if file confirmed to exist:

    if path.exists(img_file_path):
        toc = time.perf_counter()
        if show_verbose:
            # FIXME: took = toc - tic:0.4f seconds
            # took=""
            print(
                f'*** Download of {format_number( os.path.getsize(img_file_path))}-byte {img_file_name} ')
            # On Win32: https://stackoverflow.com/questions/12521525/reading-metadata-with-python
            # print(os.stat(img_file_path).st_creator)
    else:
        print(
            f'***{bcolors.FAIL} File {img_file_name} not readable.{bcolors.RESET}')
        # no exit()


#### SECTION 20. Manipulate image (OpenCV OCR extract)    = process_img

"""
# if process_img:
# Based on https://www.geeksforgeeks.org/python-read-blob-object-in-python-using-wand-library/

# import required libraries
from __future__ import print_function

# import Image from wand.image module
from wand.image import Image

# open image using file handling
with open('koala.jpeg') as f:

    # get blob from image file
    image_blob = f.read()

# read image using wand from blob file
with Image(blob = image_binary) as img:

    # get height of image
    print('height =', img.height)

    # get width of image
    print('width =', img.width)
"""


#### SECTION 21. Send message to Slack = send_slack_msgs

# TODO: Send Slack message - https://keestalkstech.com/2019/10/simple-python-code-to-send-message-to-slack-channel-without-packages/
#   https://api.slack.com/methods/chat.postMessage

def post_message_to_slack(text, blocks=None):
    return requests.post('https://slack.com/api/chat.postMessage', {
        'token': slack_token,
        'channel': slack_channel,
        'text': text,
        'icon_emoji': slack_icon_emoji,
        'username': slack_user_name,
        'blocks': json.dumps(blocks) if blocks else None
    }).json()
    del os.environ["SLACK_TOKEN"]  # remove


def post_file_to_slack(
    text, file_name, file_bytes, file_type=None, title=None
):
    return requests.post(
        'https://slack.com/api/files.upload',
        {
            'token': slack_token,
            'filename': file_name,
            'channels': slack_channel,
            'filetype': file_type,
            'initial_comment': text,
            'title': title
        },
        files={'file': file_bytes}).json()

    # image = "https://images.unsplash.com/photo-1495954484750-af469f2f9be5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80"
    # response = urllib.request.urlopen(image)
    # data = response.read()
    # post_file_to_slack('Amazing day at the beach. Check out this photo.', 'DayAtTheBeach.jpg', data)


class TestSendSlack(unittest.TestCase):
    def test_send_slack(self):
        if send_slack:
            print_heading("send_slack")

            slack_token = get_from_env_file('SLACK_TOKEN')       # This is a secret and should not be here
            slack_user_name = get_from_env_file('SLACK_USER_NAME')   # 'Double Images Monitor'
            slack_channel = get_from_env_file('SLACK_CHANNEL')     # #my-channel'
            slack_icon_url = get_from_env_file('SLACK_ICON_URL')
            slack_icon_emoji = get_from_env_file('SLACK_ICON_EMOJI')  # ':see_no_evil:'
            slack_text = get_from_env_file('SLACK_TEXT')

            double_images_count = 0
            products_count = 0
            bucket_name = 0
            file_name = "my.txt"

            slack_info = 'There are *{}* double images detected for *{}* products. Please check the <https://{}.s3-eu-west-1.amazonaws.com/{}|Double Images Monitor>.'.format(
                double_images_count, products_count, bucket_name, file_name)

            # post_message_to_slack(slack_info)
            #post_file_to_slack( 'Check out my text file!', 'Hello.txt', 'Hello World!')

            # PROTIP: When Slack returns a request as invalid, it returns an HTTP 200 with a JSON error message:
            # {'ok': False, 'error': 'invalid_blocks_format'}


#### SECTION 22. Send email thru Gmail         = email_via_gmail

# Inspired by
# https://www.101daysofdevops.com/courses/101-days-of-devops/lessons/day-14/

def verify_email_address( to_email_address ):
    if verify_email:
        # First, get API from https://mailboxlayer.com/product
        verify_email_api = get_from_env_file('MAILBOXLAYER_API')
        del os.environ["MAILBOXLAYER_API"]
        # https://apilayer.net/api/check?access_key = YOUR_ACCESS_KEY & email = support@apilayer.com
        url = "http://apilayer.net/api/check?access_key=" + verify_email_api + \
            "&email=" + to_email_address + \
            "&smtp=1&format=1"  # format=1 for JSON response
        print_trace(url)
        result = requests.get(url, allow_redirects=False)
        print_trace( result )
        if result:
            return True
        else:
            return False


def smtplib_sendmail_gmail(to_email_address, subject_in, body_in):
    # subject_in = "hello"
    # body_in = "testing ... "
    # "loadtesters@gmail.com" # Authenticate to google (use a separate gmail account just for this)
    from_gmail_address = get_from_env_file('THOWAWAY_GMAIL_ADDRESS')
    from_gmail_password = get_from_env_file('THOWAWAY_GMAIL_PASSWORD')  # a secret
    
    if show_trace:
        print(
            f'*** send_self_gmail : from_gmail_address={from_gmail_address} ')
    message = f'Subject: {subject_in}\n\n {body_in}'
    if True:  # try:
        import smtplib
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()  # start TLS to encrypt traffic

        response = s.login(from_gmail_address, from_gmail_password)
            # Response expected = (235, '2.7.0 Accepted')
        del os.environ["THOWAWAY_GMAIL_ADDRESS"]
        del os.environ["THOWAWAY_GMAIL_PASSWORD"]  # remove
        text_msg="Gmail login response=" + str(response)
        print_trace(text_msg)

        ok_to_email = verify_email_address( to_email_address )
        if not ok_to_email:
            print_fail("Not OK to email.")
        else:
            try:
                result = s.sendmail(from_gmail_address, to_email_address, message)  
                         # FROM addr, TO addr, message
                # To avoid this error response: Allow less secure apps: ON - see https://support.google.com/accounts/answer/6010255
                # smtplib.SMTPAuthenticationError: (535, b'5.7.8 Username and Password not accepted. Learn more at\n
                # 5.7.8  https://support.google.com/mail/?p=BadCredentials
                # nm13sm5582986pjb.56 - gsmtp')
                print(result)  # RESPONSE: <Response [200]>
            except Exception as e:
                print(f'*** sendmail() error! Quitting. ')
                s.quit()
            
    # FIXME: ResourceWarning: Enable tracemalloc to get the object allocation traceback

    # TODO: For attachments, see
    # https://github.com/Mohamed-S-Helal/Auto-gmail-draft-pdf-attatching/blob/main/gmailAPI.py


class TestSendEmail(unittest.TestCase):
    def test_email_via_gmail(self):
        if email_via_gmail:
            print_heading("email_via_gmail")

            to_gmail_address = get_from_env_file('TO_EMAIL_ADDRESS')  # static not a secret
            subject_text = "Hello from " + program_name  # Customize this!
            if True:  # TODO: for loop through email addresses and text in file:

                # Optionally, add datestamp to email body:
                trans_datetime = str(_datetime.datetime.fromtimestamp(
                    time.time()))  # Default: 2021-11-20 07:59:44.412845
                body_text = "Please call me. It's now " + trans_datetime

                if show_heading:
                    print(
                        f'***{bcolors.HEADING} email_via_gmail : {trans_datetime} {bcolors.RESET}')

                smtplib_sendmail_gmail(to_gmail_address, subject_text, body_text)
                
                # Loop to get next for 


#### SECTION 23. Calculate Hash and View Gravatar on Web Browser   = view_gravatar


def get_gravatar_url(email, size, default, rating):
    # Commentary of this is at https://wilsonmar.github.io/python-samples#view_gravatar
    hash = hashlib.md5(email.encode('utf-8')).hexdigest()
    url = "https://secure.gravatar.com/avatar/"
    
    # Validate size up to 2048px, rating G,PG,R,X per https://en.gravatar.com/site/implement/images/
    # PROTIP: Check if a data type is numeric before doing arithmetic using it.
    if not isinstance(size, int):   # if ( type(size) != "<class 'int'>" ):
        size=int(size)
    if ( size > 2048 ):
        print_fail("Parameter size cannot be more than 2048px. Set to 100.")
        size = 100
    rating = rating.upper()
    if rating not in {"G","PG","R","X"}:
        print_fail('Rating " + rating_in + " not recognized. Set to "G". ')
        rating = "G"
    
    url_string = url + hash +"&size="+ str(size) +"&d="+ default +"&r="+ rating
    return url_string


class TestViewGravatar(unittest.TestCase):
    def test_view_gravatar(self):

        if view_gravatar:
            print_heading("view_gravatar")

            # TODO: Alternately, obtain from user parameter specification:
            some_email=get_from_env_file('MY_EMAIL')  # "johnsmith@example.com"
            print_verbose( some_email)
            some_email_gravatar=""

            if not some_email_gravatar:
                url_string = get_gravatar_url( some_email, size="100", default='identicon', rating='G')            
                print_info(url_string)
                # Save gravatar_url associated with email so it won't have to be created again:
                some_email_gravatar = url_string

            import webbrowser
            print_verbose("Opening web browser to view gravatar image of "+ some_email)
            webbrowser.open(some_email_gravatar, new=2)
                # new=2 opens the url in a new tab. Default new=0 opens in an existing browser window. 
                # See https://docs.python.org/2/library/webbrowser.html#webbrowser.open


# 
#### SECTION 24. Generate BMI  = categorize_bmi

class TestGemBMI(unittest.TestCase):
    def test_categorize_bmi(self):

        if categorize_bmi:
            print_heading("categorize_bmi")

            # WARNING: Hard-coded values:
            # TODO: Get values from argparse of program invocation parameters.

            # PROTIP: Variables containing measurements should be named with
            # the unit.

            # Based on https://www.babbel.com/en/magazine/metric-system
            # and
            # https://www.nist.gov/blogs/taking-measure/busting-myths-about-metric-system
            # US, Myanmar (MM), Liberia (LR) are only countries not using
            # metric:
            if my_country in ("US", "MM", "LR"):
                # NOTE: Liberia and Myanmar already started the process of
                # “metrication.”
                if my_country == "MM":
                    country_name = "for Myanmar (formerly Burma)"
                elif my_country == "LR":
                    country_name = "for Liberia"
                else:
                    country_name = ""
                text_to_print = "Using US(English) system of measurement " + \
                    country_name
                print_verbose(text_to_print)
                height_inches = 67   # 5 foot * 12 = 60 inches
                weight_pounds = 203  # = BMI 31
                print_warning("Using hard-coded input values.")

                # TODO: Convert: 1 kilogram = 2.20462 pounds. cm = 2.54 *
                # inches.
                # input("Enter your height in cm: "))
                height_cm = float(height_inches * 2.54)
                # input("Enter your weight in kg: "))
                weight_kg = float(weight_pounds * 0.453592)
            else:  # all other countries:
                print_verbose("Using metric (International System of Units):")
                height_cm = 170
                weight_kg = 92
                print_warning("Using hard-coded input values.")

                height_inches = float(height_cm / 2.54)
                weight_pounds = float(weight_kg / 0.453592)

            # Show input in both metric and English:
            print(
                f'*** height_inches={height_inches} weight_pounds={weight_pounds} ')
            print(f'*** height_cm={height_cm} weight_kg={weight_kg} ')

            # TODO: PROTIP: Check if cm or kg based on range of valid values:
            # BMI tables at https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmi_tbl2.htm
            # Has height from 58 (91 pounds) to 76 inches for BMI up to 54 (at
            # 443 pounds)

            # PROTIP: Format the number immediately if there is no use for full floating point.
            # https://www.nhlbi.nih.gov/health/educational/lose_wt/BMI/bmicalc.htm
            # https://www.cdc.gov/healthyweight/assessing/bmi/Index.html
            # https://en.wikipedia.org/wiki/Body_mass_index

            # if height_inches > 0:
            # BMI = ( weight_pounds / height_inches / height_inches ) * 703  #
            # BMI = Body Mass Index
            if height_cm > 0:  # https://www.cdc.gov/nccdphp/dnpao/growthcharts/training/bmiage/page5_1.html
                BMI = (weight_kg / height_cm / height_cm) * 10000
            if BMI < 16:
                print(f'*** categorize_bmi ERROR: BMI of {BMI} lower than 16.')
            elif BMI > 40:
                print(
                    f'*** categorize_bmi ERROR: BMI of {BMI} higher than 40.')
            BMI = round(int(BMI), 1)  # BMI = Body Mass Index

            # PROTIP: Ensure that the full spectrum of values are covered in if
            # statements.
            if BMI == 0:
                category_text = 'ERROR'
            elif BMI <= 18.4:
                category_text = '(< 18.4) = ' + localize_blob('Underweight')
            elif BMI <= 24.9:
                category_text = '(18.5 to 24.9) = ' + \
                    localize_blob('Healthy')
            elif BMI <= 29.9:
                category_text = '(25 to 29.9) = ' + localize_blob('Overweight')
            elif BMI <= 34.9:
                category_text = '(30 to 34.9) = ' + \
                    localize_blob('Moderately Obese (class 1)')
            elif BMI <= 39.9:
                category_text = '(35 to 39.9) = ' + \
                    localize_blob('Severely Obese (class 2)')
            else:
                category_text = '(40 or above) = ' + \
                    localize_blob('Morbidly Obese (class 3)')

            text_to_show = "BMI " + str(BMI) + " " + category_text
            print_info(text_to_show)

            # TODO: Calculate weight loss/gain to ideal BMI of 21.7 based on height (discounting all other factors).
            # 138 = 21.7 / 703 = 0.030867709815078  # http://www.moneychimp.com/diversions/bmi.htm
            # ideal_pounds = ( 21.7 / 703 / weight_pounds ) * height_inches
            # print(f'*** Ideal weight at BMI 21.7 = {ideal_pounds} pounds.')


#### SECTION 97. Play text to sound:

# https://cloud.google.com/text-to-speech/docs/quickstart-protocol

if gen_sound_for_text:
    print_heading("gen_sound_for_text")

    my_accent=get_from_env_file('MY_ACCENT')
    if not my_accent:
        my_accent="en"  # or "en" "uk" "fr" (for English with French accent)
    text_from_env = get_from_env_file('TEXT_TO_SAY')
    if not text_from_env:
        text_from_env="hello world!"
    from gtts import gTTS            # pip install -upgrade gtts
    s = gTTS(text=text_from_env, lang=my_accent)

    speech_file_name = get_from_env_file('SPEECH_FILE_NAME')
    if not speech_file_name:
        speech_file_name="speech.mp3"
    s.save(speech_file_name)  # generate mp3 file.
    
    # Alternate 1:
    # On a Mac, double-clicking on the mp3 file by default invokes Apple Music app:
       # so NO: os.system(f'start {speech_file_name}')
    
    # Alternate 2:  # pip install -U playsound
    import playsound
    playsound.playsound(speech_file_name, True)

    # Alternate 3:  # pip install -U pyttsx3
    #import pyttsx3
    #engine = pyttsx3.init()
    #engine.say
    
    # Alternate 4:
    # from playsound import playsound  # pip install -upgrade playsound
    # playsound(speech_file_name)

    # Remove file:
    if remove_sound_file_generated:
        os.remove(speech_file_name)


#### SECTION 98. Remove (clean-up) folder/files created   = cleanup_files
if cleanup_img_files:
    # Remove files and folders to conserve disk space and avoid extraneous
    # files:

    if remove_img_dir_at_end:
        if verify_manually:  # Since this is dangerous, request manual confirmation:
            Join = input('Delete a folder used by several other programs?\n')
            if Join.lower() == 'yes' or Join.lower() == 'y':
                dir_remove(img_project_path)
        else:
            dir_remove(img_project_path)

    if remove_img_file_at_end:
        if show_verbose:
            print(
                f'*** {localize_blob("File")} \"{img_file_path}\" {localize_blob("being removed")} ')
        file_remove(img_file_path)

    if show_verbose:
        print(f'*** After this run: {img_project_path} ')
        dir_tree(img_project_path)


#### SECTION 99. Display run stats at end of program       = display_run_stats


class TestDisplayRunStats(unittest.TestCase):
    def test_display_run_stats(self):

        if display_run_stats:
            print_heading("display_run_stats")

            # Compare for run duration:
            stop_run_time = time.monotonic()
            stop_epoch_time = time.time()
            stop_datetime = _datetime.datetime.fromtimestamp(stop_epoch_time)  # Default: 2021-11-20 07:59:44.412845
            # if show_info == True:
            #    print(f'*** {localize_blob("Ended")} {stop_run_time.strftime(my_date_format)} ')
            #print(f'*** {localize_blob("Ended")} {stop_datetime.strftime(my_date_format)} ')

            run_time_duration = stop_run_time - start_run_time
            print(type(run_time_duration))  # <class 'datetime.timedelta'>
            if show_info:
                print(
                    f'*** {program_name} done in {round( run_time_duration, 2 )} seconds clock time. ')



#########################################################################

if __name__ == '__main__':
    unittest.main()
    # Automatically invokes all functions within classes which inherits (unittest.TestCase):
    # Example: class TestMakeChange(unittest.TestCase):
    # The setup() is run, then all functions starting with "test_".

# END