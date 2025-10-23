# नीला-जल्दी

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## विषयसूची

-   [भाषा](#Language)
-   [दृष्टि](#Vision)
-   [सभी सूची](#Todos)
-   [स्थापित करना](#Install)
-   [शेल स्क्रिप्ट कोडिंग ट्रिक्स](#ShellCoding)
-   [प्रयोग](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [संदर्भ](#References)
-   [देखरेख](#maintainers)
-   [योगदान](#contributing)
-   [लाइसेंस](#license)
-   [नीति](#Ethics)

## भाषा

यहां सभी कोड, टिप्पणियाँ और दस्तावेज़ीकरण यू.एस. अंग्रेजी में लिखे गए हैं। इसलिए हम दुनिया भर के डेवलपर्स के साथ अपनी सीख साझा कर सकते हैं, अनुवाद के लिए धन्यवाद<https://github.com/dephraiim/translate-readme>

-   [अंग्रेज़ी](README.md)
-   [सरलीकृत चीनी](README.zh-CN.md)
-   [परंपरागत चीनी](README.zh-TW.md)
-   [हिंदी](README.hi.md)
-   [फ़्रेंच](README.fr.md)
-   [अरब](README.ar.md)<br /><br />

इस रेपो में अधिकांश स्क्रिप्ट हैं<strong>बैश शेल स्क्रिप्ट जो मूल रूप से MacOS और Linux पर चलती हैं</strong>.

स्क्रिप्ट कोड विंडोज़ गिट बैश शेल पर चल सकता है। 
PowerShell स्क्रिप्ट का उपयोग उन मामलों में किया जाता है जहां यही एकमात्र समाधान है।

अधिक जटिलता को संभालने के लिए, प्रोग्रामों को कोडित किया गया<a target="_blank" href="https://wilsonmar.github.io/python/">अजगर</a>या<a target="_blank" href="https://wilsonmar.github.io/golang">जाना</a>भाषा कहा जा सकता है<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">जब उचित हो</a>उनकी क्षमताओं का लाभ उठाने के लिए.

ऐसा जोखिम है कि अंतर्निहित होने पर सीएलआई फ़ंक्शन काम नहीं करेगा<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">एज़्योर रेस्ट एपीआई</a>काम करता है. इसलिए उपयुक्त होने पर पोस्टमैन फ़ाइलें शामिल की जाती हैं।

## दृष्टि

इस रेपो का उपयोग कर सकते हैं<strong>आपका समय और पैसा बचाएं</strong>और आपको मानसिक शांति और खुशी प्रदान करें।

लोग संसाधनों को चालू छोड़ देते हैं क्योंकि वे<strong>वे अपना जीवन शारीरिक श्रम को दोहराते हुए नहीं बिताना चाहते</strong>Azure पोर्टल GUI पर क्लिक करने का, जैसा कि अधिकांश Azure ट्यूटोरियल्स में बताया गया है।

यह रेपो (at<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>) में स्वचालन स्क्रिप्ट शामिल हैं जो आपको आत्मविश्वास से सक्षम बनाती हैं<strong>संसाधन समूह हटाएँ</strong>जब आप आराम कर रहे हों या खेल रहे हों क्योंकि यह आपको सक्षम बनाता है<strong>संसाधन वापस प्राप्त करें</strong>केवल कुछ आदेशों के साथ, यहां तक ​​कि बिल्कुल नई सदस्यता के साथ भी।

आप पैसे बचाते हैं क्योंकि आपको संसाधनों को चालू नहीं छोड़ना पड़ता, क्रेडिट का उपभोग नहीं करना पड़ता या अपने क्रेडिट कार्ड बिल को बढ़ाना नहीं पड़ता।

Azure पोर्टल (जो जल्दी से दोहराने योग्य नहीं है) के माध्यम से मैन्युअल माउसिंग और टाइपिंग को सटीक रूप से दोहराना तनावपूर्ण है।

तो, यह README बताता है कि आप CLI बैश टर्मिनल का उपयोग करके अपने कस्टम वातावरण को स्क्रैच से कैसे आरंभ कर सकते हैं।

<a name="Todos"></a>

## सभी सूची

-   उपनाम जोड़ें.sh
-   यह सुनिश्चित करने के लिए परीक्षण करें कि स्क्रिप्ट कोड विंडोज़ गिट बैश शेल पर चल सकता है।
-   ए<strong>चर पुनरीक्षण</strong>मंगलाचरण से पहले स्मृति चर को मान्य करने के लिए स्क्रिप्ट।

<a name="Install"></a>

## स्थापित करना

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

प्रत्येक Azure सदस्यता के लिए निम्नलिखित एक-बार की गतिविधियाँ हैं, जो मेरे गहन लेकिन संक्षिप्त ट्यूटोरियल में शामिल हैं:

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

इसमें क्लाउडड्राइव में फ़ाइलें रखने के लिए मुफ़्त Azure खाते और Azure स्टोरेज खाते का निर्माण शामिल है:

1.  Azure सदस्यता प्राप्त करें (जैसे कि विज़ुअल स्टूडियो लाइसेंस खरीदकर)।

2.  पता करने के लिए इंटरनेट ब्राउज़र (Google Chrome) का उपयोग करें<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>और लॉगइन करें.

3.  अंदर रहो<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>या पोर्टल के भीतर सीएलआई आइकन पर क्लिक करें।

4.  के लिए एक भंडारण खाता बनाएँ<strong>क्लाउड ड्राइव</strong>खोल के भीतर.

### नई सदस्यता के लिए एक वातावरण स्थापित करें

1.  इसे हाइलाइट करने के लिए नीचे दिए गए आदेश पर तीन बार क्लिक करें:

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  हाइलाइट किए गए पर राइट-क्लिक करें और अपने क्लिपबोर्ड में अस्थायी रूप से सहेजने के लिए "कॉपी करें" चुनें।

3.  अंदर आना<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>या प्रवेश करने के बाद सीएलआई आइकन पर क्लिक करें<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  सीएलआई बैश टर्मिनल विंडो पर कहीं भी राइट-क्लिक करें, फिर दबाएँ<strong>कमांड+वी</strong>क्लिपबोर्ड से चिपकाने के लिए.

5.  स्क्रिप्ट चलाने के लिए Enter दबाएँ. इसे चलने में कई मिनट लगते हैं.

    द्वारा निष्पादित कदम<a href="#az-setup-cli.sh">स्क्रिप्ट "az-setup-cli.sh" का वर्णन नीचे किया गया है</a>.

    जब पूरा हो जाए, तो आपको स्क्रिप्ट वाला फ़ोल्डर और बाईं ओर प्रॉम्प्ट देखना चाहिए, जहां यह प्रत्येक कमांड के बाद रहेगा (फ़ोल्डर पथ के अंत के बजाय):

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### setmem.sh मानों को अनुकूलित करें

Init स्क्रिप्ट एक नमूने से भी स्थापित होती है<strong>सेटमेम स्क्रिप्ट</strong>जो स्क्रिप्ट ऑपरेशन को नियंत्रित करने के लिए मेमोरी में पर्यावरण चर मानों को परिभाषित करता है। ध्यान दें कि सेटमेन फ़ाइल उससे ऊंचे फ़ोल्डर में है जहां स्क्रिप्ट कोड को जीथब पर धकेला जा सकता है। ऐसा है क्योंकि

1.  setmem.sh फ़ाइल को संपादित करने के लिए अंतर्निहित विज़ुअल स्टूडियो कोड संपादक का उपयोग करें:

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  पोर्टल GUI पर स्विच करें.

3.  सदस्यता ब्लेड खोलें. अपनी वर्तमान सदस्यता पर क्लिक करें।

4.  सदस्यता कोड के आगे कॉपी आइकन पर क्लिक करें (ताकि यह आपके क्लिपबोर्ड पर सहेजा जा सके)।

5.  कोड संपादक विंडो पर स्विच करें. वेरिएबल MY_SUBSCRIPTION_ID में मौजूदा टेक्स्ट को हाइलाइट करें और पेस्ट दबाएँ (Macs पर Command+V या Windows पर Ctrl+V)।

    प्रत्येक वातावरण के लिए एक अलग फ़ाइल हो सकती है (जैसे कि देव बनाम उत्पाद)।

6.  सहेजने के लिए कोड संपादक विंडो के दाईं ओर "..." मेनू पर क्लिक करें, फिर बाहर निकलें।

    अब आप संसाधन बनाने और प्रबंधित करने के लिए स्क्रिप्ट चला सकते हैं। 
    अधिकांश स्क्रिप्ट्स माइक्रोसॉफ्ट लर्न, क्लाउडएकेडेमी, प्लुरलसाइट, कौरसेरा आदि पर एक ट्यूटोरियल का संदर्भ देती हैं।

    Azure मशीन लर्निंग स्टूडियो में चलाने के लिए, आपको Azure ML वर्कस्पेस, कंप्यूट, इनसाइट्स और कुंजी वॉल्ट के एक या अधिक उदाहरणों की आवश्यकता है।
    उन्हें बनाने के लिए:

### az ml cli v2 का उपयोग करके कार्यस्थान बनाएं

एमएल सीएलआई v2 (पूर्वावलोकन) एक स्वचालन दृष्टिकोण प्रदान करता है:<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  पर्यावरण चर और अतिरिक्त संपादनों का उपयोग करने के लिए मैंने जो स्क्रिप्ट संशोधित की है उसे चलाएँ:

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    स्क्रिप्ट पर्यावरण में एक गिट क्लोन निष्पादित करती है।

    ### अपनी पसंद के अनुसार उपनाम कॉन्फ़िगर करें

2.  संपादित करें<tt>aliases.sh</tt>फ़ाइल करें और कीबोर्ड मैक्रोज़ हटाएं या जोड़ें।

अब जब आपके पास आवश्यक संसाधन हैं:

<a name="ShellCoding"></a>

## शेल स्क्रिप्ट कोडिंग ट्रिक्स

इस रेपो के भीतर बैश स्क्रिप्ट की सामग्री को परिभाषित कोडिंग सम्मेलनों का उपयोग करके लिखा गया है<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>जिसमें शामिल हैं:

-   <tt>स्रोत ./az-all-start.sh</tt>पर्यावरण चर और उपयोगिता फ़ंक्शन सेट करता है।

-   <tt>सेट-ओ उठाया</tt>इसे ऐसा बनाता है कि स्क्रिप्ट पहली त्रुटि पर रुक जाती है (चलने के बजाय)।

-   एक नया संसाधन समूह और सभी संसाधन बनाए जाते हैं<strong>हर रन नया</strong>निष्क्रियता के लिए कोडिंग की जटिलता को कम करने के लिए (जहां हर पुन: संचालन के अंत में स्थिति समान होती है)।

-   <tt>--संसाधन-समूह</tt>कई आदेशों पर एक आवश्यक तर्क है। यह अंतिम है इसलिए इसके ऊपर की एक पंक्ति में स्लैश लाइन गायब होने से कमांड विफल हो जाएगी।

-   उसी az शेल कमांड के भीतर एक पंक्ति के अंत में एक बैकस्लैश \\ वर्ण उस कमांड को जारी रखता है।

-   पाइथॉन प्रोग्राम को नियंत्रित करने वाले वेरिएबल (विनिर्देश) डेटा को वेरिएबल के रूप में सहेजकर पाइथॉन प्रोग्राम को पास कर दिया जाता है<strong>.env फ़ाइल</strong>Python प्रोग्राम के समान फ़ोल्डर में।

ज्यूपिटर की पायथन नोटबुक की गैलरी:

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## प्रयोग

प्रत्येक सत्र के लिए नीचे दी गई प्रत्येक गतिविधि को आज़माएँ (यह मानते हुए कि आपने उपरोक्त इंस्टाल किया है):

### व्यक्तिगत .ipynb फ़ाइल चलाएँ

के अनुसार<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">ज्यूपिटर कैसे चलायें</a>:

1.  के पास जाओ<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">एज़्योर मशीन लर्निंग स्टूडियो</a>

2.  बनाए गए उदाहरण पर क्लिक करें.

3.  क्लिक करें "<https://ml.azure.com/?tid=...">"स्टूडियो वेब यूआरएल" के अंतर्गत यूआरएल।

4.  यदि "आरंभ करें" पॉप-अप संवाद प्रकट होता है, तो इसे ख़ारिज करने के लिए X पर क्लिक करें।

5.  "नोटबुक" पर क्लिक करें।

    ### Git रिपॉजिटरी को अपने कार्यक्षेत्र फ़ाइल सिस्टम में क्लोन करें

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  अपने उपयोगकर्ता नाम (उपयोगकर्ताओं के बीच) पर माउस ले जाएँ और "फ़ाइलें अपलोड करें" चुनने के लिए "..." पर क्लिक करें।

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  जैसे फ़ोल्डर्स पर नेविगेट करें<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">तेज़</a>
    -   लाइटजीबीएम
    -   पाइटोरच
    -   आर
    -   टेंसरफ्लो<br /><br />

    ### Mnist

एज़ एमएल जॉब क्रिएट -एफ जॉब्स/ट्रेन/लाइटजीबीएम/आईरिस/जॉब.वाईएमएल --सेट कंप्यूट.टारगेट=लोकल --वेब --स्ट्रीम

1.  पर नेविगेट करें<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  "job.yml" चुनें।

3.  "अपलोड करें" पर क्लिक करें।

4.  नोटबुक को चलाने के लिए गणना का चयन करें।

    पहला सेल चलने पर रुका हुआ कंप्यूट इंस्टेंस स्वचालित रूप से प्रारंभ हो जाएगा।

5.  "रन" आइकन पर क्लिक करें.

    ### वैकल्पिक रूप से

6.  में<strong>उपयोगकर्ता फ़ाइलें</strong>आपके कार्यक्षेत्र का अनुभाग. उस सेल पर क्लिक करें जिसे आप संपादित करना चाहते हैं। यदि आपके पास इस अनुभाग में कोई नोटबुक नहीं है, तो अपने कार्यक्षेत्र में फ़ाइलें बनाएं और प्रबंधित करें देखें।

मेरे एज़्योर-क्विकली रेपो से अधिक स्क्रिप्ट:

-   एपीआई का उपयोग करके बिंग सर्च चलाएँ:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   अनुसरण करने योग्य स्क्रिप्ट द्वारा उपयोग के लिए एक Azure कुंजी वॉल्ट बनाएं:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    वैकल्पिक रूप से, इसमें एक रहस्य डालें; रहस्य दिखाओ; रहस्य हटाएं; रहस्य पुनर्प्राप्त करें; एक वीएम बनाएं; प्रबंधित सेवा पहचान; अद्यतन अनुमतियाँ; कस्टम स्क्रिप्ट एक्सटेंशन; कस्टम स्क्रिप्ट एक्सटेंशन लागू करें:

-   JupyterLab का उपयोग करके iPython नोटबुक चलाने के लिए एक मशीन लर्निंग वर्कस्पेस बनाएं:

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   Azure संज्ञानात्मक सेवाओं का उपयोग करें:

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   हेल्म चार्ट का प्रयोग करें

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   सार्वजनिक आईपी पते के साथ एक वीएम बनाएं:

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   MY_APPNAME दिखाने के लिए एक ऐप सेवा योजना, Azure वेब ऐप, परिनियोजन बनाएं।

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   दो सबनेट और एक नेटवर्क सुरक्षा समूह के साथ एक नेटवर्क बनाएं जो आने वाले ट्रैफ़िक को सुरक्षित करता है। एक सबनेट रिमोट एक्सेस ट्रैफिक के लिए है, एक वीएम के लिए वेब ट्रैफिक है जो वेब सर्वर चलाता है। फिर दो VM बनाए जाते हैं। एक एसएसएच पहुंच की अनुमति देता है और उचित नेटवर्क सुरक्षा समूह नियम लागू करता है। आप इस वीएम का उपयोग एक के रूप में करते हैं<strong>एसएसएच जंपबॉक्स</strong>फिर दूसरे VM से कनेक्ट करें जिसे वेब सर्वर के रूप में उपयोग किया जा सकता है:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   सार्वजनिक आईपी पते के साथ एक वीएम बनाएं। सक्षम एक स्टोरेज खाता है, वीएम डायग्नोस्टिक्स एक्सटेंशन के साथ बूट डायग्नोस्टिक्स लागू किया गया है:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   एक वीएम बनाएं; रिकवरी सर्विसेज वॉल्ट, एक बैकअप नीति, फिर एक वीएम बनाता है और प्रारंभिक बैकअप कार्य शुरू करने से पहले बैकअप नीति लागू करता है।

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   Dockerfile से एक Docker कंटेनर बनाएं; एकेएस बनाएं; प्रतिकृतियाँ बढ़ाएँ

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    आईपी ​​"कंटेनर में पिज़्ज़ा लंच का महीना" वेबसाइट (लोड संतुलित) दिखाता है।

-   वेबएप के लिए IoT बनाएं:

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   Azure फ़ंक्शन बनाएं:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    Azure CLI में कई फ़ंक्शन घटक उपलब्ध नहीं हैं, इसलिए अंतराल को भरने के लिए Azure पोर्टल पर मैन्युअल क्रियाओं की आवश्यकता होती है।
     "दोपहर के भोजन का महीना" ईबुक देखें।

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

स्क्रिप्ट को नीचे दिए गए सभी चरण करने चाहिए:

1.  वैकल्पिक: संपादित करें<tt>.bashrc</tt>प्रॉम्प्ट को अनुकूलित करने के लिए फ़ाइल:

    यदि आप में हैं<strong>बादल शैल</strong>(जो लिनक्स ऑपरेटिंग सिस्टम चलाता है), इन पंक्तियों को नीचे जोड़ें<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    PS1 प्रॉम्प्ट सेट करता है ताकि यह स्क्रीन पर प्रत्येक पंक्ति में एक ही स्थान पर, वर्तमान फ़ोल्डर और फ़ाइल पथ के नीचे (स्क्रीन पर विभिन्न बिंदुओं पर इसके दाईं ओर के बजाय) दिखाई दे।

    "#" at the last line of the file is a hack to make a comment out of the PS1 the system adds on its own.

2.  उस फ़ोल्डर में नेविगेट करें जिसमें डाउनलोड करने के लिए रिपॉजिटरी है:

    क्लाउड शेल के भीतर, यह है<br /><tt><strong>सीडी क्लाउडशेल</strong></tt>

    वैकल्पिक रूप से, मैं अपने लैपटॉप पर इसका उपयोग करता हूं<br /><tt>सीडी gmail_acct</tt>

3.  पिछला रेपो फ़ोल्डर हटाएँ:

    PROTIP: प्रत्येक बार कमांड को चलाने में कितना समय लगा, इसकी पहचान करने के लिए कमांड के सामने एक टाइम प्रॉक्सी कमांड जोड़ा जाता है। उदाहरण के लिए, "0m4.559s" का अर्थ लगभग 4.6 सेकंड है।

4.  रन वातावरण स्थापित करने के लिए इस रेपो को डाउनलोड करें:

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--गहराई 1</tt>उपयोग की गई जगह को बचाने के लिए, केवल नवीनतम संस्करण के डाउनलोड को निर्दिष्ट करता है।

    <tt>रास</tt>डाउनलोड वास्तव में हुआ इसकी पुष्टि करने के लिए फ़ोल्डरों और फ़ाइलों को सूचीबद्ध करता है।

5.  सभी शेल फ़ाइल को चलाने की अनुमति दें:

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  Azure प्रदाताओं को सेटअप करने के लिए स्क्रिप्ट चलाएँ:

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    प्रतिक्रिया जोड़े गए प्रदाताओं की एक सूची है।

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

    उपरोक्त को केवल एक बार करने की आवश्यकता है, लेकिन इसे दोबारा चलाना हानिकारक नहीं होगा।

7.  इसे चलाने और चलाने के लिए setmem.sh को अनुमति दें:

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  "sample-setmem.sh" को "setmem.sh" फ़ाइल में ले जाएँ (कॉपी करें और नाम बदलें)

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    PROTIP: हम फ़ाइल को वहां ले जाते हैं जहां इसे कभी भी किसी रिपॉजिटरी (GitHub, GitLab, आदि) पर अपलोड नहीं किया जाएगा।

### Setmem.sh में मानों को मैन्युअल रूप से अनुकूलित करें

9.  प्रोग्राम "कोड" (विज़ुअल स्टूडियो कोड) का उपयोग करके संपादन के लिए फ़ाइल खोलें:

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>उपयोग किया जाता है क्योंकि फ़ाइल, जिसमें रहस्य हैं, एक फ़ोल्डर में है जिसे कभी भी GitHub पर नहीं धकेला जाना चाहिए।

10. ../setmem.sh फ़ाइल को संपादित करने के लिए टेक्स्ट एडिटर प्रोग्राम का उपयोग करें:

    स्क्रिप्ट्स रही हैं<strong>सामान्यीकृत</strong>स्क्रिप्ट में हार्ड-कोडित मानों को प्रतिस्थापित करते हुए पर्यावरण चर द्वारा। PROTIP: हार्ड-कोडिंग के बजाय वेरिएबल का उपयोग करने से टाइपो और गलत कॉन्फ़िगरेशन से बचा जा सकता है।

    नीचे दी गई पंक्तियाँ प्रत्येक चर के लिए मानों को परिभाषित करती हैं ताकि स्क्रिप्ट फ़ाइल को बदलने की आवश्यकता के बिना एकाधिक रन विभिन्न मानों का उपयोग कर सकें।

11. में<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com सदस्यता ब्लेड</a>, वह सदस्यता चुनें जिसका आप उपयोग करना चाहते हैं, फिर क्लिपबोर्ड पर कॉपी करने के लिए आइकन पर क्लिक करें।

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    फ़ाइल में, आईडी को हाइलाइट करें और पेस्ट करें:

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. में<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">portal.azure.com किरायेदार ब्लेड</a>, उस किरायेदार का चयन करें जिसका आप उपयोग करना चाहते हैं, फिर क्लिपबोर्ड पर कॉपी करने के लिए आइकन पर क्लिक करें।

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    फ़ाइल में, आईडी को हाइलाइट करें और पेस्ट करें:

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    कार्य: लंबे समय से चल रहे Azure KeyVault से रहस्यों को पुनः प्राप्त करने के लिए उनके निर्यात विवरणों को कॉल के साथ बदलें। लेकिन इस फ़ाइल में कोई भी तब तक नहीं होगा जब तक कि वे आपके खाते के अंतर्गत Azure में ठीक से लॉग इन न हों।

13. MY_LOC (स्थान = क्षेत्र) और अन्य डिफ़ॉल्ट संपादित करें।

14. फ़ाइल के निचले भाग में, एक स्टेटमेंट जोड़ें जो किसी एक वेरिएबल को प्रिंट करता है, ताकि आप जान सकें कि निर्यात स्टेटमेंट लिया गया:

    बैश स्क्रिप्ट में:

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. फ़ाइल सहेजें। क्लाउड शेल में, कमांड + क्यू दबाएँ या सेव दबाने के लिए "..." पर क्लिक करें, फिर बंद करें।

### प्रत्येक कार्य सत्र

1.  प्रत्येक सत्र की शुरुआत में अपने कस्टम स्क्रिप्ट रेपो के ठीक ऊपर फ़ोल्डर में स्क्रिप्ट को आमंत्रित करें:

    <pre><strong>source ../setmem.sh
    </strong></pre>

    ध्यान दें: स्क्रिप्ट को चलाने के लिए "स्रोत" का उपयोग करें ताकि स्क्रिप्ट में परिभाषित पर्यावरण चर स्क्रिप्ट के पूरा होने के बाद दिखाई दे सकें, और आपके द्वारा लॉन्च किए गए किसी भी प्रोग्राम द्वारा विरासत में प्राप्त किए जा सकें। ऐसा इसलिए है क्योंकि स्रोत स्क्रिप्ट को वर्तमान शेल में चलाता है। लेकिन ध्यान रखें कि कोई भी एक्जिट स्टेटमेंट रन को रोक देगा।

    वैकल्पिक रूप से,

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    निष्पादन के बाद, आप किसी अन्य स्क्रिप्ट को चलाने से पहले अभी भी परिवर्तनीय मानों को ओवरराइड कर सकते हैं।

    इस प्रकार आप कई क्षेत्रों/स्थानों के लिए स्क्रिप्ट चला सकते हैं - केवल परिवर्तन करके<tt>MY_LOC</tt>पर्यावरण चर का मान और स्क्रिप्ट को फिर से चलाना।

2.  प्रोटोटाइप:<strong>संसाधन समूह हटाएँ</strong>वर्चुअल सर्वर पर शुल्क जमा होने से रोकने के लिए:

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt>--हाँ</tt>इससे पहले कि az कमांड स्वचालित रूप से अनुरोध का उत्तर देने के लिए "y" फीड करे:<br />क्या आप आश्वस्त हैं कि आपकी यह कार्रवाई करने की इच्छा है? (य/एन): य

<hr />

## संदर्भ

यहां की स्क्रिप्ट विभिन्न विशेषज्ञों द्वारा अपनाई गई हैं जो अपना कोड साझा करने में उदार हैं:

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>इयान फ़ोल्ड्स द्वारा, में समझाया गया<https://aka.ms/monthoflunches>4/30/2020 को प्रकाशित।

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>माइक्रोसॉफ्ट द्वारा

-   <https://github.com/timothywarner/az400>और az303 टिम वार्नर द्वारा

-   <https://github.com/zaalion/oreilly-azure-app-security>रेजा सालेही द्वारा

-   <https://github.com/Azure/azure-quickstart-templates>(एआरएम टेम्पलेट्स)

-   <https://github.com/johnthebrit/AzureMasterClass>पॉवरशेल स्क्रिप्ट

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   स्काईलाइन्स अकादमी

-   ग्रंटवर्क (टेराफ़ॉर्म)

-   CloudPosse (AWS के लिए टेराफ़ॉर्म)<br /><br />

## देखरेख

[@विल्सनमर](https://github.com/wilsonmar)

## योगदान

पीआर स्वीकार किए गए.

यदि इस README को संपादित कर रहे हैं, तो कृपया इसके अनुरूप बनें[मानक-रीडमी](https://github.com/RichardLitt/standard-readme)विशिष्टता.

## लाइसेंस

साथ में © 2021 विल्सन मार्च

## नीति

यह परियोजना W3C के अंतर्गत संचालित होती है[आचार संहिता और व्यावसायिक आचरण](https://www.w3.org/Consortium/cepc):

> W3C एक बढ़ता हुआ और वैश्विक समुदाय है जहां प्रतिभागी काम करना चुनते हैं
> एक साथ और उस प्रक्रिया में भाषा, स्थान, में अंतर का अनुभव करते हैं
> राष्ट्रीयता, और अनुभव। इतने विविध वातावरण में, गलतफहमियाँ
> और असहमति होती है, जिसे ज्यादातर मामलों में अनौपचारिक रूप से हल किया जा सकता है। में
> हालाँकि, दुर्लभ मामले, व्यवहार किसी को डरा सकता है, परेशान कर सकता है या अन्यथा बाधित कर सकता है
> या समुदाय में अधिक लोग, जिसे W3C बर्दाश्त नहीं करेगा।
>
> स्वीकृत और परिभाषित करने के लिए आचार संहिता और व्यावसायिक आचरण उपयोगी है
> स्वीकार्य व्यवहार और पेशेवर के उच्च मानकों को बढ़ावा देना
> अभ्यास। यह स्व-मूल्यांकन के लिए एक बेंचमार्क भी प्रदान करता है और एक के रूप में कार्य करता है
> संगठन की बेहतर पहचान के लिए वाहन।

हम आशा करते हैं कि हमारा सामुदायिक समूह इन दिशानिर्देशों के अनुसार कार्य करेगा
प्रतिभागी एक-दूसरे को इन उच्च मानकों पर रखते हैं। यदि आपके कोई प्रश्न हैं तो
या चिंतित हैं कि कोड का पालन नहीं किया जा रहा है, कृपया रिपॉजिटरी के मालिक से संपर्क करें।
