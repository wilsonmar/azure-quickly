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
export MY_GITHUB_ACCT="Azure"
export MY_GITHUB_REPO="azureml-examples"
export MY_REPO_FOLDER="$MY_GITHUB_REPO"

export MY_COMPUTE_SPEC="STANDARD_D3_V2"  # Standard_NC12"

   RUN_DEBUG=false              # -vv
   RUN_QUIET=false              # -q
   RUN_VERBOSE=false            # -v
   SET_TRACE=false              # -x

   RMV_RG_AT_END=false       # parm -RRGe
   RMV_GITHUB_AT_END=false   # parm -RGe

# <az_ml_code_download>
function thisfile_DO_GITHUB_CLONE() {
   echo ">>> Cloning folder \"${MY_GITHUB_ACCT}\" from \"$MY_REPO_FOLDER\" "
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
      echo ">>> Pulling into folder \"$MY_REPO_FOLDER\" "
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
function thisfile_ADD_EXTENSION() {
   echo ">>> az extension add -n $1 "  # $1 is the first parameter
   az extension add -n $1
   # The installed extension 'ml' is experimental and not covered by customer support. Please use with discretion.
}
# echo ">>> az extension version check ... "
EXT_VERSION=$( az extension list -o table --query "[?contains(name, 'ml')].{Version:version}" -o tsv )
if [ -z "${EXT_VERSION}" ]; then
   echo ">>> az extension \"ml\" not found."
   thisfile_ADD_EXTENSION ml
else
   echo ">>> Remove az extionsion \"ml\" version $EXT_VERSION and add again:"
   # Per https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli
   # Ensure no conflicting extension using the ml namespace:
   az extension remove -n ml
   thisfile_ADD_EXTENSION ml
fi
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
time az ml compute create -n cpu-cluster --type AmlCompute --min-instances 0  --max-instances 10 

echo ">>> az ml compute create AmlCompute 4 of \"${MY_COMPUTE_SPEC}\" ..."
time az ml compute create -n gpu-cluster --type AmlCompute --min-instances 0 --max-instances 4 \
   --size "${MY_COMPUTE_SPEC}"
# </create_computes>


# <ml_run>
echo ">>> az ml job create -f jobs/hello-world-env-var.yml ..."
pwd
echo ">>> MY_PROJECTS_FOLDER=${MY_PROJECTS_FOLDER}, MY_REPO_FOLDER=${MY_REPO_FOLDER} "
cd
#cd "~/${MY_PROJECTS_FOLDER}/${MY_REPO_FOLDER}/cli"
cd "~/clouddrive/${MY_REPO_FOLDER}/cli"
pwd
# cd jobs  # https://github.com/Azure/azureml-examples/tree/main/cli/jobs
# https://docs.microsoft.com/en-us/cli/azure/ml/job
time az ml job create -f jobs/train/lightgbm/iris/job.yml --set compute.target=local --web --stream
#az ml job create -f jobs/hello-world-env-var.yml --web --stream
#az ml job create -f jobs/hello-world.yml --web --stream
# QUESTION: Where is the output "hello world"?
# </ml_run>


if [ "${RMV_RG_AT_END}" = true ]; then  # param -d 
   echo ">>> Delete Resource Group \"$MY_RG\" at end of script ..."
   time az group delete --resource-group "${MY_RG}" --yes
fi
