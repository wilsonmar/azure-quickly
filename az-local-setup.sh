# ./az-local-setup.sh
# Run this on your local laptop to install what is needed for Azure development.
# Alternately, https://shell.azure.com comes with all prerequsites pre-installed.
# But a local environment does not inconveniently time out.

# Homebrew
# VSCode
# Node
# nvm (Node Version Manager)
# pyenv (Python Version manager)
# Python

# az cli
brew install az

brew install 

# https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=macos%2Ccsharp%2Cbash
brew tap azure/functions
brew install azure-functions-core-tools@3
# if upgrading on a machine that has 2.x installed
brew link --overwrite azure-functions-core-tools@3
   #Cloning into '/usr/local/Homebrew/Library/Taps/azure/homebrew-functions'...
   #remote: Enumerating objects: 467, done.
   #remote: Counting objects: 100% (65/65), done.
   #remote: Compressing objects: 100% (45/45), done.
   #remote: Total 467 (delta 44), reused 29 (delta 20), pack-reused 402
   #Receiving objects: 100% (467/467), 63.66 KiB | 341.00 KiB/s, done.
   #Resolving deltas: 100% (280/280), done.
   #Tapped 4 formulae (32 files, 112.8KB).

az extension add -n ml

npm

# If you're using Azure Functions:
npm install -g azure-functions-core-tools@3 --unsafe-perm true
# RESPONSE: added 51 packages, and audited 52 packages in 1s

# Install Azure Functions extension for Visual Studio Code:
# https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions

# https://docs.microsoft.com/en-us/azure/azure-functions/create-first-function-vs-code-csharp?pivots=programming-language-python
# https://docs.microsoft.com/en-us/azure/azure-functions/functions-get-started?pivots=programming-language-python
# https://docs.microsoft.com/en-us/azure/azure-functions/functions-get-started?pivots=programming-language-csharp

# https://microsoftlearning.github.io/AZ-204-DevelopingSolutionsforMicrosoftAzure/Instructions/Labs/AZ-204_06_lab.html
# Exercise 2 Task 1
dotnet new console --name GraphClient --output .
   # Getting ready...
   # The template "Console Application" was created successfully.
   # Processing post-creation actions...
   # Running 'dotnet restore' on ./GraphClient.csproj...
   #   Restore completed in 154.36 ms for /Users/wilson_mar/gmail_acct/az-labs/GraphClient.csproj.
   # Restore succeeded.

dotnet add package Microsoft.Identity.Client --version 4.7.1

dotnet build
   # GraphClient.csproj Program.cs         bin                obj