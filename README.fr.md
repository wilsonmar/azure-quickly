# azur-rapidement

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Table des matières

-   [Langue](#Language)
-   [Vision](#Vision)
-   [Toutes les listes](#Todos)
-   [Installer](#Install)
-   [Astuces de codage de script Shell](#ShellCoding)
-   [Usage](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [Les références](#References)
-   [Mainteneurs](#maintainers)
-   [Contribuant](#contributing)
-   [Licence](#license)
-   [Éthique](#Ethics)

## Langue

Tous les codes, commentaires et documentations ici sont rédigés en anglais américain. Afin que nous puissions partager nos apprentissages avec des développeurs du monde entier, les traductions sont grâce à<https://github.com/dephraiim/translate-readme>

-   [Anglais](README.md)
-   [Chinois simplifié](README.zh-CN.md)
-   [chinois traditionnel](README.zh-TW.md)
-   [hindi](README.hi.md)
-   [Française](README.fr.md)
-   [arabe](README.ar.md)<br /><br />

La plupart des scripts de ce dépôt sont<strong>Scripts shell Bash qui s'exécutent nativement sur MacOS et Linux</strong>.

Le code de script peut s'exécuter sur Windows Git Bash Shell.
Les scripts PowerShell sont utilisés dans les cas où c'est la seule solution.

Pour gérer plus de complexité, les programmes codés en<a target="_blank" href="https://wilsonmar.github.io/python/">Python</a>ou<a target="_blank" href="https://wilsonmar.github.io/golang">Aller</a>la langue peut être appelée<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">le cas échéant</a>pour profiter de leurs capacités.

Il existe un risque que les fonctions CLI ne fonctionnent pas lorsque leur<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">API REST Azure</a>ça marche. Les fichiers Postman sont donc inclus le cas échéant.

## Vision

L'utilisation de ce dépôt peut<strong>vous fait gagner du temps et de l'argent</strong>et vous apporte une certaine tranquillité d'esprit et du bonheur.

Les gens laissent les ressources fonctionner parce qu'ils<strong>ne veulent pas passer leur vie à répéter le travail manuel</strong>de cliquer via l'interface graphique du portail Azure, comme décrit dans la plupart des didacticiels Azure.

Ce dépôt (à<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>) contient des scripts d'automatisation qui vous permettent de gérer en toute confiance<strong>supprimer des groupes de ressources</strong>lorsque vous vous reposez ou jouez, car cela vous permet de<strong>récupérer des ressources</strong>avec seulement quelques commandes, même avec un tout nouvel abonnement.

Vous économisez de l'argent parce que vous n'avez pas besoin de laisser fonctionner des ressources, de consommer des crédits ou d'augmenter votre facture de carte de crédit.

Il est stressant de répéter avec précision le passage manuel de la souris et la saisie via le portail Azure (ce qui n'est pas rapidement reproductible).

Ainsi, ce README explique comment vous pouvez lancer votre environnement personnalisé à partir de zéro à l'aide du terminal CLI Bash.

<a name="Todos"></a>

## Toutes les listes

-   Ajouter un alias.sh
-   Testez pour vous assurer que le code du script peut s’exécuter sur Windows Git Bash Shell.
-   UN<strong>vérification des variables</strong>script pour valider les variables de mémoire avant l’invocation.

<a name="Install"></a>

## Installer

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

Les activités suivantes sont des activités ponctuelles pour chaque abonnement Azure, couvertes dans mon didacticiel approfondi mais concis sur :

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

Il couvre la création de comptes Azure gratuits et de comptes Azure Storage pour conserver des fichiers dans un clouddrive :

1.  Obtenez un abonnement Azure (par exemple en achetant une licence Visual Studio).

2.  Utilisez un navigateur Internet (Google Chrome) pour répondre<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>et connectez-vous.

3.  Soyez dedans<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>ou cliquez sur l'icône CLI dans le portail.

4.  Créez un compte de stockage pour un<strong>Cloud Drive</strong>à l'intérieur de la coquille.

### Configurer un environnement pour un nouvel abonnement

1.  Triple-cliquez sur la commande ci-dessous pour la mettre en surbrillance :

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  Cliquez avec le bouton droit sur le surligné et sélectionnez "Copier" pour enregistrer temporairement le surligné dans votre Presse-papiers.

3.  Montez<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>ou cliquez sur l'icône CLI après avoir entré<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  Cliquez avec le bouton droit n’importe où sur la fenêtre du terminal CLI Bash, puis appuyez sur<strong>commande+V</strong>à coller depuis le Presse-papiers.

5.  Appuyez sur Entrée pour exécuter le script. L'exécution prend plusieurs minutes.

    Les étapes exécutées par le<a href="#az-setup-cli.sh">le script "az-setup-cli.sh" est décrit ci-dessous</a>.

    Une fois terminé, vous devriez voir le dossier contenant les scripts et l'invite à gauche, où il restera après chaque commande (au lieu d'être à la fin du chemin du dossier) :

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### Personnaliser les valeurs setmem.sh

Le script d'initialisation établit également à partir d'un échantillon le<strong>script setmem</strong>qui définit les valeurs des variables d'environnement en mémoire pour contrôler le fonctionnement du script. Notez que le fichier setmen se trouve dans un dossier supérieur à celui où le code de script peut être poussé vers github. C'est parce que

1.  Utilisez l'éditeur Visual Studio Code intégré pour modifier le fichier setmem.sh :

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  Basculez vers l’interface graphique du portail.

3.  Ouvrez le panneau Abonnement. Cliquez sur votre abonnement actuel.

4.  Cliquez sur l'icône de copie à côté du code d'abonnement (pour qu'il soit enregistré dans votre Presse-papiers).

5.  Passez à la fenêtre de l'éditeur de code. Mettez en surbrillance le texte existant dans la variable MY_SUBSCRIPTION_ID et appuyez sur Coller (Commande+V sur Mac ou Ctrl+V sous Windows).

    Il peut y avoir un fichier différent pour chaque environnement (comme dev ou prod).

6.  Cliquez sur le menu "..." à droite de la fenêtre de l'éditeur de code pour enregistrer, puis quitter.

    Vous pouvez désormais exécuter des scripts pour créer et gérer des ressources.
    La plupart des scripts font référence à un didacticiel sur Microsoft Learn, CloudAcademy, Pluralsight, Coursera, etc.

    Pour exécuter dans le studio Azure Machine Learning, vous avez besoin d’une ou plusieurs instances d’Azure ML Workspace, Compute, Insights et Key Vault.
    Pour les créer :

### Créer un espace de travail à l'aide d'az ml cli v2

ML CLI v2 (aperçu) propose une approche d'automatisation :<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  Exécutez le script que j'ai modifié à partir de celui-ci pour utiliser des variables d'environnement et des modifications supplémentaires :

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    Le script effectue un clone git dans l'environnement.

    ### Configurez les alias à votre guise

2.  Modifier le<tt>aliases.sh</tt>fichier et supprimez ou ajoutez des macros de clavier.

Maintenant que vous disposez des ressources nécessaires :

<a name="ShellCoding"></a>

## Astuces de codage de script Shell

Le contenu des scripts Bash de ce référentiel est écrit en utilisant les conventions de codage définies sur<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>qui inclut:

-   <tt>source ./az-all-start.sh</tt>configure les variables d'environnement et les fonctions utilitaires.

-   <tt>set -o élevé</tt>fait en sorte que le script s'arrête à la première erreur (au lieu de s'exécuter).

-   Un nouveau groupe de ressources et toutes les ressources sont créées<strong>nouveau à chaque course</strong>pour réduire la complexité du codage de l'idempotence (où le statut est le même à la fin de chaque réexécution).

-   <tt>--groupe-de-ressources</tt>est un argument obligatoire sur de nombreuses commandes. C'est le dernier, de sorte que le manque de ligne oblique une ligne au-dessus entraînerait l'échec de la commande.

-   Une barre oblique inverse \\ à la fin d’une ligne dans la même commande az shell continue cette commande.

-   Les données variables (spécifications) contrôlant les programmes Python sont transmises aux programmes Python en les enregistrant en tant que variables dans un fichier Python.<strong>fichier .env</strong>dans le même dossier que le programme Python.

Galerie Jupyter de blocs-notes Python :

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## Usage

Essayez chacune des activités ci-dessous pour chaque session (en supposant que vous ayez effectué l'installation ci-dessus) :

### Exécutez un fichier .ipynb individuel

Selon<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">Comment exécuter Jupyter</a>:

1.  Allez au<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure Machine Learning Studio</a>

2.  Cliquez sur l'instance créée.

3.  Clique le "<https://ml.azure.com/?tid=...">URL sous "URL Web du studio".

4.  Si la boîte de dialogue contextuelle « Commencer » apparaît, cliquez sur X pour la fermer.

5.  Cliquez sur "Carnets".

    ### Clonez les référentiels Git dans le système de fichiers de votre espace de travail

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  Passez la souris sur votre nom d'utilisateur (parmi les utilisateurs) et cliquez sur le "..." pour choisir "Télécharger des fichiers".

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  Accédez aux dossiers comme<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">rapide</a>
    -   lumièregbm
    -   torche
    -   r
    -   flux tensoriel<br /><br />

    ### MNIST

az ml job create -f jobs/train/lightgbm/iris/job.yml --set computation.target=local --web --stream

1.  Aller vers<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  Sélectionnez "job.yml".

3.  Cliquez sur "Télécharger".

4.  Sélectionnez le calcul sur lequel exécuter le Notebook.

    Une instance de calcul arrêtée démarrera automatiquement lorsque la première cellule sera exécutée.

5.  Cliquez sur l'icône "Exécuter".

    ### Alternativement

6.  Dans le<strong>Fichiers utilisateur</strong>section de votre espace de travail. Cliquez sur la cellule que vous souhaitez modifier. Si vous n'avez aucun bloc-notes dans cette section, consultez Créer et gérer des fichiers dans votre espace de travail.

Plus de scripts de mon dépôt Azure-quickly :

-   Exécutez une recherche Bing à l'aide de l'API :

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   Créez un Azure Key Vault à utiliser par les scripts à suivre :

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    Éventuellement, mettez-y un secret ; montrer un secret ; supprimer le secret ; récupérer le secret ; créer une machine virtuelle ; Identité de service géré ; mettre à jour les autorisations ; Extension de script personnalisé ; Appliquez l'extension de script personnalisé :

-   Créez un espace de travail de Machine Learning pour exécuter des notebooks iPython à l'aide de JupyterLab :

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   Utilisez Azure Cognitive Services :

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   Utiliser les cartes Helm

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   Créez une VM avec une adresse IP publique :

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   Créez un plan App Service, Azure Web App, déploiement, pour afficher MY_APPNAME.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   Créez un réseau avec deux sous-réseaux et un groupe de sécurité réseau qui sécurise le trafic entrant. Un sous-réseau est destiné au trafic d'accès à distance, l'autre est au trafic Web pour les machines virtuelles qui exécutent un serveur Web. Deux VM sont alors créées. L’un autorise l’accès SSH et applique les règles de groupe de sécurité réseau appropriées. Vous utilisez cette VM comme<strong>Boîte de connexion SSH</strong>pour ensuite se connecter à la deuxième VM qui peut servir de serveur web :

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   Créez une VM avec une adresse IP publique. Sont activés un compte de stockage, les diagnostics de démarrage avec l'extension de diagnostics de VM appliquée :

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   Créez une VM ; Le coffre-fort Recovery Services, une politique de sauvegarde, crée ensuite une machine virtuelle et applique la politique de sauvegarde avant de démarrer la tâche de sauvegarde initiale.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   Créez un conteneur Docker à partir d'un Dockerfile ; Créer AKS ; Augmenter les répliques

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    L'IP montre le site Web "Mois des déjeuners pizza dans un conteneur" (charge équilibrée).

-   Créez l'IoT pour l'application Web :

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   Créer des fonctions Azure :

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Plusieurs composants Functions ne sont pas disponibles dans Azure CLI, des actions manuelles sont donc nécessaires sur le portail Azure pour combler les lacunes.
     Voir l'ebook "Mois des déjeuners".

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

Le script doit effectuer toutes les étapes ci-dessous :

1.  FACULTATIF : Modifiez le<tt>.bashrc</tt>fichier pour personnaliser l'invite :

    Si vous êtes dans le<strong>coquille de nuage</strong>(qui exécute le système d'exploitation Linux), ajoutez ces lignes au bas du<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    La PS1 définit l'invite de manière à ce qu'elle apparaisse au même endroit sur l'écran à chaque ligne, sous le dossier et le chemin du fichier actuels (plutôt qu'à droite de ceux-ci à différents endroits de l'écran).

    "#" à la dernière ligne du fichier est un hack pour faire un commentaire sur la PS1 que le système ajoute lui-même.

2.  Accédez à un dossier contenant le référentiel à télécharger :

    Dans Cloud Shell, c'est<br /><tt><strong>cd cloudshell</strong></tt>

    Alternativement, sur mon ordinateur portable, j'utilise<br /><tt>cdgmail_acct</tt>

3.  Supprimez le dossier du dépôt précédent :

    CONSEIL PRO : une commande proxy de temps est ajoutée devant les commandes pour identifier le temps nécessaire à l'exécution de la commande à chaque fois. Par exemple, « 0m4.559s » signifie environ 4,6 secondes.

4.  Téléchargez ce dépôt pour établir un environnement d'exécution :

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--profondeur 1</tt>spécifie le téléchargement de la dernière version uniquement, pour économiser l'espace utilisé.

    <tt>ls</tt>répertorie les dossiers et les fichiers pour confirmer que le téléchargement a réellement eu lieu.

5.  Donnez à tous les fichiers shell les autorisations d'exécution :

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  Exécutez le script pour configurer les fournisseurs Azure :

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    La réponse est une liste de fournisseurs ajoutés.

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

    Ce qui précède ne doit être fait qu'une seule fois, mais l'exécuter à nouveau ne sera pas dangereux.

7.  Donnez à setmem.sh les autorisations pour l'exécuter et l'exécuter :

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  Déplacez (copiez et renommez) "sample-setmem.sh" vers le fichier "setmem.sh"

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    CONSEIL DE PRO : Nous déplaçons le fichier là où il ne sera jamais téléchargé vers un référentiel (GitHub, GitLab, etc.).

### Personnaliser manuellement les valeurs dans setmem.sh

9.  Ouvrez le fichier pour le modifier à l'aide du programme "code" (Visual Studio Code) :

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>est utilisé car le fichier, contenant des secrets, se trouve dans un dossier qui ne doit jamais être poussé vers GitHub.

10. Utilisez un éditeur de texte pour modifier le fichier ../setmem.sh :

    Les scripts ont été<strong>généralisé</strong>par des variables d'environnement remplaçant les valeurs codées en dur dans les scripts. CONSEIL DE PRO : L'utilisation de variables au lieu du codage en dur évite les fautes de frappe et les erreurs de configuration.

    Les lignes ci-dessous définissent les valeurs de chaque variable afin que plusieurs exécutions puissent utiliser des valeurs différentes, sans qu'il soit nécessaire de modifier le fichier de script.

11. Dans<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Lame d'abonnement portal.azure.com</a>, sélectionnez l'abonnement que vous souhaitez utiliser, puis cliquez sur l'icône pour copier dans le presse-papiers.

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    Dans le fichier, mettez en surbrillance l'ID et collez-le :

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. Dans<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Lame de locataire portal.azure.com</a>, sélectionnez le locataire que vous souhaitez utiliser, puis cliquez sur l'icône pour copier dans le presse-papiers.

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    Dans le fichier, mettez en surbrillance l'ID et collez-le :

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    À FAIRE : Remplacez les instructions d'exportation des secrets par des appels pour les récupérer à partir d'un Azure KeyVault de longue durée. Mais personne d’autre ne consulterait ce fichier à moins d’être correctement connecté à Azure sous votre compte.

13. Modifiez le MY_LOC (Emplacement = Région) et les autres valeurs par défaut.

14. Au bas du fichier, ajoutez une instruction qui imprime l'une des variables, afin que vous sachiez que les instructions d'exportation ont pris :

    Dans un script Bash :

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. Enregistrez le fichier. Dans Cloud Shell, appuyez sur Commande + Q ou cliquez sur "..." pour appuyer sur Enregistrer, puis sur Fermer.

### Chaque séance de travail

1.  Au début de chaque session, appelez le script dans le dossier juste au-dessus de votre dépôt de scripts personnalisés :

    <pre><strong>source ../setmem.sh
    </strong></pre>

    REMARQUE : utilisez "source" pour exécuter le script afin que les variables d'environnement définies dans le script soient visibles une fois le script terminé et héritées par tous les programmes que vous lancez à partir de celui-ci. C'est parce que la source exécute le script dans le shell actuel. Mais notez que toute instruction de sortie arrêterait l'exécution.

    Alternativement,

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    Après l'exécution, vous pouvez toujours remplacer les valeurs des variables avant d'exécuter un autre script.

    C'est ainsi que vous pouvez exécuter des scripts pour plusieurs régions/emplacements - en modifiant simplement le<tt>MY_LOC</tt>valeur de la variable d'environnement et exécutez à nouveau le script.

2.  PROTYPE :<strong>Supprimer des groupes de ressources</strong>pour empêcher les frais de s'accumuler sur les serveurs virtuels :

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt>--Oui</tt>avant que la commande az alimente un "y" pour répondre automatiquement à la requête :<br />Etes-vous sûr de vouloir effectuer cette opération? (o/n) : oui

<hr />

## Les références

Les scripts ici sont adaptés de divers experts généreux en partageant leur code :

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>par Iain Foulds, expliqué dans<https://aka.ms/monthoflunches>publié le 30/04/2020.

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>par Microsoft

-   <https://github.com/timothywarner/az400>& az303 par Tim Warner

-   <https://github.com/zaalion/oreilly-azure-app-security>Par Raza Saleh

-   <https://github.com/Azure/azure-quickstart-templates>(Modèles BRAS)

-   <https://github.com/johnthebrit/AzureMasterClass>Scripts PowerShell

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   Académie Skylines

-   Gruntwork (Terraform)

-   CloudPosse (Terraform pour AWS)<br /><br />

## Mainteneurs

[@wilsonmar](https://github.com/wilsonmar)

## Contribuant

PR acceptés.

Si vous modifiez ce README, veuillez vous conformer aux[standard-readme](https://github.com/RichardLitt/standard-readme)spécification.

## Licence

AVEC © 2021 Wilson Mar

## Éthique

Ce projet fonctionne sous l'égide du W3C[Code d'éthique et de conduite professionnelle](https://www.w3.org/Consortium/cepc):

> Le W3C est une communauté mondiale en pleine croissance où les participants choisissent de travailler
> ensemble et, dans ce processus, expérimentons des différences de langue, de lieu,
> nationalité et expérience. Dans un environnement aussi diversifié, des malentendus
> et des désaccords surviennent, qui dans la plupart des cas peuvent être résolus de manière informelle. Dans
> Dans de rares cas, cependant, le comportement peut intimider, harceler ou perturber une personne.
> ou plusieurs personnes dans la communauté, ce que le W3C ne tolérera pas.
>
> Un code d’éthique et de conduite professionnelle est utile pour définir les normes acceptées et
> comportements acceptables et promouvoir des normes élevées de professionnalisme
> pratique. Il fournit également une référence pour l'auto-évaluation et fait office de
> véhicule d’une meilleure identité de l’organisation.

Nous espérons que notre groupe communautaire agira conformément à ces directives et que
les participants s’engagent mutuellement à respecter ces normes élevées. Si vous avez des questions
ou si vous craignez que le code ne soit pas suivi, veuillez contacter le propriétaire du référentiel.
