      # https://docs.microsoft.com/en-us/azure/azure-resource-manager/templates/error-not-found


MY_RG="wow"
MY_STORAGE_ACCT="wowstorage32010"
   echo ">>> Save key1 for ${MY_STORAGE_ACCT} "
   export MY_STORAGE_KEY1=$( az storage account keys list -n "${MY_STORAGE_ACCT}" \
             --resource-group "${MY_RG}"  --query "[0].value" -o tsv )
   echo ">>> MY_STORAGE_KEY1=$MY_STORAGE_KEY1 "
