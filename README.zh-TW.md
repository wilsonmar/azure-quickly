# 天藍色快速

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 目錄

-   [語言](#Language)
-   [想像](#Vision)
-   [全部列表](#Todos)
-   [安裝](#Install)
-   [Shell 腳本編碼技巧](#ShellCoding)
-   [用法](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [參考](#References)
-   [維護者](#maintainers)
-   [貢獻](#contributing)
-   [執照](#license)
-   [倫理](#Ethics)

## 語言

這裡的所有代碼、註釋和文檔都是用美國英語編寫的。這樣我們就可以與世界各地的開發者分享我們的經驗，翻譯歸功於<https://github.com/dephraiim/translate-readme>

-   [英語](README.md)
-   [簡體中文](README.zh-CN.md)
-   [繁體中文](README.zh-TW.md)
-   [印地語](README.hi.md)
-   [法語](README.fr.md)
-   [阿拉伯](README.ar.md)<br /><br />

這個倉庫中的大多數腳本都是<strong>在 MacOS 和 Linux 上本機運行的 Bash shell 腳本</strong>.

腳本代碼可以在 Windows Git Bash Shell 上運行。 
PowerShell 腳本用於唯一解決方案的情況。

為了處理更多的複雜性，程序編碼為<a target="_blank" href="https://wilsonmar.github.io/python/">Python</a>或者<a target="_blank" href="https://wilsonmar.github.io/golang">去</a>語言可以稱為<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">在適當的時候</a> to take advantage of their capabilities.

存在以下風險：CLI 功能在其底層時可能無法工作<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">Azure REST API</a>確實有效。因此，適當時會包含 Postman 文件。

## 想像

使用這個repo可以<strong>節省您的時間和金錢</strong>並給你一些心靈的平靜和幸福。

人們讓資源保持運行是因為他們<strong>不想把一生都花在重複體力勞動上</strong>單擊 Azure 門戶 GUI，如大多數 Azure 教程所述。

這個倉庫（位於<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>）包含自動化腳本，使您能夠自信地<strong>刪除資源組</strong>當您休息或玩耍時，因為它使您能夠<strong>拿回資源</strong>即使使用全新的訂閱，也只需幾個命令。

您可以節省金錢，因為您不必讓資源保持運行、消耗積分或增加信用卡賬單。

通過 Azure 門戶準確地重複手動鼠標操作和打字（無法快速重複）是很有壓力的。

因此，本自述文件解釋瞭如何使用 CLI Bash 終端從頭開始啟動自定義環境。

<a name="Todos"></a>

## 全部列表

-   添加別名.sh
-   進行測試以確保腳本代碼可以在 Windows Git Bash Shell 上運行。
-   一個<strong>變量審查</strong>腳本在調用之前驗證內存變量。

<a name="Install"></a>

## 安裝

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

以下是每個 Azure 訂閱的一次性活動，我的深入而簡潔的教程中對此進行了介紹：

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

它涵蓋了創建免費的 Azure 帳戶和 Azure 存儲帳戶以將文件保存在雲驅動器中：

1.  獲取 Azure 訂閱（例如通過購買 Visual Studio 許可證）。

2.  使用互聯網瀏覽器（Google Chrome）來解決<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>並登錄。

3.  處於<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>或單擊門戶中的 CLI 圖標。

4.  創建一個存儲帳戶<strong>雲盤</strong>殼內。

### 為新訂閱設置環境

1.  三擊以下命令以突出顯示它：

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  右鍵單擊突出顯示的內容並選擇“複製”將突出顯示的內容暫時保存在剪貼板中。

3.  進來<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>或者輸入後點擊CLI圖標<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  右鍵單擊 CLI Bash 終端窗口上的任意位置，然後按<strong>命令+V</strong>從剪貼板粘貼。

5.  按 Enter 運行腳本。運行需要幾分鐘。

    執行的步驟<a href="#az-setup-cli.sh">腳本“az-setup-cli.sh”如下所述</a>.

    完成後，您應該在左側看到包含腳本和提示的文件夾，它將在每個命令之後保留在此處（而不是在文件夾路徑的末尾）：

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### 自定義 setmem.sh 值

初始化腳本還從示例中建立<strong>設置內存腳本</strong>它定義內存中的環境變量值來控制腳本操作。請注意，setmen 文件所在的文件夾比腳本代碼推送到 github 的文件夾要高。那是因為

1.  使用內置的 Visual Studio Code 編輯器編輯文件 setmem.sh：

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  切換到門戶 GUI。

3.  打開訂閱邊欄選項卡。單擊您當前的訂閱。

4.  單擊訂閱代碼旁邊的複製圖標（以便將其保存到剪貼板）。

5.  切換到代碼編輯器窗口。突出顯示變量 MY_SUBSCRIPTION_ID 中的現有文本，然後按“粘貼”（在 Mac 上按 Command+V，在 Windows 上按 Ctrl+V）。

    每個環境可能有不同的文件（例如 dev 與 prod）。

6.  單擊代碼編輯器窗口右側的“...”菜單進行保存，然後退出。

    現在您可以運行腳本來創建和管理資源。 
    大多數腳本引用了 Microsoft Learn、CloudAcademy、Pluralsight、Coursera 等的教程。

    要在 Azure 機器學習工作室中運行，您需要一個或多個 Azure ML 工作區、計算、見解和 Key Vault 實例。
    創建它們：

### 使用 az ml cli v2 創建工作區

ML CLI v2（預覽版）提供了一種自動化方法：<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  運行我修改後的腳本以使用環境變量和其他編輯：

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    該腳本執行 git 克隆到環境中。

    ### 根據您的喜好配置別名

2.  編輯<tt>aliases.sh</tt>文件並刪除或添加鍵盤宏。

現在您已經擁有所需的資源：

<a name="ShellCoding"></a>

## Shell 腳本編碼技巧

此存儲庫中的 Bash 腳本內的內容是使用以下定義的編碼約定編寫的<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>其中包括：

-   <tt>來源 ./az-all-start.sh</tt>設置環境變量和實用函數。

-   <tt>設置-o 豎立</tt>使腳本在出現第一個錯誤時停止（而不是繼續運行）。

-   創建一個新的資源組和所有資源<strong>每次運行都有新內容</strong>降低冪等性編碼的複雜性（每次重新運行結束時狀態相同）。

-   <tt>--資源組</tt>是許多命令的必需參數。它是最後一個，因此上面的一行缺少斜線會導致命令失敗。

-   同一 az shell 命令中行尾的反斜杠 \\ 字符繼續該命令。

-   控制Python程序的變量（規範）數據通過將它們保存為變量來傳遞給Python程序<strong>.env 文件</strong>與 Python 程序位於同一文件夾中。

Jupyter 的 Python 筆記本圖庫：

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## 用法

針對每個會話嘗試以下每項活動（假設您執行了上面的安裝）：

### 運行單獨的 .ipynb 文件

根據<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">如何運行 Jupyter</a>:

1.  前往<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure 機器學習工作室</a>

2.  單擊創建的實例。

3.  單擊“<https://ml.azure.com/?tid=...">“Studio Web URL”下的 URL。

4.  如果出現“開始”彈出對話框，請單擊 X 將其關閉。

5.  單擊“筆記本”。

    ### 將 Git 存儲庫克隆到您的工作區文件系統中

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  將鼠標懸停在您的用戶名上（在“用戶”中），然後單擊“...”以選擇“上傳文件”。

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  導航到文件夾<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">就業</a>
    -   光GBM
    -   火炬
    -   r
    -   張量流<br /><br />

    ### MNIST

az ml job create -f jobs/train/lightgbm/iris/job.yml --setcompute.target=local --web --stream

1.  導航至<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  選擇“job.yml”。

3.  點擊“上傳”。

4.  選擇運行筆記本的計算位置。

    當第一個單元運行時，停止的計算實例將自動啟動。

5.  單擊“運行”圖標。

    ### 交替

6.  在<strong>用戶文件</strong>您工作空間的一部分。單擊您要編輯的單元格。如果您在本部分中沒有任何筆記本，請參閱在工作區中創建和管理文件。

來自我的 azure-quickly 存儲庫的更多腳本：

-   使用 API 運行 Bing 搜索：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   創建一個 Azure Key Vault 供以下腳本使用：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    （可選）在其中添加一個秘密；顯示秘密；刪除秘密；恢復秘密；創建一個虛擬機；託管服務身份；更新權限；自定義腳本擴展；應用自定義腳本擴展：

-   創建機器學習工作區以使用 JupyterLab 運行 iPython Notebook：

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   使用 Azure 認知服務：

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   使用 Helm 圖表

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   創建具有公共 IP 地址的虛擬機：

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   創建應用服務計劃、Azure Web 應用、部署以顯示 MY_APPNAME。

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   創建一個具有兩個子網和一個保護入站流量的網絡安全組的網絡。一個子網用於遠程訪問流量，一個子網用於運行 Web 服務器的虛擬機的 Web 流量。然後創建兩個虛擬機。一種允許 SSH 訪問並應用適當的網絡安全組規則。您將此虛擬機用作<strong>SSH 跳線盒</strong>然後連接到可用作 Web 服務器的第二個虛擬機：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   創建具有公共 IP 地址的虛擬機。啟用的是存儲帳戶、應用了 VM 診斷擴展的啟動診斷：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   創建虛擬機；恢復服務保管庫（一種備份策略）會在開始初始備份作業之前創建虛擬機並應用備份策略。

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   從 Dockerfile 創建 Docker 容器；創建AKS；擴大副本規模

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    該 IP 顯示“容器中的披薩午餐月”網站（負載平衡）。

-   為 WebApp 創建 IoT：

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   創建 Azure 函數：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Azure CLI 中不提供多個 Functions 組件，因此需要在 Azure 門戶上執行手動操作來填補空白。
     請參閱“午餐月”電子書。

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

該腳本應執行以下所有步驟：

1.  可選：編輯<tt>.bashrc</tt>文件來自定義提示：

    如果你在<strong>雲殼</strong>（運行 Linux 操作系統），將這些行添加到<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    PS1 設置提示，使其每行都出現在屏幕上的同一位置，位於當前文件夾和文件路徑下（而不是在屏幕上各個點的右側）。

    文件最後一行的“#”是對系統自行添加的 PS1 進行註釋的 hack。

2.  導航到保存要下載的存儲庫的文件夾：

    在 Cloud Shell 中，它是<br /><tt><strong>cd 雲殼</strong></tt>

    或者，在我的筆記本電腦上，我使用<br /><tt>cd gmail_acct</tt>

3.  刪除以前的 repo 文件夾：

    PROTIP：在命令前面添加一個時間代理命令，用於標識每次運行該命令花費的時間。例如，“0m4.559s”表示大約4.6秒。

4.  下載此存儲庫以建立運行環境：

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--深度1</tt>指定僅下載最新版本，以節省所用空間。

    <tt>LS</tt>列出文件夾和文件以確認下載確實發生。

5.  授予所有 shell 文件運行權限：

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  運行腳本來設置 Azure 提供商：

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    響應是添加的提供者列表。

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

    上述只需要執行一次，但再次運行不會有什麼害處。

7.  授予 setmem.sh 運行權限並運行它：

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  將“sample-setmem.sh”移動（複製並重命名）到文件“setmem.sh”

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    PROTIP：我們將文件移動到永遠不會上傳到任何存儲庫（GitHub、GitLab 等）的位置。

### 在 setmem.sh 中手動自定義值

9.  使用程序“code”（Visual Studio Code）打開文件進行編輯：

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>使用它是因為包含機密的文件位於永遠不應該推送到 GitHub 的文件夾中。

10. 使用文本編輯器程序編輯 ../setmem.sh 文件：

    腳本已<strong>廣義的</strong>通過環境變量替換腳本中的硬編碼值。 PROTIP：使用變量而不是硬編碼可以避免拼寫錯誤和錯誤配置。

    下面的行定義了每個變量的值，以便多次運行可以使用不同的值，而無需更改腳本文件。

11. 在<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com 訂閱刀片</a>，選擇您要使用的訂閱，然後單擊圖標複製到剪貼板。

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    在文件中，突出顯示 ID 並將其粘貼：

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. 在<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com 租戶刀片</a>，選擇您要使用的租戶，然後單擊圖標複製到剪貼板。

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    在文件中，突出顯示 ID 並將其粘貼：

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    TODO：用從長期運行的 Azure KeyVault 中檢索機密的調用來替換機密的導出語句。但其他人不會查看此文件，除非他們使用你的帳戶正確登錄到 Azure。

13. 編輯 MY_LOC（位置 = 區域）和其他默認值。

14. 在文件底部，添加一條打印出其中一個變量的語句，以便您知道導出語句採用了：

    在 Bash 腳本中：

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. 保存文件。在 Cloud Shell 中，按 command+Q 或單擊“...”以按“保存”，然後按“關閉”。

### 每一次工作會議

1.  在每個會話開始時，調用自定義腳本存儲庫上方文件夾中的腳本：

    <pre><strong>source ../setmem.sh
    </strong></pre>

    注意：使用“source”運行腳本，以便腳本中定義的環境變量在腳本完成後可見，並由您從中啟動的任何程序繼承。這是因為源在當前 shell 中運行腳本。但請注意，任何退出語句都會停止運行。

    交替，

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    執行後，您仍然可以在運行另一個腳本之前覆蓋變量值。

    這就是您可以為多個區域/位置運行腳本的方法 - 只需更改<tt>我的位置</tt>環境變量的值並再次運行腳本。

2.  拿：<strong>刪除資源組</strong>阻止虛擬服務器上累積費用：

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt> - 是的</tt>在 az 命令輸入“y”以自動應答請求之前：<br />您確定要執行此操作嗎？ （是/否）： 是

<hr />

## 參考

這裡的腳本改編自慷慨分享代碼的多位專家：

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>作者：Iain Foulds，解釋於<https://aka.ms/monthoflunches>2020 年 4 月 30 日發布。

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>由微軟

-   <https://github.com/timothywarner/az400>& 蒂姆·華納的 az303

-   <https://github.com/zaalion/oreilly-azure-app-security>通過禮薩·薩利希

-   <https://github.com/Azure/azure-quickstart-templates>（ARM 模板）

-   <https://github.com/johnthebrit/AzureMasterClass>PowerShell 腳本

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   天際線學院

-   咕嚕聲（Terraform）

-   CloudPosse（AWS 的 Terraform）<br /><br />

## 維護者

[@wilsonmar](https://github.com/wilsonmar)

## 貢獻

PR 已被接受。

如果編輯本自述文件，請遵守[標準自述文件](https://github.com/RichardLitt/standard-readme)規格。

## 執照

©2021 威爾遜·瑪爾

## 倫理

該項目在 W3C 的框架下運作[道德和職業行為準則](https://www.w3.org/Consortium/cepc):

> W3C 是一個不斷發展的全球性社區，參與者可以選擇在其中工作
> 在一起，並在這個過程中經歷語言、地點的差異，
> 國籍、經驗。在如此多元化的環境下，誤解
> 有時會出現分歧，但在大多數情況下可以通過非正式方式解決。在
> 然而，在極少數情況下，行為可能會恐嚇、騷擾或以其他方式擾亂一個人
> 或者社區中有更多的人，W3C 不會容忍這種情況。
>
> 道德和職業行為準則有助於定義公認的和
> 可接受的行為並促進高標準的專業
> 實踐。它還為自我評價提供了基準，並作為
> 更好地展現組織形象的工具。

我們希望我們的社區團體按照這些準則行事，並且
參與者互相要求遵守這些高標準。如有任何問題
或者擔心代碼沒有被遵循，請聯繫存儲庫的所有者。
