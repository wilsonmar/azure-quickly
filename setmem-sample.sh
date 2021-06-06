#!/usr/bin/env bash

# ./setmem.sh is based on https://github.com/wilsonmar/azure-quickly/blob/main/setmem-sample.sh
# copied above the azure-quickly repo folder by az-setup-cli.sh
# CAUTION: DO NOT SAVE THIS FILE IN GITHUB
# TODO: Save secrets in KeyVault (to rotate keys) and retrieve from there.

   export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"            # From Tenant Properties blade
   export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
   export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"   # From Subscriptions blade
#
   export ARM_CLIENT_ID="..."
   export ARM_CLIENT_SECRET="..."
   export ARM_SUBSCRIPTION_ID="$MY_SUBSCRIPTION_ID"
   export ARM_TENANT_ID="$TENANT_ID"
   export ARM_USE_MSI=true   # Managed Identities:
   export ARM_SUBSCRIPTION_ID="$MY_SUBSCRIPTION_ID"
   export ARM_TENANT_ID="$TENANT_ID"
#
   export MY_REPO="azure-quickly"           # repo name in my GitHub.com/wilsonmar
  #export MY_SCRIPT="az-???-cli.sh"          # the script being called
   export MY_SCRIPT_VERSION="0.1.4"          # to be sure that you're getting the right one.
#
   export MY_LOC="westus"               # aka region
   export MY_ENV="dev"                  # "dev", "qa", "stage", "prod"
   export MY_COST_CENTER=""             # Company-specific
   export MY_RG="${MY_ENV}"  # "x$( date +%y%m%dT%H%M%S )"        # example: x210131T1259 for always a new one
#
   export MY_GIT_CONTAINER="$HOME/clouddrive"      # "clouddrive" in Cloud Shell
   export MY_PROJECT_FOLDER="iot-project"
#
   export MY_ADMIN_USER_NAME="johndoe" 
        # MY_ADMIN_USER_NAME cannot contain upper case character A-Z, special characters
        #  \/"[]:|<>+=;,?*@#()! or start with $ or -
#
   export MY_COSMO_ACCT="cosmo$RANDOM"  # lower case and less than 44 chars
   export MY_COSMO_REGION0="West US 2"
   export MY_COSMO_REGION1="East US 2"
#
   export COG_SERVICE_NAME="${MY_RG}cog$RANDOM"  # generate globally unique one
      # "$COG_SERVICE_NAME/text/analytics/v3.0/languages?" 
   export MY_COG_PRICING_TIER="F0" # "F0" or "S0" or "Standard_F2s_v2""
 # export MY_COG_KIND="Bing.Search.v7"  # AnomalyDetector, Bing.Search.v7, etc.
     # Specified before calling
   export COG_SERVICE_ENDPOINT="https://$MY_LOC.api.cognitive.microsoft.com/"
   export COG_SERVICE_KEY=""  # obtained for COG service created.
#
   export MY_FACE_ACCT="faceme"
   export MY_FACE_KEY1="abcdef123456f4b3a9d1279ad57294802"
#
   export MY_SEARCH_STRING="How much is that dog?"
   export MY_SEARCH_SVC="How much is that dog?"
#
   export MY_WEBAPP_NAME="${MY_RG}app$RANDOM"
   export MY_ACR="jollygoodacr"    
   export MY_VM_NAME=""
   export MY_APPNAME="azuremol"         # 
   export MY_SVC_BUS_NAME="azuremol"
   export MY_MLWORKSPACE_NAME="mela"
#
if [[ -z "${MY_STORAGE_ACCT}" ]]; then  # not defined
   export MY_STORAGE_ACCT="${MY_RG}storage$RANDOM"  # One acct per day
         # LIMIT: Max. 24 lower-case char & numbers, no dashes. globally unique 
         # MY_STORAGE_ACCT.core.windows.net
fi
   export MY_STORAGE_SKU="standard_lrs"  # 
   export MY_STORAGE_TAGS=""   # env=dev"
   export MY_STORAGE_CONTAINER="wooz"
#
   export MY_COMPUTE_NAME="eat"  # several of these?
   export MY_COMPUTE_SPEC="STANDARD_D3_V2"  # Standard_NC12
#
   export MY_PLAN="${MY_RG}plan$RANDOM"    # used by Function App
   export MY_FUNC_APP_NAME="${MY_RG}funcapp$RANDOM"  # globally unique in front of .azurewebsites.net
   export MY_FUNC_APP_VER=2                # New!
   export MY_FUNC_APP_URL="https://raw.githubusercontent.com/wilsonmar/azure-quickly/main/analyzeTemperature.js"
#
   export MY_SSH_KEY_FILE_NAME="id_rsa".        # default is id_rsa.
   export MY_MANAGED_IDENTITY="${MY_RG}identity$RANDOM" # LIMIT: Max. 24 chars/nums, no dashes.
          # lower-case for global
#
   export KEY_VAULT="${MY_RG}keyvault$RANDOM"   # LIMIT: Max 24 characters.
            # globally unique "https://$KEY_VAULT.vault.azure.net/"
   export MY_KEY_NAME="databasepassword"
   export APP_ID="woohoo"
   export APP_PASSWORD="SecureP@ssw0rd"     # for saving into Key Vault
   export MY_KEY_CONTENT_TYPE="Database password"
#
   export MY_DOCKERHUB_ACCT="iainfoulds"     # globally unique in Docker.io (DockerHub)
   export MY_CONTAINER="azuremol"            # within DockerHub
#
   export MY_IOT_HUB_NAME="hubahuba"
   export MY_IOT_HUB_GROUP="hubgroupie"
#
   export MY_REPO_URL="https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies"
   export MY_REPO_FOLDER="AZ303"
   export MY_TEMPLATE_PATH="AllFiles/Labs/05"
   export MY_TEMPLATE_FILE="azuredeploy30305suba.json"
   export MY_LB_TEMPLATE="azuredeploy30305rga.json"
   export MY_LB_PARM_FILE="azuredeploy30305rga.parameters.json"
   export MY_LB_NAME="az30305a-lb"  # defined inside JSON template file
# Set before calling each program:  # az-vm-lb-init.sh
   export RMV_RG_BEFORE=true         # parm -RGb
   export RMV_RG_AT_END=false        # parm -RGe
   export RMV_GITHUB_BEFORE=false    # parm -RGb
   export RMV_GITHUB_AT_END=false    # parm -RGe
   export DO_GITHUB_CLONE=true       # parm -c

echo "setmem.sh $MY_SCRIPT_VERSION MY_LOC=$MY_LOC"
