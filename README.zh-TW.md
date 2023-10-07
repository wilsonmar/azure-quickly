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

這裡的所有程式碼、註解和文件都是用美國英語寫的。這樣我們就可以與世界各地的開發者分享我們的經驗，翻譯歸功於<https://github.com/dephraiim/translate-readme>

-   [英語](README.md)
-   [簡體中文](README.zh-CN.md)
-   [繁體中文](README.zh-TW.md)
-   [印地語](README.hi.md)
-   [法語](README.fr.md)
-   [阿拉伯](README.ar.md)<br /><br />

這個倉庫中的大多數腳本都是<strong>在 MacOS 和 Linux 上本機執行的 Bash shell 腳本</strong>.

腳本程式碼可以在 Windows Git Bash Shell 上運行。
PowerShell 腳本用於唯一解決方案的情況。

為了處理更多的複雜性，程式編碼為<a target="_blank" href="https://wilsonmar.github.io/python/">Python</a>或者<a target="_blank" href="https://wilsonmar.github.io/golang">去</a>語言可以稱為<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">在適當的時候</a>充分利用他們的能力。

存在以下風險：CLI 功能在其底層時可能無法運作<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">Azure REST API</a>確實有效。因此，適當時會包含 Postman 檔案。

## 想像

使用這個repo可以<strong>節省您的時間和金錢</strong>並給你一些心靈的平靜和幸福。

人們讓資源保持運作是因為他們<strong>不想把一輩子都花在重複體力勞動上</strong>按一下 Azure 入口網站 GUI，如大多數 Azure 教學課程所述。

這個倉庫（位於<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>）包含自動化腳本，使您能夠自信地<strong>刪除資源組</strong>當您休息或玩耍時，因為它使您能夠<strong>拿回資源</strong>即使使用全新的訂閱，也只需要幾個指令。

您可以節省金錢，因為您不必讓資源保持運作、消耗積分或增加信用卡帳單。

透過 Azure 入口網站準確地重複手動滑鼠操作和打字（無法快速重複）是很有壓力的。

因此，本自述文件說明如何使用 CLI Bash 終端從頭開始啟動自訂環境。

<a name="Todos"></a>

## 全部列表

-   Add alias.sh
-   進行測試以確保腳本程式碼可以在 Windows Git Bash Shell 上運行。
-   A<strong>變數審查</strong>腳本在呼叫之前驗證記憶體變數。

<a name="Install"></a>

## 安裝

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

以下是每個 Azure 訂閱的一次性活動，我的深入而簡潔的教程中對此進行了介紹：

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

它涵蓋了建立免費的 Azure 帳戶和 Azure 儲存體帳戶以將檔案保存在雲端硬碟中：

1.  取得 Azure 訂閱（例如透過購買 Visual Studio 授權）。

2.  使用網路瀏覽器（Google Chrome）來解決<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>並登入。

3.  處於<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>或點選入口網站中的 CLI 圖示。

4.  建立一個儲存帳戶<strong>雲端硬碟</strong>殼內。

### 為新訂閱設定環境

1.  三擊以下命令以突出顯示它：

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  右鍵單擊突出顯示的內容並選擇“複製”將突出顯示的內容暫時保存在剪貼簿中。

3.  進來<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>或輸入後點選CLI圖標<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  右鍵點選 CLI Bash 終端機視窗上的任意位置，然後按<strong>指令+V</strong>從剪貼簿貼上。

5.  按 Enter 執行腳本。運行需要幾分鐘。

    執行的步驟<a href="#az-setup-cli.sh">腳本“az-setup-cli.sh”如下所述</a>.

    完成後，您應該在左側看到包含腳本和提示的資料夾，它將在每個命令之後保留在此處（而不是在資料夾路徑的末尾）：

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### 自訂 setmem.sh 值

初始化腳本也會從範例建立<strong>設定記憶體腳本</strong>它定義記憶體中的環境變數值來控制腳本操作。請注意，setmen 檔案所在的資料夾比腳本程式碼推送到 github 的資料夾要高。那是因為

1.  使用內建的 Visual Studio Code 編輯器編輯檔案 setmem.sh：

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  切換到門戶 GUI。

3.  打開訂閱側邊欄標籤。點擊您目前的訂閱。

4.  點擊訂閱代碼旁的複製圖示（以便將其儲存到剪貼簿）。

5.  切換到程式碼編輯器視窗。反白顯示變數 MY_SUBSCRIPTION_ID 中的現有文本，然後按下「貼上」（在 Mac 上按 Command+V，在 Windows 上按 Ctrl+V）。

    每個環境可能有不同的檔案（例如 dev 與 prod）。

6.  點擊程式碼編輯器視窗右側的“...”選單進行儲存，然後退出。

    現在您可以執行腳本來建立和管理資源。
    大多數腳本引用了 Microsoft Learn、CloudAcademy、Pluralsight、Coursera 等的教學。

    要在 Azure 機器學習工作室中執行，您需要一個或多個 Azure ML 工作區、運算、見解和 Key Vault 執行個體。
    創建它們：

### 使用 az ml cli v2 建立工作區

ML CLI v2（預覽版）提供了一種自動化方法：<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  運行我修改後的腳本以使用環境變數和其他編輯：

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    該腳本執行 git 克隆到環境中。

    ### 依照您的喜好設定別名

2.  編輯<tt>aliases.sh</tt>文件並刪除或新增鍵盤巨集。

現在您已經擁有所需的資源：

<a name="ShellCoding"></a>

## Shell 腳本編碼技巧

此儲存庫中的 Bash 腳本內的內容是使用以下定義的編碼約定編寫的<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>其中包括：

-   <tt>來源 ./az-all-start.sh</tt>設定環境變數和實用函數。

-   <tt>設定-O 凸起</tt>使腳本在出現第一個錯誤時停止（而不是繼續執行）。

-   建立一個新的資源組和所有資源<strong>每次運行都有新內容</strong>降低冪等性編碼的複雜性（每次重新運行結束時狀態相同）。

-   <tt>--資源群組</tt>是許多命令的必需參數。它是最後一個，因此上面的一行缺少斜線會導致命令失敗。

-   同一 az shell 指令中行尾的反斜線 \\ 字元繼續該指令。

-   控制Python程式的變數（規範）資料透過將它們保存為變數來傳遞給Python程序<strong>.env 文件</strong>與 Python 程式位於同一資料夾中。

Jupyter 的 Python 筆記本圖庫：

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## 用法

針對每個會話嘗試以下每項活動（假設您執行了上面的安裝）：

### 運行單獨的 .ipynb 文件

根據<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">如何運行 Jupyter</a>:

1.  前往<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure 機器學習工作室</a>

2.  按一下已建立的實例。

3.  點擊 ”<https://ml.azure.com/?tid=...">“Studio Web URL”下的 URL。

4.  如果出現「開始」彈出對話框，請按一下 X 將其關閉。

5.  按一下“筆記本”。

    ### 將 Git 儲存庫複製到您的工作區檔案系統中

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  將滑鼠懸停在您的使用者名稱上（在“使用者”中），然後按一下“...”以選擇“上傳檔案”。

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  導航到資料夾<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">快速地</a>
    -   光GBM
    -   火炬
    -   r
    -   張量流<br /><br />

    ### MNIST

az ml job create -f jobs/train/lightgbm/iris/job.yml --setcompute.target=local --web --stream

1.  導航<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  選擇“job.yml”。

3.  按一下“上傳”。

4.  選擇運行筆記本的計算位置。

    當第一個單元運作時，停止的計算實例將自動啟動。

5.  點擊“運行”圖示。

    ### 交替

6.  在裡面<strong>使用者檔案</strong>您工作空間的一部分。按一下您要編輯的儲存格。如果您在本部分中沒有任何筆記本，請參閱在工作區中建立和管理文件。

來自我的 azure-quickly 存儲庫的更多腳本：

-   使用 API 執行 Bing 搜尋：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   建立 Azure Key Vault 供以下腳本使用：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    （可選）在其中添加一個秘密；顯示秘密；刪除秘密；恢復秘密；創建一個虛擬機器；託管服務身分；更新權限；自訂腳本擴充；應用自訂腳本擴充功能：

-   建立機器學習工作區以使用 JupyterLab 執行 iPython Notebook：

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

-   建立具有公用 IP 位址的虛擬機器：

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   建立應用服務計劃、Azure Web 應用程式、部署以顯示 MY_APPNAME。

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   建立一個具有兩個子網路和一個保護入站流量的網路安全群組的網路。一個子網路用於遠端存取流量，一個子網路用於運行 Web 伺服器的虛擬機器的 Web 流量。然後創建兩個虛擬機器。一種允許 SSH 存取並應用適當的網路安全群組規則。您將此虛擬機器用作<strong>SSH 跳線盒</strong>然後連接到第二個可用作 Web 伺服器的虛擬機器：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   建立具有公用 IP 位址的虛擬機器。啟用的是儲存帳戶、應用了 VM 診斷擴充的啟動診斷：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   創建虛擬機器；復原服務保管庫（備份策略）會在開始初始備份作業之前建立虛擬機器並套用備份策略。

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   從 Dockerfile 建立 Docker 容器；創建AKS；擴大副本規模

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    該 IP 顯示「容器中的披薩午餐月」網站（負載平衡）。

-   為 WebApp 建立 IoT：

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   建立 Azure 函數：

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Azure CLI 中不提供多個 Functions 元件，因此需要在 Azure 入口網站上執行手動操作來填補空白。
     請參閱“午餐月”電子書。

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

該腳本應執行以下所有步驟：

1.  可選：編輯<tt>.bashrc</tt>文件來自訂提示：

    如果你在<strong>雲殼</strong>（運行 Linux 作業系統），將這些行加入<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    PS1 設定提示，使其每行都出現在螢幕上的相同位置，位於目前資料夾和檔案路徑下（而不是在螢幕上各點的右側）。

    文件最後一行的「#」是對系統自行加入的 PS1 進行註解的 hack。

2.  導航至儲存要下載的儲存庫的資料夾：

    在 Cloud Shell 中，它是<br />
    <tt><strong>cd 雲殼</strong></tt>

    或者，在我的筆記型電腦上，我使用<br /><tt>cd gmail_acct</tt>

3.  刪除先前的 repo 資料夾：

    PROTIP：在指令前面新增一個時間代理指令，用來識別每次執行指令花費了多少時間。例如，「0m4.559s」表示大約4.6秒。

4.  下載此儲存庫以建立運行環境：

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--深度1</tt>指定僅下載最新版本，以節省所用空間。

    <tt>LS</tt>列出資料夾和檔案以確認下載確實發生。

5.  授予所有 shell 檔案運行權限：

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  執行腳本來設定 Azure 提供者：

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    回應是新增的提供者清單。

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

    上述只需要執行一次，但再次運行不會有什麼壞處。

7.  授予 setmem.sh 運行權限並運行它：

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  將“sample-setmem.sh”移動（複製並重新命名）到檔案“setmem.sh”

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    PROTIP：我們將檔案移到永遠不會上傳到任何儲存庫（GitHub、GitLab 等）的位置。

### 在 setmem.sh 中手動自訂值

9.  使用程式“code”（Visual Studio Code）開啟檔案進行編輯：

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>使用它是因為包含機密的文件位於永遠不應該推送到 GitHub 的資料夾中。

10. 使用文字編輯器程式編輯 ../setmem.sh 檔案：

    腳本已<strong>廣義的</strong>透過環境變數替換腳本中的硬編碼值。 PROTIP：使用變數而不是硬編碼可以避免拼字錯誤和錯誤配置。

    下面的行定義了每個變數的值，以便多次執行可以使用不同的值，而無需更改腳本檔案。

11. 在<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com 訂閱刀片</a>，選擇您要使用的訂閱，然後按一下圖示複製到剪貼簿。

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    在文件中，突出顯示 ID 並將其貼上：

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. 在<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com 租用戶刀片</a>，選擇您要使用的租戶，然後按一下圖示複製到剪貼簿。

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    在文件中，突出顯示 ID 並將其貼上：

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    TODO：使用從長期運行的 Azure KeyVault 擷取機密的呼叫來取代機密的匯出語句。但其他人不會查看此文件，除非他們使用您的帳戶正確登入 Azure。

13. 編輯 MY_LOC（位置 = 區域）和其他預設值。

14. 在文件底部，加入一條印出其中一個變數的語句，以便您知道導出語句採用了：

    在 Bash 腳本中：

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. 儲存文件。在 Cloud Shell 中，按 command+Q 或按一下“...”以按“儲存”，然後按“關閉”。

### 每一次工作會議

1.  在每個會話開始時，呼叫自訂腳本儲存庫上方資料夾中的腳本：

    <pre><strong>source ../setmem.sh
    </strong></pre>

    注意：使用「source」執行腳本，以便腳本中定義的環境變數在腳本完成後可見，並由您從中啟動的任何程式繼承。這是因為來源在目前 shell 中執行腳本。但請注意，任何退出語句都會停止運作。

    交替，

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    執行後，您仍然可以在執行另一個腳本之前覆蓋變數值。

    這就是您可以為多個區域/位置運行腳本的方法 - 只需更改<tt>我的位置</tt>環境變數的值並再次運行腳本。

2.  原型：<strong>刪除資源組</strong>阻止虛擬伺服器上累積費用：

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt>- 是的</tt>在 az 指令輸入「y」以自動應答請求之前：<br />您確定要執行此操作嗎？ （是/否）： 是

<hr />

## 參考

這裡的腳本改編自慷慨分享程式碼的多位專家：

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>作者：Iain Foulds，解釋於<https://aka.ms/monthoflunches>2020 年 4 月 30 日發布。

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>由微軟

-   <https://github.com/timothywarner/az400>& 提姆華納的 az303

-   <https://github.com/zaalion/oreilly-azure-app-security>拉扎·薩利赫

-   <https://github.com/Azure/azure-quickstart-templates>（ARM 範本）

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

©2021 威爾森‧瑪爾

## 倫理

該計畫在 W3C 的框架下運作[道德和專業行為準則](https://www.w3.org/Consortium/cepc):

> W3C 是一個不斷發展的全球性社區，參與者可以選擇在其中工作
> 在一起，並在這個過程中經歷語言、地點的差異，
> 國籍、經驗。在如此多元化的環境下，誤解
> 有時會出現分歧，但在大多數情況下可以透過非正式方式解決。在
> 然而，在極少數情況下，行為可能會恐嚇、騷擾或以其他方式擾亂一個人
> 或者社區中有更多的人，W3C 不會容忍這種情況。
>
> 道德和專業行為準則有助於定義公認的和
> 可接受的行為並促進高標準的專業
> 實踐。它也為自我評價提供了基準，並作為
> 更好展現組織形象的工具。

We hope that our community group act according to these guidelines, and that
participants hold each other to these high standards. If you have any questions
or are worried that the code isn't being followed, please contact the owner of the repository.
