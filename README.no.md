# Azure-quickly

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## Innholdsfortegnelse

-   [Språk](#Language)
-   [Syn](#Vision)
-   [Alle listen](#Todos)
-   [Installer](#Install)
-   [Shell Script Coding Tricks](#ShellCoding)
-   [Bruk](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [Referanser](#References)
-   [Vedlikeholdere](#maintainers)
-   [Bidra](#contributing)
-   [Tillatelse](#license)
-   [Etikk](#Ethics)

## Språk

All kode, kommentarer og dokumentasjon her er skrevet på amerikansk engelsk. Så vi kan dele læringene våre med utviklere over hele verden, oversettelser er takket være<https://github.com/dephraiim/translate-readme>

-   [Engelsk](README.md)
-   [Forenklet kinesisk](README.zh-CN.md)
-   [Tradisjonell kinesisk](README.zh-TW.md)
-   [Hindi](README.hi.md)
-   [Fransk](README.fr.md)
-   [Arabisk](README.ar.md)<br /><br />

De fleste skript i denne repoen er<strong>Bash shell manus som kjører innfødt på macOS og Linux</strong>.

Skriptkode kan kjøres på Windows Git Bash Shell. 
PowerShell -skript brukes i tilfeller der det er den eneste løsningen.

For å håndtere mer kompleksitet, programmer kodet i<a target="_blank" href="https://wilsonmar.github.io/python/">Python</a>eller<a target="_blank" href="https://wilsonmar.github.io/golang">Gå</a>Språk kan kalles<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">Når det er passende</a>å dra nytte av deres evner.

Det er en risiko for at CLI -funksjoner kanskje ikke fungerer når det er underliggende<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">Azure REST API</a>Fungerer. Så postmanfiler er inkludert når det er aktuelt.

## Syn

Bruke denne repo kan<strong>Spar deg tid og penger</strong>og gi deg litt sinnsro og lykke.

Folk lar ressursene løpe fordi de<strong>Vil ikke bruke livet på å gjenta det manuelle slit</strong>av å klikke på Azure Portal GUI, som beskrevet av de fleste Azure Tutorials.

Denne repoen (kl<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>) inneholder automatiseringsskript som gjør deg i stand til å trygt<strong>Slett ressursgrupper</strong>Når du hviler eller spiller fordi det gjør deg i stand til å<strong>Få ressursene tilbake</strong>med bare noen få kommandoer, selv med et helt nytt abonnement.

Du sparer penger fordi du ikke trenger å la ressursene løpe, konsumere studiepoeng eller løpe opp kredittkortregningen.

Det er stressende å gjenta den manuelle musing og skriving gjennom Azure -portalen (som ikke raskt kan repeteres).

Så denne Readme forklarer hvordan du kan sette i gang ditt tilpassede miljø fra bunnen av ved hjelp av CLI Bash -terminalen.

<a name="Todos"></a>

## Alle listen

-   Legg til aliash
-   Test for å sikre at skriptkoden kan kjøres på Windows Git Bash Shell.
-   EN<strong>variabler vetting</strong>manus for å validere minnevariablene før påkallelse.

<a name="Install"></a>

## Installer

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

Følgende er engangsaktiviteter for hvert Azure-abonnement, dekket av min dype, men likevel konsise opplæring på:

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

Den dekker opprettelsen av frie Azure -kontoer og Azure lagringskontoer for å holde filer i en CloudDrive:

1.  Få et Azure -abonnement (for eksempel ved å kjøpe en visuell studielisens).

2.  Bruk en nettleser (Google Chrome) for å adressere<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>og pålogging.

3.  Være i<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>eller klikk på CLI -ikonet i portalen.

4.  Opprett en lagringskonto for en<strong>CloudDrive</strong>innenfor skallet.

### Sett opp et miljø for et nytt abonnement

1.  Trippelklikk på kommandoen nedenfor for å markere den:

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  Høyreklikk på uthevet og velg "Kopier" for å lagre det uthevet midlertidig i utklippstavlen.

3.  Komme inn<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>eller klikk på CLI -ikonet etter å ha kommet inn<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  Høyreklikk hvor som helst på CLI Bash Terminal-vinduet, og trykk deretter<strong>Kommando+v</strong>å lime inn fra utklippstavlen.

5.  Trykk Enter for å kjøre skriptet. Det tar flere minutter å løpe.

    Trinn utført av<a href="#az-setup-cli.sh">manus "AZ-Setup-cli.sh" er beskrevet nedenfor</a>.

    Når du er ferdig, bør du se mappen som inneholder skript og ledeteksten til venstre, der den vil holde seg etter hver kommando (i stedet for på slutten av mappestien):

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### Tilpass setmem.sh -verdier

Init -skriptet etablerer også fra en prøve<strong>setmem manus</strong>som definerer miljøvariable verdier i minnet for å kontrollere skriptdrift. Merk at setmen -filen er i en høyere mappe enn der skriptkoden kan skyves til Github. Det er fordi

1.  Bruk den innebygde Visual Studio Code Editor for å redigere File SetMem.sh:

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  Bytt til portalen GUI.

3.  Åpne abonnementsbladet. Klikk på ditt nåværende abonnement.

4.  Klikk på Kopierikonet ved siden av abonnementskoden (så det blir lagret på utklippstavlen).

5.  Bytt til Code Editor -vinduet. Uthev den eksisterende teksten i variabelen my_subscription_id og trykk pasta (kommando+v på mac -maskiner eller ctrl+v på Windows).

    Det kan være en annen fil for hvert miljø (for eksempel Dev vs. Prod).

6.  Klikk på "..." -menyen til høyre for Code Editor -vinduet for å lagre, og avslutt deretter.

    Nå kan du kjøre skript for å lage og administrere ressurser. 
    De fleste av skriptene refererer til en opplæring hos Microsoft Learn, Cloudacademy, Pluralsight, Coursera, etc.

    For å løpe i Azure Machine Learning Studio, trenger du ett eller flere tilfeller et Azure ML -arbeidsområde, beregning, innsikt og nøkkelhvelv.
    Å lage dem:

### Lag arbeidsområde ved hjelp av AZ ML CLI V2

ML CLI V2 (forhåndsvisning) gir en automatiseringsmetode:<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  Kjør skriptet jeg har endret fra det for å bruke miljøvariabler og tilleggsredigeringer:

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    Manuset utfører en Git -klon i miljøet.

    ### Konfigurer aliaser etter din smak

2.  Rediger<tt>aliases.sh</tt>fil og fjern eller legg til tastaturmakroer.

Nå som du har ressursene som trengs:

<a name="ShellCoding"></a>

## Shell Script Coding Tricks

Innhold i bash -skript i denne repoen er skrevet ved hjelp av kodingskonvensjoner definert på<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>som inkluderer:

-   <tt>kilde ./az-all-start.sh</tt>Sett opp miljøvariabler og verktøyfunksjoner.

-   <tt>Sett -o reist</tt>Gjør det slik at skriptet stopper på den første feilen (i stedet for å kjøre videre).

-   En ny ressursgruppe og alle ressurser opprettes<strong>Ny hvert løp</strong>For å redusere kompleksiteten i koding for idempotency (der statusen er den samme på slutten av hvert omløp).

-   <tt>-Ressursgruppe</tt>er et nødvendig argument på mange kommandoer. Det er sist slik at manglende skråstrek en linje over den vil føre til at kommandoen mislykkes.

-   En tilbakeslag \\ tegn på slutten av en linje innenfor den samme AZ Shell -kommandoen fortsetter den kommandoen.

-   Variable (Spesifikasjon) Data som kontrollerer Python -programmer sendes til Python -programmer ved å lagre dem som variabler i en<strong>.Env -fil</strong>I samme mappe som Python -programmet.

Jupyter's Gallery of Python Notebooks:

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## Bruk

Prøv hver av aktivitetene nedenfor for hver økt (forutsatt at du utførte installasjonen over):

### Kjør individuell .ipynb -fil

Ifølge<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">Hvordan kjøre Jupyter</a>:

1.  Gå til<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">Azure Machine Learning Studio</a>

2.  Klikk på forekomsten som er opprettet.

3.  Klikk på "<https://ml.azure.com/?tid=...">URL under "Studio Web URL".

4.  Hvis pop-up-dialogen "Kom i gang", klikker du på X for å avskjedige den.

5.  Klikk "Notebøker".

    ### Klon Git -lagringsplasser i arbeidsområdet ditt Filsystem

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  Mus over brukernavnet ditt (blant brukere) og klikk på "..." for å velge "Last opp filer".

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  Naviger til mappene som<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">Empetanse</a>
    -   LightGBM
    -   Pytorch
    -   r
    -   Tensorflow<br /><br />

    ### Mnist

AZ ML Job Create -F Jobs/Train/LightGBM/Iris/Job.yml -Set Compute.Target = Local --Web -Stream

1.  Naviger til<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  Velg "Job.yml".

3.  Klikk "Last opp".

4.  Velg Beregne hvor du kjører den bærbare PC -en.

    En stoppet beregningsforekomst starter automatisk når den første cellen kjøres.

5.  Klikk på "Kjør" -ikonet.

    ### Alternativt

6.  I<strong>Brukerfiler</strong>delen av arbeidsområdet ditt. Klikk på cellen du vil redigere. Hvis du ikke har noen notatbøker i denne delen, kan du se Opprett og administrere filer i arbeidsområdet ditt.

Flere skript fra min Azure-Quickly repo:

-   Kjør et Bing -søk ved hjelp av API:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   Lag et Azure Key Vault for bruk av skript som skal følges:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    Eventuelt, legg en hemmelighet i den; Vis hemmelighet; slette hemmelighet; gjenopprette hemmelighet; lage en VM; Administrert serviceidentitet; oppdateringstillatelser; Tilpasset skriptforlengelse; Bruk den tilpassede skriptforlengelsen:

-   Lag et arbeidsområde for maskinlæring for å kjøre Ipython notatbøker ved hjelp av Jupyterlab:

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   Bruk Azure kognitive tjenester:

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   Bruk rorkart

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   Opprett en VM med en offentlig IP -adresse:

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   Lag en app -tjenesteplan, Azure Web App, Deployment, for å vise MY_APPNAME.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   Lag et nettverk med to undernett og en nettverkssikkerhetsgruppe som sikrer inngående trafikk. Ett undernett er for fjerntilgangstrafikk, en er netttrafikk for VM -er som kjører en webserver. To VM -er blir deretter opprettet. Man tillater SSH -tilgang og har de aktuelle nettverkssikkerhetsgruppens regler som er brukt. Du bruker denne VM som en<strong>Ssh Jumpbox</strong>For å koble til den andre VM som kan brukes som en webserver:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   Opprett en VM med en offentlig IP -adresse. Aktivert er en lagringskonto, oppstartsdiagnostikk med VM -diagnostikkutvidelsen anvendt:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   Lage en VM; Gjenopprettingstjenester Vault, en sikkerhetskopieringspolicy, oppretter deretter en VM og bruker sikkerhetskopieringspolicyen før du starter den første sikkerhetskopijobben.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   Lag en Docker -beholder fra en DockerFile; Lage AKs; Skala opp kopier

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    IP -en viser "måneden med pizza -lunsjer i en container" nettsted (last balansert).

-   Lag IoT for WebApp:

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   Lag Azure -funksjoner:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Flere funksjonskomponenter er ikke tilgjengelige i Azure CLI, så manuelle handlinger er nødvendige på Azure Portal for å fylle ut hullene.
     Se eboken "Måned".

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

Skriptet skal gjøre alle trinnene nedenfor:

1.  Valgfritt: Rediger<tt>.bashrc</tt>fil for å tilpasse ledeteksten:

    Hvis du er i<strong>Cloud Shell</strong>(som kjører Linux -operativsystemet), legg disse linjene til bunnen av<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    PS1 setter ledeteksten slik at den vises på samme sted på skjermen hver linje, under gjeldende mappe og filsti (snarere enn til høyre for den på forskjellige punkter på skjermen).

    "#" på den siste linjen i filen er et hack for å komme med en kommentar av PS1 systemet legger til på egen hånd.

2.  Naviger inn i en mappe som holder depot som skal lastes ned:

    Innenfor skyskall, er det<br /><tt><strong>CD Cloudshell</strong></tt>

    Alternativt, på den bærbare datamaskinen min, bruker jeg<br /><tt>CD Gmail_ACCT</tt>

3.  Fjern den forrige repo -mappen:

    Protip: En Time Proxy -kommando legges til foran kommandoer for å identifisere hvor mange ganger som ble tatt for å kjøre kommandoen hver gang. For eksempel betyr "0m4.559s" omtrent 4,6 sekunder.

4.  Last ned denne repoen for å etablere et løpsmiljø:

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--dybde 1</tt>Spesifiserer nedlasting av bare den nyeste versjonen, for å spare plass som brukes.

    <tt>ls</tt>Lister mapper og filer for å bekrefte at nedlastingen faktisk skjedde.

5.  Gi alle Shell -filtillatelser til å kjøre:

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  Kjør skript for å konfigurere Azure -leverandører:

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    Responsen er en liste over leverandører lagt til.

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

    Ovennevnte trenger bare å gjøres en gang, men å kjøre det igjen vil ikke være skadelig.

7.  Gi SetMem.sh -tillatelser til å kjøre og kjøre den:

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  Flytt (kopier og gi nytt navn til) "Sample SetMem.sh" for å arkivere "SetMem.sh"

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    Protip: Vi flytter filen der den aldri blir lastet opp til noe depot (GitHub, Gitlab, etc.).

### Tilpass verdier manuelt i setmem.sh

9.  Åpne filen for redigering ved hjelp av programmet "Kode" (Visual Studio Code):

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>brukes fordi filen, som inneholder hemmeligheter, er i en mappe som aldri skal skyves til Github.

10. Bruk et tekstredigeringsprogram for å redigere ../setmem.sh -filen:

    Skript har vært<strong>generalisert</strong>ved miljøvariabler som erstatter hardkodede verdier i skript. Protip: Bruke variabel i stedet for hardkoding unngår skrivefeil og feilkonfigurasjoner.

    Linjer nedenfor definerer verdier for hver variabel slik at flere kjøringer kan bruke forskjellige verdier, uten behov for å endre skriptfilen.

11. I<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com abonnementsblad</a>Velg abonnementet du vil bruke, og klikk deretter på ikonet for å kopiere for å utklippstavle.

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    I filen, fremhev IDen og lim den inn:

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. I<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com leietakerblad</a>, Velg leietaker du vil bruke, og klikk deretter på ikonet for å kopiere til utklippstavlen.

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    I filen, fremhev IDen og lim den inn:

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    TODO: erstatte eksportuttalelser om hemmeligheter med samtaler for å hente dem fra en langvarig Azure KeyVault. Men ingen andre ville være på denne filen med mindre de er riktig logget inn på Azure under kontoen din.

13. Rediger my_loc (plassering = region) og andre standardverdier.

14. Nederst i filen, legg til en uttalelse som skriver ut en av variablene, slik at du vet at eksportuttalelsene tok:

    I et bashpt:

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. Lagre filen. I Cloud Shell, trykk Kommando+q eller klikk på "..." for å trykke på Lagre, og lukk deretter.

### Hver arbeidsøkt

1.  I begynnelsen av hver økt påkaller skriptet i mappen rett over dine tilpassede skript repo:

    <pre><strong>source ../setmem.sh
    </strong></pre>

    Merk: Å bruke "kilde" for å kjøre skriptet slik at miljøvariabler definert i skriptet vil være synlig etter at skriptet er gjort, og bli arvet av alle programmer du lanserer fra det. Det er fordi kilden kjører skriptet i det nåværende skallet. Men merk at enhver exit -uttalelse vil stoppe løpet.

    Alternativt,

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    Etter utførelse kan du fremdeles overstyre variable verdier før du kjører et annet skript.

    Det er slik du kan kjøre skript i flere regioner/steder - ved å endre bare<tt>My_loc</tt>Miljøvariables verdi og kjører skriptet igjen.

2.  TA:<strong>Slett ressursgrupper</strong>For å stoppe kostnadene fra å samle seg på virtuelle servere:

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt>--ja</tt>Før AZ -kommandoen mater en "y" for automatisk å svare på forespørselen:<br />Er du sikker på at du vil utføre denne operasjonen? (y/n): y

<hr />

## Referanser

Skript her er tilpasset fra forskjellige eksperter som er generøse med å dele koden sin:

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>av Iain Foulds, forklart i<https://aka.ms/monthoflunches>Publisert 4/30/2020.

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>av Microsoft

-   <https://github.com/timothywarner/az400>& AZ303 av Tim Warner

-   <https://github.com/zaalion/oreilly-azure-app-security>av Reza Salehi

-   <https://github.com/Azure/azure-quickstart-templates>(Armmaler)

-   <https://github.com/johnthebrit/AzureMasterClass>PowerShell -skript

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   Skylines Academy

-   Gruntwork (Terraform)

-   CloudPosse (Terraform for AWS)<br /><br />

## Vedlikeholdere

[@wilsonmar](https://github.com/wilsonmar)

## Bidra

PRS akseptert.

Hvis du redigerer denne readme, må du samsvare med[Standard-Readme](https://github.com/RichardLitt/standard-readme)Spesifikasjon.

## Tillatelse

Med © 2021 Wilson Mar

## Etikk

Dette prosjektet opererer under W3C[Etikkkode og profesjonell oppførsel](https://www.w3.org/Consortium/cepc):

> W3C er et voksende og globalt samfunn der deltakerne velger å jobbe
> sammen og i den prosessen opplever forskjeller i språk, beliggenhet,
> nasjonalitet og erfaring. I et så mangfoldig miljø, misforståelser
> og uenigheter skjer, som i de fleste tilfeller kan løses uformelt. I
> Sjeldne tilfeller kan imidlertid atferd kan skremme, trakassere eller på annen måte forstyrre en
> eller flere mennesker i samfunnet, som W3C ikke vil tåle.
>
> En etikkkode og profesjonell oppførsel er nyttig for å definere akseptert og
> akseptabel atferd og for å fremme høye standarder for profesjonell
> praksis. Det gir også et mål for egenvurdering og fungerer som en
> Kjøretøy for bedre identitet i organisasjonen.

Vi håper at samfunnsgruppen vår handler etter disse retningslinjene, og at
Deltakerne holder hverandre til disse høye standardene. Hvis du har spørsmål
Eller er bekymret for at koden ikke blir fulgt, vennligst kontakt eieren av depotet.
