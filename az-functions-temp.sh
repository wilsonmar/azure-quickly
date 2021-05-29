#!/usr/bin/env bash

# ./az-functions-temp.sh
# This script was adapted from https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/21/azure_cli_sample.sh
# released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
# and chapter 21 of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
# Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition
#
# There are quite a few components here that aren't available in the Azure CLI
# The complete examples from chapter 21 fill in the gaps with use of the Azure portal GUI.
# As such, this is not a complete example script that provides a functional end
# result at the end of the script.

set -o errexit

echo ">>> Create a Function App:"
# Instead of Port GUI https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2Fsites/kind/functionapp
# PORTAL VIDEO DEMO: https://app.pluralsight.com/course-player?clipId=2308c37d-0804-4834-86f3-2f38937170c2
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest#az_functionapp_create
# The Function App is set up to be manually connected to a sample app in GitHub
az functionapp create \
    --name "${FUNC_APP_NAME}" \
    --storage-account "${MY_STORAGE_ACCT}" \
    --consumption-plan-location "${MY_LOC}" \
    --deployment-source-url https://raw.githubusercontent.com/wilson-mar/azure-quickly/main/analyzeTemperature.js \
    --resource-group "${MY_RG}"
  # -p $MY_PLAN  # Region, SKU Dynamic, Operating System: Windows
     # Consumption plan is used, which means you are only charged based on memory usage while your app is running. 
  # Publish: Code (not Docker Container)
  # Runtime Stack: .NET Core
  # Version: 3.1
    

export MY_FUNC_WORKER_RUNTIME="dotnet"  # "dotnet", et.

func init --worker-runtime "${MY_FUNC_WORKER_RUNTIME}" --force

# Define a unique name for the Service Bus namespace
MY_SVC_BUS_NAMESPACE=$MY_SVC_BUS_NAME$RANDOM
echo "MY_SVC_BUS_NAMESPACE=$MY_SVC_BUS_NAMESPACE"

echo ">>> Create a Service Bus namespace:"
# This namespace is used to then create a queue that allows messages to be
# transmitted between your Azure IoT Hub and applications such as Logic Apps
# and Function Apps
az servicebus namespace create --name "${MY_SVC_BUS_NAMESPACE}" \
    --resource-group "${MY_RG}"

echo ">>> Create a Service Bus queue:"
# This queue is used to connect Azure IoT Hub with your serverless applications
# to pass messages back and forth
az servicebus queue create \
    --name "${MY_SVC_BUS_NAME}" \
    --namespace-name "${MY_SVC_BUS_NAMESPACE}" \
    --resource-group "${MY_RG}"
    
echo ">>> Storage account: $MY_STORAGE_ACCT$RANDOM"

echo ">>> Create an Azure Storage account:"
# The Function App requires a Storage account
az storage account create \
   --name "${MY_STORAGE_ACCT}" \
   --sku standard_lrs \
   --resource-group "${MY_RG}"
    
echo ">>> Define a unique name for the Function App:"
FUNC_APP_NAME="$MY_SVC_BUS_NAME$RANDOM"

    
