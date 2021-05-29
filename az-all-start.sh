#!/usr/bin/env bash
# shellcheck disable=SC2001 # See if you can use ${variable//search/replace} instead.
# shellcheck disable=SC1090 # Can't follow non-constant source. Use a directive to specify location.
# shellcheck disable=SC2129  # Consider using { cmd1; cmd2; } >> file instead of individual redirects.

# source ./az-all-start.sh within https://github.com/wilsonmar/azure-your-way
# This Bash script is explained in https://wilsonmar.github.io/bash-scripts.
# This script is called by others to performs standard actions for all scripts:
# 1. Capture and display start of script time stamp.

### 1. Capture a time stamp to later calculate how long the script runs, no matter how it ends:
THIS_PROGRAM="$0"
SCRIPT_VERSION="v0.72"
EPOCH_START="$( date -u +%s )"  # such as 1572634619
LOG_DATETIME=$( date +%Y-%m-%dT%H:%M:%S%z)-$((1 + RANDOM % 1000))
# clear  # screen (but not history)
echo "=========================== $LOG_DATETIME $THIS_PROGRAM $SCRIPT_VERSION"

#if [[ -z "${MY_RG+x}" ]]; then
   source ../setmem.sh   # in folder above this.
#git fi

### 3. Define devault values for script invocation parameter "feature flags" not specified:
   CLONE_GITHUB=false           # -c
   CONTINUE_ON_ERR=false        # -E
   REMOVE_GITHUB_AFTER=false    # -R
   RUN_DEBUG=false              # -vv
   RUN_QUIET=false              # -q
   RUN_VERBOSE=false            # -v
   SET_TRACE=false              # -x
   RMV_RG_BEFORE=true       # parm -RRGb
   RMV_RG_AT_END=false       # parm -RRGe
   RMV_GITHUB_BEFORE=false   # parm -RGb
   RMV_GITHUB_AT_END=false   # parm -RGe
   DO_GITHUB_CLONE=true      # parm -c

### 4. Set variables associated with each parameter flag
while test $# -gt 0; do
  case "$1" in
    -c)
      export DO_GITHUB_CLONE=true   # CLONE_GITHUB
      shift
      ;;
    -RGb)
      export RMV_GITHUB_BEFORE=true
      shift
      ;;
    -RGe)
      export RMV_GITHUB_AT_END=true
      shift
      ;;
    -RRGb)
      export RMV_RG_BEFORE=true
      shift
      ;;
    -RRGe)
      export RMV_RG_AT_END=true
      shift
      ;;
    -E)
      export CONTINUE_ON_ERR=true
      shift
      ;;
    -q)
      export RUN_QUIET=true
      shift
      ;;
    -vv)
      export RUN_DEBUG=true
      shift
      ;;
    -v)
      export RUN_VERBOSE=true
      shift
      ;;
    -x)
      export SET_TRACE=true
      shift
      ;;
    *)
      error "Parameter \"$1\" not recognized. Aborting."
      exit 0
      break
      ;;
  esac
done

### 5. Custom functions to echo text to screen
# \e ANSI color variables are defined in https://wilsonmar.github.io/bash-scripts#TextColors
h2() { if [ "${RUN_QUIET}" = false ]; then    # heading
   printf "\n\e[1m\e[33m\u2665 %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
   fi
}
info() {   # output on every run
   printf "\e[2m\n➜ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
note() { if [ "${RUN_VERBOSE}" = true ]; then
   printf "\n\e[1m\e[36m \e[0m \e[36m%s\e[0m" "$(echo "$@" | sed '/./,$!d')"
   printf "\n"
   fi
}
success() {
   printf "\n\e[32m\e[1m✔ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
error() {    # &#9747;
   printf "\n\e[31m\e[1m✖ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
warning() {  # &#9758; or &#9755;
   printf "\n\e[5m\e[36m\e[1m☞ %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}
fatal() {   # Skull: &#9760;  # Star: &starf; &#9733; U+02606  # Toxic: &#9762;
   printf "\n\e[31m\e[1m☢  %s\e[0m\n" "$(echo "$@" | sed '/./,$!d')"
}

if [ "${RUN_DEBUG}" = true ]; then  # -vv
   h2 "Header here"
   info "info"
   note "note"
   success "success!"
   error "error"
   warning "warning (warnNotice)"
   fatal "fatal (warnError)"
fi


if [ "${CONTINUE_ON_ERR}" = true ]; then  # -E
   warning ">>> Set to continue despite error ..."
else
   note ">>> Set -e (error stops execution) ..."
   set -e  # exits script when a command fails
   set -o errexit
   # ALTERNATE: set -eu pipefail  # pipefail counts as a parameter
fi

if [ "${SET_TRACE}" = true ]; then
   h2 "Set -x ..."
   set -x  # (-o xtrace) to show commands for specific issues.
fi
# set -o nounset

if [ "${RUN_VERBOSE}" = true ]; then  # -v
   echo ">>> DEL_RG_BEFORE=$DEL_RG_BEFORE, DEL_RG_AT_END=$DEL_RG_AT_END "
   echo ">>> DEL_GITHUB_BEFORE=$DEL_GITHUB_BEFORE, DO_GITHUB_CLONE=$DO_GITHUB_CLONE, DEL_GITHUB_AT_END=$DEL_GITHUB_AT_END "
   export CMD_GENERAL_PARM="--verbose"
else
   export CMD_GENERAL_PARM=""
fi
echo ">>> CMD_GENERAL_PARM=\"$CMD_GENERAL_PARM\" "


if [[ -z "${MY_SUBSCRIPTION_ID}" ]]; then
   echo ">>> MY_SUBSCRIPTION_ID not defined. Exiting. "
   exit
else
   echo ">>> MY_SUBSCRIPTION_ID \"${MY_SUBSCRIPTION_ID}\" being used. "
   az account set --subscription "$MY_SUBSCRIPTION_ID"
fi


function thisfile_create_rg() {
   echo ">>> Create Resource Group \"$MY_RG\" "
   az group create --name "${MY_RG}" --location "${MY_LOC}"  # -o none
}
if [ "${DEL_RG_BEFORE}" = true ]; then  # param -RGb 
   if [ $( az group exists --name "${MY_RG}" ) == true ]; then
      echo ">>> Delete Resource Group \"$MY_RG\" before recreating ..."
      time az group delete --resource-group "${MY_RG}" --yes
   fi
   thisfile_create_rg
else  # don't delete before
   if [ $( az group exists --name "${MY_RG}" ) == true ]; then
      echo ">>> Using existing \"$MY_RG\" ..."
   else
      thisfile_create_rg
   fi
fi

echo ">>> Set Resource Group \"$MY_RG\" and Location \"${MY_LOC}\" as defaults. "
# See https://docs.microsoft.com/en-us/cli/azure/azure-cli-configuration
az configure --defaults group="${MY_RG}" location="${MY_LOC}"  # for subsequent commands.
