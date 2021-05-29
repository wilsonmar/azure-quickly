#!/usr/bin/env bash

# ./az-mon.sh
# Adapted from https://github.com/MicrosoftLearning/AI-102-AIEngineer/blob/master/03-monitor/rest-test.cmd

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

curl -X POST "<yourEndpoint>/text/analytics/v3.0/languages?" \
   -H "Content-Type: application/json" \
   -H "Ocp-Apim-Subscription-Key: <yourKey>" 
   --data-ascii "{'documents':[{'id':1,'text':'hello'}]}"