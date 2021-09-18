# azure-quickly

![git-tag](https://img.shields.io/github/v/tag/wilsonmar/azure-quickly)
![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Table of Contents

  - [Table of Contents](#table-of-contents)
  - [Language](#Language)
  - [Vision](#Vision)
  - [Infrastructure](#Infrastructure)
  - [Install](#Install)
  
  - [Usage](#Usage)
  - [Shell Coding](#ShellCoding)
  - [az-setup-cli.sh](#az-setup-cli.sh)
  
  - [References](#References)
  - [Todo List](#Todos)
  - [Maintainers](#maintainers)
  - [Contributing](#contributing)
  - [License](#license)
  - [Ethics](#Ethics)

## Language

The development language is English. All comments and documentation should be written in English, so that we don't end up with “franglais” methods, and so we can share our learnings with developers around the world.


## Vision

Using this repo can <strong>save you time and money</strong> and give you some peace of mind and happiness.

Why and How?

People leave resources running because they <strong>don't want to spend their life repeating the manual toil</strong> of clicking though the Azure Portal GUI, as described by most Azure tutorials.

This repo (at <a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https://github.com/wilsonmar/azure-quickly</a>) contains automation scripts which enable you to confidently <strong>delete Resource Groups</strong> when you're resting or playing becuase it enables you to <strong>get resources back</strong> with just a few commands, even with a brand-new Subscription.

You save money because you don't have to leave resources running, consuming credits or running up your credit card bill.

It's stressful to accurately repeat the manual mousing and typing through the Azure Portal (which is not quickly repeatable).

Most scripts in the rep are <strong>Bash shell scripts that run natively on MacOS and Linux</strong>. PowerShell scripts are used in cases where they are the only solution. Script code can run on Windowsw Git Bash Shell. However, there is a risk that CLI functions may not work when its underlying <a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">REST API</a> does work. So Postman files are included when appropriate. 

Additionally, some Bash scripts calls PowerShell commands when PowerShell is the only solution. 
Python or Go programs may be called <a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">when appropriate</a> to take advantage of their capabilities.


<a name="Infrastructure"></a>

## Infrastructure: How this works internally

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

After you get a new subscription and use the portal to create a storage account for a <strong>clouddrive</strong> within the shell, this tutorial explains how you can initiate your custom environment from scratch in the CLI Bash terminal. In there, from the github README we copy a bash command and <strong>paste</strong> it in the shell. The script both downloads and runs an initialization script. That init script clones from GitHub a repo containing various scripts that can run alone or be called by the <strong>deploy</strong> script. The init script also establishes from a sample the <strong>setmem script</strong> which defines environment variable values in memory to control script operation. Note that the setmen file is in a higher folder than where script code may be pushed to github. That's because the setmem file is manually edited with values private to the individual subscription. There may be a different file for each environment (such as dev vs. prod). When one of the scripts run, it can call setmem to establish the memory variables it needs. Optionally, parameter flags such as <strong>–v for verbose</strong> display can be specified. A <strong>variables vetting</strong> script may also be called to validate the memory variables before invocation. Alternately, instead of a setmem script, we can edit a JSON specification file and which a Python program reads to update environment variables.


<a name="Install"></a>

## Install

1. First, get fundamental skill at installing and using Azure Portal and CLI Bash by following my deep yet concise tutorial at:

   <a target="_blank" href="https://wilsonmar.github.io/azure-cloud-onramp/">https://wilsonmar.github.io/azure-cloud-onramp</a>

   It covers creation of free Azure accounts and Azure Storage accounts to hold files in a clouddrive.

1. Be in <a target="_blank" href="https://shell.azure.com/">https://shell.azure.com</a><br />
   or click the CLI icon after entering<br />
   <a target="_blank" href="https://portal.azure.com/">https://portal.azure.com</a>


   ### Setup an environment for new Subscription

1. Triple-click the command below to highlight it:

   <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

1. Right-click the highlighted     and select "Copy" to save the highlighted temporarily in your Clipboard.

1. Get in <a target="_blank" href="https://shell.azure.com/">https://shell.azure.com</a>
   or click the CLI icon after entering
   <a target="_blank" href="https://portal.azure.com/">https://portal.azure.com</a>

1. Right-click anywhere on the CLI Bash terminal window, then press <strong>command+V</strong> to paste from the Clipboard.

1. Press Enter to run the script. It takes several minutes to run.

   Steps executed by the script "az-setup-cli.sh" are <a href="#az-setup-cli.sh">described in the section below</a>. When done, you should see the folder containing scripts and the prompt at the left, where it will stay after each command (instead of at the end of the folder path):

   <pre>~/clouddrive/azure-quickly
   $ _</pre>


   ### Customize setmem.sh values

1. Use the built-in Visual Studio Code editor to edit file setmem.sh 

   <pre><strong>code ../setmem.sh
   </strong></pre>

1. Switch to the Portal GUI.
1. Open the Subscription blade. Click on your current Subscription. 
1. Click the copy icon next to the Subscription code (so it gets saved to your Clipboard).

1. Switch to the Code editor window. Highlight the existing text in variable MY_SUBSCRIPTION_ID and press Paste (Command+V on Macs or Ctrl+V on Windows).
1. Click the "..." menu to the right of the Code editor window to save, then exit.

   Now you can run scripts to create and manage resources. 
   Most of the scripts reference a tutorial at Microsoft Learn, CloudAcademy, Pluralsight, Coursera, etc.

   To run in the Azure Machine Learning studio, you need one or more instances an Azure ML Workspace, Compute, Insights, and Key Vault.
   To create them:

   ### Create Workspace using az ml cli v2

   The ML CLI v2 (Preview) provides one automation approach:<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1. Run the script I've modified from that to use environment variables and additional edits:

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
   </strong></pre>

   The scipt performs a git clone into the environment.

   Now that you have the Resources needed:


<a name="Usage"></a>

## Usage: Let's Go!


   ### Run individual .ipynb file

   According to <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">How to run Jupyter</a>:

1. Go to the <a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure Machine Learning Studio</a>

1. Click the instance created.
1. Click the "https://ml.azure.com/?tid=..." URL under the "Studio web URL".
1. If the "get started" pop-up dialog appears, click X to dismiss it.
1. Click "Notebooks".
 
   ### Clone Git repositories into your workspace file system

   <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">*</a>

1. Mouse over your user name (among Users) and click the "..." to choose "Upload files".

   <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

1. Navigate to the folders as <a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

   * <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">fastai</a>
   * lightbm
   * pytorch
   * r
   * tensorflow
   <br /><br />

   ### MNIST

az ml job create -f jobs/train/lightgbm/iris/job.yml --set compute.target=local --web --stream

1. Navigate to https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/
1. Select "job.yml".
1. Click "Upload".
1. 
1. Select the compute where to run the Notebook.

   A stopped compute instance will automatically start when the first cell is run.

1. Click the "Run" icon.

   ### Alternately

1. In the <strong>User files</strong> section of your workspace. Click on the cell you wish to edit. If you don't have any notebooks in this section, see Create and manage files in your workspace.

More scripts from my azure-quickly repo:

* Run a Bing Search using API:

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
   </strong></pre>


* Create an Azure Key Vault for use by scripts to follow:

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
   </strong></pre>

   Optionally, put a secret in it; show secret; delete secret; recover secret; create a vm; Managed Service Identity; update permissions; Custom Script Extension; Apply the Custom Script Extension:

* Create a Machine Learning Workspace to run iPython Notebooks using JupyterLab:

   <pre><strong>export MY_MLWORKSPACE_NAME="mela"
   ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
   </strong></pre>
   

* Use Azure Cognitive Services:

   <pre><strong>export MY_COG_ACCT="cogme"
   export MY_COG_PRICING_TIER="F0"  # or S0
   ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
   </strong></pre>

* Use Helm charts

   <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
   </strong></pre>

* Create a VM with a public IP address:

   <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
   </strong></pre>

* Create an App Service Plan, Azure Web App, Deployment, to show MY_APPNAME.

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
   </strong></pre>

* Create a network with two subnets and a network security group that secures inbound traffic. One subnet is for remote access traffic, one is web traffic for VMs that run a web server. Two VMs are then created. One allows SSH access and has the appropriate network security group rules applied. You use this VM as an <strong>SSH jumpbox</strong> to then connect to the the second VM which can be used an web server:

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
   </strong></pre> 

* Create a VM with a public IP address. Enabled are a storage account, boot diagnostics with the VM diagnostics extension applied:

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
   </strong></pre>

* Create a VM; Recovery Services vault, a backup policy, then creates a VM and applies the backup policy before starting the initial backup job.

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
   </strong></pre>

* Create a Docker container from a Dockerfile; Create AKS; Scale up replicas 

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
   </strong></pre>
   
   The IP shows the "Month of Pizza Lunches in a container" website (load balanced).

* Create IoT for WebApp:

   <pre><strong>export MY_PROJECT_FOLDER="iot-project"
  export MY_IOT_HUB_NAME="hubahuba"
  export MY_IOT_HUB_GROUP="hubgroupie"
  ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
   </strong></pre>

* Create Azure Functions:

   <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
   </strong></pre>

   Several Functions components are not available in the Azure CLI, so manual actions are needed on Azure portal to fill in the gaps.
   See the "Month of Lunches" ebook.

https://github.com/Azure/azure-quickstart-templates

<hr />

<a name="ShellCoding"></a>

## Shell Script coding tricks

Bash scripts here are written with coding conventions defined at <a target="_blank" href="https://wilsonmar.github.io/bash-codng">https://wilsonmar.github.io/bash-coding</a> which include:

   * <tt>source ./az-all-start.sh </tt> sets up environment variables and utility functions.

   * <tt>set -o errexit</tt> makes it so that the script stops on the first error (instead of running on).

   * A backslash \ character at the end of a line within the same az shell command continues that command.

   * A new Resource Group and all resources are created new every run to reduce the complexity of coding for idempotency (the status is the same at the end of every re-run).

   * <tt>--resource-group</tt> is a required argument on many commands. It's last so that missing slash line a line above it would cause the command to fail.

   * Variable (specification) data controlling Python programs are passed to Python programs by saving them as variables in an <strong>.env file</strong> in the same folder as the Python program.

Jupyter's Gallery of Python Notebooks:

   * https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks

<hr />
   
<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

   The script should do all the steps below:

1. OPTIONAL: Edit the <tt>.bashrc</tt> file to customize the prompt:
   
   If you're in the <strong>cloud Shell</strong> (which runs the Linux operating system), add these lines to the bottom of the <strong>.bashrc</strong>:
   
   <pre>export PS1="\n  \w\[\033[33m\]\n$ "
   #</pre>

   The PS1 sets the prompt so it appears in the same spot on the screen every line, under the current folder and file path (rather than to the right of it at various points on the screen).

   "#" at the last line of the file is a hack to make a comment out of the PS1 the system adds on its own.

2. Navigate into a folder which holds repository to be downloaded:

   Within Cloud Shell, it's<br />
   <tt><strong>cd cloudshell</strong></tt>

   Alternately, on my laptop, I use<br />
   <tt>cd gmail_acct</tt>

3. Remove the previous repo folder:

   PROTIP: A time proxy command is added in front of commands to identify how many time was taken to run the command each time. For example, "0m4.559s" means about 4.6 seconds.

4. Download this repo to establish a run environment:

   <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
   cd azure-quickly
   ls
   </strong></pre>

   <tt>\-\-depth 1</tt> specifies download of only the latest version, to save space used.

   <tt>ls</tt> lists folders and files to confirm the download actually occurred.

5. Give all the shell file permissions to run:

   <pre><strong>chmod +x *.sh
   </strong></pre>

6. Run script to setup Azure Providers:

   <pre><strong>source az-providers-setup.sh
   </strong></pre>

   The response is a list of providers added.
   <pre>>>> Microsoft.AlertsManagement already Registered.
>>> Microsoft.BotService already Registered.
>>> Microsoft.ChangeAnalysis already Registered.
>>> Microsoft.CognitiveServices already Registered.
>>> Microsoft.Compute already Registered.
>>> Microsoft.ContainerInstance already Registered.
>>> Microsoft.ContainerRegistry already Registered.
>>> Microsoft.Devices already Registered.
>>> Microsoft.Insights already Registered.
>>> Microsoft.KeyVault already Registered.
>>> Microsoft.Notebooks already Registered.
>>> Microsoft.MachineLearningServices already Registered.
>>> Microsoft.ManagedIdentity already Registered.
>>> Microsoft.Search already Registered.
>>> Microsoft.Storage already Registered.
>>> Microsoft.Web already Registered.
   </pre>

   The above only needs to be done once, but running it again won't be harmful.

7. Give setmem.sh permissions to run and run it :

   <pre><strong>chmod +x ../setmem.sh
   source ../setmem.sh
   </strong></pre>

8. Move (copy and rename) "sample-setmem.sh" to file "setmem.sh" 

   <pre><strong>mv setmem-sample.sh ../setmem.sh
   </strong></pre>

   PROTIP: We move the file where it will never be uploaded to any repository (GitHub, GitLab, etc.). 


   ### Manually customize values in setmem.sh

9. Open the file for edit using program "code" (Visual Studio Code):

   <pre><strong>code ../setmem.sh
   </strong></pre>

   <tt>..</tt> is used because the file, containing secrets, is in a folder which should never be pushed to GitHub.

1. Use a text editor program to edit the ../setmem.sh file:

   Scripts have been <strong>generalized</strong> by environment variables substituting for hard-coded values in scripts. PROTIP: Using variable instead of hard-coding avoids typos and misconfigurations.
   
   Lines below define values for each variable so that multiple runs can use different values, without need to change the script file. 

1. In <a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com Subscription blade</a>, select the Subscription you wnat to use, then click the icon to Copy to Clipboard. 

   ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

   In the file, highlight the ID and paste it:

   <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
   export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
   </pre>

1. In <a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com Tenant blade</a>, select the Tenant you wnat to use, then click the icon to Copy to Clipboard. 

   ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

   In the file, highlight the ID and paste it:

   <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
   </pre>

   TODO: Substitute export statements of secrets with calls to retrieve them from a long-running Azure KeyVault. But no one else would be at this file unless they are properly logged into Azure under your account.

1. Edit the MY_LOC (Location = Region) and other defaults.

1. At the bottom of the file, add a statement which prints out one of the variables, so you know the export statements took:

   In a Bash script:

   <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

1. Save the file. In Cloud Shell, press command+Q or clicking the "..." to press Save, then Close.


   ### Each work session

1. At the beginning of each session invoke the script in the folder just above your custom scripts repo:

   <pre><strong>source ../setmem.sh
   </strong></pre>

   NOTE: Using "source" to run the script so that environment variables defined in the script will be visible after the script is done, and be inherited by any programs you launch from it. That's because source runs the script in the current shell. But note that any exit statement would stop the run.

   Alternately,
   <pre>source <(curl -s -L https://example.com/install.sh)</pre>

   After execution, you can still override variable values before running another script.

   That is how you can run scripts for several regions/locations - by changing just the <tt>MY_LOC</tt> environment variable's value and running the script again.

1. PROTIP: <strong>Delete resource groups</strong> to stop charges from accumulating on Virtual Servers:

   <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
   </strong></pre>

   <tt>--yes</tt> before the az command feeds a "y" to automatically answer the request:<br />
   Are you sure you want to perform this operation? (y/n): y


<hr />

## References

Scripts here are adapted from various experts generous with sharing their code:

   * https://github.com/fouldsy/azure-mol-samples-2nd-ed by Iain Foulds, explained in https://aka.ms/monthoflunches published 4/30/2020.

   * https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies
   * https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies
   * https://github.com/Azure/azure-cli by Microsoft

   * https://github.com/timothywarner/az400 & az303 by Tim Warner
   * https://github.com/zaalion/oreilly-azure-app-security by Reza Salehi 
   
   * https://github.com/Azure/azure-quickstart-templates (ARM Templates)
   * https://github.com/johnthebrit/AzureMasterClass PowerShell scripts
   * https://github.com/terraform-providers/terraform-provider-azurerm

   * Skylines Academy
   * Gruntwork (Terraform)
   * CloudPosse (Terraform for AWS)
   <br /><br />

<a name="Todos"></a>

## Todo List

- Add alias.sh

## Maintainers

[@wilsonmar](https://github.com/wilsonmar)

## Contributing

PRs accepted.

If editing this README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## License

MIT © 2021 Wilson Mar

## Ethics

This project operates under the W3C's
[Code of Ethics and Professional Conduct](https://www.w3.org/Consortium/cepc):

> W3C is a growing and global community where participants choose to work
> together, and in that process experience differences in language, location,
> nationality, and experience. In such a diverse environment, misunderstandings
> and disagreements happen, which in most cases can be resolved informally. In
> rare cases, however, behavior can intimidate, harass, or otherwise disrupt one
> or more people in the community, which W3C will not tolerate.
>
> A Code of Ethics and Professional Conduct is useful to define accepted and
> acceptable behaviors and to promote high standards of professional
> practice. It also provides a benchmark for self evaluation and acts as a
> vehicle for better identity of the organization.

We hope that our community group act according to these guidelines, and that
participants hold each other to these high standards. If you have any questions
or are worried that the code isn't being followed, please contact the owner of the repository.
