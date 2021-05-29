#!/bin/bash

# ./az-storage-init.sh
# This creates a storage account, the equivalent of manual portal
# 1. Prepare your CLI Bash environment according to https://wilsonmar.github.io/azure-quickly
#    which references repo https://github.com/wilsonmar/azure-quickly.
# 2. In your clouddrive folder edit your preferences in ../setmem.sh (MY_RG, MY_LOC, etc.)
# 3. Copy and paste this to the Bash command line:
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-storage-init.sh)" -v -i

set -o errexit

if [[ -z "${MY_RG}" ]]; then
   echo ">>> MY_RG \"${MY_RG}\" not defined. "
   source ../setmem.sh   # in folder above this.
else
   echo ">>> MY_RG \"${MY_RG}\" defined. "
fi


#   export MY_STORAGE_ACCT="${MY_RG}storage$RANDOM"   
#         # LIMIT: Max. 24 lower-case char & numbers, no dashes. globally unique 
#         # MY_STORAGE_ACCT.core.windows.net
#   export MY_STORAGE_CONTAINER="wooz"
#   export MY_STORAGE_TAGS="env=dev"

if [[ -z "${MY_SUBSCRIPTION_ID}" ]]; then
   echo ">>> MY_SUBSCRIPTION_ID \"${MY_SUBSCRIPTION_ID}\" not defined. Aborting. "
   exit
fi


# CLI DOC: https://docs.microsoft.com/en-us/cli/azure/storage/account?view=azure-cli-latest
# https://docs.microsoft.com/en-us/azure/storage/common/storage-account-keys-manage?tabs=azure-portal
if [[ -z "${MY_STORAGE_ACCT}" ]]; then  # not defined
   export MY_STORAGE_ACCT="${MY_RG}storage$RANDOM"  # One acct per day
         # LIMIT: Max. 24 lower-case char & numbers, no dashes. globally unique 
         # MY_STORAGE_ACCT.core.windows.net
fi


# Check if name is avialable:
#   RESPONSE=$( az storage account check-name --name "$MY_STORAGE_ACCT" \
#      --query nameAvailable \
#      --subscription "${MY_SUBSCRIPTION_ID}" )
## TODO: If flag says to crate
#if [[ true != "$RESPONSE" ]]; then
#   echo ">>> Storage acct \"$MY_STORAGE_ACCT\" already created "
#else

   echo ">>> Create storage acct \"$MY_STORAGE_ACCT\" with \"${MY_STORAGE_SKU}\" "
   az storage account create \
      --name "${MY_STORAGE_ACCT}" \
      --sku "${MY_STORAGE_SKU}" \
      --resource-group "${MY_RG}"
   

   # https://docs.microsoft.com/en-us/cli/azure/storage/account/keys?view=azure-cli-latest
   echo ">>> Getting key1 for ${MY_STORAGE_ACCT} "
   export MY_STORAGE_KEY1=$( az storage account keys list -n "${MY_STORAGE_ACCT}" \
         --resource-group "${MY_RG}" --query [0].value -o tsv )
   echo ">>> MY_STORAGE_KEY1=$MY_STORAGE_KEY1 "
# export MY_STORAGE_KEY1"${MY_STORAGE_KEY1}"
#[
# {
#    "keyName": "key1",
#    "permissions": "FULL",
#    "value": "aaaT0ODtTwUC+5dNP2sv7YmvJW8/E4rfngGyxApxw7A0eUrAhWwUzm92cKVOgv75X66kFdgb+TsdmZ7cQ4vWew=="
#  },
#]

#az storage account list --resource-group "${MY_RG}" --output table 
   # --query [*].{Name:name,Location:primaryLocation,Kind:kind}  CreationTime
   # grep to show only on created to filter out cloud-shell-storage account


#   export MY_STORAGE_TAGS="env=dev"
if [[ -n "${MY_STORAGE_TAG}" ]]; then  # not blank:
   echo ">>> Add tag \"${MY_STORAGE_TAG}\" to Storage account \"$MY_STORAGE_ACCT\":"
   az storage account update --name "${MY_STORAGE_ACCT}" \
      --tags “${MY_STORAGE_TAGS}” \
      --resource-group "${MY_RG}"
   # RESPONSE: "tags": {
   #             "“env": "dev”"
fi


# az storage account network-rule add
# echo ">>> Show current count & limit of storage accounts under subscription:"
# az storage account show-usage
#az storage account show-usage --location westus2
#   --subscription "${MY_SUBSCRIPTION_ID}"

