#!/usr/bin/env bash

echo ">>> Starting ./az-speech-init.sh "

set -o errexit

if [[ -z "${MY_RG}" ]]; then  # not found:
#   exit
   source ../setmem.sh   # in folder above this.
fi

if [ $( az group exists --name "${MY_RG}" ) = true ]; then
   echo ">>> Resource Group \"$MY_RG\" exists ..."
else
   echo ">>> Create Resource Group \"$MY_RG\" used for KeyVault, Storage Acct, etc."
   az group create --name "${MY_RG}" --location "${MY_LOC}" -o none
fi
### PROTIP: Resource Group is deleted and recreated becuase only one Cognitive Service account can use "F0" free Plan.

# https://docs.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest

# echo ">>> List SKUs available in region/location \"${MY_RG}\" ..."
# az vm list-skus --location "${MY_RG}" --size Standard_F --all --output table | grep "${MY_RG}"

echo ">>> Create speech profile "
# https://docs.microsoft.com/en-us/rest/api/speakerrecognition/verification/textdependent/createprofile
# https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/get-started-speaker-recognition?tabs=script&pivots=programming-language-curl
curl --location --request POST '"${MY_SPEECH_ENDPOINT}"/speaker/verification/v2.0/text-dependent/profiles' \
   --header 'Ocp-Apim-Subscription-Key: "${MY_SUBSCRIPTION_ID}" ' \
   --header 'Content-Type: application/json' \
   --data-raw '{ '\''locale'\'':'\''en-us'\'' }'

# Speech-to-text API for speech recognition using
   # https://<LOCATION>.api.cognitive.microsoft.com/sts/v1.0

# Speech-to-text Short Audio API, optimized for short streams of audio (up to 60 seconds). 
   # https://<LOCATION>.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1

