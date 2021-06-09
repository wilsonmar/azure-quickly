# Based on https://docs.microsoft.com/en-us/learn/modules/control-and-organize-with-azure-resource-manager/3-use-tagging-to-organize-resources
az resource tag --tags Department=Finance \
    --name vnet1 \
    --resource-group "${MY_RG}" \
    --resource-type "Microsoft.Network/virtualNetworks"

# Use Azure Policy to automatically add or enforce tags based on policy conditions you define. 
# For example, require a Department tag when a virtual network is created in a specific resource group.

# Add a shutdown:6PM and startup:7AM tag to the virtual machines for an automation job that 
# looks for them and shuts them down or starts them up based on the tag value. 
# Look at the Azure Automation Runbooks Gallery for tag usage.
# https://github.com/azureautomation

# https://azure.microsoft.com/en-us/services/automation/
# https://www.lunavi.com/blog/how-to-run-azure-automation-runbook-locally-while-accessing-assets
# https://azure.microsoft.com/en-us/pricing/details/automation/ pricing
# Job run time free	500 minutes	$0.002/minute
# Watchers free	744 hours	$0.002/hour

# https://github.com/uglide/azure-content/blob/master/articles/automation/automation-runbook-gallery.md
# https://azure.microsoft.com/en-us/blog/introducing-the-azure-automation-runbook-gallery/
# https://docs.microsoft.com/en-us/azure/automation/automation-runbook-gallery
# TechNet Script Center gallery hosting Automation scripts (runbooks) as shown in the Runbooks Gallery 
# was retired on December 2020

