# O'Sullivan and Ravasi (2026), Prompt-making and sensemaking: using generative artificial intelligence to interpret empirical patterns in qualitative research, Strategic Organization

Source: `o-sullivan-ravasi-2026-prompt-making-and-sensemaking-using-generative-artificial-intelligence-to-interpret-empirical.pdf`. Text extracted by pdftotext; layout kept, page breaks marked. A quote from this file is the extraction's, so check an odd word against the page it names.

--- page 1 ---

1476963
research-article2026
                       SOQ0010.1177/14761270261476963Strategic OrganizationO’Sullivan and Ravasi




                             Essay

                                                                                                                               Strategic Organization

                             Prompt-making and sensemaking:
                                                                                                                                                ﻿1­–21
                                                                                                                               © The Author(s) 2026

                             Using generative artificial                                                                       Article reuse guidelines:
                             intelligence to interpret empirical                                                   sagepub.com/journals-permissions
                                                                                                                 DOI: 10.1177/14761270261476963
                                                                                                              https://doi.org/10.1177/14761270261476963

                             patterns in qualitative research                                                         journals.sagepub.com/home/soq




                             Daniel O’Sullivan1 and Davide Ravasi1



                             Abstract
                             Debates about how generative artificial intelligence will impact the practice of qualitative methods have
                             largely focused on how generative artificial intelligence may be used to collect and analyse data, as well as
                             the ethical implications of doing so. In this article, we shift attention to a less-examined but vital aspect of
                             qualitative research: the interpretation – or theorization – of empirical patterns. We argue that generative
                             artificial intelligence’s core capabilities – autoregressive generation, self-attention, and latent knowledge
                             – make it particularly well-suited to augment qualitative theorization. Based on an understanding of
                             qualitative theorization as disciplined imagination, we elucidate how generative artificial intelligence can
                             support this process by expanding and enriching imagination and broadening and scaffolding discipline. We
                             offer practical guidance on how to prompt generative artificial intelligence to realize these benefits, while
                             also identifying potential pitfalls and how to avoid them. Ultimately, we contend that, although generative
                             artificial intelligence is no substitute for human interpretation, it represents a powerful tool for extending
                             and structuring the theorization process.


                             Keywords
                             qualitative methods, generative AI, grounded theory, sensemaking theory, case method, field research


                             Introduction
                             The rise of generative artificial intelligence (GenAI) has ignited debate among qualitative research-
                             ers about whether GenAI can assist in the analysis of raw qualitative data (i.e. coding) (Hayes,
                             2025; Kulkarni et al., 2024; Schildt, 2026; Sinha et al., 2024), how it may be used during data col-
                             lection – either as the data collector (Burleigh and Wilson, 2024; Ciechanowski et al., 2020; Susarla
                             et al., 2023), or as an informant (Aristidou and Scheuermann, 2024; Wang, 2024) – and the ethical
                             and methodological concerns these applications may raise (Davison et al., 2024; Lin and
                             Corley, 2026).

                             1
                                  UCL School of Management, London, UK

                             Corresponding author:
                             Daniel O’Sullivan, UCL School of Management, One Canada Square, London, E14 5AA, UK.
                             Email: daniel.o’sullivan.21@ucl.ac.uk

--- page 2 ---

2                                                                        Strategic Organization 00(0)

   As these debates unfold, some qualitative researchers, like us, have begun to use GenAI for
other tasks that fall instead within the remit of interpreting – or theorizing – qualitative data (see
also Sloan and Glaser, 2026), such as reworking conceptual labels, sharpening tentative interpreta-
tions of observed patterns, or considering alternative explanations. These uses have proven no less
contentious (Cornelissen, 2026; Jowsey et al., 2025), and we certainly share existing concerns
about fully delegating theorization to artificial intelligence. Based on our experiences, however, we
remain optimistic about the capacity of GenAI – if used appropriately – to assist researchers in
making sense of qualitative data.
   In this article, we propose that three core capabilities of GenAI – autoregressive generation,
self-attention, and latent knowledge – are particularly relevant to qualitative theorization. We offer
practical guidance on how to effectively prompt GenAI to augment this process, outline pitfalls
that can arise when doing so, and suggest ways to manage these risks.

Theorizing qualitative observations as disciplined imagination
The theorization of qualitative observations may be generally conceived as an act of sensemaking:
attempting to offer an explanation for empirical observations (Rouse et al., 2025). While it is not
uncommon for this process to be triggered by a single puzzling or otherwise noteworthy observa-
tion (Bamberger, 2019; Sætre and Van De Ven, 2021), robust theorizations tend to be grounded in
multiple observations, the mutual relevance of which takes the form of ostensible similarities, dif-
ferences, co-occurrences, themes, sequences, cycles, and so on – which we refer to as empirical
patterns. These patterns are as constructed as they are uncovered, in that they reflect more or less
conscious choices to “extract” cues from a multitude of empirical data, and to relate them in ways
that support possible interpretations of the observed reality (Weick, 1995). These choices are
shaped by researchers’ aims and predispositions and are subject to change as their understandings
of their data evolve (Charmaz, 2006; Strauss and Corbin, 1998).
   The acts of noticing and bracketing cues and elaborating and interpreting empirical patterns
have been widely studied in qualitative methodological literature (e.g. Grodal et al., 2021; Locke
et al., 2022; Strauss and Corbin, 1998). Empirical patterns, however, are not, in themselves, theo-
ries (Sutton and Staw, 1995): theorization requires offering an explanation that gives meaning to
empirical patterns by structuring them in a sensible and internally consistent manner and by linking
them to broader theoretical frameworks.
   This conceptualization of theorization is not limited to the propositional style of theorizing
(Cornelissen, 2017) associated with grounded theory (Glaser and Strauss, 1967) or case study
research (Eisenhardt, 1989; Yin, 2009). Process theorizing is also based on the attribution of
sequential, consequential, or contingent relations among empirical observations, so that a seem-
ingly unrelated set of actions and events is “emplotted” into a meaningful storyline or presented as
manifestations of generative mechanisms that drive a process (Cloutier and Langley, 2020; Langley,
1999). When adopting a typological style, establishing empirical similarities and differences along
common analytical categories is essential to the construction of types, and co-occurrences of fea-
tures, outcomes, and/or contextual conditions help develop possible explanations for – or conse-
quences of – typological variation (Furnari et al., 2021). Common to these different approaches is
the effort to move beyond empirical patterns to offer a more general, theoretical explanation.
   We should note that theorization and the construction of a “theoretical contribution” (Whetten,
1989) are interconnected but distinct processes. Contributing to theory requires both a deep under-
standing of and sensitivity to an ongoing scholarly conversation (Huff, 1998) and the advancement
of justificatory accounts that convince others that a piece of research substantively advances this
conversation (Locke and Golden-Biddle, 1997). Such accounts typically appeal to the novelty and

--- page 3 ---

O’Sullivan and Ravasi                                                                                            3




Figure 1. Qualitative theorization as disciplined imagination.


importance of the research (Corley and Gioia, 2011; Whetten, 1989) and are subsequently vali-
dated through social processes (such as peer review) within a scholarly community (Astley, 1985).
While producing tentative explanations is a necessary precursor to advancing a theoretical contri-
bution, the focus of this article is to articulate how GenAI may augment the generation of explana-
tions, rather than the crafting of contributions.
   The process of moving from observation to explanation is often underemphasized in methodo-
logical texts and yet, we argue, is especially amenable to augmentation by GenAI. To prepare the
ground for our discussion of how this can be accomplished, in the remainder of this section, we
offer a conceptualization of this process (depicted in Figure 1) grounded in Weick’s (1989) view of
theory construction as “disciplined imagination” as it applies to the case of working with qualita-
tive data. From this perspective, theorization is conceptualized as an evolutionary process, whereby
researchers generate variation in potential explanations for an empirical observation (imagination)
and establish means of selecting among them (discipline), before retaining the explanation that
they believe outcompetes the others.

Imagination
Weick (2006) describes a researcher’s imagination as their “ability to conceive of something, seen
only fragmentarily or superficially, as a complete, perfected, and integral whole” (p. 447). As an
inferential act, imagination may be understood as the generation of conjectures – or “thought tri-
als” (Weick, 1989) – to offer a coherent and complete theoretical account for a noticed empirical
pattern (represented in Figure 1 as numerous beams of light), through a persistent asking of
“Why?,” “What if  ?”, and “So what?” (Gabriel, 2015). Imagination corresponds, therefore, to the
mode of logical reasoning that philosopher of science Charles Peirce termed “abduction,” which
involves inferring plausible explanations for specific, and often surprising, observations (Pierce,
1934).1
   In qualitative theorizing, this imaginative process is widely regarded as a key element of the
“conceptual leap,” defined as the act of:

   moving from the mass of words and other data (the world of the field), through and beyond the mechanics of
   analysis to an abstract and explicit set of concepts, relations and explanations that have meaning and relevance
   beyond the specific context of their development (the world of ideas). (Klag and Langley, 2013: 150)

   According to Weick (1989), the quality of the outcome of this imaginative leap depends on the
capacity to generate multiple and diverse possible explanations for a given pattern, such that

--- page 4 ---

4                                                                          Strategic Organization 00(0)

theorists are more likely to arrive at compelling eventual theorizations the greater the number and
the heterogeneity of thought trials they imagine.

Discipline
Discipline may, in contrast, be understood as the application of “selection criteria” – rules of judge-
ment that guide the provisional retention or discarding of conjectures (represented in Figure 1 as
discs with slits that light may pass through if it satisfies the criteria). Sensemaking is ultimately an
act of reducing equivocality – that is, the condition in which an observation may be explained in
multiple possible ways such that its meaning remains unclear. Imagination alone, however, is
likely to increase equivocality rather than reduce it. Scrutinizing conjectures against selection cri-
teria is thus necessary to narrow down the several ways in which an observation can be explained.
    In qualitative theorization, the most foundational selection criterion is empirical “plausibility”
(Weick, 1989) – that is, that there are no inconsistencies between the available data and the tenta-
tive explanation that could not be resolved through elaboration of the explanation to account for
contextual conditions or empirical contingencies (Howard-Grenville et al., 2021). In this respect,
additional data collection can alert about the weakness of an early conjecture and may also be
conducted with the explicit purpose of “testing” provisional interpretations (Glaser and Strauss,
1967) or ruling out competing explanations (Harley and Cornelissen, 2022).
    A closely related and equally foundational criterion is methodological plausibility, or “theory-
method fit” (Gehman et al., 2018). While empirical plausibility (what may be called “theory-data
fit”) concerns whether a theoretical claim accurately represents empirical observations, theory-
method fit concerns whether such claims are credibly supported by the study’s research design.
Conjectures concerning longitudinal processes, for instance, are unlikely to satisfy this criterion if
they are supported solely by thematic analysis of cross-sectional interview data conducted at a set
point in time.
    Correspondence with empirical observations and methodological choices, however, are neces-
sary but often insufficient criteria to select among conjectures. Additional selection criteria may
include that a conjecture be interesting (Davis, 1971), parsimonious (Bacharach, 1989), transfera-
ble (Lincoln and Guba, 1985), useful (Corley and Gioia, 2011), relevant to a scholarly audience
(Huff, 1998), and so on. Table 1 describes a number of selection criteria common in qualitative
research and outlines how they informed the prompting procedures we describe below. It is none-
theless the researcher’s role to specify appropriate criteria that fit their specific aims. They are
more likely to arrive at a compelling theorization the greater the number and diversity of selection
criteria they impose, and the more consistently and strictly they apply selection criteria across
thought trials (Weick, 1989).
    Finally, it should be noted that arriving at one or more tentative explanations that satisfy speci-
fied selection criteria does not mean that theorization has concluded. Nor is it the case that qualita-
tive theorization is a linear process of observing–imagining–disciplining–retaining. Rather, the
process is recursive and iterative; at any stage, the researcher may revise their interpretation of
what they observed empirically, may generate new thought trials, or devise new selection criteria.
Based on the tentative explanations they form, they may also collect new data, which will impact
their understanding of observations, or produce new ones, which will induce another loop through
the process of theorization (see Figure 1). Theorization ends and retention occurs, then, only at the
point where the researcher ceases to work on their project – often at, but perhaps even beyond, the
point of publication.

--- page 5 ---

Table 1. Common selection criteria used to assess conjectures in qualitative research.

Criteria                    Description                                             Illustrative research     Manifestation in running example with GenAI
Empirical plausibility      The conjecture convincingly accounts for – in that                            We recommend assessing theory-data fit
                                                                                    Howard-Grenville et al.
                                                                                                                                                              O’Sullivan and Ravasi




 (Theory-data fit)           it can reasonably be supported by – the empirical       (2021)                manually to avoid inputting raw data into
                             material generated during the course of the study.                            GenAI.
Methodological              The conjecture is compatible with – in that it could Gehman et al. (2018)     “The conjecture could plausibly be inferred
 plausibility (Theory-       reasonably have emerged from – the research                                   from cross-sectional data from semi-
 methods fit)                design, analytic approach, and epistemological                                structured interviews with platform
                             assumptions on which the study is built.                                      workers.”
Explanatory plausibility    The conjecture is logical, coherent, makes sense, andWeick (1989)             “The conjecture adheres to general
                             appears at face value to represent an explanation.                            plausibility and logical coherence.”
Internal coherence          The elements constituting this conjecture do not     Bacharach (1989);        “The conjecture does not rely on structural
                             contradict or undermine other elements of the         Howard-Grenville        differences (given that all workers face the
                             broader theoretical model (where a model can be       et al. (2021)           same platform structure despite variance in
                             understood as a set of conjectures).                                          their experiences).”
Theoretical embedding       The conjecture appropriately engages relevant        Huff (1998)              “The conjecture draws upon well-established
                             existing theoretical material and is relevant to an                           Management and Organization theory,
                             ongoing scholarly conversation.                                               without being rendered entirely obvious
                                                                                                           by it.”
Parsimony                   The conjecture meaningfully explains the empirical   Bacharach (1989);        “The conjecture can account for both paths
                             pattern using the minimum conceptual complexity       Whetten (1989)          using the same underlying process or
                             necessary.                                                                    mechanism(s) in a parsimonious manner.”
Transferability             The conjecture appears capable of explaining similar Lincoln and Guba (1985) “The conjecture could plausibly transfer
                             phenomena outside the immediate empirical setting                             (or analytically generalize) to other work
                             and thus has broader analytic relevance beyond this                           contexts outside of platform-based work.”
                             setting.
Potential for theoretical   The conjecture offers original theoretical insights  Corley and Gioia (2011); We recommend assessing potential for
 contribution                and meaningfully advances existing conceptual         Kilduff and O’Sullivan  theoretical contribution manually, given typical
                             understanding within a scholarly community.           (2026); Whetten         limitations in GenAI’s latent knowledge.
                                                                                   (1989)
                                                                                                                                                              5

--- page 6 ---

6                                                                           Strategic Organization 00(0)

Core capabilities of GenAI for qualitative theorization
To appreciate how GenAI may augment these aspects of qualitative theorization, it is first neces-
sary to understand its core capabilities, which we summarize as latent knowledge, autoregressive
generation, and self-attention.2 Together, these capabilities allow GenAI to respond to prompts in
a way that is fluent (via autoregressive generation), structured, and sensitive to the context of the
interaction (via self-attention), and ostensibly informed by a vast, preexisting store of information
(via latent knowledge). We elaborate briefly on these core capabilities below.

Latent knowledge
This capability stems from the training of GenAI models, during which they are exposed to mas-
sive volumes of textual data. Based on these corpora of text, models adjust their internal parame-
ters – numerical values that determine how they transform textual input into output – to optimize
their ability to predict the next word in a sequence (Bommasani et al., 2022). These parameters,
which often number in the billions, encode a web of statistical regularities learned from co-occur-
rences in the training data.
   During training, a fixed structure of parameters emerges that effectively represents the “brain”
of the GenAI model: a high-dimensional representation space in which words, phrases, and con-
cepts are positioned relative to one another according to their learned associations. Knowledge, in
this sense, is thus latent in the model. This means that the model does not “remember” or “look up”
facts; the texts it was trained on are effectively discarded after training. What remains is the statisti-
cal imprint of the patterns in those texts. Thus, while the model actually constructs responses
spontaneously, its outputs give the impression of having drawn upon a vast, preexisting store of
knowledge (Petroni et al., 2019).


Autoregressive generation
Autoregressive generation is the core mechanism through which GenAI models produce language
outputs in response to a given input (Murphy, 2023; Radford et al., 2018). Put simply, this process
refers to the statistical generation of the next word, or “token,” in a sequence based on those that
precede it. When a user inputs an initial prompt (e.g. “Are you human?”), the model first decom-
poses it into discrete tokens (e.g. “Are”, “you”, and “human?”). In processing these tokens – and
drawing upon its latent knowledge – the model then probabilistically generates the most likely next
token (e.g. “Yes”) and appends this onto the inputted sequence. It then reprocesses this longer
sequence to generate an additional token (e.g. “I”), and continues iteratively (e.g. “am”), producing
a full output (“Yes, I am”). The model does not plan an entire response in advance, but generates
one token at a time, with each prediction conditioned on what has come before. Through autore-
gressive generation, GenAI models thus transform their latent knowledge into coherent, fluent
responses to a given prompt.


Self-attention
Self-attention is the mechanism that allows GenAI models to interpret the contextual relationships
between tokens in a sequence (Vaswani et al., 2017). Through self-attention, the model calculates
how strongly each token relates to others to determine which parts of the input are most relevant
for interpreting any given word. For example, in the prompt, “Although the manager praised the
employee, she remained uncertain,” the model uses self-attention to infer whether the token “she”

--- page 7 ---

O’Sullivan and Ravasi                                                                                7




Figure 2. How GenAI augments qualitative theorization.


is more likely to refer to “manager” or “employee,” by identifying earlier tokens that carry the most
weight in shaping the sentence’s meaning. This relational information is incorporated during
autoregressive generation, so that each predicted token reflects contextual interdependencies
between tokens. In this way, self-attention enables the model to interpret the meaning of a prompt
as it unfolds and to generate responses that are coherent and sensitive to this context.

Leveraging GenAI capabilities to augment qualitative theorization
The abovementioned capabilities, we argue, enable GenAI to meaningfully augment qualitative
theorization by expanding and enriching imagination, and by scaffolding and broadening disci-
pline (see Figure 2).
   In this section, we illustrate our arguments using a fictitious study of freelancers on labour plat-
forms as a running example inspired by how we have used GenAI in our own research. The pattern
we want to theorize is the following: some informants describe choosing to offer services that they
are passionate about, while others describe choosing to offer services that align with their existing
skills or are in demand on the platform. The former often describe feeling more pressured and more
constrained than those who offer services based on their skills and demand. To help us attempt to
explain this observation, we entered a summary of this pattern into ChatGPT 5.23 alongside a num-
ber of prompts (described in the leftmost column of Table 2). See our Online Appendix for com-
plete examples of the prompts we used and responses they generated across a range of modes of
theorizing.


Expanding imagination
GenAI appears particularly adept at expanding imagination by increasing the number and hetero-
geneity of thought trials generated, which – a sensemaking perspective on theorizing contends –
increases the likelihood of eventually producing high-quality theory (Weick, 1989). By inputting a
summary of a noticed empirical pattern and prompting GenAI to offer explanations, autoregressive

--- page 8 ---

8
Table 2. Example of how prompting may vary across different modes of theorizing.
Variance theorizing                                           Process theorizing                                         Typological theorizing

Example Empirical Pattern
“I am a researcher in the field of Organization and           “I am a researcher in the field of Organization and        “I am a researcher in the field of Organization and Management Studies,
   Management Studies, conducting a qualitative study            Management Studies, conducting a qualitative study         conducting a qualitative study of how freelancers using online labour
   of how freelancers using online labour platforms              of how freelancers using online labour platforms           platforms experience autonomy at work. In reviewing interview data, I have
   experience autonomy at work. In reviewing interview           experience autonomy at work. In reviewing                  noticed three clusters, or configurational patterns, in how freelancers perform
   transcripts, I have noticed a pattern in how freelancers      longitudinal interview and observational data, I have      platform work:
   describe their work experiences in relation to the            noticed a three-phase pattern in how freelancers
                                                                                                                         Cluster 1: (1) Workers describe platforms as offering opportunities and
   kinds of services they provide:                               describe the evolution of their autonomy over time.
Some informants describe choosing to offer services           Most informants describe experiencing substantial            flexibility. (2) Workers select projects based on interest or enjoyment.
   that they are passionate about, whilst others describe        autonomy in the early days as platform workers,           (3) Workers emphasize ongoing relationships with clients. (4) Workers
   choosing to offer services primarily because they             emphasizing their freedom to choose when they             describe themselves as independent contractors. (5) Workers describe having
   align with their existing skills or because there is          work and which gigs they take on. Over time,              discretion over how they perform their work.
   demand for them on the platform. Informants who               however, they begin to describe experiencing notably    Cluster 2: (1) Workers frequently refer to platform rules and metrics. (2)
   describe offering services they are passionate about          little autonomy, reporting pressure to remain             Workers describe their work using terms associated with traditional
   often describe external pressures and feelings of             constantly available, take on undesirable work, and       employment. (3) Workers feel the need to maintain high ratings. (4) Workers
   constraint. They describe a lack of autonomy in their         maintain high ratings on the platform. As more time       describe feeling constrained by platform mechanisms. (5) Workers describe
   work, despite recognizing their freedom to choose the         passes, they begin to describe a moderate degree of       accepting most projects available to them.
   services they offer. Informants who describe offering         autonomy, which they describe as similar to a regular   Cluster 3: (1) Workers rarely express strong opinions about platforms. (2)
   services based on existing skills or market demand, in        job, where they have a balance of things they have        Workers emphasize efficiency and minimizing time spent on tasks. (3)
   contrast, often describe their work as flexible and high      discretion over and limitations.                          Workers prioritize projects based on how much they pay. (4) Workers
   in autonomy.                                               This temporal progression appeared across interviews         describe platform work as a supplemental income source. (5) Workers
These differences appear across interviews with workers          with workers using the same platforms, who thus           describe a lack of commitment towards platform work.
   using the same platform, who thus face similar formal         face similar formal work conditions.”                   These clusters of empirical material appeared across interviews with workers
   work conditions.”                                                                                                       using the same platforms, who thus face similar formal work conditions.”
Expanding Imagination
“[Statement of empirical pattern]. How might this             “[Statement of noticed empirical pattern]. How might       “[Statement of noticed empirical pattern]. How might this pattern be explained,
  pattern be explained, theoretically? Please produce as        this pattern be explained, theoretically? Please           theoretically? Please produce as many typological conjectures as you can.
  many possible explanations of this empirical pattern as       produce as many possible explanations of this            Each separate conjecture should propose a set of conceptual labels for the
  you can.”                                                     empirical pattern as you can.”                             clusters which position them as distinct types and specify the underlying
                                                                                                                           dimension(s) or organizing principle(s) along which these types are
                                                                                                                           differentiated.”
                                                                                                                                                                                                   (continued)
                                                                                                                                                                                                                 Strategic Organization 00(0)

--- page 9 ---

Table 2. (continued)

Variance theorizing                                           Process theorizing                                          Typological theorizing

Enriching Imagination
“[Specification of empirical pattern and conjectures].       “[Specification of empirical pattern and conjectures].      “[Specification of empirical pattern and conjectures]. Expand upon these
  Expand upon these potential explanations in as               Expand upon these potential explanations in as much         typological conjectures in as much detail as possible – specifying the
  much detail as possible, specifying mechanisms and           detail as possible – specifying phases, transitions,        conceptual meaning of each type and suggesting additional empirical material
  relationships between concepts.                              underlying drivers of change, and, where possible,          that would plausibly co-occur within each type given its conceptual labelling,
                                                                                                                                                                                                                O’Sullivan and Ravasi




Where possible, make reference to existing Management          turning points or “triggers” of change – to produce         as well as providing more detail about the underlying dimensions and
  and Organization theories – and, when you do so, offer       process accounts for the three-phase pattern described.     organizing principles, and explicitly positioning each type along these specified
  a brief description of the theoretical ideas you are       Where possible, make reference to existing                    dimensions.
  drawing upon.”                                               Management and Organization theories – and, when          Where possible, make reference to existing Management and Organization
                                                               you do so, offer a brief description of the theoretical     theories – and, when you do so, offer a brief description of the theoretical
                                                               ideas you are drawing upon.”                                ideas you are drawing upon.”
Broadening Discipline
“Across the possible explanations described above,           “Across the possible explanations described above,          “Across the typological conjectures identified above, identify only the
  identify only the conjecture that most fails to satisfy,     identify only the conjecture that most fails to satisfy,    conjecture that most fails to satisfy, or strains against, the following criteria.
  or strains against, the following criteria. Explain          or strains against, the following criteria. Explain         Explain your reasoning in detail and also conclude with a brief critique of your
  your reasoning in detail and also conclude with a            your reasoning in detail and also conclude with a           position. These criteria (in no particular order) are that the conjecture in
  brief critique of your position. These criteria (in no       brief critique of your position. These criteria (in no      question:
  particular order) are that the explanation in question:      particular order) are that the explanation in question:
                                                                                                                         (1) Could plausibly be inferred from cross-sectional data from semi-structured
(1) Could plausibly be inferred from cross-sectional data (1) Could plausibly be inferred from longitudinal semi-              interviews with platform workers.
      from semi-structured interviews with platform                structured interviews with platform workers.          (2) Identifies dimensions or organizing principles that meaningfully differentiate
      workers.                                               (2) Identifies an underlying driver that similarly explains       the articulated “types” (whether linearly or categorically).
(2) Does not rely primarily on structural differences              transitions between each distinct phase.              (3) Maintain internal coherence within, and distinctiveness between, the “types”
      (given that all workers face the same platform         (3) Can be reconciled with the empirical observation              articulated.
      structure despite variance in their experiences).            that this trajectory occurs for workers who began (4) Does not rely primarily on structural differences (given that all workers face
(3) Can account for both paths using the same underlying           using platforms at different historical moments.            the same platform structure despite describing different experiences).
      process or mechanism(s) in a parsimonious manner. (4) Adheres to general plausibility and logical coherence. (5) Adheres to general plausibility and logical coherence.
(4) Adheres to general plausibility and logical coherence. (5) Draws upon well-established Management and                (6) Draws upon well-established Management and Organization theory, without
(5) Draws upon well-established Management and                     Organization theory, without being rendered                 being rendered entirely obvious by it.
      Organization theory, without being rendered                  entirely obvious by it.                               (7) Could plausibly transfer (or analytically generalize) to other work contexts
      entirely obvious by it.                                (6) Could plausibly transfer (or analytically generalize)         outside of platform-based work.”
(6) Could plausibly transfer (or analytically generalize) to       to other work contexts outside of platform-based
      other work contexts outside of platform-based work.”         work.”
Scaffolding Discipline
“For each of the same possible explanations, make the        “For each of the same possible explanations, make the       “For each of the same typological conjectures, make the strongest case possible
  strongest case possible (one for each conjecture) that       strongest case possible (one for each conjecture) that      (one for each conjecture) that it satisfies each of the previously specified
  it satisfies each of the previously specified criteria.      it satisfies each of the previously specified criteria.     criteria. Then, argue the opposite: make the strongest case possible or how
  Then, argue the opposite: make the strongest case            Then, argue the opposite: make the strongest case           each conjecture fails to satisfy each of these previously specified criteria.”
  possible for how each conjecture fails to satisfy each of    possible for how each conjecture fails to satisfy each
  these previously specified criteria.”                        of these previously specified criteria.”
                                                                                                                                                                                                                9

--- page 10 ---

10                                                                       Strategic Organization 00(0)

generation becomes homologous to the imaginative process of articulating possible ways of mak-
ing sense of an observation.
   Due to autoregressive generation, GenAI can articulate conjectured explanations at a pace that
far exceeds that of human thought (visualized as a greater number of beams of light in Figure 2). It
may be objected that, because autoregressive generation is probabilistic, not all of the text it pro-
duces will constitute appropriate or coherent conjectures. However, even such outputs may prove
productive for imagination, insofar as they can serve as unexpected stimuli that prompt researchers
to generate or elaborate alternative conjectures themselves.
   GenAI’s autoregressive generation also facilitates the production of more heterogeneous con-
jectures – that is, conjectures that differ more substantially in their underlying content or emphasis
(visualized as greater distance between beams of light in Figure 2). It does so by avoiding the
human tendency to anchor the imaginative process on the first few conjectures generated, which
often become reference points during the generation of further conjectures (Tversky and Kahneman,
1974). Although autoregression is path-dependent at the level of individual tokens, GenAI does not
develop commitment to particular conjectures and can readily articulate multiple, even mutually
incompatible, explanations in sequence. As Weick (1989) observed, “any device that short-circuits
memory, foresight, or preference in the generation of thought trials increases [their heterogeneity]”
(p. 522). While unforeseeable at the time of his writing, GenAI now appears to offer a compara-
tively simple means of achieving this otherwise difficult aim without recourse to the complex
procedures Weick proposed.
   Importantly, while in this case the initial generation of conjectures is performed by GenAI,
researchers remain fully responsible for scrutinizing, adjusting, and elaborating generated conjec-
tures into coherent theoretical accounts. The use of GenAI to expand imagination does not remove
the need for judgement but rather shifts researchers’ effort from generating explanations to evaluat-
ing and developing them. Moreover, there is no guarantee that thought trials generated autoregres-
sively correspond closely to the underlying data. From a sensemaking perspective on theorization,
however, this does not constitute a problem in itself: thought trials are conjectural, and their rele-
vancy and adequacy are established only through subsequent disciplinary scrutiny.
   In its simplest form, prompting GenAI to expand imagination involves entering a summary of
an empirical observation (rather than raw data itself – for reasons we elaborate later) and request-
ing possible explanations. Researchers may request a specific number of conjectures, or prompt
GenAI to produce as many as possible. In our running example, we prompted GenAI with contex-
tual information about our study and disciplinary background, a summary of the focal empirical
observation, and a request to produce as many potential theoretical explanations as possible (see
Table 2).
   In response to this relatively simple prompt, GenAI generated 15 distinct conjectures, which
varied in their underlying assumptions and emphases. One, for instance, proposed that workers
who offer services they are passionate about, because they care about their work, may self-impose
greater demands on themselves, spurring an intensification of their work that they eventually
reflect upon as evidence of a lack of autonomy. Another proposed that those who pursue passion
may hold higher initial expectations for autonomy and thus experience greater disappointment in
the face of platform constraints, leading them to pay more attention to constraints and feel less
autonomous as a result. Other conjectures were of a similar quality, and many we would not have
thought of on our own. While not perfect, these conjectures, together, covered significant concep-
tual ground, and were useful starting points for further elaboration and eventual scrutiny against
selection criteria.
   Moving beyond this example, several additional prompting strategies may help expand imagi-
nation. For instance, because autoregressive generation is probabilistic, GenAI may offer different

--- page 11 ---

O’Sullivan and Ravasi                                                                              11

responses to the same prompt when entered repeatedly; accordingly, simply entering the same
prompt multiple times constitutes a low-effort strategy for increasing the number of conjectures
generated. To increase the heterogeneity of conjectures, researchers may also specifically request
explanations that are counterintuitive, rely on theoretical arguments that are niche or used outside
of their field (e.g. organization and management theorists requesting explanations that draw meta-
phorically on computer science or biological theories), or that rely on fundamentally different
underlying mechanisms. One strategy we found particularly effective in our own research is
prompting GenAI to produce pairs of explanations for an observation that are maximally different
from one another (or even opposites) and repeating this process iteratively.

Enriching imagination
GenAI may also enrich imagination by increasing the detail and resolution (i.e. conceptual speci-
ficity) of generated thought trials (visualized in Figure 2 by increasing the boldness and sharpness
of the beams of light). It does so primarily through its capabilities of autoregressive generation and
latent knowledge. Autoregression enables the elaboration of conjectures that have already been
generated; latent knowledge enables the embedding of these elaborations in a wide range of exist-
ing organizational theory and general contextual knowledge.
    As a result, GenAI may generate conjectures that are more detailed and internally specified than
those researchers might otherwise articulate on their own. More importantly, it can be used to sub-
stantiate existing conjectures or to expose researchers to theoretical concepts or empirical exam-
ples that aid them in doing so themselves. In qualitative theorization, imaginative insights often
emerge as nebulous and underdeveloped “seeds” of conjectures. Simply typing these proto-conjec-
tures into GenAI’s chat interface and prompting GenAI to work them into more coherent accounts
can help develop a thought trial that would otherwise have been prematurely abandoned.
    Researchers may also prompt GenAI to enrich imagination by entering existing conjectures
generated during earlier stages aimed at expanding imagination and requesting that GenAI elabo-
rate upon them or suggest relevant theoretical ideas that may substantiate these conjectures. In our
running example, we combined these approaches. After streamlining and reinterpreting the 15
conjectures generated in the previous step, which produced 6 of particular interest, we prompted
GenAI to elaborate upon each of them in as much detail as possible and explicitly requested that it
draw on relevant management and organization theories in doing so (see Table 2). As a general
practice, we find it useful to ask GenAI to provide brief descriptions of any theoretical ideas it
invokes, which can then be cross-referenced against researchers’ own understanding or subsequent
independent engagement with the literature, to assess the accuracy of these references to extant
theory.
    In response to our prompt, GenAI elaborated each conjecture into a more fully specified set of
potential explanations, often articulating a core argument, outlining potential underlying mecha-
nisms, identifying specific constructs, proposing relationships between them, and even suggesting
the kinds of empirical observations that might be consistent with the conjecture. For instance, in
elaborating the conjecture that digital freelancers may self-impose constraints when offering ser-
vices that they are passionate about, GenAI suggested – among other potential mechanisms – that
heightened care for one’s work could necessitate greater emotional labour (Hochschild, 1983),
leading to exhaustion and, in turn, diminished perceptions of autonomy. Other elaborations referred
to theories of normative control (Alvesson and Willmott, 2002; Kunda, 1992), self-verification
(Swann, 1983), and psychological ownership (Pierce et al., 2001), among others. The purpose of
these elaborations is not to provide “better” or even more accurate conjectures, but to provide
richer and more articulated starting points for subsequent disciplinary scrutiny.

--- page 12 ---

12                                                                           Strategic Organization 00(0)

Broadening discipline
GenAI may also broaden discipline by facilitating the use of a greater number and diversity of
selection criteria simultaneously (visualized in Figure 2 as a greater number of slitted discs through
which beams of light have to pass). It does so primarily through its capability of self-attention,
which enables autoregressively generated text to remain responsive to multiple conditions speci-
fied in inputted prompts. As such, researchers may explicitly prompt GenAI to fulfil specific crite-
ria as it generates conjectures, or to assess already-generated conjectures against these criteria.
Critically, this allows multiple, potentially competing selection criteria to be applied in parallel,
rather than sequentially or selectively. Doing so is likely to produce “better” theories by increasing
the stringency of the process through which tentative explanations are scrutinized (Weick, 1989).
    The application of multiple selection criteria at once places considerable cognitive demands on
researchers, who must actively hold each criterion in mind while assessing a conjectured explana-
tion and repeat this process iteratively across multiple thought trials (Sweller, 2011). As the num-
ber or complexity of criteria increases, researchers are therefore likely to simplify or selectively
apply them, often focusing – consciously or unconsciously – on a subset of especially salient or
familiar criteria (Weick, 1989). They are also likely to use these criteria sequentially, for instance,
by first attempting to establish the plausibility of a conjecture, and later to assess its transferability.
By contrast, GenAI can consider multiple criteria simultaneously and treat them as jointly relevant
(unless the prompter specifies otherwise), such that the disciplinary process becomes broad rather
than selective. It can do so at a number of selection criteria beyond the point at which human cogni-
tive load typically falters, and in a manner where specification of additional criteria is minimally
taxing.
    To ensure that epistemic authority remains with the researcher during disciplinary scrutiny (Lin
and Corley, 2026), we do not recommend prompting GenAI to eliminate conjectures itself, and, to
avoid premature closure or bias towards specific conjectures, we do not recommend prompting it
to identify a “best” conjecture. Rather, prompting should focus on identifying conjectures that
struggle to satisfy a set of selection criteria, such that researchers may progressively (manually)
discard conjectures to “discover” those which are more robust.
    To illustrate, we prompted GenAI with the 6 previously elaborated conjectures, provided it with
a list of selection criteria (see Table 2 for how we described these criteria in prompting, and Table
1 for their relationship with typical selection criteria in qualitative research), and asked it to iden-
tify and justify which conjecture may struggle most to satisfy these criteria overall. The selection
criteria we used (which are not exhaustive or perhaps even the most appropriate but serve only as
examples) reflected a range of methodological, empirical, and theoretical considerations, but we
encourage researchers to articulate their own criteria in accordance with their purposes. In response
to this prompt, GenAI presented a conjecture concerning expectation–disconfirmation dynamics as
the one that most struggled to satisfy the criteria4 (see Online Appendix Table A1). Researchers
may then reflect on the arguments presented by GenAI as they decide whether to drop this conjec-
ture or perhaps strengthen it as necessary.
    The purpose of this example is solely to demonstrate how a large and diverse set of selection
criteria can be applied simultaneously during disciplinary scrutiny. While we specified only 6 cri-
teria and 6 conjectures, researchers could expand these numbers drastically with minimal addi-
tional effort. They may also prompt GenAI to identify a greater number of potentially ill-fitting
conjectures (instead of one); as the number of criteria and conjectures increases, it may be neces-
sary to de-prioritize numerous thought trials to reach a manageable starting point for closer scru-
tiny. Importantly, it remains the researcher’s role to reflect upon the justifications GenAI provides
and decide for themselves which conjectures to take forward or eliminate. For a researcher who

--- page 13 ---

O’Sullivan and Ravasi                                                                                13

believed a particular conjecture was strong, its identification by GenAI as the weakest-fitting pre-
sents an opportunity for elaborating and strengthening this conjecture such that it is no longer
flagged as such.

Scaffolding discipline
Finally, GenAI scaffolds discipline by helping researchers more consistently scrutinize whether
conjectures satisfy or fail to satisfy given selection criteria (visualized in Figure 2 as narrowing the
slits on each disc through which beams of light may pass). It does so primarily through its capabili-
ties of self-attention and latent knowledge. Self-attention, again, enables the joint referencing of
conjectures and selection criteria during text generation. Latent knowledge, in turn, ensures that
concepts composing selection criteria are “understood” in line with a range of potential meanings
as captured in training data. As such, GenAI can generate diverse and sometimes competing inter-
pretations of how ambiguous concepts may be understood and applied.
    Disciplining imagination involves the scrutiny of conjectures against selection criteria. However,
given that many of the criteria commonly used to assess qualitative theories are abstract and
socially negotiated (Astley, 1985), whether a conjecture satisfies a given criterion is often some-
what ambiguous, creating scope for inconsistent application of criteria. That is, researchers may
come to believe that different conjectures satisfy the same criterion largely because they have
implicitly adopted different interpretations of the criterion, or what constitutes conjecture-criterion
fitness, in each case.
    GenAI can help structure this scrutiny by generating contrastive accounts both for and against
the fitness between conjectures and criteria. Each appraisal is likely to reflect a slightly different
interpretation of criteria and assumptions about what satisfies them. Exposure to such variation
marks an opportunity for researchers to compare how criteria may be differentially interpreted and
applied and to consider whether they endorse these appraisals; reflecting on these differences may
support gradual recognition of how one understands and wishes to employ a specific criterion.
Moreover, the generation of countervailing arguments exposes researchers to reasoning that chal-
lenges their initial inclinations, rendering it more difficult to sustain one-sided appraisals without
justification.
    In combination, these effects increase the visibility of appraisals and make inconsistencies in
criteria application more detectable, thus pushing researchers to better articulate both the selection
criteria they devise and how they appraise conjectures against these criteria, ultimately potentiating
greater consistency in the disciplinary process. Rather than directly resolving ambiguity or deter-
mining whether criteria are satisfied, then, GenAI can scaffold discipline by structuring the reason-
ing through which judgements are formed, and by providing opportunities for greater reflexivity
about these judgements. The devising of prompts, therefore, should emphasize these capabilities of
constructive argumentation, leaving ultimate judgement, selection, and elimination of conjectures
to the researcher.
    In our running example, we repeated the procedure outlined in the prior step three times, each
time discarding the conjecture GenAI articulated as the least appropriate after deliberation. We
took the three remaining conjectures and prompted GenAI to justify why each of these conjectures
satisfied the list of selection criteria described above, as well as why they failed to satisfy each of
these criteria. We also prompted GenAI to explicate its interpretation of the criterion in each
appraisal. While the previous prompting procedure compared all conjectures to all selection crite-
ria simultaneously (hence broadening discipline), this procedure iterated through each conjecture-
criteria appraisal.

--- page 14 ---

14                                                                       Strategic Organization 00(0)

    In response to this prompt, GenAI articulated its interpretation of each criterion and provided a
number of arguments for and against the alignment of conjectures and criteria (see Online Appendix
Table A1). Such responses may stimulate the ongoing revision or sharpening of selection criteria
but may also encourage researchers to revise other aspects of their research design to address the
shortcomings articulated by GenAI, such as consulting additional data sources if a conjecture is
identified as poorly fitting selection criteria concerning theory-method fit (Gehman et al., 2018).
    Once again, we advise that researchers devise their own prompting procedures in line with the
general principles we articulate. A procedure we have experimented with (which must be
approached with caution and not treated as authoritative) is prompting GenAI to use coarse-grained
qualitative categories (e.g. “low”, “moderate”, and “high”) to assess each conjecture against each
criterion and then rank conjectures in terms of their holistic fit across criteria. Although there is
reason to be sceptical of GenAI’s capacity to consistently produce such rankings and categoriza-
tions5 (i.e. repeating the same procedure will typically produce varied results), we have found that
seeing a rank or categorization that one was not expecting can trigger useful reflections about one’s
interpretations and/or selection criteria.
    It should be noted that GenAI appears unable to assist in credibly scrutinizing the fit of conjec-
tures with all selection criteria. For instance, criteria concerning empirical plausibility, or align-
ment of theory and data, would require observation of this raw data – something we do not
recommend entering into GenAI (as described further below). Criteria concerning theoretical con-
tributions, since they typically revolve around the novelty and utility of a theory (Corley and Gioia,
2011; Whetten, 1989), would require a concrete and up-to-date understanding of and sensitivity to
an ongoing scholarly conversation – something that is unlikely to be reflected in GenAI’s latent
knowledge, since training data lags behind practice; and since understanding of a theoretical
domain is often grounded in sources beyond published papers, such as conference presentations
and conversations with peers. We thus advise that the process of discipline remains within the
epistemic jurisdiction of researchers, that GenAI-supported scrutiny be manually subject to criti-
cism, and that researchers remain aware of the selection criteria that GenAI may be unhelpful in
evaluating conjectures against.
    As we conclude our running example, we should note that the procedures illustrated above are
not intended to culminate in a single movement through imagination and discipline, but to support
an iterative process of progressive sensemaking. Insights generated through disciplinary scrutiny
are likely to prompt researchers to refine their understanding of the focal empirical observation, or
to adjust data collection in ways that produce new empirical observations, which may initiate fur-
ther cycles of expanded and enriched imagination, and broadened and scaffolded discipline.


Applications across modes of theorizing
The example we used to illustrate our arguments reflects a variance-based (implicitly “proposi-
tional”; Cornelissen, 2017) mode of theorizing, which is aimed at the specification of theoretical
constructs and cause–effect relationships between them. In our experience, however, the underly-
ing logic of our approach can be extended beyond propositional theorizing to a broader range of
styles of qualitative theorization.
   Most forms of theorization require producing tentative explanations for empirical observations
and establishing means of evaluating them and selecting among them. An important difference, as
the procedures outlined above are applied to other modes of theorizing, is how researchers specify
summaries of empirical patterns entered into GenAI, and the responses that GenAI generates (see
Table 2 for examples). Researchers may also need to make minor adjustments to the formulation
of prompts to reflect different theoretical idioms, but these will still reflect the principles of

--- page 15 ---

O’Sullivan and Ravasi                                                                               15

producing more detailed, numerous, and heterogeneous conjectures, and subjecting them more
consistently and stringently to a greater number and diversity of selection criteria. While we leave
the full exploration of these adaptations for future research, the two rightmost columns in Table 2
offer a schematic overview of how the procedures we have outlined may apply to different styles
of qualitative theorizing (and Tables A2 and A3 of our Online Appendix offer full examples of
these procedures).
    For instance, when taking a process (or “narrative”; Cornelissen, 2017) approach to theorizing,
researchers typically seek to explain how outcomes emerge through sequences of actions or
events unfolding over time, often by identifying phases, transitions, and underlying processual
drivers that connect them (Langley, 1999). In this case, summarized empirical patterns tend to
incorporate a temporal dimension and may describe recurrent sequences of events, turning points,
or events that seemingly “trigger” consistent changes. Entering such patterns into GenAI and
prompting for conjectures that make sense of them (expanding imagination) tend to produce
thought trials of a different form from those in variance-based theorizing, emphasizing distinct
drivers of change, sequencing logics, and interpretations of how and why transitions occur.
Researchers may then prompt GenAI to elaborate these conjectures (enriching imagination) with
specific requests to articulate phases, triggers, and temporal mechanisms, rather than variance-
explaining mechanisms.
    When taking a typological approach, researchers aim instead to construct theoretically mean-
ingful types by identifying recurrent configurations of empirical observations and specifying
dimensions along which they differ (Doty and Glick, 1994). Summarized empirical patterns, in this
case, do not consist of sequences or associations, but of observed clusters or configurations – that
is, recurring sets of features – across cases. Prompting GenAI to expand imagination will generate
conjectures that specify or explain these observations – for instance, by proposing distinct differ-
entiating dimensions, logics of categorization, or typological structures. Conjectures here will not
necessarily correspond to explanatory mechanisms or drivers, but to different ways of organizing
observations into coherent sets of types. Enriching imagination also largely involves the proce-
dures outlined above, but researchers may also explicitly request clarification of the meanings of
dimensions, sharpening of distinctions between types, or exploration of how certain configurations
relate to those found in existing theory.
    Finally, during disciplinary scrutiny, researchers may also adapt the selection criteria they use
to the intended form of theorizing (see Table 2). Rather than specifying that thought trials identify
mechanisms that drive variance, for instance, researchers theorizing processes may emphasize
criteria stipulating that conjectures identify underlying drivers that consistently explain transitions
between a number of distinct phases. In typological theorizing, in contrast, researchers may use
criteria stipulating that conjectures maintain internal coherence within types and distinctiveness
between types. Many selection criteria, such as plausibility and appropriate embedding in existing
theory, however, are arguably relevant across modes of theorizing. Accordingly, while the content
of prompts and criteria may vary, the underlying procedures of scrutinizing conjectures against a
greater number of selection criteria (broadening discipline) and applying selection criteria in a
more consistent manner (scaffolding discipline) remain consistent across different styles of quali-
tative theorizing.

Limitations and pitfalls
Each of the four ways in which GenAI may augment qualitative theorization discussed above is
accompanied by distinct pitfalls that need to be accounted for. First, when using GenAI to expand
imagination, researchers must remember that autoregression is probabilistic and based on

--- page 16 ---

16                                                                         Strategic Organization 00(0)

statistical regularities encoded in the model’s parameters during training. As such, each token
GenAI generates may be said to reflect dominant, prototypical, or “average” responses. Such
observations have been used to argue that GenAI is unlikely to produce original theoretical insights
(Jowsey et al., 2025; Nguyen and Welch, 2026). A related risk arises when using GenAI to enrich
imagination: the training data that conditions GenAI’s latent knowledge is naturally time-lagged
and limited to open-access material. This means, as can be seen to an extent in our running example
(see Online Appendix Table A1), that GenAI’s parameters privilege theoretical material that has
“stood the test of time,” thus occupying a greater proportion of the training data. Accordingly, more
recent theoretical advances are likely to be overlooked or missing from GenAI’s attempts to elabo-
rate upon conjectures.
    However, given that theories must strike a balance between the known and unknown (Davis,
1971) and that the most novel explanations may not always be the most effective, these observa-
tions do not render GenAI useless in augmenting imagination but highlight the importance of
scholars themselves appraising (during disciplinary scrutiny) the novelty or redundancy of conjec-
tures. Furthermore, while GenAI outputs reflect “averages,” narrowing the input space – for
instance, by requesting conjectures within the remit of, say, “feminist organizational theory,” rather
than organization theory writ large – can increase the likelihood that average responses are them-
selves less conventional. Further still, these observations highlight the importance of aligning the
requests made of GenAI with its core capabilities: while GenAI may be less helpful in assessing
whether a similar conjecture was advanced in recent publications (which would likely lie outside
of its training data), it may help scholars recognize whether a given conjecture was advanced by
more foundational theories that feature less prominently in current academic conversations.
    It is important, however, to keep in mind that, because latent knowledge is encoded as statistical
associations rather than accurate understandings, and since autoregressive generation is probabil-
istic, GenAI may generate elaborations that are rhetorically compelling and plausible yet inaccu-
rate or partially fabricated. This potential to “hallucinate” (Ji et al., 2023; Maleki et al., 2024)
means that GenAI can sometimes produce responses that involve mischaracterized theories and
non-existent empirical findings.
    In our experience, prompting GenAI to reflect on or justify its own claims – for instance, by
simply asking “Is that really the case?” in response to an output, or asking for supportive evidence
– is often sufficient for it to revise its response or acknowledge uncertainty. However, researchers
working with GenAI to enrich their imagination need to maintain a critical stance towards GenAI
outputs and remain responsible for independently assessing outputs through direct engagement
with theory and data. The use of GenAI, then, should not be seen as a substitute for engagement
with academic literature, nor does it replace the necessity that researchers cultivate theoretical
sensitivity (Glaser, 1978) – that is, the capacity to recognize which conjectures are theoretically
meaningful and to evaluate and develop them in line with existing theory, rather than accepting
articulated explanations at face value.
    During disciplinary scrutiny, issues may arise if the application of selection criteria is not appro-
priately delineated from the imagination of conjectures. Because GenAI’s self-attention ensures
that generated text is conditioned by the entirety of preceding prompts and responses within a
given “chat,” selection criteria and thought trials risk influencing one another. In particular, if
selection criteria are specified prior to the generation of conjectures, the latter may be shaped to
fulfil those criteria. Conversely, if researchers use GenAI to generate or refine selection criteria
after having specified conjectures, the criteria themselves may become implicitly tailored to the
conjectures they are later used to assess. In both cases, disciplinary standards risk becoming endog-
enous to the imaginative process, undermining the process of disciplined imagination – not due to
inherent limitations of GenAI, but as a consequence of how it is used (Schildt, 2026).

--- page 17 ---

O’Sullivan and Ravasi                                                                               17

    To mitigate this risk, researchers should specify selection criteria prior to and independently
from the generation of conjectures, disable the memory functions of GenAI (to ensure it does not
retain information across chat instances), and use distinct chats when generating conjectures and
specifying criteria. When introducing additional criteria or conjectures, researchers should open a
new chat instance and begin the process again. Prompt construction is a substantive methodologi-
cal decision: while GenAI reduces cognitive constraints associated with holding many criteria in
mind, it does not remove the need for careful design and sequencing of prompts.
    A final limitation also concerns the use of GenAI to broaden and scaffold discipline. Although
GenAI may attempt to “persuade” (Randazzo et al., 2025; Salvi et al., 2025) researchers that it can
understand and apply any and all selection criteria, it most likely cannot. For instance, and of spe-
cial importance, GenAI appears (currently) unqualified to assess whether a conjecture represents a
theoretical contribution. Some of the reasons for this are technical: latent knowledge is time-lagged
and limited (e.g. to open-access papers); much up-to-date scholarly understanding exists tacitly,
beyond published papers, and is communicated informally in practice; autoregression is biased
towards prevalent trends, overlooking novelty, and so on. Other reasons are epistemological: what
makes a theoretical contribution is largely beyond the comprehension of an individual researcher;
theoretical contributions are rhetorical claims constructed in the context of deep embedding in a
scholarly community and validated by its gatekeepers (Astley, 1985; Locke and Golden-Biddle,
1997). Such observations may hold for a range of other potential criteria. Researchers themselves
must reason – in part by reflecting on the core competencies described above – whether GenAI is
“qualified” to apply a given criterion, and not to invite GenAI to contribute where it is less
fruitful.
    Finally, one may wonder whether it might be possible to short-circuit the process we described
by entering raw qualitative data into GenAI to directly generate conjectures or to use as potential
selection criteria. It is possible, of course, that, at some point, GenAI will develop to a degree that
will enable doing so credibly and reliably (c.f., Cornelissen, 2026). At the time we are writing this
article, however, we are not sure it is advisable (yet). Besides ethical concerns (see Davison et al.,
2024; Kulkarni et al., 2024), doing so risks loosening the researcher’s grip over the theorization
process. Because GenAI is optimized to surface linguistic patterns rather than theoretically mean-
ingful ones, providing raw data may orient theorization towards statistically salient but analytically
irrelevant patterns. Moreover, when conjectures are shaped by GenAI’s processing of raw data, it
becomes more difficult for researchers to trace and account for the interpretive decisions through
which empirical material is rendered theoretically meaningful, undermining transparency and
reflexivity (Macbeth, 2001; Pratt et al., 2020).
    In fact, there might be little benefit, procedurally, in entering raw data into GenAI. While a
higher-resolution specification of an empirical pattern should enable the generation of more appro-
priate conjectures (Weick, 1989), a carefully crafted summary can achieve this aim without
recourse to raw data – and, given the typical messiness and context-specificity of qualitative data,
may even do more efficaciously. Introducing these methodological and ethical concerns into the
research process, then, entails taking on substantial risk for comparatively little theoretical reward.

Conclusion
In this article, we conceptualized qualitative theorization as a process of “disciplined imagination”
(Weick, 1989), identified core capabilities of GenAI that pertain to this process, and explained how
these capabilities may be harnessed to augment qualitative theorization in substantive, non-trivial
ways. We illustrated these arguments through a running example and prompting suggestions
informed by our own experiences. These illustrations should not be interpreted as a prescription for

--- page 18 ---

18                                                                                Strategic Organization 00(0)

the automation of theorization, but rather as a framework for thinking more carefully about how
emerging technologies can support one of the most elusive, yet most consequential, activities in
qualitative research.
   We would like to close by reflecting on a comment raised by one anonymous reviewer, who
rightly asked why one would bother to use GenAI in the manner we have described when one could
instead have a chat with a colleague over coffee. Indeed, these brief interactions often provide
opportunities for imagination and discipline. But many researchers (especially those more junior,
or more peripheral to academic networks) lack access to a broad set of peers with whom they can
regularly discuss their work. Furthermore, many of these brief interactions turn out to be less
insightful than one would hope – perhaps because they must end before anything substantive was
discussed; perhaps because one realizes too late that their ideas were not yet quite coherent or
developed enough to seek input on. The augmentations we describe may give less connected
researchers at least some means of “discussing” their theorizations, or aid others in preparing for
future discussions with peers. While GenAI, as we understand it, certainly cannot, and should not,
replace human contribution to the theorization of qualitative data, we may still underestimate the
benefits that a careful – but open-minded – use of these tools might bring to our scholarly
practices.

ORCID iD
Davide Ravasi       https://orcid.org/0000-0001-7498-467X

Funding
The authors received no financial support for the research, authorship, and/or publication of this article.

Declaration of conflicting interests
The authors declared no potential conflicts of interest with respect to the research, authorship, and/or publica-
tion of this article.

Supplemental material
Supplemental material for this article is available online.

Notes
1.   Peirce initially referred to this inference mode as retroduction, and later used the terms retroduction and
     abduction somewhat interchangeably to refer essentially to inference-to-best-explanation (Pietarinen &
     Bellucci, 2014). In management studies, the use of the term abduction is now prevailing (Klag and
     Langley, 2013; Mantere & Ketokivi, 2013); some, however, use the term retroduction to label a different
     inferential process, based on the search for generative forces and mechanisms for empirical observations
     (Bhaskar, 1975; Sayer, 1992).
2.   We employ these terms as more accessible short-hand simplifications of the actual technical features
     underlying GenAI. While self-attention and autoregression are established technical terms, “latent
     knowledge” is our own coinage to refer more simply to the processes surrounding the training of GenAI
     models.
3.   We disabled ChatGPT’s memory functions and used “temporary chats” to ensure that it produced results
     that others could reasonably expect.
4.   Autoregressive generation involves a degree of stochasticity, such that it may produce different outputs
     across trials (in this case, different conjectures being presented as the poorest fitting). Responses to this
     procedure, however, appear quite consistent. In any case, researchers can address this by running the
     same prompt multiple times and observing which conjectures are most and least frequently identified.

--- page 19 ---

O’Sullivan and Ravasi                                                                                      19

5.   Autoregressive generation involves a degree of stochasticity that can produce different outputs – and
     thus rankings – across repeated runs of the same prompt. Models can be adjusted to always return the
     highest probability token, with no stochastic variation across trials, but fine-grained control over this
     process is not available for the easy-to-use standard interfaces of LLMs like ChatGPT and Claude.

References
Alvesson M and Willmott H (2002) Identity regulation as organizational control: Producing the appropriate
     individual. Journal of Management Studies 39(5): 619–644.
Aristidou A and Scheuermann K (2024) Could AI speak on behalf of future humans? Stanford Social
     Innovation Review. https://doi.org/10.48558/N4BW-ND72
Astley WG (1985) Administrative science as socially constructed truth. Administrative Science Quarterly 30:
     497–513.
Bacharach SB (1989) Organizational theories: Some criteria for evaluation. The Academy of Management
     Review 14(4): 496.
Bamberger PA (2019) On the replicability of abductive research in management and organizations: Internal
     replication and its alternatives. Academy of Management Discoveries 5(2): 103–108.
Bhaskar R (1975) A Realist Theory of Science. Taylor & Francis.
Bommasani R, Hudson DA, Adeli E, et al. (2022) On the opportunities and risks of foundation models.
     arXiv:2108.07258. Available at: http://arxiv.org/abs/2108.07258
Burleigh C and Wilson AM (2024) Generative AI: Is authentic qualitative research data collection possible?
     Journal of Educational Technology Systems 53(2): 89–115.
Charmaz K (2006) Constructing Grounded Theory: A Practical Guide through Qualitative Analysis. SAGE.
Ciechanowski L, Jemielniak D and Gloor PA (2020) Tutorial: AI research without coding: The art of fighting
     without fighting: Data science for qualitative researchers. Journal of Business Research 117: 322–330.
Cloutier C and Langley A (2020) What makes a process theoretical contribution? Organization Theory 1(1):
     902473.
Corley KG and Gioia DA (2011) Building theory about theory building: What constitutes a theoretical con-
     tribution? Academy of Management Review 36(1): 12–32.
Cornelissen J (2017) Editor’s comments: Developing propositions, a process model, or a typology? Addressing
     the challenges of writing theory without a boilerplate. Academy of Management Review 42(1): 1–9.
Cornelissen J (2026) The AI con: The commodification of theory and the new and improved credibility crisis.
     Organization Studies. Epub ahead of print 1 May. https://doi.org/10.1177/01708406261450467
Davis MS (1971) That’s interesting! Towards a phenomenology of sociology and a sociology of phenomenol-
     ogy. Philosophy of the Social Sciences 1(2): 309–344.
Davison RM, Chughtai H, Nielsen P, et al. (2024) The ethics of using generative AI for qualitative data analy-
     sis. Information Systems Journal 34(5): 1433–1439.
Doty DH and Glick WH (1994) Typologies as a unique form of theory building: Toward improved under-
     standing and modeling. Academy of Management Review 19(2): 230–251.
Eisenhardt KM (1989) Building theories from case study research. Academy of Management Review 14(4):
     532–550.
Furnari S, Crilly D, Misangyi VF, et al. (2021) Capturing causal complexity: Heuristics for configurational
     theorizing. Academy of Management Review 46(4): 778–799.
Gabriel Y (2015) Reflexivity and beyond: A plea for imagination in qualitative research methodology.
     Qualitative Research in Organizations and Management: An International Journal 10(4): 332–336.
Gehman J, Glaser VL, Eisenhardt KM, et al. (2018) Finding theory–method fit: A comparison of three quali-
     tative approaches to theory building. Journal of Management Inquiry 27(3): 284–300.
Glaser B (1978) Theoretical Sensitivity: Advances in the Methodology of Grounded Theory. The Sociology
     Press.
Glaser B and Strauss AL (1967) The Discovery of Grounded Theory. Aldine Pub. Co.
Grodal S, Anteby M and Holm AL (2021) Achieving rigor in qualitative analysis: The role of active catego-
     rization in theory building. Academy of Management Review 46(3): 591–612.
Harley B and Cornelissen J (2022) Rigor with or without templates? The pursuit of methodological rigor in
     qualitative research. Organizational Research Methods 25(2): 239–261.

--- page 20 ---

20                                                                               Strategic Organization 00(0)

Hayes AS (2025) “Conversing” with qualitative data: Enhancing qualitative research through large language
      models (LLMs). International Journal of Qualitative Methods 24: 322346.
Hochschild AR (1983) The Managed Heart: Commercialization of Human Feeling. University of California
      Press.
Howard-Grenville J, Nelson A, Vough H, et al. (2021) From the editors: Achieving fit and avoiding .misfit in
      qualitative research. Academy of Management Journal 64(5): 1313–1323.
Huff AS (1998) Writing for Scholarly Publication. SAGE.
Ji Z, Lee N, Frieske R, et al. (2023) Survey of hallucination in natural language generation. ACM Computing
      Surveys 55(12): 1–38.
Jowsey T, Braun V, Clarke V, et al. (2025) We reject the use of generative artificial intelligence for
      reflexive qualitative research. Qualitative Inquiry. Epub ahead of print 17 December. https://doi.
      org/10.1177/10778004251401851
Kilduff M and O’Sullivan D (2026) Where’s the theory contribution? An answer in four parts. Organizational
      Psychology Review 16(1): 127–140.
Klag M and Langley A (2013) Approaching the conceptual leap in qualitative research. International Journal
      of Management Reviews 15(2): 149–166.
Kulkarni M, Mantere S, Vaara E, et al. (2024) The future of research in an artificial intelligence-driven world.
      Journal of Management Inquiry 33(3): 207–229.
Kunda G (1992) Engineering Culture: Control and Commitment in a High-Tech Corporation. Temple
      University Press.
Langley A (1999) Strategies for theorizing from process data. Academy of Management Review 24(4): 691–
      710.
Lin X and Corley K (2026) Interpretive orchestration: An essay exploring the epistemic intersection of human
      intuition and machine intelligence. Strategic Organization. Epub ahead of print 27 April. https://doi.
      org/10.1177/14761270261448645
Lincoln YS and Guba EG (1985) Naturalistic Inquiry. SAGE.
Locke K and Golden-Biddle K (1997) Constructing opportunities for contribution: Structuring intertextual
      coherence and “problematizing” in organizational studies. Academy of Management Journal 40(5):
      1023–1062.
Locke K, Feldman M and Golden-Biddle K (2022) Coding practices and iterativity: Beyond templates for
      analyzing qualitative data. Organizational Research Methods 25(2): 262–284.
Macbeth D (2001) On “reflexivity” in qualitative research: Two readings, and a third. Qualitative Inquiry
      7(1): 35–68.
Maleki N, Padmanabhan B and Dutta K (2024) AI hallucinations: A misnomer worth clarifying. In:
      Proceedings of the 2024 IEEE conference on artificial intelligence (CAI), IEEE, pp.133–138.
Mantere S and Ketokivi M (2013) Reasoning in organization science. Academy of Management Review 38(1):
      70–89.
Murphy KP (2023) Probabilistic Machine Learning: Advanced Topics. MIT Press.
Nguyen DC and Welch C (2026) Generative artificial intelligence in qualitative data analysis: Analyzing – Or
      just chatting? Organizational Research Methods 29(1): 3–39.
Pierce CS (1934) Collected Papers, vol. 5. Harvard University Press.
Petroni F, Rocktäschel T, Lewis P, et al. (2019) Language models as knowledge bases? arXiv:1909.01066.
      Available at: http://arxiv.org/abs/1909.01066
Pierce JL, Kostova T and Dirks KT (2001) Toward a theory of psychological ownership in organizations. The
      Academy of Management Review 26(2): 298.
Pietarinen AV and Bellucci F (2014) New light on Peirce’s conceptions of retroduction, deduction, and scien-
      tific reasoning. International Studies in the Philosophy of Science 28(4): 353–373.
Pratt MG, Kaplan S and Whittington R (2020) Editorial essay: The tumult over transparency: Decoupling
      transparency from replication in establishing trustworthy qualitative research. Administrative Science
      Quarterly 65(1): 1–19.
Radford A, Narasimhan K, Salimans T, et al. (2018) Improving language understanding by generative pre-
      training. Available at: https://cdn.openai.com/research-covers/language-unsupervised/language_under-
      standing_paper.pdf

--- page 21 ---

O’Sullivan and Ravasi                                                                                        21

Randazzo S, Joshi A, Kellogg K, et al. (2025) GenAI as a power persuader: How professionals get persua-
     sion bombed when they attempt to validate LLMs. Available at: https://papers.ssrn.com/sol3/papers.
     cfm?abstract_id=5678644
Rouse E, Reinecke J, Ravasi D, et al. (2025) Making a theoretical contribution with qualitative research.
     Academy of Management Journal 68(2): 257–266.
Sætre AS and Van De Ven A (2021) Generating theory by abduction. Academy of Management Review 46(4):
     684–701.
Salvi F, Horta Ribeiro M, Gallotti R, et al. (2025) On the conversational persuasiveness of GPT-4. Nature
     Human Behaviour 9(8): 1645–1653.
Sayer RA (1992) Method in Social Science: A Realist Approach. Psychology Press.
Schildt H (2026) The case for AI in qualitative research. Organization Studies. Epub ahead of print 10 May.
     https://doi.org/10.1177/01708406261452993
Sinha R, Solola I, Nguyen H, et al. (2024) The role of generative AI in qualitative research: GPT-4’s contribu-
     tions to a grounded theory analysis. In: Proceedings of the symposium on learning, design and technol-
     ogy, Delft, 21 June. ACM, pp.17–25. Available at: https://dl.acm.org/doi/10.1145/3663433.3663456.
Sloan J and Glaser V (2026) Robotic artistry: Four surprise pathways for GenAI-assisted abductive theoriza-
     tion. Strategic Organization. Epub ahead of print 28 April. https://doi.org/10.1177/14761270261448648
Strauss A and Corbin J (1998) Basics of Qualitative Research Techniques. Citeseer.
Susarla A, Gopal R, Thatcher JB, et al. (2023) The Janus effect of generative AI: Charting the path for
     responsible conduct of scholarly activities in information systems. Information Systems Research 34(2):
     399–408.
Sutton RI and Staw BM (1995) What theory is not. Administrative Science Quarterly 40(3): 371–384.
Swann WB (1983) Self-verification: Bringing social reality into harmony with the self. In: Suls J and
     Greenwald AG (eds) Social Psychological Perspectives on the Self, vol. 2. New York, Lawrence:
     Erlbaum, pp.33–66.
Sweller J (2011) Cognitive load theory. In: Federmeier KD (ed.) Psychology of Learning and Motivation.
     Elsevier, pp.37–76.
Tversky A and Kahneman D (1974) Judgment under uncertainty: Heuristics and biases – Biases in judgments
     reveal some heuristics of thinking under uncertainty. Science 185(4157): 1124–1131.
Vaswani A, Shazeer N, Parmar N, et al. (2017) Attention is all you need. arXiv: 1706.03762.
Wang Y (2024) Interviewing GPTs: Can generative AI intelligence become a new source of qualitative
     research data?. Available at: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4874356
Weick KE (1989) Theory construction as disciplined imagination. Academy of Management Review 14(4):
     516–531.
Weick KE (1995) Sensemaking in Organizations. SAGE.
Weick KE (2006) The role of imagination in the organizing of knowledge. European Journal of Information
     Systems 15(5): 446–452.
Whetten DA (1989) What constitutes a theoretical contribution? Academy of Management Review 14(4):
     490–495.
Yin RK (2009) Case Study Research: Design and Methods. SAGE.

Author biographies
Daniel O’Sullivan is a PhD candidate at the UCL School of Management, University College London. He
uses qualitative methods to examine how individuals pursue meaning and autonomy in emerging work con-
texts – particularly those marked by novel, technologically facilitated forms of control and evaluation. He also
conducts research on advances in qualitative research methods and theory development.
Davide Ravasi is Professor of Strategy and Entrepreneurship and School Director at UCL School of
Management, University College London. His research primarily examines strategic and organizational
changes, with particular emphasis on how organizational culture and identity affect these changes or are
affected by them. His more recent work examines the role that history and memory play in these events. He
is also interested more generally in socio-cognitive processes surrounding design, craft, and innovation.
