#!/usr/bin/env bash

echo ">>> Starting ./az-bing-cli.sh "

set -o errexit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi

## Create Cognitive service:


# https://stackoverflow.com/questions/42123633/access-denied-due-to-invalid-subscription-key-face-api

### No need to login ifcan be found:
#   az login --allow-no-subscriptions  # --use-device-code
#sleep 5  # wait to see https://docs.microsoft.com/en-us/cli/azure/

## A Resource Group does not need to be created for Bing search

# Search API DOC: https://dev.cognitive.microsoft.com/docs/services/f40197291cd14401b93a478716e818bf/operations/56b4447dcf5ff8098cef380d

#echo "https://api.cognitive.microsoft.com/bing/v7.0/search fails with message:"
#echo " The request is not authorized because credentials are missing or invalid. code : 401000"
#exit
# https://docs.microsoft.com/en-us/answers/questions/160048/request-to-bing-search-v7-api-unauthorized.html

# NOTE: Deprecated: GET 'https://api.bing.microsoft.com/v7.0/search?q=Welsch%20Corgis&count=10&offset=0&mkt=en-us&safesearch=Moderate' \
# echo ">>> Bing GET \"$MY_SUBSCRIPTION_ID\" "
curl -X GET 'https://westus.cognitiveservices.azure.com/bing/v7.0/search?q=Welsch%20Corgis&count=10&offset=0&mkt=en-us&safesearch=Moderate' \
   -H 'Ocp-Apim-Subscription-Key: $MY_SEARCH_STRING' \
   -H 'Ocp-Apim-Subscription-Region: $MY_LOC' \
   | json_pp

exit


https://westus.api.cognitive.microsoft.com/





