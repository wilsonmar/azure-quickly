#!/usr/bin/env bash

# This is ./az-vm-lb2.sh within https://github.com/wilsonmar/azure-quickly
# Described in https://wilsonmar.github.io/azure-networking
# Created to automate https://microsoftlearning.github.io/AZ-303-Microsoft-Azure-Architect-Technologies/Instructions/Labs/Module_05_Lab.html#exercise-2-implement-and-analyze-highly-available-azure-vm-deployments-using-availability-zones-and-azure-load-balancer-standard
# 1. Prepare your CLI Bash environment according to https://wilsonmar.github.io/azure-quickly
#    which references repo https://github.com/wilsonmar/azure-quickly.
# 2. In your clouddrive folder edit your preferences in ../setmem.sh (MY_RG, MY_LOC, etc.)
# 3. Copy and paste this to the Bash command line:
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-vm-lb2.sh)" -v -i

source ./az-all-start.sh  # to setup environment variables and utility functions

set -o errexit

#export MY_REPO_URL="https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies"
#export MY_REPO_FOLDER="AZ303"
# To be specified in script call parms:"
export RMV_RG_BEFORE=true        # parm -RRGb
#export RMV_RG_AT_END=false       # parm -RRGe
#export RMV_GITHUB_BEFORE=false   # parm -RGb
#export RMV_GITHUB_AT_END=false   # parm -RGe
#export DO_GITHUB_CLONE=true      # parm -c

# TODO: Get all public frontend IP addresses for the load balancer.
# publicIpIds=$( az network lb show -g ${resourceGroupName} -n ${lbName} --query "frontendIpConfigurations[].publicIpAddress.id" --out tsv)


# Network Watcher Concepts Overview: https://docs.microsoft.com/en-us/azure/network-watcher/network-watcher-monitoring-overview
echo ">>> network watcher configure $MY_LOC in RG $MY_RG "
# DOCS: https://docs.microsoft.com/en-us/azure/network-watcher/network-watcher-create
# CLI:  https://docs.microsoft.com/en-US/cli/azure/network/watcher?view=azure-cli-latest#az_network_watcher_configure
# Portal  All Services > Networking > Network Watcher.
# TODO: Check if already exists
   az network watcher configure --enabled true \
      --locations "$MY_LOC" -o table \
      -g "$MY_RG"
   # Location    Name            ProvisioningState    ResourceGroup
   # ----------  --------------  -------------------  ---------------
   # westus      westus-watcher  Succeeded            wow


echo ">>> Navigate top "
if [ -d "../clouddrive" ]; then
   cd 
else
   if [ -d "../gmail_acct" ]; then
      cd
   fi
   echo ">>> not in clouddrive "
fi
pwd


function thisfile_DO_GITHUB_CLONE() {
   echo ">>> Cloning $MY_REPO_FOLDER "
   time git clone "$MY_REPO_URL" "$MY_REPO_FOLDER" --depth 1 
   cd "$MY_REPO_FOLDER"
   pwd
}
if [ -d "$MY_REPO_FOLDER" ]; then
   if [ "${RMV_GITHUB_BEFORE}" = true ]; then  # param -d 
      echo ">>> Removing folder $MY_REPO_FOLDER "
      time rm -rf "$MY_REPO_FOLDER"
      thisfile_DO_GITHUB_CLONE
   else
      echo ">>> Found folder $MY_REPO_FOLDER "
      cd "$MY_REPO_FOLDER"
      git config pull.rebase false
      git pull
   fi 
else   #  "$MY_REPO_FOLDER" not found:
   if [ "${DO_GITHUB_CLONE}" = true ]; then  # param -c
      thisfile_DO_GITHUB_CLONE
   # else leave no trace.
   fi
fi


export MY_TEMPLATE_PATH="AllFiles/Labs/05"
echo ">>> Before \"$MY_TEMPLATE_PATH\" at $PWD "
cd "$MY_TEMPLATE_PATH"
echo ">>> Now at $PWD"
ls


export MY_DEPLOY_SUB_FILE="azuredeploy30305subb.json"
export MY_LB_TEMPLATE="azuredeploy30305rgb.json"
export MY_LB_PARM_FILE="azuredeploy30305rgb.parameters.json"
export MY_LB_NAME="az30305b-lb"  # inside parameters file 

function thisfile_confirm_deployment_sub() {
   RESPONSE=$( az deployment sub list --query "[?name == '$MY_RG']" )
   echo ">>> $RESPONSE"
}
thisfile_confirm_deployment_sub  # Check if deployment exists
if [[ "[]" == *"${RESPONSE}"* ]]; then
   if [ ! -f "$MY_DEPLOY_SUB_FILE" ]; then
      echo ">>> Template file $MY_DEPLOY_SUB_FILE not found. Exiting."
      exit
   fi

   echo ">>> az deployment sub create $MY_RG in \"$MY_LOC\" using template $MY_DEPLOY_SUB_FILE "
   # https://docs.microsoft.com/en-us/cli/azure/deployment/sub?view=azure-cli-latest#az_deployment_sub_list
   time az deployment sub create \
      --location "$MY_LOC" \
      --template-file "$MY_DEPLOY_SUB_FILE" \
      --parameters rgName="$MY_RG" rgLocation="$MY_LOC"
fi
thisfile_confirm_deployment_sub
if [[ "[]" == *"${RESPONSE}"* ]]; then
   echo ">>> Deployment sub not identified. Exiting "
   exit
fi


if [[ -z "${MY_LB_PARM_FILE}" ]]; then
   echo ">>> MY_LB_PARM_FILE \"$MY_LB_PARM_FILE\" not defined. "
fi

function thisfile_confirm_deployment_group() {
   RESPONSE=$( az deployment group list --query "[?name == '$MY_RG']" )
   echo ">>> $RESPONSE"
}
thisfile_confirm_deployment_group  # Check if deployment exists
if [[ "[]" == *"${RESPONSE}"* ]]; then
   echo ">>> az deployment group create based on \"$MY_LB_TEMPLATE\" & parms \"$MY_LB_PARM_FILE\" "
   pwd
   # with its backend pool "
   # consisting of a pair of Azure VMs hosting Windows Server 2019 Datacenter Core 
   # into the same availability set: 
   # https://docs.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest
   time az deployment group create \
      --template-file "$MY_LB_TEMPLATE" \
      --parameters "$MY_LB_PARM_FILE" \
      --resource-group "$MY_RG" 
   #    --mode incremental \
   #    --verbose \
   #    --parameters "{ `"location`": { `"value`": `"$location`" },`"projectPrefix`": { `"value`": `"$prefix`" } }"
    #time 5m
fi
thisfile_confirm_deployment_group
if [[ "[]" == *"${RESPONSE}"* ]]; then
   echo ">>> Deployment group not identified. Exiting "
   exit
fi

# As in Portal, LB_PUBLIC_IP is Load Balancer -> Overview -> Public IP address:
#$pipId = $(az network lb show --id $loadBalancer.id --query "frontendIpConfigurations | [?loadBalancingRules != null].publicIpAddress.id" -o tsv)
#$ip = (az network public-ip show --ids $pipId --query "ipAddress" -o tsv)

# Based on https://gist.github.com/twitchax/a7eb251bc69fe37ba055262f0008771a
   MY_PUBLIC_IPS=$( az network lb show -g ${MY_RG} -n "${MY_LB_NAME}" \
      --query "frontendIpConfigurations[].publicIpAddress.id" )
   echo ">>> Extracted for MY_LB_NAME \"$MY_LB_NAME\" : $MY_PUBLIC_IPS "

publicIpFqdnTuple=$(
    while read LB_PUBLIC_IP; do 
        az network public-ip show --ids "${LB_PUBLIC_IPS}" --query "{ ipAddress: ipAddress, fqdn: dnsSettings.fqdn }" --out tsv 
    done <<< "${MY_PUBLIC_IPS}" 
)
echo ">>> publicIpFqdnTuple=$publicIpFqdnTuple "
exit

# TODO: Extract Public IP address from Load Balancer 40.83.174.66 (az30305a-pip)
# In azuredeploy30305rga.json, under variables, "pipName": "az30305a-pip", 
LB_PUBLIC_IP="40.83.174.66"

echo ">>> curl LB_PUBLIC_IP=$LB_PUBLIC_IP "
for i in {1..4}; do curl "$LB_PUBLIC_IP"; done
   # RESULTS: Evidence of round-robin allocation:
   # Hello World from az30305a-vm0
   # Hello World from az30305a-vm1
   # Hello World from az30305a-vm1
   # Hello World from az30305a-vm1

# Access:
   curl -v telnet://"$LB_PUBLIC_IP":33890
   # * Rebuilt URL to: telnet://40.83.174.66:33890/
   # *   Trying 40.83.174.66...
   # * TCP_NODELAY set
   # * Connected to 40.83.174.66 (40.83.174.66) port 33890 (#0)


if [ "${DEL_RG_AT_END}" = true ]; then  # param -d 
      echo ">>> Delete Resource Group \"$MY_RG\" "
      time az group delete --resource-group "${MY_RG}" --yes "$CMD_GENERAL_PARM"
fi


echo ">>> END"
# See https://github.com/Azure/azure-quickstart-templates/tree/master/201-2-vms-loadbalancer-lbrules.