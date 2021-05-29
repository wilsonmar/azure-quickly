#!/usr/bin/env bash
# source ./az-rest-test.sh
# This detects language of input text "hello" or "hola" (Spanish)
# Adapted from 
# https://github.com/wilsonmar/azure-quickly/blob/main/02-cognitive-security/rest-test.cmd
# and
# https://github.com/MicrosoftLearning/AI-102-AIEngineer/blob/master/03-monitor/rest-test.cmd

echo "COG_SERVICE_NAME=$COG_SERVICE_NAME"
echo "MY_LOC=$MY_LOC"
echo "COG_SERVICE_KEY=$COG_SERVICE_KEY"

# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/how-tos/text-analytics-how-to-language-detection
# https://docs.microsoft.com/en-us/azure/cognitive-services/text-analytics/how-tos/text-analytics-how-to-call-api?tabs=synchronous
# https://westus.dev.cognitive.microsoft.com/docs/services/TextAnalytics-v3-0/operations/Languages
#curl -X POST "$COG_SERVICE_NAME.cognitiveservices.azure.com/text/analytics/v3.0/languages?" \

curl -X POST "https://westus.api.cognitive.microsoft.com/text/analytics/v3.0/languages?" \
   -H "Content-Type: application/json" \
   -H "Ocp-Apim-Subscription-Key: $COG_SERVICE_KEY" \
   --data-ascii "{'documents':[{'id':1,'text':'hola'}]}"
