#!/bin/bash

# ./iot/az-iot-cli.sh
# This is referenced in my hands-on tutorial IoT at https://wilsonmar.github.io/azure-iot
# This script was adapted from several samples:
#    https://github.com/Azure-Samples/web-apps-node-iot-hub-data-visualization
#    https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/20/azure_cli_sample.sh
#       released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
#       and chapter 20 of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
#       Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition
# This script was designed to be idempotent, where each time files are removed from the previous run.

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi


echo ">>> Set subscription \"$MY_SUBSCRIPTION_ID\" "
az account set --subscription "${MY_SUBSCRIPTION_ID}"


if [ $(az group exists --name "${MY_RG}") = true ]; then
   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
   time az group delete --resource-group "${MY_RG}" --yes
fi
echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   time az group create --name "${MY_RG}" --location "${MY_LOC}"


# https://docs.microsoft.com/en-us/cli/azure/azure-cli-reference-for-iot

echo ">>> Add Azure IoT CLI extension \"azure-iot\" "
# This CLI extension provides some additional functionality to the core Azure
# CLI 2.0, and can be updated out-of-band from the core tooling itself.
time az extension add --name azure-iot
   # formerly azure-cli-iot-ext
   # https://docs.microsoft.com/en-us/cli/azure/azure-cli-extensions-overview
   # echo ">>> List available Azure IoT CLI extensions "
   # az extension list-available -o table
# RESPONSE: Extension 'azure-iot' is already installed.


echo ">>> Create an IoT Hub"
# A Hub provides you with a way to connect, provision, and secure IoT devices
# and allow other services and applications to use the IoT devices. 
time az iot hub create \
    --name "${MY_IOT_HUB_NAME}" \
    --sku f1 \
    --partition-count 2 \
    --resource-group "${MY_RG}" --debug
# "f1" is the free tier, which allows up to 8,000 messages per day.

## BLOCKED HERE:
## --debug got msrest.serialization: container_uri is not a known attribute of class <class 'azure.mgmt.iothub.v2020_03_01.models._models_py3.StorageEndpointProperties'> and will be ignored
## IotHub name 'hubahuba' not available. If you contact a support representative please include this correlation identifier: f20061af-4715-4189-a83c-ecabc8d16f81, timestamp: 2021-05-01 23:15:59Z, errorcode: IH409004

echo ">>> List IoT Hubs created:"
az iot hub list   # -o table

exit


echo ">>> List IoT Hub"
az iot hub list -o table


echo ">>> Create an IoT identity"
# An identity is used by an IoT device to connect to the Azure IoT Hub. Each
# device has a unique identity. This identity can be used for a simulated, or
# real Raspberry Pi device.
time az iot hub device-identity create \
    --hub-name "${MY_IOT_HUB_NAME}" \
    --device-id raspberrypi


echo ">>> Show the IoT device connection string"
# This connection string can be provided to your IoT device to allow it to
# connect to the Azure IoT Hub.
time az iot hub device-identity show-connection-string \
    --hub-name "${MY_IOT_HUB_NAME}" \
    --device-id raspberrypi \
    --output tsv


echo ">>> Show the status of the IoT device and message quota"
# As your device connects and transmits messages, the change in quota can be
# viewed.
time az iot hub show-quota-metrics --name "${MY_IOT_HUB_NAME}"


echo ">>> Create an App Service plan"
# An App Service plan defines the location and available features
# These features include deployment slots, traffic routing options, and
# security options.
time az appservice plan create \
    --resource-group "${MY_RG}" \
    --name "${MY_IOT_HUB_NAME}" \
    --sku f1


echo ">>> Define variable for unique Web App name"
# As we create DNS for the Web App, the DNS name must be unique. By adding some
# randomization to the resource name, the commands can run without user 
# intervention or errors. Feel free to provide your own varation of unique 
# name for use throughout the script.
webAppName="${MY_IOT_HUB_NAME}"$RANDOM


echo ">>> Create WebApp \"$webAppName\" in the App Service plan \"${MY_IOT_HUB_NAME}\" "
# enabled for local Git deployments
# The Web App is what actually runs your web site, lets you create deployment
# slots, stream logs, etc.
time az webapp create \
    --resource-group "${MY_RG}" \
    --plan "${MY_IOT_HUB_NAME}" \
    --name $webAppName \
    --deployment-local-git


echo ">>> Create Azure IoT Hub consumer group"
# A consumer group allows you to define messages that are streamed to available
# connected services and applications. By default, messages received from IoT
# device are placed on a shared events endpoint.
time az iot hub consumer-group create \
    --hub-name "${MY_IOT_HUB_NAME}" \
    --name "${MY_IOT_HUB_GROUP}"


echo ">>> Set a Web App application setting for the consumer group"
# Application settings let you define variables that are available to your Web
# Apps. This allows you to dynamically adjust names, connection strings, etc.
# without needing to update your code.
time az webapp config appsettings set \
    --resource-group "${MY_RG}" \
    --name $webAppName \
    --settings consumergroup="${MY_IOT_HUB_GROUP}"


echo ">>> Obtain the IoT connection string "
# for use with Web App connection
iotconnectionstring=$(az iot hub show-connection-string \
                        --hub-name "${MY_IOT_HUB_NAME}" \
                        --output tsv)


echo ">>> Create another Web App application setting"
# for the connection string
# This setting allows your Web App to connect to Azure IoT Hub without
# needing to update your code.
time az webapp config appsettings set \
    --resource-group "${MY_RG}" \
    --name $webAppName \
    --settings iot=$iotconnectionstring


echo ">>> Enable websockets on the Web App"
# Websockets allows your app to dynamically update the web browser when a user
# is connected to displayed the latest information from your IoT device
time az webapp config set \
    --resource-group "${MY_RG}" \
    --name $webAppName \
    --web-sockets-enabled


echo ">>> Create a Git user accout and set credentials"
# Deployment users are used to authenticate with the App Service when you
# upload your web application to Azure.
time az webapp deployment user set \
    --user-name "${MY_IOT_HUB_NAME}" \
    --password M0lPassword!
# TODO: Use Azure Vault instead of static secret text.


echo ">>> Clone the Azure sample repo, if it's not already there"
# TODO:
cd ~ 
cd clouddrive
rm -rf "${MY_PROJECT_FOLDER}"
git clone https://github.com/wilsonmar/azure-your-way.git  "${MY_PROJECT_FOLDER}"  --depth 1 
cd "${MY_PROJECT_FOLDER}"
pwd


echo ">>> Initialize the directory for use with Git, add the sample files, and commit"
git init && git add . && git commit -m “Pizza”


echo ">>> Add Web App as a remote destination in Git"
git remote add "${MY_IOT_HUB_GROUP}"iot \
    $( az webapp deployment source config-local-git \
        --resource-group "${MY_RG}" \
        --name $webAppName -o tsv 
    )


echo ">>> Push, or upload, the sample app to your Web App"
git push "${MY_IOT_HUB_GROUP}"iot master


echo ">>> Get the hostname of the Web App"
# This hostname is set to the variable hostName and output to the screen in the next command.
hostName=$( az webapp show --resource-group "${MY_RG}" --name $webAppName \
   --query defaultHostName -o tsv)

# Now you can access the Web App in your web browser
echo "To see your IoT-connected Web App in action, enter the following address in to your web browser:" $hostName
