#!/usr/bin/env bash

# ./az-providers-setup.sh
# Implements https://github.com/MicrosoftLearning/AI-102-AIEngineer/blob/master/Instructions/00-update-resource-providers.md

set -o errexit

# NOTE: This is not for an individual Region/Location.


# There is no additional charge for this.
# Among resource providers listed at https://docs.microsoft.com/en-us/azure/azure-resource-manager/management/azure-services-resource-providers
# To avoid error "The subscription is not registered to use namespace 'Microsoft.KeyVault'"
# when you try to create a new key vault. This is a one-time operation for each subscription.
# CLI DOC: https://docs.microsoft.com/en-US/cli/azure/provider#az_provider_register
function Register_AzProvider {
   AzProvider=$1
   RESPONSE=$( az provider show --namespace $AzProvider  --query registrationState -o tsv )
   if [ $RESPONSE == "Registered" ]; then
      echo ">>> $AzProvider already Registered."
   else
      az provider register -n $AzProvider
      echo ">>> Provider \"$AzProvider\" registered for subscription."
   fi
}  # Alphabetical order:
Register_AzProvider "Microsoft.AlertsManagement"
Register_AzProvider "Microsoft.BotService"
Register_AzProvider "Microsoft.ChangeAnalysis"
Register_AzProvider "Microsoft.CognitiveServices"
Register_AzProvider "Microsoft.Compute"
Register_AzProvider "Microsoft.ContainerInstance"
Register_AzProvider "Microsoft.ContainerRegistry"
Register_AzProvider "Microsoft.Devices"
Register_AzProvider "Microsoft.EventGrid"
Register_AzProvider "Microsoft.EventHub"
Register_AzProvider "Microsoft.Insights"
Register_AzProvider "Microsoft.KeyVault"
Register_AzProvider "Microsoft.Notebooks"
Register_AzProvider "Microsoft.MachineLearningServices"
Register_AzProvider "Microsoft.ManagedIdentity"
Register_AzProvider "Microsoft.Search"
Register_AzProvider "Microsoft.Storage"
Register_AzProvider "Microsoft.Web"

echo ">>> -vv List providers available for registration. "
az provider list --query "[].namespace"