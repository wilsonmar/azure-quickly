# 天蓝色快速

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 目录

-   [语言](#Language)
-   [想象](#Vision)
-   [全部列表](#Todos)
-   [安装](#Install)
-   [Shell 脚本编码技巧](#ShellCoding)
-   [用法](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [参考](#References)
-   [维护者](#maintainers)
-   [贡献](#contributing)
-   [执照](#license)
-   [伦理](#Ethics)

## 语言

这里的所有代码、注释和文档都是用美国英语编写的。这样我们就可以与世界各地的开发者分享我们的经验，翻译归功于<https://github.com/dephraiim/translate-readme>

-   [英语](README.md)
-   [简体中文](README.zh-CN.md)
-   [繁体中文](README.zh-TW.md)
-   [印地语](README.hi.md)
-   [法语](README.fr.md)
-   [阿拉伯](README.ar.md)<br /><br />

Most scripts in this repo are <strong>在 MacOS 和 Linux 上本机运行的 Bash shell 脚本</strong>.

脚本代码可以在 Windows Git Bash Shell 上运行。 
PowerShell 脚本用于唯一解决方案的情况。

为了处理更多的复杂性，程序编码为<a target="_blank" href="https://wilsonmar.github.io/python/">Python</a>或者<a target="_blank" href="https://wilsonmar.github.io/golang">去</a>语言可以称为<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">在适当的时候</a>充分利用他们的能力。

存在以下风险：CLI 功能在其底层时可能无法工作<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">Azure REST API</a>确实有效。因此，适当时会包含 Postman 文件。

## 想象

使用这个repo可以<strong>节省您的时间和金钱</strong>并给你一些心灵的平静和幸福。

人们让资源保持运行是因为他们<strong>不想把一生都花在重复体力劳动上</strong>单击 Azure 门户 GUI，如大多数 Azure 教程所述。

这个仓库（位于<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>）包含自动化脚本，使您能够自信地<strong>删除资源组</strong>当您休息或玩耍时，因为它使您能够<strong>拿回资源</strong>即使使用全新的订阅，也只需几个命令。

您可以节省金钱，因为您不必让资源保持运行、消耗积分或增加信用卡账单。

通过 Azure 门户准确地重复手动鼠标操作和打字（无法快速重复）是很有压力的。

因此，本自述文件解释了如何使用 CLI Bash 终端从头开始启动自定义环境。

<a name="Todos"></a>

## 全部列表

-   添加别名.sh
-   进行测试以确保脚本代码可以在 Windows Git Bash Shell 上运行。
-   一个<strong>变量审查</strong>脚本在调用之前验证内存变量。

<a name="Install"></a>

## 安装

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

以下是每个 Azure 订阅的一次性活动，我的深入而简洁的教程中对此进行了介绍：

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

它涵盖了创建免费的 Azure 帐户和 Azure 存储帐户以将文件保存在云驱动器中：

1.  获取 Azure 订阅（例如通过购买 Visual Studio 许可证）。

2.  使用互联网浏览器（Google Chrome）来解决<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>并登录。

3.  处于<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>或单击门户中的 CLI 图标。

4.  创建一个存储帐户<strong>云盘</strong>壳内。

### 为新订阅设置环境

1.  三击以下命令以突出显示它：

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  右键单击突出显示的内容并选择“复制”将突出显示的内容暂时保存在剪贴板中。

3.  进来<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>或者输入后点击CLI图标<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  右键单击 CLI Bash 终端窗口上的任意位置，然后按<strong>命令+V</strong>从剪贴板粘贴。

5.  按 Enter 运行脚本。运行需要几分钟。

    执行的步骤<a href="#az-setup-cli.sh">脚本“az-setup-cli.sh”如下所述</a>.

    完成后，您应该在左侧看到包含脚本和提示的文件夹，它将在每个命令之后保留在此处（而不是在文件夹路径的末尾）：

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### 自定义 setmem.sh 值

初始化脚本还从示例中建立<strong>设置内存脚本</strong>它定义内存中的环境变量值来控制脚本操作。请注意，setmen 文件所在的文件夹比脚本代码推送到 github 的文件夹要高。那是因为

1.  使用内置的 Visual Studio Code 编辑器编辑文件 setmem.sh：

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  切换到门户 GUI。

3.  打开订阅边栏选项卡。单击您当前的订阅。

4.  单击订阅代码旁边的复制图标（以便将其保存到剪贴板）。

5.  切换到代码编辑器窗口。突出显示变量 MY_SUBSCRIPTION_ID 中的现有文本，然后按“粘贴”（在 Mac 上按 Command+V，在 Windows 上按 Ctrl+V）。

    每个环境可能有不同的文件（例如 dev 与 prod）。

6.  单击代码编辑器窗口右侧的“...”菜单进行保存，然后退出。

    现在您可以运行脚本来创建和管理资源。 
    大多数脚本引用了 Microsoft Learn、CloudAcademy、Pluralsight、Coursera 等的教程。

    要在 Azure 机器学习工作室中运行，您需要一个或多个 Azure ML 工作区、计算、见解和 Key Vault 实例。
    创建它们：

### 使用 az ml cli v2 创建工作区

ML CLI v2（预览版）提供了一种自动化方法：<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  运行我修改后的脚本以使用环境变量和其他编辑：

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    该脚本执行 git 克隆到环境中。

    ### 根据您的喜好配置别名

2.  编辑<tt>aliases.sh</tt>文件并删除或添加键盘宏。

现在您已经拥有所需的资源：

<a name="ShellCoding"></a>

## Shell 脚本编码技巧

此存储库中的 Bash 脚本内的内容是使用以下定义的编码约定编写的<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>其中包括：

-   <tt>来源 ./az-all-start.sh</tt>设置环境变量和实用函数。

-   <tt>设置-O 凸起</tt>使脚本在出现第一个错误时停止（而不是继续运行）。

-   创建一个新的资源组和所有资源<strong>每次运行都有新内容</strong>降低幂等性编码的复杂性（每次重新运行结束时状态相同）。

-   <tt>--资源组</tt>是许多命令的必需参数。它是最后一个，因此上面的一行缺少斜线会导致命令失败。

-   同一 az shell 命令中行尾的反斜杠 \\ 字符继续该命令。

-   控制Python程序的变量（规范）数据通过将它们保存为变量来传递给Python程序<strong>.env 文件</strong>与 Python 程序位于同一文件夹中。

Jupyter 的 Python 笔记本图库：

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## 用法

针对每个会话尝试以下每项活动（假设您执行了上面的安装）：

### 运行单独的 .ipynb 文件

根据<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">如何运行 Jupyter</a>:

1.  前往<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure 机器学习工作室</a>

2.  单击创建的实例。

3.  单击“<https://ml.azure.com/?tid=...">“Studio Web URL”下的 URL。

4.  如果出现“开始”弹出对话框，请单击 X 将其关闭。

5.  单击“笔记本”。

    ### 将 Git 存储库克隆到您的工作区文件系统中

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  将鼠标悬停在您的用户名上（在“用户”中），然后单击“...”以选择“上传文件”。

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  导航到文件夹<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">快速地</a>
    -   光GBM
    -   火炬
    -   r
    -   张量流<br /><br />

    ### MNIST

az ml job create -f jobs/train/lightgbm/iris/job.yml --setcompute.target=local --web --stream

1.  导航至<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  选择“job.yml”。

3.  点击“上传”。

4.  选择运行笔记本的计算位置。

    当第一个单元运行时，停止的计算实例将自动启动。

5.  单击“运行”图标。

    ### 交替

6.  在<strong>用户文件</strong>您工作空间的一部分。单击您要编辑的单元格。如果您在本部分中没有任何笔记本，请参阅在工作区中创建和管理文件。

来自我的 azure-quickly 存储库的更多脚本：

-   使用 API 运行 Bing 搜索：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   创建一个 Azure Key Vault 供以下脚本使用：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    （可选）在其中添加一个秘密；显示秘密；删除秘密；恢复秘密；创建一个虚拟机；托管服务身份；更新权限；自定义脚本扩展；应用自定义脚本扩展：

-   创建机器学习工作区以使用 JupyterLab 运行 iPython Notebook：

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   使用 Azure 认知服务：

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   使用 Helm 图表

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   创建具有公共 IP 地址的虚拟机：

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   创建应用服务计划、Azure Web 应用、部署以显示 MY_APPNAME。

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   创建一个具有两个子网和一个保护入站流量的网络安全组的网络。一个子网用于远程访问流量，一个子网用于运行 Web 服务器的虚拟机的 Web 流量。然后创建两个虚拟机。一种允许 SSH 访问并应用适当的网络安全组规则。您将此虚拟机用作<strong>SSH 跳线盒</strong>然后连接到可用作 Web 服务器的第二个虚拟机：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   创建具有公共 IP 地址的虚拟机。启用的是存储帐户、应用了 VM 诊断扩展的启动诊断：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   创建虚拟机；恢复服务保管库（一种备份策略）会在开始初始备份作业之前创建虚拟机并应用备份策略。

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   从 Dockerfile 创建 Docker 容器；创建AKS；扩大副本规模

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    该 IP 显示“容器中的披萨午餐月”网站（负载平衡）。

-   为 WebApp 创建 IoT：

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   创建 Azure 函数：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Azure CLI 中不提供多个 Functions 组件，因此需要在 Azure 门户上执行手动操作来填补空白。
     请参阅“午餐月”电子书。

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

该脚本应执行以下所有步骤：

1.  可选：编辑<tt>.bashrc</tt>文件来自定义提示：

    如果你在<strong>云壳</strong>（运行 Linux 操作系统），将这些行添加到<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    PS1 设置提示，使其每行都出现在屏幕上的同一位置，位于当前文件夹和文件路径下（而不是在屏幕上各个点的右侧）。

    文件最后一行的“#”是对系统自行添加的 PS1 进行注释的 hack。

2.  导航到保存要下载的存储库的文件夹：

    在 Cloud Shell 中，它是<br /><tt><strong>cd 云壳</strong></tt>

    或者，在我的笔记本电脑上，我使用<br /><tt>cd gmail_acct</tt>

3.  删除以前的 repo 文件夹：

    PROTIP：在命令前面添加一个时间代理命令，用于标识每次运行该命令花费的时间。例如，“0m4.559s”表示大约4.6秒。

4.  下载此存储库以建立运行环境：

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--深度1</tt>指定仅下载最新版本，以节省所用空间。

    <tt>LS</tt>列出文件夹和文件以确认下载确实发生。

5.  授予所有 shell 文件运行权限：

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  运行脚本来设置 Azure 提供商：

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    响应是添加的提供者列表。

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

    上述只需要执行一次，但再次运行不会有什么害处。

7.  授予 setmem.sh 运行权限并运行它：

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  将“sample-setmem.sh”移动（复制并重命名）到文件“setmem.sh”

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    PROTIP：我们将文件移动到永远不会上传到任何存储库（GitHub、GitLab 等）的位置。

### 在 setmem.sh 中手动自定义值

9.  使用程序“code”（Visual Studio Code）打开文件进行编辑：

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>使用它是因为包含机密的文件位于永远不应该推送到 GitHub 的文件夹中。

10. 使用文本编辑器程序编辑 ../setmem.sh 文件：

    脚本已<strong>广义的</strong>通过环境变量替换脚本中的硬编码值。 PROTIP：使用变量而不是硬编码可以避免拼写错误和错误配置。

    下面的行定义了每个变量的值，以便多次运行可以使用不同的值，而无需更改脚本文件。

11. 在<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com 订阅刀片</a>，选择您要使用的订阅，然后单击图标复制到剪贴板。

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    在文件中，突出显示 ID 并将其粘贴：

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. 在<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com 租户刀片</a>，选择您要使用的租户，然后单击图标复制到剪贴板。

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    在文件中，突出显示 ID 并将其粘贴：

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    TODO：用从长期运行的 Azure KeyVault 中检索机密的调用来替换机密的导出语句。但其他人不会查看此文件，除非他们使用你的帐户正确登录到 Azure。

13. 编辑 MY_LOC（位置 = 区域）和其他默认值。

14. 在文件底部，添加一条打印出其中一个变量的语句，以便您知道导出语句采用了：

    在 Bash 脚本中：

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. 保存文件。在 Cloud Shell 中，按 command+Q 或单击“...”以按“保存”，然后按“关闭”。

### 每一次工作会议

1.  在每个会话开始时，调用自定义脚本存储库上方文件夹中的脚本：

    <pre><strong>source ../setmem.sh
    </strong></pre>

    注意：使用“source”运行脚本，以便脚本中定义的环境变量在脚本完成后可见，并由您从中启动的任何程序继承。这是因为源在当前 shell 中运行脚本。但请注意，任何退出语句都会停止运行。

    交替，

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    执行后，您仍然可以在运行另一个脚本之前覆盖变量值。

    这就是您可以为多个区域/位置运行脚本的方法 - 只需更改<tt>我的位置</tt>环境变量的值并再次运行脚本。

2.  原型：<strong>删除资源组</strong>阻止虚拟服务器上累积费用：

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt> - 是的</tt>在 az 命令输入“y”以自动应答请求之前：<br />您确定要执行此操作吗？ （是/否）： 是

<hr />

## 参考

这里的脚本改编自慷慨分享代码的多位专家：

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>作者：Iain Foulds，解释于<https://aka.ms/monthoflunches>2020 年 4 月 30 日发布。

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>由微软

-   <https://github.com/timothywarner/az400>& 蒂姆·华纳的 az303

-   <https://github.com/zaalion/oreilly-azure-app-security>通过礼萨·萨利希

-   <https://github.com/Azure/azure-quickstart-templates>（ARM 模板）

-   <https://github.com/johnthebrit/AzureMasterClass>PowerShell 脚本

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   天际线学院

-   咕噜声（Terraform）

-   CloudPosse（AWS 的 Terraform）<br /><br />

## 维护者

[@wilsonmar](https://github.com/wilsonmar)

## 贡献

PR 已被接受。

如果编辑本自述文件，请遵守[标准自述文件](https://github.com/RichardLitt/standard-readme)规格。

## 执照

©2021 威尔逊·玛尔

## 伦理

该项目在 W3C 的框架下运作[道德和职业行为准则](https://www.w3.org/Consortium/cepc):

> W3C 是一个不断发展的全球性社区，参与者可以选择在其中工作
> 在一起，并在这个过程中经历语言、地点的差异，
> 国籍、经验。在如此多元化的环境下，误解
> 有时会出现分歧，但在大多数情况下可以通过非正式方式解决。在
> 然而，在极少数情况下，行为可能会恐吓、骚扰或以其他方式扰乱一个人
> 或者社区中有更多的人，W3C 不会容忍这种情况。
>
> 道德和职业行为准则有助于定义公认的和
> 可接受的行为并促进高标准的专业
> 实践。它还为自我评价提供了基准，并作为
> 更好地展现组织形象的工具。

我们希望我们的社区团体按照这些准则行事，并且
参与者互相要求遵守这些高标准。如有任何问题
或者担心代码没有被遵循，请联系存储库的所有者。
