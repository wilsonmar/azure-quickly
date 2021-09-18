#!/usr/bin/env bash
# shellcheck disable=SC2001 # See if you can use ${variable//search/replace} instead.
# shellcheck disable=SC1090 # Can't follow non-constant source. Use a directive to specify location.
# shellcheck disable=SC2129  # Consider using { cmd1; cmd2; } >> file instead of individual redirects.

# source ./az-spring-init.sh within https://github.com/wilsonmar/azure-quickly
# explained in https://wilsonmar.github.io/spring
# and https://docs.microsoft.com/en-us/learn/modules/azure-spring-cloud-workshop/2-create-instance

az extension add -n spring-cloud -y

az configure --defaults group=${RESOURCE_GROUP_NAME}
az configure --defaults spring-cloud=${SPRING_CLOUD_NAME}
# The name of an Azure Spring Cloud cluster should be unique across all of Azure.

echo ">>> Create the Azure Spring Cloud instance:"
az spring-cloud create \
    -g "$RESOURCE_GROUP_NAME" \
    -n "$SPRING_CLOUD_NAME" \
    --sku standard \
    --enable-java-agent

# The Azure Spring Cloud used by Spring Boot microservices is managed and supported by 
# a Spring Cloud Config Server. Its configuration data can be obtained from a Git repository, 
# https://docs.microsoft.com/en-us/learn/modules/azure-spring-cloud-workshop/3-configure-server

echo ">>> Create an app"
az spring-cloud app create --name todo-service \
   --service "$SPRING_CLOUD_NAME" \
   --resource-group "$RESOURCE_GROUP_NAME" 
 
 # Create a MySQL database
 az mysql server create \
    --name ${SPRING_CLOUD_NAME}-mysql \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --sku-name B_Gen5_1 \
    --storage-size 5120 \
    --admin-user "spring"

# create a todos database in that server, and open up its firewall so that Azure Spring Cloud can access it:
az mysql db create \
    --name "todos" \
    --server-name ${SPRING_CLOUD_NAME}-mysql
az mysql server firewall-rule create \
    --name ${SPRING_CLOUD_NAME}-mysql-allow-azure-ip \
    --resource-group "$RESOURCE_GROUP_NAME" \
    --server ${SPRING_CLOUD_NAME}-mysql \
    --start-ip-address "0.0.0.0" \
    --end-ip-address "0.0.0.0"

# Create a Spring Boot microservice https://start.spring.io/
# https://docs.microsoft.com/en-us/learn/modules/azure-spring-cloud-workshop/4-build-spring-boot-microservice
curl https://start.spring.io/starter.tgz -d dependencies=web,mysql,data-jpa,cloud-eureka,cloud-config-client \
   -d baseDir=todo-service \
   -d bootVersion=2.3.6.RELEASE \
   -d javaVersion=1.8 | tar -xzvf -    

# Create a Spring Cloud Gateway
curl https://start.spring.io/starter.tgz -d dependencies=cloud-gateway,cloud-eureka,cloud-config-client \
   -d baseDir=todo-gateway \
   -d bootVersion=2.3.6.RELEASE \
   -d javaVersion=1.8 | tar -xzvf -
