#!/usr/bin/env bash

# ./az-cog-init.sh in https://github.com/wilsonmar/azure-your-way
# Described in https://wilsonmar.github.io/microsoft-ai/#Text_Analytics

set -o errexit

   export RMV_RG_BEFORE=true         # parm -RGb
source ./az-all-start.sh  # to setup environment variables and utility functions

if [[ -z "${MY_RG}" ]]; then  # not found:
   exit
#   source ../setup.sh   # in folder above this.
fi

### PROTIP: Resource Group is deleted and recreated becuase only ONE Cognitive Service account can use "F0" free Plan.

# https://docs.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest

# echo ">>> List SKUs available in region/location \"${MY_RG}\" ..."
# az vm list-skus --location "${MY_RG}" --size Standard_F --all --output table | grep "${MY_RG}"

export MY_COG_KIND="TextAnalytics"
   export COG_SERVICE_NAME="${MY_RG}cog$RANDOM"  # generate globally unique one
      # "$COG_SERVICE_NAME/text/analytics/v3.0/languages?" 
   export MY_COG_PRICING_TIER="F0" # "F0" or "S0" or "Standard_F2s_v2""
 # export MY_COG_KIND="Bing.Search.v7"  # AnomalyDetector, Bing.Search.v7, etc.
     # Specified before calling
   export COG_SERVICE_ENDPOINT="https://$MY_LOC.api.cognitive.microsoft.com/"
#   export COG_SERVICE_KEY=""  # generated for COG service created.

# TODO: Don't create if already exists
function az-all-start-cog-acct-create() {
   echo ">>> Create cognitiveservices \"$MY_COG_KIND\" account in \"$COG_SERVICE_NAME\" :"
   time az cognitiveservices account create \
       --name "${COG_SERVICE_NAME}"  \
       --kind "${MY_COG_KIND}" \
       --sku "${MY_COG_PRICING_TIER}" \
       --location "${MY_LOC}" \
       --yes \
       --resource-group "${MY_RG}" 
}
az-all-start-cog-acct-create

COG_SERVICE_KEY=$( az cognitiveservices account keys list \
    --name "${COG_SERVICE_NAME}" \
    --resource-group "${MY_RG}" --query key1 -o tsv )
# SAMPLE RESPONSE: 27900c313d0e494b9d53993cab31f92f 
echo  ">>> Exporting COG_SERVICE_KEY \"$COG_SERVICE_KEY\" ..."
export COG_SERVICE_KEY="$COG_SERVICE_KEY"

# https://wilsonmar.github.io/microsoft-ai/#Text_Analytics

echo  ">>> \"$MY_COG_KIND\" keyPhrases Extraction ..."
# https://docs.microsoft.com/en-us/learn/modules/extract-key-phrases-text-analytics-api/2-exercise-prepare-json-document-use-key-phrase-extraction
curl -v -X POST "https://$MY_RG.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases?showStats=true"
-H "Content-Type: application/json"
-H "Ocp-Apim-Subscription-Key: $COG_SERVICE_KEY"
--data-ascii "{
  "documents": [
    {
      "language": "en",
      "id": "1",
      "text": "Bill Gates and Paul Allen founded Microsoft, in part, to develop a BASIC interpreter for the popular Altair 8800 personal computer."
    },
    {
      "language": "es",
      "id": "2",
      "text": "La sede principal de Microsoft se encuentra en la ciudad de Redmond, a 21 kilómetros de Seattle."
    }
  ]
}"

exit

echo  ">>> \"$MY_COG_KIND\" Detect Language ..."
curl -v -X POST "https://$MY_RG.api.cognitive.microsoft.com/text/analytics/v2.1/languages?showStats=true"
-H "Content-Type: application/json"
-H "Ocp-Apim-Subscription-Key: $COG_SERVICE_KEY"
--data-ascii "{
    "documents": [
        {
            "id": "1",
            "text": "This document is in English."
        },
        {
            "id": "2",
            "text": "Este documento está en inglés."
        },
        {
            "id": "3",
            "text": "Ce document est en anglais."
        },
        {
            "id": "4",
            "text": "本文件为英文"
        },
        {
            "id": "5",
            "text": "Этот документ на английском языке."
        }
    ]
}"
