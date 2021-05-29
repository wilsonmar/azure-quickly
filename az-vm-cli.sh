#!/usr/bin/env bash

# az-vm-cli.sh
# This script was adapted from https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/02/azure_cli_sample.sh
# released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
# and chapter 2 of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
# Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi


# Create a resource group. This is a logical container to hold your resources.
# You can specify any name you wish, so long as it's unique with your Azure
# subscription and location
echo "MY_RG=$MY_RG MY_LOC=${MY_LOC}"
az group create --name "${MY_RG}" --location "${MY_LOC}"

# Ensure a .ssh folder is available to hold key pairs:
if [ ! -d ~/.ssh ]; then  # directory not found:
   mkdir ~/.ssh
fi 
cd ~/.ssh

if [   -f ~/.ssh/"${SSH_KEY_FILE_NAME}" ]; then  # directory not found:
   rm -rf ~/.ssh/"${SSH_KEY_FILE_NAME}"
fi 

# Generate SSH key pair using built-in Linux ssh-keygen program in folder
# /home/wilson/.ssh/"${SSH_KEY_FILE_NAME}"  # (instead of file id_rsa)
# SSH keys are used to securely authenticate with a Linux VM
# This is somewhat optional, as the Azure CLI can generate keys for you
ssh-keygen -t rsa -b 2048 -f "${SSH_KEY_FILE_NAME}" -N ""
   # -N ""  makes the command not prompt for manual input.

# View the public part of your SSH key pair:
# From the CLI, you don't really need this. But if you use the Azure portal or
# Resource Manager templates (which we look at in chapter 6), you need to
# provide this public key
ls -al ~/.ssh/"${SSH_KEY_FILE_NAME}"*

echo ">>> Create a Linux VM: ${MY_VM_NAME}"
# You specify the resoure group from the previous step, then provide a name.
# This VM uses Ubuntu LTS as the VM image, and creates a user name `azuremol`
# The `--generate-ssh-keys` checks for keys you may have created earlier. If
# SSH keys are found, they are used. Otherwise, they are created for you:
az vm create \
    --name "${MY_VM_NAME}" \
    --image UbuntuLTS \
    --admin-username "${MY_ADMIN_USER_NAME}" \
    --generate-ssh-keys \
    --resource-group "${MY_RG}"

echo ">>> Obtain the public IP address of your VM. Enter the name of your resource group and VM if you changed them:"
publicIp=$(az vm show \
    --name "${MY_VM_NAME}" \
    --show-details \
    --query publicIps \
    --output tsv \
    --resource-group "${MY_RG}" )

# TODO: if publicIp is blank, stop

# SSH to your VM with the username and public IP address for your VM
#ssh "${MY_ADMIN_USER_NAME}"@$publicIp 'uname -a; sudo apt update && sudo apt install -y lamp-server^; exit'
   # uname -a  # Display information to verify entry in the Linux machine:
   # Once logged in to your VM, install the LAMP web stack with apt-get
   # sudo apt update && sudo apt install -y lamp-server^

echo ">>> Open port 80 to your webserver (not HTTPS) while testing:"
az vm open-port --name "${MY_VM_NAME}" --port 80 --resource-group "${MY_RG}"
# TODO: Enable TLS for port 443?

# Now you can access the basic website in your web browser
echo ">>> To see your web server in action, enter the public IP address in to your web browser: http://$publicIp"

# In Portal, list Virtual Machines at https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Compute%2FVirtualMachines

# More VM CLI commands are at https://docs.microsoft.com/en-us/azure/virtual-machines/linux/cli-manage



echo ">>> Create a VM:"
az vm create \
    --name molvm \
    --image ubuntults \
    --admin-username "${MY_ADMIN_USER_NAME}" \
    --generate-ssh-keys \
    --resource-group "${MY_RG}"

echo ">>> List VMs:"
az vm list --query '[].{name:name,os:storageProfile.osDisk.osType}'

echo ">>> Define the scope for upcoming Managed Service Identity tasks:"
# The scope is set to the resource group of the VM. This scope limits what
# access is granted to the identity
scope=$(az group show --query id --output tsv) \
    --resource-group "${MY_RG}"

echo ">>> Create a Managed Service Identity:"
# The VM is assigned an identity, scoped to its resource group. The ID of this
# identity, the systemAssignedIdentity, is then stored as a variable for use
# in remaining commands
read systemAssignedIdentity <<< $(az vm identity assign \
    --name molvm \
    --role reader \
    --scope $scope \
    --query systemAssignedIdentity \
    --output tsv) \
    --resource-group "${MY_RG}"

echo ">>> List the service principal name of the identity:"
# This identity is stored in Azure Active Directory and is used to actually
# assign permissions on the Key Vault. The VM's identity is queried within
# Azure Active directory, then the SPN is assigned to a variable
spn=$(az ad sp list \
    --query "[?contains(objectId, '$systemAssignedIdentity')].servicePrincipalNames[0]" \
    --output tsv) 

echo ">>> Update permissions on Key Vault:"
# Add the VM's identity, based on the Azure Active Directory SPN. The identity
# is granted permissions to get secrets from the vault.
az keyvault set-policy \
    --name $MY_KEYVAULT_NAME \
    --secret-permissions get \
    --spn $spn

echo ">>> Apply the Custom Script Extension:"
# The Custom Script Extension runs on the VM to execute a command that obtains
# the secret from Key Vault using the Instance Metadata Service, then uses the
# key to perform an unattended install of MySQL Server that automatically
# provides a password
az vm extension set \
    --publisher Microsoft.Azure.Extensions \
    --version 2.0 \
    --name CustomScript \
    --vm-name molvm \
    --settings '{"fileUris":["https://raw.githubusercontent.com/fouldsy/azure-mol-samples-2nd-ed/master/15/install_mysql_server.sh"]}' \
    --protected-settings '{"commandToExecute":"sh install_mysql_server.sh $MY_KEYVAULT_NAME"}' \
    --resource-group "${MY_RG}"

# TODO: Replace reference to fouldsy install_mysql_server.sh with our own vm image.

