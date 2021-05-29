#!/usr/bin/env bash

# ./az-knowstore-setup.sh
# Adapted from CMD 

set -o errexit

if [[ -z "${MY_RG}" ]]; then
   echo ">>> Running $PWD/setup.sh ..."
   source ../setup.sh   # in folder above this.
fi

### No need to login if user is signed in:
RESPONSE=$( az ad signed-in-user show --query "userPrincipalName" -o tsv )
echo ">>> Running as user \"$RESPONSE\" ..."
#   az login  # --allow-no-subscriptions  # --use-device-code
    # wait to see https://docs.microsoft.com/en-us/cli/azure/


echo ">>> Set subscription ..."
az account set --subscription "${MY_SUBSCRIPTION_ID}"


if [ $( az group exists --name "${MY_RG}" ) = true ]; then
   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
   time az group delete --resource-group "${MY_RG}" --yes
else
   echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   time az group create --name "${MY_RG}" --location "${MY_LOC}"
fi

#### Storage accounts are not under Resources
# IF VERBOSE:
# SpecialFeatureOrQuotaIdRequired: The subscription does not have QuotaId/Feature required by SKU 'F0'.
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/error-sku-not-available
#   echo ">>> List SKUs for Location \"$MY_LOC\" :"
#    az vm list-skus --location "${MY_LOC}" --size Standard_F --all -o table | grep "${MY_LOC}"

   echo ">>> Storage accounts ..."
# https://docs.microsoft.com/en-us/cli/azure/storage/account?view=azure-cli-latest#az_storage_account_list
# https://docs.microsoft.com/cli/azure/query-azure-cli
RESPONSE=$( az storage account list --subscription "${MY_SUBSCRIPTION_ID}" \
   --resource-group  "${MY_RG}" -o table )
#   --query-examples [?name = `"${MY_STORAGE_ACCT}"`].[name, provisioningState] \
#    --query provisioningState "[?name == `margies`]" \
#--query-examples "${MY_STORAGE_ACCT}"
# ProvisioningState 
# echo "RESPONSE=$RESPONSE"

#if [[ "ProvisioningState" == *"$RESPONSE"* ]]; then   # response contains it:
#   echo ">>> Storage \"${MY_STORAGE_ACCT}\" exists."
#else
   echo ">>> Create storage \"${MY_STORAGE_ACCT}\" to persist enriched data to a knowledge store ..."
   # https://stackoverflow.com/questions/56894664/retrieve-azure-storage-account-key-using-azure-cli
   time az storage account create --name "${MY_STORAGE_ACCT}" \
      --subscription "${MY_SUBSCRIPTION_ID}" \
      --location "${MY_LOC}" \
      --sku Standard_LRS --encryption-services blob --default-action Allow --output none \
      --resource-group "${MY_RG}" 
#fi

echo ">>> Get storage key1 from \"${MY_STORAGE_ACCT}\" ... "
AZURE_STORAGE_KEY=$( az storage account keys list \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --account-name "${MY_STORAGE_ACCT}" \
   --query [0].value -o tsv \
   --resource-group "${MY_RG}" 
   )
#   --query "[?keyName=='key1']" \

time az storage container create --name "${MY_STORAGE_ACCT}" \
   --account-name "${MY_STORAGE_ACCT}" \
   --auth-mode key --account-key "${MY_STORAGE_KEY}" \
   --public-access blob --output none

echo ">>> Uploading to \"${MY_STORAGE_ACCT}\" ... "
# https://docs.microsoft.com/en-us/cli/azure/storage/blob?view=azure-cli-latest#az_storage_blob_upload_batch
time az storage blob upload-batch --account-name "${MY_STORAGE_ACCT}" \
   --auth-mode key --account-key "${MY_STORAGE_KEY}" \
   -d "${MY_STORAGE_CONTAINER}" -s data --output none


# https://docs.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest
export MY_COG_KIND="CognitiveServices"
#export MY_COG_PRICING_TIER="Standard_F2s_v2"
export MY_COG_PRICING_TIER="S0"
echo ">>> Creating cognitive services account \"${COG_SERVICE_ENDPOINT}\" ..."
time az cognitiveservices account create --kind "${MY_COG_KIND}" \
   --location "${MY_LOC}" --name "${COG_SERVICE_ENDPOINT}" \
   --sku "${MY_COG_PRICING_TIER}" \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --resource-group "${MY_RG}" --yes --output none

echo ">>> Creating search service \"${MY_SEARCH_SVC}\" ..."
echo "(If this gets stuck at '- Running ..' for more than a minute, press CTRL+C then select N)"
time az search service create --name "${MY_SEARCH_SVC}" \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --location "${MY_LOC}" --sku basic --output none \
   --resource-group "${MY_RG}" 

echo ">>> Storage account: "${MY_STORAGE_ACCT}""
time az storage account show-connection-string  --name "${MY_STORAGE_ACCT}" \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --resource-group "${MY_RG}"


echo ">>> Cognitive Services account: "${COG_SERVICE_ENDPOINT}""
time az cognitiveservices account keys list --name "${COG_SERVICE_ENDPOINT}" \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --resource-group "${MY_RG}" 


echo ">>> Search Service URL: https://${MY_SEARCH_SVC}.search.windows.net/ " 

echo ">>> Admin Keys \"${MY_SEARCH_SVC}\" ..."
# https://docs.microsoft.com/en-us/cli/azure/search/admin-key?view=azure-cli-latest#az_search_admin_key_show
time az search admin-key show --service-name "${MY_SEARCH_SVC}" \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --resource-group "${MY_RG}" 

echo ">>> Query Keys for \"${MY_SEARCH_SVC}\" ..."
# https://docs.microsoft.com/en-us/cli/azure/search/query-key?view=azure-cli-latest#az_search_query_key_list
time az search query-key list --service-name "${MY_SEARCH_SVC}" \
   --subscription "${MY_SUBSCRIPTION_ID}" \
   --resource-group "${MY_RG}" 

