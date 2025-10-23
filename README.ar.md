# الأزرق السماوي بسرعة

![license](https://img.shields.io/github/license/wilsonmar/azure-quickly)[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg)](https://github.com/RichardLitt/standard-readme)[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## جدول المحتويات

-   [لغة](#Language)
-   [رؤية](#Vision)
-   [كل القائمة](#Todos)
-   [ثَبَّتَ](#Install)
-   [حيل ترميز نصوص شل](#ShellCoding)
-   [الاستخدام](#Usage)
-   [az-setup-cli.sh](#az-setup-cli.sh)
-   [مراجع](#References)
-   [المشرفون](#maintainers)
-   [المساهمة](#contributing)
-   [رخصة](#license)
-   [أخلاق مهنية](#Ethics)

## لغة

جميع التعليمات البرمجية والتعليقات والوثائق هنا مكتوبة باللغة الإنجليزية الأمريكية. حتى نتمكن من مشاركة ما تعلمناه مع المطورين في جميع أنحاء العالم، وذلك بفضل الترجمات<https://github.com/dephraiim/translate-readme>

-   [إنجليزي](README.md)
-   [الصينية المبسطة](README.zh-CN.md)
-   [الصينية التقليدية](README.zh-TW.md)
-   [الهندية](README.hi.md)
-   [فرنسي](README.fr.md)
-   [عربى](README.ar.md)<br /><br />

معظم البرامج النصية في هذا الريبو هي<strong>البرامج النصية لـ Bash Shell التي تعمل أصلاً على نظامي التشغيل MacOS وLinux</strong>.

يمكن تشغيل التعليمات البرمجية النصية على Windows Git Bash Shell. 
يتم استخدام البرامج النصية PowerShell في الحالات التي يكون فيها هذا هو الحل الوحيد.

ولمعالجة المزيد من التعقيد، تم ترميز البرامج<a target="_blank" href="https://wilsonmar.github.io/python/">بايثون</a>أو<a target="_blank" href="https://wilsonmar.github.io/golang">يذهب</a>يمكن أن تسمى اللغة<a target="_blank" href="https://medium.com/capital-one-tech/bashing-the-bash-replacing-shell-scripts-with-python-d8d201bc0989">عندما يكون ذلك مناسبا</a>للاستفادة من قدراتهم.

هناك خطر من أن وظائف CLI قد لا تعمل عندما تكون أساسية<a target="_blank" href="https://docs.microsoft.com/en-us/rest/api/azure/">أزور ريست API</a>لا يعمل. لذلك يتم تضمين ملفات Postman عند الاقتضاء.

## رؤية

باستخدام هذا الريبو يمكن<strong>يوفر لك الوقت والمال</strong>ويعطيك بعض راحة البال والسعادة.

يترك الأشخاص الموارد قيد التشغيل لأنهم<strong>لا يريدون قضاء حياتهم في تكرار الكدح اليدوي</strong>النقر على واجهة المستخدم الرسومية لـ Azure Portal، كما هو موضح في معظم البرامج التعليمية لـ Azure.

هذا الريبو (في<a target="_blank" href="https://github.com/wilsonmar/azure-quickly">https&#x3A;//github.com/wilsonmar/azure-quickly</a>) يحتوي على نصوص برمجية للأتمتة تمكنك من ذلك بثقة<strong>حذف مجموعات الموارد</strong>عندما تستريح أو تلعب لأنه يمكّنك من ذلك<strong>الحصول على الموارد مرة أخرى</strong>مع عدد قليل من الأوامر، حتى مع اشتراك جديد تمامًا.

يمكنك توفير المال لأنك لا تضطر إلى ترك الموارد قيد التشغيل، أو استهلاك الاعتمادات، أو زيادة فاتورة بطاقتك الائتمانية.

من المرهق تكرار استخدام الماوس والكتابة يدويًا بدقة من خلال Azure Portal (وهو أمر لا يمكن تكراره بسرعة).

لذلك، يشرح هذا الملف التمهيدي كيف يمكنك بدء بيئتك المخصصة من البداية باستخدام محطة CLI Bash.

<a name="Todos"></a>

## كل القائمة

-   إضافة الاسم المستعار.sh
-   اختبار للتأكد من إمكانية تشغيل التعليمات البرمجية النصية على Windows Git Bash Shell.
-   أ<strong>فحص المتغيرات</strong>البرنامج النصي للتحقق من صحة متغيرات الذاكرة قبل الاستدعاء.

<a name="Install"></a>

## ثَبَّتَ

![azure-quickly-cli.png](https://user-images.githubusercontent.com/300046/120510665-e3370580-c386-11eb-947d-477191a8888e.png)

فيما يلي أنشطة لمرة واحدة لكل اشتراك في Azure، والتي تمت تغطيتها في البرنامج التعليمي العميق والموجز على الرابط:

   <ul><a target="_blank" href="https://wilsonmar.github.io/azure-onboarding/">https://wilsonmar.github.io/azure-onboarding</a>
   </ul>

ويغطي إنشاء حسابات Azure مجانية وحسابات Azure Storage للاحتفاظ بالملفات في محرك أقراص سحابي:

1.  احصل على اشتراك Azure (مثل شراء ترخيص Visual Studio).

2.  استخدم متصفح الانترنت (جوجل كروم) للعنوان<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>وتسجيل الدخول.

3.  كن في<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>أو انقر فوق أيقونة CLI داخل البوابة.

4.  إنشاء حساب تخزين ل<strong>com.clouddrive</strong>داخل القشرة.

### قم بإعداد بيئة لاشتراك جديد

1.  انقر ثلاث مرات على الأمر أدناه لتمييزه:

    <pre><strong>bash -c "$(curl -fsSL https://raw.githubusercontent.com/wilsonmar/azure-quickly/master/az-setup-cli.sh)" -v -i</strong></pre>

2.  انقر بزر الماوس الأيمن فوق العنصر المميز وحدد "نسخ" لحفظ العنصر المميز مؤقتًا في الحافظة الخاصة بك.

3.  أدخل<a target="_blank" href="https://shell.azure.com/">https&#x3A;//shell.azure.com</a>أو انقر على أيقونة CLI بعد الدخول<a target="_blank" href="https://portal.azure.com/">https&#x3A;//portal.azure.com</a>

4.  انقر بزر الماوس الأيمن في أي مكان على نافذة محطة CLI Bash، ثم اضغط<strong>الأمر+V</strong>للصق من الحافظة.

5.  اضغط على Enter لتشغيل البرنامج النصي. يستغرق عدة دقائق للتشغيل.

    الخطوات التي تم تنفيذها بواسطة<a href="#az-setup-cli.sh">تم وصف البرنامج النصي "az-setup-cli.sh" أدناه</a>.

    عند الانتهاء، من المفترض أن ترى المجلد الذي يحتوي على البرامج النصية والموجه على اليسار، حيث سيبقى بعد كل أمر (بدلاً من نهاية مسار المجلد):

    <pre>~/clouddrive/azure-quickly
    $ _</pre>

### تخصيص قيم setmem.sh

يقوم البرنامج النصي init أيضًا بإنشاء ملف<strong>البرنامج النصي setmem</strong>الذي يحدد قيم متغيرات البيئة في الذاكرة للتحكم في تشغيل البرنامج النصي. لاحظ أن ملف setmen موجود في مجلد أعلى من حيث يمكن دفع كود البرنامج النصي إلى github. هذا بسبب

1.  استخدم محرر Visual Studio Code المدمج لتحرير الملف setmem.sh:

    <pre><strong>code ../setmem.sh
    </strong></pre>

2.  قم بالتبديل إلى واجهة المستخدم الرسومية للبوابة.

3.  افتح شفرة الاشتراك. انقر على اشتراكك الحالي.

4.  انقر فوق أيقونة النسخ بجوار رمز الاشتراك (حتى يتم حفظه في الحافظة الخاصة بك).

5.  قم بالتبديل إلى نافذة محرر التعليمات البرمجية. قم بتمييز النص الموجود في المتغير MY_SUBSCRIPTION_ID واضغط على "لصق" (Command+V على أجهزة Mac أو Ctrl+V على نظام Windows).

    قد يكون هناك ملف مختلف لكل بيئة (مثل dev vs.prod).

6.  انقر فوق القائمة "..." الموجودة على يمين نافذة Code Editor للحفظ، ثم قم بالخروج.

    يمكنك الآن تشغيل البرامج النصية لإنشاء الموارد وإدارتها. 
    تشير معظم البرامج النصية إلى برنامج تعليمي في Microsoft Learn وCloudAcademy وPluralsight وCoursera وما إلى ذلك.

    للتشغيل في استوديو Azure Machine Learning، تحتاج إلى مثيل واحد أو أكثر من Azure ML Workspace وCompute وInsights وKey Vault.
    لإنشائها:

### إنشاء مساحة عمل باستخدام az ml cli v2

يوفر ML CLI v2 (معاينة) نهجًا واحدًا للأتمتة:<br /><a target="_blank" href="https://github.com/Azure/azureml-examples/blob/main/cli/setup.sh">github.com/Azure/azureml-examples/blob/main/cli/setup.sh</a>.

1.  قم بتشغيل البرنامج النصي الذي قمت بتعديله من ذلك لاستخدام متغيرات البيئة والتعديلات الإضافية:

    <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlcli2.sh">az-mlcli2.sh</a>
    </strong></pre>

    يقوم البرنامج النصي بإجراء استنساخ git في البيئة.

    ### تكوين الأسماء المستعارة ترضيك

2.  تحرير<tt>aliases.sh</tt>ملف وإزالة أو إضافة وحدات ماكرو لوحة المفاتيح.

الآن بعد أن أصبحت لديك الموارد اللازمة:

<a name="ShellCoding"></a>

## حيل ترميز نصوص شل

تتم كتابة المحتويات الموجودة داخل نصوص Bash داخل هذا الريبو باستخدام اصطلاحات الترميز المحددة في<a target="_blank" href="https://wilsonmar.github.io/bash-codng">https&#x3A;//wilsonmar.github.io/bash-coding</a>والتي تشمل:

-   <tt>المصدر ./az-all-start.sh</tt>يقوم بإعداد متغيرات البيئة ووظائف الأداة المساعدة.

-   <tt>مجموعة -o مرفوعة</tt>يجعله يتوقف البرنامج النصي عند الخطأ الأول (بدلاً من الاستمرار فيه).

-   يتم إنشاء مجموعة موارد جديدة وجميع الموارد<strong>جديد في كل شوط</strong>لتقليل تعقيد ترميز العجز الجنسي (حيث تكون الحالة هي نفسها في نهاية كل عملية إعادة تشغيل).

-   <tt>--resource-group</tt>هي وسيطة مطلوبة في العديد من الأوامر. إنه الأخير بحيث يؤدي فقدان خط مائل فوقه إلى فشل الأمر.

-   يستمر حرف الشرطة المائلة العكسية \\ في نهاية السطر داخل نفس أمر az Shell في هذا الأمر.

-   يتم تمرير البيانات (المواصفات) المتغيرة التي تتحكم في برامج بايثون إلى برامج بايثون عن طريق حفظها كمتغيرات في ملف<strong>ملف .env</strong>في نفس المجلد مثل برنامج بايثون.

معرض Jupyter لدفاتر ملاحظات Python:

-   <https://github.com/jupyter/jupyter/wiki/A-gallery-of-interesting-Jupyter-Notebooks>

<hr />

<a name="Usage"></a>

## الاستخدام

جرب كل من الأنشطة أدناه لكل جلسة (على افتراض أنك قمت بالتثبيت أعلاه):

### قم بتشغيل ملف .ipynb فردي

وفق<a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/how-to-run-jupyter-notebooks">كيفية تشغيل جوبيتر</a>:

1.  اذهب الى<a target="_blank" href="https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.MachineLearningServices%2Fworkspaces">استوديو أزور لتعلم الآلة</a>

2.  انقر فوق المثيل الذي تم إنشاؤه.

3.  انقر فوق "<https://ml.azure.com/?tid=...">عنوان URL ضمن "عنوان URL للويب الخاص بالاستوديو".

4.  إذا ظهر مربع الحوار المنبثق "البدء"، فانقر فوق X لتجاهله.

5.  انقر فوق "أجهزة الكمبيوتر المحمولة".

    ### استنساخ مستودعات Git في نظام ملفات مساحة العمل لديك

    <a target="_blank" href="https://docs.microsoft.com/en-us/azure/machine-learning/concept-train-model-git-integration?WT.mc_id=Portal-Microsoft_Azure_Support#clone-git-repositories-into-your-workspace-file-system">\*</a>

6.  قم بالماوس فوق اسم المستخدم الخاص بك (بين المستخدمين) وانقر فوق "..." لاختيار "تحميل الملفات".

    <img width="361" alt="az-ml-notebooks-722x312" src="https://user-images.githubusercontent.com/300046/120910778-eeb45600-c63e-11eb-8bd2-24725c7fd74e.png">

7.  انتقل إلى المجلدات باسم<a target="_blank" href="https://github.com/Azure/azureml-examples/tree/main/cli/jobs/train">https&#x3A;//github.com/Azure/azureml-examples/tree/main/cli/jobs/train</a>:

    -   <a target="_blank" href="https://forums.fast.ai/t/platform-azure/35920">سريع</a>
    -   com.lightgbm
    -   pytorch
    -   ص
    -   com.tensorflow<br /><br />

    ### منيست

إنشاء وظيفة من الألف إلى الياء -f jobs/train/lightgbm/iris/job.yml --set compute.target=local --web --stream

1.  انتقل إلى<https://github.com/Azure/azureml-examples/blob/main/cli/jobs/train/fastai/mnist/>

2.  حدد "job.yml".

3.  انقر فوق "تحميل".

4.  حدد الحساب الذي تريد تشغيل الكمبيوتر الدفتري فيه.

    سيبدأ مثيل الحوسبة المتوقف تلقائيًا عند تشغيل الخلية الأولى.

5.  انقر على أيقونة "تشغيل".

    ### بالتناوب

6.  في<strong>ملفات المستخدم</strong>قسم من مساحة العمل الخاصة بك. انقر على الخلية التي ترغب في تحريرها. إذا لم يكن لديك أي دفاتر ملاحظات في هذا القسم، فراجع إنشاء الملفات وإدارتها في مساحة العمل الخاصة بك.

المزيد من البرامج النصية من الريبو azure-quickly الخاص بي:

-   قم بتشغيل بحث Bing باستخدام واجهة برمجة التطبيقات:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-bing-cli.sh">az-bing-cli.sh</a>
     </strong></pre>


-   قم بإنشاء Azure Key Vault لاستخدامه بواسطة البرامج النصية للمتابعة:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-keyvault-cli.sh">az-keyvault-cli.sh</a>
     </strong></pre>

    اختياريًا، ضع سرًا فيه؛ أظهر السر؛ حذف السر؛ استعادة السر؛ إنشاء جهاز افتراضي؛ هوية الخدمة المدارة؛ أذونات التحديث؛ ملحق البرنامج النصي المخصص؛ تطبيق ملحق البرنامج النصي المخصص:

-   قم بإنشاء مساحة عمل للتعلم الآلي لتشغيل iPython Notebooks باستخدام JupyterLab:

     <pre><strong>export MY_MLWORKSPACE_NAME="mela"
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-mlworkspace-cli.sh">az-mlworkspace-cli.sh</a>
     </strong></pre>


-   استخدم خدمات Azure المعرفية:

     <pre><strong>export MY_COG_ACCT="cogme"
     export MY_COG_PRICING_TIER="F0"  # or S0
     ./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-cog-cli.sh">az-cog-cli.sh</a>
     </strong></pre>

-   استخدم مخططات هيلم

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-helm-cli.sh">az-helm-cli.sh</a>
     </strong></pre>

-   قم بإنشاء جهاز افتراضي بعنوان IP عام:

     <pre><strong>./<a href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-cli.sh">az-vm-cli.sh</a>
     </strong></pre>

-   قم بإنشاء خطة خدمة التطبيق، تطبيق Azure Web App، النشر، لإظهار MY_APPNAME.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-webapp-cli.sh">az-webapp-cli.sh</a>
     </strong></pre>

-   قم بإنشاء شبكة تحتوي على شبكتين فرعيتين ومجموعة أمان الشبكة التي تعمل على تأمين حركة المرور الواردة. شبكة فرعية واحدة مخصصة لحركة مرور الوصول عن بعد، والأخرى هي حركة مرور الويب للأجهزة الافتراضية التي تقوم بتشغيل خادم الويب. يتم بعد ذلك إنشاء جهازين افتراضيين. أحدهما يسمح بالوصول إلى SSH ويتم تطبيق قواعد مجموعة أمان الشبكة المناسبة. يمكنك استخدام هذا VM باعتباره<strong>صندوق القفز SSH</strong>للاتصال بعد ذلك بالجهاز الظاهري الثاني الذي يمكن استخدامه كخادم ويب:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-jumpbox-cli.sh">az-vm-jumpbox-cli.sh</a>
     </strong></pre> 

-   قم بإنشاء جهاز افتراضي بعنوان IP عام. تم تمكين حساب التخزين وتشخيصات التمهيد مع تطبيق ملحق تشخيص VM:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-diag-cli.sh">az-vm-diag-cli.sh</a>
     </strong></pre>

-   إنشاء جهاز افتراضي؛ يقوم قبو خدمات الاسترداد، وهو سياسة النسخ الاحتياطي، بإنشاء جهاز افتراضي وتطبيق سياسة النسخ الاحتياطي قبل بدء مهمة النسخ الاحتياطي الأولية.

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-vm-backup-cli.sh">az-vm-backup-cli.sh</a>
     </strong></pre>

-   إنشاء حاوية Docker من ملف Dockerfile؛ إنشاء AKS؛ توسيع نطاق النسخ المتماثلة

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-aks-cli.sh">az-aks-cli.sh</a>
     </strong></pre>

    يعرض عنوان IP الموقع الإلكتروني "شهر وجبات غداء البيتزا في حاوية" (متوازن التحميل).

-   إنشاء إنترنت الأشياء لتطبيق WebApp:

     <pre><strong>export MY_PROJECT_FOLDER="iot-project"
    export MY_IOT_HUB_NAME="hubahuba"
    export MY_IOT_HUB_GROUP="hubgroupie"
    ./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/iot/az-iot-cli.sh">az-iot-cli.sh</a>
     </strong></pre>

-   إنشاء وظائف أزور:

     <pre><strong>./<a target="_blank" href="https://github.com/wilsonmar/azure-quickly/blob/main/az-functions-temp.sh">az-functions-temp.sh</a>
     </strong></pre>

    لا تتوفر العديد من مكونات الوظائف في Azure CLI، لذا يلزم اتخاذ إجراءات يدوية على بوابة Azure لملء الفجوات.
     راجع الكتاب الإلكتروني "شهر الغداء".

<https://github.com/Azure/azure-quickstart-templates>

<hr />

<a name="az-setup-cli.sh"></a>

## az-setup-cli.sh

يجب أن يقوم البرنامج النصي بجميع الخطوات أدناه:

1.  اختياري: قم بتحرير<tt>.bashrc</tt>ملف لتخصيص المطالبة:

    إذا كنت في<strong>سحابة شل</strong>(الذي يعمل بنظام التشغيل Linux)، أضف هذه السطور إلى أسفل الملف<strong>.bashrc</strong>:

    <pre>export PS1="\n  \w\[\033[33m\]\n$ "
    #</pre>

    يقوم PS1 بتعيين المطالبة بحيث تظهر في نفس المكان على الشاشة في كل سطر، أسفل المجلد الحالي ومسار الملف (بدلاً من ظهوره على يمينه في نقاط مختلفة على الشاشة).

    "#" في السطر الأخير من الملف عبارة عن اختراق لإبداء تعليق من جهاز PS1 الذي يضيفه النظام من تلقاء نفسه.

2.  انتقل إلى المجلد الذي يحتوي على المستودع المراد تنزيله:

    داخل Cloud Shell، إنه<br /><tt><strong>قرص مضغوط كلاودشيل</strong></tt>

    بالتناوب، على جهاز الكمبيوتر المحمول، أستخدمه<br /><tt>القرص المضغوط gmail_acct</tt>

3.  قم بإزالة مجلد الريبو السابق:

    PROTIP: تتم إضافة أمر وكيل الوقت أمام الأوامر لتحديد عدد الوقت المستغرق لتشغيل الأمر في كل مرة. على سبيل المثال، "0m4.559s" تعني حوالي 4.6 ثانية.

4.  قم بتنزيل هذا الريبو لإنشاء بيئة تشغيل:

    <pre><strong>git clone https://github.com/wilsonmar/azure-quickly.git --depth 1 
    cd azure-quickly
    ls
    </strong></pre>

    <tt>--العمق 1</tt>يحدد تنزيل الإصدار الأحدث فقط، لتوفير المساحة المستخدمة.

    <tt>ليرة سورية</tt>يسرد المجلدات والملفات لتأكيد حدوث التنزيل بالفعل.

5.  امنح جميع أذونات ملف Shell للتشغيل:

    <pre><strong>chmod +x *.sh
    </strong></pre>

6.  قم بتشغيل البرنامج النصي لإعداد موفري Azure:

       <pre><strong>source az-providers-setup.sh
       </strong></pre>

    الرد عبارة عن قائمة مقدمي الخدمات المضافة.

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

    ما سبق يجب القيام به مرة واحدة فقط، ولكن تشغيله مرة أخرى لن يكون ضارًا.

7.  امنح setmem.sh أذونات لتشغيله وتشغيله:

    <pre><strong>chmod +x ../setmem.sh
    source ../setmem.sh
    </strong></pre>

8.  نقل (نسخ وإعادة تسمية) "sample-setmem.sh" إلى ملف "setmem.sh"

    <pre><strong>mv setmem-sample.sh ../setmem.sh
    </strong></pre>

    نصيحة: نقوم بنقل الملف حيث لن يتم تحميله أبدًا إلى أي مستودع (GitHub، GitLab، وما إلى ذلك).

### تخصيص القيم يدويًا في setmem.sh

9.  افتح الملف للتحرير باستخدام برنامج "كود" (Visual Studio Code):

    <pre><strong>code ../setmem.sh
    </strong></pre>

    <tt>..</tt>يتم استخدامه لأن الملف الذي يحتوي على أسرار موجود في مجلد ولا ينبغي أبدًا دفعه إلى GitHub.

10. استخدم برنامج محرر النصوص لتحرير الملف ../setmem.sh:

    كانت البرامج النصية<strong>معمم</strong>عن طريق استبدال متغيرات البيئة بالقيم المرمزة في البرامج النصية. نصيحة: يؤدي استخدام المتغير بدلاً من الترميز الثابت إلى تجنب الأخطاء المطبعية والتكوينات الخاطئة.

    تحدد الأسطر الموجودة أدناه قيمًا لكل متغير بحيث يمكن لعمليات التشغيل المتعددة استخدام قيم مختلفة، دون الحاجة إلى تغيير ملف البرنامج النصي.

11. في<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com شفرة الاشتراك</a>، وحدد الاشتراك الذي تريد استخدامه، ثم انقر فوق أيقونة النسخ إلى الحافظة.

    ![az-copy-sponsorship-195x65](https://user-images.githubusercontent.com/300046/117761823-45b44000-b1e5-11eb-976c-213d918ca163.png)

    في الملف، قم بتمييز المعرف ولصقه:

    <pre>export MY_SUBSCRIPTION_NAME="Azure Pass - Sponsorship"
    export MY_SUBSCRIPTION_ID="11cb040d-4e32-4524-bc8e-0bee213dddae"  # for gmail 
    </pre>

12. في<a target="_blank" href="https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade">Portal.azure.com شفرة المستأجر</a>، وحدد المستأجر الذي تريد استخدامه، ثم انقر فوق أيقونة النسخ إلى الحافظة.

    ![az-copy-tenant-129x71](https://user-images.githubusercontent.com/300046/117761778-346b3380-b1e5-11eb-8d9b-4e01211db392.png)

    في الملف، قم بتمييز المعرف ولصقه:

    <pre>export TENANT_ID="22223348-f7f0-4cc2-addc-11021d882720"           # for gmail, in Portal
    </pre>

    المهام المطلوبة: استبدل بيانات تصدير الأسرار باستدعاءات لاستردادها من Azure KeyVault طويل الأمد. ولكن لن يكون هناك أي شخص آخر في هذا الملف ما لم يتم تسجيل دخوله بشكل صحيح إلى Azure ضمن حسابك.

13. قم بتحرير MY_LOC (الموقع = المنطقة) والإعدادات الافتراضية الأخرى.

14. في الجزء السفلي من الملف، أضف عبارة تطبع أحد المتغيرات، حتى تعرف أن عبارات التصدير أخذت:

    في نص باش:

    <pre><strong>echo "MY_RG=$MY_RG"</strong></pre>

15. احفظ الملف. في Cloud Shell، اضغط على Command+Q أو انقر على "..." للضغط على Save، ثم Close.

### كل جلسة عمل

1.  في بداية كل جلسة، قم باستدعاء البرنامج النصي الموجود في المجلد الموجود أعلى مستودع البرامج النصية المخصصة مباشرةً:

    <pre><strong>source ../setmem.sh
    </strong></pre>

    ملاحظة: استخدام "المصدر" لتشغيل البرنامج النصي بحيث تكون متغيرات البيئة المحددة في البرنامج النصي مرئية بعد انتهاء البرنامج النصي، ويتم توريثها بواسطة أي برامج تقوم بتشغيلها منه. وذلك لأن المصدر يقوم بتشغيل البرنامج النصي في الصدفة الحالية. ولكن لاحظ أن أي بيان خروج من شأنه أن يوقف التشغيل.

    بالتناوب،

    <pre>source <(curl -s -L https://example.com/install.sh)</pre>

    بعد التنفيذ، لا يزال بإمكانك تجاوز القيم المتغيرة قبل تشغيل برنامج نصي آخر.

    هذه هي الطريقة التي يمكنك بها تشغيل البرامج النصية لعدة مناطق/مواقع - عن طريق تغيير ملف<tt>MY_LOC</tt>قيمة متغير البيئة وتشغيل البرنامج النصي مرة أخرى.

2.  النموذج:<strong>حذف مجموعات الموارد</strong>لمنع تراكم الرسوم على الخوادم الافتراضية:

    <pre><strong>time az group delete --name "${MY_RG}" --yes   # takes several minutes
    </strong></pre>

    <tt>--نعم</tt>قبل أن يقوم الأمر az بتغذية "y" للرد على الطلب تلقائيًا:<br />هل أنت متأكد أنك تريد إجراء هذه العملية؟ (ص / ن): ذ

<hr />

## مراجع

النصوص البرمجية هنا مقتبسة من خبراء مختلفين كرماء في مشاركة التعليمات البرمجية الخاصة بهم:

-   <https://github.com/fouldsy/azure-mol-samples-2nd-ed>بواسطة إيان فولز، وأوضح في<https://aka.ms/monthoflunches>تم النشر بتاريخ 30/04/2020.

-   <https://github.com/MicrosoftLearning/AZ-303-Microsoft-Azure-Architect-Technologies>

-   <https://github.com/MicrosoftLearning/AZ500-AzureSecurityTechnologies>

-   <https://github.com/Azure/azure-cli>بواسطة مايكروسوفت

-   <https://github.com/timothywarner/az400>& az303 بواسطة تيم وارنر

-   <https://github.com/zaalion/oreilly-azure-app-security>بواسطة رضا الصالحي

-   <https://github.com/Azure/azure-quickstart-templates>(قوالب أرم)

-   <https://github.com/johnthebrit/AzureMasterClass>البرامج النصية بوويرشيل

-   <https://github.com/terraform-providers/terraform-provider-azurerm>

-   أكاديمية سكاي لاينز

-   العمل الشائك (Terraform)

-   CloudPosse (Terraform لـ AWS)<br /><br />

## المشرفون

[@ ويلسونمار](https://github.com/wilsonmar)

## المساهمة

العلاقات العامة مقبولة.

في حالة تحرير هذا الملف التمهيدي، يرجى الالتزام بـ[الملف التمهيدي القياسي](https://github.com/RichardLitt/standard-readme)مواصفة.

## رخصة

مع © 2021 ويلسون مار

## أخلاق مهنية

يعمل هذا المشروع تحت W3C[مدونة الأخلاقيات والسلوك المهني](https://www.w3.org/Consortium/cepc):

> W3C هو مجتمع متنامي وعالمي حيث يختار المشاركون العمل
> معًا وفي تلك العملية نواجه اختلافات في اللغة والموقع،
> الجنسية والخبرة. في مثل هذه البيئة المتنوعة، هناك سوء فهم
> وتحدث الخلافات، والتي في معظم الحالات يمكن حلها بشكل غير رسمي. في
> ومع ذلك، في حالات نادرة، يمكن للسلوك أن يخيف الشخص أو يضايقه أو يعطله
> أو المزيد من الأشخاص في المجتمع، وهو ما لن يتسامح معه W3C.
>
> تعتبر مدونة قواعد الأخلاق والسلوك المهني مفيدة في تحديد المعايير المقبولة والمقبولة
> السلوكيات المقبولة وتعزيز المعايير المهنية العالية
> يمارس. كما أنه يوفر معيارًا للتقييم الذاتي ويعمل كمقياس
> وسيلة لتحسين هوية المنظمة.

نأمل أن تتصرف مجموعة مجتمعنا وفقًا لهذه الإرشادات
المشاركون يحملون بعضهم البعض لهذه المعايير العالية. إذا كان لديك أي أسئلة
أو إذا كنت قلقًا من عدم اتباع الكود، فيرجى الاتصال بمالك المستودع.
