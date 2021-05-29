#!/bin/bash

# az-helm-cli.sh
# This script contains all that's needed to, from a MacOS laptop, establish Docker, ACR, etc. to
# run a Helm v3 chart 
# which create resources in Azure to:
# ???
# Based on # https://docs.microsoft.com/en-us/azure/container-registry/container-registry-oci-artifacts
# A. Before invoking this script: Define environment variables 
#       MY_GIT_CONTAINER, MY_REPO, MY_LOC, MY_RG, MY_ACR, --username $SP_APP_ID --password $SP_PASSWD, MY_ACR_REPO
#       MY_SCRIPT
# B. To invoke this script: Navigate/create container folder and download this repo into it
#       After you obtain a Terminal (console) in your environment,
#       cd to folder, copy this line and paste in the terminal:
#
#       bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilson-mar/$MY_REPO/master/$MY_SCRIPT)" 
##
# Authenticate with your registry using the helm registry login command.
# Use helm chart commands in the Helm CLI to push, pull, and manage Helm charts in a registry
# Use helm install to install charts to a Kubernetes cluster from a local repository cache.
#
# Adapted from https://docs.microsoft.com/en-us/azure/container-registry/container-registry-helm-repos
# and https://gaunacode.com/publishing-helm-3-charts-to-azure-container-registry-using-azure-devops-part-1

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi


###  01. Establish starting times of this run:
THIS_PROGRAM="$0"
EPOCH_START="$( date -u +%s )"  # such as 1572634619
LOG_DATETIME=$( date +%Y-%m-%dT%H:%M:%S%z)-$((1 + RANDOM % 1000))   # EX: 2021-04-20T10:16:02+0000-296
echo "=============== $LOG_DATETIME $THIS_PROGRAM $MY_SCRIPT $MY_SCRIPT_VERSION at $PWD"


###  02. Define a menu and display it if -h is specified in the command line:
EMAIL_HOST="gmail.com"
args_prompt() {
   echo "OPTIONS:"
   echo "   -h           -help (this menu)"
   echo "   -E            continue (NOT stop) on error"
   echo "   -v            run -verbose (list space use and each image to console)"
   echo "   -vv           run -very verbose (debug)"
   echo "   -q           -quiet headings for each step"
   echo " "
   echo "   -I           -Install packages (default is not)"
   echo "   -U           -Upgrade installed packages"
   echo " "
   echo "   -S  \"~/.secrets.sh\"  -Secrets full file path to local user home folder"
   echo "   -vra         -vault revoke (logout) before login"
   echo "   -V  \"vault.${EMAIL_HOST}:8200\" (override default VAULT_ADDR)"
   echo "   -e  \"john_doe@${EMAIL_HOST}\" -email for github (gen'd from os user)"
   echo "   -ve \"suresh_kumar-ggn@external.${EMAIL_HOST}\" -vault email (not gen'd from macOS user)"
   echo "   -n  \"john-doe\" GitHub.com user accou-nt"
   echo "   -fn \"John Doe\"  user full name (based on GitHub user name"
   echo " "
#  echo "   -p   \"clouddrive\" = folder holding repos (the org name)"
   echo "   -org \"Internal\" (default, case sensitive for Vault)"
   echo "   -ou           (like org-12345678)"
   echo "   -o           -open/view web page in default browser"
   echo " "
   echo "   -c           -clone from GitHub"
   echo "   -d           -delete repo before clone (on purpose)"
   echo "   -O \"repo1\" repo name (defaults based on -org)"
   echo "   -C    remove -Cloned files after run (to save disk space)"
   echo "   -xx       stop and not exit at end"
#   echo "WINDOWS EXAMPLE INVOCATION:"
#   echo "sh $MY_SCRIPT -n \"wilson-mar\" -e \"wilson_mar@${EMAIL_HOST}\" -os \"Windows\" -v"  
   echo "MAC EXAMPLE INVOCATION:"
   echo "./$MY_SCRIPT "
}

if [ $# -eq 0 ]; then  # display if no parameters are provided:
   args_prompt
#   exit 1      # and stop processing.
fi


###  03. Define TOGGLE variables for use as "feature flags":
   CLONE_GITHUB=false           # -c
   INSTALL_PKGS_TOGGLE=false    # -I
   GITHUB_USER_EMAIL_PARM=""    # -e
   GITHUB_ACCOUNT=""            # -n
   GITHUB_ORG=""                # -org
   GITHUB_ORG_USER=""           # -ou
   GITHUB_REPO=""               # -O
   USER_FULL_NAME=""            # -fn
   OPEN_APP=false               # -o
   LOCAL_SSH_KEYFILE=""         # -p
   DELETE_BEFORE=false          # -d
   PAUSE_AT_END=""              # -xx
   REMOVE_GITHUB_AFTER=false    # -R
   RUN_VERBOSE=false            # -v  for true or false
   RUN_DEBUG=false              # -vv  (very verbose)
   RUN_QUIET=false              # -q
   MY_FOLDER=""                 # -F folder
   OS_UNAME=""                  # -os
   SECRETS_FILEPATH=""          # -S
   UPDATE_PKGS=false            # -U
   USE_SECRETS_FILE=false       # -s
   VAULT_HOST=""                # -V
   VAULT_USERNAME_PARM=""       # -ve
   VAULT_REVOKE_ACCT=false      # -vra

###  04. Set variables associated with each parameter flag:
while test $# -gt 0; do
  case "$1" in
    -c)
      export CLONE_GITHUB=true
      shift
      ;;
    -C)
      export REMOVE_GITHUB_AFTER=true
      shift
      ;;
    -d)
      export DELETE_BEFORE=true
      shift
      ;;
    -e*)
      shift
             GITHUB_USER_EMAIL_PARM=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export GITHUB_USER_EMAIL_PARM
      shift
      ;;
    -E)
      export CONTINUE_ON_ERR=true
      shift
      ;;
    -fn*)
      shift
             USER_FULL_NAME=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export USER_FULL_NAME
      shift
      ;;
    -F*)
      shift
      MY_FOLDER=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      shift
      ;;
     -h)
      args_prompt
      exit 0
      break
      ;;
    -I)
      export DOWNLOAD_INSTALL=true
      shift
      ;;
    -n*)
      shift
             GITHUB_ACCOUNT=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export GITHUB_ACCOUNT
      shift
      ;;
    -org*)
      shift
             GITHUB_ORG=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export GITHUB_ORG
      shift
      ;;
    -os*)
      shift
             OS_UNAME=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export OS_UNAME
      shift
      ;;
    -ou*)
      shift
             GITHUB_ORG_USER=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export GITHUB_ORG_USER
      shift
      ;;
    -o)
      export OPEN_APP=true
      shift
      ;;
    -O*)
      shift
             GITHUB_REPO=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export GITHUB_REPO
      shift
      ;;
    -p*)
      shift
             LOCAL_SSH_KEYFILE=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export LOCAL_SSH_KEYFILE
      shift
      ;;
    -q)
      export RUN_QUIET=true
      shift
      ;;
    -s)
      export USE_SECRETS_FILE=true
      shift
      ;;
    -xx)
      export PAUSE_AT_END=true
      shift
      ;;
    -U)
      export UPDATE_PKGS=true
      shift
      ;;
    -vra)
      export VAULT_REVOKE_ACCT=true
      shift
      ;;
    -ve*)
      shift
             VAULT_USERNAME_PARM=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export VAULT_USERNAME_PARM
      shift
      ;;
    -v)
      export RUN_VERBOSE=true
      shift
      ;;
    -vv)
      export RUN_DEBUG=true
      shift
      ;;
    -V*)
      shift
             VAULT_HOST=$( echo "$1" | sed -e 's/^[^=]*=//g' )
      export VAULT_HOST
      shift
      ;;
    *)
      error "Parameter \"$1\" not recognized. Aborting."
      exit 0
      break
      ;;
  esac
done


###  05. Set custom functions to echo text to screen:

# \e ANSI color variables are defined in https://wilsonmar.github.io/bash-scripts#TextColors
h2() { if [ "${RUN_QUIET}" = false ]; then    # heading
   printf "\n\e[1m\e[33m\u2665 %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
   fi
}
info() {   # output on every run
   printf "\e[2m\n➜ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
note() { if [ "${RUN_VERBOSE}" = true ]; then
   printf "\n\e[1m\e[36m \e[0m \e[36m%s\e[0m" "$(echo "$@" | sed '/./,$!d')"
   printf "\n"
   fi
}
success() {
   printf "\n\e[32m\e[1m✔ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
error() {    # &#9747;
   printf "\n\e[31m\e[1m✖ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
warning() {  # &#9758; or &#9755;
   printf "\n\e[5m\e[36m\e[1m☞ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
fatal_msg() {   # Skull: &#9760;  # Star: &starf; &#9733; U+02606  # Toxic: &#9762;
   printf "\n\e[31m\e[1m☢  %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}


###  06. Edit and set run error control:

exit_abnormal() {            # Function: Exit with error.
  echo "exiting abnormally"
  #args_prompt
  echo "Deleting Azure Resource Group "${MY_RG}" to stop charges ..."
  az group delete --name "${MY_RG}" --yes   # takes several minutes
  exit 1
}

if [ "${CONTINUE_ON_ERR}" = true ]; then  # -E
   warning "Set to continue despite error ..."
else
   note "set -e  # error stops execution ..."
   set -e  # exits script when a command fails
   # ALTERNATE: set -eu pipefail  # pipefail counts as a parameter
fi

if [ "${RUN_DEBUG}" = true ]; then   # -vv
   set -x
fi


###  07. Obtain operating system info to define package manager usage:

###  08. Validate variables controlling run:

h2 " 09. Create/recreate container folder and download this repo into it:"
cd
# TODO: WILSON: using Azure Storage Account ???
if [ !   -d "${MY_GIT_CONTAINER}" ]; then  # folder not found, so make it:
   mkdir -p "${MY_GIT_CONTAINER}"    # default "clouddrive" in Cloud Shell
fi
         cd "${MY_GIT_CONTAINER}"

# TODO: Assume delete previous version of GitHub:
if [   -d "${MY_REPO}" ]; then  # folder found, so remove it:
   rm -rf "${MY_REPO}"
fi
git clone https://github.com/wilson-mar/"${MY_REPO}".git --depth 1 
cd "${MY_REPO}"
ls
chmod +x *.sh   # make shell files executable.

###  10. Install and use CLI for logging into Azure:

###  11. :

h2 " 12. Install and start the Docker client if it's not already installed and started  (if needed locally):"
# TODO: If local

h2 " 13. Install az CLI to log into Azure (if needed locally):"
# TODO: if not installed: install it
az --version  # 2.22.0 and extensions

h2 " 14. Use az login # to Azure:"
# See https://docs.microsoft.com/en-us/cli/azure/ad/signed-in-user?view=azure-cli-latest
az login  # pops-up browser
      # Cloud Shell is automatically authenticated under the initial account signed-in with. Run 'az login' only if you need to use a different account
      # To sign in, use a web browser to open the page https://microsoft.com/devicelogin and enter the code RTGDJB9TN to authenticate.
RESPONSE=$( az ad signed-in-user show --query "accountEnabled" -o json )
if [[ "$RESPONSE" != *"true"* ]]; then  # TODO: state": "Enabled", userPrincipalName
   h2 " RESPONSE after az login not Enabled"
   abort
fi

h2 " 15. Create Resource Group: ${MY_RG}"
az group create --name "${MY_RG}" --location "${MY_LOC}"
   #    "provisioningState": "Succeeded"


h2 " 16. Create your private ACR (Azure Container Registry): \"${MY_ACR}\""
# https://docs.microsoft.com/en-us/azure/container-registry/container-registry-get-started-azure-cli
# https://docs.microsoft.com/en-us/azure/container-registry/container-registry-tutorial-prepare-registry

# See https://docs.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest
RESPONSE=$( az acr check-name -n "${MY_ACR}" )
# ERROR: Parameter 'RegistryNameCheckRequest.name' must have length greater than 5.
# if RESPONSE = exists:
   # fall thru
# "message": null,  # not created.
# if "nameAvailable": false   # abort to pick another ACR name.
# true,
   az acr create --sku Basic \
      --name "${MY_ACR}" \
      --resource-group "${MY_RG}"
# For more parms, see https://docs.microsoft.com/en-us/cli/azure/acr?view=azure-cli-latest

# TODO: In output, capture to $GEND_ACR_LOGIN_SERVER
  # "loginServer": "litthouse.azurecr.io",
#fi

# Service Tier: see https://docs.microsoft.com/en-us/azure/container-registry/container-registry-skus#changing-tiers
# az acr update --name "${MY_ACR}" --sku Standard
         # or --sku Premium   
         # or --sku Standard  # for increased storage and image throughput
         # or --sku Basic     # for best cost savings

h2 " 17. Login into your ACR: loginServer: ${MY_ACR}.azurecr.io:"
# If running Docker:
   # az acr login --name "${MY_ACR}"
# If running Cloud Shell, get an access token, which does not require Docker to be installed:
   RESPONSE=$( az acr login -n "${MY_ACR}" --expose-token )
   echo "$RESPONSE" | head -c 70   # first 70 characters of variable
   echo "\n"
   
h2 " 18. Create a Dockerfile (instead of reference one pre-created):"
# echo "FROM mcr.microsoft.com/hello-world" > hello-world.dockerfile # ???

h2 " 19. Use a Dockerfile to create a Docker container image:"


h2 " 20. Tag Docker image:"
# TODO: docker tag mcr.microsoft.com/hello-world <login-server>/hello-world:v1

h2 " 21. Install in ${MY_GIT_CONTAINER}/${MY_REPO} the OCI Registry as Storage (ORAS) tool:"
# On MacOS:
cd
cd "${MY_GIT_CONTAINER}"/"${MY_REPO}"  # use github repo.
pwd

   curl -LO https://github.com/deislabs/oras/releases/download/v0.11.1/oras_0.11.1_darwin_amd64.tar.gz
   tar -zxf oras_0.11.1_*.tar.gz   # unzip
   rm -rf oras_0.11.1_*.tar.gz     # remove
   if grep -q "${MY_REPO}" "$PATH"; then  # not in $PATH:
      echo "Already in PATH=$PATH"
   else
      # in Cloud Shell:
         PATH="/usr/csuser/${MY_GIT_CONTAINER}/${MY_REPO}/oras:$PATH\"    
      # Local:   
         PATH="$HOME/${MY_GIT_CONTAINER}/${MY_REPO}/oras:$PATH\"    
      echo "new PATH=$PATH"
   fi
   chmod +x oras
   ls -al oras

if ! command -v oras ; then    # not installed, so:
   fatal_msg "oras not found after install!"
   exit
fi

h2 " 22. Create a Service Principal with push rights:"
# TODO: 

h2 " 23. Sign in ORAS:"
oras login "${MY_ACR}".azurecr.io --username $SP_APP_ID --password $SP_PASSWD

h2 " 24. Use ORAS to push the new image into your ACR (Azure Container Registry), instead of DockerHub:">
# docker push <login-server>/hello-world:v1
oras push "${MY_ACR}".azurecr.io/samples/artifact:1.0 \
    --manifest-config /dev/null:application/vnd.unknown.config.v1+json \
    ./artifact.txt:application/vnd.unknown.layer.v1+txt
#
   # SAMPLE OUTPUT:
   # Uploading 33998889555f artifact.txt
   # Pushed myregistry.azurecr.io/samples/artifact:1.0
   # Digest: sha256:xxxxxxbc912ef63e69136f05f1078dbf8d00960a79ee73c210eb2a5f65xxxxxx

h2 " 25. Remove the image tag from your local Docker environment."
# (Note that this docker rmi command does not remove the image from the hello-world repository in your Azure container registry.)
docker rmi <login-server>/hello-world:v1

h2 " 26. List repos (artifacts) in ACR, to confirm:"
az acr repository list --name "${MY_ACR}" --output table

h2 " 27. List tags in ACR, to confirm:"
az acr repository show-tags --name "${MY_ACR}" --repository "${MY_ACR_REPO}" --output table

export registry="jasonacrr.azurecr.io"
export user="jasonacrr"
export password="t4AH+K86xxxxxxx2SMxxxxxzjNAMVOFb3c" 
export operation="/v2/aci-helloworld/tags/list" 
export credentials=$(echo -n "$user:$password" | base64 -w 0) 
export catalog=$(curl -s -H "Authorization: Basic $credentials" https://$registry$operation)
echo "Catalog"
echo $catalog


h2 " 28. Get attributes of an artifact in ACR, to confirm:"
az acr repository show \
    --name "${MY_ACR}" \
    --image samples/artifact:1.0.  # ???

h2 " 29. Have Azure Defender Security Center scan images in ACR:"
# https://docs.microsoft.com/en-us/azure/security-center/defender-for-container-registries-introduction?bc=/azure/container-registry/breadcrumb/toc.json&toc=/azure/container-registry/toc.json

h2 " 30a. Run individual Docker image or "
docker run <login-server>/hello-world:v1

h2 " 30b. Reference Helm3 charts as OCI artifacts in the ACR (Azure Container Registry):"
#          The OCI (Open Container Initiative) Image Format Specs is at https://github.com/opencontainers/distribution-spec"
# https://docs.fluxcd.io/projects/helm-operator/en/1.0.0-rc9/references/helmrelease-custom-resource.html

h2 " 31. Use ACR tasks to build and test container images."

h2 " 32. Install Helm, get helm version."

h2 " 33. Push change into Helm to trigger run which establishes services in Azure."

h2 " 34. Validate automation."

h2 " 35. List resource group:"
az group list -o table
   # Ignore "cloud-shell-storage-westus" and "NetworkWatcherRG"

h2 " 36. List resources under resource group:"
az resource list --resource group "${MY_RG}" --location "${MY_LOC}"
   # Alternative: a. Install Python environment
   # python --version
   # Install b. In requirements.txt azure-mgmt-resource>=1.15.0 & azure-identity>=1.5.0
   # pip install -r requirements.txt
   # Bring in code from https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-example-list-resource-groups 
      # to 3b. List resources within a specific resource group
   # Authenticate Python apps with Azure services: https://docs.microsoft.com/en-us/azure/developer/python/azure-sdk-authenticate
   # Run: python list_resources.py "${MY_RG}"
   
   # https://vincentlauzon.com/2016/01/21/listing-resources-under-resource-group-with-azure-powershell/
   
h2 " 37. Clean up resource group, ACR, images, then list Resource Groups:"
az group delete --name "${MY_RG}"

