#!/usr/bin/env bash

# ./az-102-run.sh

# within https://github.com/MicrosoftLearning/AI-102-AIEngineer/blob/master/...
#
set -o errexit

echo ">>> 00-setup.md"
   chmod +x ../setmem.sh  # One folder up from repo to keep it from being pushed to github.
   source   ../setmem.sh
   echo ">>> MY_RG=\"$MY_RG\" from setmem.sh "

if [[ -z "${MY_RG}" ]]; then  # not found:
   exit
else
   echo ">>> Set subscription (ID not shown to keep it secure) ..."
   az account set --subscription "${MY_SUBSCRIPTION_ID}"
fi

az configure --defaults group=myResourceGroup location=westus

echo ">>> 00-update-resource-providers.md"
#    chmod +x ./az-providers-cli.sh
#!   source ./az-providers-cli.sh

echo ">>> 01-get-started-cognitive-services.md"
#!   pip install azure-ai-textanalytics==5.0.0
   export MY_COG_KIND="TextAnalytics"  # AnomalyDetector, Bing.Search.v7, etc.
   export MY_COG_PRICING_TIER="F0" # "Standard_F1s"  # "S0" # "F0"  
   source ./az-cog-init.sh
   # echo "COG_SERVICE_KEY=$COG_SERVICE_KEY"

   pushd 01-getting-started/Python/sdk-client
   # Requirement already satisfied: azure-ai-textanalytics==5.0.0 in /Users/wilson_mar/.pyenv/versions/3.7.9/lib/python3.7/site-packages (5.0.0)
   echo "COG_SERVICE_ENDPOINT=https://$MY_LOC.api.cognitive.microsoft.com/" > .env   # single > to create/overwrite file!
   echo "COG_SERVICE_KEY=$COG_SERVICE_KEY" >> .env
   echo "MY_TEXT_TO_TRANSLATE=hola" >> .env
   cat .env
   python sdk-client.py
      # STDOUT: Language: Spanish
   popd
   pwd
#   pushd 01-getting-started/Python/rest-client
#   # Requirement already satisfied: azure-ai-textanalytics==5.0.0 in /Users/wilson_mar/.pyenv/versions/3.7.9/lib/python3.7/site-packages (5.0.0)
#   echo "COG_SERVICE_ENDPOINT=https://$MY_LOC.api.cognitive.microsoft.com/" > .env   # single > to create/overwrite file!
#   echo "COG_SERVICE_KEY=$COG_SERVICE_KEY" >> .env
#   echo "MY_TEXT_TO_TRANSLATE=hello" >> .env
#   cat .env
#   python rest-client.py
#      # STDOUT: Language: English
#   popd
#   pwd
#
   pushd 02-cognitive-security/Python/keyvault-client.py
   echo "COG_SERVICE_ENDPOINT=https://$KEY_VAULT.vault.azure.net" > .env   # single > to create/overwrite file!
   echo "COG_SERVICE_KEY=$COG_SERVICE_KEY" >> .env
   echo "KEY_VAULT=$KEY_VAULT" >> .env
   echo "TENANT_ID=$TENANT_ID" >> .env
   echo "APP_ID=$APP_ID" >> .env
   echo "APP_PASSWORD=$APP_PASSWORD" >> .env
   cat .env
   source ./az-keyvault-init.sh
   popd
exit
   # 03-monitor/rest-test.cmd -> source ./az-anal-data.sh
#
   # 05-analyze-text/Python/text-analysis/text-analysis.py
   cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
   cog_key = os.getenv('COG_SERVICE_KEY')
#
   # 06-translate-text/Python/text-translation/text-translation.py
   cog_key = os.getenv('COG_SERVICE_KEY')
   cog_region = os.getenv('COG_SERVICE_REGION')
#
   # 07-speech/Python/speaking-clock/speaking-clock.py
   cog_key = os.getenv('COG_SERVICE_KEY')
   cog_region = os.getenv('COG_SERVICE_REGION')   
#
   # 08-speech-translation/Python/translator/translator.py
   cog_key = os.getenv('COG_SERVICE_KEY')
   cog_region = os.getenv('COG_SERVICE_REGION')   
#
   # 09-luis-app/GetIntent.cmd
   set app_id=YOUR_APP_ID
   set endpoint=YOUR_ENDPOINT
   set key=YOUR_KEY
#
   # 10-luis-client/Python/clock-client/clock-client.py
   export LU_APP_ID=""
   export LU_PREDICTION_ENDPOINT=""
   export LU_PREDICTION_KEY=""
#
   # 11-luis-speech/Python/speaking-clock-client/speaking-clock-client.py
   lu_app_id = os.getenv('LU_APP_ID')
   lu_prediction_region = os.getenv('LU_PREDICTION_REGION')
   lu_prediction_key = os.getenv('LU_PREDICTION_KEY')   
#
   # 15-computer-vision/Python/image-analysis/image-analysis.py
   cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
   cog_key = os.getenv('COG_SERVICE_KEY')
#
   # 17-image-classification/Python/train-classifier/train-classifier.py
   training_endpoint = os.getenv('TrainingEndpoint')
   training_key = os.getenv('TrainingKey')
   project_id = os.getenv('ProjectID')
#
   # 17-image-classification/Python/test-classifier/test-classifier.py
   prediction_endpoint = os.getenv('PredictionEndpoint')
   prediction_key = os.getenv('PredictionKey')
   project_id = os.getenv('ProjectID')
   model_name = os.getenv('ModelName')
#
   # 18-object-detection/Python/train-detector/train-detector.py
   training_endpoint = os.getenv('TrainingEndpoint')
   training_key = os.getenv('TrainingKey')
   project_id = os.getenv('ProjectID')
#
   # 18-object-detection/Python/test-detector/test-detector.py
   prediction_endpoint = os.getenv('PredictionEndpoint')
   prediction_key = os.getenv('PredictionKey')
   project_id = os.getenv('ProjectID')
   model_name = os.getenv('ModelName')
#
   # 19-face/Python/computer-vision/detect-faces.py
   cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
   cog_key = os.getenv('COG_SERVICE_KEY')   
#
   # 20-ocr/Python/read-text/read-text.py
   cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
   cog_key = os.getenv('COG_SERVICE_KEY')
#
   # 21-custom-form/Python/train-model/train-model.py
   form_endpoint = os.getenv('FORM_ENDPOINT')
   form_key = os.getenv('FORM_KEY')
   trainingDataUrl = os.getenv('STORAGE_URL')
   model_id = os.getenv('MODEL_ID')
#
   # 21-custom-form/setup.cmd
   form_endpoint = os.getenv('FORM_ENDPOINT')
   form_key = os.getenv('FORM_KEY')
   model_id = os.getenv('MODEL_ID')
#
   # 21-custom-form/setup.cmd
   set subscription_id=YOUR_SUBSCRIPTION_ID
   set resource_group=YOUR_RESOURCE_GROUP
   set location=YOUR_LOCATION_NAME
   set expiry_date=2022-01-01T00:00:00Z
#
   # 22-Create-a-search-solution/Python/margies-travel/app.py
   search_endpoint = os.getenv('SEARCH_SERVICE_ENDPOINT')
   search_key = os.getenv('SEARCH_SERVICE_QUERY_KEY')
   search_index = os.getenv('SEARCH_INDEX_NAME')
#
   # 22-Create-a-search-solution/UploadDocs.cmd
   set subscription_id=YOUR_SUBSCRIPTION_ID
   set azure_storage_account=YOUR_AZURE_STORAGE_ACCOUNT_NAME
   set azure_storage_key=YOUR_AZURE_STORAGE_KEY
#
   # 23-custom-search-skill/setup.cmd
   set subscription_id=YOUR_SUBSCRIPTION_ID
   set resource_group=YOUR_RESOURCE_GROUP
   set location=YOUR_LOCATION_NAME
#
   # 24-knowledge-store/setup.cmd
   set subscription_id=YOUR_SUBSCRIPTION_ID
   set resource_group=YOUR_RESOURCE_GROUP
   set location=YOUR_LOCATION_NAME
   </pre>
