#!/usr/bin/env bash

# USAGE:
# ./az-info.sh  # with no parameters displays.
# From https://github.com/wilsonmar/azure-quickly/blob/main/az-info.sh

# After you obtain a Terminal (console) in your environment,
# cd to folder, copy this line (without the # first character) and paste in the Terminal:
# sh -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-info.sh)"

# SETUP STEP 01 - Capture starting timestamp and display no matter how it ends:
THIS_PROGRAM="$0"
SCRIPT_VERSION="v0.1.16" # " add PSRule install in az-info.sh"

clear  # screen (but not history)

EPOCH_START="$( date -u +%s )"  # such as 1572634619
LOG_DATETIME=$( date +%Y-%m-%dT%H:%M:%S%z)-$((1 + RANDOM % 1000))

# SETUP STEP 02 - Ensure run variables are based on arguments or defaults ..."
args_prompt() {
   echo "OPTIONS:"
   echo "   -E           to set -e to NOT stop on error"
   echo "   -x           to set -x to trace command lines"
   echo "   -v           to run -verbose (list space use and each image to console)"
   echo "   -vv          to run -very verbose for debugging"
   echo "   -q           -quiet headings for each step"
   echo "   -docs        Pop-up documentation web pages on browser"
   echo " "
   echo "   -I           to install software"
   echo "   -L           to login Azure with an account"
   echo "   -R \"eastus\"  to set specific Region"

#  echo "   -p \"xxx-az-##\" to use [Default] within ~/.az/credentials"
   echo " "
   echo "   -all         to show all sections of info below:"
   echo "   -regions     to show Regions/Locations."

   echo "   -subs        to show Subscriptions & Accounts."
   echo "   -users       to show User info."
   echo " "
   echo "   -groups      to show Resource/Deployment/Lock Groups."
   echo "   -deploys     to show Deployments."
   echo "   -bicep       to show Bicep info."
   echo " "
   echo "   -keyvault    to show Key Vault info."
   echo "   -storage     to show Storage info."
   echo "   -vms         to show Virtual Machine sizes for Region."

   echo "   -netinfo     to show Network info."
#   echo "   -svcinfo     to show Services info with cost history."
#   echo "   -funcs       to show Functions info."
#   echo "   -webapp      to show Web Applications info."
#   echo "   -sql         to show SQL Server database info."
    echo "   -sentinel    to show Sentinel logs/alerts."

#   echo " "
#CosmosDB	az cosmosdb
#Storage accounts	az storage account

#   echo "   -amiinfo     to show AMI info."
#   echo "   -computeinfo     to show compute info."
#   echo " "
#   echo "   -s3info      to show S3 info."
#   echo "   -diskinfo    to show Disk info."
#   echo "   -dbinfo      to show Database info."
#   echo "   -certinfo    to show Certificates info."
#   echo "   -loginfo     to show Logging info."
   echo " "
   echo "USAGE EXAMPLE:"
   echo "./az-info.sh -v -subs "
 }
if [ $# -eq 0 ]; then  # display if no parameters are provided:
   args_prompt
   exit 1
fi
exit_abnormal() {            # Function: Exit with error.
  echo "exiting abnormally"
  #args_prompt
  exit 1
}

# SETUP STEP 03 - Set Defaults (default true so flag turns it true):
   SET_EXIT=true                # -E
   RUN_QUIET=false              # -q
   SET_TRACE=false              # -x
   RUN_VERBOSE=false            # -v
   RUN_DEBUG=false              # -vv
   UPDATE_PKGS=false            # -U
   DOWNLOAD_INSTALL=false       # -I
   LOGIN=false                  # -L
   AZ_PROFILE="default"         # -p
   AZ_REGION_IN=""              # -R region

   ALL_INFO=false               # -all
   REGIONS=false                # -regions
   USER_INFO=false              # -userinfo
   DOCS_INFO=false              # -docs
   KEYVAULT_INFO=false          # -keyvault
   STORAGE_INFO=false           # -storage
   GROUPS_INFO=false            # -groups
   DEPLOY_INFO=false            # -deploys
   BICEP_INFO=false             # -bicep
   VMS_INFO=false               # -vms

   NET_INFO=false               # -netinfo
   LAMBDA_INFO=false            # -funcs
   AMI_INFO=false               # -amiinfo
   SUBS_INFO=false              # -subs
   S3_INFO=false                # -s3info
   DISK_INFO=false              # -diskinfo
   CERT_INFO=false              # -diskinfo
   LOG_INFO=false               # -loginfo
   SENTINEL_INFO=false          # -sentinel

   MY_AMI_TYPE="Amazon Linux 2"
   MY_AMI_CONTAINS=".NET Core 2.1"

# SETUP STEP 04 - Read parameters specified:
while test $# -gt 0; do
  case "$1" in
    -all)
      export ALL_INFO=true
      shift
      ;;
    -amiinfo)
      export AMI_INFO=true
      shift
      ;;
    -bicep)
      export BICEP_INFO=true
      shift
      ;;
    -certinfo)
      export CERT_INFO=true
      shift
      ;;
    -deploys)
      export DEPLOY_INFO=true
      shift
      ;;
    -diskinfo)
      export DISK_INFO=true
      shift
      ;;
    -docs)
      export DOCS_INFO=true
      shift
      ;;
    -groups)
      export GROUPS_INFO=true
      shift
      ;;
    -keyvault)
      export KEYVAULT_INFO=true
      shift
      ;;
    -E)
      export SET_EXIT=false
      shift
      ;;
    -funcs)
      export LAMBDA_INFO=true
      shift
      ;;
    -q)
      export RUN_QUIET=true
      shift
      ;;
    -I)
      export DOWNLOAD_INSTALL=true
      shift
      ;;
    -L)
      export LOGIN=true
      shift
      ;;
    -loginfo)
      export LOG_INFO=true
      shift
      ;;
    -netinfo)
      export NET_INFO=true
      shift
      ;;
    -regions)
      export REGIONS=true
      shift
      ;;
    -R*)
      shift
             AZ_REGION_IN=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export AZ_REGION_IN
      shift
      ;;
    -sentinel)
      export SENTINEL_INFO=true
      shift
      ;;
    -storage)
      export STORAGE_INFO=true
      shift
      ;;
    -subs)
      export SUBS_INFO=true
      shift
      ;;
    -svcinfo)
      export SVC_INFO=true
      shift
      ;;
    -users)
      export USER_INFO=true
      shift
      ;;
    -U)
      export UPDATE_PKGS=true
      shift
      ;;
    -v)
      export RUN_VERBOSE=true
      shift
      ;;
    -vms)
      export VMS_INFO=true
      shift
      ;;
    -vv)
      export RUN_DEBUG=true
      shift
      ;;
    -p*)
      shift
             AZ_PROFILE=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export AZ_PROFILE
      shift
      ;;
    -x)
      export SET_TRACE=true
      shift
      ;;
    *)
      error "Parameter \"$1\" not recognized. Aborting."
      exit 0
      break
      ;;
  esac
done


# SETUP STEP 04 - Set ANSI color variables (based on AZ_code_deploy.sh): 
bold="\e[1m"
dim="\e[2m"
# shellcheck disable=SC2034 # ... appears unused. Verify use (or export if used externally).
underline="\e[4m"
# shellcheck disable=SC2034 # ... appears unused. Verify use (or export if used externally).
blink="\e[5m"
reset="\e[0m"
red="\e[31m"
green="\e[32m"
# shellcheck disable=SC2034 # ... appears unused. Verify use (or export if used externally).
blue="\e[34m"
cyan="\e[36m"

# SETUP STEP 05 - Specify alternate echo commands:
h2() { if [ "${RUN_QUIET}" = false ]; then    # heading
   printf "\n${bold}\e[33m\u2665 %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
   fi
}
info() {   # output on every run
   printf "${dim}\n➜ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
note() { if [ "${RUN_VERBOSE}" = true ]; then
   printf "\n${bold}${cyan} ${reset} ${cyan}%s${reset}" "$(echo "$@" | sed '/./,$!d')"
   printf "\n"
   fi
}
debug_echo() { if [ "${RUN_DEBUG}" = true ]; then
   printf "\n${bold}${cyan} ${reset} ${cyan}%s${reset}" "$(echo "$@" | sed '/./,$!d')"
   printf "\n"
   fi
}
success() {
   printf "\n${green}✔ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
error() {    # &#9747;
   printf "\n${red}${bold}✖ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
warning() {  # &#9758; or &#9755;
   printf "\n${cyan}☞ %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
fatal() {   # Skull: &#9760;  # Star: &starf; &#9733; U+02606  # Toxic: &#9762;
   printf "\n${red}☢  %s${reset}\n" "$(echo "$@" | sed '/./,$!d')"
}
divider() {
  printf "\r\033[0;1m========================================================================\033[0m\n"
}

pause_for_confirmation() {
  read -rsp $'Press any key to continue (ctrl-c to quit):\n' -n1 key
}

# SETUP STEP 06 - Check what operating system is in use:
   OS_TYPE="$( uname )"
   OS_DETAILS=""  # default blank.
if [ "$(uname)" == "Darwin" ]; then  # it's on a Mac:
      OS_TYPE="macOS"
      PACKAGE_MANAGER="brew"
elif [ "$(uname)" == "Linux" ]; then  # it's on a Mac:
   if command -v lsb_release ; then
      lsb_release -a
      OS_TYPE="Ubuntu"
      # TODO: OS_TYPE="WSL" ???
      PACKAGE_MANAGER="apt-get"

      # TODO: sudo dnf install pipenv  # for Fedora 28

      silent-apt-get-install(){  # see https://wilsonmar.github.io/bash-scripts/#silent-apt-get-install
         if [ "${RUN_VERBOSE}" = true ]; then
            info "apt-get install $1 ... "
            sudo apt-get install "$1"
         else
            sudo DEBIAN_FRONTEND=noninteractive apt-get install -qq "$1" < /dev/null > /dev/null
         fi
      }
   elif [ -f "/etc/os-release" ]; then
      OS_DETAILS=$( cat "/etc/os-release" )  # ID_LIKE="rhel fedora"
      OS_TYPE="Fedora"
      PACKAGE_MANAGER="yum"
   elif [ -f "/etc/redhat-release" ]; then
      OS_DETAILS=$( cat "/etc/redhat-release" )
      OS_TYPE="RedHat"
      PACKAGE_MANAGER="yum"
   elif [ -f "/etc/centos-release" ]; then
      OS_TYPE="CentOS"
      PACKAGE_MANAGER="yum"
   else
      error "Linux distribution not anticipated. Please update script. Aborting."
      exit 0
   fi
else 
   error "Operating system not anticipated. Please update script. Aborting."
   exit 0
fi
# note "OS_DETAILS=$OS_DETAILS"

# SETUP STEP 07 - Define utility functions, such as bash function to kill process by name:
ps_kill(){  # $1=process name
      PSID=$(ps aux | grep $1 | awk '{print $2}')
      if [ -z "$PSID" ]; then
         h2 "Kill $1 PSID= $PSID ..."
         kill 2 "$PSID"
         sleep 2
      fi
}

# SETUP STEP 08 - Adjust Bash version:
BASH_VERSION=$( bash --version | grep bash | cut -d' ' -f4 | head -c 1 )
   if [ "${BASH_VERSION}" -ge "4" ]; then  # use array feature in BASH v4+ :
      DISK_PCT_FREE=$(read -d '' -ra df_arr < <(LC_ALL=C df -P /); echo "${df_arr[11]}" )
      FREE_DISKBLOCKS_START=$(read -d '' -ra df_arr < <(LC_ALL=C df -P /); echo "${df_arr[10]}" )
   else
      if [ "${UPDATE_PKGS}" = true ]; then
         info "Bash version ${BASH_VERSION} too old. Upgrading to latest ..."
         if [ "${PACKAGE_MANAGER}" == "brew" ]; then
            brew install bash
         elif [ "${PACKAGE_MANAGER}" == "apt-get" ]; then
            silent-apt-get-install "bash"
         elif [ "${PACKAGE_MANAGER}" == "yum" ]; then    # For Redhat distro:
            sudo yum install bash      # please test
         elif [ "${PACKAGE_MANAGER}" == "zypper" ]; then   # for [open]SuSE:
            sudo zypper install bash   # please test
         fi
         info "Now at $( bash --version  | grep 'bash' )"
         fatal "Now please run this script again now that Bash is up to date. Exiting ..."
         exit 0
      else   # carry on with old bash:
         DISK_PCT_FREE="0"
         FREE_DISKBLOCKS_START="0"
      fi
   fi

# SETUP STEP 09 - Handle run endings:"

# In case of interrupt control+C confirm to exit gracefully:
#interrupt_count=0
#interrupt_handler() {
#  ((interrupt_count += 1))
#  echo ""
#  if [[ $interrupt_count -eq 1 ]]; then
#    fail "Really quit? Hit ctrl-c again to confirm."
#  else
#    echo "Goodbye!"
#    exit
#  fi
#}

trap interrupt_handler SIGINT SIGTERM
trap this_ending EXIT
trap this_ending INT QUIT TERM
this_ending() {
   EPOCH_END=$(date -u +%s);
   EPOCH_DIFF=$((EPOCH_END-EPOCH_START))
   # Using BASH_VERSION identified above:
   if [ "${BASH_VERSION}" -lt "4" ]; then
      FREE_DISKBLOCKS_END="0"
   else
      FREE_DISKBLOCKS_END=$(read -d '' -ra df_arr < <(LC_ALL=C df -P /); echo "${df_arr[10]}" )
   fi
   FREE_DIFF=$(((FREE_DISKBLOCKS_END-FREE_DISKBLOCKS_START)))
   MSG="End of script $SCRIPT_VERSION after $((EPOCH_DIFF/360)) seconds."  # and $((FREE_DIFF*512)) bytes on disk."
   # echo 'Elapsed HH:MM:SS: ' $( awk -v t=$beg-seconds 'BEGIN{t=int(t*1000); printf "%d:%02d:%02d\n", t/3600000, t/60000%60, t/1000%60}' )
   success "$MSG"
   # note "Disk $FREE_DISKBLOCKS_START to $FREE_DISKBLOCKS_END"
}
sig_cleanup() {
    trap '' EXIT  # some shells call EXIT after the INT handler.
    false # sets $?
    this_ending
}

#################### Print run heading:

if [ "${RUN_VERBOSE}" = true ]; then   # -v
    echo "  $THIS_PROGRAM $SCRIPT_VERSION ============== $LOG_DATETIME "
fi

# SETUP STEP 09 - Operating environment information:
HOSTNAME=$( hostname )
PUBLIC_IP=$( curl -s ifconfig.me )

if [ "$OS_TYPE" == "macOS" ]; then  # it's on a Mac:
   debug_echo "BASHFILE=~/.bash_profile ..."
   BASHFILE="$HOME/.bash_profile"  # on Macs
else
   debug_echo "BASHFILE=~/.bashrc ..."
   BASHFILE="$HOME/.bashrc"  # on Linux
fi
   debug_echo "Running $0 in $PWD"  # $0 = script being run in Present Wording Directory.
   debug_echo "OS_TYPE=$OS_TYPE using $PACKAGE_MANAGER from $DISK_PCT_FREE disk free"
   debug_echo "on hostname=$HOSTNAME at PUBLIC_IP=$PUBLIC_IP."
   debug_echo " "

# print all command arguments submitted:
#while (( "$#" )); do 
#  echo $1 
#  shift 
#done 


# SETUP STEP 10 - Define run error handling:

EXIT_CODE=0
if [ "${SET_EXIT}" = true ]; then  # don't
   debug_echo "Set -e (no -E parameter  )..."
   set -e  # exits script when a command fails
   # set -eu pipefail  # pipefail counts as a parameter
else
   warning "Don't set -e (-E parameter)..."
fi
if [ "${SET_XTRACE}" = true ]; then
   debug_echo "Set -x ..."
   set -x  # (-o xtrace) to show commands for specific issues.
fi
# set -o nounset


# SETUP STEP 11 - Install/Upgrade Azure CLI, Bicep, Extensions:

if [ "${DOWNLOAD_INSTALL}" = true ]; then  # -I
    # Release notes: https://docs.microsoft.com/cli/azure/release-notes-azure-cli
    brew install azure-cli  # Now updates if already installed
        # The above installs a bunch of packages (ansible, openssl, python, readline, sqlite, xz, zlib, etc.)
    az version
        # az upgrade results in fatal: couldn't find remote ref refs/heads/master

    # https://medium.com/@woeterman_94/how-to-install-azure-bicep-on-your-computer-d84f8aa7988a
    # https://azure.github.io/PSRule.Rules.Azure/setup/setup-bicep/
    az bicep install
    az bicep version

    az bicep upgrade
    az bicep version
    # https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/azure-resource-manager/bicep/bicep-cli.md

    # To allow installing extensions in CLI without prompting for confirmation: 
    az config set extension.use_dynamic_install=yes_without_prompt

    # https://azure.github.io/PSRule.Rules.Azure/  # Rules module for testing ARM & Bicep files.
    # https://github.com/Azure/PSRule.Rules.Azure/ by Bernie White
    # In .github/workflows/analyze-arm.yaml
        # https://www.youtube.com/watch?v=L4CIDqnXLPk 
        # https://www.youtube.com/watch?v=zdoB80PlN0Y getting started in GitHub Actions
        # https://www.youtube.com/watch?v=3697rG8tkOI&list=PLM4Db0UWu45Kv-QMpyEv9znqA2t0Xlcvk&index=2
    # Outputs in SARIF format or to an Azure Monitor Log Analytics workspace for analysis by Power BI.

    # Install VSCode add-ons:
    # https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/install
    # https://marketplace.visualstudio.com/items?itemName=bewhite.psrule-vscode

    # .workflows folder for GitHub Actions ?

fi


# SETUP STEP 12 - Set Azure environment variables defaults:

# TODO: Read from env file.

if [ -z "$AZ_REGION_IN" ]; then  # NOT specified
   AZ_REGION="eastus"
   warning "-Region \"$AZ_REGION\" by hard-coded default..."
fi

##############################################################################

if [ "${DOCS_INFO}" = true ]; then  # -docs
    echo "Opening web browser for get-started-with-azure-cli ..."
    open https://learn.microsoft.com/en-us/cli/azure/get-started-with-azure-cli
    # https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli?view=azure-cli-latest
    # https://github.com/Azure/azure-cli
fi # DOCS_INFO

if [ "${DOWNLOAD_INSTALL}" = true ]; then   # -I
    h2 "============= -I = Install:"

    echo "az bicep upgrade ..."
    # https://docs.microsoft.com/cli/azure/install-azure-cli
    az bicep upgrade

fi  # DOWNLOAD_INSTALL

##############################################################################

if [ "${LOGIN}" = true ]; then   # -L
    az login
        # A web browser has been opened at ...
fi

##############################################################################

if [ "${REGIONS}" = true ] || [ "${ALL_INFO}" = true ]; then   # -regions
    if [ "${RUN_VERBOSE}" = true ]; then   # -v
      RESPONSE=$( az account list-locations --output table | wc -l | tr -d '[:space:]' )
      h2 "============= -regions [$RESPONSE SORTED by Region]"
      az account list-locations --output table \
         --query "sort_by([].{DisplayName:displayName, Name:name, Region:regionalDisplayName}, &Name)" 
         # DisplayName  Name  RegionalDisplayName
    fi

    # TODO: echo "Regions in Southern Hemisphere (Longitude < 0):"
    #rgArray=($( az account list-locations list --output tsv --query "[?metadata:Longitude < 0].metadata:Longitude"))
    #echo ${rgArray[0]}
    #echo ${rgArray[*]}
fi


if [ "${SUBS_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -subs
    h2 "============= -subs = Subscriptions: [WIDE SCREEN]"

    if [ "${RUN_DEBUG}" = true ]; then   # -vv
        az account list --output table --all
    else
        az account list --output table
           # Name  CloudName  SubscriptionId  TenantId  State  IsDefault
    fi

    echo -e "/n"  # blank line
    az account show --output table
       # EnvironmentName  HomeTenantId  IsDefault  Name  State  TenantId

    # https://learn.microsoft.com/en-us/cli/azure/use-cli-effectively?tabs=bash%2Cbash2

fi # SUBS_INFO


if [ "${USER_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -users
    h2 "============= az ad user list"
    # if --id $AZ_USER
    # https://learn.microsoft.com/en-us/cli/azure/ad/user?view=azure-cli-latest
    if [ "${RUN_VERBOSE}" = true ]; then   # -I
        az ad user list --output json
        # DisplayName    GivenName    Surname    UserPrincipalName
        # [--display-name]
        # [--filter]
        # [--upn]
    else
        az ad user list --output table
    fi
    retVal=$?
    if [ $retVal -ne 0 ]; then
    exit -1 
    fi

    # https://docs.microsoft.com/en-us/cli/azure/ad/user?view=azure-cli-latest#az-ad-user-show
    # https://learn.microsoft.com/en-us/cli/azure/devops/user?view=azure-cli-latest
    # https://learn.microsoft.com/en-us/cli/azure/ad/signed-in-user?view=azure-cli-latest

    # https://vinijmoura.medium.com/how-to-list-all-users-and-group-permissions-on-azure-devops-using-azure-devops-cli-54f73a20a4c7
    # https://github.com/vinijmoura/Azure-DevOps/tree/master/PowerShell/ListUserAndPermissions

    # List role assignments for each user:
    # https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-list-cli
    # az role assignment list --all --assignee patlong@contoso.com --output json --query '[].{principalName:principalName, roleDefinitionName:roleDefinitionName, scope:scope}'

fi  # "${USER_INFO}"


if [ "${GROUPS_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -groups
   h2 "============= -groups = Resources/Deployments/Locks: [WIDE SCREEN]"
   # https://learn.microsoft.com/en-us/cli/azure/group?view=azure-cli-latest

   az group list --output table

   #note "Group lock list:"
   #az group lock list --output table
fi


if [ "${DEPLOYS_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -deploys
   h2 "============= -deploys = Deployments: [WIDE SCREEN]"
   az deployment sub list --output table
fi


if [ "${BICEP_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -bicep
    # https://learn.microsoft.com/en-us/cli/azure/bicep?view=azure-cli-latest
    h2 "============= -bicep"
    az bicep version

    if [ "${RUN_VERBOSE}" = true ]; then   # -v
      echo "All available versions of Bicep CLI app:"
      az bicep list-versions --output json
    fi

    if [ "${RUN_DEBUG}" = true ]; then   # -vv
        az bicep -h
    fi
fi


if [ "${KEYVAULT_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -keyvault
   h2 "============= -keyvault"
   # https://learn.microsoft.com/en-us/cli/azure/keyvault?view=azure-cli-latest

   echo "First provide --vault-name or --hsm-name"
   # az keyvault key list --output table 
fi


if [ "${STORAGE_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -storage
    h2 "============= -storage = Storage: [WIDE SCREEN]"
    # https://learn.microsoft.com/en-us/cli/azure/storage/account?view=azure-cli-latest

    echo "List storage accounts:"
    # az storage account list --output table | jq -r '.[] | "\(.Name) \(.PrimaryLocation)"'
    az storage account list --output table
        # AccessTier  AllowBlobPublicAccess  CreationTime  EnableHttpsTrafficOnly  Kind       
        # Location  MinimumTlsVersion  Name  PrimaryLocation ProvisioningState 
        # ResourceGroup  StatusOfPrimary

    #echo "List storage account keys:"
    #az storage account keys list --output table

    #echo "List encryption scopes within storage account:"
    #az storage account encryption-scope list --output table

    # List network rules:
    # az storage account network-rule list

    # List Object Replication Service Policies associated with the specified storage account.
    # az storage account or-policy list	

    # List all the rules in the specified Object Replication Service Policy.
    # az storage account or-policy rule list	

    # Get the private link resources that need to be created for a storage account.
    # az storage account private-link-resource list	

    # List all CORS rules of a storage account's blob service properties.
    # az storage account blob-service-properties cors-rule list	

fi


if [ "${VMS_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -vms
    # https://learn.microsoft.com/en-us/cli/azure/service-page/virtual%20machines?view=azure-cli-latest
    h2 "============= -vms = Virtual Machines :"
    # From https://www.azurecitadel.com/cli/scripting/
    ids=$( az vm list --show-details --query "[?tags.environment != 'production' && powerState == 'VM running'].id" --output tsv)
    if [ -n "$PSID" ]; then  # found:
       echo "VMs: $ids" 
       # az vm stop --ids $ids
    fi

    if [ "${RUN_DEBUG}" = true ]; then   # -vv
       echo "az vm list-sizes -l $AZ_REGION --output table"
       az vm list-sizes -l $AZ_REGION --output table
       az vm list-sizes -l $AZ_REGION --output table | wc -l
    fi

fi


if [ "${NET_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -netinfo
    # https://learn.microsoft.com/en-us/cli/azure/network/vnet?view=azure-cli-latest
    h2 "============= -netinfo "

    echo "List virtual networks (vnets):"
    az network vnet list --output table

    note "List peerings:"
    # az network vnet peering list --output table --resource-group $AZ_RESOURCE_GROUP --vnet-name $AZ_VNET_NAME

    note "List subnets in a virtual network:"
    # az network vnet subnet list --output table  --resource-group $AZ_RESOURCE_GROUP --vnet-name $AZ_VNET_NAME

    note "List network vnet tap list: using extension virtual-network-tap :"
    az network vnet tap list --output table

    # TODO: Use JMESPATH https://www.azurecitadel.com/cli/scripting/
fi



if [ "${SENTINEL_INFO}" = true ] || [ "${ALL_INFO}" = true ]; then   # -sentinel
    # https://learn.microsoft.com/en-us/cli/azure/sentinel?view=azure-cli-latest
    h2 "============= -sentinel (SIEM/SOAR):"

   if [ -n "$RESC_GROUP" ]; then  # value found:
   # -w/--workspace-name $WORKSPACE
      echo "Sentinel settings for Resource Group $RESC_GROUP & Workspace:"  # requires the extension sentinel
      az sentinel setting list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

      echo "Security ML Analytics Settings:"
      az sentinel analytics-setting list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

      echo "Get all alert rules:"
      az sentinel alert-rule list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

      echo "Get all alert rule templates:"
      az sentinel alert-rule template list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

      echo "Automation rules:"
      az sentinel automation-rule list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

      echo "Sentinel bookmarks:"
      az sentinel bookmark list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        az sentinel bookmark relation list --resource-group $RESC_GROUP --workspace-name $WORKSPACE
        echo "bookmark relations:"

        echo "Data connectors:"
        az sentinel data-connector list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Entity query templates:"
        az sentinel entity-query template list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Entity queries:"
        az sentinel entity-query list	


        echo "Incident comments:"
        az sentinel incident comment list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Incidents:"
        az sentinel incident list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Incident alerts:"
        az sentinel incident list-alert --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Incident bookmarks:"
        az sentinel incident list-bookmark --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Incident related entities:"
        az sentinel incident list-entity --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Incident relations:"
        az sentinel incident relation list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Sentinel metadata:"
        az sentinel metadata list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "office365 consents:"
        az sentinel office-consent list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Sentinel onboarding states:"
        az sentinel onboarding-state list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "source controls, without source control items:"
        az sentinel source-control list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "repositories metadata:"
        az sentinel source-control list-repository --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "threat intelligence indicators:"
        az sentinel threat-indicator list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "Manage watchlist with sentinel:"
        az sentinel watchlist --resource-group $RESC_GROUP --workspace-name $WORKSPACE

        echo "watchlists, without watchlist items:"
        az sentinel watchlist list --resource-group $RESC_GROUP --workspace-name $WORKSPACE

      if [ -n "$RULE_NAME" ]; then  # value found:
         echo "Get all actions of alert rule:"
         az sentinel alert-rule action list --resource-group $RESC_GROUP --workspace-name $WORKSPACE \
            --rule-name $RULE_NAME
      fi

   fi

fi

# END