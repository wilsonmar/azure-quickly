#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "azure-keyvault-secrets",
#   "azure-ai-textanalytics",
#   "azure-ai-projects", 
#   "azure-functions",
#   "azure-identity",
#   "azure-maps-search",
#   "azure-maps-timezone",
#   "azure-mgmt-billing",
#   "azure-mgmt-consumption",
#   "azure-mgmt-costmanagement",
#   "azure-mgmt-resource",
#   "azure-mgmt-keyvault",
#   "azure-mgmt-storage",
#   "azure-storage-blob",
#   "click",
#   "opentelemetry-api",
#   "opentelemetry-sdk",
#   "python-dotenv",
#   "psutil",
#   "pythonping",
#   "requests",
#   "tabulate",
# ]
# ///
# https://docs.astral.sh/uv/guides/scripts/#using-a-shebang-to-create-an-executable-file
#   "pprint",
#   "threema-gateway",
#   "libnacl",
#   "pynacl",

# Azure KeyVault SDK components imported below in SECTION 03

"""az-utils.py here.

at https://github.com/wilsonmar/azure-quickly/blob/main/az-utils.py
by Wilson Mar

Utilities for using Microsoft's Azure Python SDK and Microsoft Authentication Library (MSAL) for Python
to calculate the least-cost, closest, and/or fastest region to you.
Thie program obtains Region Latitude/Longitude automatically.

This integrates with the Microsoft identity platform. It allows you to sign in users or apps with Microsoft identities (Microsoft Entra ID, External identities, Microsoft Accounts and Azure AD B2C accounts) and obtain tokens to call Microsoft APIs such as Microsoft Graph or your own APIs registered with the Microsoft identity platform. 
It is built using industry standard OAuth2 and OpenID Connect protocols.    
    
TODO: sets access policies and premissions to control actions in this program.
See https://pypi.org/project/azure-mgmt-keyvault/
to obtain for an account's email its Subscription Id and Tenant Id needed to
create resources, storage accounts, Key Vault, secrets, Functions.
Based on https://www.perplexity.ai/search/how-to-create-populate-and-use-Q4EyT9iYSSaVQtyUK5N31g#0

#### Before running this program:
### Prerequisites:
1. Create an .env file defining global static variables and their secret values (Account, Subscription, Tenant ID)
2. Use your email address, phone, credit card to create an account and log into Azure Portal.
3. In "Entra Admin Center" (previously Azure Active Directory) https://entra.microsoft.com/#home
4. Get a Subscription Id and Tenant Id to place in the .env file

   AIPROJECT_CONNECTION_STRING=<your-connection-string>
   See https://learn.microsoft.com/en-us/azure/ai-foundry/tutorials/copilot-sdk-create-resources?tabs=macos

5. Create a new Azure AD Enterprise application. Store the Application (client) ID in your .env file.
6. Get the app's Service Principal Id, which is similar to a user account but to access resources used by apps & services.
   See https://learn.microsoft.com/en-us/entra/architecture/service-accounts-principal
7. In CLI, get a long list of info about your account from:
   az ad sp list   # For its parms: https://learn.microsoft.com/en-us/powershell/module/microsoft.graph.applications/get-mgserviceprincipal?view=graph-powershell-1.0

    "appDisplayName": "Cortana Runtime Service",
    "appId": "??473081-50b9-469a-b9d8-303109583ecb",
    ...
       "servicePrincipalNames": [
      "??473081-50b9-469a-b9d8-303109583ecb",
      "https://cortana.ai"
    ],

?. Deploy your app with CLI command: az webapp up --runtime PYTHON:3.9 --sku B1 --logs

?. In https://entra.microsoft.com/#view/Microsoft_AAD_IAM/StartboardApplicationsMenuBlade/~/AppAppsPreview
   Click on your app in the list.
?. Under Properties, Copy the Service Principal Object ID to save the value in your .env file.
   The client_id = Application (client) ID assigned to your Azure AD app registration (service principal).
   It's required when authenticating your app or service principal programmatically.

?. Define RBAC to each Service Principal

uv python install 3.12
# See https://realpython.com/python-pyproject-toml/ & https://realpython.com/python-uv/

source .venv/bin/activate

# Repeat this CLI command after customizing with the email you use for Azure:
uv run az-utils.py -v -vv -u "wmar@joliet.k12.mt.us"

PROTIP: Each function displays its own error messages. Function callers display expected responses.

REMEMBER on CLI after running uv run az-utils.py: deactivate

https://udemy.com/course/python-sdk-for-azure-bootcamp/ by Benjamin Bigelow at Pierian Training Jun 2023
https://support.udemy.com/hc/en-us/articles/229604708-Downloading-Course-Resources

USAGE:
    # Add /.venv/ to .gitignore (for use by uv, instead of venv)
    deactivate       # out from within venv
    brew install uv  # new package manager
    brew install libsodium
    uv add pynacl, libsodium
    uv --help
    uv init   # for pyproject.toml & .python-version files https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
    uv lock
    uv sync
    uv venv  # to create an environment,
    python -m venv .venv
    source .venv/bin/activate
        ./scripts/activate       # PowerShell only
        ./scripts/activate.bat   # Windows CMD only
    uv run az-utils.py --lat 47.6204 --long -122.3491 -v    # For Seattle Space Needle
    uv run az-utils.py -v                                   # For .env file
    pip-audit -r requirements.txt
    ruff check az-utils.py
"""

#### SECTION 01. Metadata about this program file:

__last_commit__ = "25-10-13 v004 + address from lat long :az-utils.py"
__status__      = "Run info, Resource lists working on macOS Sequoia 15.3.1"

#### SECTION 02: Import internal libraries already built-in into Python:

# listed at https://docs.python.org/3/library/*.html
from datetime import datetime, timezone
import argparse
import base64
# import boto3  # for aws python
#from collections import OrderedDict
from dotenv import load_dotenv   # install python-dotenv
import functools
import http.client
import json
import logging   # see https://realpython.com/python-logging/
import math
import os
from pathlib import Path
import platform # https://docs.python.org/3/library/platform.html
import pwd                # https://www.geeksforgeeks.org/pwd-module-in-python/
import site
import shutil     # for disk space calcs
import socket
import subprocess
import sys
import time  #from time import perf_counter_ns   # for timestamp 
#import urllib.request
#from urllib import parse #request, error
import uuid
#from zoneinfo import ZoneInfo  # For Python 3.9+ 

# See https://wilsonmar.github.io/python-features/#StartingTime


#### SECTION 03: Import external library (from outside this program):

xpt_strt_timestamp =  time.monotonic()

# Fix SSL certificate verification issues on macOS (thank you Warp!)
try:
    import certifi
    #import ssl     # consider using `importlib.util.find_spec` to test for availability
    # Set certificate bundle paths for requests and urllib
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    os.environ['CURL_CA_BUNDLE'] = certifi.where()
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    # Fallback to system certificates if certifi is not available
    pass

try:   # These should match the uv list at top of this file.
    #import argparse
    #import asyncio
    from azure.ai.textanalytics import TextAnalyticsClient
    #    azure-ai-projects 
    from azure.core.exceptions import HttpResponseError, ClientAuthenticationError
    from azure.core.credentials import AzureKeyCredential
    from azure.identity import DefaultAzureCredential
    from azure.identity import ClientSecretCredential
    #from azure.identity import AzureCliCredential  # for local only. Do not use!

    import azure.functions as func
    from azure.keyvault.secrets import SecretClient
    from azure.maps.search import MapsSearchClient
    from azure.maps.timezone import MapsTimeZoneClient
    from azure.mgmt.billing import BillingManagementClient
                                 # accounts, profiles (payment), customers, invoices
    from azure.mgmt.costmanagement import CostManagementClient, models
    #from azure.mgmt.consumption import ConsumptionManagementClient
    # from azure.mgmt.consumption import models  # F811 Redefinition of unused `models`
    from azure.mgmt.resource import ResourceManagementClient
    from azure.mgmt.resource.resources.models import TagsResource
    from azure.mgmt.keyvault import KeyVaultManagementClient
    from azure.mgmt.resource import SubscriptionClient
    from azure.mgmt.storage import StorageManagementClient
    
    from azure.storage.blob import BlobServiceClient  # noqa
    # from msgraph.core import GraphClient   # doesn't work if included?
    # See https://github.com/AzureAD/microsoft-authentication-library-for-python?tab=readme-ov-file
    # NOT msgraph-core           # for msgraph.core.GraphClient

    #import click
    from opentelemetry import trace   # opentelemetry-api 
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

    #from click_default_group
    #import pandas as pd
    from pathlib import Path
    import pprint
    import psutil  #  psutil-5.9.5
    from pythonping import ping
    #import pytz   # time zones
    import requests
    from tabulate import tabulate 
    #from threema.gateway import ( Connection, GatewayError, util, )  # to send_theema_msg()
    import uuid
except Exception as e:
    print(f"Python module import failed: {e}")
    # pyproject.toml file exists
    print("Please uv add library, then activate your virtual environment:\n")
    print("\n  uv venv .venv\n  source .venv/bin/activate\n  uv add ___")
    print("\n  uv run az-utils.py")
    exit(9)
xpt_stop_timestamp =  time.monotonic()


#print(f"threema.gateway version: {threema.connection.__version__}")
                                        
# To display wall clock date & time of program start:
# pgm_strt_datetimestamp = datetime.now() has been deprecated.
pgm_strt_timestamp = time.monotonic()

# TODO: Display Z (UTC/GMT) instead of local time
pgm_strt_epoch_timestamp = time.time()
pgm_strt_local_timestamp = time.localtime()
# NOTE: Can't display the dates until formatting code is run below


#### SECTION 04: Define default global variables, which are set to True using parms:

show_dates_in_logs = False
show_info = False
show_heading = False
show_fail = False
show_error = False
show_verbose = False
show_warning = False
show_todo = False
show_trace = False

show_secrets = False   # Never show
show_print_samples = False

#LOG_DOWNLOADS = args.log
CLI_PFX = ""
global_tags = {
    "Dept": "Finance",
    "Status": "Normal"
}

#### SECTION 05: Retry, logging, telemetry decorators:

def retry(f):
    """Add @retry above a function to automatically handle multiple types of exceptions.

    to improve robustness in scenarios with intermittent failures, such as network requests.
    Its options include the time of delay between retries (backoff).

    :param f: The target function to be decorated and retried when applicable.
    :type f: Callable
    :raises requests.exceptions.ConnectionError: Raised when a connection error occurs.
    :raises requests.exceptions.Timeout: Raised when a timeout error occurs.
    :raises Exception: Raised after the maximum number of retries if the exception persists.
    :return: The decorator function that wraps the target function with retry functionality.
    :rtype: Callable
    """
    def decorator(func):
        """Standard python @decorator for retries."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """Wrapper within decorator."""
            tries = 0
            delay = 2
            while True:
                try:
                    rc = func(*args, **kwargs)
                    return rc
                except exceptions as e:
                    print(f"[client:error] caught exception attempt #{tries + 1}: {type(e).__name__}: {e}")
                    tries += 1

                    if tries >= retries:
                        e.add_note(f"Retried function {func.__name__} {retries} times without success")
                        raise

                    if delay > 0:
                        time.sleep(delay)

        # start of decorator:
        exceptions = (requests.exceptions.ConnectionError, requests.exceptions.Timeout)
        retry_count = 3  # TODO: from parm?
        retries = retry_count
        return wrapper

    # start of retry
    return decorator(f)


# TODO: OpTel (OpenTelemetry) spans and logging:

def export_optel():
    """Create and export a trace to your console.

    https://www.perplexity.ai/search/python-code-to-use-opentelemet-bGjntbF4Sk6I6z3l5HBBSg#0
    """
    #from opentelemetry import trace
    #from opentelemetry.sdk.trace import TracerProvider
    #from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

    # Set up the tracer provider and exporter
    trace.set_tracer_provider(TracerProvider())
    span_processor = SimpleSpanProcessor(ConsoleSpanExporter())
    trace.get_tracer_provider().add_span_processor(span_processor)

    # Get a tracer:
    tracer = trace.get_tracer(__name__)

    # Create spans:
    with tracer.start_as_current_span("parent-span"):
        print_verbose("Doing some work in the parent span")
        with tracer.start_as_current_span("child-span"):
            print_verbose("Doing some work in the child span")


#### SECTION 06: Print Utility Python Functions:

class bcolors:
    """Set static ANSI color escape sequences for printing."""

    BOLD = '\033[1m'       # Begin bold text
    UNDERLINE = '\033[4m'  # Begin underlined text

    HEADING = '\033[37m'   # [37 white
    FAIL = '\033[91m'      # [91 red
    ERROR = '\033[91m'     # [91 red
    WARNING = '\033[93m'   # [93 yellow
    INFO = '\033[92m'      # [92 green
    VERBOSE = '\033[95m'   # [95 purple
    TRACE = '\033[96m'     # [96 blue/green
                 # [94 blue (bad on black background)
    CVIOLET = '\033[35m'
    CBEIGE = '\033[36m'
    CWHITE = '\033[37m'
    GRAY = '\033[90m'

    RESET = '\033[0m'   # switch back to default color

def print_separator():
    """A function to put a blank line in CLI output. Used in case the technique changes throughout this code."""
    print(" ")

def print_heading(text_in):
    """Print heading with uderlines."""
    if show_heading:
        if str(show_dates_in_logs) == "True":
            print('\n***', get_log_datetime(), bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)
        else:
            print('\n***', bcolors.HEADING+bcolors.UNDERLINE,f'{text_in}', bcolors.RESET)

def print_fail(text_in):
    """Print when program should stop."""
    if show_fail:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.FAIL, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.FAIL, f'{text_in}', bcolors.RESET)

def print_error(text_in):
    """Print when a programming error is evident."""
    if show_error:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.ERROR, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.ERROR, f'{text_in}', bcolors.RESET)

def print_warning(text_in):
    """Print warning to users."""
    if show_warning:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.WARNING, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.WARNING, f'{text_in}', bcolors.RESET)

def print_todo(text_in):
    """Print TODO item for developers."""
    if show_todo:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.CVIOLET, "TODO:", f'{text_in}', bcolors.RESET)

def print_info(text_in):
    """Print information for users."""
    if show_info:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.INFO+bcolors.BOLD, f'{text_in}', bcolors.RESET)

def print_verbose(text_in):
    """Print extra."""
    if show_verbose:
        if str(show_dates_in_logs) == "True":
            print('***', get_log_datetime(), bcolors.VERBOSE, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.VERBOSE, f'{text_in}', bcolors.RESET)

def print_trace(text_in):
    """Displayed as each object is created in pgm."""
    if show_trace:
        if str(show_dates_in_logs) == "True":
            print('***',get_log_datetime(), bcolors.TRACE, f'{text_in}', bcolors.RESET)
        else:
            print('***', bcolors.TRACE, f'{text_in}', bcolors.RESET)

def no_newlines(in_string):
    """Strip new line from in_string."""
    return ''.join(in_string.splitlines())

def print_datetime():
    """Print current date/time stamp."""
    # TODO:
    return ""

def print_secret(secret_in: str) -> None:
    """ Outputs secrets discreetly - display only the first few characters (like Git) with dots replacing the rest.
    """
    # See https://stackoverflow.com/questions/3503879/assign-output-of-os-system-to-a-variable-and-prevent-it-from-being-displayed-on
    if show_secrets:  # program parameter
        if show_dates_in_logs:
            now_utc=datetime.now(timezone('UTC'))
            print(bcolors.WARNING, CLI_PFX,now_utc,"SECRET: ", secret_in, bcolors.RESET)
        else:
            print(bcolors.CBEIGE, CLI_PFX, "SECRET: ", secret_in, bcolors.RESET)
    else:
        # same length regardless of secret length to reduce ability to guess:
        secret_len = 8
        if len(secret_in) >= 8:  # slice
            secret_out = secret_in[0:4] + "."*(secret_len-4)
        else:
            secret_out = secret_in[0:4] + "."*(secret_len-1)
            if show_dates_in_logs:
                print(bcolors.WARNING, CLI_PFX, print_datetime(), f'{secret_in}', bcolors.RESET)
            else:
                print(bcolors.CBEIGE, CLI_PFX, " SECRET: ", f'{secret_out}', bcolors.RESET)
    # NOTE: secrets should not be printed to logs.
    return None


def print_samples():
    """Display what different type of output look like."""
    # See https://wilsonmar.github.io/python-samples/#PrintColors
    if not show_print_samples:
        return None
    print_heading("show_print_samples")
    print_fail("sample fail")
    print_error("sample error")
    print_warning("sample warning")
    print_todo("sample task to do")
    print_info("sample info")
    print_verbose("sample verbose")
    print_trace("sample trace")
    print_secret("1234567890123456789")
    return True


#### SECTION 07: Parameters from call arguments:

# USAGE: uv run az-utils.py -kv "kv-westcentralus-897e56" -s "westcentralus2504" -v -vv

parser = argparse.ArgumentParser(description="Azure Key Vault")
parser.add_argument("-q", "--quiet", action="store_true", help="Quiet")
parser.add_argument("-v", "--verbose", action="store_true", help="Show each download")
parser.add_argument("-vv", "--debug", action="store_true", help="Show debug")
parser.add_argument("-l", "--log", help="Log to external file")

parser.add_argument("-ri", "--runid", action="store_true", help="Run ID (no spaces or special characters)")
parser.add_argument("-u", "--user", help="User email (for credential)")
parser.add_argument("-lat", "--lat", help="Latitude")
parser.add_argument("-long", "--long", help="Longitude")
# --tenant
parser.add_argument("-sub", "--subscription", help="Subscription ID (for costing)")
parser.add_argument("-z", "--zip", help="6-digit Zip code (in USA)")
parser.add_argument("-rg", "--resource", help="Resource Group Name")
parser.add_argument("-st", "--storage", help="Storage Name")
parser.add_argument("-kv", "--keyvault", help="KeyVault Namo")

parser.add_argument("-t", "--text", help="Text input (for language detection)")

# -h = --help (list arguments)
args = parser.parse_args()

#### SECTION 08: Edit global parameters:

RUNID = "R011"  # This value should have no spaces or special characters.
   # TODO: Store and increment externally each run (usign Python Generators?) into a database for tying runs to parmeters such as the PROMPT_TEXT, etc. https://www.linkedin.com/learning/learning-python-generators-17425534/

show_fail = True       # Always show
show_error = True      # Always show

SHOW_QUIET = args.quiet
if SHOW_QUIET:  # -vv
    show_warning = False   # -wx  Don't display warning
    show_todo = False      # -td  Display TODO item for developer
    show_info = False      # -qq  Display app's informational status and results for end-users
else:
    show_warning = True    # -wx  Don't display warning
    show_todo = True       # -td  Display TODO item for developer
    show_info = True       # -qq  Display app's informational status and results for end-users

SHOW_VERBOSE = args.verbose
if SHOW_VERBOSE:  # -vv
    SHOW_SUMMARY = True
    show_heading = True    # -q  Don't display step headings before attempting actions
    show_verbose = True    # -v  Display technical program run conditions
    show_sys_info = True
else:
    show_heading = False    # -q  Don't display step headings before attempting actions
    show_verbose = False   # -v  Display technical program run conditions
    show_sys_info = False

SHOW_DEBUG = args.debug  # print metadata before use by code during troubleshooting
if SHOW_DEBUG:  # -vv
    show_trace = True      # -vv Display responses from API calls for debugging code
else:
    show_trace = False     # -vv Display responses from API calls for debugging code

SHOW_SUMMARY_COUNTS = True

#if args.resource:
#    #AZURE_RESOURCE_GROUP = args.resource
#    resource_group = args.resource
#else:
#    resource_group = "westcentralus-92b065"
#print(f"resource_group = {resource_group}")

AZURE_ACCT_NAME = args.user
AZURE_SUBSCRIPTION_ID = args.subscription

AZURE_STORAGE_ACCOUNT = args.storage
AZURE_KEYVAULT_NAME = args.keyvault  # also used as resource group name

TEXT_INPUT = args.text
if not TEXT_INPUT:
    TEXT_INPUT = "The quick brown fox jumps over the lazy dog"

# if args.zip in get_longitude_latitude()

user_home_dir_path = str(Path.home())
env_file="python-samples.env"  # the hard-coded default
global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

# TODO: Make these configurable
DELETE_RG_AFTER = False
DELETE_KV_AFTER = False
LIST_ALL_PROVIDERS = False

# PROTIP: Global variable referenced within Python functions:
# values obtained from .env file can be overriden in program call arguments:


#### SECTION 09: Pull in external reference data:

# Python code to show regions of azure as a dictionary named AZURE_REGIONS with region name, latitude, longitude, with location with. Sort by region name.
AZURE_REGIONS = {                               # City/Town name
    "australiasoutheast": (-37.814, 144.963),   # Melbourne
    "australiacentral": (-35.282, 149.128),     # Canberra
    "australiacentral2": (-35.282, 149.128),    # Canberra
    "southafricawest": (-33.925, 18.423),       # Cape Town
    "australiaeast": (-33.865, 151.209),        # Sydney
    "southafricanorth": (-25.731, 28.218),      # Johannesburg
    "brazilsouth": (-23.55, -46.633),           # Sao Paulo
    "southeastasia": (1.283, 103.833),          # Singapore
    "southindia": (13.0827, 80.2707),           # Chennai
    "centralindia": (18.5204, 73.8567),         # Pune
    "jioindiacentral": (18.5204, 73.8567),      # Pune
    "westindia": (19.076, 72.8777),             # Mumbai
    "jioindiawest": (19.076, 72.8777),          # Mumbai
    "eastasia": (22.267, 114.188),              # Hong Kong
    "uaecentral": (24.466, 54.366),             # Abu Dhabi
    "uaenorth": (25.096, 55.174),               # Dubai
    "qatarcentral": (25.2854, 51.531),          # Doha
    "southcentralus": (29.4167, -98.5),         # Texas
    "isrealcentral": (31.046, 34.851),          # Jerusalem
    "chinaeast": (31.2304, 121.4737),           # Shanghai
    "chinaeast2": (31.2304, 121.4737),          # Shanghai
    "israelnorth": (32.0853, 34.7818),          # Tel Aviv
    "westus3": (33.448, -112.074),              # Arizona
    "japanwest": (34.6939, 135.5022),           # Osaka
    "koreasouth": (35.1796, 129.0756),          # Busan
    "japaneast": (35.68, 139.77),               # Tokyo
    "eastus2": (36.6681, -78.3889),             # Virginia, US
    "eastus": (37.3719, -79.8164),              # Virginia, US
    "koreacentral": (37.5665, 126.9780),        # Seoul
    "westus": (37.783, -122.417),               # California
    "chinanorth": (39.9042, 116.4074),          # Beijing
    "chinanorth2": (39.9042, 116.4074),         # Beijing
    "westcentralus": (40.89, -110.234),         # Wyoming
    "centralus": (41.5908, -93.6208),           # Iowa
    "northcentralus": (43.653, -92.332),        # Illinois
    "canadacentral": (43.653, -79.383),         # Toronto
    "francesouth": (43.7102, 7.2620),           # Marseille
    "italynorth": (45.4642, 9.19),              # Milan
    "switzerlandwest": (46.204, 6.143),         # Geneva
    "francecentral": (46.3772, 2.373),          # Paris
    "canadaeast": (46.817, -71.217),            # Quebec City
    "westus2": (47.233, -119.852),              # Washington
    "switzerlandnorth": (47.451, 8.564),        # Zurich
    "germanywestcentral": (50.11, 8.682),       # Frankfurt
    "uksouth": (51.5074, -0.1278),              # London
    "polandcentral": (52.2297, 21.0122),        # Warsaw
    "westeurope": (52.3667, 4.9),               # Amsterdam, Netherlands
    "ukwest": (52.4796, -1.9036),               # Cardiff
    "northeurope": (53.3478, -6.2597),          # Dublin, Ireland
    "germanynorth": (53.55, 10.0),              # Hamburg
    "swedencentral": (59.329, 18.068),          # Stockholm
    "norwayeast": (59.913, 10.752),             # Oslo
    "norwaywest": (60.391, 5.322),              # Bergen
}  # TODO: Occassionally update the lisit of Azure regions by scraping 
# Historical list: https://gist.github.com/ausfestivus/04e55c7d80229069bf3bc75870630ec8
# Tutorial https://dev.to/holger/python-list-all-current-and-planned-azure-regions-29pk
   # scape of url = 'https://azure.microsoft.com/en-us/explore/global-infrastructure/geographies/
# print_trace(f"closest_az_region_by_latlong(): from among {len(AZURE_REGIONS.items())} regions")
    # Equivalent of CLI: az account list-locations --output table --query "length([])" 
    # Equivalent of CLI: az account list-locations --query "[?contains(regionalDisplayName, '(US)')]" -o table
    # Equivalent of CLI: az account list-locations -o table --query "[?contains(regionalDisplayName, '(US)')]|sort_by(@, &name)[]|length(@)"
        # Remove "|length(@)"
# Sorted list of physical locations:
# az account list-locations --query "sort_by([?metadata.regionType == 'Physical'], &regionalDisplayName)" -o table
# DisplayName               Name                 RegionalDisplayName
#------------------------  -------------------  -------------------------------------
#East US                   eastus               (US) East US



#### SECTION 10: OS level utilities

# https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts

def is_uv_venv_activated() -> None:
    """Check if uv is installed and if the .venv directory exists.

    https://github.com/astral-sh/uv/issues/8775
    """
    uv_path = os.environ.get("UV")
    if not uv_path:
        print("uv is NOT installed at \"/opt/homebrew/bin/uv\" ")
        exit(9)
    file_path = os.path.abspath('.venv')  # such as /Users/johndoe/github-wilsonmar/python-samples/.venv
    if not os.path.exists(file_path):   #Alternately: if '.venv' in os.listdir():
        print(f"is_uv_venv_activated(): sys.base_prefix =\n{sys.base_prefix} ")
        print(f"is_uv_venv_activated():      sys.prefix =\n{sys.prefix}")
        print("Folder .venv NOT found. Please issue command uv init ")
        exit(9)
    #in_venv = sys.prefix != sys.base_prefix
    file_path = os.path.abspath('requirements.txt')  # such as /Users/johndoe/github-wilsonmar/python-samples/...
    if not os.path.exists(file_path):
        print("File requirements.txt not found for CLI: uv pip install -r requirements.txt")
        exit(9)
    file_path = os.path.abspath('uv.lock')  # such as /Users/johndoe/github-wilsonmar/python-samples/...
    if not os.path.exists(file_path):
        print("File uv.lock not found. Please issue command uv lock ")
        exit(9)
    # sys.prefix may be a symlink, so resolve both to their real paths
    real_base_prefix = os.path.realpath(sys.base_prefix)
    print(f"real_base_prefix = {real_base_prefix}")
    base_prefix = os.path.realpath(sys.prefix)
    print(f"     base_prefix = {base_prefix}")

    #if venv_base_prefix != venv_prefix:
    #    print_info("venv_prefix is different from venv_base_prefix!")
    return None  # can't tell if True or False



#### SECTION 11: Python script control utilities:


# See https://bomonike.github.io/python-samples/#ParseArguments

def do_clear_cli():
    """Clear CLI Terminal console."""
    # import os
    # QUESTION: What's the output variable?
    lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')


#def set_cli_parms(count):
#    """Present menu and parameters to control program."""
    # import click
    #@click.command()
    #@click.option('--count', default=1, help='Number of greetings.')
    #@click.option('--name', prompt='Your name',
    #              help='The person to greet.')
    #def set_cli_parms(count):
    #    """Set internal var."""
    #    for x in range(count):
    #        click.echo("Hello!")
    # Test by running: ./python-examples.py --help


def open_env_file() -> bool:
    """Update global variables obtained from .env file based on key provided."""
    global global_env_path
    global user_home_dir_path
    global env_file
    if not global_env_path:
        # from pathlib import Path
        # See https://wilsonmar.github.io/python-samples#run_env
        if not user_home_dir_path:  # example: /users/john_doe
            user_home_dir_path = str(Path.home())
            if not env_file:
                env_file="python-samples.env"  # the hard-coded default
            global_env_path = user_home_dir_path + "/" + env_file  # concatenate path

    # PROTIP: Check if .env file on global_env_path is readable:
    if not os.path.isfile(global_env_path):
        print_error(global_env_path+" (global_env_path) not found!")
        return None
    else:
        #env_path = pathlib.Path(global_env_path)
        # Based on: pip3 install python-dotenv
        # from dotenv import load_dotenv
        # See https://www.python-engineer.com/posts/dotenv-python/
        # See https://pypi.org/project/python-dotenv/
        load_dotenv(global_env_path)  # using load_dotenv
        # Wait until variables for print_trace are retrieved:
        print_info(f"open_env_file() to \"{global_env_path}\" ")

    return True

def get_str_from_env_file(key_in) -> str:
    """Return a value of string data type from OS environment or .env file.

    (using pip python-dotenv)
    """
    # TODO: Default env_file name:
    # env_file="python-samples.env"

    env_var = os.environ.get(key_in)
    if not env_var:  # yes, defined=True, use it:
        print_trace(f"get_str_from_env_file(\"{key_in}\") not found in .env file.")
        return None
    else:
        # PROTIP: Display only first characters of a potentially secret long string:
        if len(env_var) > 5:
            print_trace(key_in + "=\"" + str(env_var[:5]) +" (remainder removed)")
        else:
            print_trace(key_in + "=\"" + str(env_var) + "\" from .env")
        return str(env_var)


def print_env_vars():
    """List all environment variables, one line each using pretty print (pprint)."""
    # import os
    # import pprint
    if not show_secrets:
        print_error("print_env_vars() not done due to show_secrets control flag set to False (by default).")
        return None
    #else:
    environ_vars = os.environ
    print_heading("print_env_vars(): CAUTION: Secrets User's Environment variable:")
    pprint.pprint(dict(environ_vars), width = 1)

def az_parms_list():
    """Print Azure control parameter values."""
    print_secret(f"my_credential = {my_credential}")
    print_secret(f"my_user_principal_id = {my_user_principal_id}")
    print_secret(f"my_subscription_id = {my_subscription_id}")
    print_secret(f"my_tenant_id = {my_tenant_id}")
    print_info(f"region_choice_basis = {region_choice_basis}") # "cost" or "distance" or "latency" [Edit Manually]


#### SECTION 12: Time Utility Python Functions:


def get_user_local_time() -> str:
    """Return a string formatted with datetime stamp in local timezone.

    Example: "07:17 AM (07:17:54) 2025-04-21 MDT"
    """
    now: datetime = datetime.now()
    local_tz = datetime.now(timezone.utc).astimezone().tzinfo
    return f'{now:%I:%M %p (%H:%M:%S) %Y-%m-%d} {local_tz}'


def get_log_datetime() -> str:
    """Return a formatted datetime string in UTC (GMT) timezone so all logs are aligned.

    Example: 2504210416UTC for a minimal with year, month, day, hour, minute, second and timezone code.
    """
    #from datetime import datetime
    # importing timezone from pytz module
    #from pytz import timezone

    # To get current time in (non-naive) UTC timezone
    # instead of: now_utc = datetime.now(timezone('UTC'))
    # Based on https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    fts = datetime.fromtimestamp(time.time(), tz=timezone.utc)
    time_str = fts.strftime("%y%m%d%H%M%Z")  # EX: "...-250419" UTC %H%M%Z https://strftime.org

    # See https://stackoverflow.com/questions/7588511/format-a-datetime-into-a-string-with-milliseconds
    # time_str=datetime.utcnow().strftime('%F %T.%f')
        # for ISO 8601-1:2019 like 2023-06-26 04:55:37.123456 https://www.iso.org/news/2017/02/Ref2164.html
    # time_str=now_utc.strftime(MY_DATE_FORMAT)

    # Alternative: Converting to Asia/Kolkata time zone using the .astimezone method:
    # now_asia = now_utc.astimezone(timezone('Asia/Kolkata'))
    # Format the above datetime using the strftime()
    # print('Current Time in Asia/Kolkata TimeZone:',now_asia.strftime(format))
    # if show_dates:  https://medium.com/tech-iiitg/zulu-module-in-python-8840f0447801

    return time_str

#### SECTION 13: Run statistics reporting

def show_summary() -> bool:
    """Print summary of timings together at end of run."""
    if not SHOW_SUMMARY_COUNTS:
        return None

    pgm_stop_mem_diff = get_mem_used() - float(pgm_strt_mem_used)
    print_info(f"{pgm_stop_mem_diff:.2f} MB memory consumed during run {RUNID}.")

    pgm_stop_disk_diff = pgm_strt_disk_free - get_disk_free()
    print_info(f"{pgm_stop_disk_diff:.2f} GB disk space consumed during run {RUNID}.")

    print_info("Monotonic wall times (seconds):")
    # TODO: Write to log for longer-term analytics

    # For wall time of std imports:
    #std_elapsed_wall_time = std_stop_timestamp -  std_strt_timestamp
    #print_verbose("for import of Python standard libraries: "+ \
    #    f"{std_elapsed_wall_time:.4f}")

    # For wall time of xpt imports:
    xpt_elapsed_wall_time = xpt_stop_timestamp -  xpt_strt_timestamp
    print_verbose("for import of Python extra    libraries: "+ \
        f"{xpt_elapsed_wall_time:.4f}")

    pgm_stop_timestamp =  time.monotonic()
    pgm_elapsed_wall_time = pgm_stop_timestamp -  pgm_strt_timestamp
    # pgm_stop_perftimestamp = time.perf_counter()
    print_verbose("for whole program run:                   "+ \
        f"{pgm_elapsed_wall_time:.4f}")

    # TODO: Write wall times to log for longer-term analytics
    return True


#### SECTION 14. Obtain program environment metadata:


# See https://bomonike.github.io/python-samples/#run_env

def os_platform():
    """Return a friendly name for the operating system."""
    #import platform # https://docs.python.org/3/library/platform.html
    platform_system = str(platform.system())
       # 'Linux', 'Darwin', 'Java', 'Windows'
    print_trace("platform_system="+str(platform_system))
    if platform_system == "Darwin":
        my_platform = "macOS"
    elif platform_system == "linux" or platform_system == "linux2":
        my_platform = "Linux"
    elif platform_system == "win32":  # includes 64-bit
        my_platform = "Windows"
    else:
        print_fail("platform_system="+platform_system+" is unknown!")
        exit(1)  # entire program
    return my_platform

def macos_version_name(release_in):
    """Return the marketing name of macOS versions.
     
    Not available from the running macOS operating system.
    """
    # NOTE: Return value is a list!
    # This has to be updated every year, so perhaps put this in an external library so updated
    # gets loaded during each run.
    # Apple has a way of forcing users to upgrade, so this is used as an
    # example of coding.
    # FIXME: https://github.com/nexB/scancode-plugins/blob/main/etc/scripts/homebrew.py
    # See https://support.apple.com/en-us/HT201260 and https://www.wikiwand.com/en/MacOS_version_history
    macos_versions_table = {
        '22.7': ['Next2024', 2024, '24'],
        '22.6': ['macOS Sonoma', 2023, '23'],
        '22.5': ['macOS Ventura', 2022, '13'],
        '12.1': ['macOS Monterey', 2021, '21'],
        '11.1': ['macOS Big Sur', 2020, '20'],
        '10.15': ['macOS Catalina', 2019, '19'],
        '10.14': ['macOS Mojave', 2018, '18'],
        '10.13': ['macOS High Sierra', 2017, '17'],
        '10.12': ['macOS Sierra', 2016, '16'],
        '10.11': ['OS X El Capitan', 2015, '15'],
        '10.10': ['OS X Yosemite', 2014, '14'],
        '10.9': ['OS X Mavericks', 2013, '10.9'],
        '10.8': ['OS X Mountain Lion', 2012, '10.8'],
        '10.7': ['OS X Lion', 2011, '10.7'],
        '10.6': ['Mac OS X Snow Leopard', 2008, '10.6'],
        '10.5': ['Mac OS X Leopard', 2007, '10.5'],
        '10.4': ['Mac OS X Tiger', 2005, '10.4'],
        '10.3': ['Mac OS X Panther', 2004, '10.3'],
        '10.2': ['Mac OS X Jaguar', 2003, '10.2'],
        '10.1': ['Mac OS X Puma', 2002, '10.1'],
        '10.0': ['Mac OS X Cheetah', 2001, '10.0'],
    }
    # WRONG: On macOS Monterey, platform.mac_ver()[0]) returns "10.16", which is Big Sur and thus wrong.
    # See https://eclecticlight.co/2020/08/13/macos-version-numbering-isnt-so-simple/
    # and https://stackoverflow.com/questions/65290242/pythons-platform-mac-ver-reports-incorrect-macos-version/65402241
    # and https://docs.python.org/3/library/platform.html
    # So that is not a reliable way, especialy for Big Sur
       # https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html#b404-import-subprocess
    # import subprocess  # built-in
    # from subprocess import PIPE, run
    # p = subprocess.Popen("sw_vers", stdout=subprocess.PIPE)
    # result = p.communicate()[0]
    macos_platform_release = platform.release()
    # Alternately:
    release = '.'.join(release_in.split(".")[:2])  # ['10', '15', '7']
    macos_info = macos_versions_table[release]  # lookup for ['Monterey', 2021]
    print_trace("macos_info="+str(macos_info))
    print_trace("macos_platform_release="+macos_platform_release)
    return macos_platform_release


def macos_sys_info():
    """Print macOS System Info."""
    if not show_sys_info:   # defined among CLI arguments
        return None
    print_heading("macos_sys_info():")

        # or socket.gethostname()
    my_platform_node = platform.node()
    print_trace("my_platform_node = "+my_platform_node + " (machine name)")

    # print_trace("env_file = "+env_file)
    print_trace("user_home_dir_path = "+user_home_dir_path)
    # the . in .secrets tells Linux that it should be a hidden file.

    # import platform # https://docs.python.org/3/library/platform.html
    platform_system = platform.system()
       # 'Linux', 'Darwin', 'Java', 'Win32'
    print_trace("platform_system = "+str(platform_system))

    # my_os_platform=localize_blob("version")
    print_trace("my_os_version = "+str(platform.release()))
    #           " = "+str(macos_version_name(my_os_version)))

    my_os_process = str(os.getpid())
    print_trace("my_os_process = "+my_os_process)

    my_os_uname = str(os.uname())
    print_trace("my_os_uname = "+my_os_uname)
        # MacOS version=%s 10.14.6 # posix.uname_result(sysname='Darwin',
        # nodename='NYC-192850-C02Z70CMLVDT', release='18.7.0', version='Darwin
        # Kernel Version 18.7.0: Thu Jan 23 06:52:12 PST 2020;
        # root:xnu-4903.278.25~1/RELEASE_X86_64', machine='x86_64')

    # import pwd   #  https://zetcode.com/python/os-getuid/
    pwuid_shell = pwd.getpwuid(os.getuid()).pw_shell     # like "/bin/zsh" on MacOS
    # preferred over os.getuid())[0]
    # Instead of: conda install psutil   # found
    # import psutil

    # machine_uid_pw_name = psutil.Process().username()
    print_trace("pwuid_shell = "+pwuid_shell)

    # Obtain machine login name:
    # This handles situation when user is in su mode.
    # See https://docs.python.org/3/library/pwd.html
    pwuid_gid = pwd.getpwuid(os.getuid()).pw_gid         # Group number datatype
    print_trace("pwuid_gid = "+str(pwuid_gid)+" (process group ID number)")

    pwuid_uid = pwd.getpwuid(os.getuid()).pw_uid
    print_trace("pwuid_uid = "+str(pwuid_uid)+" (process user ID number)")

    pwuid_name = pwd.getpwuid(os.getuid()).pw_name
    print_trace("pwuid_name = "+pwuid_name)

    pwuid_dir = pwd.getpwuid(os.getuid()).pw_dir         # like "/Users/johndoe"
    print_trace("pwuid_dir = "+pwuid_dir)

    # Several ways to obtain:
    # See https://stackoverflow.com/questions/4152963/get-name-of-current-script-in-python
    # this_pgm_name = sys.argv[0]                     # = ./python-samples.py
    # this_pgm_name = os.path.basename(sys.argv[0])   # = python-samples.py
    # this_pgm_name = os.path.basename(__file__)      # = python-samples.py
    # this_pgm_path = os.path.realpath(sys.argv[0])   # = python-samples.py
    # Used by display_run_stats() at bottom:
    this_pgm_name = os.path.basename(os.path.normpath(sys.argv[0]))
    print_trace("this_pgm_name = "+this_pgm_name)

    #this_pgm_last_commit = __last_commit__
    #    # Adapted from https://www.python-course.eu/python3_formatted_output.php
    #print_trace("this_pgm_last_commit = "+this_pgm_last_commit)

    this_pgm_os_path = os.path.realpath(sys.argv[0])
    print_trace("this_pgm_os_path = "+this_pgm_os_path)
    # Example: this_pgm_os_path=/Users/wilsonmar/github-wilsonmar/python-samples/python-samples.py

    # import site
    site_packages_path = site.getsitepackages()[0]
    print_trace("site_packages_path = "+site_packages_path)

    this_pgm_last_modified_epoch = os.path.getmtime(this_pgm_os_path)
    print_trace("this_pgm_last_modified_epoch = "+str(this_pgm_last_modified_epoch))

    #this_pgm_last_modified_datetime = datetime.fromtimestamp(
    #    this_pgm_last_modified_epoch)
    #print_trace("this_pgm_last_modified_datetime=" +
    #            str(this_pgm_last_modified_datetime)+" (local time)")
        # Default like: 2021-11-20 07:59:44.412845  (with space between date & time)

    # Obtain to know whether to use new interpreter features:
    python_ver = platform.python_version()
        # 3.8.12, 3.9.16, etc.
    print_trace("python_ver = "+python_ver)

    # python_info():
    python_version = no_newlines(sys.version)
        # 3.9.16 (main, Dec  7 2022, 10:16:11) [Clang 14.0.0 (clang-1400.0.29.202)]
        # 3.8.3 (default, Jul 2 2020, 17:30:36) [MSC v.1916 64 bit (AMD64)]
    print_trace("python_version = "+python_version)

    print_trace("python_version_info = "+str(sys.version_info))
        # Same as on command line: python -c "print_trace(__import__('sys').version)"
        # 2.7.16 (default, Mar 25 2021, 03:11:28)
        # [GCC 4.2.1 Compatible Apple LLVM 11.0.3 (clang-1103.0.29.20) (-macos10.15-objc-

    if sys.version_info.major == 3 and sys.version_info.minor <= 6:
            # major, minor, micro, release level, and serial: for sys.version_info.major, etc.
            # Version info sys.version_info(major=3, minor=7, micro=6,
            # releaselevel='final', serial=0)
        print_fail("Python 3.6 or higher is required for this program. Please upgrade.")
        sys.exit(1)

    # TODO: Make this function for call before & after run:
    #    disk_list = get_disk_free()
    #    disk_space_free = disk_list[1]:,.1f / disk_list[0]:,.1f
    #    print_info(localize_blob("Disk space free")+"="+disk_space_free+" GB")
        # left-to-right order of fields are re-arranged from the function's output.

    is_uv_venv_activated()  # both True:


def get_mem_used() -> float:
    """Return the memory used by the current process in MiB."""
    # import os, psutil  #  psutil-5.9.5
    process = psutil.Process()
    mem=process.memory_info().rss / (1024 ** 2)  # in bytes
    print_trace(str(process))
    return float(mem)
    # to print_verbose("get_mem_used(): "+str(mem)+" MiB used.")


def get_disk_free() -> float:
    """Return the disk space free in GB."""
    # import shutil
    # Replace '/' with your target path (e.g., 'C:\\' on Windows)
    usage = shutil.disk_usage('/')
    pct_free = ( float(usage.free) / float(usage.total) ) * 100
    gb = 1073741824  # = 1024 * 1024 * 1024 = Terrabyte
    disk_gb_free = float(usage.free) / gb
    print_verbose(f"{disk_gb_free:.2f} ({pct_free:.2f}%) disk free")
    return disk_gb_free


def handle_fatal_exit():
    """Handle fatal exit with a message first."""
    print_trace("handle_fatal_exit() called.")
    sys.exit(9)


#### SECTION 15: External Messaging:



# TODO: Gmail, Slack, Discord, MS-Teams


#### SECTION 16. Generic Geo utility APIs:


def get_ip_address() -> str:
    """Return IP address of client running this program.

    TODO: If this is running as a web server (like Flask or Django), extract it from the request headers
    from the user making a request to your site:
    See https://www.perplexity.ai/search/python-code-to-get-client-ip-a-6au51O4RTtO_NY2pImnyrw#0
    """
    try:
        ext_ip_address = requests.get('https://api.ipify.org').text
        # import socket  (built-in)
        hostname = socket.gethostname()
        int_ip_address = socket.gethostbyname(hostname)
        print_info(f"get_ip_address(): \"{int_ip_address}\" for hostname \"{hostname}\" ")
        print_info(f"get_ip_address(): \"{ext_ip_address}\" ... ")
        return ext_ip_address
    except Exception as e:   
        print_error(f"get_ip_address(): {e}")
        return None


def get_ip_geo_coordinates(ip_address=None) -> (str, str):
    """Return latitude and longitude for a given IP address by calling the DistanceMatrix API.

    # CODING EXAMPLE: Return of two variable values that travel together.
    """
    # Validate ip_address input:
    if not ip_address:
        ip_address = get_ip_address()
        print_verbose(f"get_ip_geo_coordinates(using: \"{ip_address}\" ... ")
    if not ip_address:
        print_error("get_ip_geo_coordinates() ip_address not valid/specified!")
        return None, None

    # Try getting latitude and longitude from IP address by calling the ip2geotools 
    try:  # no API key needed for limited ipapi.co free tier:
        url = f'https://ipapi.co/{ip_address}/json/'
        response = requests.get(url).json()
        latitude = response.get('latitude')
        longitude = response.get('longitude')
        print_info(f"get_ip_geo_coordinates({ip_address}): lat={latitude} & lng={longitude}")
        return latitude, longitude
    except Exception as e:   
        print_error(f"get_ip_geo_coordinates(ipapi.co call): {e}")
        return None, None


def get_geo_coordinates(zip_code) -> (float, float):
    """Return latitude and longitude for a given zip code by calling the DistanceMatrix API.

    # CODING EXAMPLE: Return of two variable values that travel together.
    """
    # Validate zip_code input:
    if not zip_code:
        print_error("get_geo_coordinates() zip_code not valid/specified!")
    
        # OPTION C: Try getting latitude and longitude from IP address by calling the ip2geotools 
        latitude, longitude = get_ip_geo_coordinates("")
        print_verbose(f"get_geo_coordinates(): lat={latitude} & lng={longitude}")

    # Instead of DISTANCEMATRIX_API_KEY = get_str_from_env_file('DISTANCEMATRIX_API_KEY')
    try:
        distancematrix_api_key = os.environ["DISTANCEMATRIX_API_KEY"]
    except KeyError:   
        print_error("get_geo_coordinates() DISTANCEMATRIX_API_KEY not specified in .env file!")
        pass

    if not distancematrix_api_key:
        print_error("get_geo_coordinates() DISTANCEMATRIX_API_KEY not specified in .env file!")
        return None, None

    # Construct the API URL: CAUTION: This is a paid API, so do not expose the API key in logs.
    url = f'https://api.distancematrix.ai/maps/api/geocode/json?address={zip_code}&key={distancematrix_api_key}' 
    print_verbose(f"get_geo_coordinates() zip: \"{zip_code}\" URL = \"{url}\" ")
    try:
        # import requestsxr
        response = requests.get(url)
        data = response.json()    # Parse JSON response
        #print("data=",data)
        # data={'result': [{'address_components': [{'long_name': 'mountain view', 'short_name': 'mountain view', 'types': ['locality']}, {'long_name': 'ca', 'short_name': 'ca', 'types': ['state']}, {'long_name': 'usa', 'short_name': 'usa', 'types': ['country']}], 'formatted_address': 'Mountain View, CA, USA',
        # 'geometry': {'location': {'lat': 37.418918000000005, 'lng': -122.07220494999999}, 'location_type': 'APPROXIMATE',
        # 'viewport': {'northeast': {'lat': 37.418918000000005, 'lng': -122.07220494999999},
        # 'southwest': {'lat': 37.418918000000005, 'lng': -122.07220494999999}}},
        # 'place_id': '', 'plus_code': {}, 'types': ['locality', 'political']}], 'status': 'OK'}
    except Exception as e:
        print_error(f"get_geo_coordinates(\"{zip_code}\") {e}")
        return None, None

    if data['status'] == 'OK':
        # Extract latitude and longitude
        latitude = data['result'][0]['geometry']['location']['lat']
        longitude = data['result'][0]['geometry']['location']['lng']
        print_verbose(f"get_geo_coordinates(\"{zip_code}\") is at lat={latitude} & lng={longitude}")
        return latitude, longitude
    else:
        print_error(f"get_geo_coordinates(\"{zip_code}\") failed: {data}")
        return None, None


def get_longitude_latitude() -> (float, float):
    """Return longitude and latitude, determined various ways.

    A. From parm --lat and --long.
    B. From .env file containing "MY_LONGITUDE" and "MY_LATITUDE" variable values
    C. From parm --zipcode which calls the DistanceMatrix API.
    D. From lookup based on user's IP address.
    E. From hard-coded defaults.
    """
    # OPTION A. From parms -lat & -long defined.
    if args.lat and args.long:
        latitude = args.lat
        longitude = args.long
        print_trace(f"get_longitude_latitude() --lat \"{latitude}\" --long \"{longitude}\"  ")
        return float(latitude), float(longitude)

    # OPTION B. From .env file containing "MY_LONGITUDE" and "MY_LATITUDE" variable values
    try:
        latitude = float(os.environ["MY_LATITUDE"])
        # latitude = get_str_from_env_file('MY_LATITUDE')
        print_info(f"MY_LATITUDE = \"{latitude:.7f}\"  # (North/South) from .env being used. ")
        # drop thru to longitude
    except KeyError:   
        latitude = 0
        pass  # do below.

    try:
        longitude = float(os.environ["MY_LONGITUDE"])
        # longitude = get_str_from_env_file('MY_LONGITUDE')
        print_info(f"MY_LONGITUDE = \"{longitude:.7f}\"  # (East/West of GMT) from .env being used. ")
        return float(latitude), float(longitude)
    
    except KeyError:   
        longitude = 0
        pass  # do below.

    # OPTION C. From parm --zipcode, which calls the DistanceMatrix API.
    if args.zip:
        zip_code = args.zip   # zip_code = ' '.join(map(str, args.zip))   # convert list from parms to string.
        print_trace(f"get_longitude_latitude() -zip: \"{zip_code}\" ")
        latitude, longitude = get_geo_coordinates(zip_code)
        return float(latitude), float(longitude)

    if not (latitude and longitude):
        ip_address = get_ip_address()
        if ip_address:
            # print_info(f"get_ip_address() = \"{ip_address}\"")
            latitude, longitude = get_ip_geo_coordinates(ip_address)
            print_verbose(f"get_longitude_latitude() latitude={str(latitude)} longitude={str(longitude)} from {ip_address}")
    
    if not (latitude and longitude):
        # OPTION D. From hard-coded default values (for demos of how other parts of this program runs)
        latitude = 34.123
        print_warning(f"get_longitude_latitude() latitude={latitude:.7f} from default!")
        longitude = -104.322
        print_warning(f"get_longitude_latitude() longitude={longitude:.7f} from default!")

    if latitude and longitude:
        # format response:
        latitude_direction = "North" if latitude >= 0 else "South"
        longitude_direction = "West" if longitude >= 0 else "East"
        print_info(f"get_longitude_latitude() latitude={latitude:.7f} {latitude_direction}, longitude={longitude:.7f} {longitude_direction}")
        return latitude, longitude
    else:
        print_error("get_longitude_latitude() failed to get values!")
        return None, None


def get_elevation(longitude, latitude, units='Meters', service='google' ) -> str:
    """Return elevation in metric meters or imperial (US) feet for the given longitude and latitude.

    using the USGS (US Geologic Survey's National Map's Elevation Point Query Service Digital Elevation Model (DEM) at
    https://apps.nationalmap.gov/epqs/ version 1.0.0 returning error!
    https://epqs.nationalmap.gov/v1/docs
    Alternatives: Google Earth: Provides altitude data in its desktop application.
        Third-party tools offer elevation estimates but require manual input of coordinates:
            Freemaptools.com, MapCoordinates.net, DaftLogic.com
    No retries sessions as in https://www.perplexity.ai/search/python-code-to-obtain-elevatio-mtFsgRSgQXie68kzKDrVmw
    """
    print_trace(f"get_elevation(longitude={longitude} latitude={latitude}")
    try:
        # import requests
        if service == 'freemaptools':
            # WARNING: Freemaptools' API endpoint and parameters are undocumented here
            # This is a hypothetical implementation
            url = 'https://www.freemaptools.com/ajax/elevation-service.ashx'
            params = {"lat": latitude, "lng": longitude}
            response = requests.get(url, params=params)
            elevation = response.json()['elevation']
        
        # Alternative services from search results
        elif service == 'google':
            url = 'https://maps.googleapis.com/maps/api/elevation/json'
            # https://console.cloud.google.com/google/maps-apis/credentials?hl=en&project=stoked-woods-362514
            # TODO: Get API Key from https://cloud.google.com/maps-platform => mapsplatform
            try:
                api_key = os.environ["GOOGLE_API_KEY"]
            except KeyError:   
                print_error("get_geo_cget_elevationoordinates() GOOGLE_API_KEY not specified in .env file!")
                return None
            params = {"locations": f"{latitude},{longitude}", "key": api_key}
            print_trace(f"get_elevation() params={params}")
            data = requests.get(url, params=params).json()
            print_trace(f"get_elevation() response={data}")
            elevation = data['results'][0]['elevation']
        
        elif service == 'national_map':
            url = 'https://nationalmap.gov/epqs/pqs.php'
            params = {'x': longitude, 'y': latitude, 'units': 'Meters', 'output': 'json'}
            data = requests.get(url, params=params).json()
            # FIXME: Expecting value: line 1 column 1 (char 0) 
            elevation = data['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']

    except (requests.exceptions.RequestException, KeyError) as e:
        print_error(f"get_elevation(): ERROR {e}")
        # https://www.perplexity.ai/search/what-is-cause-of-error-expecti-K3fjy0UGQwSOivoS3YQQ9g#0
        return None

    print_info(f"get_elevation() elevation={elevation}")  # Example: 
    return elevation if elevation != -1000000 else None

# print(get_elevation(39.7392, -104.9903, service='google', api_key='YOUR_KEY'))


#### SECTION 17. Region & Location Geo utilities:


table_data = []  # Global variable
def build_az_pricing_table(json_data, table_data):
    """Build Azure Pricing Table from collections import OrderedDict."""
    for item in json_data['Items']:
        #meter = item['meterName']
        table_data.append([item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], item['productName']])
        #table_data.append(OrderedDict([item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], item['productName']]))
        #table_data.append(OrderedDict([item['armSkuName'], item['retailPrice'], item['unitOfMeasure'], item['armRegionName'], item['productName']]))
        
def get_cheapest_az_region(arm_sku_name_to_find) -> str:
    """Return the region with the lowest retailPrice for a given SKU (Stock Keeping Unit).

    For the given SKU, after listing prices in all regions.
    Equivalent CLI: az vm list-sizes --location westus
    See https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices
    """
    print_verbose(f"Among {len(AZURE_REGIONS)} possible AZURE_REGIONS in get_cheapest_az_region(): ")
    
    table_data.append(['retailPrice', 'unitOfMeasure', 'armRegionName', 'productName'])
    
    # TODO: NE https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    # Loop through earmRegionName eq 'southcentralus' etc. from AZURE_REGIONS array:
    print_verbose(f"For: armSkuName='{arm_sku_name_to_find}', meterName='NP20s Spot', priceType='Consumption'")
    query = f"armSkuName eq '{arm_sku_name_to_find}' and priceType eq 'Consumption' and contains(meterName, 'Spot')"
    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)

    build_az_pricing_table(json_data, table_data)
    next_page = json_data.get('next_pageLink')  # Use .get() to safely access the key

    # Retrieve several pages to get them all:
    while next_page:
        response = requests.get(next_page)
        json_data = json.loads(response.text)
        next_page = json_data.get('next_pageLink')  # Use .get() to safely access the key
        build_az_pricing_table(json_data, table_data)

    # Sort the table data by price (first column) - skip the header row
    header = table_data[0]
    data_rows = table_data[1:]
    sorted_data = sorted(data_rows, key=lambda x: x[0])  # Sort by price ([0]=first column)
    
    # Reconstruct the table with header and sorted data:
    sorted_table = [header] + sorted_data
    if len(sorted_data) > 0:
        print(tabulate(sorted_table, headers='firstrow', tablefmt='psql'))
    else:
        print_error(f"No pricing data found for {arm_sku_name_to_find}")
        return None

    # TODO: Add to table the distance from each Azure region from user/client location.

    #    ***  Among 53 possible AZURE_REGIONS in get_cheapest_az_region():  
    #    ***  FILTER: armSkuName='Standard_NP20s', meterName='NP20s Spot', priceType='Consumption' 
    #    +---------------+-----------------+-----------------+------------------------------------+
    #    |   retailPrice | unitOfMeasure   | armRegionName   | productName                        |
    #    |---------------+-----------------+-----------------+------------------------------------|
    #    |        0.462  | 1 Hour          | eastus          | Virtual Machines NP Series         |
    #    |        0.462  | 1 Hour          | westus2         | Virtual Machines NP Series         |
    # TODO: Return several regions with the same price.
    az_svc_region = sorted_data[0][2]   # First armRegionName value.
    if az_svc_region:
        print_info(f"my_az_svc_region: \"{az_svc_region}\" from get_cheapest_az_region() ")
        return az_svc_region
    else:
        return None


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great circle distance between two points on earth (specified in decimal degrees)."""
    # import math

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371  # Radius of earth in kilometers
    return c * r   

def closest_az_region_by_latlong(latitude: float, longitude: float) -> str:
    """Return the closeset Azure Region by Latitude Longitude.

    This identifies the Azure region/location for a given geo longitude and latitude.
    based on the ping speed and distance from each Azure region.
    TODO: More importantly, for a particular service (resource) Azure charges a different cost each region.
    WARNING: The variable name "location" is reserved by Azure for its current region name.
    PROTIP: Notice how variables are defined with float and integers hints.
    """
    # CODING EXAMPLE: Ensure valid inputs into function:
    if not (-90 <= float(latitude) <= 90) or not (-180 <= float(longitude) <= 180):
        print("Error: Invalid coordinates. Latitude must be between -90 and 90, and longitude between -180 and 180.")
        return

    # TODO: Identify the longest region name (germanywestcentral) and announce its number of characters (18)
        # for use in keyvault name which must be no longer than 24 characters long.

    # num_regions = 1
    distances = []
    for region, (region_lat, region_lon) in AZURE_REGIONS.items():
        distance = haversine_distance(latitude, longitude, region_lat, region_lon)
        distances.append((region, distance))
    
    # Sort by distance and return the n closest:
    n:int = 3
    closest_regions = sorted(distances, key=lambda x: x[1])[:n]
    print_verbose(f"closest_az_region_by_latlong({n}:): {closest_regions}")
    closest_region = closest_regions[0][0]  # the first region ID in the list
    print_info(f"closest_az_region_by_latlong(of {len(AZURE_REGIONS.items())} in Azure:): \"{closest_region}\" ")
    
    return closest_region


def get_az_region_by_latency(storage_account_name, attempts=5) -> str:
    """Return the HTTP latency to a storage account within the Azure cloud."""
    # import requests
    # import time

    url = storage_account_name + ".blob.core.windows.net"
    latencies = []
    for _ in range(attempts):
        start = time.time()
        try:
            response = requests.get(url, timeout=5)
            latency = (time.time() - start) * 1000  # ms
            latencies.append(latency)
            print(f"get_az_region_by_latency(): response={response}")
        except requests.RequestException:
            # FIXME: <Error data-darkreader-white-flash-suppressor="active">
            # <Code>InvalidQueryParameterValue</Code>
            # <Message>
            # Value for one of the query parameters specified in the request URI is invalid. RequestId:3b433e32-d01e-003f-274c-b37a10000000 Time:2025-04-22T06:06:36.7748787Z
            # </Message>
            # <QueryParameterName>comp</QueryParameterName>
            # <QueryParameterValue/>
            # <Reason/>
            # </Error>
            latencies.append(None)

    #valid_latencies = [lm for lx in latencies if lx is not None]
    #if valid_latencies:
    #    avg_latencies = sum(valid_latencies)/len(valid_latencies)
    #    print_info(f"HTTP latency to : avg {avg_latencies:.2f} ms")
    #else:
    print_error(f"get_az_region_by_latency(): requests failed to {url}")
    return None


#### SECTION 18. Azure cloud authentication utilities:


# def job roles permissions RBAC:
    """
    The different personas/roles in an enterprise, each with job-relevant dashboards and alerts:
    A. TechOps (SREs) who establish, troubleshoot, and restore the services (CA, dashbords, alerts) that others to operate. See https://github.com/bregman-arie/sre-checklist
    B. SecOps who enable people, Web (Flask, Django, FastAPI) apps & Serverless Functios accessing secrets based on RBAC policies. Operations Center that responds to security alerts.
    C. Managers with authority to permanently delete (purge) secrets and backups https://learn.microsoft.com/en-us/azure/key-vault/policy-reference
    D. AppDevs who request, obtain, use, rotate secrets (but not delete) access to Networks, Apps. and Functions
    E. End Users who make use of Networks, Apps. and Functions built by others
    F. DataOps to regularly backup and rotate secrets, manage log storage. Data governance. Migrate data.
    """


def get_tenant_id() -> str:
    """Get Azure Tenant ID.
   
    from .env or by making a subprocess call of CLI from within Python:
            az account show --query tenantId -o tsv
    The Tenant ID uniquely identifies the Microsoft Entra (formerly Azure AD) directory you use.
    Obtain from Portal at: https://portal.azure.com/#view/Microsoft_AAD_IAM/TenantProperties.ReactView
    Organization ID at https://portal.azure.com/#view/Microsoft_AAD_IAM/DirectorySwitchBlade/subtitle/
    """
    try:
        tenant_id = os.environ["AZURE_TENANT_ID"]  # EntraID
        print_info(f"AZURE_TENANT_ID from .env: \"{tenant_id}\"")
        return tenant_id
    except KeyError:   
        # import subprocess
        #     az    account    show    --query    tenantId    -o    tsv
        tenant_id = subprocess.check_output(
            ["az", "account", "show", "--query", "tenantId", "-o", "tsv"]
        ).decode().strip()
        if tenant_id:
            print_info(f"get_tenant_id(): \"{tenant_id}\"")
            return tenant_id


def get_acct_credential() -> object:
    """Return an Azure cloud credential object for the given user account name (email).

    for local development after CLI:
    az cloud set -n AzureCloud   # return to Public Azure.
    az login
    """
    if AZURE_ACCT_NAME:  # defined by parameter:
        print_info(f"-u or -user \"{AZURE_ACCT_NAME}\"  # (AZURE_ACCT_NAME) being used.")
        my_acct_name = AZURE_ACCT_NAME
        pass   # to get credential object
    else:   # see if .env file has a value:
        try:
            my_acct_name = os.environ["AZURE_ACCT_NAME"]
            print_info(f"AZURE_ACCT_NAME = \"{my_acct_name}\"  # from .env file being used.")
        except Exception:
            print_error("-u or -user in parms or AZURE_ACCT_NAME in .env not provided in get_acct_credential()")
            exit(9)

    # TODO: For Web Applications (e.g., Flask, Django) with Azure AD Authentication.
    # For Azure App Service (Web Apps) with Built-in Authentication

    try:
        # from azure.mgmt.resource import SubscriptionClient
        # from azure.core.exceptions import ClientAuthenticationError
        credential = DefaultAzureCredential()
            # Sequentially tries a "chain" of auth credentials including AzureCliCredential()
        print_trace(f"get_acct_credential(): \"{str(credential)}\")")
        # subscription_client = SubscriptionClient(credential)
            # F841 Local variable `subscription_client` is assigned to but never used
        #subscriptions = list(subscription_client.subscriptions.list())
        #print_verbose("User \"{my_acct_name}\" is logged in to Azure at get_acct_credential().")
                #blob_service_client = BlobServiceClient(
        #    account_url="https://{az_acct_name}.blob.core.windows.net",
        #    credential=credential
        #)
        return credential  # as logged in to Azure.
            # <azure.identity._credentials.default.DefaultAzureCredential object at 0x106be6ba0>
    except ClientAuthenticationError:
        print_fail("Please run CLI command: 'az login' (with authentication) and select Subscription.")
        exit(9)
    # Raised by the Azure Storage Blob client library:
    #except blob_service_client.exceptions.HTTPError as errh:
    #    print_error("get_acct_credential() HTTP Error:", errh)
    #except blob_service_client.exceptions.ConnectionError as errc:
    #    print_error("get_acct_credential() Connection Error:", errc)
    #except blob_service_client.exceptions.Timeout as errt:
    #    print_error("get_acct_credential() Timeout Error:", errt)
    #except blob_service_client.exceptions.RequestException as err:
    #    print_error("get_acct_credential() Other Error:", err)
    return None


def get_user_principal_id(credential) -> str:
    """Return the singed-in user's principal object ID string.

    Equivlent of CLI: az ad signed-in-user show --query id -o tsv
    """
    #from azure.identity import DefaultAzureCredential
    try:
        token = credential.get_token("https://graph.microsoft.com/.default").token
        # print_trace(f"get_user_principal_id() token: "+ token)
        print_trace(f"get_user_principal_id() token size: {len(token)}")
    except Exception as e:
        print_error(f"get_user_principal_id() token ERROR: {e}")
        return None

    try:
        # Call Microsoft Graph to get the signed-in user's details:
        # Call the /me endpoint on Microsoft Graph for the signed-in user's profile:
        headers = {
            "Authorization": f"Bearer {token}"
        }
        # import requests
        response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers=headers
        )
        # Extract from the returned profile the id field (the Azure AD object ID):
        response.raise_for_status()
        user = response.json()
        user_principal_id = user.get('id')
        return user_principal_id
    except Exception as e:
        print_error(f"get_user_principal_id() ERROR: {e}")
        return None


def use_app_credential(tenant_id, client_id, client_secret) -> object:
    """Return a credential object after app registration.

    no need for CLI az login.
    """
    try:
        credential = ClientSecretCredential(tenant_id, client_id, client_secret)
        return credential
    except Exception as e:
        print(f"use_app_credential() ERROR: {e}")
        return None


def get_azure_subscription_id(credential) -> str:
    """Return Azure subscription ID string from credential object.

    Equivalent of CLI to list: az account show --query id --output tsv
    Portal: https://portal.azure.com/#@jetbloom.com/resource/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/overview
    """
    if AZURE_SUBSCRIPTION_ID:  # defined by parameter:
        print_info(f"-sub or -subscription \"{AZURE_SUBSCRIPTION_ID}\"  # (AZURE_SUBSCRIPTION_ID) being used.")
        return AZURE_SUBSCRIPTION_ID
    else:   # see if .env file has a value:
        print_trace(f"get_azure_subscription_id( \"{str(credential)}\" ")
        try:
            subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
            print_trace(f"AZURE_SUBSCRIPTION_ID = \"{subscription_id}\"  # from .env file being used.")
            return subscription_id
        except Exception:
            print_fail("-sub or -subscription / AZURE_SUBSCRIPTION_ID in .env not defined for get_azure_subscription_id()")
            pass  # to below to get a subscription_id
        finally:
            pass

    # Authenticate using Azure CLI credentials
    # credential = AzureCliCredential()  <- from function input.

    # Initialize the SubscriptionClient:
    # from azure.identity import AzureCliCredential
    # from azure.mgmt.resource import SubscriptionClient
    subscription_client = SubscriptionClient(credential)

    # List all subscriptions and print their IDs and display names
    for subscription in subscription_client.subscriptions.list():
        print(f"Subscription Name: {subscription.display_name}, ID: {subscription.subscription_id}")
    # PROTIP: Pick the first one to use:
    subscription_id = subscription.subscription_id
    print_info(f"get_azure_subscription_id(): \"{subscription_id}\" ")
    return subscription_id 


def register_subscription_providers(credential, subscription_id) -> bool:
    """Ensure providers are registered for the Subscription ID provided.

    which requires getting the long (300+) list of providers
    """
    #uv add azure-identity
    #uv add azure-mgmt-resource
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.resource import ResourceManagementClient

    # WARNING: Only register providers you need to maintain least-privilege security:
    required_providers = [
        "Microsoft.BotService",
        "Microsoft.Web",
        "Microsoft.ManagedIdentity",
        "Microsoft.Search",
        "Microsoft.Storage",
        "Microsoft.CognitiveServices",
        "Microsoft.AlertsManagement",
        "microsoft.insights",
        "Microsoft.KeyVault",
        "Microsoft.ContainerInstance"
    ]  # there are many others.

    try:
        # Obtain the management object for resources:
        resource_client = ResourceManagementClient(credential, subscription_id)

        # It's said that there is no lookup of
        # Get all providers and their registration states:
        all_providers = {provider.namespace: provider.registration_state for provider in resource_client.providers.list()}

        print_verbose(f"register_subscription_providers() {len(all_providers)}:")
        for provider in required_providers:
            reg_state = all_providers.get(provider, None)
            if reg_state != "Registered":  # Register providers if not registered:
                rg_result = resource_client.providers.register(provider)
                print_trace(f"   \"{provider}\" being registered: {rg_result}")
                    # NOTE: If a provider is in the “Registering” state, you don’t need to wait for all regions to complete—resource creation can proceed as soon as the region you need is ready.
            else:
                print_trace(f"   \"{provider}\" already registered.")
        return True

    except Exception as e:
        print_error(f"register_subscription_providers() ERROR: {e}")
        return False



#### SECTION 18. Azure cloud Resource Group:

def resource_object(subscription_id=""):
    """List resource groups for subscription."""
    if not subscription_id:
        subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
                
    try:
        # Acquire a credential object:
        credential = DefaultAzureCredential()

        # Obtain the management object for resources:
        resource_client = ResourceManagementClient(credential, subscription_id)
        print_trace(f"resource_object() subscription_id: \"{subscription_id}\" {resource_client} ")
        return resource_client
    except Exception as e:
        print_error(f"resource_object() {e}")
        return None


def resource_group_list(subscription_id="") -> int:
    """List resource groups for subscription.

    Equivalent to: az resource group list --output table
    Name  ResourceGroup  Location  Type  Status
    Based on https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-list-resource-groups?tabs=bash
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.resource import ResourceManagementClient
    #import os

    if not subscription_id:
        subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    print_trace(f"resource_group_list() subscription_id: \"{subscription_id}\"")
                
    # Acquire a credential object:
    credential = DefaultAzureCredential()

    # Obtain the management object for resources:
    resource_client = ResourceManagementClient(credential, subscription_id)
    group_list = resource_client.resource_groups.list()
    # Show the groups in formatted output:
    column_width = 40

    func_start = time.perf_counter()
    print("Resource Group".ljust(column_width) + "Location")
    print("-" * (column_width * 2))

    row_count = 0
    for group in list(group_list):
        row_count += 1
        print(f"{group.name:<{column_width}}{group.location}")
    
    func_elapsed = time.perf_counter() - func_start
    print_info(f"{row_count} in {func_elapsed:.2f} secs.")
    return row_count


def resource_list(subscription_id="", resource_group="") -> int:
    """List resources in specified resource group for subscription.

    Equivalent to: az resource list --output table
    Name  ResourceGroup  Location  Type  Status
    See https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-list-resource-groups?tabs=bash
    """
    # Import the needed credential and management objects from the libraries.
    #from azure.identity import DefaultAzureCredential
    #import os

    # Acquire a credential object.
    credential = DefaultAzureCredential()

    # Retrieve subscription ID from environment variable.
    if not subscription_id:
        subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    if not resource_group:
        resource_group = os.getenv("AZURE_RESOURCE_GROUP")

    # Obtain the management object for resources.
    resource_client = ResourceManagementClient(credential, subscription_id)

    func_start = time.perf_counter()
    # Retrieve the list of resources in "myResourceGroup" (change to any name desired).
    #from azure.mgmt.resource import ResourceManagementClient
    resource_list = resource_client.resources.list_by_resource_group(
        resource_group, expand = "createdTime,changedTime")

    # Show the groups in formatted output
    column_width = 36

    print("Resource".ljust(column_width) + "Type".ljust(column_width)
        + "Create date".ljust(column_width) + "Change date".ljust(column_width))
    print("-" * (column_width * 4))

    row_count = 0
    for resource in list(resource_list):
        row_count += 1
        print(f"{resource.name:<{column_width}}{resource.type:<{column_width}}"
        f"{str(resource.created_time):<{column_width}}{str(resource.changed_time):<{column_width}}")

    func_elapsed = time.perf_counter() - func_start
    print_info(f"{row_count} in {func_elapsed:.2f} secs.")
    return row_count

    
def get_resource_group(subscription_id, region_filter) -> str:
    """Return a list of existing resources for a specified region.

    Alternative to https://portal.azure.com/#browse/resourcegroups
    # https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-list-resource-groups?tabs=bash
    """
    print_trace(f"get_resource_group() subscription_id: \"{subscription_id}\" region_filter: \"{region_filter}\"")
    try:
        #from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()

        #from azure.mgmt.resource import ResourceManagementClient 
        resource_client = ResourceManagementClient(credential, subscription_id)
        print_trace(f"get_resource_group() resource_client: \"{str(resource_client)}\")")
        group_list = resource_client.resource_groups.list()
        #print_info(f"get_resource_group() found {len(group_list)} resource groups.")
            # FIXME: object of type 'ItemPaged' has no len() 

        # Print each line using "rg" the common abbreviation for "resource group":
        for rg in list(group_list):
            if rg.location == region_filter:
                print_info(f"Resource_group: \"{rg.name}\" for region {rg.location} within get_resource_group() ")
                return rg.name  # the first one
            else:
                print_error(f"NO Resource_group: for region {rg.location} within get_resource_group() ")

    except Exception as e:
        print_error(f"get_resource_group() {e}")
        return None


def create_get_resource_group(credential, subscription_id, new_location) -> str:
    """Create Resource Group if the resource_group_name is not already defined.

    Return json object such as {'additional_properties': {}, 'id': '/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/resourceGroups/az-keyvault-for-python-250413', 'name': 'az-keyvault-for-python-250413', 'type': 'Microsoft.Resources/resourceGroups', 'properties': <azure.mgmt.resource.resources.v2024_11_01.models._models_py3.ResourceGroupProperties object at 0x1075ec1a0>, 'location': 'westus', 'managed_by': None, 'tags': None}
    Equivalent to CLI: az group create -n "myResourceGroup" -l "useast2"
        --tags "department=tech" "environment=test"
    Equivalent of Portal: https://portal.azure.com/#browse/resourcegroups
                          https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView
    See https://learn.microsoft.com/en-us/azure/developer/python/sdk/examples/azure-sdk-example-resource-group?tabs=cmd
    """
    try:
        if my_resource_group:
            print_info(f"create_get_resource_group() existing resource_group_name: \"{my_resource_group}\"")
            return my_resource_group
    except Exception as e:
        print_error(f"create_get_resource_group() global my_resource_group not defined: {e}")
        return None


    #uv add azure-mgmt-resource
    #uv add azure-identity
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.resource import ResourceManagementClient

    try:
        # Obtain the management object for resources:
        resource_client = ResourceManagementClient(credential, subscription_id)

        # Get all providers and their registration states:
        #all_providers = {provider.namespace: provider.registration_state for provider in resource_client.providers.list()}
        # print(f"create_get_resource_group() all_providers: {all_providers}")
        # TODO: List resource groups like https://portal.azure.com/#view/HubsExtension/BrowseResourceGroups.ReactView

        # Provision the resource group:
        rg_result = resource_client.resource_groups.create_or_update(
            my_resource_group, {"location": new_location}
        )
        print_info(f"create_get_resource_group() new resource_group_name: \"{my_resource_group}\"")
        return rg_result
    except Exception as e:
        print_error(f"create_get_resource_group() {str(rg_result)}")
        print_error(f"create_get_resource_group() {e}")
        # FIXME: ERROR: (InvalidApiVersionParameter) The api-version '2024-01-01' is invalid. The supported versions are 2024-11-01
        return None


def delete_resource_group(credential, resource_group_name, subscription_id) -> int:
    """Delete Azure resource group.
    
    Equivalent of CLI: az group delete -n PythonAzureExample-rg  --no-wait
    """
    try:
        resource_client = ResourceManagementClient(credential, subscription_id)
        if not resource_client:
            print(f"Cannot find ResourceManagementClient to delete_resource_group({resource_group_name})!")
            return False
        #rp_result = resource_client.resource_groups.begin_delete(resource_group_name)
            # EX: <azure.core.polling._poller.LROPoller object at 0x1055f1550>
        # if DEBUG: print(f"delete_resource_group({resource_group_name}) for {rp_result}")
        return True
    except Exception as e:
        print(f"delete_resource_group() ERROR: {e}")
        return False


#### SECTION 19. Azure Services Pricing by Resource


def load_costs_from_api(svc_name_in) -> str:
    """Load Azure costs from API.
    
    STATUS: Not working
    Calls Azure's unauthenticated Retail Prices API iteratively for all Azure services 
    into a database for access based on sku, to retrieve the region containing the lowest price.
    Because of the amount of data, each API call returns a "$skip=1000".
    The API holds several "Meter" (versions).
    Since prices change often, data is pulled again and stored in-memory as an array.
    served by an AI Agent that responds to MCP host.
    https://www.cloudbolt.io/azure-costs/azure-sql-pricing/
    https://docs.azure.cn/en-us/azure-sql/database/in-memory-oltp-monitor-space
    A web page linking to Azure services and pricing is at:
    https://azure.microsoft.com/en-us/products/
    """
    svc_name_in="Cognitive Services" # skuName in this function's signature
    print_verbose(f"load_costs_from_api( svc_name_in: {svc_name_in}) ...")
    # FUTURE: svc_skus = ["KeyVault","VirtualMachines"]   # ???
    
    base_url = "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&meterRegion='primary"
        # Primary meter filtering is supported with 2021-10-01 and later API versions including 2023-01-01.
        # The "?" is required for the filter query!
    all_items = []  # Responses accumulated into this.
    while base_url:  # inifinite loop:
        filter_query = f"?$filter=serviceName eq '{svc_name_in}'"
        url = base_url + filter_query
        # NOTE: $filter=serviceFamily eq 'Compute' returns too many items.
        # NOTE: "type": "Consumption" or "Reservation" or "Meter" or "Usage"
        # https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&meterRegion='primary'&currencyCode='USD'&$filter=serviceName eq 'Virtual Machines'
        # After pagination that translates to:
        # https://prices.azure.com:443/api/retail/prices?$filter=serviceName%20eq%20%27Virtual%20Machines%27&$skip=1000
        try:
            # import requests
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch data: {response.status_code}")
                break  # from while
            data = response.json()
            all_items.extend(data.get('Items', []))
            url = data.get('next_pageLink')
        except Exception as e:
            print_error(f"load_costs_from_api(): {e}")
            return None

    # Group by serviceName and print cost details:
    service_costs = {}
    for item in all_items:
        #meter_name = item.get('meterName')
        service_name = item.get('serviceName')
        sku = item.get('skuName')
        armsku = item.get('armSkuName')
        product = item.get('productName')

        price = item.get('retailPrice')
        unit = item.get('unitOfMeasure')
        region = item.get('armRegionName')
        if service_name not in service_costs:
            service_costs[service_name] = []
        service_costs[service_name].append((sku, price, unit, region))

    # Print summary:
    for service_name, prices in service_costs.items():
        if service_name == svc_name_in:
            print(f"\nService: {service_name}")
            for sku, armsku, product, price, unit, region in prices:
                # ValueError: too many values to unpack (expected 6, got 4)
                print(f"  {sku} | {armsku} | {product} | {price} | {unit} | {region}")

    # NOTE: tierMinimumUnits is the minimum number of units that can be purchased.
    # NOTE: reservationTerm	1 year	Reservation term – one year or three years

    # TODO: Return lowest cost region for the given service SKU.


def get_azure_service_costs(sku_name) -> str:
    """Get Azure Service Costs.
     
    STATUS: Not working 
    Returns the lowest cost by region for each given service SKU, based on unauthenticated access to the 
    Azure Retail Prices API for all Azure services (organized within a Meter):
    See https://spot.io/resources/azure-pricing/the-complete-guide/#:~:text=Azure%20Advisor-,Azure%20Pricing%20Models,reserved%20instances%2C%20and%20spot%20instances.
    and https://umbrellacost.com/blog/azure-pricing-guide/?hsa_acc=7559118320&hsa_cam=22420396504&hsa_grp=181520889030&hsa_ad=744486570175&hsa_src=s&hsa_tgt=dsa-19959388920&hsa_kw=&hsa_mt=&hsa_net=adwords&hsa_ver=3&gad_source=5
    See https://learn.microsoft.com/en-us/rest/api/cost-management/retail-prices/azure-retail-prices
    and https://dev.to/holger/how-to-retrieve-a-list-of-available-services-from-the-azure-retail-rates-prices-api-2nk6
    Based on https://www.perplexity.ai/search/python-code-to-get-cost-of-eac-chT5VY0TQiiIrYUnCN11aw
    and docs https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/storage/blobs/storage-blob-python-get-started.md
             https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/storage/blobs/storage-blob-object-model.md

    After obtaining meters as JSON: https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview
    Each call returns a "$skip=1000".
    So this function accumulates to the "all_items" in-memory build_pricing_table (array) from multiple calls to the API,

    Filters: Meter: "NP20s Spot", currencyCode: USD, "serviceName": "Virtual Machines", "serviceFamily": "Compute"
    | skuName        | armSkuName | productName                        | retailPrice | unitOfMeasure  | armRegionName  |
    |----------------+------------+------------------------------------+-------------+----------------+----------------|
    | Standard_NP20s | NP20s Spot | Virtual Machines NP Series Windows |    0.828503 | 1 Hour         | southcentralus |
    
    The above is modified from the table at https://azure.microsoft.com/en-us/pricing/details/virtual-machines/windows/
    Not shown: "productId": "DZH318Z0D1L7", "skuId": "DZH318Z0D1L7/018J",
    # {
    # "effectiveStartDate": "2019-05-14T00:00:00Z",
    # "meterId": "0084b086-37bf-4bee-b27f-6eb0f9ee4954",
    # "meterName": "M8ms",

    #    "serviceFamily": "Compute",
    #    "productId": "DZH318Z0BQ4W",
    #    "skuId": "DZH318Z0BQ4W/00BQ",
    #    "availabilityId": null,

    #       "serviceId": "DZH313Z7MMC8",
    #       "serviceName": "Virtual Machines",
    #       "productName": "Virtual Machines MS Series",
    #          "skuName": "M8ms",
    #          "armSkuName": "Standard_M8ms",
    #                "isPrimaryMeterRegion": true,
    #                "armRegionName": "southindia",
    #                "location": "IN South",
    #                    "currencyCode": "USD",
    #                    "retailPrice": 2.305,
    #                    "unitPrice": 2.305,
    #                    "unitOfMeasure": "1 Hour",
    #                    "tierMinimumUnits": 0.0,
    #                    "type": "Consumption",
    #        "savingsPlan": [
    #            {
    #                "unitPrice": 0.8065195,
    #                "retailPrice": 0.8065195,
    #                "term": "3 Years"
    #            },
    #            {
    #                "unitPrice": 1.5902195,
    #                "retailPrice": 1.5902195,
    #                "term": "1 Year"
    #            }
    #        ]
    #    },
    #
    # for svc_sku in svc_skus:
    """
    svc_name_in="Cognitive Services" # skuName in this function's signature
    print_verbose(f"load_costs_from_api( svc_name_in: {svc_name_in}) ...")
    # FUTURE: svc_skus = ["KeyVault","VirtualMachines"]   # ???
    
    service = "Microsoft Dev Box"
    sku_name = "Standard_F64s_v2"
    arm_sku_name = "Standard"
    region_code = "westcentralus"
    base_url = "https://prices.azure.com/api/retail/prices?api-version=2023-01-01-preview&meterRegion='primary"
    filter_query = ""
    #filter_query = f"?$filter=arm_sku_name eq '{arm_sku_name}'"
    #filter_query = f"?$filter=service eq '{service}'"
    filter_query = f"?$filter=armRegionName eq '{region_code}'"
    url = base_url + filter_query

    all_items = []
    while base_url:
        # import requests
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch data: {response.status_code}")
            break
            # Failed to fetch data: 400
        data = response.json()
        all_items.extend(data.get('Items', []))
        url = data.get('next_pageLink')
        # TODO: Save all_items to a database for access based on sku, to retrieve the region containing the lowest price.

    # Group by serviceName and print cost details
    service_costs = {}
    for item in all_items:
        service_name = item.get('serviceName')
        sku_name = item.get('skuName')
        arm_sku_name = item.get('armSkuName')
        price = item.get('retailPrice')
        unit = item.get('unitOfMeasure')
        region = item.get('armRegionName')
        if service_name not in service_costs:
            service_costs[service_name] = []
        service_costs[service_name].append((sku_name, price, unit))

    item_count = 0
    # TODO: if item_count are found meeting filter:
    # Print summary 
    if item_count > 0:
        print_heading("  armSkuName   | sku    | price | unit | region | armSkuName | product ")
    for service, prices in service_costs.items():
        print_heading(f"{service}:")
        for arm_sku_name, price, unit in prices:
            print(f"  {arm_sku_name:<15} | {sku_name:<35} | {price:<10} | {unit:<10} | {region} ")
                # FIXME: only a single region appears, and not the filter value.
    return "ha ha"


# API Management

# Service: Time Series Insights
#  SKU: S1 | Price: 4.838709 | Unit: 1/Day
#  SKU: Data Processing | Price: 0.2 | Unit: 1 GB


def az_costmanagement(subscription_id) -> bool:
    """Azure Cost Management.

    STATUS: NOT WORKING
    https://learn.microsoft.com/en-us/rest/api/cost-management/
    for both "Usage" and "ActualCost"
    # Cost Management Portal: https://portal.azure.com/#view/Microsoft_Azure_CostManagement/Menu/~/overview
    Based on https://www.perplexity.ai/search/python-code-to-obtain-azure-us-cMV6v.PtTISPHWKAB_0ZNA#0
    """
    try:
        #from azure.mgmt.costmanagement import CostManagementClient, models
        #from azure.identity import DefaultAzureCredential
        #from settings import subscription_id, DEFAULT_LOCATION, DEFAULT_RESOURCE_GROUP
        credential = DefaultAzureCredential()
        cm_client = CostManagementClient(credential, subscription_id)
    except Exception as e:
        print_error(f"az_costmanagement() client: {e}")
        return False
    
    # azure.mgmt.consumption.models
    try:
        query = cm_client.query.usage(
            scope=f'/subscriptions/{subscription_id}',
            parameters=models.QueryDefinition(type='Usage')
        )
        print_verbose(f"az_costmanagement(): Usage: {query}")

        query = cm_client.query.usage(
            scope=f'/subscriptions/{subscription_id}',
            parameters=models.QueryDefinition(type='ActualCost')
        )
        print_verbose(f"az_costmanagement(): ActualCost: {query}")

        # print_info(f"az_costmanagement(): {end info ???}")
        return True
    except Exception as e:
        print_error(f"az_costmanagement(): {e}")
        return False


def az_billing(credential, subscription_id) -> bool:
    """Azure billing.
    
    STATUS: NOT WORKING
    Tutorial: https://learn.microsoft.com/en-us/azure/cost-management-billing/
    Tutorial: https://learn.microsoft.com/en-us/azure/cost-management-billing/manage/view-all-accounts
    Portal: https://portal.azure.com/#view/Microsoft_Azure_GTM/BillingAccountMenuBlade/~/Overview/
    Portal: https://portal.azure.com/#view/Microsoft_Azure_GTM/ModernBillingMenuBlade/~/BillingAccounts
    https://portal.azure.com/#view/Microsoft_Azure_GTM/Billing.MenuView/~/overview/scopeId/
    See https://www.udemy.com/course/python-sdk-for-azure-bootcamp/learn/lecture/39013196#overview
    """
    #import os
    try:
        #from azure.mgmt.billing import BillingManagementClient
        #from azure.identity import DefaultAzureCredential
        billing_client = BillingManagementClient(credential, subscription_id)
        accounts_obj = billing_client.billing_accounts.list()
        print_trace(f"az_billing(): Billing Account Display Name: {accounts_obj} ")
        for account in accounts_obj:
            account_name_guid = account.name
            print_verbose(f"az_billing(): Billing Account GUID: {account_name_guid}")
            billing_account = billing_client.billing_accounts.get(account_name_guid)
            print_trace(f"az_billing(): Billing Account: {billing_account}")
            # QUESTION: How to get 'billing_account_name' displayName like "John Doe"?
        return True
    except Exception as e:
        print_error(f"az_billing(): ERROR: {e}")
        return False



#### SECTION 20. Azure Blob Storage Containers

    
def get_az_blob_storage_acct_name() -> str:
    """Return the storage account name from parm or the environment variable AZURE_STORAGE_ACCOUNT in os.
    
    environ.
    using from global my_subscription_id and my_az_svc_region
    ??? Authenticate using a connection string or with Azure Active Directory (recommended for security).
    See https://learn.microsoft.com/en-us/python/api/overview/azure/storage-blob-readme?view=azure-python 
    See https://learn.microsoft.com/en-us/azure/developer/python/sdk/fundamentals/errors
    """
    # NOTE: Parms defined in CLI call take precedence over .env:

    # STEP 3: Try to get AZURE_STORAGE_ACCOUNT from CLI parms:
    # AZURE_STORAGE_ACCOUNT = args.storage  # done in code above.
    if AZURE_STORAGE_ACCOUNT:
        print_info(f"--storage_account \"{AZURE_STORAGE_ACCOUNT}\" from parms within get_az_blob_storage_acct_name() ")
        return AZURE_STORAGE_ACCOUNT
    else:
        print_trace("--storage_account \"___\" not defined in parms within get_az_blob_storage_acct_name() ")

    # STEP 2: Try to get AZURE_STORAGE_ACCOUNT from .env file:
    storage_account_name = get_str_from_env_file("AZURE_STORAGE_ACCOUNT")
        # instead of storage_account_name = os.environ["AZURE_STORAGE_ACCOUNT"]
    if storage_account_name:
        print_info(f"AZURE_STORAGE_ACCOUNT=\"{storage_account_name}\" from .env within get_az_blob_storage_acct_name() ")
        return storage_account_name
    # else:

    # STEP 3: See if an account has already been created within global subscription id
    if my_subscription_id:
        subscription_id = my_subscription_id  # from global
        if not subscription_id:  # available:
            print_error("No global Subscription_id for use within get_az_blob_storage_acct_name()!")
            return None    
        print_trace(f"Using global subscription_id=\"{subscription_id}\" within get_az_blob_storage_acct_name() ")
        # from azure.identity import DefaultAzureCredential
        credential = DefaultAzureCredential()   # Authenticate.
        # from azure.mgmt.storage import StorageManagementClient
        storage_client = StorageManagementClient(credential, subscription_id)
        # List all storage accounts in the subscription
        accounts_obj = storage_client.storage_accounts.list()
        print_trace(f"accounts_obj=\"{list(accounts_obj)}\" within get_az_blob_storage_acct_name() ")
        if list(accounts_obj):
            # TODO: Print storage account names and their blob endpoints:
            print_info("get_az_blob_storage_acct_name(): specify --storage or AZURE_STORAGE_ACCOUNT in .env!")
            for account in accounts_obj:
                print(f"Name: {account.name}")
                print(f"Resource Group: {account.id.split('/')[4]}")
                # Blob endpoint is typically in the primary_endpoints property
                if account.primary_endpoints and account.primary_endpoints.blob:
                    print(f"Blob Endpoint: {account.primary_endpoints.blob}")
                print("-" * 40)
        else:
            print_error("No Azure blob storage accounts found for subscription_id within get_az_blob_storage_acct_name()!")
            # TODO: Create storage account:

    # STEP 4: Define new account based on the Region:
    # WARNING: No underlines or dashes in storage account name up to 24 characters:
    if not my_az_svc_region:
        print_error("Global Region not available in get_az_blob_storage_acct_name()")
        return None
    else:
        # get_az_blob_storage_acct_name()
        fts = datetime.fromtimestamp(time.time(), tz=timezone.utc)
        date_str = fts.strftime("%y%m")  # EX: "...-250419" no year, minute, UTC %y%m%d%H%M%Z https://strftime.org
        # Max. my_az_svc_region is "germanywestcentral" of 19 characters + 5 (yymm of 2504) = 24 characters (the max):
        storage_account_name = f"{date_str}{my_az_svc_region}"  # no dashes/underlines
        # Example: AZURE_STORAGE_ACCOUNT="germanywestcentral-2504"
        # Alternative: AZURE_STORAGE_ACCOUNT = f"pythonazurestorage{random.randint(1,100000):05}"
        print_verbose(f"storage_acct_name \"{storage_account_name}\" defined from global region in create_az_blog_storage_acct() ")
    return None


def create_az_blog_storage_acct(storage_acct_name, credential, subscription_id, resource_group_name, new_location) -> str:
    """Return an Azure storage account object for the given account name.

    using global AZURE_STORAGE_ACCOUNT
    At Portal: https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts
    Equivalent CLI: az cloud set -n AzureCloud   // return to Public Azure.
    az storage account create --name mystorageacct --resource-group mygroup --location eastus --sku Standard_LRS --kind StorageV2 --api-version 2024-08-01
    # TODO: allowed_copy_scope = "MicrosoftEntraID" to prevent data exfiltration from untrusted sources.
        See https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    # TODO: PrivateLink endpoints
    https://microsoftlearning.github.io/DP-900T00A-Azure-Data-Fundamentals/Instructions/Labs/dp900-02-storage-lab.html
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.storage import StorageManagementClient
    #from azure.storage.blob import BlobServiceClient
    #import os

    if not storage_acct_name:
        # WARNING: No underlines or dashes in storage account name up to 24 characters:
        fts = datetime.fromtimestamp(time.time(), tz=timezone.utc)
        date_str = fts.strftime("%y%m")  # EX: "...-250419" no year, minute, UTC %y%m%d%H%M%Z https://strftime.org
        # Max. my_az_svc_region is "germanywestcentral" of 19 characters + 5 (yymm of 2504) = 24 characters (the max):
        storage_account_name = f"{date_str}{my_az_svc_region}"  # no dashes/underlines
        # Example: AZURE_STORAGE_ACCOUNT="germanywestcentral-2504"
        # Alternative: AZURE_STORAGE_ACCOUNT = f"pythonazurestorage{random.randint(1,100000):05}"
        print_verbose(f"storage_acct_name \"{storage_account_name}\" defined from region in create_az_blog_storage_acct() ")


    # Fetch current account properties
    storage_client = obtain_blob_storage_object(credential, subscription_id)
    if not storage_client:
        print_error("create_az_blog_storage_acct(): obtain_blob_storage_object() failed to fetch storage_client! ")
        exit(9)
    else:  # redundant
        print_trace(f"create_az_blog_storage_acct(): {storage_client}")


    try:
        # Fetch current storage account properties:
        account_props = storage_client.storage_accounts.get_properties(resource_group_name, storage_account_name)
        print_verbose(f"create_az_blog_storage_acct() properties: {account_props}")
           #  {'additional_properties': {}, 'id': '/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/resourceGroups/westus2-2589c1/providers/Microsoft.Storage/storageAccounts/westus32505', 
           # 'name': 'westus32505', 'type': 'Microsoft.Storage/storageAccounts', 'tags': {}, 'location': 'westus3', 
           # 'sku': <azure.mgmt.storage.v2024_01_01.models._models_py3.Sku object at 0x10a13ae90>, 
           # 'kind': 'StorageV2', 'identity': None, 'extended_location': None, 'provisioning_state': 'Succeeded', 
           # 'primary_endpoints': <azure.mgmt.storage.v2024_01_01.models._models_py3.Endpoints object at 0x10a13b390>, 
           # 'primary_location': 'westus3', 'status_of_primary': 'available', 'last_geo_failover_time': None, 
           # 'secondary_location': None, 'status_of_secondary': None, 'creation_time': datetime.datetime(2025, 5, 4, 2, 9, 28, 507661, 
           #  tzinfo=<isodate.tzinfo.Utc object at 0x103f26660>), 'custom_domain': None, 'sas_policy': None, 'key_policy': None, 
           # 'key_creation_time': <azure.mgmt.storage.v2024_01_01.models._models_py3.KeyCreationTime object at 0x118322fd0>, 
           # 'secondary_endpoints': None, 'encryption': <azure.mgmt.storage.v2024_01_01.models._models_py3.Encryption object at 0x118322210>, 
           # 'access_tier': 'Hot', 'azure_files_identity_based_authentication': None, 
           # 'enable_https_traffic_only': True, 'network_rule_set': <azure.mgmt.storage.v2024_01_01.models._models_py3.NetworkRuleSet object at 0x118320f50>, 
           # 'is_sftp_enabled': None, 'is_local_user_enabled': None, 'enable_extended_groups': None, 'is_hns_enabled': None, 
           # 'geo_replication_stats': None, 'failover_in_progress': None, 'large_file_shares_state': None, 
           # 'private_endpoint_connections': [], 'routing_preference': None, 'blob_restore_status': None, 
           # 'allow_blob_public_access': False, 'minimum_tls_version': 'TLS1_2', 'allow_shared_key_access': None, 
           # 'enable_nfs_v3': None, 'allow_cross_tenant_replication': False, 'default_to_o_auth_authentication': None, 
           # 'public_network_access': None, 'immutable_storage_with_versioning': None, 'allowed_copy_scope': None, 
           # 'storage_account_sku_conversion_status': None, 'dns_endpoint_type': None, 'is_sku_conversion_blocked': None, 
           # 'account_migration_in_progress': None} 
    except Exception as e:
        print_trace(f"create_az_blog_storage_acct(): account_props: {e}")
            # (ResourceNotFound) The Resource 'Microsoft.Storage/storageAccounts/westus32505' under resource group 'westus2-2589c1' was not found. 
            # For more details please go to https://aka.ms/ARMResourceNotFoundFix 
            # Code: ResourceNotFound
            # Message: The Resource 'Microsoft.Storage/storageAccounts/westus32505' under resource group 'westus2-2589c1' was not found. 
            # For more details please go to https://aka.ms/ARMResourceNotFoundFix 
        pass  # to create storage account below
    else:  # if storage account already exists:
        # List all storage accounts in the subscription for credential:
        storage_accounts = storage_client.storage_accounts.list()
        for account in storage_accounts:
            print_verbose(f"Storage Account: \"{account.name}\" in \"{account.location}\" within create_az_blog_storage_acct() ")
        return storage_account_name

    # CAUTION: API version needs update occassionally:
    # See https://learn.microsoft.com/en-us/python/api/azure-mgmt-storage/azure.mgmt.storage.storagemanagementclient?view=azure-python
    parameters = {
        "location": new_location,
        "kind": "StorageV2",
        "api_version": "2024-01-01",
        "sku": {"name": "Standard_LRS"},
        "deleteRetentionPolicy": {
            "enabled": True,
            "days": 99  # Set between 1 and 365
        },
        "minimum_tls_version": "TLS1_2"
    }  # LRS = Locally-redundant storage
    # TODO: Set soft delete policies, 
    # For update: https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    # https://learn.microsoft.com/en-us/rest/api/storagerp/storage-accounts/create?view=rest-storagerp-2024-01-01&tabs=HTTP
    try:  # Create the storage account:
        poller = storage_client.storage_accounts.begin_create(
            resource_group_name=resource_group_name,
            account_name=storage_account_name,
            api_version="2024-01-01",
            parameters=parameters
        )
        # Wait for completion:
        account_result = poller.result()
        print_info(f"create_az_blog_storage_acct(\"{account_result.name}\") created!")
        return account_result  # storage_account_name
    except Exception as e:
        print_error(f"create_az_blog_storage_acct(): {e}")
        # FIXME: api_version="2024-03-01" -> API version 2024-03-01 does not have operation group 'storage_accounts' 
        # See https://www.perplexity.ai/search/azure-api-version-2024-03-01-d-7aatmHRXQ32L0PF3zaraxg#0
        return None

# def create_az_blob_storage_container():
    """
    Create an unlimited number of Azure Blob Storage Containers 
    to organize a set of blobs (similar to a directory in a file system).
    Also, a container can store an unlimited number of blobs.
    The URI for a container is similar to:
    https://sampleaccount.blob.core.windows.net/sample-container
    For more information about naming containers, 
    see https://github.com/MicrosoftDocs/azure-docs/blob/main/rest/api/storageservices/Naming-and-Referencing-Containers--Blobs--and-Metadata
    """


def obtain_blob_storage_object(credential, subscription_id) -> object:
    """Return an Azure blob storage client object for the given credential and subscription ID.

    after creating it manually at Portal: https://portal.azure.com/#browse/Microsoft.Storage%2FStorageAccounts
    There are three types of blobs:
    A. Block blobs store text and binary data in blocks of data that can be managed individually. 
    Block blobs can store up to about 190.7 TiB.
    B. Append blobs are made up of blocks like block blobs optimized for logging data from virtual machines.
    C. Page blobs store random access files up to 8 TiB in size. See https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/storage/blobs/storage-blob-pageblob-overview.md

    The URI for a blob is similar to:
    https://sampleaccount.blob.core.windows.net/sample-container/sample-blob
    See https://github.com/MicrosoftDocs/azure-docs/blob/main/rest/api/storageservices/understanding-block-blobs--append-blobs--and-page-blobs

    Equivalent CLI: az cloud set -n AzureCloud   // return to Public Azure.
    # TODO: allowed_copy_scope = "MicrosoftEntraID" to prevent data exfiltration from untrusted sources.
        See https://www.perplexity.ai/search/python-code-to-set-azure-stora-549_KJogQOKcFMcHvynG3w#0
    # TODO: PrivateLink endpoints
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.mgmt.storage import StorageManagementClient
    #import os
    storage_account_name = get_az_blob_storage_acct_name()
    if storage_account_name:
        print_verbose("Storage Account: \"{storage_account_name}\" within obtain_blob_storage_object() ")
        return storage_account_name
    #else: AZURE_STORAGE_ACCOUNT not found:
    try:
        # Initialize and return a StorageManagementClient to manage Azure Storage Accounts:
        #from azure.storage.blob import BlobServiceClient
        #from azure.core.exceptions import HttpResponseError
        account_url = f"https://{storage_account_name}.blob.core.windows.net"
        # container_client = blob_service_client.get_container_client("your-container")

        credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)
            # F841 Local variable `blob_service_client` is assigned to but never used
        print(f"obtain_blob_storage_object():blob_service_client={blob_service_client} ")
        storage_client = StorageManagementClient(
            credential=credential,
            subscription_id=subscription_id,
            # api_version="2024-01-01" 
            #resource_group=resource_group,
            #storage_account_name=storage_account_name,
            #location=my_az_svc_region
        )
        print_verbose(f"obtain_blob_storage_object(): {storage_client}")
        return storage_client
    except HttpResponseError as e:
        print(f"HTTP error occurred: {e.message} (status code {e.status_code})")
        if e.status_code == 403:
            print("obtain_blob_storage_object(): Access denied: check permissions.")
        elif 500 <= e.status_code < 600:
            print("obtain_blob_storage_object(): Server error: consider retry logic.")
    except Exception as e:
        print_error(f"obtain_blob_storage_object(): {e}")
        return None


def ping_az_storage_acct(storage_account_name) -> str:
    """Ping Azure Storage Account.

    CAUTION: This is not currently used due to "Destination Host Unreachable" error.
    Returns the ping utility latency to a storage account within the Azure cloud.
    """
    ping_host = f"{storage_account_name}.blob.core.windows.net"
    try:
        # from pythonping import ping
        response = ping(ping_host, count=5, timeout=2)
        response_text = f"Min-Avg-Max Latency: {response.rtt_min_ms:.2f}-{response.rtt_avg_ms:.2f}-{response.rtt_max_ms:.2f} ms"
        response_text =+ f"  Packet loss: {response.packet_loss * 100:.0f}%"
        return response_text
    except Exception as e:  # such as "Destination Host Unreachable"
        print_error(f"ping_az_storage_acct() ERROR: {e}")
        return None
 

def tag_storage(resource_group,storage_acct) -> bool:
    """Update storage resources with tag."""
    #import os
    #from azure.identity import AzureCliCredential
    #credential = AzureCliCredential()
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    #from azure.mgmt.resource import ResourceManagementClient
    #resource_client = ResourceManagementClient(credential, subscription_id)
    tags = {
        "Dept": "Finance",
        "Status": "Normal"
    }
    #from azure.mgmt.resource.resources.models import TagsResource
    tag_resource = TagsResource(
        properties={'tags': tags}
    )
    resource = resource_client.resources.get_by_id(
        f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Storage/storageAccounts/{storage_acct}",
        "2022-09-01"
    )
    resource_client.tags.begin_create_or_update_at_scope(resource.id, tag_resource)
    print(f"Tags {tag_resource.properties.tags} were added to resource with ID: {resource.id}")
    return True



# def create_storage_blob():
#     See https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-delete-python

# def delete_storage_blob():
#     """
#     A blob that was soft deleted due to the delete_retention_policy.
#     See https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blob-delete-python
#     See https://learn.microsoft.com/en-us/rest/api/storageservices/delete-blob
#     """
#     # from azure.identity import DefaultAzureCredential
      # from azure.storage.blob import BlobServiceClient
      # First, delete all snapshots under the storageaccount:
      # undelete_storage_blob():

# def access_storage_blob():


# TODO: Azure Data Factory for data integration, 
# TODO: Azure Gen2 Data Lake Storage of structured & unstructured data (videos)
# TODO: Synapse Analytics (Spark ETL jobs)

# TODO: set the principal with the appropriate level of permissions (typically Directory.Read.All for these operations).


def get_func_principal_id(credential, app_id, tenant_id) -> object:
    """Get Func Principal ID.

    TODO: Get userId by decoding function's X-MS-CLIENT-PRINCIPAL header. Sometimes, properties like userPrincipalName or name might not be present, 
    depending on the identity provider or user type (like guest users). 
    In such a case, check the userDetails property, which often contains the user's email or username.
    # Extract the user's email from the claims using:  user_email = client_principal.get('userDetails')
    based on https://learn.microsoft.com/en-us/answers/questions/2243286/azure-function-app-using-python-how-to-get-the-pri
    """
    app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
    return app


# @app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    """Trigger HTTP."""
    logging.info('Python HTTP trigger function processed a request.')

    # Retrieve the X-MS-CLIENT-PRINCIPAL header
    client_principal_header = req.headers.get('X-MS-CLIENT-PRINCIPAL')
    logging.info(f"X-MS-CLIENT-PRINCIPAL header: {client_principal_header}")
    user_name = None

    if client_principal_header:
        try:
            # Decode the Base64-encoded header
            decoded_header = base64.b64decode(client_principal_header).decode('utf-8')
            logging.info(f"Decoded X-MS-CLIENT-PRINCIPAL: {decoded_header}")
            client_principal = json.loads(decoded_header)

            # Log the entire client principal for debugging
            logging.info(f"Client Principal: {client_principal}")

            # Extract the user's name from the claims
            user_name = client_principal.get('userPrincipalName') or client_principal.get('name')
        except Exception as e:
            logging.error(f"Error decoding client principal: {e}")

    if user_name:
        return func.HttpResponse(f"Hello, {user_name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. However, no authenticated user information was found.",
            status_code=200
        )


#### SECTION 21. TODO: Azure Keyvault


def create_content_safety_policy(credential, subscription_id, resource_group_name, keyvault_name) -> bool:
    """Create content safety policy.

    CAUTION: Before running this function, manual steps need to be taken in the GUI Portal to obtain the CONTENT_SAFETY_KEY and ENDPOINT:
    https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/05-implement-content-safety.html
    """
    # pip install azure-ai-contentsafety
    # Set endpoint and key as environment variables for security:
    # export/setx CONTENT_SAFETY_KEY "YOUR_CONTENT_SAFETY_KEY"
    # export/setx CONTENT_SAFETY_ENDPOINT "YOUR_CONTENT_SAFETY_ENDPOINT"

    # import os
    # from azure.ai.contentsafety import ContentSafetyClient
    # from azure.core.credentials import AzureKeyCredential
    # from azure.core.exceptions import HttpResponseError
    # from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory


def define_keyvault_name(my_az_svc_region) -> str:
    """Come up with a globally unique keyvault name that's 24 characters long."""
    if AZURE_KEYVAULT_NAME:  # defined by parameter:
        print_info(f"-kv \"{AZURE_KEYVAULT_NAME}\"  # (AZURE_AZURE_KEYVAULT_NAME) being used.")
        return AZURE_KEYVAULT_NAME
    # else see if .env file has a value:
    try:
        keyvault_name = os.environ["AZURE_AZURE_KEYVAULT_NAME"]  # EntraID
        print_info(f"AZURE_AZURE_KEYVAULT_NAME = \"{keyvault_name}\"  # from .env file being used.")
        return keyvault_name
    except KeyError:
        pass

    # TODO: Calcuate how many characters can fit within 24 character limit.
    # With the longest region name being 18, such as "westcentralus-fa5bdb":
    keyvault_name = f"{my_az_svc_region}-{uuid.uuid4().hex[:6]}"
        # So no room for prefix "kv-" as in
    #    my_keyvault_root = os.environ["AZURE_KEYVAULT_ROOT_NAME"]
    #except KeyError as e:
    #    my_keyvault_root = "kv"
    # Also no room for both: "{my_keyvault_root}-{my_az_svc_region}-{get_log_datetime()}"
        # PROTIP: Define datestamps Timezone UTC: https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow
    return keyvault_name


def check_keyvault(credential, keyvault_name, vault_url) -> int:
    """Check if a Key Vault exists.

    Return True if found, False if not.
    See https://learn.microsoft.com/en-us/python/api/overview/azure/keyvault-secrets-readme?view=azure-python
    """
    #from azure.identity import DefaultAzureCredential
    #from azure.keyvault.secrets import SecretClient
    #from azure.core.exceptions import HttpResponseError
    #import sys
    
    client = SecretClient(vault_url=vault_url, credential=credential)
        # Expected: "<azure.keyvault.secrets._client.SecretClient object at 0x106fc42f0>")
    if not client:
        print_fail(f"check_keyvault(client) failed to obtain client: \"{client}\")")
        exit(9)
    secrets = client.list_properties_of_secrets()
        # Expected: <iterator object azure.core.paging.ItemPaged at 0x106911550>
    if not secrets:
        print_fail(f"check_keyvault(client) failed to obtain secrets: \"{secrets}\") ...")
        exit(9)

    try:
        for secret in secrets:
            # CAUTION: Avoid printing out {secret.name} values in logs:
            print_verbose(f"check_keyvault(\"{keyvault_name}\" exists with secrets.")
            return True
        else:
            print_info(f"check_keyvault({keyvault_name}) Vault exists but contains no secrets.")
            return True
    except Exception as e:
        print_fail(f"Key Vault not recognized in check_keyvault({keyvault_name}): {e}")
        # This is expected if the Key Vault does not exist.
        return False  # KeyVault not found, so create it!


def create_keyvault(credential, subscription_id, resource_group, keyvault_name, location, tenant_id, user_principal_id) -> object:
    """Create KeyVault.

    # 1. Ensure the credential is for a service principal with Key Vault Contributor or Contributor RBAC role assignments.
    # Equivalent to CLI: az keyvault create --name "{$keyvault_name}" -g "${resc_group}" --enable-rbac-authorization 
    # 2. Create the Key Vault using azure-mgmt-keyvault
    Alternative is https://registry.terraform.io/modules/Azure/avm-res-keyvault-vault/azurerm/latest
    Based on https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/02-ai-services-security/Python/keyvault_client/keyvault-client.py
    """
    resource_client = ResourceManagementClient(credential, subscription_id)
    if not resource_client:
        print(f"Cannot find ResourceManagementClient to create_keyvault({keyvault_name})!")
        return None
    
    # Create a KeyVault management client:
    keyvault_client = KeyVaultManagementClient(credential, subscription_id)
    if not keyvault_client:
        print(f"Cannot find KeyVaultManagementClient to create_keyvault({keyvault_name})!")
        return None

    # CAUTION: Replace <service-principal-object-id> with your SP’s object ID.
    keyvault_client.vaults.begin_create_or_update(
        resource_group,
        keyvault_name,
        {
            "location": location,
            "properties": {
                "tenant_id": tenant_id,
                "sku": {"name": "standard", "family": "A"},
                "access_policies": [{
                    "tenant_id": tenant_id,
                    "object_id": user_principal_id,
                    "permissions": {"secrets": ["all"], "keys": ["all"]}
                }]
            }
        }
    ).result()
    # TODO: CAUTION: set permissions to least privilege.


def delete_keyvault(credential, keyvault_name, vault_url) -> bool:
    """Delete KeyVault.
     
    Equivalent to CLI: az keyvault delete --name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())  
        if secret_client:
            secret_client.delete_secret(keyvault_name)
        return True
    except Exception as e:
        print(f"delete_keyvault() ERROR: {e}")
        return False


def populate_keyvault_secret(credential, keyvault_name, secret_name, secret_value) -> bool:
    """Populate KeyVault secret.
    
    Equivalent to az keyvault secret set --name "{$secret_name}" --value "{$secret_value}" --vault-name "{$keyvault_name}" 
    """
    # from azure.keyvault.secrets import SecretClient
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())    
        if secret_client:
            #TODO: rp_secret not used!
            #rp_secret = secret_client.set_secret(secret_name, secret_value)
            print(f"VERBOSE: populate_keyvault_secret(): secret_client={secret_client}")
        return True
    except Exception as e:
       print(f"populate_keyvault_secret() ERROR: {e}")
           # <urllib3.connection.HTTPSConnection object at 0x1054a5a90>: Failed to resolve 'az-keyvault-2504190459utc.vault.azure.net' ([Errno 8] nodename nor servname provided, or not known)
       return False


def get_keyvault_secret(credential, keyvault_name, secret_name) -> object:
    """Get KeyVault Secret value from key.
    
    Equivalent to CLI: az keyvault secret show --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        if secret_client:
            rp_secret = secret_client.get_secret(secret_name)
            if rp_secret:
                return rp_secret
        return None
    except Exception as e:
       print(f"get_keyvault_secret() ERROR: {e}")
       return None


def delete_keyvault_secret(credential, keyvault_name, secret_name) -> bool:
    """Delete KeyVault secret.
     
    Equivalent to CLI: 
    az keyvault secret delete --name "{$secret_name}" --vault-name "{$keyvault_name}" 
    """
    try:
        secret_client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
        if secret_client:
            rp_secret = secret_client.delete_secret(secret_name)
            if rp_secret:
                print_info(f"delete_keyvault_secret(\"{secret_name}\") done!")
                return True
        print_error(f"delete_keyvault_secret() {secret_client} failed!")
        return False
    except Exception as e:
       print_error(f"delete_keyvault_secret() ERROR: {e}")
       return False


#### SECTION 22. Azure Maps


def coords_from_string(coord_str):
    """Convert latitude longitude together in a string to a tuple.

    USAGE: Input to function is a string containing two numbers separated by a comma:
    coords = coords_from_string("44.6463, -49.583")
    For output coords = (44.6463, -49.583)
    """
    return tuple(map(float, coord_str.split(', ')))

def timezone_client(subscription_key=""):
    """Return Azure maps timezone client for latlong2timezone().
    
    https://learn.microsoft.com/en-us/python/api/overview/azure/maps-search-readme?view=azure-python-preview&preserve-view=true
    First create az maps account create --kind "Gen2" --account-name "myMapAccountName" --resource-group "<resource group>" --sku "G2"
    # https://portal.azure.com/#browse/Microsoft.Maps%2Faccounts
    # map-westcentralus-92b065 on Gen2
    # From "View Authentication" section, copy Primary key = your AZURE_timezone_SUBSCRIPTION_KEY in .env
    """
    # import os
    # from azure.core.credentials import AzureKeyCredential
    # from azure.core.exceptions import HttpResponseError

    if not subscription_key:
        subscription_key = os.getenv("AZURE_MAPS_SUBSCRIPTION_KEY")

    if not subscription_key:
        print_error("latlong2timezone(): AZURE_MAPS_SUBSCRIPTION_KEY not found in .env file!")
        return None
    else:
        print_trace(f"latlong2timezone(): AZURE_MAPS_SUBSCRIPTION_KEY={subscription_key}")

    try:
        timezone_client = MapsTimeZoneClient(credential=AzureKeyCredential(subscription_key))
        print_trace(f"latlong2timezone(): client: {timezone_client}")
            #  latlong2timezone(): client: <azure.maps.timezone._patch.MapsTimeZoneClient object at 0x10c892510> 
        return timezone_client
    except Exception as e:
        print_error(f"latlong2timezone(): subscription: {e}")
        return None

def latlong2timezone(timezone_client, lat, long) -> str:
    """Lookup timezone based on geocode latitude and longitude coordinate tuple for subscription_id.

    # per https://learn.microsoft.com/en-us/python/api/overview/azure/maps-timezone-readme?view=azure-python-preview#get-timezone-by-coordinates
    """
    lat_float = float(lat)
    long_float = float(long)
    if lat_float and long_float:
        print_trace(f"latlong2timezone(lat={lat_float} long={long_float})")
    else:
        print_fail(f"latlong2timezone(): lat & long missing!")
        return None
    try:
        json_result = timezone_client.get_timezone_by_coordinates(coordinates=[lat_float, long_float])
            # FIXME: latlong2timezone(): Error Code: 400 BadRequest
        print_trace(f"latlong2timezone(): {json_result}")  # if call works.
        # TimeZones: {'Version': '2025b', 'ReferenceUtcTimestamp': '2025-10-14T03:42:57.8321228Z', 'TimeZones': [{'Id': 'America/Denver', 'Names': {'ISO6391LanguageCode': 'en', 'Generic': 'Mountain Time', 'Standard': 'Mountain Standard Time', 'Daylight': 'Mountain Daylight Time'}, 'ReferenceTime': {'Tag': 'MDT', 'StandardOffset': '-07:00:00', 'DaylightSavings': '01:00:00', 'WallTime': '2025-10-13T21:42:57.8321228-06:00', 'PosixTzValidYear': 2025, 'PosixTz': 'MST+7MDT,M3.2.0,M11.1.0', 'Sunrise': '2025-10-13T07:29:39.1395261-06:00', 'Sunset': '2025-10-13T18:34:35.710823-06:00'}}]} 
        timezone_version = json_result["Version"]
        timezone_abbr = json_result["TimeZones"][0]["ReferenceTime"]["Tag"]
        timezone_offset = json_result["TimeZones"][0]["ReferenceTime"]["StandardOffset"]
        if show_verbose:
            tz = json_result['TimeZones'][0]
            print_verbose(f"latlong2timezone(): Time Zone Information for Latitude={lat_float} Longitude={long_float}:")
            print_verbose(f"   ID:      \"{timezone_abbr}\" = \"{tz['Id']}\" at Version \"{timezone_version}\" ")
            print_verbose(f"   Standard: {tz['Names']['Standard']}")
            print_verbose(f"   Daylight: {tz['Names']['Daylight']}. Offset from GMT/UTC: {timezone_offset} ")
            print_verbose(f"   Time now: {tz['ReferenceTime']['WallTime']} (24-hour time format local time)")
            print_verbose(f"   Sunrise:  {tz['ReferenceTime']['Sunrise']}")
            print_verbose(f"   Sunset:   {tz['ReferenceTime']['Sunset']}")
        return timezone_abbr

    except HttpResponseError as exception:
        if exception.error is not None:
            print_error(f"latlong2timezone(): Error Code: {exception.error.code}")
            print_error(f"latlong2timezone(): Message: {exception.error.message}")
            return None
    except Exception as e:
        print_error(f"latlong2timezone() ERROR: {e}")
        return None


def maps_search_client(subscription_id):
    """Return Azure maps search client for latlong2street().

    https://learn.microsoft.com/en-us/python/api/overview/azure/maps-search-readme?view=azure-python-preview&preserve-view=true
    First create az maps account create --kind "Gen2" --account-name "myMapAccountName" --resource-group "<resource group>" --sku "G2"
    # https://portal.azure.com/#browse/Microsoft.Maps%2Faccounts
    # map-westcentralus-92b065 on Gen2
    # From "View Authentication" section, copy Primary key = your AZURE_MAPS_SUBSCRIPTION_KEY in .env
    """
    # import os
    # from azure.core.credentials import AzureKeyCredential
    # from azure.maps.search import MapsSearchClient

    # Retrieve the Azure Maps subscription key from environment:
    subscription_key = os.getenv("AZURE_MAPS_SUBSCRIPTION_KEY")
    if not subscription_key:
        print_error("maps_search_client(): AZURE_MAPS_SUBSCRIPTION_KEY not found in .env file!")
        return None
    else:
        print_trace(f"maps_search_client(): AZURE_MAPS_SUBSCRIPTION_KEY={subscription_key}")

    try:
        maps_search_client = MapsSearchClient(credential=AzureKeyCredential(subscription_key))
        print_trace(f"maps_search_client(): client: {maps_search_client}")
        return maps_search_client
    except Exception as e:
        print_error(f"maps_search_client() SUBSCRIPTION: {e}")
        return None

def latlong2street(maps_search_client, lat, long) -> str:
    """Reverse geocode latitude and longitude coordinate tuple to street address.

    # per https://learn.microsoft.com/en-us/python/api/overview/azure/maps-search-readme?view=azure-python-preview&preserve-view=true#make-a-reverse-address-search-to-translate-coordinate-location-to-street-address
    Alternative: https://support.google.com/maps/answer/18539?co=GENIE.Platform%3DDesktop&hl=en
    """
    lat_float = float(lat)
    long_float = float(long)
    if lat_float and long_float:
        print_verbose(f"latlong2street(lat={lat_float} long={long_float})")
    else:
        print_fail(f"latlong2street(): lat & long missing!")
        return None, None
    
    try:
        print_trace(f"maps_search_client(): {maps_search_client}")
        json_result = maps_search_client.get_reverse_geocoding(coordinates=[long_float, lat_float])
            # FIXME: latlong2street(): Error Code: InvalidKey Message: The provided key was incorrect or the account resource does not exist. 
        print_trace(f"latlong2street(): {json_result}")
        if json_result.get('features', False):
            props = json_result['features'][0].get('properties', {})
            if props and props.get('address', False):
                street_addr = props['address'].get('formattedAddress', 'No formatted address found!')
                # TODO: print from json:  'confidence': 'High', {'name': 'King County',
                print_info(f"latlong2street((lat={lat_float} long={long_float}): street_addr=\"{street_addr}\"")
                # return street_addr
            else:
                print_error("latlong2street(): Address is None!")
                street_addr = None
        else:
            print_error("latlong2street(): No features available!")
            street_addr = None

        # Get subscription key for timezone client
        maps_subscription_key = os.getenv("AZURE_MAPS_SUBSCRIPTION_KEY")
        if maps_subscription_key:
            timezone_client = MapsTimeZoneClient(credential=AzureKeyCredential(maps_subscription_key))
            timezone_str = timezone_client.get_timezone_by_coordinates(coordinates=[lat_float, long_float])
            print_trace(f"latlong2street(): timezone_str=\"{timezone_str}\" ")
        else:
            print_warning("latlong2street(): AZURE_MAPS_SUBSCRIPTION_KEY not found for timezone lookup")

    except HttpResponseError as exception:
        if exception.error is not None:
            print_error(f"latlong2street(): Error Code: {exception.error.code}")
            print_error(f"latlong2street(): Message: {exception.error.message}")
            return None
    except Exception as e:
        print_error(f"latlong2street() ERROR: {e}")
        return None

    
def street2latlong(subscription_id) -> (str, str):
    """Geocode street address to geo latitude and longitude coordinates.
    
    per https://learn.microsoft.com/en-us/python/api/overview/azure/maps-search-readme?view=azure-python-preview&preserve-view=true#make-a-reverse-address-search-to-translate-coordinate-location-to-street-address
    """
    search_client = maps_search_client(subscription_id)
    if not search_client:
       print("street2latlong(): search_client not created!")
       return (None, None)

    try:

        return latitude, longitude

    except Exception as e:
        print_error(f"street2latlong() ERROR: {e}")
        return (None, None)


# TODO: per https://learn.microsoft.com/en-us/azure/azure-maps/how-to-dev-guide-py-sdk   
# Route	azure-maps-route 	route samples
# Render	azure-maps-render	render sample
# Geolocation	azure-maps-geolocation	geolocation sample



#### SECTION 23. Azure AI Services


def get_ai_svc_globals() -> bool:
    """Load Configuration from environment variables in .env file.

    See https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/01-use-azure-ai-services.html
    Manually follow https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/sdk-client/sdk-client.py
    1. Use the Edge browser to htps://portal.azure.com and sign in using the Microsoft account associated with your Azure subscription.
    2. In the top search bar, search for "Azure AI services" at https://portal.azure.com/#view/Microsoft_Azure_ProjectOxford/CognitiveServicesHub/~/AIServices
    3. Select the blue "Azure AI services multi-service account" at https://portal.azure.com/#create/Microsoft.CognitiveServicesAllInOne to create a new resource:
       1. Subscription: Your Azure subscription
       2. Resource group: Choose or create a resource group (if you are using a restricted subscription, you may not have permission to create a new resource group - use the one provided)
       3. Region: Choose any available region
       4. Name: Enter a unique name (such as "ai-instance-250429a") up to 64 chars with dashes.
       5. Pricing tier: "Standard S0"
       6. Select the required checkboxes 
       7. Click "Create" and "Create" to create the resource for "Your deployment is complete".
       8. Click "Go to resource" then click the "Azure AI services multi-service account" name at
       https://portal.azure.com/#@jetbloom.com/resource/subscriptions/15e19a4e-ca95-4101-8e5f-8b289cbf602b/resourceGroups/westcentralus-42ad1a/providers/Microsoft.CognitiveServices/accounts/ai-instance-250429a/overview
       9. Copy the Endpoint to copy and paste in your .env file:
       AI_SERVICE_ENDPOINT="https://ai-instance-250429a.cognitiveservices.azure.com/"
       10. Click "Click here to manage keys", "Show Keys", "KEY 1" to copy and paste in your .env file:
       AI_SERVICE_KEY="12345..." KEY2 can also be used.
       11. Copy the Location and (for example) paste into AZURE_REGION="centralus"
    """
    global ai_svc_resc
    global ai_endpoint
    global ai_key
    # TODO: ai_svc_name from parms.
    try:
        # Get Configuration Settings:
        load_dotenv()   #from dotenv import load_dotenv

        # TODO: retrieve based on ai_svc_name in

        #import os
        ai_svc_resc = os.getenv('AI_SERVICE_RESOURCE')
        # These are associated with the resource:
        ai_endpoint = os.getenv('AI_SERVICE_ENDPOINT')
        ai_key = os.getenv('AI_SERVICE_KEY')
        print_info(f"get_ai_svc_globals() ai_svc_resc: \"{ai_svc_resc}\" endpoint: \"{ai_endpoint}\" ")
            # CAUTION: Don't display secure ai_key.
        return True

    except Exception as e:
       print_error(f"get_ai_svc_globals() ERROR: {e}")
       return False


def input_az_ai_language() -> str:
    """Return language code.

    See https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/01-use-azure-ai-services.html
    Referencing https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/sdk-client/sdk-client.py
    """
    # TODO: Get language from parameters instead of user input:
    try:
        # Get user input (until they enter "quit")
        user_text =''
        while user_text.lower() != 'quit':
            user_text = input('\nEnter some text ("quit" to stop)\n')
#            if user_text.lower() != 'quit':
#                language = GetLanguage(user_text)
#                print_info(f"input_az_ai_language()() Language: {language}")
#        return language
        return None
    except Exception as e:
        print_error(f"input_az_ai_language() ERROR: {e}")
            # ERROR: name 'GetLanguage' is not defined 
        return None


# Alternative: get_az_ai_textanalytics_rest_client() based on rest-client.py
def get_az_ai_textanalytics_sdk_client() -> object:
    """Create client using global endpoint and key.

    See https://microsoftlearning.github.io/mslearn-ai-services/Instructions/Exercises/01-use-azure-ai-services.html
    Referencing https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/sdk-client/sdk-client.py
    """
    get_ai_svc_globals()  # retrieves ai_endpoint, ai_key, ai_svc_resc
    try:
        #from azure.ai.textanalytics import TextAnalyticsClient
        #from azure.core.credentials import AzureKeyCredential
        credential = AzureKeyCredential(ai_key)
        client = TextAnalyticsClient(endpoint=ai_endpoint, credential=credential)
        print_verbose(f"get_az_ai_textanalytics_sdk_client() client: \"{client}\" ")
        return client
    except Exception as e:
       print_error(f"get_az_ai_textanalytics_sdk_client() ERROR: {e}")
       return None


def detect_language_using_az_ai_sdk_client(ai_svc_name,text_in) -> str:
    """Detect language using Azure AI SDK client.

    Docs:    https://learn.microsoft.com/en-us/azure/ai-services/translator/
    Pricing: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator/
    """
    client = get_az_ai_textanalytics_sdk_client()
    try:
        # Call the service to get the detected language:
        detectedLanguage = client.detect_language(documents = [text_in])[0]   # noqa: N806 
            # Ignoring Ruff err: Variable `detectedLanguage` in function should be lowercase
        print_info(f"detect_language_using_az_ai_sdk_client({len(text_in)} chars) lang: \"{detectedLanguage.primary_language.name}\" " )
        return detectedLanguage.primary_language.name
            # Example: "English"
    except Exception as e:
        print_error(f"detect_language_using_az_ai_sdk_client() ERROR: {e}")
            # ERROR: No connection adapters were found for '/:analyze-text???/language&api-version=2023-04-01' 
        return None


def detect_language_using_az_ai_rest_client( text_in) -> str:
    """Return language name (such as "English") with confidence score using REST API call.

    Docs:    https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Labfiles/01-use-azure-ai-services/Python/rest-client/rest-client.py
    Pricing: https://azure.microsoft.com/en-us/pricing/details/cognitive-services/translator/
    """
    #client = get_az_ai_textanalytics_sdk_client()
    try:
        get_ai_svc_globals()  # retrieves ai_endpoint, ai_key, ai_svc_resc

        # Construct the JSON request body (a collection of documents, each with an ID and text)
        json_body = {
            "documents":[
                {"id": 1,
                 "text": text_in}
            ]
        }  # TODO: target_languages???

        # Let's take a look at the JSON we'll send to the service
        print(json.dumps(json_body, indent=2))

        # Make an HTTP request to the REST interface:
        #import http.client, base64, json, urllib
        #from urllib import request, parse, error        
        uri = ai_endpoint.rstrip('/').replace('https://', '')
        conn = http.client.HTTPSConnection(uri)

        # Add the authentication key to the request header
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': ai_key
        }

        # Use the Text Analytics language API
        conn.request("POST", "/text/analytics/v3.1/languages?", str(json_body).encode('utf-8'), headers)

        # Send the request
        response = conn.getresponse()
        data = response.read().decode("UTF-8")

        # If the call was successful, get the response
        if response.status == 200:
            # Display the JSON response in full (just so we can see it)
            results = json.loads(data)
            print_trace(json.dumps(results, indent=1))
                # Extract the detected language name for each document:
                    #    {
                    #    "documents": [
                    #        {
                    #        "id": "1",
                    #        "warnings": [],
                    #        "detectedLanguage": {
                    #            "name": "English",
                    #            "iso6391Name": "en",
                    #            "confidenceScore": 0.79
            for document in results["documents"]:
                # TODO: Parse language name such as "English" in a list:
                print_info(f"detect_language_using_az_ai_rest_client(): Language: \"{document["detectedLanguage"]["name"]}\" iso6391Name: \"{document["detectedLanguage"]["iso6391Name"]}\" Confidence: \"{document["detectedLanguage"]["confidenceScore"]}\" ")
        else:
            # Something went wrong, write the whole response:
            print_error(f"detect_language_using_az_ai_rest_client() {response.status} ERROR: {data}")

        conn.close()

    except Exception as e:
        print_error(f"detect_language_using_az_ai_rest_client() ERROR: {e}")
        return None


def translate_text_using_az_ai_rest_client(text_in, ai_languages, location_in):
    """Translate text using Azure AI Rest client.

    ai_languages, such as "['fr', 'zu']"
    Based on: https://learn.microsoft.com/en-us/azure/ai-services/translator/text-translation/quickstart/rest-api?tabs=python&source=docs
    """
    #import requests, uuid, json

    # Ocp-Apim-Subscription-Key from KeyVault 
    get_ai_svc_globals()  # retrieves ai_endpoint, ai_key, ai_svc_resc

    # location, also known as region is required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ai_languages
    }
    headers = {
        'Ocp-Apim-Subscription-Key': ai_key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location_in,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': text_in
    }]
    try:
        constructed_url = "https://api.cognitive.microsofttranslator.com/translate"
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        response = request.json()
        print_verbose(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))
        print_info(f"translate_text_using_az_ai_rest_client({len(text_in)} chars) translated to {ai_languages}.")
        return True
    except Exception as e:
        print_error(f"translate_text_using_az_ai_rest_client() ERROR: {e}")
        return False


# https://github.com/MicrosoftLearning/mslearn-ai-services/blob/main/Instructions/Exercises/05-implement-content-safety.md


#### SECTION 23. TODO: Azure VMs (Virtual Machines)



#### SECTION 24. TODO: (Event-triggered) Azure Serverless Functions
# to send messages to Azure services (Blob Storage, Event Hubs, Service Bus)


# Install Azure Functions Core Tools
# After creating a start function using Azure tab in VS Code.
# Set Bindings to Azure resources 
# See https://www.udemy.com/course/python-sdk-for-azure-bootcamp/learn/lecture/39014330#overview

# Service: Functions
#   SKU: Always Ready | Price: 1.6e-05 | Unit: 1 GB Second
#   SKU: Premium | Price: 0.0123 | Unit: 1 GiB Hour



#### SECTION 21. Main control loop:


if __name__ == "__main__":

    # print_env_vars()
    
    # Load environment variables first before trying to get credentials
    still_good = open_env_file()
    if not still_good:
        print_fail("main: Failed to load .env file. Exiting.")
        exit(9)

    my_credential = get_acct_credential()
        # my_credential=<azure.identity._credentials.default.DefaultAzureCredential object at 0x111f11400>
    if not my_credential:
        exit()
    my_subscription_id = get_azure_subscription_id(my_credential)

    lat, long = get_longitude_latitude()
    if lat and long:
        timezone_client = timezone_client()
        my_timezone = latlong2timezone(timezone_client, lat, long)
        # latlong2timezone() TRACE: {'Version': '2025b', 'ReferenceUtcTimestamp': '2025-10-14T03:42:57.8321228Z', 'TimeZones': [{'Id': 'America/Denver', 'Names': {'ISO6391LanguageCode': 'en', 'Generic': 'Mountain Time', 'Standard': 'Mountain Standard Time', 'Daylight': 'Mountain Daylight Time'}, 'ReferenceTime': {'Tag': 'MDT', 'StandardOffset': '-07:00:00', 'DaylightSavings': '01:00:00', 'WallTime': '2025-10-13T21:42:57.8321228-06:00', 'PosixTzValidYear': 2025, 'PosixTz': 'MST+7MDT,M3.2.0,M11.1.0', 'Sunrise': '2025-10-13T07:29:39.1395261-06:00', 'Sunset': '2025-10-13T18:34:35.710823-06:00'}}]} 

        maps_search_client = maps_search_client(my_subscription_id)
        street_addr = latlong2street(maps_search_client, lat, long)
        exit()

    resource_client = resource_object()

    # TODO: When Threema Support responds about secret.
    #recipient_id = "SYKR8UHT"   # Kermit
    #send_theema_msg(recipient_id, phone="", text_to_send="Testing")

    still_good = True

    #### STAGE 1 - Show starting environment:

    print_info(f"Started: {get_user_local_time()}, in logs: {get_log_datetime()} ")
    pgm_strt_mem_used = get_mem_used()
    print_info(f"Started: {pgm_strt_mem_used:.2f} MiB RAM being used.")
    pgm_strt_disk_free = get_disk_free()
    print_info(f"Started: {pgm_strt_disk_free:.2f} GB disk space free.")
    
    #### STAGE 2 - Load environment variables, Azure Account:

    still_good = open_env_file()
    if still_good:
        if show_trace:
            macos_sys_info()

    #### STAGE 3 - Load Azure environment variables, Azure Account:

    if still_good:
        my_credential = get_acct_credential()
            # my_credential=<azure.identity._credentials.default.DefaultAzureCredential object at 0x111f11400>
        my_subscription_id = get_azure_subscription_id(my_credential)
        resource_group_list(my_subscription_id)

        my_user_principal_id = get_user_principal_id(my_credential)
        register_subscription_providers(my_credential, my_subscription_id)
        my_tenant_id = get_tenant_id()
        
        region_choice_basis = "cost"  # "cost" or "distance" or "latency" [Edit Manually]
        az_parms_list()
        if region_choice_basis == "distance":
            longitude, latitude = get_longitude_latitude() # from parms or .env file calling 
            get_geo_coordinates("")  # (zip_code if you have it)
            my_az_svc_region = closest_az_region_by_latlong(longitude, latitude)
                #get_elevation(longitude, latitude)  # has error
        elif region_choice_basis == "cost":
            arm_sku_name_to_find = "Standard_NP20s"  # from https://learn.microsoft.com/en-us/azure/virtual-machines/ ???
            # rc = load_costs_from_api("latest")
            # if rc: my_az_svc_region = get_azure_service_costs(arm_sku_name_to_find)
            my_az_svc_region = get_cheapest_az_region(arm_sku_name_to_find)
        elif region_choice_basis == "latency":
            my_az_svc_region = get_az_region_by_latency()
        else:
            print_fail(f"region_choice_basis: \"{region_choice_basis}\" not recognized.")
            exit(9)
    
        my_resource_group = get_resource_group(my_subscription_id, my_az_svc_region)        

        my_storage_account = get_az_blob_storage_acct_name()
        if not my_storage_account:
            my_storage_account = create_az_blog_storage_acct(None, my_credential, my_subscription_id, my_resource_group, my_az_svc_region)
            if not my_storage_account:
                still_good = False
        if still_good:    
            #ping_az_storage_acct(my_storage_account)
            get_az_region_by_latency(my_storage_account, attempts=5)

        # az_costmanagement(my_subscription_id)
    
    #### STAGE 4 - Azure Resources:

    #resource_group_list()
    #resource_group_list(my_subscription_id)
    #resource_list()
    resource_list(my_subscription_id,my_resource_group)
    exit()

    #### STAGE 4 - Azure Key Vault at a location:

    #if still_good:    
        # get_ai_svc_globals()
        # TEXT_INPUT = "The quick brown fox jumps over the lazy dog."
        # ai_language = detect_language_using_az_ai_sdk_client(TEXT_INPUT)
        #ai_language = detect_language_using_az_ai_rest_client(TEXT_INPUT)

        # CAUTION: This costs money:
        # ai_languages = ["fr"]   # ["fr","zn"] for French & Simplified Chinese
        # "code": 401001 "The request is not authorized because credentials are missing or invalid."
        #translated_text = translate_text_using_az_ai_rest_client(TEXT_INPUT, ai_languages, my_az_svc_region)
        #print_info(f"translated_text: \"{translated_text}\"")

    if still_good:
        if AZURE_KEYVAULT_NAME:
            my_keyvault_name = AZURE_KEYVAULT_NAME
        else:
            my_keyvault_name = define_keyvault_name(my_az_svc_region)
            #my_resource_group = create_get_resource_group(my_credential, my_keyvault_name, my_az_svc_region, my_subscription_id)
            # TODO: Add tags to resource group.
        vault_url = f"https://{my_keyvault_name}.vault.azure.net"
        rc = check_keyvault(my_credential, my_keyvault_name, vault_url)
        if rc is True: 
            print_verbose(f"Key Vault \"{my_keyvault_name}\" already exists.")
        if rc is False:  # False (does not exist), so create it:
            create_keyvault(my_credential, my_subscription_id, my_resource_group, my_keyvault_name, my_az_svc_region, my_tenant_id, my_user_principal_id)

        # List Azure Key Vaults:
        # Equivalent of Portal: List Key Vaults: https://portal.azure.com/#browse/Microsoft.KeyVault%2Fvaults
        # TODO: List costs like https://portal.azure.com/#view/HubsExtension/BrowseCosts.ReactView
        # PRICING: STANDARD SKU: $0.03 per 10,000 app restart operation, plus $3 for cert renewal, PLUS $1/HSM/month.
            # See https://www.perplexity.ai/search/what-is-the-cost-of-running-a-Fr6DTbKQSWKzpdSGv6qyiw
    
        # Add secrets to Azure Key Vault:

        #my_secret_name = os.environ["MY_SECRET_NAME"]
        #my_secret_value = os.environ["MY_SECRET_PLAINTEXT"]

        #rp_result = populate_keyvault_secret(my_credential, my_keyvault_name, my_secret_name, my_secret_value)

        # TODO: List secrets in Key Vault

        # Use KeyVault: https://www.youtube.com/watch?v=VisyAWX533U&pp=ygUcYXp1cmUga2V5IHZhdWx0IHB5dGhvbiBsb2NhbA%3D%3D
            # Get Azure Key Vault Secrets within Python
            # https://www.youtube.com/watch?v=Vs3wyFk9upo&pp=ygUcYXp1cmUga2V5IHZhdWx0IHB5dGhvbiBsb2NhbA%3D%3D
            # https://www.youtube.com/watch?v=FI44MhwklSc&pp=ygUcYXp1cmUga2V5IHZhdWx0IHB5dGhvbiBsb2NhbA%3D%3D

        #rp_result = get_keyvault_secret(my_credential, my_keyvault_name, my_secret_name)
    
        # delete_keyvault_secret(my_credential, my_keyvault_name, my_secret_name)

        # Retrieve secrets from Azure Key Vault:    
        # Rotate secrets in Azure Key Vault:
        # Azure Key Vault allows you to more securely store and manage SSL/TLS certificates.

        #my_principal_id = os.environ["AZURE_KEYVAULT_PRINCIPAL_ID"]


    #### STAGE 5 - Azure AI


    #if still_good:
        # Before: Register an app in Azure and create a client secret.
        #my_app_id = os.environ["AZURE_APP_ID"]
        #my_client_id = os.environ["AZURE_CLIENT_ID"]
        #my_client_secret = os.environ["AZURE_CLIENT_SECRET"]
        #my_principal_id = get_app_principal_id(my_credential, my_app_id, my_tenant_id)
        #if not my_principal_id:
        #    print(f"get_app_principal_id() failed with JSON: \"{my_principal_id}\" ")
        #    exit(9)
        # Alternative: Using Azure Function App Headers (For Authenticated Users) using Easy Auth and returns the signed-in user's principal ID.


    #### STAGE 6 - ABilling and Cost Management:
    
    # https://portal.azure.com/#view/Microsoft_Azure_GTM/Billing.MenuView/~/overview/scopeId/%2Fproviders%2FMicrosoft.Billing%2FbillingAccounts%2F5ba2e1dd-9482-5047-3b24-7e9e94ef26f0%3A065621ab-5bf1-4373-962d-178897041d45_2019-05-31/scope/BillingAccount
    #az_billing(my_credential, my_subscription_id)  # has error
    # Cost Analysis: https://portal.azure.com/#view/Microsoft_Azure_CostManagement/CostAnalysis/scope/%2Fproviders%2FMicrosoft.Billing%2FbillingAccounts%2F5ba2e1dd-9482-5047-3b24-7e9e94ef26f0%3A065621ab-5bf1-4373-962d-178897041d45_2019-05-31/externalState~/%7B%22dateRange%22%3A%22ThisMonth%22%2C%22query%22%3A%7B%22timeframe%22%3A%22None%22%7D%7D
    
    
    #### STAGE 7 - Delete what was created (to stop charge accumulation and cruft):
    
    # -D to delete Key Vault created above.
    if DELETE_KV_AFTER:
        rp_result = delete_keyvault(my_credential, my_keyvault_name, vault_url)

    # -D to delete Resource Group for Key Vault created above.
    if DELETE_RG_AFTER:
        rp_result = delete_resource_group(my_credential, my_keyvault_name, my_subscription_id)



    #    Perplexity.ai: Sonar API 
    # https://docs.perplexity.ai/home
    # https://docs.perplexity.ai/api-reference/chat-completions
    # https://perplexityhackathon.devpost.com/


    #### STAGE 8 - SUMMARY STATISTICS

    show_summary()
    print("DONE")

# END