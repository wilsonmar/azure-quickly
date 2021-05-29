#!/usr/bin/env bash

# This is ./az-vm-lb-init.sh within https://github.com/wilsonmar/azure-quickly
# Described in https://wilsonmar.github.io/azure-networking
# Created to automate Exercise 1 in https://microsoftlearning.github.io/AZ-303-Microsoft-Azure-Architect-Technologies/Instructions/Labs/Module_05_Lab.html#exercise-1-implement-and-analyze-highly-available-azure-vm-deployments-using-availability-sets-and-azure-load-balancer-basic
# 1. Prepare your CLI Bash environment according to https://wilsonmar.github.io/azure-quickly
#    which references repo https://github.com/wilsonmar/azure-quickly.
# 2. In your clouddrive folder edit your preferences in ../setmem.sh (MY_RG, MY_LOC, etc.)
# 3. Copy and paste this to the Bash command line:
#    bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-vm-lb.sh)" -v -i

source ./az-all-start.sh  # to setup environment variables and utility functions

set -o errexit

#export MY_REPO_URL="https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies"
#export MY_REPO_FOLDER="AZ303"
export MY_TEMPLATE_PATH="work"
export MY_TEMPLATE_FILE="azuredeploy30305suba.json"
export MY_LB_TEMPLATE="azuredeploy30305rga.json"
export MY_LB_PARM_FILE="azuredeploy30305rga.parameters.json"
export MY_LB_NAME="az30305a-lb"  # inside file 
# To be specified in script call parms:"
export RMV_RG_BEFORE=true        # parm -RRGb
#export RMV_RG_AT_END=false       # parm -RRGe
#export RMV_GITHUB_BEFORE=false   # parm -RGb
#export RMV_GITHUB_AT_END=false   # parm -RGe
#export DO_GITHUB_CLONE=true      # parm -c

# TODO: Get all public frontend IP addresses for the load balancer.
# publicIpIds=$( az network lb show -g ${resourceGroupName} -n ${lbName} --query "frontendIpConfigurations[].publicIpAddress.id" --out tsv)

echo ">>> Navigate to top "
cd
if [ -d "clouddrive" ]; then
   cd clouddrive
   echo ">>> now in clouddrive "
else
   if [ -d "gmail_acct" ]; then
      cd gmail_acct
      echo ">>> now in gmail_acct locally "
   fi
fi
pwd

export MY_TEMPLATE_FILE="azuredeploy30305suba.json"
cat > "$MY_TEMPLATE_FILE" <<TEMPLATEX
{
  "$schema": "https://schema.management.azure.com/schemas/2018-05-01/subscriptionDeploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "rgName": {
      "type": "string"
    },
    "rgLocation": {
      "type": "string"
    }
  },
  "variables": {},
  "resources": [
    {
      "type": "Microsoft.Resources/resourceGroups",
      "apiVersion": "2018-05-01",
      "name": "[parameters('rgName')]",
      "location": "[parameters('rgLocation')]",
      "properties": {}
    }
  ],
  "outputs": {}
}
TEMPLATEX

function thisfile_confirm_deployment_sub() {
   RESPONSE=$( az deployment sub list --query "[?name == '$MY_RG']" )
   echo ">>> $RESPONSE"
}
thisfile_confirm_deployment_sub  # Check if deployment exists
if [[ "[]" == *"${RESPONSE}"* ]]; then
pwd
   if [ ! -f "$MY_TEMPLATE_FILE" ]; then
      echo ">>> Template file $MY_TEMPLATE_FILE not found. Exiting."
      exit
   fi

   echo ">>> az deployment sub create $MY_RG in \"$MY_LOC\" using template $MY_TEMPLATE_FILE "
   # https://docs.microsoft.com/en-us/cli/azure/deployment/sub?view=azure-cli-latest#az_deployment_sub_list
   time az deployment sub create \
      --location "$MY_LOC" \
      --template-file "$MY_TEMPLATE_FILE" \
      --parameters rgName="$MY_RG" rgLocation="$MY_LOC"
# {"error":{"code":"InvalidRequestContent","message":"The request content was invalid and could not be deserialized: 'Could not find member '' on object of type 'Template'. Path 'properties.template.', line 2, position 5.'."}}
fi
thisfile_confirm_deployment_sub
if [[ "[]" == *"${RESPONSE}"* ]]; then
   echo ">>> Deployment sub not identified. Exiting "
   exit
fi

export MY_LB_PARM_FILE="azuredeploy30305rga.parameters.json"
cat > "$MY_LB_PARM_FILE" <<TEMPLATEX
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentParameters.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "adminUsername": {
            "value": "Student"
        },
        "adminPassword": {
            "value": "Pa55w.rd1234"
        }
    }
}
TEMPLATEX

export MY_LB_TEMPLATE="azuredeploy30305rga.json"
cat > "$MY_LB_TEMPLATE" <<TEMPLATEX
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "vnetName": {
      "type": "string",
      "defaultValue": "az30305a-vnet",
      "metadata": {
        "description": "Virtual network name"
      }
    },
    "vmCount": {
      "type": "int",
      "defaultValue": 2,
      "minValue": 1,
      "maxValue": 3,
      "metadata": {
        "description": "Number of VMs to provision"
      }
    },
    "nicNamePrefix": {
      "type": "string",
      "defaultValue": "az30305a-nic",
      "metadata": {
        "description": "Network interface name prefix"
      }
    },
    "vmNamePrefix": {
      "type": "string",
      "defaultValue": "az30305a-vm",
      "metadata": {
        "description": "VM name prefix"
      }
    },
    "adminUsername": {
      "type": "string",
      "metadata": {
        "description": "Windows admin username"
      }
    },
    "adminPassword": {
      "type": "securestring",
      "metadata": {
        "description": "Windows admin password"
      }
    },
    "vmSize": {
      "type": "string",
      "defaultValue": "Standard_D2s_v3",
      "metadata": {
        "description": "VM size"
      }
    },
    "diskType": {
      "type": "string",
      "defaultValue": "Standard_LRS",
      "allowedValues": [
        "StandardSSD_LRS",
        "Standard_LRS",
        "Premium_LRS"
      ],
      "metadata": {
        "description": "disk storage type"
      }
    }
  },
  "variables": {
    "availabilitySetName": "az30305a-avset",
    "subnet0Name": "web",
    "vnetID": "[resourceId('Microsoft.Network/virtualNetworks',parameters('vnetName'))]",
    "subnetRef": "[concat(variables('vnetID'),'/subnets/',variables('subnet0Name'))]",
    "webNetworkSecurityGroupName": "az30305a-web-nsg",
    "lbname": "az30305a-lb",
    "lbrule1name": "az303005a-lbruletcp80",
    "lbbepoolname": "az30305a-bepool",
    "lbprobename": "az30305a-hp",
    "natruleNamePrefix": "[concat(parameters('nicNamePrefix'), '-rdp-')]",
    "lbId": "[resourceId('Microsoft.Network/loadBalancers', variables('lbName'))]",
    "frontEndIPConfigId": "[concat(variables('lbId'), '/frontendIPConfigurations/loadBalancerFrontend')]",
    "pipName": "az30305a-pip",
    "storageAccountName": "[concat('az30005a', uniqueString(subscription().subscriptionId,resourceGroup().id, deployment().name))]",
    "storageAccountType": "Standard_LRS",
    "windowsImage": {
      "publisher": "MicrosoftWindowsServer",
      "offer": "WindowsServer",
      "sku": "2019-Datacenter-Core",
      "version": "latest"
    },
    "vmExtensionName": "customScriptExtension",
    "computeAPIVersion": "2019-07-01",
    "networkAPIVersion": "2019-11-01",
    "storageAPIVersion": "2019-06-01"
  },
  "resources": [
    {
      "type": "Microsoft.Storage/storageAccounts",
      "name": "[variables('storageAccountName')]",
      "apiVersion": "[variables('storageAPIVersion')]",
      "location": "[resourceGroup().location]",
      "sku": {
        "name": "[variables('storageAccountType')]"
      },
      "kind": "Storage",
      "properties": {}
    },
    {
      "type": "Microsoft.Compute/availabilitySets",
      "name": "[variables('availabilitySetName')]",
      "apiVersion": "[variables('computeApiVersion')]",
      "location": "[resourceGroup().location]",
      "sku": {
        "name": "Aligned"
      },
      "properties": {
        "platformFaultDomainCount": "2",
        "platformUpdateDomainCount": "5"
      }
    },
    {
      "type": "Microsoft.Network/publicIPAddresses",
      "name": "[variables('pipName')]",
      "apiVersion": "[variables('networkAPIVersion')]",
      "location": "[resourceGroup().location]",
      "sku": {
       "name": "Basic"
      },
      "properties": {
        "publicIPAddressVersion": "IPv4",
        "publicIPAllocationMethod": "Dynamic",
        "idleTimeoutInMinutes": 4
      }
    },
    {
      "name": "[variables('webNetworkSecurityGroupName')]",
      "type": "Microsoft.Network/networkSecurityGroups",
      "apiVersion": "[variables('networkAPIVersion')]",
      "location": "[resourceGroup().location]",
      "comments": "Network Security Group for the web subnet",
      "properties": {
        "securityRules": [
          {
            "name": "custom-allow-rdp",
            "properties": {
              "priority": 1000,
              "sourceAddressPrefix": "*",
              "protocol": "Tcp",
              "destinationPortRange": "3389",
              "access": "Allow",
              "direction": "Inbound",
              "sourcePortRange": "*",
              "destinationAddressPrefix": "*"
            }
          },
          {
            "name": "custom-allow-http",
            "properties": {
              "priority": 1100,
              "sourceAddressPrefix": "*",
              "protocol": "Tcp",
              "destinationPortRange": "80",
              "access": "Allow",
              "direction": "Inbound",
              "sourcePortRange": "*",
              "destinationAddressPrefix": "*"
            }
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/virtualNetworks",
      "name": "[parameters('vnetName')]",
      "apiVersion": "[variables('networkAPIVersion')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[concat('Microsoft.Network/networkSecurityGroups/', variables('webNetworkSecurityGroupName'))]"
      ],
      "properties": {
        "addressSpace": {
          "addressPrefixes": [
            "10.1.0.0/22"
          ]
        },
        "subnets": [
          {
            "name": "[variables('subnet0Name')]",
            "properties": {
              "addressPrefix": "10.1.0.0/24",
              "networkSecurityGroup": {
                "id": "[resourceId('Microsoft.Network/networkSecurityGroups', variables('webNetworkSecurityGroupName'))]"
              }
            }
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/networkInterfaces",
      "name": "[concat(parameters('nicNamePrefix'), copyindex())]",
      "apiVersion": "[variables('networkAPIVersion')]",
      "location": "[resourceGroup().location]",
      "copy": {
        "name": "nicLoop",
        "count": "[parameters('vmCount')]"
      },
      "dependsOn": [
        "[resourceId('Microsoft.Network/virtualNetworks', parameters('vnetName'))]",
        "[resourceId('Microsoft.Network/loadBalancers', variables('lbname'))]",
        "lbNatLoop"
      ],
      "properties": {
        "ipConfigurations": [
          {
            "name": "ipconfig1",
            "properties": {
              "privateIPAllocationMethod": "Dynamic",
              "subnet": {
                "id": "[variables('subnetRef')]"
              },
              "loadBalancerBackendAddressPools": [
                {
                  "id": "[concat(resourceId('Microsoft.Network/loadBalancers', variables('lbname')), '/backendAddressPools/', variables('lbbepoolname'))]"
                }
              ],
              "loadBalancerInboundNatRules": [
                {
                  "id": "[concat(resourceId('Microsoft.Network/loadBalancers', variables('lbname')), '/inboundNatRules/', parameters('nicNamePrefix'), '-rdp-', copyindex())]"
                }
              ]
            }
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/loadBalancers",
      "name": "[variables('lbname')]",
      "apiVersion": "[variables('networkAPIVersion')]",
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "[resourceId('Microsoft.Network/publicIPAddresses', variables('pipname'))]"
      ],
      "sku": {
        "name": "Basic"
      },
      "properties": {
        "frontendIPConfigurations": [
          {
            "name": "LoadBalancerFrontEnd",
            "properties": {
              "privateIPAllocationMethod": "Dynamic",
              "publicIPAddress": {
                "id": "[resourceId('Microsoft.Network/publicIPAddresses', variables('pipname'))]"
              },
              "privateIPAddressVersion": "IPv4"
            }
          }
        ],
        "backendAddressPools": [
          {
            "name": "[variables('lbbepoolname')]"
          }
        ],
        "loadBalancingRules": [
          {
            "name": "[variables('lbrule1name')]",
            "properties": {
              "frontendIPConfiguration": {
                "id": "[variables('frontEndIPConfigId')]"
              },
              "frontendPort": 80,
              "backendPort": 80,
              "enableFloatingIP": false,
              "idleTimeoutInMinutes": 4,
              "protocol": "Tcp",
              "enableTcpReset": false,
              "loadDistribution": "Default",
              "backendAddressPool": {
                "id": "[concat(resourceId('Microsoft.Network/loadBalancers', variables('lbname')), '/backendAddressPools/', variables('lbbepoolname'))]"
                },
              "probe": {
                "id": "[concat(resourceId('Microsoft.Network/loadBalancers', variables('lbname')), '/probes/', variables('lbprobename'))]"
              }
            }
          }
        ],
        "probes": [
            {
            "name": "[variables('lbprobename')]",
            "properties": {
                "protocol": "Tcp",
                "port": 80,
                "intervalInSeconds": 5,
                "numberOfProbes": 2
            }
          }
        ]
      }
    },
    {
      "type": "Microsoft.Network/loadBalancers/inboundNatRules",
      "name": "[concat(variables('lbName'), '/', variables('natRuleNamePrefix'), copyIndex())]",
      "apiVersion": "[variables('networkAPIVersion')]",
      "location": "[resourceGroup().location]",
      "copy": {
        "name": "lbNatLoop",
        "count": "[parameters('vmCount')]"
      },
      "dependsOn": [
        "[variables('lbName')]"
      ],
      "properties": {
        "frontendIPConfiguration": {
          "id": "[variables('frontEndIPConfigId')]"
        },
        "protocol": "Tcp",
        "frontendPort": "[copyIndex(33890)]",
        "backendPort": "3389",
        "enableFloatingIP": false
      }
    },
    {
      "type": "Microsoft.Compute/virtualMachines",
      "name": "[concat(parameters('vmNamePrefix'), copyindex())]",
      "apiVersion": "[variables('computeApiVersion')]",
      "copy": {
        "name": "virtualMachineLoop",
        "count": "[parameters('vmCount')]"
      },
      "location": "[resourceGroup().location]",
      "dependsOn": [
        "nicLoop",
        "[concat('Microsoft.Compute/availabilitySets/', variables('availabilitySetName'))]"
      ],
      "properties": {
        "availabilitySet": {
          "id": "[resourceId('Microsoft.Compute/availabilitySets',variables('availabilitySetName'))]"
        },
        "hardwareProfile": {
          "vmSize": "[parameters('vmSize')]"
        },
        "osProfile": {
          "computerName": "[concat(parameters('vmNamePrefix'), copyIndex())]",
          "adminUsername": "[parameters('adminUsername')]",
          "adminPassword": "[parameters('adminPassword')]"
        },
        "storageProfile": {
          "imageReference": "[variables('windowsImage')]",
          "osDisk": {
            "createOption": "FromImage",
            "managedDisk": {
              "storageAccountType": "[parameters('diskType')]"
            }
          }
        },
        "networkProfile": {
          "networkInterfaces": [
            {
              "id": "[resourceId('Microsoft.Network/networkInterfaces',concat(parameters('nicNamePrefix'),copyindex()))]"
            }
          ]
        },
        "diagnosticsProfile": {
          "bootDiagnostics": {
            "enabled": true,
            "storageUri": "[reference(resourceId('Microsoft.Storage/storageAccounts/', variables('storageAccountName'))).primaryEndpoints.blob]"
          }
        }
      }
    },
    {
      "type": "Microsoft.Compute/virtualMachines/extensions",
      "name": "[concat(parameters('vmNamePrefix'), copyindex(), '/', variables('vmExtensionName'))]",
      "apiVersion": "[variables('computeApiVersion')]",
      "location": "[resourceGroup().location]",
      "copy": {
        "name": "virtualMachineLoop",
        "count": "[parameters('vmCount')]"
      },
      "dependsOn": [
        "[concat('Microsoft.Compute/virtualMachines/', parameters('vmNamePrefix'), copyindex())]"
      ],
      "properties": {
        "publisher": "Microsoft.Compute",
        "type": "CustomScriptExtension",
        "typeHandlerVersion": "1.7",
        "autoUpgradeMinorVersion": true,
        "settings": {
          "commandToExecute": "powershell.exe Install-WindowsFeature -name Web-Server -IncludeManagementTools && powershell.exe remove-item 'C:\\inetpub\\wwwroot\\iisstart.htm' && powershell.exe Add-Content -Path 'C:\\inetpub\\wwwroot\\iisstart.htm' -Value $('Hello World from ' + $env:computername)"
        }
      }
    }
  ]
}
TEMPLATEX



if [[ -z "${MY_LB_PARM_FILE}" ]]; then
   echo ">>> MY_LB_PARM_FILE \"$MY_LB_PARM_FILE\" not defined. "
fi

function thisfile_confirm_deployment_group() {
   echo ">>> list deploy group for $MY_RG "
   RESPONSE=$( az deployment group list --query "[?name == '$MY_RG']" )
   echo ">>> $RESPONSE"
}
thisfile_confirm_deployment_group  # Check if deployment exists
if [[ "[]" == *"${RESPONSE}"* ]]; then
   echo ">>> az deployment group create based on \"$MY_LB_TEMPLATE\" & parms \"$MY_LB_PARM_FILE\" "
   pwd
   # with its backend pool "
   # consisting of a pair of Azure VMs hosting Windows Server 2019 Datacenter Core 
   # into the same availability set: 
   # https://docs.microsoft.com/en-us/cli/azure/deployment/group?view=azure-cli-latest
   time az deployment group create \
      --template-file "$MY_LB_TEMPLATE" \
      --parameters "$MY_LB_PARM_FILE" \
      --resource-group "$MY_RG" 
   #    --mode incremental \
   #    --verbose \
   #    --parameters "{ `"location`": { `"value`": `"$location`" },`"projectPrefix`": { `"value`": `"$prefix`" } }"
    #time 5m
fi
thisfile_confirm_deployment_group
if [[ "[]" == *"${RESPONSE}"* ]]; then
   echo ">>> Deployment group not identified. Exiting "
   exit
fi

# As in Portal, LB_PUBLIC_IP is Load Balancer -> Overview -> Public IP address:
#$pipId = $(az network lb show --id $loadBalancer.id --query "frontendIpConfigurations | [?loadBalancingRules != null].publicIpAddress.id" -o tsv)
#$ip = (az network public-ip show --ids $pipId --query "ipAddress" -o tsv)

LB_PUBLIC_IP=$( az network public-ip list --query "[].ipAddress" -o tsv )

# TODO: Extract Public IP address from Load Balancer 40.83.174.66 (az30305a-pip)
# In azuredeploy30305rga.json, under variables, "pipName": "az30305a-pip", 

echo ">>> curl LB_PUBLIC_IP=$LB_PUBLIC_IP "
for i in {1..4}; do curl "$LB_PUBLIC_IP"; done
   # RESULTS: Evidence of round-robin allocation:
   # Hello World from az30305a-vm0
   # Hello World from az30305a-vm1
   # Hello World from az30305a-vm1
   # Hello World from az30305a-vm1

# Access:
   curl -v telnet://"$LB_PUBLIC_IP":33890
   # * Rebuilt URL to: telnet://40.83.174.66:33890/
   # *   Trying 40.83.174.66...
   # * TCP_NODELAY set
   # * Connected to 40.83.174.66 (40.83.174.66) port 33890 (#0)


if [ "${DEL_RG_AT_END}" = true ]; then  # param -d 
      echo ">>> Delete Resource Group \"$MY_RG\" "
      time az group delete --resource-group "${MY_RG}" --yes "$CMD_GENERAL_PARM"
fi


# Network Watcher Concepts Overview: https://docs.microsoft.com/en-us/azure/network-watcher/network-watcher-monitoring-overview
echo ">>> network watcher configure $MY_LOC in RG $MY_RG "
# DOCS: https://docs.microsoft.com/en-us/azure/network-watcher/network-watcher-create
# CLI:  https://docs.microsoft.com/en-US/cli/azure/network/watcher?view=azure-cli-latest#az_network_watcher_configure
# Portal  All Services > Networking > Network Watcher.
# TODO: Check if already exists
   az network watcher configure --enabled true \
      --locations "$MY_LOC" -o table \
      -g "$MY_RG"
   # Location    Name            ProvisioningState    ResourceGroup
   # ----------  --------------  -------------------  ---------------
   # westus      westus-watcher  Succeeded            wow


echo ">>> END"
# See https://github.com/Azure/azure-quickstart-templates/tree/master/201-2-vms-loadbalancer-lbrules.