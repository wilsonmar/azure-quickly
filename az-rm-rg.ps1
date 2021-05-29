# az-rm-rg.ps1
#================================================================
#= Very dangerous interactive script that delete all resources 
#= from all rescourcegroup in a specified subscription
#================================================================
# Adapted from http://www.frankysnotes.com/2016/12/need-to-nuke-azure-subscription.html
# How to install and configure Azure PowerShell
# https://docs.microsoft.com/en-us/powershell/azureps-cmdlets-docs/

# Instead of asking every time: $theSub = Read-Host "Enter the subscriptionId you want to clean"
# Read from file containing export commands used by CLI.
$theSub = 

# Login
Login-AzureRmAccount 

# Get a list of all Azure subscriptions that the user can access
$allSubs = Get-AzureRmSubscription 

>$allSubs | Sort-Object Name | Format-Table -Property ame, SubscriptionId, State



Write-Host "You select the following subscription. (it will be display 15 sec.)" -ForegroundColor Cyan
Get-AzureRmSubscription -SubscriptionId $theSub | Select-AzureRmSubscription 

#Get all the resources groups
$allRG = Get-AzureRmResourceGroup

foreach ( $g in $allRG){
    Write-Host $g.ResourceGroupName -ForegroundColor Yellow 
    Write-Host "------------------------------------------------------`n" -ForegroundColor Yellow 
    $allResources = Find-AzureRmResource -ResourceGroupNameContains $g.ResourceGroupName
    if($allResources){
        $allResources | Format-Table -Property Name, ResourceName
    }else{
        Write-Host "-- empty--`n"
    } 
    Write-Host "`n`n------------------------------------------------------" -ForegroundColor Yellow 
}

$lastValidation = Read-Host "Do you wich to delete ALL the resouces previously listed? (YES/ NO)"
if($lastValidation.ToLower().Equals("yes")){
    foreach ( $g in $allRG){
        Write-Host "Deleting " $g.ResourceGroupName 
        Remove-AzureRmResourceGroup -Name $g.ResourceGroupName -Force -WhatIf
    }
}else{
    Write-Host "Aborded. Nothing was deleted." -ForegroundColor Cyan
}