#!/usr/bin/env bash

# ./az-mlworkspace-cli.sh  # under MIT license.
# This script is based on https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace-cli
# It lists LIMITATIONS: 
#   The storage account is not a premium account (Premium_LRS and Premium_GRS)
#   Both Azure Blob and Azure File capabilities enabled
#   Hierarchical Namespace (ADLS Gen 2) is disabled

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setmem.sh   # in folder above this.
fi


if [ $(az group exists --name "${MY_RG}") = true ]; then
   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
   timeaz group delete --resource-group "${MY_RG}" --yes
fi
echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   time az group create --name "${MY_RG}" --location "${MY_LOC}"


# https://docs.microsoft.com/en-us/azure/machine-learning/reference-azure-machine-learning-cli
# https://docs.microsoft.com/en-us/cli/azure/azure-cli-extensions-overview
# https://docs.microsoft.com/en-us/azure/virtual-machines/extensions/overview
# https://docs.microsoft.com/en-us/cli/azure/ml?view=azure-cli-latest
# Python wheels 
echo ">>> Check & Add CLI extension \"azure-cli-ml\" "
RESPONSE=$( time az extension update -n azure-cli-ml )
if [ "The extension azure-cli-ml is not installed." == "${RESPONSE}" ]; then
   time az extension add -n "azure-cli-ml"
fi
# Check:
   # az extension list-available -o table | grep azure-cli-ml 


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


   echo ">>> Create Compute \"$MY_COMPUTE_NAME\" using \"$MY_COMPUTE_SPEC\":"
   # CLI DOC: https://docs.microsoft.com/en-us/cli/azure/ml/computetarget/create?view=azure-cli-latest#az_ml_computetarget_create_computeinstance
   time az ml computetarget create computeinstance \
      -n "${MY_COMPUTE_NAME}" \
      -s "${MY_COMPUTE_SPEC}"  \
      --workspace-name "${MY_MLWORKSPACE_NAME}" \
      --ssh-public-access False \
      --resource-group "${MY_RG}" -v

# https://docs.microsoft.com/en-us/samples/azure/azureml-examples/azure-machine-learning-20-cli-preview-examples/
