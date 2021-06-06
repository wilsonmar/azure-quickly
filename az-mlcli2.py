#!/usr/bin/env bash
f
# ./az-mlcli2.sh within https://github.com/wilsonmar/azure-qu
# This script incorporats into a single script the setup.sh and hello-world in 
# https://docs.microsoft.com/en-us/samples/azure/azureml-examples/azure-machine-learning-20-cli-preview-examples/
# https://docs.microsoft.com/en-us/samples/azure/azureml-examples/azure-machine-learning-python-sdk-examples/
# This script contains bash setup.sh with customization of ResourceGroups, Location/Region, vm size, etc.
   # https://ms.portal.azure.com/#blade/HubsExtension/DeploymentDetailsBlade/overview/id/%2Fsubscriptions%2F32f0f1ee-690d-4b02-9e58-baa3715aabf7%2FresourceGroups%2Fazureml-examples-rg%2Fproviders%2FMicrosoft.Resources%2Fdeployments%2Fmain-5626528
   # shows "Your deployment is complete"

# MY_LOC="uswest"
# MY_RG="devml"
# MY_MLWORKSPACE_NAME="devml01"
# MY_STORAGE_SKU="Standard_NC12"

   RMV_RG_BEFORE=true        # parm -RRGb
   RMV_GITHUB_BEFORE=false   # parm -RGb
   DO_GITHUB_CLONE=true      # parm -c
MY_GITHUB_ACCT="Azure"
MY_GITHUB_REPO="azureml-examples"
MY_REPO_FOLDER="$MY_GITHUB_REPO"

   RUN_DEBUG=false              # -vv
   RUN_QUIET=false              # -q
   RUN_VERBOSE=false            # -v
   SET_TRACE=false              # -x

   RMV_RG_AT_END=false       # parm -RRGe
   RMV_GITHUB_AT_END=false   # parm -RGe

set -o errexit


# <az_ml_code_download>
function thisfile_DO_GITHUB_CLONE() {
   echo ">>> Cloning $MY_REPO_FOLDER "
   time git clone "https://github.com/${MY_GITHUB_ACCT}/${MY_GITHUB_REPO}.git"  "$MY_REPO_FOLDER" --depth 1 
   cd "$MY_REPO_FOLDER"
   pwd
}
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

exit

if [[ -z $MY_RG ]]; then
   source ../setmem.sh   # in folder above this.
fi

# <az_ml_install>
echo ">>> Check & Add CLI extension \"azure-cli-ml\" "
RESPONSE=$( time az extension update -n azure-cli-ml )
if [ "The extension azure-cli-ml is not installed." == "${RESPONSE}" ]; then
   time az extension add -n "azure-cli-ml"
fi
# Check:
   # az extension list-available -o table | grep azure-cli-ml 
# </az_ml_install>


# <az_group_create>
if [ $(az group exists --name "${MY_RG}") = true ]; then
   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
   timeaz group delete --resource-group "${MY_RG}" --yes
fi
echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   time az group create --name "${MY_RG}" --location "${MY_LOC}"
# </az_group_create>


# <az_configure_defaults>
az configure --defaults group="${MY_RG}" workspace="${MY_MLWORKSPACE_NAME}"
# </az_configure_defaults>


# <az_ml_workspace_create>
## ????
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
az ml compute create -n cpu-cluster --type AmlCompute \
    --min-instances 0 --max-instances 10 
az ml compute create -n gpu-cluster --type AmlCompute \
    --min-instances 0 --max-instances 4 --size "${MY_STORAGE_SKU}"
# </create_computes>


# <ml_run>
cd jobs  # https://github.com/Azure/azureml-examples/tree/main/cli/jobs
az ml job create -f jobs/hello-world-env-var.yml --web --stream
#az ml job create -f jobs/hello-world.yml --web --stream
# </ml_run>


exit

   echo ">>> Create Compute \"$MY_COMPUTE_NAME\" using \"$MY_COMPUTE_SPEC\":"
   # CLI DOC: https://docs.microsoft.com/en-us/cli/azure/ml/computetarget/create?view=azure-cli-latest#az_ml_computetarget_create_computeinstance
   time az ml computetarget create computeinstance \
      -n "${MY_COMPUTE_NAME}" \
      -s "${MY_COMPUTE_SPEC}"  \
      --workspace-name "${MY_MLWORKSPACE_NAME}" \
      --ssh-public-access False \
      --resource-group "${MY_RG}" -v
