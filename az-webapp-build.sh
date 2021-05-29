#!/usr/bin/env bash

# ./az-webapp-build.sh
# in https://github.com/wilsonmar/azure-your-way
# Data based on https://microsoftlearning.github.io/AZ-204-DevelopingSolutionsforMicrosoftAzure/Instructions/Labs/AZ-204_01_lab.html
# 1. Prepare your CLI Bash environment according to https://wilsonmar.github.io/azure-your-way
#    which references repo https://github.com/wilsonmar/azure-your-way.
# 2. In your clouddrive folder edit your preferences in ../setmem.sh (MY_RG, MY_LOC, etc.)
# 3. Copy and paste this to the Bash command line:
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-your-way/master/az-webapp-build.sh)" -v -i

set -o errexit

if [[ -z "${MY_RG+x}" ]]; then
   source ../setmem.sh   # in folder above this.
fi

if [ $( az group exists --name "${MY_RG}" ) == true ]; then
   echo ">>> Resource Group \"$MY_RG\" exists ..."
#   echo ">>> Delete Resource Group \"$MY_RG\" exists before recreating ..."
#   time az group delete --resource-group "${MY_RG}" --yes
else
   echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   az group create --name "${MY_RG}" --location "${MY_LOC}" -o none
fi

# Get Storage account?

echo ">>> webapp list \"$MY_WEBAPP_NAME\" " 
az webapp list --query "[?starts_with(name, '$MY_WEBAPP_NAME')]" -o table \
   --resource-group "${MY_RG}" 
# Name        Location    State    ResourceGroup    DefaultHostName               AppServicePlan
#----------  ----------  -------  ---------------  ----------------------------  ------------------------
#imgapi1113  East US     Running  ManagedPlatform  imgapi1113.azurewebsites.net  ASP-ManagedPlatform-8749

echo ">>> python --version "
   # Python 3.7.9"


export MY_WEBAPP_DATA_REPO="AZ-204-DevelopingSolutionsforMicrosoftAzure"
export MY_WEBAPP_DATA_URL="https://github.com/MicrosoftLearning/AZ-204-DevelopingSolutionsforMicrosoftAzure.git"
export MY_WEBAPP_SRC_PATH="Allfiles/Labs/01/Starter/Web"  # web.zip
export MY_WEBAPP_DATA_PATH="Allfiles/Labs/01/Starter/Images"  # *.jpg
cd ..
if [[ -d "${MY_WEBAPP_DATA_REPO}" ]]; then
   echo ">>> \"$MY_WEBAPP_DATA_REPO\" already created "
else
   echo ">>> Clone the sample data repo in \"${MY_WEBAPP_DATA_PATH}\" "
   pushd ..
   pwd
   git clone "${MY_WEBAPP_DATA_URL}" --depth 1
   # cd "${MY_WEBAPP_DATA_REPO}"
   popd  
fi
cd $MY_WEBAPP_DATA_REPO

if [[ -d "${MY_WEBAPP_SRC_PATH}" ]]; then
   cd $MY_WEBAPP_SRC_PATH
else
   echo ">>> Cannot see \"$MY_WEBAPP_SRC_PATH\" "
   exit
fi

pwd

if [[ -z ${MY_WEBAPP_NAME+x} ]]; then
   echo ">>> MY_WEBAPP_NAME variable not defined."
   exit
else
   echo ">>> Create and deploy web app ${MY_WEBAPP_NAME}.azurewebsites.net "
   az webapp up --name "${MY_WEBAPP_NAME}" --logs --launch-browser
   # --logs displays the log stream immediately after launching the webapp.
   # --launch-browser command opens the default browser to the new app. 
   # NOTE: Use the same command to redeploy the entire app again.
fi

my_webapp_instance=$( az webapp list --resource-group ManagedPlatform \
   --query "[?starts_with(name, 'imgapi')].{Name:name}" --output tsv )
if [[ -z ${my_webapp_instance+x} ]]; then
   echo ">>> webapp_instance name not defined in az webapp list "
   exit
else
   echo ">>> $my_webapp_instance"  # such as "imgapi1113"
fi

echo ">>> Deploy app $my_webapp_instance instance of \"${MY_WEBAPP_NAME}\" file \"${MY_WEBAPP_DATA_PATH}\" "
# https://docs.microsoft.com/en-us/azure/app-service/deploy-zip
   # CAUTION: There is a file size limit of 2048 MB.
if [[ -z "${MY_WEBAPP_DATA_PATH}" ]]; then
   echo ">>> ${MY_WEBAPP_DATA_PATH} file not found."
   exit
else
   az webapp deployment source config-zip --src "${MY_WEBAPP_SRC_PATH}" \
      --src clouddrive/"${MY_WEBAPP_DATA_PATH}"
      --name "${MY_WEBAPP_NAME}" \
      --resource-group "${MY_RG}" 
fi

# Change your current directory to the Allfiles (F):\Allfiles\Labs\01\Starter\Web 
   #   directory that contains the lab files:

echo ">>> Access the imgweb[yourname] web app that you created earlier "
# Open the imgweb[yourname] web app in your browser."
# From the Contoso Photo Gallery webpage, find the Upload a new image section, and then 
# upload the bahnmi.jpg file in the Allfiles (F):\Allfiles\Labs\01\Starter\Images folder on your lab machine.

# 1. Click the Upload button to upload the image to Azure.

# Observe that the list of gallery images has updated with your new image.
# You might need to refresh your browser window to retrieve the new image.


