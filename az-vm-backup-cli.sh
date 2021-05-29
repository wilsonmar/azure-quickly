#!/usr/bin/env bash
# az-vm-backup-cli.sh

# This script was adapted from https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/13/azure_cli_sample.sh
# released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
# and chapter 13 of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
# Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi


# Create a resource group
az group create --name "${MY_RG}" --location "${MY_LOC}"

# Create a Linux VM
# You specify the resoure group from the previous step, then provide a name.
# This VM uses Ubuntu LTS as the VM image, and creates a user name MY_ADMIN_USER_NAME `azuremol`
# The `--generate-ssh-keys` checks for keys you may have created earlier. If
# SSH keys are found, they are used. Otherwise, they are created for you
az vm create \
    --name "${MY_VM_NAME}" \
    --image UbuntuLTS \
    --admin-username "${MY_ADMIN_USER_NAME}" \
    --generate-ssh-keys \
    --resource-group "${MY_RG}"

# Create a Recovery Services vault
# This vault is used to store your backups
az backup vault create \
    --name "${MY_RECOVERY_VAULT_NAME}" \
    --location "${MY_LOC}" \
    --resource-group "${MY_RG}"
    
# It can take a few seconds for the Recovery Services vault to become
# available, so wait before trying to enable the VM for protection
sleep 10

# Enable backup for the VM
# The Recovery Services vault created in the previous step is used as the
# destination for the VM backup data
# The default backup policy for retention is also then applied
az backup protection enable-for-vm \
    --vm molvm \
    --vault-name "${MY_RECOVERY_VAULT_NAME}" \
    --policy-name DefaultPolicy \
    --resource-group "${MY_RG}"

# Start a backup job for the VM
# The data is formatted into the d-m-Y format and is retained for 30 days
az backup protection backup-now \
    --item-name "${MY_VM_NAME}" \
    --vault-name "${MY_RECOVERY_VAULT_NAME}" \
    --container-name molvm \
    --retain-until $(date +%d-%m-%Y -d "+30 days") \
    --resource-group "${MY_RG}"

# List the backup jobs
# The status of the backup should be listed as InProgress. It can 15-20 minutes
# for the initial backup job to complete
az backup job list \
    --vault-name "${MY_KEYVAULT_NAME}" \
    --output table \
    --resource-group "${MY_RG}"
    
echo "It can take 25-30 minutes for the initial backup job to complete."
