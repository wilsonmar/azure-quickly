#!/usr/bin/env bash
# ./az-mlcli2.sh within https://github.com/wilsonmar/azure-quickly
# This script incorporats into a single script the setup.sh and hello-world in 
# https://docs.microsoft.com/en-us/samples/azure/azureml-examples/azure-machine-learning-20-cli-preview-examples/
# https://docs.microsoft.com/en-us/samples/azure/azureml-examples/azure-machine-learning-python-sdk-examples/
# This script contains bash setup.sh with customization of ResourceGroups, Location/Region, vm size, etc.
   # https://ms.portal.azure.com/#blade/HubsExtension/DeploymentDetailsBlade/overview/id/%2Fsubscriptions%2F32f0f1ee-690d-4b02-9e58-baa3715aabf7%2FresourceGroups%2Fazureml-examples-rg%2Fproviders%2FMicrosoft.Resources%2Fdeployments%2Fmain-5626528
   # shows "Your deployment is complete"

set -o errexit   # So don't have any errors ;)


if [[ -z $MY_RG ]]; then
   source ../setmem.sh   # in folder above this.
fi


# MY_LOC="westus2"
# MY_RG="devml"
# MY_MLWORKSPACE_NAME="devml01"
# MY_STORAGE_SKU="Standard_NC12"

   RMV_RG_BEFORE=true        # parm -RRGb
   RMV_GITHUB_BEFORE=false   # parm -RGb
   DO_GITHUB_CLONE=true      # parm -c
# MY_PROJECTS_FOLDER="projects"   # "projects" if local, "clouddrive" if cloud shell 
MY_GITHUB_ACCT="Azure"
MY_GITHUB_REPO="azureml-examples"
MY_REPO_FOLDER="$MY_GITHUB_REPO"

MY_STORAGE_SKU="Standard_NC12"

   RUN_DEBUG=false              # -vv
   RUN_QUIET=false              # -q
   RUN_VERBOSE=false            # -v
   SET_TRACE=false              # -x

   RMV_RG_AT_END=false       # parm -RRGe
   RMV_GITHUB_AT_END=false   # parm -RGe

# <az_ml_code_download>
function thisfile_DO_GITHUB_CLONE() {
   echo ">>> Cloning $MY_REPO_FOLDER "
   time git clone "https://github.com/${MY_GITHUB_ACCT}/${MY_GITHUB_REPO}.git"  "$MY_REPO_FOLDER" --depth 1 
   cd "$MY_REPO_FOLDER"
   pwd
}
cd
cd "${MY_PROJECTS_FOLDER}"
pwd
if [ -d "$MY_REPO_FOLDER" ]; then
   if [ "${RMV_GITHUB_BEFORE}" = true ]; then  # param -d 
      echo ">>> Removing folder $MY_REPO_FOLDER "
      time rm -rf "$MY_REPO_FOLDER"
      thisfile_DO_GITHUB_CLONE
   else
      echo ">>> Found folder $MY_REPO_FOLDER "
      cd "$MY_REPO_FOLDER"
      git config pull.rebase false
      git pull
   fi 
else   #  "$MY_REPO_FOLDER" not found:
   if [ "${DO_GITHUB_CLONE}" = true ]; then  # param -c
      thisfile_DO_GITHUB_CLONE
   # else use repo previously cloned.
   fi
fi
# </az_ml_code_download>


# <az_ml_install>
echo ">>> az extension version check ... "
EXT_VERSION=$( az extension list -o table --query "[?contains(name, 'xx')].{Version:version}" -o tsv )
if [ -z "${EXT_VERSION}" ]; then
   echo ">>> 1 EXT_VERSION=$EXT_VERSION"
else
   echo ">>> 2 EXT_VERSION=$EXT_VERSION"
fi

exit


# <az_ml_install>
echo ">>> az extension list ... "
EXT_VERSION=$( az extension list -o table --query "[?contains(name, 'ml')].{Version:version}" -o tsv )
if [ "not installed." == *"${RESPONSE}"* ]; then
fi

az extension list --query "[].{Name:name, Version:version}" -o tsv

function thisfile_ADD_EXTENSION_ML() {
   echo ">>> az extension add -n ml "
   az extension add -n ml
   # The installed extension 'ml' is experimental and not covered by customer support. Please use with discretion.
}
RESPONSE=$( time az extension update -n azure-cli-ml )
if [ "not installed." == *"${RESPONSE}"* ]; then
   echo ">>> $RESPONSE "  # not installed:
   thisfile_ADD_EXTENSION_ML
else
   echo ">>> ML CLI extension already installed. Removing. "
   # Per https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli
   # Ensure no conflicting extension using the ml namespace:
   az extension remove -n azure-cli-ml
   az extension remove -n ml
   thisfile_ADD_EXTENSION_ML
fi
# Check:
   # az extension list-available -o table | grep azure-cli-ml 
# </az_ml_install>


# <az_group_create>
if [ $(az group exists --name "${MY_RG}") = true ]; then
   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
   time az group delete --resource-group "${MY_RG}" --yes
fi
echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   time az group create --name "${MY_RG}" --location "${MY_LOC}"
# </az_group_create>


# <az_configure_defaults>
az configure --defaults group="${MY_RG}" workspace="${MY_MLWORKSPACE_NAME}"
# </az_configure_defaults>


# <az_ml_workspace_create>
RESPONSE=$( time az ml workspace list )  # any workspace:
if [ $RESPONSE == "[]" ]; then
   echo ">>> Create ML workspace \"$MY_MLWORKSPACE_NAME\" ..."
   time az ml workspace create \
      --workspace-name "${MY_MLWORKSPACE_NAME}" \
      --resource-group "${MY_RG}" 
   # This creates resources:
   #   * Machine learning
   #   * Application Insights
   #   * Key vault
   #   * Storage account
fi
# RESPONSE: 
# </az_ml_workspace_create>



# <create_computes>
echo ">>> az ml compute create AmlCompute 10 (default size)..."
az ml compute create -n cpu-cluster --type AmlCompute --min-instances 0  --max-instances 10 

echo ">>> az ml compute create AmlCompute 4 of \"${MY_STORAGE_SKU}\" ..."
az ml compute create -n gpu-cluster --type AmlCompute --min-instances 0 --max-instances 4 \
--size "${MY_STORAGE_SKU}"
# </create_computes>



# <ml_run>
echo ">>> az ml job create -f jobs/hello-world-env-var.yml ..."
cd jobs  # https://github.com/Azure/azureml-examples/tree/main/cli/jobs
az ml job create -f jobs/hello-world-env-var.yml --web --stream
#az ml job create -f jobs/hello-world.yml --web --stream
# QUESTION: Where is the output "hello world"?
# </ml_run>


if [ "${RMV_RG_AT_END}" = true ]; then  # param -d 
   echo ">>> Delete Resource Group \"$MY_RG\" at end of script ..."
   time az group delete --resource-group "${MY_RG}" --yes
fi
