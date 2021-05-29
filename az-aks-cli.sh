#!/bin/bash

# az-aks-cli.sh
# This script was adapted from https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/19/azure_cli_sample.sh
# released under the MIT license. See https://github.com/fouldsy/azure-mol-samples-2nd-ed/blob/master/LICENSE
# and chapter 19 (page 290) of the ebook "Learn Azure in a Month of Lunches - 2nd edition" (Manning Publications) by Iain Foulds,
# Purchase at https://www.manning.com/books/learn-azure-in-a-month-of-lunches-second-edition

set -o errexit

echo "This is not usable at the moment."
exit

if [[ -z $MY_RG ]]; then
   source ../setup.sh   # in folder above this.
fi


# Create a resource group
az group create --name "${MY_RG}" --location "${MY_LOC}"

# aks installed by default. See https://docs.microsoft.com/en-us/azure/cloud-shell/features#tools
#echo "<<< Install the kubectl CLI for managing the Kubernetes cluster:"
# az aks install-cli --install-location /usr/local/bin
   # https://github.com/MicrosoftDocs/azure-docs/issues/6609
   # Downloading client to "/usr/local/bin/kubectl" from "https://storage.googleapis.com/kubernetes-release/release/v1.21.0/bin/linux/amd64/kubectl"
   # Connection error while attempting to download client ([Errno 13] Permission denied: '/usr/local/bin/kubectl')

echo "<<< Create a Dockerfile:"
cat <<EOF > Dockerfile
FROM nginx:1.17.5
EXPOSE 80:80
COPY index.html /usr/share/nginx/html
EOF

echo "<<< Create an Azure Container Instance:"
# A public image from Dockerhub is used as the source image for the container,
# and a public IP address is assigned. To allow web traffic to reach the 
# container instance, port 80 is also opened
az container create \
    --name "${MY_CONTAINER}" \
    --image "${MY_DOCKERHUB_ACCT}"/"${MY_CONTAINER}" \
    --ip-address public \
    --ports 80 \
    --resource-group "${MY_RG}"

echo "<<< Show the container instance public IP address:"
az container show \
    --name "${MY_CONTAINER}" \
    --query ipAddress.ip \
    --output tsv \
    --resource-group "${MY_RG}"

echo "<<< Create an Azure Container Service with Kubernetes (AKS) cluster:"
# Two nodes are created. 
az aks create \
  --name "${MY_CONTAINER}" \
  --node-count 2 \
  --vm-set-type VirtualMachineScaleSets \
  --zones 1 2 3 \
    --resource-group "${MY_RG}"
# It can take ~10 minutes for this operation to successfully complete.

echo "<<< Get the AKS credentials:"
# This gets the Kuebernetes connection information and applies to a local
# config file. You can then use native Kubernetes tools to connect to the
# cluster.
az aks get-credentials \
    --name "${MY_CONTAINER}" \
    --resource-group "${MY_RG}"

   # Merged "azuremol" as current context in /home/wilson/.kube/config

echo "<<< Kubernetes client version:"
kubectl version -c 

echo "<<< Start a Kubernetes deployment:"
# This deployment uses the same base container image as the ACI instance in
# a previous example. Again, port 80 is opened to allow web traffic.
# https://stackoverflow.com/questions/52890718/kubectl-run-is-deprecated-looking-for-alternative
kubectl run --generator=run/v1 "${MY_CONTAINER}" \
    --image=docker.io/"${MY_DOCKERHUB_ACCT}"/"${MY_CONTAINER}":latest \
    --port=80 

# FIXME: We need the new way to replace 
# --generator=deployment/v1beta1 \  # has been deprecated since k8s v1.17 https://kubernetes.io/docs/reference/kubectl/conventions/
   # Error: unknown flag: --generator=run-pod/v1
   # --generator=run/v1 from https://unofficial-kubernetes.readthedocs.io/en/latest/user-guide/kubectl-conventions/
# NOTE: Moving to kubectl create command, loses the ability to fully customize generated Deployment. For example, 
   # it is no longer possible to define replicas (--replicas option), resources (--requests and --limits options) 
   # or implicitly create an associated Service with --expose option.


echo "<<< Create a load balancer for Kubernetes deployment:"
# Although port 80 is open to the deployment, external traffic can't reach the
# Kubernetes pods that run the containers. A load balancer needs to be created
# that maps external traffic on port 80 to the pods. Although this is a
# Kubernetes command (kubectl) under the hood an Azure load balancer and rules
# are created
kubectl expose deployment/"${MY_CONTAINER}" \
    --type="LoadBalancer" \
    --port 80
    
echo "<<< View the public IP address of the load balancer:"
# It can take 2-3 minutes for the load balancer to be created and the public
# IP address associated to correctly direct traffic to the pod
kubectl get service

echo "<<< Scale out the number of nodes in the AKS cluster:"
# The cluster is scaled up to 3 nodes
az aks scale \
    --name "${MY_CONTAINER}" \
    --node-count 3 \
    --resource-group "${MY_RG}"

echo "<<< Scale up the number of replicas:"
# When our web app container was deployed, only one instance was created. Scale
# up to 5 instances, distributed across all three nodes in the cluster
kubectl scale deployment "${MY_CONTAINER}" --replicas 5

