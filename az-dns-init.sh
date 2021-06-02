#!/usr/bin/env bash

# ./az-dns-init.sh within https://github.com/wilsonmar/azure-quickly
# To implement LAB https://microsoftlearning.github.io/AZ-304-Microsoft-Azure-Architect-Design/Instructions/Labs/Module_4_Lab.html
# Test-AzDnsAvailability 
# within 

set -o errexit

if [[ -z $MY_RG ]]; then
   echo ">>> Running $PWD/setup.sh ..."
   source ../setup.sh   # in folder above this.
fi


# Identify an available DNS name for use in the next task "
# PowerShell: Test-AzDnsAvailability -DomainNameLabel <custom-label> -Location '<location>'
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

