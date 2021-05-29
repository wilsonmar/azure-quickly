#!/usr/bin/env bash

# ./az-cog-lang.sh
# within 

set -o errexit

if [[ -z $MY_RG ]]; then
   echo ">>> Running $PWD/setup.sh ..."
   source ../setup.sh   # in folder above this.
fi

## Create Cognitive service:

### No need to login ifcan be found:
#   az login  # --allow-no-subscriptions  # --use-device-code
#sleep 10  # wait to see https://docs.microsoft.com/en-us/cli/azure/


echo ">>> Set subscription ..."
az account set --subscription "${MY_SUBSCRIPTION_ID}"


if [ $(az group exists --name "${MY_RG}") = true ]; then
   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
   time az group delete --resource-group "${MY_RG}" --yes
fi
echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
    time az group create --name "${MY_RG}" --location "${MY_LOC}"


# SpecialFeatureOrQuotaIdRequired: The subscription does not have QuotaId/Feature required by SKU 'F0'.
# https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/error-sku-not-available
   echo ">>> List SKUs for Location \"$MY_LOC\" :"
    az vm list-skus --location "${MY_LOC}" --size Standard_F --all -o table | grep "${MY_LOC}"


# https://docs.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest
export MY_COG_KIND="TextTranslation" 
#export MY_COG_PRICING_TIER="Standard_F2s_v2"
export MY_COG_PRICING_TIER="Standard_F1s"
echo ">>> Create $MY_COG_KIND for cognitiveservices account \"$MY_COG_ACCT\" :"
exit
 az cognitiveservices account create \
    --name "${MY_COG_ACCT}"  \
    --kind "${MY_COG_KIND}" \
    --sku "${MY_COG_PRICING_TIER}" \
    --location "${MY_LOC}" \
    --yes \
    --resource-group "${MY_RG}" 

echo ">>> Get COGNITIVE_SERVICE_KEY:"
COGNITIVE_SERVICE_KEY=$( az cognitiveservices account keys list \
    --name "${MY_COG_ACCT}" \
    --resource-group "${MY_RG}" --query key1 -o tsv
    )
# RESPONSE:
#  "key1": "27900c313d0e494b9d53993cab31f92f",
#  "key2": "3c0c2c36bc704f28b79f4e6cd81dadd2"
# trace echo "COGNITIVE_SERVICE_KEY=$COGNITIVE_SERVICE_KEY  # used by Azure"

echo ">>> COGNITIVE_SERVICE_KEY=$COGNITIVE_SERVICE_KEY"


curl -X POST "<yourEndpoint>/text/analytics/v3.0/languages?" \
     -H "Content-Type: application/json" \
     -H "Ocp-Apim-Subscription-Key: <yourKey>" \
     --data-ascii "{'documents':[{'id':1,'text':'hello'}]}"