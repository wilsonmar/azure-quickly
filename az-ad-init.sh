#!/usr/bin/env bash

# ./az-ad-init.sh in https://github.com/wilsonmar/azure-quickly
# To fulfill https://microsoftlearning.github.io/AZ-304-Microsoft-Azure-Architect-Design/Instructions/Labs/Module_4_Lab.html
# Described in https://wilsonmar.github.io/azure-iam/#Text_Analytics

set -o errexit

export RMV_RG_BEFORE=true         # parm -RGb
source ./az-all-start.sh  # to setup environment variables and utility functions

# Task 1: 

# Task 2: Deploy an Azure VM running an AD DS domain controller by using an Azure Resource Manager QuickStart template

# Instead of PowerShell New-AzSubscriptionDeployment `
New-AzSubscriptionDeployment `
  -Location $location `
  -Name az30410subaDeployment `
  -TemplateFile az304/azuredeploy30410suba.json `
  -rgLocation $location `
  -rgName 'az30410a-labRG'

# https://github.com/Azure/azure-quickstart-templates/tree/master/application-workloads/active-directory/active-directory-new-domain  

# On the Create a new Windows VM and create a new AD Forest, Domain and DC page, select Deploy to Azure. This will automatically redirect the browser to the Create an Azure VM with a new AD Forest blade in the Azure portal.

# On the Create an Azure VM with a new AD Forest blade, select Edit parameters.

# On the Edit parameters blade, select Load file, in the Open dialog box, select \\AZ304\AllFiles\Labs\10\azuredeploy30410rga.parameters.json, select Open, and then select Save.

# On the Create an Azure VM with a new AD Forest blade, specify the following settings (leave others with their existing values):
Setting 	Value
Subscription 	the name of the Azure subscription you are using in this lab
Resource group 	az30410a-labRG
Dns Prefix 	the DNS hostname you identified in the previous task

# On the Create an Azure VM with a new AD Forest blade, select Review + create and select Create.