#!/bin/bash

# az-static-webapp-init.sh at https://github.com/wilsonmar/azure-quickly
# Based on https://docs.microsoft.com/en-us/azure/static-web-apps/get-started-cli?tabs=angular

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setmem.sh   # in folder above this.
fi

# Install Homebrew, Git

# Generate repo from sample 
#    https://github.com/staticwebdev/vanilla-basic/generate
# or https://github.com/staticwebdev/react-basic/generate
# or https://github.com/staticwebdev/vue-basic/generate
# to "https://github.com/${MY_GITHUB_ACCT}/${MY_GITHUB_REPO}" 

echo ">>> Create Azure Web App ${MY_GITHUB_REPO}\" "
az staticwebapp create \
    -n "${MY_STATIC_APP_NAME}" \
    -s "https://github.com/${MY_GITHUB_ACCT}/${MY_GITHUB_REPO}" \
    -b main \
    --token "${MY_GITHUB_PAT_SECRET}" \
    --app-artifact-location "build" \
    -l "${MY_LOC}" \
    -g "${MY_RG}" 
#    --app-artifact-location "build"  # "build" for React, "dist" for Vue, "dist/angular-basic" for Angular
   # This would auto-pick a URL name such as "https://thankful-group.azurestaticapps.net"

# Manually view the app in Azure Portal to get the URL.
# View the website 


function this_staticwebapp_delete() {
    az staticwebapp delete \
       --name "${MY_STATIC_APP_NAME}" \
       --resource-group "${MY_RG}"
}
# this_staticwebapp_delete
