# von Krogh, Roberson and Gruber (2023), Recognizing and utilizing novel research opportunities with artificial intelligence, Academy of Management Journal 66(2)

Source: `von-krogh-roberson-gruber-2023.pdf`. Text extracted by pdftotext; layout kept, page breaks marked. A quote from this file is the extraction's, so check an odd word against the page it names.

--- page 1 ---

r Academy of Management Journal
2023, Vol. 66, No. 2, 367–373.
https://doi.org/10.5465/amj.2023.4002




                                                                 FROM THE EDITORS
                           RECOGNIZING AND UTILIZING NOVEL RESEARCH
                           OPPORTUNITIES WITH ARTIFICIAL INTELLIGENCE

   As we are witnessing a fundamental transformation                                              of building machines that “mimic” human intelli-
of organizations, societies, and economies through                                                gence. Today, research focuses on exploring how
the rapid growth of data and development of digital                                               aspects of artificial intelligence work in practice. As
technology (George, Osinga, Lavie, & Scott, 2016),                                                a subset of AI, machine learning (ML) has become a
artificial intelligence (AI) has the potential to trans-                                          powerful means of discovering patterns in massive
form the management field. With the power to                                                      amounts of data and making predictions based on
automatize, provide predictions of outcomes, and                                                  such intelligence (George, Haas, & Pentland, 2014;
discover patterns in massive amounts of data (Iansiti                                             Hannah, Tidhar, & Eisenhardt, 2021). As manage-
& Lakhani, 2020), AI changes many aspects of con-                                                 ment scholars enjoy unprecedented access to numer-
temporary organizing, including decision-making,                                                  ous new data sources offering vast amounts of data,
problem-solving, and other processes (Bailey, Faraj,                                              we believe that ML may be of great value to scholars
Hinds, Leonardi, & von Krogh, 2022). AI also enables                                              across the different divisions and interest groups of
firms with capabilities for offering new products and                                             the Academy of Management. We also believe man-
services, developing new business models, and con-                                                agement research can offer important insights to the
necting stakeholders. In line with these develop-                                                 study of AI by enlarging the types and scope of data
ments, AI is not only an interesting phenomenon to                                                to which we expose ML.
study in and around organizations (e.g., Krakowski,                                                  The primary purpose of this FTE is to support scho-
Luger, & Raisch, 2022; Tang et al., 2022; Tong, Jia,                                              lars in taking advantage of research opportunities in
Luo, & Fang, 2021), but also offers management scho-                                              ML applications and to offer guidelines for work sub-
lars a wealth of research opportunities in enlarging                                              mitted to AMJ. Specifically, as ML may have broad
their methodological toolbox to leverage vast amounts                                             appeal to management scholars, we discuss the associ-
and various types of data (e.g., Choudhury, Allen, &                                              ated benefits and challenges to be considered when
Endres, 2020; Vanneste & Gulati, 2022). In our quest to                                           engaging in this type of research. We also review
push scientific boundaries, we encourage authors to                                               recent advancements in AI that may help management
explore these opportunities within Academy of Man-                                                scholars leverage the benefits of ML applications
agement Journal (AMJ).                                                                            while dealing with some of the challenges of these
   While AI is a trending and “hot” topic discussed by
                                                                                                  methods. Finally, we offer a typology for conducting
policy-makers, business leaders, and scientists, under-
                                                                                                  ML research in ways that build and test theory and
standing when and how machines display intelligent
                                                                                                  advancing an understanding of management phe-
behaviors is at the center of modern AI scholarship
                                                                                                  nomena, consistent with papers published in AMJ.
(Nilsson, 1998). AI represents a broad field of tech-
nologies that display intelligent behaviors, includ-
ing self-awareness, goal formulation, goal-directed
action, reasoning, optimization, learning, and auton-                                                              BENEFITS OF ML METHODS
omous movements. While many readers will imme-                                                       One key benefit of ML to management scholars is
diately recall the Terminator in the movie by the                                                 its statistical flexibility, or the use of algorithms to
same name, or the rogue artificial psychopath (HAL)                                               fit complex functional forms to a data set (without
in the movie 2001: A Space Odyssey, which epito-                                                  over-fitting) that can also work well out-of-sample.1
mizes the horrific efficiency of AI (Clarke, 1968/2000),
computer scientists have long abandoned the idea                                                     1
                                                                                                       While classical statistics focuses on extracting inferences
                                                                                                  for a population from a sample, ML aims at finding general-
                                                                                                  izable predictive patterns (Bzdok, Altman, & Krzywinski,
   We are very grateful for comments on earlier versions of                                       2018). This essential feature may support researchers in
this editorial from Savindu Herath, Riitta Katila, Phanish                                        scrutinizing effect sizes in very large samples (see Combs,
Puranam, and Yash Raj Shrestha. Any errors are our own.                                           2010).
                                                                                         367
Copyright of the Academy of Management, all rights reserved. Contents may not be copied, emailed, posted to a listserv, or otherwise transmitted without the copyright holder's express
written permission. Users may print, download, or email articles for individual use only.

--- page 2 ---

368                                            Academy of Management Journal                                        April

Current ML algorithms fall into three broad categories:          unsupervised learning approach or manual annotation
(1) reinforcement, (2) unsupervised, and (3) super-              of a data set may be used to train models, such anno-
vised. “Reinforcement learning” comprises algorithms             tation is prone to errors when data grow. Therefore,
that autonomously learn courses of action to reach a             access issues continue to create barriers to the use
goal within an environment. For example, such algo-              of ML methods and, therefore, to the examination of
rithms form the backbone of self-driving vehicles that           pertinent phenomena or development of relevant
adapt to traffic patterns as they seek to reach a destina-       theories.
tion, or of advanced chess programs that learn and                  Second, ML algorithms are subject to human biases
adapt based on opponents’ moves. “Unsupervised                   that can become reinforcing, as they are reproduced
learning” algorithms learn to discover patterns in               in future data sets and models. Researchers are often
input data (often called “features”) without any spe-            biased toward selecting algorithms they know rather
cified target for learning. Such algorithms do not nec-          than those needed to solve the task at hand, which can
essarily require annotated and curated data, which               produce faulty models that are fatal to accurate predic-
makes them very useful for clustering or dimension-              tions or pattern discovery. For example, research high-
ality reduction. For example, unsupervised learning              lights biases in ML-based candidate selection systems
algorithms can support a researcher in identifying               stemming from hidden biases embedded in data
groups of firms adopting related business models,                from previous candidate pools (Feuerriegel, Shrestha,
pursuing similar strategies within an industry (an               von Krogh, & Zhang, 2022). Specifically, algorithms
initial step in strategic group analysis), or offering           trained on White male candidate pools were shown to
competing digital services on a platform based on a              choose similar candidates and to discriminate against
large and complex feature set. In contrast, “supervised          female and ethnic minority candidates. There is also a
learning” algorithms, which are most common in                   potential for ML to fall prey to biases resulting from
the social sciences, learn how to map associations               data structures, as the selection of “correct” algo-
between inputs (“features” X) and outputs (“targets”             rithms depends on the available data and how they
Y). For example, ML can be used with categorical                 are handled. For example, choosing a deep learning
variables to arrange data as they relate to the target,          model over supervised learning when data are lim-
such as classifying credit card transactions as fraudu-          ited can produce faulty predictions. Biases may also
lent or non-fraudulent based on the time and fre-                derive from performance metrics to evaluate ML
quency of transactions, location, amount of payment,             models that fail to detect class imbalances and instead,
and other data. For continuous variables, supervised             show high performance of target prediction—thus,
learning algorithms learn to perform complex regres-             creating an illusion of model accuracy relative to other
sion tasks, such as predicting firm performance based            models.
on extensive firm and industry data.                                Third, researchers must consider the costs associ-
                                                                 ated with ML. In particular, massive and variegated
         CHALLENGES OF ML METHODS                                data sets often make traditional ML approaches less
                                                                 efficient and pose important constraints for research-
  Because AI and its subset of ML-based methods                  ers in understanding such data. We also often hear
involve considerable human effort and management,                scholars complaining that the intricate functioning
there are also associated ethical and technical chal-            of ML algorithms remains opaque. Of course, this
lenges when applying them. First, limited access to              perceived challenge can be addressed through educa-
certain types of data can challenge AI and ML meth-              tion and learning on how algorithms work. However,
ods. With a few exceptions, most ML algorithms                   in many cases, the amount of one’s own training, and
only work effectively with large amounts of data.                of training data needed, makes it economically ineffi-
However, management scholars must grapple with                   cient to study their detailed functioning. Thus, the
matching the data to which they have access to data              required effort to engage in ML methods presents a
models. Since many firms consider data to be a stra-             challenge to researchers who do not regularly utilize
tegic asset that must be protected through substantial           this approach.
technical and social mechanisms, the extent to                      Despite this range of challenges, recent develop-
which critical data are available may become deci-               ments in computer science can help management
sive for the type of questions that drive a research             scholars deal with issues of access, bias, and cost.
agenda. Researchers may further be constrained                   For example, to build powerful learning models,
by their ability to obtain structured or annotated               researchers may draw on data to which they have
data for training and evaluating models. While an                limited access. “Federated learning” is a technique

--- page 3 ---

2023                                          von Krogh, Roberson, and Gruber                                         369

to train models across a variety of data stored on sep-             AutoML is promising for expanding researchers’
arate servers without exchanging that data (Zhang,                  methods portfolio.
Xie, Bai, Yu, Li, & Gao, 2021), such as utilizing data
from CCTVs to monitor and predict traffic patterns                          ML STRATEGIES TO BUILD AND TEST
across several local conditions and without revealing                               THEORY IN AMJ
sensitive personal information. Similarly, “transfer                  Considering that the mission of AMJ is to publish
learning,” an ML method in which pre-trained mod-                   empirical research that tests, extends, or builds man-
els are used as starting points to model a new task                 agement theory, strategies to apply ML in manage-
(Niu, Liu, Wang, & Song, 2020), is also becoming
                                                                    ment research should consider the state of theorizing
increasingly important in industries where data pro-
                                                                    about an empirical phenomenon. Within the land-
tection is crucial, such as defense and pharmaceuti-
                                                                    scape of management and organizational research,
cals. To address biases in ML, scientists have begun
                                                                    there are four primary ML research strategies that
developing “explainable AI” that can insert explana-
                                                                    can be distinguished based on the continuity of the
tion and reasoning steps to show researchers the evo-
                                                                    phenomenon investigated and its theoretical coher-
lution of models while maintaining their predictive
                                                                    ence: (1) predictive selection, (2) predictive refine-
accuracy (e.g., Senoner, Netland, & Feuerriegel, 2022).
                                                                    ment, (3) formative discovery, and (4) reductive
Further, while these explanations often remain lim-
                                                                    discovery. Such distinctions are important given
ited to predictions for a local area of the data set,
                                                                    that ML predictions can only be built on relatively
researchers are also developing robust methods for
                                                                    stable data and should be used for the purposes of
integrating them, and, thus, making them universally
                                                                    advancing our scholarly understanding of a phenom-
applicable for the full data set (Lundberg et al., 2020).
                                                                    enon. We discuss these four research strategies in
To address learning curve challenges related to the use
                                                                    greater detail below (see also Table 1).
of ML methods, scientists have developed “AutoML”
systems, which support the choice and evaluation of
                                                                    Predictive Selection
learning models (He, Zhao, & Chu, 2021). Such sys-
tems automatically tune hyperparameters, thereby                      Management research thrives on a proliferation of
removing many otherwise complex manual tasks                        theories, methods, and data, and researchers often
that demand significant research experience. While                  formulate competing features and hypotheses to ex-
manually working through iterations in building                     plain a phenomenon. In predictive selection, data
ML models may be the best way to learn about                        about a phenomenon are continuous and therefore
the opportunities and threats in model selection,                   offer an opportunity to use ML to predict outcomes.

                                                 TABLE 1
       Machine Learning Strategies for Theoretical Contribution in the Landscape of Management and
                                         Organizational Research

                                                 Theoretical fragmentation          Theoretical coherence




                          Continuous                 Predictive selection            Predictive refinement
                          phenomena
                                                 Finding stable predictors        Refining theory by training
                                                 across alternative theories      and evaluating models on
                                                                                     new but similar data




                         Discontinuous              Formative discovery              Reductive discovery
                          phenomena
                                                Patterns in data that give rise    Patterns in data that show
                                                to novel (alternative) theory     the limit to generalizability
                                                                                        of existing theory

--- page 4 ---

370                                          Academy of Management Journal                                       April

At the same time, there is theoretical fragmentation           alone versus with public organization partners, with a
in terms of the availability of many (and maybe com-           subset of 33,130 patents resulting from private–public
peting) priors, such as candidate theories and vari-           R&D relationships. Rathje and Katila (2021) con-
ables, for explaining the phenomenon. Thus, ML can             ducted a quasi-experimental design drawing upon
be used to examine the predictive strength of these            supervised ML to build and investigate the treatment
priors (features) relative to a dependent variable (tar-       versus control groups. ML was used to perform pro-
get). For example, He, Puranam, Shrestha, and von              pensity score matching, which helped to identify
Krogh (2020) studied how open-source software pro-             balanced subsamples of patents with respect to
jects resolve collective disputes around the choice of         observed covariates. This learning model avoided
intellectual property rights. Framing their study in a         intractability associated with conventional propen-
“governance of the commons” perspective (Ostrom,               sity score-matching methods and enabled the authors
1990), the authors argued there is limited theoretical         to consider a much larger set of potentially con-
explanation of how communities resolve disputes                founding dimensions. In particular, regularization
over principles to license their open-source software.         and cross-validation made it possible to circumvent
After manually identifying 11 priors from existing             the issue of overfitting of the model to the data, and
theories and observations on structural and proces-            the ML training sample, optimization techniques,
sual features of governance disputes, they exploited           and holdout sample were used to make the most
these priors to code the entire sample of disputes             accurate predictions. Thus, this approach illustrates
(183 projects). Then, after building an ensemble of            how ML can be used to fine-tune causal inference,
ML algorithms to detect robust association between             perform sensitivity analyses, and refine measures
those independent variables and dispute resolution             with an ultimate goal of refining theory.
outcomes (resolved or non-resolved), four algorithms
were run and evaluated to achieve the best fit. The            Formative Discovery
model demonstrated that the size of the group
involved in a dispute, active efforts to add informa-             A researcher may be confronted with a discontinu-
tion in discussion, application of a choice procedure          ous phenomenon wherein the data set does not allow
(e.g., voting), and type of issue under dispute (e.g.,         for accurate predictions through ML. Additionally,
changing an existing or selecting a new license) pre-          theory about the phenomenon may be fragmented.
dicted the resolution outcome. Based on these insights,        Under these conditions, ML can support formative
the authors created a subsample of 61 cases that guar-         discovery identifying patterns in the data set useful
anteed minimum and maximum variance in obser-                  for gaining insights into the phenomenon. Specifi-
vations to “manually” build a theory of governance             cally, formative discovery is a strategy that can help
dispute resolution. Thus, this study demonstrates              scholars build unprecedented and often pre-theoretical
how ML can be useful for inductively building or               understanding of a phenomenon by revealing pat-
elaborating theory.                                            terns that may not be obvious to even the best-
                                                               trained observer. For example, drawing on a rapidly
                                                               emerging and foundational literature on the out-
Predictive Refinement
                                                               comes of diversity in organizations, Wang, Dinh,
   ML methods can aid researchers further when the             Jones, Upadhyay, and Yang (2023) studied align-
stability of the phenomenon enables prediction by              ment between firms’ diversity statements and their
ML. Predictive refinement is a viable strategy when            employees’ online rating of those firms’ diversity,
alternative theories about mechanisms explaining               equality, and inclusion (DEI) efforts. As several firms
the phenomenon have become gradually integrated,               publicly condemned racism and affirmed their stance
and the variables and measures are relatively well             on DEI following the rise of the Black Lives Matter
established. For example, Rathje and Katila (2021)             social movement and the death of many Black Ameri-
examined firms’ investment decisions and the im-               cans during the spring of 2020, the authors drew
pact on the enabling nature of technologies using a            attention to a limited scholarly understanding of the
data set comprising the full set of patents awarded to         contents of such statements and their impact on
U.S. firms between 1982 and 2022 (almost two mil-              organizational outcomes. To explore the statement–
lion patents). Predicting antecedents of relationship          outcome link, the authors first applied structural
(e.g., grants) and the effects of partner type (e.g.,          topic modeling (STM), an unsupervised ML tech-
science agencies), the authors uncovered differ-               nique, to data from open letters to stakeholders
ences across firms inventing such technologies                 across the Fortune 1000 during late May to early

--- page 5 ---

2023                                          von Krogh, Roberson, and Gruber                                        371

June 2020 to identify themes (patterns) in DEI state-            as the expertise and efforts needed at each step.
ments. After training, the learning models identified            Because such requirements are apparent in research
general DEI themes related to supporting and acknowl-            that makes predictions with supervised learning, we
edging the Black community and committing to diver-              offer an example that highlights relevant choices and
sifying the workforce, which were used in a second               outcomes involved in ML methods (Shrestha, He,
study targeting millions of data points of employees’            Puranam, & von Krogh, 2020; Shrestha, Krishna, &
DEI ratings of firms on Glassdoor.com. Through the               von Krogh, 2021). Specifically, because an ML model
performance of topic probability scores (based on                (as a specified set of computations built as ML algo-
STM) for each firm’s statement, which represent the              rithms) works through different values in the data
likelihood that a statement falls into a particular              when solving a task, we discuss the three steps in
theme, the results showed that firms that released               building a learning model: (1) data management,
public statements and referenced identity-conscious              (2) learning, and (3) evaluation.
topics received more favorable DEI ratings from their               During data management, the researcher specifies
employees. Accordingly, this study is an exemplar                the task to be completed and the relevant data sources,
of how ML can help to discover patterns in massive               and proceeds to collect and analyze the data (identify-
data sets, and thereby provide novel conceptual                  ing distributions, skewness in data, or class imbal-
insights into poorly understood phenomena.                       ance). She then divides the data into two sets—the
                                                                 “training data,” used to iteratively improve the model,
Reductive Discovery                                              and the “holdout data,” used to evaluate the predictive
                                                                 power of the model (80:20 or 70:30)—and applies
   Researchers are often challenged by a need to iden-           techniques to deal with outlier treatment and miss-
tify limitations to existing theory. Suitably, reductive         ing values. The researcher also conducts “feature
discovery strategies are useful for identifying pat-             engineering,” which specifies features in the data
terns in data that show such conceptual limits to gen-           used to build the model. Feature engineering is
eralizability. While limits to generalizability may be
                                                                 constructing, deriving, and transforming data into
revealed through replication studies, there is addi-
                                                                 variables that can be used as input features for the
tional value in using ML to examine emerging patterns
                                                                 model (Chapman, Gilmore, Chapman, Mehrubeoglu, &
in novel data sets on a discontinuous phenomenon.
                                                                 Mittelstet, 2020). For numerical data, this may
ML can reveal hitherto unknown associations across
                                                                 imply normalizing the data by features into a 0:1
features, bringing into question the applicability
                                                                 interval. Accordingly, a sound ML design relies on
of existing theoretical explanations, and offer up
                                                                 finding the right features on which to train the
novel learning opportunities. For example, Belikov,
                                                                 model and reporting on the details of this activity. It
Rzhetsky, and Evans (2022) developed a promising
                                                                 is useful to sense-test the features with the existing
approach to mitigating the challenges of generalizabil-
                                                                 literature, since the purpose of ML is to help
ity using Bayesian calculus to predict robust scientific
                                                                 researchers build and test theory.
claims based on data extracted from prior publica-
                                                                    During the learning stage, the researcher chooses a
tions and weighted by institutional, social, and scien-
                                                                 performance metric for the prediction task (e.g., log
tific factors. The authors applied ML to the case of
                                                                 loss score). Once the correct performance metrics
gene regulatory interaction studies and identified a
                                                                 have been established, ML algorithms must be cho-
set of fundamental characteristics that predict replica-
                                                                 sen to fit data type and data size, prediction accu-
bility across contexts, which have been used to guide
scholars’ choices in research topics and programs.               racy, interpretability of the model, extent of the
While our field thrives on great diversity in categories,        feature set, etc. Notably, there are many specialized
constructs, theories, methods and data compared                  ML algorithms from which to choose for classifica-
with the life sciences, this diversity is an opportunity         tion (Y is a categorical variable) or regression (Y is a
for our field, bearing in mind that ML improves task             continuous variable) tasks. Some will be familiar to
performance over time as the underlying models                   management scholars, such as linear and logistic
become exposed to increasingly diverse data.                     regression, although many useful algorithms are less
                                                                 common and demand careful examination and ex-
                                                                 planation prior to use (e.g., tree models: decision
       ML STRATEGIES TO BUILD AND TEST
                                                                 tree, random forest, gradient-boosted trees). Having
             THEORY: AN EXAMPLE
                                                                 chosen an algorithm, the researcher next selects and
   Engaging in rigorous ML research requires an under-           optimizes the model by searching for hyperpara-
standing of the requisite methodological steps as well           meters (e.g., number of trees, tree depth, batch size,

--- page 6 ---

372                                           Academy of Management Journal                                             April

learning rate), which are intended to control the               the goals they are trying to achieve. Similarly, research-
learning process. While some simple algorithms                  ers should make sure their training data sets are the
require no hyperparameters, many demand research-               best representative of the whole population. It is also
ers to carefully select such parameters (or automatize          important that we devote space (in text or in online
such selection) to achieve a good learning perfor-              appendices) to explain such choices and other aspects
mance of the model. This “tuning” is commonly done              of feature engineering in detail. It is also important for
by applying standard search techniques, such as sim-            researchers to share their code (at least during the
ple or greedy search (i.e., locally optimal choices at          review process), and we generally encourage publish-
each stage of search) to search for the best fit. Thus,         ing code on publicly accessible repositories.
the selection of ML algorithms, as well as the inclu-              Finally, authors of ML-based studies must take
sion and tuning of hyperparameters, is critically               particular care in the management of their data. In
important in applying ML.                                       addition to following ethical standards set by the
  During evaluation, the researcher examines how the            Academy of Management, scholars who apply these
chosen model performs predictions on the holdout                methods to private and publicly available individual
data relative to the set performance metrics. This step         data must safeguard data security and privacy. For
involves the analysis of model errors and aims to give          example, authors should anonymize data and develop
the researcher a sense of a model’s generalizability            a comprehensive data management plan to protect
beyond the training data. In addition, reporting the            data and avoid any breach of privacy.
outcome of the evaluation step is necessary for future
research to advance on the same or similar data sets. An                             CONCLUSION
important aspect of evaluation is also to check usability
                                                                  AI should not ossify a creative mind but instead
and deficiency of the model in a real-world context.
                                                                embolden and inspire researchers to engage with
                                                                novel and unconventional data in their area of inter-
                A CALL TO ACTION                                est. The mindset driving this engagement should be:
   With a mission of publishing empirical research              “How can these tools help me uncover what I always
that significantly advances management theory and               wanted to know, but never had the power to study?”
contributes to management practice, there are several           Once clarity exists on that question, we may ap-
considerations for authors targeting AMJ as an outlet           proach our research questions and phenomena with
for their significant value-added contributions to the          a portfolio of research strategies, including formative
field’s understanding of an issue or topic via AI and           and reductive discovery, predictive selection, and
ML. While the Journal has augmented its reviewer                predictive refinement. In doing so, we have both the
capacity and methodological expertise to handle                 opportunity and the ability to transform manage-
manuscripts with ML applications, there are a few               ment research and practice.
deliberations that will improve the likelihood that a
submission will be favorably received. Beyond being                                            Georg von Krogh
clear about why they use ML to discover patterns and                Eidgen€
                                                                          ossische Technische Hochschule Z€
                                                                                                          urich
build and test theory, researchers should focus on data                                            (ETH Zurich)
engagement, data treatment, and data management.                                                   Quinetta Roberson
   Submissions to AMJ that draw on ML methods                                                Michigan State University
should demonstrate deep understanding of and en-
gagement with the data. Researchers should take steps                                                Marc Gruber
to comprehensively familiarize themselves with the              Ecole Polytechnique Federale de Lausanne (EPFL)
data at hand and to ask what can or should be learnt
from this data. In so doing, they should pay particular
attention to feature engineering—specifying what fea-                                 REFERENCES
tures can be extracted from the raw data relevant for           Bailey, D. E., Faraj, S., Hinds, P. J., Leonardi, P. M., & von
predicting the target.                                              Krogh, G. 2022. We are all theorists of technology
   Authors drawing on AI and ML methods should                      now: A relational perspective on technology and orga-
also consider parameter choices and reflect on how                  nizing. Organization Science, 33: 1–18.
bias may influence those choices and interpretation             Belikov, A. V., Rzhetsky, A., & Evans, J. 2022. Prediction of
of their findings. For example, when choosing a                     robust scientific facts from literature. Nature Machine
model, it is imperative that researchers understand                 Intelligence, 4: 445–454.

--- page 7 ---

2023                                                von Krogh, Roberson, and Gruber                                              373

Bzdok, D., Altman, N., & Krzywinski, M. 2018. Statistics ver-          Nilsson, N. J. 1998. Artificial intelligence: A new synthe-
    sus machine learning. Nature Methods, 15: 233–234.                     sis. San Francisco, CA: Morgan Kaufmann.
Chapman, K. W., Gilmore, T. E., Chapman, C. D., Mehru-                 Niu, S., Liu, Y., Wang, J., & Song, H. 2020. A decade of sur-
   beoglu, M., & Mittelstet, A. R. 2020. Camera-based                      vey of transfer learning (2010–2020). IEEE Transac-
   water stage and discharge prediction with machine                       tions on Artificial Intelligence, 1: 151–166.
   learning. Hydrology and Earth System Sciences
   Discussion. Forthcoming.                                            Ostrom, E. 1990. Governing the commons: The evolution
                                                                           of institutions for collective action. Cambridge, U.K.:
Choudhury, P., Allen, R. T., & Endres, M. H. 2020. Machine                 Cambridge University Press.
   learning for pattern discovery in management research.
   Strategic Management Journal, 42: 30–57.                            Rathje, J. M., & Katila, R. 2021. Enabling technologies and
                                                                           the role of private firms: A machine learning matching
Clarke, A. C. 2000. 2001: A space odyssey. New York, NY:                   analysis. Strategy Science, 6: 1–109.
    ROC. (Original work published 1968)
                                                                       Senoner, K., Netland, T., & Feuerriegel, S. 2022. Using
Combs, J. G. 2010. Big samples and small effects: Let’s not
                                                                           explainable artificial intelligence to process quality:
   trade rigor and relevance for power. Academy of
                                                                           Evidence from semiconductor manufacturing. Man-
   Management Journal, 53: 9–18.
                                                                           agement Science, 68: 5704–5723.
Feuerriegel, S., Shrestha, Y. R., von Krogh, G., & Zhang, C.
    2022. Bringing artificial intelligence to business man-            Shrestha, Y. R., He, V. F., Puranam, P., & von Krogh, G.
    agement. Nature Machine Intelligence, 4: 611–613.                      2020. Algorithm supported induction for building the-
                                                                           ory: How can we use prediction models to theorize?
George, G., Haas, M., & Pentland, A. 2014. Big data and                    Organization Science, 32: 856–880.
    management. Academy of Management Journal, 57:
    321–326.                                                           Shrestha, Y. R., Krishna, V., & von Krogh, G. 2021. Aug-
                                                                           menting organizational decision-making with deep
George, G., Osinga, E. C., Lavie, D., & Scott, B. A. 2016.
                                                                           learning algorithms: Principles, promises, and chal-
    From the editors: Big data and data science methods
                                                                           lenges. Journal of Business Research, 123: 588–603.
    for management research. Academy of Management
    Journal, 59: 1493–1507.                                            Tang, P. M., Koopman, J., McClean, S. T., Zhang, J. H., Li,
Hannah, D. P., Tidhar, R., & Eisenhardt, K. M. 2021. Ana-                  C. H., De Cremer, D., Lu, Y., & Ng, C. T. S. 2022. When
   lytic models in strategy, organizations, and manage-                    conscientious employees meet intelligent machines:
   ment research: A guide for consumers. Strategic                         An integrative approach inspired by complementarity
   Management Journal, 42: 329–360.                                        theory and role theory. Academy of Management
                                                                           Journal, 65: 1019–1054.
He, V. F., Puranam, P., Shrestha, Y. R., & von Krogh, G.
    2020. Resolving governance disputes in communities:                Tong, S., Jia, N., Luo, X., & Fang, Z. 2021. The Janus face of
    A study of software license decisions. Strategic Man-                 artificial intelligence feedback: Deployment versus
    agement Journal, 41: 1837–1868.                                       disclosure effects in employee performance. Strategic
                                                                          Management Journal, 42: 1600–1631.
He, X., Zhao, K., & Chu, X. 2021. AutoML: A survey of
    the state-of-the art. Knowledge-Based Systems, 212:                Vanneste, B., & Gulati, R. 2022. Generalized trust, external
    106622.                                                               sourcing, and firm performance in economic down-
                                                                          turns. Organization Science, 33: 1599–1619.
Iansiti, M., & Lakhani, K. R. 2020. Competing in the age of
     AI: Strategy and leadership when algorithms run the               Wang, W., Dinh, J. V., Jones, K. S., Upadhyay, S., & Yang, J.
     world. Boston, MA: Harvard Business Review Press.                    2023. Corporate diversity statements and employees’
                                                                          online DEI ratings: An unsupervised machine-learning
Krakowski, S., Luger, J., & Raisch, S. 2022. Artificial intelli-          text-mining analysis. Journal of Business and Psy-
    gence and the changing sources of competitive advan-                  chology, 38: 45–61.
    tage. Strategic Management Journal. Forthcoming.
                                                                       Zhang, C., Xie, Y., Bai, H., Yu, B., Li, W., & Gao, Y. 2021. A
Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin,
                                                                          survey of federated learning. Knowledge-Based
   J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., &
                                                                          Systems.
   Lee, S.-I. 2020. From local explanations to global
   understanding with explainable AI for trees. Nature
   Machine Intelligence, 2: 56–67.
