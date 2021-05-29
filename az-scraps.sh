./az-scraps.sh

# This is a scrap area for unfinished work.

exit


echo ">>> create service principal :"
az ad sp create-for-rbac [--cert]
                         [--create-cert]
                         [--keyvault]
                         [--name "${MY_USER_PRINCIPAL_NAME}"
                         [--role]
                         [--scopes]
                         [--sdk-auth {false, true}]
                         [--skip-assignment {false, true}]
                         [--years]
                         
echo ">>> role definition list:"
az role definition list --name "${MY_ROLE_NAME}"

echo ">>> role definition create:"
az role assignment create --role "${MY_ROLE_NAME}" \
  --assignee "${MY_USER_PRINCIPAL_NAME}" --scope $vaultId

echo ">>> Get the subscription ID:"
subId=$( az account show | jq -r .id )

echo ">>> Replace the subscription ID in the custom role json:"
sed s/SUBSCRIPTION_ID/$subId/g custom_role.json > updated_role.json

echo ">>> Get the role ID, vault ID, and user ID:"
role=$( az role definition create --role-definition updated_role.json )

echo ">>> Add AD user show:"
user=$( az ad user show  --id "${MY_USER_PRINCIPAL_NAME}" | jq -r .objectId )

echo ">>> Assign \"$user\" role \"$role\" with vault \"$vaultId\" as the scope:"
az role assignment create --role "Secret Reader" \
  --assignee $user --scope $vaultId
  
exit
  
echo ">>> Limit Admin's IP address by Add network rule to Key Vault \"$MY_KEYVAULT_NAME\":"
# Define your MY_CLIENT_IP using "curl -s ifconfig.me"
# If you're on a VPN, it rotates among various IPs, so it is not a good option to limit access to your IP address.
  # CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/keyvault/network-rule?view=azure-cli-latest
  # --network-acls # Network ACLs. It accepts a JSON filename or a JSON string. JSON format: {"ip":[<ip1>, <ip2>...],"vnet":[<vnet_name_1>/<subnet_name_1>,<subnet_id2>...]}.
  # --network-acls-ips  # Network ACLs IP rules. Space-separated list of IP addresses.
  # --network-acls-vnets  # Network ACLS VNet rules. Space-separated list of Vnet/subnet pairs or subnet resource ids.
az keyvault network-rule add --name "${MY_KEYVAULT_NAME}"  \
                             --ip-address "${MY_CLIENT_IP}"

az keyvault list -o table
# az keyvault show # RESPONSE: The HSM 'None' not found within subscription.


echo ">>> Create new Storage Account \"$MY_STORAGE_ACCT\" for Function App:"
az storage account create \
   --name "${MY_STORAGE_ACCT}" \
   --sku standard_lrs \
   --resource-group "${MY_RG}"

az storage account list --resource-group "${MY_RG}" --output table 
   # --query [*].{Name:name,Location:primaryLocation,Kind:kind}  CreationTime
   # grep to show only on created to filter out cloud-shell-storage account

echo ">>> Add tag \"${MY_STORAGE_TAG}\" to Storage account \"$MY_STORAGE_ACCT\":"
az storage account update --name "${MY_STORAGE_ACCT}" \
   --tags “${MY_STORAGE_TAGS}” \
   --resource-group "${MY_RG}"


echo ">>> Create App Service Plan \"$MY_PLAN\":"
# CLI DOC: https://docs.microsoft.com/en-us/cli/azure/appservice/plan?view=azure-cli-latest
az appservice plan create --name "${MY_PLAN}" \
   --resource-group "${MY_RG}"
#   --is-linux --number-of-workers 1 --sku FREE
#   --hyper-v --sku P1V3  # Windows

echo ">>> Create Function App \"$MY_FUNC_APP_NAME\":"
# TODO: Instead use https://github.com/timothywarner/function-image-upload-resize
# Instead of Port GUI https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2Fsites/kind/functionapp
# PORTAL VIDEO DEMO: https://app.pluralsight.com/course-player?clipId=2308c37d-0804-4834-86f3-2f38937170c2
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest#az_functionapp_create
# The Function App is set up to be manually connected to a sample app in GitHub
az functionapp create \
    --name "${MY_FUNC_APP_NAME}" \
    --storage-account "${MY_STORAGE_ACCT}" \
    --plan "${MY_PLAN}" \
    --deployment-source-url "${MY_FUNC_APP_URL}" \
    --resource-group "${MY_RG}"
    
  # --consumption-plan-location "${MY_LOC}" \
  # --functions-version "${MY_FUNC_APP_VER}" \
  # -p $MY_PLAN  # Region, SKU Dynamic, Operating System: Windows
     # Consumption plan is used, which means you are only charged based on memory usage while your app is running. 
  # Publish: Code (not Docker Container)
  # Runtime Stack: .NET Core
  # Version: 3.1


# echo ">>> Create a Service Principal (service acct):"
# Instead # See https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli
# See https://docs.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest#az_ad_sp_create_for_rbac



echo ">>> Add Managed Identity \"${MY_MANAGED_IDENTITY}\":"  # using tokens from Azure Active Directory, instead of Service Principal (service acct)  credentials
# Tutorial: https://docs.microsoft.com/en-us/azure/key-vault/general/tutorial-net-create-vault-azure-web-app
# See https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview
# See https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-cli-windows-vm
# System-assigned identidfy to specific resource means when that resource is deleted, Azure automatically deletes the identity.
# CLI DOC: https://docs.microsoft.com/en-us/cli/azure/identity?view=azure-cli-latest
az identity create --name "${MY_MANAGED_IDENTITY}" \
                   --resource-group "${MY_RG}"


#echo ">>> Add Access Policy:"
# See https://docs.microsoft.com/en-us/azure/key-vault/general/network-security
# To avoid these error messages:
   # Client address is not authorized and caller is not a trusted service.

echo ">>> Set (Create, generate) secret named \"${MY_KEY_NAME}\" in Key Vault \"${MY_KEYVAULT_NAME}\":"
# Overview: https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-cli
# This secret is a basic password that is used to install a database server
az keyvault secret set \
    --vault-name "${MY_KEYVAULT_NAME}" \
    --name "${MY_KEY_NAME}" \
    --value "${MY_KEY_SECRET}" \
    --description "${MY_KEY_CONTENT_TYPE}"  # such as "Database password"  # = GUI Content Type (optional)
  # Upload options: Manual as Certificate, which is deprecated.
  # Set activation date?
  # Set expiration date?
  # Enabled: Yes
  # Use PowerShell to set multi-line secrets.
   # ERROR RESPONSE: Client address is not authorized and caller is not a trusted service.

echo ">>> Show the secret stored in Key Vault:"
az keyvault secret show \
    --name "${MY_KEY_NAME}" \
    --vault-name "${MY_KEYVAULT_NAME}"


echo ">>> As Admin, Delete the secret:"
az keyvault secret delete \
    --name "${MY_KEY_NAME}" \
    --vault-name $MY_KEYVAULT_NAME
# RESPONSE: Secret databasepassword is currently being deleted.

# Wait 5 seconds for the secret to be successfully deleted before recovering
sleep 5

echo ">>> As Admin, Recover the deleted secret:"
# As the vault was enabled for soft delete, key are secret metadata is retained
# for a period of time. This allows keys and secrets to be recovered back to
# the vault.
az keyvault secret recover \
    --name "${MY_KEY_NAME}" \
    --vault-name $MY_KEYVAULT_NAME


echo ">>> Use Managed Identity to read secret:"
# VIDEO DEMO https://app.pluralsight.com/course-player?clipId=2308c37d-0804-4834-86f3-2f38937170c2

# https://www.youtube.com/watch?v=PgujSug1ZbI use KeyVault in Logic App, ADF 

# TODO: Issue certificate use Key Vault:
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/keyvault/certificate/issuer?view=azure-cli-latest
# https://github.com/Azure-Samples/key-vault-java-certificate-authentication/blob/master/README.md




echo ">>> DEBUG"
az group list

echo ">>> Get current quota usage for resource:"
az cognitiveservices account list-usage \
    --name "${COG_SERVICE_ENDPOINT}" \
    --subscription "${MY_SUBSCRIPTION_NAME}" \
    --resource-group "${MY_RG}" 
# CURRENTLY STUCK:
# ResourceGroupNotFound: Resource group 'x210501' could not be found.
    
exit

# Parameters are in order shown on the Portal GUI screen https://portal.azure.com/#create/Microsoft.KeyVault
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/keyvault?view=azure-cli-latest#az_keyvault_create
RESPONSE=$( az keyvault list )   # Identify if keyvault already exists
if [ $RESPONSE == "[]" ]; then
   echo ">>> Create Key Vault \"$MY_KEYVAULT_NAME\":"
   az keyvault create \
    --name "${MY_KEYVAULT_NAME}" \
    --location "${MY_LOC}" \
    --retention-days 90 \
    --enabled-for-deployment \
    --default-action Deny \
    --resource-group "${MY_RG}" 
fi
#    --enabled-for-deployment \. in GUI Portal is checkbox "Enable Access to: Azure Resource Manager for template deployment"
  # Argument 'enable_soft_delete' has been deprecated and will be removed in a future release.
  # --enable-purge-protection false # during test env usage when Vault is rebuilt between sessions.
# QUESTION: The vault is enabled for soft delete by default, which allows deleted keys to recovered, but a new keyvault name needs to be created every run.
# and is also enable for deployment which allows VMs to use the keys stored.
  # --default-action Deny # Default action to apply when no rule matches.
  # --retention-days 90 \  # 90 is max allowed.
  # --sku Standard  # or Premium (includes support for HSM backed keys) HSM: Standard_B1, Custom_B32. Default: Standard_B1.
  # See https://docs.microsoft.com/en-us/azure/key-vault/general/soft-delete-overview
# RESPONSE: Resource provider 'Microsoft.KeyVault' used by this operation is not registered. We are registering for you.

vaultId=$(az keyvault show -g "${MY_RG}" -n "${MY_KEYVAULT_NAME}" | jq -r .id)


echo ">>> create service principal :"
az ad sp create-for-rbac [--cert]
                         [--create-cert]
                         [--keyvault]
                         [--name "${MY_USER_PRINCIPAL_NAME}"
                         [--role]
                         [--scopes]
                         [--sdk-auth {false, true}]
                         [--skip-assignment {false, true}]
                         [--years]
                         
echo ">>> role definition list:"
az role definition list --name "${MY_ROLE_NAME}"

echo ">>> role definition create:"
az role assignment create --role "${MY_ROLE_NAME}" \
  --assignee "${MY_USER_PRINCIPAL_NAME}" --scope $vaultId

echo ">>> Get the subscription ID:"
subId=$( az account show | jq -r .id )

echo ">>> Replace the subscription ID in the custom role json:"
sed s/SUBSCRIPTION_ID/$subId/g custom_role.json > updated_role.json

echo ">>> Get the role ID, vault ID, and user ID:"
role=$( az role definition create --role-definition updated_role.json )

echo ">>> Add AD user show:"
user=$( az ad user show  --id "${MY_USER_PRINCIPAL_NAME}" | jq -r .objectId )

echo ">>> Assign \"$user\" role \"$role\" with vault \"$vaultId\" as the scope:"
az role assignment create --role "Secret Reader" \
  --assignee $user --scope $vaultId
  
exit
  
echo ">>> Limit Admin's IP address by Add network rule to Key Vault \"$MY_KEYVAULT_NAME\":"
# Define your MY_CLIENT_IP using "curl -s ifconfig.me"
# If you're on a VPN, it rotates among various IPs, so it is not a good option to limit access to your IP address.
  # CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/keyvault/network-rule?view=azure-cli-latest
  # --network-acls # Network ACLs. It accepts a JSON filename or a JSON string. JSON format: {"ip":[<ip1>, <ip2>...],"vnet":[<vnet_name_1>/<subnet_name_1>,<subnet_id2>...]}.
  # --network-acls-ips  # Network ACLs IP rules. Space-separated list of IP addresses.
  # --network-acls-vnets  # Network ACLS VNet rules. Space-separated list of Vnet/subnet pairs or subnet resource ids.
az keyvault network-rule add --name "${MY_KEYVAULT_NAME}"  \
                             --ip-address "${MY_CLIENT_IP}"

az keyvault list -o table
# az keyvault show # RESPONSE: The HSM 'None' not found within subscription.


echo ">>> Create new Storage Account \"$MY_STORAGE_ACCT\" for Function App:"
az storage account create \
   --name "${MY_STORAGE_ACCT}" \
   --sku standard_lrs \
   --resource-group "${MY_RG}"

az storage account list --resource-group "${MY_RG}" --output table 
   # --query [*].{Name:name,Location:primaryLocation,Kind:kind}  CreationTime
   # grep to show only on created to filter out cloud-shell-storage account

echo ">>> Add tag \"${MY_STORAGE_TAG}\" to Storage account \"$MY_STORAGE_ACCT\":"
az storage account update --name "${MY_STORAGE_ACCT}" \
   --tags “${MY_STORAGE_TAGS}” \
   --resource-group "${MY_RG}"


echo ">>> Create App Service Plan \"$MY_PLAN\":"
# CLI DOC: https://docs.microsoft.com/en-us/cli/azure/appservice/plan?view=azure-cli-latest
az appservice plan create --name "${MY_PLAN}" \
   --resource-group "${MY_RG}"
#   --is-linux --number-of-workers 1 --sku FREE
#   --hyper-v --sku P1V3  # Windows

echo ">>> Create Function App \"$MY_FUNC_APP_NAME\":"
# TODO: Instead use https://github.com/timothywarner/function-image-upload-resize
# Instead of Port GUI https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Web%2Fsites/kind/functionapp
# PORTAL VIDEO DEMO: https://app.pluralsight.com/course-player?clipId=2308c37d-0804-4834-86f3-2f38937170c2
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/functionapp?view=azure-cli-latest#az_functionapp_create
# The Function App is set up to be manually connected to a sample app in GitHub
az functionapp create \
    --name "${MY_FUNC_APP_NAME}" \
    --storage-account "${MY_STORAGE_ACCT}" \
    --plan "${MY_PLAN}" \
    --deployment-source-url "${MY_FUNC_APP_URL}" \
    --resource-group "${MY_RG}"
    
  # --consumption-plan-location "${MY_LOC}" \
  # --functions-version "${MY_FUNC_APP_VER}" \
  # -p $MY_PLAN  # Region, SKU Dynamic, Operating System: Windows
     # Consumption plan is used, which means you are only charged based on memory usage while your app is running. 
  # Publish: Code (not Docker Container)
  # Runtime Stack: .NET Core
  # Version: 3.1


# echo ">>> Create a Service Principal (service acct):"
# Instead # See https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli
# See https://docs.microsoft.com/en-us/cli/azure/ad/sp?view=azure-cli-latest#az_ad_sp_create_for_rbac


echo ">>> Add Managed Identity \"${MY_MANAGED_IDENTITY}\":"  # using tokens from Azure Active Directory, instead of Service Principal (service acct)  credentials
# Tutorial: https://docs.microsoft.com/en-us/azure/key-vault/general/tutorial-net-create-vault-azure-web-app
# See https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/overview
# See https://docs.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/qs-configure-cli-windows-vm
# System-assigned identidfy to specific resource means when that resource is deleted, Azure automatically deletes the identity.
# CLI DOC: https://docs.microsoft.com/en-us/cli/azure/identity?view=azure-cli-latest
az identity create --name "${MY_MANAGED_IDENTITY}" \
                   --resource-group "${MY_RG}"


#echo ">>> Add Access Policy:"
# See https://docs.microsoft.com/en-us/azure/key-vault/general/network-security
# To avoid these error messages:
   # Client address is not authorized and caller is not a trusted service.

echo ">>> Set (Create, generate) secret named \"${MY_KEY_NAME}\" in Key Vault \"${MY_KEYVAULT_NAME}\":"
# Overview: https://docs.microsoft.com/en-us/azure/key-vault/secrets/quick-create-cli
# This secret is a basic password that is used to install a database server
az keyvault secret set \
    --vault-name "${MY_KEYVAULT_NAME}" \
    --name "${MY_KEY_NAME}" \
    --value "${MY_KEY_SECRET}" \
    --description "${MY_KEY_CONTENT_TYPE}"  # such as "Database password"  # = GUI Content Type (optional)
  # Upload options: Manual as Certificate, which is deprecated.
  # Set activation date?
  # Set expiration date?
  # Enabled: Yes
  # Use PowerShell to set multi-line secrets.
   # ERROR RESPONSE: Client address is not authorized and caller is not a trusted service.

echo ">>> Show the secret stored in Key Vault:"
az keyvault secret show \
    --name "${MY_KEY_NAME}" \
    --vault-name "${MY_KEYVAULT_NAME}"

exit

echo ">>> As Admin, Delete the secret:"
az keyvault secret delete \
    --name "${MY_KEY_NAME}" \
    --vault-name $MY_KEYVAULT_NAME
# RESPONSE: Secret databasepassword is currently being deleted.

# Wait 5 seconds for the secret to be successfully deleted before recovering
sleep 5

echo ">>> As Admin, Recover the deleted secret:"
# As the vault was enabled for soft delete, key are secret metadata is retained
# for a period of time. This allows keys and secrets to be recovered back to
# the vault.
az keyvault secret recover \
    --name "${MY_KEY_NAME}" \
    --vault-name $MY_KEYVAULT_NAME


echo ">>> Use Managed Identity to read secret:"
# VIDEO DEMO https://app.pluralsight.com/course-player?clipId=2308c37d-0804-4834-86f3-2f38937170c2

# https://www.youtube.com/watch?v=PgujSug1ZbI use KeyVault in Logic App, ADF 

# TODO: Issue certificate use Key Vault:
# CLI DOCS: https://docs.microsoft.com/en-us/cli/azure/keyvault/certificate/issuer?view=azure-cli-latest
# https://github.com/Azure-Samples/key-vault-java-certificate-authentication/blob/master/README.md


az group list --query "[?name == '$RESOURCE_GROUP']"

az group list --query "[?starts_with(name,'az30305a-')]".name --output tsv