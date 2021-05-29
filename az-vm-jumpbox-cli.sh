#!/bin/bash

# az-vm-jumpbox-cli.sh
# This script was adapted from https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/05/azure_cli_sample.sh
# released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
# explained in chapter 5 of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
# Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi


# Create a resource group
az group create --name azuremolchapter5 --location eastus

# Create a virtual network and subnet
# The virtual network and subnet both create regular IP ranges assigned
# to them, just like an on-premises network
az network vnet create \
    --name vnetmol \
    --address-prefix 10.0.0.0/16 \
    --subnet-name websubnet \
    --subnet-prefix 10.0.1.0/24 \
    --resource-group "${MY_RB}"

# Define a unique DNS name
dnsName=azuremol$RANDOM

# Create a public IP address
# This public IP address assigned gets assigned to a web server VM in a
# following step. We also assigned the DNS prefix of `webmol`
az network public-ip create \
    --name webpublicip \
    --dns-name $dnsName \
    --resource-group "${MY_RB}"

# Create a virtual network adapter
# All VMs need a virtual network interace card (vNIC) that connects them to a
# virtual network subnet. We assign the public IP address created in the previos
# step, along with the a static internal IP address of 10.0.1.4
az network nic create \
    --name webvnic \
    --vnet-name vnetmol \
    --subnet websubnet \
    --public-ip-address webpublicip \
    --private-ip-address 10.0.1.4 \
    --resource-group "${MY_RB}"

# Create network security group
# A network security group secures and filters both inbound + outbound virtual
# network traffic
az network nsg create \
    --name webnsg \
    --resource-group "${MY_RB}"

# Associate the network security group with your virtual network
# Network security groups can be assigned to a virtual network subnet, as we do
# here, or to an individual vNIC
az network vnet subnet update \
    --vnet-name vnetmol \
    --name websubnet \
    --network-security-group webnsg \
    --resource-group "${MY_RB}"

# Add a network security group rule to allow port 80
# Rules can be applied to inbound or outbound traffic, to a specific protocol or
# port, and for certain IP address ranges or port ranges
az network nsg rule create \
    --nsg-name webnsg \
    --name allowhttp \
    --access allow \
    --protocol tcp \
    --direction inbound \
    --priority 100 \
    --source-address-prefix "*" \
    --source-port-range "*" \
    --destination-address-prefix "*" \
    --destination-port-range 80 \
    --resource-group "${MY_RB}"

# Create an additional network security group for remote access
az network nsg create \
    --name remotensg \
    --resource-group "${MY_RB}"

# Create an additional network security group rule to allow SSH connections
# Here, we don't specify the address prefixes, direction, or destinations, as the
# Azure CLI can use smart defaults to populate these for us
az network nsg rule create \
    --nsg-name remotensg \
    --name allowssh \
    --protocol tcp \
    --priority 100 \
    --destination-port-range 22 \
    --access allow \
    --resource-group "${MY_RB}"

# Create an additional virtual network subnet and associate our remote network
# security group. This is a little different to the previous steps where we
# associated a network security group with a virtual network subnet.
az network vnet subnet create \
    --vnet-name vnetmol \
    --name remotesubnet \
    --address-prefix 10.0.2.0/24 \
    --network-security-group remotensg \
    --resource-group "${MY_RB}"

# Create a VM that will act as a web server
# Attach the virtual NIC created in the previous steps
az vm create \
    --name webvm \
    --nics webvnic \
    --image ubuntults \
    --size Standard_B1ms \
    --admin-username azuremol \
    --generate-ssh-keys \
    --resource-group "${MY_RB}"

# Create a VM that will act as our remote connection VM
# Connect the VM to the virtual network subnet for remote connectivity
az vm create \
    --name remotevm \
    --vnet-name vnetmol \
    --subnet remotesubnet \
    --nsg remotensg \
    --public-ip-address remotepublicip \
    --image ubuntults \
    --size Standard_B1ms \
    --admin-username azuremol \
    --generate-ssh-keys \
    --resource-group "${MY_RB}"

# Enable the SSH agent and add our SSH keys
eval $(ssh-agent)
ssh-add

# Obtain the public IP address of the web server VM
remotevmIp=$(az vm show \
    --name remotevm \
    --show-details \
    --query publicIps \
    --output tsv) \
    --resource-group "${MY_RB}"

# SSH to the remote VM, passing through our SSH keys
ssh -A azuremol@$remotevmIp
