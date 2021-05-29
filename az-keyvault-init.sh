#!/usr/bin/env bash

# ./az-keyvault-init.sh
# This script was adapted from https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/15/azure_cli_sample.sh
# released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
# and chapter 15 of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
# Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition
# References:
# https://github.com/Azure-Samples/app-service-msi-keyvault-dotnet
# https://app.pluralsight.com/library/courses/microsoft-azure-security-engineer-configure-manage-key-vault Sep 08, 2020
# https://app.pluralsight.com/library/courses/microsoft-azure-key-vault-configuring-managing Nov 18, 2020
   # https://github.com/ned1313/Configure-and-Manage-Key-Vault
# https://newsignature.com/articles/azure-devops-with-a-firewall-enabled-key-vault/
# TODO: https://portal.cloudskills.io/products/build-a-ci-cd-pipeline-with-azure-devops
# https://portal.cloudskills.io/products/build-a-ci-cd-pipeline-with-azure-devops/categories/4475187/posts/15021741 [18:27] by Michael Levan

set -o errexit

if [[ -z "${MY_RG}" ]]; then
   exit
   # source ../setup.sh   # in folder above this.
fi


# Parameters are in order shown on the Portal GUI screen https://portal.azure.com/#create/Microsoft.KeyVault
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/keyvault?view=azure-cli-latest#az_keyvault_create
RESPONSE=$( az keyvault list )   # Identify if keyvault already exists
if [ $RESPONSE == "[]" ]; then
   echo ">>> Create Key Vault \"$MY_KEYVAULT_NAME\":"
   az keyvault create \
    --name "${MY_KEYVAULT_NAME}" \
    --location "${MY_LOC}" \
    --retention-days 90 \
    --enabled-for-deployment \
    --default-action Deny \
    --resource-group "${MY_RG}" 
fi
#    --enabled-for-deployment \. in GUI Portal is checkbox "Enable Access to: Azure Resource Manager for template deployment"
  # Argument 'enable_soft_delete' has been deprecated and will be removed in a future release.
  # --enable-purge-protection false # during test env usage when Vault is rebuilt between sessions.
# QUESTION: The vault is enabled for soft delete by default, which allows deleted keys to recovered, but a new keyvault name needs to be created every run.
# and is also enable for deployment which allows VMs to use the keys stored.
  # --default-action Deny # Default action to apply when no rule matches.
  # --retention-days 90 \  # 90 is max allowed.
  # --sku Standard  # or Premium (includes support for HSM backed keys) HSM: Standard_B1, Custom_B32. Default: Standard_B1.
  # See https://docs.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview
# RESPONSE: Resource provider 'Microsoft.KeyVault' used by this operation is not registered. We are registering for you.

vaultId=$( az keyvault show -g "${MY_RG}" -n "${MY_KEYVAULT_NAME}" | jq -r .id)
echo ">>> vaultId = \"$vaultId\" "

