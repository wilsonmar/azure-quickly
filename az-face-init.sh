#!/usr/bin/env bash

echo ">>> Starting ./az-face-init.sh "

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

# https://docs.microsoft.com/en-us/cli/azure/cognitiveservices/account?view=azure-cli-latest

# source ./az-cog-init.sh  # to create cog key

time MY_FACE_KEY1=$( az cognitiveservices account keys list \
   --name ComputerVisionService \
   --resource-group "$MY_RG" \
   --query key1 -o tsv)

echo ">>> Find VisualFeatures=Adult "
curl "https://$MY_LOC.api.cognitive.microsoft.com/vision/v2.0/analyze?visualFeatures=Adult,Description" \
-H "Ocp-Apim-Subscription-Key: $MY_FACE_KEY1" \
-H "Content-Type: application/json" \
-d "{'url' : 'https://raw.githubusercontent.com/MicrosoftDocs/mslearn-process-images-with-the-computer-vision-service/master/images/people.png'}" \
| jq '.'

# https://docs.microsoft.com/en-us/learn/modules/create-computer-vision-service-to-classify-images/3-analyze-images
echo ">>> Detect Landmark: "
curl "https://$MY_LOC.api.cognitive.microsoft.com/vision/v2.0/analyze?visualFeatures=Categories,Description&details=Landmarks" \
-H "Ocp-Apim-Subscription-Key: $MY_FACE_KEY1" \
-H "Content-Type: application/json" \
-d "{'url' : 'https://raw.githubusercontent.com/MicrosoftDocs/mslearn-process-images-with-the-computer-vision-service/master/images/mountains.jpg'}" \
| jq '.'
# RESPONSE: [{"faceId":"2e5d3ce9-bdd2-41c4-a5f8-4faf59607a1a","faceRectangle":{"top":83,"left":208,"width":166,"height":230}}]

# https://docs.microsoft.com/en-us/azure/cognitive-services/face/quickstarts/client-libraries?tabs=visual-studio&pivots=programming-language-rest-api
echo ">>> In an image detect face location rectangle: "
curl -H "Ocp-Apim-Subscription-Key: $MY_FACE_KEY1" \
   "https://$MY_FACE_ACCT.cognitiveservices.azure.com/face/v1.0/detect?detectionModel=detection_03&returnFaceId=true&returnFaceLandmarks=false" \
   -H "Content-Type: application/json" \
   --data-ascii "{\"url\":\"https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg\"}"

#    "$MY_FACE_ENDPOINT/face/v1.0/detect?detectionModel=detection_03&returnFaceId=true&returnFaceLandmarks=false" \

# https://docs.microsoft.com/en-us/learn/modules/create-computer-vision-service-to-classify-images/4-generate-thumbnail
echo ">>> Generate a thumbnail "
curl "https://<region>.api.cognitive.microsoft.com/vision/v2.0/generateThumbnail?width=100&height=100&smartCropping=true" \
-H "Ocp-Apim-Subscription-Key: $key" \
-H "Content-Type: application/json" \
-d "{'url' : 'https://raw.githubusercontent.com/MicrosoftDocs/mslearn-process-images-with-the-computer-vision-service/master/images/dog.png'}" \
-o  thumbnail.jpg

echo ">>> Text OCR  "
# https://docs.microsoft.com/en-us/learn/modules/create-computer-vision-service-to-classify-images/5-extract-printed-text
curl "https://<region>.api.cognitive.microsoft.com/vision/v2.0/ocr" \
-H "Ocp-Apim-Subscription-Key: $key" \
-H "Content-Type: application/json"  \
-d "{'url' : 'https://raw.githubusercontent.com/MicrosoftDocs/mslearn-process-images-with-the-computer-vision-service/master/images/ebook.png'}" \
 | jq '.'