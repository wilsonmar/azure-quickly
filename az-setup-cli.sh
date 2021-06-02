#!/usr/bin/env bash

# ./az-setup-cli.sh

# This script is meant to be run by copy and paste:
# as described in https://wilsonmar.github.io/azure-quickly
# bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i
# within https://github.com/MicrosoftLearning/AI-102-AIEngineer/blob/master/...
#
   set -o errexit

# Because /setmem.sh in not set yet at this point:
export MY_GITHUB_ACCT="wilsonmar"
export MY_GITHUB_REPO="azure-quickly"
export MY_REPO_FOLDER="azure-quickly"
# To be specified in script call parms:"
export RMV_GITHUB_BEFORE=false    # parm -d
export DO_GITHUB_CLONE=false      # parm -c
export RMV_SETMEM_BEFORE=false    # parm -?

echo ">>> At root for first-time setup ..."
cd
STRING="export PATH=\"\$PATH:\$HOME\" "
if grep -q "$MY_REPO_FOLDER" "$HOME/.bashrc"; then
   echo ">>> \"${MY_REPO_FOLDER}\" already in .bashrc. Not updated."
else
   echo ">>> Appending \"${MY_REPO_FOLDER}\" to bottom of ~/.bashrc "
   echo "export PS1=\"\n  \w\[\033[33m\]\n$ \" " >> ~/.bashrc
   echo "alias get='git fetch;' " >> ~/.bashrc
   echo "cd clouddrive" >> ~/.bashrc
   echo "source setmem.sh" >> ~/.bashrc
   echo "cd ${MY_REPO_FOLDER}" >> ~/.bashrc
   echo "#" >> ~/.bashrc
fi

# If in Cloud Shell, if not already in folder:
cd
if [[ -d "clouddrive" ]]; then
   echo ">>> cd into clouddrive "
   cd clouddrive
fi
pwd


function thisfile_DO_GITHUB_CLONE() {
   echo ">>> Cloning $MY_REPO_FOLDER "
   time git clone "https://github.com/${MY_GITHUB_ACCT}/${MY_GITHUB_REPO}.git" --depth 1 
   cd "$MY_REPO_FOLDER"
   pwd
}
if [ -d "$MY_REPO_FOLDER" ]; then
   if [ "${RMV_GITHUB_BEFORE}" = true ]; then  # param -d 
      echo ">>> Removing folder $MY_REPO_FOLDER "
      time rm -rf "$MY_REPO_FOLDER"
      thisfile_DO_GITHUB_CLONE
   else
      echo ">>> Found folder $MY_REPO_FOLDER "
      cd "$MY_REPO_FOLDER"
      git config pull.rebase false
      git pull
   fi 
else   #  "$MY_REPO_FOLDER" not found:
   if [ "${DO_GITHUB_CLONE}" = true ]; then  # param -c
      thisfile_DO_GITHUB_CLONE
   # else leave no trace.
   fi
fi


echo ">>> Enable all shell files to execute:"
   chmod +x *.sh

echo ">>> Install Azure Providers  "
# Per https://microsoftlearning.github.io/AI-102-AIEngineer/Instructions/00-update-resource-providers.html
time source az-providers-setup.sh

echo ">>> az extension add -n ml [for az ml commands] "
az extension add -n ml

echo ">>> Install Python components  "
# Per https://microsoftlearning.github.io/AI-102-AIEngineer/Instructions/00-setup.html
   pip install flask requests python-dotenv pylint matplotlib pillow
   pip install --upgrade numpy

echo ">>> Copy from \"setmem-sample.sh\" file to \"../setmem.sh\" "
# where it will never be uploaded to any repository (GitHub, GitLab, etc.). 
pwd
function thisfile_INSTALL_SETMEM() {
   echo ">>> Copying setmem.sh from $MY_GITHUB_REPO "
   cp setmem-sample.sh ../setmem.sh
}
if [[ -f ../setmem.sh ]]; then  # file found:
      echo ">>> file found:"
   if [ "${RMV_SETMEM_BEFORE}" = true ]; then  # param -d 
      echo ">>> removing file "
      rm -rf ../setmem.sh
      thisfile_INSTALL_SETMEM
   fi
else
    echo ">>> file not installed yet "
      thisfile_INSTALL_SETMEM
fi
pwd
source ~/.bashrc
