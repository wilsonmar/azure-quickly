# asurblått raskt

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Innholdsfortegnelse

-   [Språk](#Language)
-   [Syn](#Vision)
-   [Alle liste](#Todos)
-   [Installer](#Install)
-   [Shell script koding triks](#ShellCoding)
-   [Bruk](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [Referanser](#References)
-   [Vedlikeholdere](#maintainers)
-   [Bidrar](#contributing)
-   [Tillatelse](#license)
-   [Etikk](#Ethics)

## Språk

All kode, kommentarer og dokumentasjon her er skrevet på amerikansk engelsk. Så vi kan dele læringen vår med utviklere over hele verden, takket være oversettelser<https://github.com/dephraiim/translate-readme>

-   [engelsk](README.md)
-   [Forenklet kinesisk](README.zh-CN.md)
-   [Tradisjonell kinesisk](README.zh-TW.md)
-   [Hindi](README.hi.md)
-   [fransk](README.fr.md)
-   [arabisk](README.ar.md)<br /><br />

De fleste skriptene i denne repoen er<strong>Bash shell-skript som kjører naturlig på MacOS og Linux</strong>.

Skriptkode kan kjøres på Windows Git Bash Shell. 
PowerShell-skript brukes i tilfeller der det er den eneste løsningen.

For å håndtere mer kompleksitet ble programmer kodet inn<a target="_blank" href="https://wilsonmar.github.io/python/">Python</a>eller<a target="_blank" href="https://wilsonmar.github.io/golang">Gå</a>språk kan kalles<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">når det passer</a>å dra nytte av deres evner.

Det er en risiko for at CLI-funksjoner ikke fungerer når de er underliggende<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">Azure REST API</a>fungerer. Så Postman-filer er inkludert når det passer.

## Syn

Ved å bruke denne repo kan<strong>spare deg tid og penger</strong>og gi deg litt fred i sinnet og lykke.

Folk lar ressurser gå fordi de<strong>ønsker ikke å bruke livet på å gjenta det manuelle slitet</strong>å klikke gjennom Azure Portal GUI, som beskrevet i de fleste Azure-veiledningene.

Denne repoen (kl<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>) inneholder automatiseringsskript som lar deg trygt<strong>slette ressursgrupper</strong>når du hviler eller spiller fordi det gjør det mulig<strong>få ressurser tilbake</strong>med bare noen få kommandoer, selv med et helt nytt abonnement.

Du sparer penger fordi du ikke trenger å la ressurser gå, forbruke kreditt eller få opp kredittkortregningen.

Det er stressende å gjenta den manuelle musingen og skrivingen nøyaktig gjennom Azure Portal (som ikke raskt kan repeteres).

Så denne README forklarer hvordan du kan starte ditt tilpassede miljø fra bunnen av ved å bruke CLI Bash-terminalen.

<a name="Todos"></a>

## Alle liste

-   Legg til alias.sh
-   Test for å sikre at skriptkode kan kjøres på Windows Git Bash Shell.
-   EN<strong>kontroll av variabler</strong>skript for å validere minnevariablene før påkalling.

<a name="Install"></a>

## Installer

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

Følgende er engangsaktiviteter for hvert Azure-abonnement, dekket i min dype, men konsise veiledning på:

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

Den dekker opprettelsen av gratis Azure-kontoer og Azure Storage-kontoer for å holde filer i en skystasjon:

1.  Få et Azure-abonnement (for eksempel ved å kjøpe en Visual Studio-lisens).

2.  Bruk en nettleser (Google Chrome) for å adressere<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>og logg inn.

3.  være inne<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>eller klikk på CLI-ikonet i portalen.

4.  Opprett en lagringskonto for en<strong>clouddrive</strong>inne i skallet.

### Sett opp et miljø for et nytt abonnement

1.  Trippelklikk på kommandoen nedenfor for å markere den:

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  Høyreklikk på den uthevede og velg "Kopier" for å lagre den uthevede midlertidig i utklippstavlen.

3.  Gå inn<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>eller klikk på CLI-ikonet etter inntasting<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  Høyreklikk hvor som helst på CLI Bash-terminalvinduet, og trykk deretter<strong>kommando+V</strong>å lime inn fra utklippstavlen.

5.  Trykk Enter for å kjøre skriptet. Det tar flere minutter å kjøre.

    Trinn utført av<a href="#az-setup-cli.sh">skriptet "az-setup-cli.sh" er beskrevet nedenfor</a>.

    Når du er ferdig, bør du se mappen som inneholder skript og ledeteksten til venstre, der den blir liggende etter hver kommando (i stedet for på slutten av mappebanen):

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### Tilpass setmem.sh-verdier

Init-skriptet etablerer også fra en prøve<strong>setmem-skript</strong>som definerer miljøvariabelverdier i minnet for å kontrollere skriptoperasjonen. Legg merke til at setmen-filen er i en høyere mappe enn der skriptkoden kan skyves til github. Det er fordi

1.  Bruk den innebygde Visual Studio Code-editoren for å redigere filen setmem.sh:

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  Bytt til Portal GUI.

3.  Åpne abonnementsbladet. Klikk på ditt nåværende abonnement.

4.  Klikk på kopiikonet ved siden av abonnementskoden (slik at den blir lagret på utklippstavlen).

5.  Bytt til koderedigeringsvinduet. Merk den eksisterende teksten i variabelen MY_SUBSCRIPTION_ID og trykk Lim inn (Kommando+V på Mac eller Ctrl+V på Windows).

    Det kan være en annen fil for hvert miljø (som dev vs. prod).

6.  Klikk på "..."-menyen til høyre for koderedigeringsvinduet for å lagre, og avslutt.

    Nå kan du kjøre skript for å opprette og administrere ressurser. 
    De fleste av skriptene refererer til en opplæring hos Microsoft Learn, CloudAcademy, Pluralsight, Coursera, etc.

    For å kjøre i Azure Machine Learning-studio, trenger du én eller flere forekomster av Azure ML Workspace, Compute, Insights og Key Vault.
    Slik lager du dem:

### Lag arbeidsområde ved hjelp av az ml cli v2

ML CLI v2 (forhåndsvisning) gir én automatiseringstilnærming:<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  Kjør skriptet jeg har modifisert fra det for å bruke miljøvariabler og tilleggsredigeringer:

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    Skriptet utfører en git-klon inn i miljøet.

    ### Konfigurer aliaser etter eget ønske

2.  Rediger<tt>aliases.sh</tt>fil og fjern eller legg til tastaturmakroer.

Nå som du har ressursene som trengs:

<a name="ShellCoding"></a>

## Shell script koding triks

Innholdet i Bash-skriptene i denne repoen er skrevet ved å bruke kodingskonvensjoner definert på<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>som inkluderer:

-   <tt>kilde ./az-all-start.sh</tt>setter opp miljøvariabler og verktøyfunksjoner.

-   <tt>sett -o hevet</tt>gjør det slik at skriptet stopper ved første feil (i stedet for å kjøre på).

-   En ny ressursgruppe og alle ressurser opprettes<strong>nytt for hvert løp</strong>for å redusere kompleksiteten ved koding for idempotens (hvor statusen er den samme på slutten av hver re-kjøring).

-   <tt>--resource-group</tt>er et nødvendig argument for mange kommandoer. Det er sist slik at manglende skråstrek en linje over den vil føre til at kommandoen mislykkes.

-   Et omvendt skråstrek \\-tegn på slutten av en linje innenfor samme az-shell-kommando fortsetter den kommandoen.

-   Variable (spesifikasjons)data som kontrollerer Python-programmer sendes til Python-programmer ved å lagre dem som variabler i en<strong>.env-fil</strong>i samme mappe som Python-programmet.

Jupyters Gallery of Python Notebooks:

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## Bruk

Prøv hver av aktivitetene nedenfor for hver økt (forutsatt at du utførte installasjonen ovenfor):

### Kjør individuell .ipynb-fil

Ifølge<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">Hvordan kjøre Jupyter</a>:

1.  Gå til<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure Machine Learning Studio</a>

2.  Klikk på forekomsten som er opprettet.

3.  Klikk på "<https://ml.azure.com/?tid=...">URL under "Studio nettadresse".

4.  Hvis popup-dialogboksen "kom i gang" vises, klikker du på X for å avvise den.

5.  Klikk på "Notatbøker".

    ### Klon Git-depoter inn i arbeidsområdets filsystem

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  Hold musen over brukernavnet ditt (blant brukere) og klikk på "..." for å velge "Last opp filer".

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  Naviger til mappene som<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">rask</a>
    -   lightgbm
    -   pytorch
    -   r
    -   tensorflyt<br /><br />

    ### MNIST

az ml job create -f jobs/train/lightgbm/iris/job.yml --set compute.target=local --web --stream

1.  Naviger til<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  Velg "job.yml".

3.  Klikk "Last opp".

4.  Velg datamaskinen hvor du vil kjøre Notebook.

    En stoppet beregningsforekomst vil automatisk starte når den første cellen kjøres.

5.  Klikk på "Kjør"-ikonet.

    ### Vekselvis

6.  I<strong>Brukerfiler</strong>delen av arbeidsområdet ditt. Klikk på cellen du ønsker å redigere. Hvis du ikke har noen notatblokker i denne delen, kan du se Opprette og administrere filer i arbeidsområdet.

Flere skript fra min azur-raskt repo:

-   Kjør et Bing-søk med API:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   Opprett et Azure Key Vault for bruk av skript som skal følges:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    Legg eventuelt en hemmelighet i den; vise hemmelighet; slette hemmelighet; gjenopprette hemmelighet; lag en vm; Administrert tjenesteidentitet; oppdatere tillatelser; Tilpasset skriptutvidelse; Bruk den tilpassede skriptutvidelsen:

-   Opprett et maskinlæringsarbeidsområde for å kjøre iPython Notebooks ved hjelp av JupyterLab:

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   Bruk Azure Cognitive Services:

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   Bruk rordiagrammer

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   Opprett en VM med en offentlig IP-adresse:

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   Opprett en App Service Plan, Azure Web App, Deployment, for å vise MY_APPNAME.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   Opprett et nettverk med to undernett og en nettverkssikkerhetsgruppe som sikrer innkommende trafikk. Ett undernett er for ekstern tilgangstrafikk, ett er nettrafikk for VM-er som kjører en webserver. To VM-er opprettes deretter. En tillater SSH-tilgang og har de riktige reglene for nettverkssikkerhetsgruppe brukt. Du bruker denne VM-en som en<strong>SSH jumpbox</strong>for deretter å koble til den andre VM-en som kan brukes som en webserver:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   Opprett en VM med en offentlig IP-adresse. Aktivert er en lagringskonto, oppstartsdiagnostikk med VM-diagnostikkutvidelsen brukt:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   Opprett en VM; Recovery Services-hvelvet, en sikkerhetskopipolicy, oppretter deretter en VM og bruker sikkerhetskopieringspolicyen før du starter den første sikkerhetskopieringsjobben.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   Lag en Docker-beholder fra en Dockerfil; Opprette AKS; Skaler opp kopier

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    IP-en viser nettstedet "Month of Pizza Lunches in a container" (lastbalansert).

-   Lag IoT for WebApp:

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   Opprett Azure-funksjoner:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Flere funksjonskomponenter er ikke tilgjengelige i Azure CLI, så manuelle handlinger er nødvendige på Azure Portal for å fylle ut hullene.
     Se e-boken "Month of Lunches".

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

Skriptet skal gjøre alle trinnene nedenfor:

1.  VALGFRITT: Rediger<tt>.bashrc</tt>fil for å tilpasse ledeteksten:

    Hvis du er i<strong>sky Shell</strong>(som kjører Linux-operativsystemet), legg til disse linjene nederst i<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    PS1 setter ledeteksten slik at den vises på samme sted på skjermen hver linje, under gjeldende mappe og filbane (i stedet for til høyre for den på forskjellige punkter på skjermen).

    "#" på den siste linjen i filen er et hack for å lage en kommentar ut av PS1-en systemet legger til på egen hånd.

2.  Naviger inn i en mappe som inneholder depot som skal lastes ned:

    Innenfor Cloud Shell er det<br /><tt><strong>cd skyskall</strong></tt>

    Alternativt, på min bærbare datamaskin, bruker jeg<br /><tt>cd gmail_acct</tt>

3.  Fjern den forrige repo-mappen:

    PROTIP: En tidsproxy-kommando legges til foran kommandoer for å identifisere hvor lang tid det tok å kjøre kommandoen hver gang. For eksempel betyr "0m4.559s" omtrent 4,6 sekunder.

4.  Last ned denne repoen for å etablere et kjøremiljø:

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--dybde 1</tt>spesifiserer nedlasting av kun den nyeste versjonen, for å spare plass brukt.

    <tt>ls</tt>viser mapper og filer for å bekrefte at nedlastingen faktisk skjedde.

5.  Gi alle shell-filen tillatelse til å kjøre:

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  Kjør skript for å konfigurere Azure-leverandører:

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    Svaret er en liste over leverandører som er lagt til.

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

    Ovennevnte trenger bare å gjøres én gang, men å kjøre det på nytt vil ikke være skadelig.

7.  Gi setmem.sh tillatelse til å kjøre og kjøre den:

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  Flytt (kopier og gi nytt navn) "sample-setmem.sh" til filen "setmem.sh"

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    PROTIP: Vi flytter filen dit den aldri vil bli lastet opp til noe depot (GitHub, GitLab, etc.).

### Tilpass verdier manuelt i setmem.sh

9.  Åpne filen for redigering ved å bruke programmet "kode" (Visual Studio Code):

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>brukes fordi filen, som inneholder hemmeligheter, er i en mappe som aldri skal skyves til GitHub.

10. Bruk et tekstredigeringsprogram for å redigere ../setmem.sh-filen:

    Manus har vært<strong>generalisert</strong>ved at miljøvariabler erstatter hardkodede verdier i skript. PROTIP: Bruk av variabel i stedet for hardkoding unngår skrivefeil og feilkonfigurasjoner.

    Linjene nedenfor definerer verdier for hver variabel slik at flere kjøringer kan bruke forskjellige verdier, uten å måtte endre skriptfilen.

11. I<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com Abonnementsblad</a>, velg abonnementet du vil bruke, og klikk deretter på ikonet for å kopiere til utklippstavlen.

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    Marker ID-en i filen og lim den inn:

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. I<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com Leietakerblad</a>, velg leietakeren du vil bruke, og klikk deretter på ikonet for å kopiere til utklippstavlen.

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    Marker ID-en i filen og lim den inn:

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    GJØRE: Erstatt eksporterklæringer av hemmeligheter med anrop for å hente dem fra et langvarig Azure KeyVault. Men ingen andre ville være på denne filen med mindre de er riktig logget på Azure under kontoen din.

13. Rediger MY_LOC (Plassering = Region) og andre standardinnstillinger.

14. Nederst i filen legger du til en setning som skriver ut en av variablene, slik at du vet at eksportsetningene tok:

    I et Bash-manus:

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. Lagre filen. I Cloud Shell, trykk på kommando+Q eller klikk på "..." for å trykke på Lagre, og deretter Lukk.

### Hver arbeidsøkt

1.  På begynnelsen av hver økt kaller du på skriptet i mappen rett over din egendefinerte skriptrepo:

    <pre><strong>source ../setmem.sh
    </strong></pre>

    MERK: Bruk av "kilde" for å kjøre skriptet slik at miljøvariabler definert i skriptet vil være synlige etter at skriptet er ferdig, og arves av alle programmer du starter fra det. Det er fordi kilden kjører skriptet i gjeldende skall. Men vær oppmerksom på at enhver exit-erklæring vil stoppe kjøringen.

    Alternativt,

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    Etter kjøring kan du fortsatt overstyre variabelverdier før du kjører et annet skript.

    Det er slik du kan kjøre skript for flere regioner/lokasjoner - ved å bare endre<tt>MY_LOC</tt>miljøvariabelens verdi og kjøre skriptet på nytt.

2.  PROTYPE:<strong>Slett ressursgrupper</strong>for å stoppe kostnadene fra å samle seg på virtuelle servere:

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt>--ja</tt>før az-kommandoen mater en "y" for automatisk å svare på forespørselen:<br />Er du sikker på at du vil utføre denne operasjonen? (y/n): y

<hr />

## Referanser

Skriptene her er tilpasset fra ulike eksperter som er sjenerøse med å dele koden sin:

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>av Iain Foulds, forklart i<https://aka.ms/monthoflunches>publisert 30.04.2020.

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>av Microsoft

-   <https://github.com/timothywarner/az400>& az303 av Tim Warner

-   <https://github.com/zaalion/oreilly-azure-app-security>av Reza Salehi

-   <https://github.com/Azure/azure-quickstart-templates>(ARM-maler)

-   <https://github.com/johnthebrit/AzureMasterClass>PowerShell-skript

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   Skylines Academy

-   Gruntwork (Terraform)

-   CloudPosse (Terraform for AWS)<br /><br />

## Vedlikeholdere

[@wilsonmar](https://github.com/wilsonmar)

## Bidrar

PR-er akseptert.

Hvis du redigerer denne README, vennligst samsvar med[standard-readme](https://github.com/RichardLitt/standard-readme)spesifikasjon.

## Tillatelse

MED © 2021 Wilson Mar

## Etikk

Dette prosjektet opererer under W3C-ene[Etiske retningslinjer og profesjonell atferd](https://www.w3.org/Consortium/cepc):

> W3C er et voksende og globalt fellesskap der deltakerne velger å jobbe
> sammen og i den prosessen oppleve forskjeller i språk, plassering,
> nasjonalitet og erfaring. I et så mangfoldig miljø, misforståelser
> og det oppstår uenigheter, som i de fleste tilfeller kan løses uformelt. I
> sjeldne tilfeller kan imidlertid atferd skremme, trakassere eller på annen måte forstyrre en
> eller flere mennesker i samfunnet, noe W3C ikke vil tolerere.
>
> Etiske retningslinjer og profesjonell atferd er nyttig for å definere akseptert og
> akseptabel atferd og å fremme høye standarder for profesjonelle
> øve. Det gir også en målestokk for selvevaluering og fungerer som en
> redskap for bedre identitet til organisasjonen.

Vi håper at samfunnsgruppen vår handler i henhold til disse retningslinjene, og det
deltakerne holder hverandre til disse høye standardene. Hvis du har spørsmål
eller er bekymret for at koden ikke blir fulgt, vennligst kontakt eieren av depotet.
