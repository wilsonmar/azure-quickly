#!/usr/bin/env bash

# ./az-cosmo-init.sh
# Described in https://wilsonmar.github.io/azure-storage
# in https://github.com/wilsonmar/azure-quickly
# Data based on https://microsoftlearning.github.io/AZ-204-DevelopingSolutionsforMicrosoftAzure/Instructions/Labs/AZ-204_01_lab.html
# 1. Prepare your CLI Bash environment according to https://wilsonmar.github.io/azure-quickly
#    which references repo https://github.com/wilsonmar/azure-quickly.
# 2. In your clouddrive folder edit your preferences in ../setmem.sh (MY_RG, MY_LOC, etc.)
# 3. Copy and paste this to the Bash command line:
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-cosmo-init.sh)" -v -i
# MY_COSMO_ACCT_DELETE=true
# See https://docs.microsoft.com/en-us/azure/cosmos-db/cli-samples
# For https://microsoftlearning.github.io/AZ-204-DevelopingSolutionsforMicrosoftAzure/Instructions/Labs/AZ-204_04_lab.html

set -o errexit

export MY_COSMO_ACCT_DELETE=true   # delete right after creation in same script.

if [[ -z "${MY_RG+x}" ]]; then
   source ../setmem.sh   # in folder above this.
fi

if [[ -z "${MY_SUBSCRIPTION_ID}" ]]; then
   echo ">>> MY_SUBSCRIPTION_ID \"${MY_SUBSCRIPTION_ID}\" not defined. Aborting. "
   exit
fi


if [ $( az group exists --name "${MY_RG}" ) == true ]; then
   echo ">>> Resource Group \"$MY_RG\" exists ..."
#   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
#   time az group delete --resource-group "${MY_RG}" --yes
else
   echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   az group create --name "${MY_RG}" --location "${MY_LOC}" -o none
fi

   export MY_COSMO_ACCT="cosmo$RANDOM"  # lower case and less than 44 chars
   export MY_COSMO_REGION0="West US 2"
   export MY_COSMO_REGION1="East US 2"

RESPONSE=$( az cosmosdb check-name-exists --name "$MY_COSMO_ACCT" )
if [ "$RESPONSE" == true ]; then
   echo ">>> Check name exists \"$MY_COSMO_ACCT\" "
else
   # CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/cosmosdb?view=azure-cli-latest#az_cosmosdb_create
   echo ">>> az cosmosdb create \"$MY_COSMO_ACCT\" in \"$MY_COSMO_REGION0\" and \"$MY_COSMO_REGION1\" "
   time az cosmosdb create \
    -n "$MY_COSMO_ACCT" \
    --default-consistency-level Session \
    --enable-free-tier true \
    --max-interval "300" \
    --max-staleness-prefix "10000" \
    --locations regionName='uswest2' failoverPriority=0 isZoneRedundant=False \
    --locations regionName='useast2' failoverPriority=1 isZoneRedundant=False \
    -g "$MY_RG"
#   --enable-multiple-write-locations \
#   --network-acl-bypass AzureServices 
#   --network-acl-bypass-resource-ids /subscriptions/subId/resourceGroups/rgName/providers/Microsoft.Synapse/workspaces/wsName
    # The first regionName is the Write region. 
    # This took 3.11m
 fi 

echo ">>> Manage Azure Cosmos DB collections."
# az cosmosdb collection 	...

# Add or remove regions
# Enable multi-region writes
# Set regional failover priority
# Enable automatic failover
# Trigger manual failover
# List account keys
# List read-only account keys
# List connection strings
# Regenerate account key


#Manage Azure Cosmos DB databases.
#az cosmosdb database 	

# Manage Azure Cosmos DB managed service identities
#az cosmodb identity
# keys


# az cosmodb cassandra ...
# az cosmodb gremlin  # graph db
# mongodb
# sql
# table

# Access API:
# https://docs.microsoft.com/en-us/azure/cosmos-db/sql-query-getting-started#:~:text=In%20your%20SQL%20API%20Cosmos%20DB%20account%2C%20open,data%20structures%20browser%2C%20to%20find%20and%20open%20it

# Cosmodb containers = tables, each with RUs max. of its own.

if [ "$MY_COSMO_ACCT_DELETE" = true ]; then
   echo ">>> az cosmosdb delete \"$MY_COSMO_ACCT\" "
   time az cosmosdb delete --name "$MY_COSMO_ACCT" \
      --resource-group "$MY_RG"  --yes
fi