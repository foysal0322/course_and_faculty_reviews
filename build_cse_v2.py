import json, os

OUT = r"C:\Users\SMFoysalAhmed\Desktop\course_and_faculty_reviews\CSE"

cse327 = {
"iqn": [
("""I did both 327 and 373 under iqn sir. He gives easy qs for cse327 but hard for 373.
For 327 slide is enough for theory, for codes slides and he will give a github link, these are enough. He slightly changes but if you can understand the codes from slide and his given git repo, you can easily do well. For diagrams 1st understand the rules from slide and class, then practice some from online ( Google or YouTube). He gives easy diagrams so just knowing the rules are enough. For project you can build an app or website as you wish but you need to implement 6 design patterns in the project, sir will teach 9 or 10 design patterns in the class, from there you have to implement 6 ( minimum 1 design pattern per person from a group). He will ask individually which part you have done in the project, apart from the design patterns, you can do easy project.
Now for 373, it's quite easy upto mid bt the 2nd quiz and final will be hard. He will provide dynamic programming qs for almost half of the mark of the final. So, you need to understand dynamic programming to do well. Actually you need to give time to understand and practice this. You can follow take you forward YouTube channel for dynamic programming which is quite similar to his slide. Apart from dynamic programming, other qs are quite easy or moderate. Other qs will be either from slide ( can be changed a bit but you can solve easily if you can understand the topics) or from the book ( you don't need to do all the problems from the book, just do the marked problems).
Sir gives partial marks in both courses and he curves as well. Also he gave a lot of A (maybe 7 or 
 in our 327 bt 4 people got A in 373. So it's very much possible to do well if you put efforts but you actually need to out efforts in 373. ( I did both courses in 252)""", "great"),
("For 327 the questions are easy till mid. Only theory all from slides, just memorize that's all. Come to classes on time, don't smile/talk/use phone on class, he'll kick you out or humiliate in front of the whole class. You'll have to apply all his criteria in the project and explain the code when he asks during demo. Final is fully on code. Two huge questions. Curves 1 grade I think", "moderate"),
("327- For quiz 1 & mid, Memorize all the diagrams from slides. For quiz 2 & Final, memorize all the codes with conceptual understanding.", "moderate"),
("""Pro tip:
You will probably not understand his lectures first up. Go through the topics beforehand from YT and try to Interact with him during lecture. You will learn a lot
For exams go through the reference books along with slides. Do the exercises. Also do leetcode problems for the Finals (373)""", "moderate"),
("sir toh best sir er 327 TA Shahran Hossain o best", "outstanding"),
("""iqn gotta be the worst faculty from ece dept
00 learning
felt like i owe him money thats why he was rude to me""", "avoid"),
("fr , only he knows what he is teaching. Could not understand a single word. For learning actually worst. And also not good for grades.", "avoid"),
("Iqn drop", "avoid"),
("iqn drop", "avoid"),
("Average", "moderate"),
("If you know basic oop. You're good to go.", "great"),
("Faltu", "avoid"),
("Foul", "avoid"),
("Drop.... pura semester apake mental trauma dite dite kokhon semester sesh apni nijeo ter pabenna... project niye korbe duniyar natok... er por grade e ekta ghorardim dibe", "avoid"),
("""Probably the best in terms of providing you the actual course materials to learn software engineering.
But behavior probably the worst. I didn't even understand his lectures properly. Class e eshe nije nijei blabber kore chole jaito.""", "moderate"),
("worst", "avoid"),
("IQN sir is very strict but joto bar bolba bujhai dibe. Mid is easy Karon maximum theory r jinish e but final e design pattern thake and code gula bujhle easy e hobe tho the question was Onek boro and sheshe sir curves 10 root x.", "great"),
("drop iqn", "avoid"),
("Drop iqn", "avoid"),
("Iqn project e design pattern implement korte bolben ar tmn kono pera den na, qs are mostly from slides, ekta GitHub er link diben oita ar slide code er Jonno dekhben", "great"),
("Did IQN this time curved Onek mid ta relatively easy but final Tao easy if you understand the question but lengthy Onek", "great"),
("IQN easier for grading", "great"),
("CSE 327 IQN best", "outstanding"),
("Did 327 and 373 under IQN sir this time. Mid question easy e Ashe like class e ja poran Oitai e. Final e ekta boro question de but that is entirely class er concept er upor bujhle easily para jai. Shesh e jeye 10 root x ekta curve den. So Bhaloi experience chilo eibar", "great"),
("boi er question, halka IQ, class e attendance some low amount of problem solving ar fth er moto last moment e kahini nai", "moderate"),
("Did IQN sir this semester, mid er question shob slide theke e so Shobai e Bhalo kore, final e class concept theke den so easily para jai Jodi question bujhen. Shesh e he curves 10 root x", "great"),
("IqN never curves\u2026worst faculty with attitude", "avoid"),
("this time in our section he curved 2 grades", "great"),
("""Not bad
I did 327 under iqn sir last year. I don't know how he is now. But during our time,in exams, he gave everything from the slides. If you go through the slides, you can do well in the exams.
Theres also a group project. During the project demonstration, he asked each of us questions about our own part.
At last, he did give a good grade. He curved.""", "great"),
("He's good.. Really knowledgable and good of a man.", "great"),
("Iqn best", "outstanding"),
("""ashen bhai 327 iqn 361 ar 3255 kori msk1
phy107L slu""", "great"),
("""CSE 327 Iqn sir
CSE 331 Mua3 sir
CSE 499A B SFM1 sir""", "great"),
("Iqn if you can memorize code. Else mma1.", "great"),
("Project ta vlo korar try kren.vlo contribution rakhen...sir huge curve krbe", "great"),
("Faculty Review: IQN (CSE327) Ei sem e uni chilen new Faculty . Amr nsu journey te uni top worst Faculty er 1 jon thakbe. Unar class neyar system ta chilo emn -", "avoid"),
],
"afe": [
("\u09ae\u09a8\u09cd\u09a6\u09c7\u09b0 \u09ad\u09be\u09b2\u09cb \u0964 \u09aa\u09cd\u09b0\u099c\u09c7\u0995\u09cd\u099f \u09a8\u09bf\u09df\u09c7 \u099d\u09be\u09ae\u09c7\u09b2\u09be \u0995\u09b0\u09ac\u09c7\u0964 \u09a4\u09be\u099b\u09be\u09a1\u09bc\u09be \u09ac\u09be\u0995\u09bf\u09b8\u09ac \u0995\u09bf\u099b\u09c1 \u098f\u0995\u09a6\u09ae \u09b0\u09bf\u09b2\u09c7\u0995\u09cd\u09b8", "moderate"),
("30% is based on the project, and he is very strict about it. He doesn't really listen to students. During demonstrations he just says whatever he understands and don't let others to explain.", "harsh"),
("He teaches well his classes are short & questions are comparatively straight forward but he is a bit strict in script checking. overall if someone put effort attend class regularly can do well", "great"),
("I'd recommend not taking AFE. He is a changed person since last semester. It seems like he only comes to the class to cater students who have prior research experience or solid understanding of topics that he didn't even teach. He openly humiliates you in each project update to the point where you would want to drop the course midway. He'll give a feedback and in the next update he'll deny what he said previously. Didn't curve as well. Overall a very bad experience.", "avoid"),
("afe", "great"),
("Avoid afe clown and save your money", "avoid"),
("Afe", "great"),
("sir 4/5 ta project upate ney,project e 30% marks, quiz 3 ta nbe best 2 count krbe,quiz gula easy hoy,mid eo easy, so mid e try krben valo krar,final e code thake tai final e marks uthano tough,apni code e valo hole final o valo jbe,sir kono curve kre na, raw marks dey,ja curve krar exam er smoy e qs easy kre theory te pera deyna,1 hr clss ney,ee moddhei theory pora ses kray dey, valo mto project krle apni A/A- pate paren, just theory te halka effort die mark ta dhire raklei hlo", "great"),
("AFE unpredictable se ki cay se nijeo jane na", "moderate"),
("AFE best", "outstanding"),
("Good", "great"),
("""Afe
Sti
Acq
Rtk
Muo""", "great"),
("""Afe sir valo
Easy going ache
Project regular basis e update nei , seta time to time update dite parle valo grade pawa possible""", "great"),
("""raw marking ei A/A- possible
Curve koren naa""", "moderate"),
],
"nbm": [
("Nbm", "great"),
("327-Nbm", "great"),
("cse327-Nbm", "great"),
("327 nbm anyday", "great"),
("""327-nbm
373-ara2
445-rtk""", "great"),
("Nbm for 327 will be the best... syllabus is short and he will mainly focus on the project...", "outstanding"),
("""unique, like very unique unlike gibberish management system
Very user friendly UI
And yes, Advanced""", "moderate"),
("shikhte parba onk kisu cz nbm and sfm1 duitai top level er faculty. but grade er asha na rakhai valo.", "great"),
("""CSE327 nbm best for learning
However, try to learn at least the basics of web development and any web based backend framework in the semester break. Project ta onek beshi value dibe uni, so make it up to the mark.""", "outstanding"),
("of course. Nbm sir frontend e oto gurutto diten na. Backend, Software design, Database design, api, testing egulai mainly dekhten project er.", "great"),
("""In CSE327 no one is better than NBM. Project charai B- uthe jabe
jodi 3ta project checkpoint e ja korsen show koren, even if it doesnt work, you are bound to end with a B.
Ar jodi effort den project e, A guaranteed. Project is the main goal here.
Best faculty in ECE department""", "outstanding"),
("327 nbm sir no doubt", "outstanding"),
("amr to valo hoy nai temn, project ta onk kothin chilo, but sir curve kore huge.", "great"),
("""if u do CSE 327 under Nabeel sir (NbM), then sir will give the project. Other faculties allow doing projects of your own choice.
It is not recommended to do modified projects for cse 299. Better make something new and challenging.""", "moderate"),
("""1. Depends on faculty's choice! NBM Sir expects a framework dev. and mobile app.
2. Yeah. Full outline. which stack are you going to put. UML diagram flowchart. (according to NBM Sir, SRS,SDS needs to polish in 1st week), i don't know other faculty's criteria.
3. Yes you can. But don't tell your faculty it's my old project. just deal as new with some extend features. Don't tell these are extended features""", "moderate"),
("Just do the 327 under goat NBM and you are good to go .", "outstanding"),
("""cse327, 299 NBM
Cse373 sfm1""", "great"),
("""327-nbm or rhk1
373-NdA sfm1""", "great"),
("""CSE373 - Sfm1
CSE327 - Nbm
CSE299 - Nbm/MUO""", "great"),
("""If you want to learn:
CSE273 - mmk1
CSE327 - NbM
CSE445 - Sfm1
CSE465 - NbM""", "great"),
("\u09ad\u09be\u0987 \u09ae\u09be\u09a8\u09c1\u09b7\u09c7\u09b0 Review \u09a4\u09c7 \u0996\u09c1\u09ac \u09ac\u09c7\u09b6\u09c0 \u09ac\u09bf\u09b6\u09cd\u09ac\u09be\u09b8 \u0995\u09b0\u09bf\u09df\u09c7\u09a8 \u09a8\u09be! RRN (CSE173), NBM (CSE327), TNR (CSE299) - \u098f\u0987 \u09e9 \u099c\u09a8 \u09ab\u09cd\u09af\u09be\u0995\u09be\u09b2\u09cd\u099f\u09bf\u09b0 \u09ac\u09cd\u09af\u09be\u09aa\u09be\u09b0\u09c7 \u09ef\u09ed% \u098f\u09b0 \u09ac\u09c7\u09b6\u09c0 negative review, drop drop drop comments \u09a5\u09be\u0995\u09be\u09b0 \u09aa\u09b0\u0993 \u0995\u09cb\u09a8\u09cb \u0995\u09be\u09b0\u09a3\u09c7 \u09a4\u09be\u09a6\u09c7\u09b0 \u0995\u09cb\u09b0\u09cd\u09b8 \u0997\u09c1\u09b2\u09be \u0995\u09b0\u09be \u09b9\u09df! \u098f\u09ac\u0982 \u098f\u0987 \u09e9 \u099c\u09a8 \u0987 \u0986\u09ae\u09be\u09b0 NSU \u099c\u09c0\u09ac\u09a8\u09c7\u09b0 \u09aa\u09be\u0993\u09df\u09be \u0985\u09a8\u09cd\u09af\u09a4\u09ae \u09b8\u09c7\u09b0\u09be \u09e9 \u099c\u09a8 \u09ab\u09cd\u09af\u09be\u0995\u09be\u09b2\u09cd\u099f\u09bf!", "outstanding"),
("Cse327 & Cse499A -Nbm", "great"),
("""327 - nbm sir
331 - skh1 sir""", "great"),
("""CSE327 - NBM Sir
CSE331 - SKH1 Sir""", "great"),
("""cse327- nbm
cse331- skh1, mua3, rsf
if you need class recordings of these courses you can ask me""", "great"),
],
"mma1": [
("Mma1 besttttt", "outstanding"),
("Mma1", "great"),
("mma1 best", "outstanding"),
("327- mma1", "great"),
("choose korte dey mma1, kintu kono project guidance nai onek \u201c____ under 5\u201d minutes type er project er help. and exams onek easy ney monehobe je 115 abar dichhen", "moderate"),
("""1 demo about if you\u2019re using discord trello and if you made the sds and srs documentations
and viva where he asks if you used any doc tools and test cases and if you used gpt to code or not. gpt use korar jonne \u201capparently\u201d kauke A deynai""", "moderate"),
("MMA1 project focused. project tay uni beshi gurutto den. ar class thik moto korle quiz, mid, final e emnetei bhalo korben.", "great"),
("""MMA1 - \u0995\u09cd\u09b2\u09be\u09b8 \u09a8\u09be \u0995\u09b0\u09b2\u09c7\u0993 \u09b8\u09cd\u09af\u09be\u09b0 \u0995\u09bf\u099b\u09c1 \u09ac\u09b2\u09ac\u09c7\u09a8\u09be\u0964
\u0995\u09bf\u09a8\u09cd\u09a4\u09c1 \u0995\u09cd\u09b2\u09be\u09b8 \u0995\u09b0\u09ac\u09c7\u09a8\u0964\u09a8\u09be\u09b9\u09b2\u09c7 \u09aa\u09b8\u09cd\u09a4\u09be\u09ac\u09c7\u09a8 \u09aa\u09cd\u09b0\u09cb\u099c\u09c7\u0995\u09cd\u099f \u0995\u09b0\u09a4\u09c7\u0964
\u0986\u09b0 \u09b9\u09cd\u09af\u09be- \u09aa\u09b0\u09c0\u0995\u09cd\u09b7\u09be\u09b0 \u09b9\u09b2\u09c7 \u09ac\u09a8\u09cd\u09a7\u09c1\u09b0 \u0996\u09be\u09a4\u09be \u09a6\u09c7\u0996\u09ac\u09c7\u09a8 \u09a8\u09be\u0964\u09aa\u09cd\u09b0\u09b6\u09cd\u09a8 \u09a6\u09c7\u0996\u09a4\u09c7 \u09b8\u09c7\u09ae,\u0995\u09bf\u09a8\u09cd\u09a4\u09c1 \u0986\u09b8\u09b2\u09c7 \u09b8\u09c7\u09ae \u09b9\u09df\u09a8\u09be\u0964""", "moderate"),
("mma1 . Project er criteria alada. bhalo nh hole C grade .", "moderate"),
("""Since a lot of people are inboxing me for a review on MMA1 sir for CSE327
Here are my 2 cents:
Sir teaches extremely well. He'll go over all the slides and mention which ones are important and which ones are not. He takes 3/4 quizzes depending on the syllabus covered.""", "great"),
("undoubtedly sir bestt", "outstanding"),
("""Undoubtedly Sir Best. (2)
I learned a lot from him through his instructions & requirements.""", "outstanding"),
("Cse327 mma1 joss", "outstanding"),
("Mma1 best", "outstanding"),
("Cse327 mma1", "great"),
("""I am doing 445 and 465 simultaneously this sem and i would say if you\u2019re fortunate enough to get into in both of the sections then don\u2019t continue with the other ones. Only focus on these two.Especially 465 has a huge learning curve about deep learning and neural networks and only 4 sections are available.
In case you get only one of either 445/465 then you can take 327 and 273 alongside with them. For 327 (mma1 sir is best) and for 273 (mkn1 sir)""", "outstanding"),
("327 - mma1", "great"),
("easy korai but sir dekhai update niyo", "great"),
("Cse327 - Mma1", "great"),
],
"mrh1": [
("Mrh1", "great"),
("""Mrh1 best for learning
Question tricky kore..
Pura curve project er upore depend krbe...
Msrh rude behaviour,,
Best for learning
Question beshi dei,sesh kora jaina...curve kre na""", "great"),
("MRH1 good", "great"),
("MRH1 easy going ,kintu class miss dey onek", "moderate"),
("Sir best for grading and learning. Ja poray tai dey exam a", "outstanding"),
("""CSE327: Mrh1
CSE331: Marh
CSE499: Sfm1""", "great"),
("""327 mrh1
373 ekd
331 acq
299 nlh
eigula bade onnogula nile mere felbo""", "great"),
("""CSE373 - SFM1
CSE327 - MRH1, MMA1
EEE111 - RTK, AKAZ
POL101 - MJU""", "great"),
("""CSE273 - MKN1
CSE327 - MRH1
CSE445 - SFR1 (Without a doubt, he is the best faculty for learning ML).
CSE465 - NBM (I Heard from many people that he teaches extremely well in this course, but FYI, grading will be challenging. You must work hard to achieve a decent grade.)
I suggest taking CSE445 in the upcoming semester and then CSE465 the semester after that because the syllabus is huge, and you must allocate a lot of time for learning and practicing. Taking these two courses in the same semester can be extremely challenging.""", "great"),
("""327-mrh1
331-dmh""", "great"),
("327 MRH1", "great"),
("""327- MRH1 Sir
331- DMH Sir""", "great"),
],
"mdsh": [
("""Cse327- Mdsh
Mat361- Ads1
Phy107L- Rks""", "great"),
("Mdsh, mua3, rtk- good", "great"),
("CSE 327 - MdSH (the best)", "outstanding"),
("Cse327- Mdsh", "great"),
("""327 MdSH
331 MUA3""", "great"),
("""MdSH sir er lectures will feel boring but self study kore apnar theory clearly bujhte hbe as he mainly makes scenario based questions, project ey uni kono pera dey na ovabe and lastly he curves a lot
MUA3 sir er jnno apnar just slide valovebe A-Z pore jete hbe and also don't miss classes,sir majhemddhe lecture er mddhei bole den kn kn ques exam ey ashte pare, 331 is a very hard course so effort na dile parben na, specially in the final exam, lastly he also curves a lot.""", "great"),
("""Cse373 EKD
CSE327 MDSH
POL101 NHS1
HIS 102 MzD""", "great"),
("""Cse373- EKD
Cse327- MdSH
EEE111- Rtk
Cse299- Tns1
His102- Kfi
Pol101- Mbu""", "great"),
("Cse-327-Mdsh and Cse-331-Smh2", "great"),
("AVOID MDSH.", "avoid"),
],
"rhk1": [
("""\u2022CSE373 - EKD
\u2022CSE327- RHK1
\u2022EEE111+L- SMMI
\u2022CSE299- SFR1
\u2022HIS102- MAKS
\u2022POL101-HMB""", "great"),
("""Cse327- Rhk1
Cse331- Dmh""", "great"),
("CSE327- Rhk1 (Easy Going & Chill)", "great"),
("""CSE327 - Rhk1
CSE 331 - MUA""", "great"),
],
"rsy": [
("Rsy", "great"),
("curve koren na maam,requirements ja chai shob thaka lagbe and kicchu missing thakle mark cut korben", "moderate"),
("Mdrk best, rsy worst.iqr A", "avoid"),
("Tushar Khan iqr A paben class korlei bujhben ar rsy curve Kore na ek no o raw grade dibe.", "harsh"),
("RMZ1 VALO RSY BEST IQR SES TUI", "outstanding"),
("""CSE327=> RsY
CSE373=> STL
MAT361=> MLM
PHY107L=> RRI""", "great"),
("bro for 327, she's good i think", "great"),
("good", "great"),
("""Cse327 - RSY
Cse373 - STI
CSE331 - MAQm
CSE445 - JSA or MAQm
CSE299 - MUO or NLH""", "great"),
],
"itn": [
("""Cse327Itn project valo korte hobe. Theory quiz mid egula easy.
Sus- Easygoing bole den ki ki pora lagbe.""", "great"),
("Avoid ITN", "avoid"),
("hmmm ITN onk irresponsible ekta lok project onk pain dei naki", "harsh"),
("Grading best, Learning zero", "moderate"),
("sir joss...mid,quiz,final easy hoy...sir is very very serious about the project...1/2 grade curve koren", "great"),
],
"slb": [
("""SLB is one useless teacher i've ever seen. She doesn't know anything, talks about random "goppo" about all the websites she has visited and all other useless things. Everything she says is common knowledge.
The only line of code she has ever written, maybe in ancient time to pass a course in her easygoing public uni, without understanding anything.
Questions are easy but you wont get marks, because she didn't write what you was supposed to answer. Question korbe examer 10min agee, kichui details e likhbe na, uni janei na ashole kivabe question korte hoy, pore examer moddhe 10-20 min kivabe ki answer korba eita bole dite hoy, because no one got what she meant.
jehetu uni code kisui bujhe na: apni any project mere dite parben.""", "avoid"),
("Drop Slb", "avoid"),
("""Avoid SLB. She is the worst. Pura semester khatay D,C dhoray dibe.
kora kora kotha bolbe egule shune students ra effort dibe erporeo worst grading pabe!! (Cse 327)""", "avoid"),
],
"mmba": [
("Cse327 avoid mmba", "avoid"),
],
"auq": [
("Auq join howar pore first sem e korsilam onar kaceh 327 , project dekhe etto praise korse bolse sem ses e approach o korte oita niye , pore dekhi decurve kore F diye boseh aseh", "avoid"),
("""slide reading pore , onar 327 er slide khub e unorganized chilo
Ques easy motamuti slide thekei kore but last e grade dey na""", "harsh"),
("""Super easygoing but mid porjonto valo marks rakha lagbe. Sir 2/3 quizes count koren. Mid usually 70/75 marks e nen pore 30 te convert koren and final 50 te nisen pore etawo convert hoise. Question pattern: There will be 3 sections A,b,c or 1,2,3 types First there will be Mcqs then True/false, in both sections you Have to write justification for your answers. In the third part there will be one or two Scenario based questions. For 323 it will be a math from the slides. For 327 sir will give a scenario and based on that you have to answer and justify it briefly. (All topics will come from the slides).
Now comes the grading part, here sir can be unpredictable sometimes. The reason is until midterm he will give you a lot of marks, even if your mcq gets wrong but you wrote justification, you will end up with half marks and don\u2019t lose it. Because in Final he won\u2019t give any marks for wrong answers. So you might expect that you got less marks then what you deserved, but it Isn\u2019t actually!
Lastly, you won't find a super easygoing faculty like him. Thats all.""", "great"),
("""Also about project which i forgot to mention:
For 327: Sir will give you a list of project topics. From them you have to select one. And here joto age tmi Project topic select korba toto valo topic choose korte parba. And it will help actually. And you can use Ai agents, no such restrictions here. You have to upload weekly progress report on canvas. And Ekdom last e sir will take a Presentation on what you have built. And demo er video canvas e upload kora lagbe. Thats it.
For 323:
You have to make two servers using Virtual machines and connect with one of your group members and perform some operations all will given in the canvas. One is SSH server its mandatory and another you can choose from the list lile web server/ftp etc. Its very easy. But Don't cram in the last minutes. You are good to go.""", "moderate"),
("Auq good", "great"),
],
}

cse299 = {
"msrb": [
("Msrb good, just be regular and on time", "great"),
("Best", "outstanding"),
("299 er kono material sir provide koren nai. Shudhu ekta report sample diyechhilen. 299 er jonno Msrb sir easygoing. Project, weekly updates, code er obostha dekhe rank koren maybe. Prottek week e sir ke update dekhano laagbe, project er upore base koree task joto para jaay complete korle bhalo. R sir monehoy onek line er code dekhle mone koren je bhalomoton kaj korse student ra project e. Ekhane ekta suggestion, kono task korar time e multiple code file e na rekhe ekta ba duitay shob rakhle better. Daily progress dekhaite parle pera hobe na. Bhaloi Grade den.", "great"),
("Not good project dibe unar iccha moto topic diye topic gula jater hoileo hoito 2/1 ta Valo topic onno keu niye gele Baki ja ase ogula te kaj Korte gele baje obostha. Resume te dekhanor moto Kono kaj e korabe na guidance o nai jhimay jhimay jabe semester based on ranking ekta grade dhoray dibe better to avoid Jodi Valo kisu Korte chan r Sikhte chan jeita future e kaje lagbe", "avoid"),
("MSRb easygoing and bhaloi curve koren. Did 215 under him.", "great"),
("""Vai MSRb curve king
MSRz Good""", "great"),
("MSRb best for cse299. just be on time and present in all classes and submit reports before deadline. no pera, easygoing, good grades", "outstanding"),
],
"muo": [
("""To get an A from MUO sir, you must make sure to show the weekly updates properly.
I missed getting a good grade because I didn\u2019t submit the first two weeks updates properly.
Sir is a great teacher, a good man indeed""", "great"),
("""\u09b8\u09cd\u09af\u09be\u09b0 \u098f\u0987\u09b0\u0995\u09ae \u09aa\u09cd\u09b0\u099c\u09c7\u0995\u09cd\u099f \u098f\u0995\u09cd\u09b8\u09aa\u09c7\u0995\u09cd\u099f \u0995\u09b0\u09c7\u09a8 \u09af\u09c7\u099f\u09be \u09b8\u09cb\u09b6\u09cd\u09af\u09be\u09b2\u09bf \u0985\u09cd\u09af\u09be\u09aa\u09cd\u09b2\u09bf\u0995\u09c7\u09ac\u09b2 \u09b9\u09ac\u09c7\u0964
\u09b0\u09bf\u09df\u09c7\u09b2 \u09b2\u09be\u0987\u09ab \u09aa\u09cd\u09b0\u09ac\u09cd\u09b2\u09c7\u09ae \u09b8\u09b2\u09ad \u0995\u09b0\u09ac\u09c7 \u098f\u0987 \u099f\u09be\u0987\u09aa \u09aa\u09cd\u09b0\u099c\u09c7\u0995\u09cd\u099f \u09aa\u09cd\u09b0\u09c7\u09ab\u09be\u09b0 \u0995\u09b0\u09c7\u09a8\u0964""", "moderate"),
("""\u099c\u09cd\u09ac\u09c0, \u0987\u09a8\u09cd\u09a1\u09bf\u09ad\u09bf\u099c\u09cd\u09af\u09c1\u09df\u09be\u09b2\u09cd\u09b2\u09bf \u0995\u09b0\u09a4\u09c7 \u09aa\u09be\u09b0\u09ac\u09c7\u09a8\u0964
\u0986\u09ae\u09bf\u0993 \u09a8\u09bf\u099c\u09c7\u0993 \u098f\u0995\u09be\u0987 \u0995\u09b0\u09c7\u099b\u09bf \u09b8\u09cd\u09af\u09be\u09b0\u09c7\u09b0 \u0995\u09be\u099b\u09c7\u0964""", "moderate"),
("Muo sir onk nice!!", "great"),
("Yes, sir does allow you to do a project alone, but a simple webpage project is not enough to earn a good grade. Sir gives you full freedom to choose your project, but it should have a social impact or solve an existing problem.\nHe evaluates based on the effort you put into the project when grading.", "great"),
("Ji... Make sure to learn and update every week, take suggestions and act accordingly, sir rewards your efforts,", "great"),
("Drop Muo. Khub pera khaben and drop deyar age amake ektu boilen:)", "avoid"),
("Muo", "great"),
("easy going..weekly report gula thik moto diben..Ekta final presentation hobe\u2026Overall apni thik moto sob requirement s gula fulfil krte parle valo grade paben", "great"),
("MUO sir ai course a ektu advance project day.", "great"),
],
"itn": [
("""ITN nen sir, just course na ekta professional level er kivabe kaj korte hoy everything sir korabe how to submit weekly report jeta life and other courses e help hobe. But ektai issue sir ashe na class e late kore online kore dey, As eta just project so issue howar kotha na & sir machine learning er project k priority dey
Btw apni to amni A paben""", "great"),
("Msk1 ba itn", "great"),
("Best faculty.. Kono pera dibe na..CR hoben... Sir weekly update nibe..ki ki korsen tar expln korbe & nxt week e ki korte hobe bole dibe..project ML niye korlei A", "outstanding"),
("Itn", "great"),
("ITN to sunsi onk hard going r pera ney", "harsh"),
("""Sir actively pays attention to weekly tasks such as reports/related paper readings/testing out a model. If you\u2019re up
for weekly progress ITN is the way to go. Otherwise ekbare onekkichu kore kore project dara korano isnt sir\u2019s way.""", "great"),
("avoid itn", "avoid"),
("sir khub Valo", "great"),
("SIR shei chill Ekta manush .", "great"),
("Avoid ITN for CSE299", "avoid"),
("Machine Learning released project korte bolbe, kisu sikhte parben na unar kase,weekly update niya onek pera dey, grade late a pawar possibility onek in that case next semester CSE499 course nite parben na !", "avoid"),
],
"nlh": [
("Drop drop.", "avoid"),
("""Nlh good.
Helpful""", "great"),
("He was good", "great"),
("\u09ad\u09be\u09b2 \u09a8\u09be \u09ad\u09be\u0987\u0964", "harsh"),
("Bhai course Nile bujben...Ami unar kache 299,311 krsi...lab instructor joggon Kichu blam na ...Sathe unra exam question,porano style Kichu Valo na..ki blbe nije bujben na.... retake nite caile krte paren unra kache", "avoid"),
("""sir ponaro style, question onkk kothin krbe....apnak Valo Korte hole onkk besi pressure dite hbe ei course......marks Tula kost ache.....
Lab instructor Valo chilo na""", "avoid"),
("Nlh er kache mara khabi, eta bolte pari just", "avoid"),
],
"oisd": [
("OISD goated, not sure about 299", "great"),
("OISD best. Tmi bujhtei parbe na tmi 299 krteso....sir Ekta topic diben...oi related idea share krte hbe...then idea finalized hoile, every week update dekhaite hbe....just dekhaba ki krso....last class a final presentation....sesh", "outstanding"),
("Hae For 299 Oisd Gem", "great"),
("Oisd- sir easygoing. Project niye pera dey na. Grading fair koren. Project report r process gulo thik vabe explain korte parle vlo grade pawa jay.", "great"),
("Drop OISD or change section.", "avoid"),
("drop OISD Teaching and grading 2 tatei baje,", "avoid"),
("drop oisd.", "avoid"),
],
"sfr1": [
("""Sfr1 sir 1cr er course e 3cr course shoman pressure dbe, shikhben o onk kichu ..
Effort dile A""", "great"),
("""Sfr1:-
1) follow his instructions properly
2) regularly update throughout the whole semester
3) don't cross the deadline
That's all, you'll get a good grade""", "great"),
("Sfr1 always Best, 299 e AI chatbot \u09ac\u09be\u09a8\u09be\u09a4\u09c7 \u09a6\u09bf\u09ac\u09c7 \u0986\u09b0 \u09b8\u09cd\u09af\u09be\u09b0\u09c7\u09b0 \u0995\u09be\u099b\u09c7 \u0997\u09c7\u09b2\u09c7 \u09ad\u09be\u09b2\u09cb \u0997\u09be\u0987\u09a1\u09c7\u09a8\u09cd\u09b8 \u09aa\u09be\u09ac\u09c7\u09a8, \u0986\u09b0 \u09b8\u09cd\u09af\u09be\u09b0 \u0985\u09a8\u09c7\u0995 \u0995\u09be\u09b0\u09cd\u09ad \u0995\u09b0\u09c7\u09a8", "outstanding"),
],
"afe": [
("AFE", "great"),
],
"mdy": [
("""Mdy sir 
, no project only presentation about Quantum computing""", "moderate"),
("ektu hard and the last presentation should be creative.", "moderate"),
],
"tns1": [
("Tns1 mam best", "outstanding"),
("Faculty Review: Tns1\ncourse: CSE299\nJunior Design is the first course where we can show off our skills by designing, implementing, and building a project (web application, mobile app, ML/DL, etc.). Ma\u2019am encouraged us to propose 3 unique project ideas with real-world applications. There weren\u2019t any restrictions to languages or frameworks that we could use. Ma\u2019am gave all the proper guidelines for submitting our project proposals and\u2026", "great"),
("Cse299- Tns1", "great"),
],
"mle": [
("He used to give rag based Chatbot for the whole class. If he still does that then easyyyy", "great"),
("he teaches from the absolute beginning, answers every question. whoever said that doesn't know how to take things from him", "great"),
("heard teaching er jonno valo na", "harsh"),
],
"sns1": [
("Sns1", "great"),
("balo ank sincere thkos A pabi confirm", "great"),
],
"nva": [
("Nva", "great"),
],
"ssh1": [
("Ssh1 sure A vai", "great"),
("Ssh1 er kono review lage na", "great"),
("Ssh1 Miss onek Valo", "great"),
("Ssh1 bestt", "outstanding"),
("Ssh1 A fr", "great"),
("Pera na nite chaile & grade valo chaile go for SSH1 \u2026\u2026. But learning er jonno not recommended.", "moderate"),
("""ekta topic just ekbar bole. tarpor na bujhle, question korle rege jay. full math nije solve kore dekhay/bujhay dey na, instead students der korte dey tarpor ar sheta nije kore dey na. so jara solve korte pare na or struggle kore, tara pichay jay.
but ques easy kore, from the slides.
she wan't good for me because i don't self-study much""", "harsh"),
("SSH1: Pera kom dibe ma'am web based project kora jay. Ma'am etoh kichu complicated chay na. As if you can give a decent presentation Ma'am easily A dibe.\nRIH: Sir onek detailed report chay as final report within 3000 words korteh bole. Viva nen.", "great"),
],
"rih": [
("SSH1: Pera kom dibe ma'am web based project kora jay. Ma'am etoh kichu complicated chay na. As if you can give a decent presentation Ma'am easily A dibe.\nRIH: Sir onek detailed report chay as final report within 3000 words korteh bole. Viva nen.", "great"),
],
"azk": [
("Azk Sir", "great"),
],
"msrz": [
("MSRz sir slide thekei hubuhu question dey slide prlei enough....\nMSRb sir er kache cse115 r cse215 korechilam sir onk curve kore but cse299 niye idea nai", "great"),
],
"nbm": [
("Nbm best", "outstanding"),
],
"tnr": [
("\u09ad\u09be\u0987 \u09ae\u09be\u09a8\u09c1\u09b7\u09c7\u09b0 Review \u09a4\u09c7 \u0996\u09c1\u09ac \u09ac\u09c7\u09b6\u09c0 \u09ac\u09bf\u09b6\u09cd\u09ac\u09be\u09b8 \u0995\u09b0\u09bf\u09df\u09c7\u09a8 \u09a8\u09be! RRN (CSE173), NBM (CSE327), TNR (CSE299) - \u098f\u0987 \u09e9 \u099c\u09a8 \u09ab\u09cd\u09af\u09be\u0995\u09be\u09b2\u09cd\u099f\u09bf\u09b0 \u09ac\u09cd\u09af\u09be\u09aa\u09be\u09b0\u09c7 \u09ef\u09ed% \u098f\u09b0 \u09ac\u09c7\u09b6\u09c0 negative review, drop drop drop comments \u09a5\u09be\u0995\u09be\u09b0 \u09aa\u09b0\u0993 \u0995\u09cb\u09a8\u09cb \u0995\u09be\u09b0\u09a3\u09c7 \u09a4\u09be\u09a6\u09c7\u09b0 \u0995\u09cb\u09b0\u09cd\u09b8 \u0997\u09c1\u09b2\u09be \u0995\u09b0\u09be \u09b9\u09df! \u098f\u09ac\u0982 \u098f\u0987 \u09e9 \u099c\u09a8 \u0987 \u0986\u09ae\u09be\u09b0 NSU \u099c\u09c0\u09ac\u09a8\u09c7\u09b0 \u09aa\u09be\u0993\u09df\u09be \u0985\u09a8\u09cd\u09af\u09a4\u09ae \u09b8\u09c7\u09b0\u09be \u09e9 \u099c\u09a8 \u09ab\u09cd\u09af\u09be\u0995\u09be\u09b2\u09cd\u099f\u09bf!", "outstanding"),
],
}

def build(course_key, facs):
    out = {course_key: {}}
    for k, items in facs.items():
        seen = set()
        lst = []
        for text, rating in items:
            t = text.replace("\r\n", "\n").strip()
            if t in seen:
                continue
            seen.add(t)
            lst.append({"review": t, "rating": rating})
        out[course_key][k] = lst
    return out

for key, facs, fname in (("cse327", cse327, "cse327_llm_review_v2.json"), ("cse299", cse299, "cse299_llm_review_v2.json")):
    data = build(key, facs)
    p = os.path.join(OUT, fname)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    total = sum(len(v) for v in data[key].values())
    print(key, "faculty:", len(data[key]), "reviews:", total, "->", fname)
