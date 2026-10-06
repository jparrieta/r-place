# Günther, Joshi and Constantinides (2026), Trustworthiness in computational theory construction: dimensionalization and category surfacing

Source: `gunther-joshi-constantinides-2026.pdf`. Text extracted by pdftotext; layout kept, page breaks marked. A quote from this file is the extraction's, so check an odd word against the page it names.

--- page 1 ---

METHODS ARTICLE




                                     TRUSTWORTHINESS IN COMPUTATIONAL THEORY
                                         CONSTRUCTION: DIMENSIONALIZATION
                                            AND CATEGORY SURFACING1
                                                                                           Wendy Arianne Günther
                                                                      KIN Center for Digital Innovation, Vrije Universiteit Amsterdam
                                                                     Amsterdam, THE NETHERLANDS {w.a.gunther@protonmail.com}

                                                                                                     Mayur Joshi
                                                                               Telfer School of Management, University of Ottawa
                                                                               Ottawa, CANADA {mayur.joshi@telfer.uottawa.ca}

                                                                                             Panos Constantinides
                                                                    Alliance Manchester Business School, The University of Manchester
                                                                         Manchester, U.K. {panos.constantinides@manchester.ac.uk}


                                   In this methods article, we unpack how researchers can foster trustworthiness in dimensionalization and
                                   category surfacing (DCS), a key method family within the genre of computational theory construction
                                   (CTC). Information systems (IS), management, and organizational scholars are increasingly leveraging
                                   DCS tools such as topic modeling, word embeddings, and clustering to surface latent categories and
                                   dimensions from textual data for theory construction. Yet they struggle because evaluations of such
                                   research often default to transparency, operationalized as replicability and accountability, which
                                   obscures the analytical choices that actually make DCS research rigorous. In this study, we recast
                                   transparency as a means toward fostering trustworthiness. We treat researchers’ analytical moves as the
                                   primary unit of methodological reasoning in how they design, conduct, and disclose their choices across
                                   research phases. We develop a framework that authors, reviewers, and editors can use to construct and
                                   evaluate DCS research. The framework specifies how trustworthiness arises from the interplay of two
                                   research design choices: giving primacy to theoretical versus practice lexicons, and whether the content
                                   of texts or the structure of the corpus carries the theoretical load. We articulate expectations for conduct
                                   and disclosure across these design choices, clarifying how proportionate reasoning anchors
                                   trustworthiness. We conclude with implications for advancing trustworthiness within the broader CTC
                                   community and across other computational approaches to research.
                                   Keywords: Computational Theory Construction, Dimensionalization and Category Surfacing,
                                   Trustworthiness, Analytical Moves, Computational Tools, Artificial Intelligence




                  1
                    Shaila Miranda was the accepting senior editor for this paper. Hani Safadi served as the associate editor. The first two authors contributed equally and are listed
                  alphabetically. The transparency materials for this paper are available at https://osf.io/c9th4/files/xcmzf

                                      ©2026. The Authors. This work is licensed under the terms of the Creative Commons Attribution CC BY 4.0 License
                                      (https://creativecommons.org/licenses/by/4.0/)




                   DOI:10.25300/MISQ/2026/18511                                                                MIS Quarterly Vol. 50 No. 3 pp. 851-878 / September 2026        851



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 2 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Introduction                                                                                      practice lexicons (i.e., whether the meaning system guiding
                                                                                                                    analysis originates primarily in theory or in the
                  Computational theory construction (CTC) is an emerging                                            phenomenon), and (2) whether the content of texts carry the
                  research genre that involves the use of machine learning                                          theoretical load, or the structure of the corpus is the focus of
                  (ML) algorithms and other artificial intelligence (AI) tools                                      theory construction. Positioning a study on these two axes
                  to construct theories from large volumes of data (Berente et                                      clarifies purpose and appropriate analytical moves against
                  al., 2019; Miranda et al., 2022a). Within CTC research,                                           emergent tensions. We then specify expectations across
                  computational tools that allow for dimensionalization and                                         three phases of DCS research, including data work, model
                  category surfacing (DCS)—including topic modeling, word                                           building and pattern surfacing, and validating and
                  embeddings, and clustering, among others (henceforth DCS                                          theorizing, as well as cross-phase iterations. We argue that
                  tools) (see Miranda et al., 2022a)—have become central for                                        researchers need to adapt their analytical moves in
                  interpretive scholars. DCS tools facilitate surfacing latent                                      accordance with their chosen approach to foster
                  categories and dimensions from textual corpora, a practice                                        trustworthiness.
                  traditionally fundamental to constructing theories through
                  qualitative analysis (Grodal et al., 2021; Strauss & Corbin,                                      Our framework offers actionable guidance for authors,
                  1990). As interest in leveraging DCS tools for constructing                                       reviewers, and editors engaged with DCS research that
                  theories (henceforth DCS research) grows, so do the                                               analytically generalizes to the broader CTC community. For
                  expectations of transparency to evaluate its rigor. Yet                                           authors, it maps two research design choices—giving
                  authors, reviewers, and editors face recurring challenges                                         primacy to theoretical versus practice lexicons, and a focus
                  when conducting and evaluating DCS research, many of                                              on the content of texts versus the structure of the corpus—to
                  which stem from treating transparency as an end in itself.                                        phase-specific and iterative analytical moves. For reviewers,
                                                                                                                    it provides a basis to inspect whether those moves are
                  Across scientific fields and leading journals in information                                      explicit and proportionate to the study’s aims. For editors, it
                  systems (IS), management, and organizational research,                                            supports reviewer assignment and decisions by emphasizing
                  calls for transparency have amplified (Burton-Jones et al.,                                       fit among research objectives, analytical moves, and
                  2021; DeCelles et al., 2021; see also Aguinis et al., 2024).                                      evidence. We also offer implications for a larger CTC and
                  However, prevailing guidelines are often calibrated to                                            computational research community who may be engaging
                  traditional quantitative and qualitative research genres and                                      with different types of computational tools for theory
                  hence travel poorly to CTC, and to DCS research in                                                construction or may be using DCS tools to test deductively
                  particular. Importing quantitative standards presumes stable                                      constructed theories.
                  procedures and externally verifiable replicability, yet
                  unsupervised DCS tools rarely yield a unique model; results
                  are sensitive to preprocessing and parameterization and
                  unsettle any ground truth (Grimmer et al., 2022; Valtonen et
                                                                                                                    From Transparency to Trustworthiness:
                  al., 2024). Importing qualitative standards presumes                                              Expectations of Rigor in DCS Tools and
                  researchers can fully account for their decisions, but DCS                                        Practices
                  research embeds algorithmic assumptions and model-
                  internal moves that remain partly opaque to the researchers,                                      In this section, we start by explaining how expectations of
                  complicating accountability (cf., Constantiou et al., 2023;                                       rigor in IS, management, and organizational research often
                  Lebovitz et al., 2021; Waardenburg et al., 2022).                                                 translate into guidance for achieving transparency. While
                                                                                                                    this guidance spans across qualitative and quantitative
                  In this methods article, we reframe the conversation by                                           genres, with divergent meanings of transparency across
                  centering trustworthiness and treating transparency as a                                          these genres, there is little guidance that speaks directly to
                  means to that end. Our methodological review and author                                           the CTC research genre and none tailored to the DCS method
                  interviews show that DCS researchers are often pushed                                             family. We then explain why treating transparency as an end
                  toward conflicting practices and expectations in how to                                           goal when evaluating rigor fits poorly with DCS research,
                  facilitate trustworthiness. We develop a framework that                                           given the nature of the computational tools and research
                  helps researchers design, conduct, and disclose analytical                                        practices. We close by arguing that instead of attempting to
                  moves for constructing theory with DCS tools in ways that                                         develop specific guidance on transparency for DCS research,
                  are conceived as trustworthy by reviewers and editors. The                                        the community needs to recast transparency as a means
                  framework turns on two research design choices that govern                                        toward fostering trustworthiness in order to integrate
                  both conduct and disclosure: (1) whether researchers choose                                       concerns for conduct and the disclosure of methods and to
                  to give primacy to theoretical lexicons or primacy to                                             improve the fit with exploratory, abductive DCS work.



                   852       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 3 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Divergent Meanings of Transparency Across                                                         Quarterly and Academy of Management Journal 2 (e.g.,
                  Research Genres                                                                                   Burton-Jones et al., 2021; DeCelles et al., 2021), there is
                                                                                                                    comparatively little guidance for CTC and DCS research.
                  Expectations of rigor in research often translate into transparency                               While one could attribute this lack of guidance to the CTC
                  guidelines (Jacobs et al., 2021; also see Constantinides et al.,                                  research genre’s nascency, we argue for a more fundamental
                  2012) with research genre-specific meanings and                                                   reason: Treating transparency as an end does not travel well
                  recommendations. While some discussions on transparency                                           into DCS research because of the nature of DCS tools and
                  imply a close connection with replicability (e.g., Aguinis &                                      research practices.
                  Solarino, 2019; Schooler, 2014), others equate transparency with
                  accountability (e.g., Monteiro et al., 2022; Sarker et al., 2013).                                DCS tools represent a class of computational methods and
                                                                                                                    techniques crucial for theory construction in contemporary
                  A first set of meanings links transparency to replicability, often                                qualitative and computationally intensive research (see
                  interchangeably with reproducibility, especially in the                                           Simeonova & Galliers, 2023). Common DCS tools for text
                  quantitative research genre. Reproducibility concerns whether                                     mining and natural language processing include topic
                  independent analysts can obtain the same results with the same                                    modeling, word embeddings, and clustering (see Aceves &
                  data and draw similar conclusions; replicability asks whether                                     Evans, 2023; Hannigan et al., 2019; Kobayashi et al., 2018;
                  comparable results can be obtained with new data collected under                                  Schmiedel et al., 2019). These tools leverage unsupervised
                  similar designs and procedures (Aguinis et al., 2018). An
                                                                                                                    algorithms to uncover latent semantic structures within
                  underlying assumption that is implicit in this pursuit of
                                                                                                                    textual data. Rather than starting with predefined categories,
                  replicability is the existence of ground truth, i.e., identification of
                                                                                                                    these approaches help researchers to inductively identify
                  a data point as a true representation of the world against which
                  the evidence provided by a given study can be evaluated (e.g.,                                    latent patterns, surfacing novel theoretical dimensions from
                  Marshall et al., 2023). Though critics have noted limits to                                       the data (Miranda et al., 2022a). DCS research proceeds
                  replication across contexts and time (e.g., Tremblay et al., 2021).                               through data work (e.g., sampling and text preprocessing),
                                                                                                                    model building and pattern surfacing (e.g., choosing
                  A second set of meanings equates transparency with                                                algorithms as well as parameters), and validation and
                  accountability, especially in the qualitative research genre. Here,                               theorizing (e.g., sensitivity analysis and interpretive
                  transparency aims to render visible the researcher’s positioning                                  validation). These steps involve significant manual labor and
                  and choices so that a knowledgeable reader can audit the chain                                    qualitative judgment. DCS research is prized in interpretive
                  from data to knowledge claims (Constantinides et al., 2012;                                       CTC precisely because it combines manual and automated
                  Monteiro et al., 2022; Sarker et al., 2013). The underlying                                       activity to surface theoretically relevant patterns in text (see
                  assumption in the discourse around accountability is the ability of                               the transparency materials3 for a primer on DCS tools).
                  researchers to systematically account for and, thus, be transparent
                  about their choices and the interpretations that they draw from the                               The nature of DCS tools makes existing transparency
                  data they analyze (Sarker et al., 2013). However, scholars have                                   templates ill-posed for DCS research. On the one hand,
                  cautioned against the accountability drive, when some research                                    importing quantitative standards assumes stable procedures
                  approaches may be bound by value judgements and may not offer                                     and externally verifiable replicability, treating DCS tools as
                  systematic methods (Elliott, 2022). In such cases, “transparency                                  similar to traditional quantitative tools (e.g., fixed effects
                  about value judgments in particular could also cause people to                                    regression models). This assumption is problematic because
                  develop an unwarranted skepticism about scientific results once                                   unsupervised DCS tools rarely yield a single model that could
                  they realize that scientific research is not as straightforward as it                             embody “one right way” of constructing theories (Grimmer et
                  might initially appear” (Elliott, 2022, p. 349).                                                  al., 2022, p. 30); outputs are sensitive to choices in
                                                                                                                    preprocessing       and     parameterization,      complicating
                                                                                                                    replicability and the very notion of a ground truth (Grimmer
                  DCS Research and the                                       Inadequacy                of           et al., 2022; Valtonen et al., 2024). On the other hand,
                  Transparency as an End                                                                            importing qualitative standards assumes that researchers can
                                                                                                                    fully account for their decisions, treating DCS tools like
                  Despite growing guidance on transparency for quantitative                                         traditional qualitative analysis tools (e.g., NVivo). But unlike
                  and qualitative genres across journals, including MIS

                  2
                   Also see transparency guidance for other journals: Management Science                            sagepub.com/pb-assets/cmscontent/ASQ/Data%20and%20Methods%20
                  (https://pubsonline.informs.org/page/mnsc/code-and-data-disclosure-policy),                       Transparency%20Policy%20040324-1712174442.pdf).
                                                                                                                    3
                  Organization Science (https://pubsonline.informs.org/page/orsc/data-and-                            The transparency materials are available at https://osf.io/c9th4/files/xcmzf
                  methods-transparency), and Administrative Science Quarterly (https://journals.




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026          853



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 4 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  typical qualitative coding exercises for surfacing categories                                     standards should be fit for purpose and attentive to the
                  (c.f., Grodal et al., 2021; Strauss & Corbin, 1990), in DCS                                       distinctive threats and assurances of the research design,
                  research with computational tools, many consequential                                             rather than imported wholesale from adjacent paradigms
                  analytical moves occur inside the tools themselves, through                                       (Amis & Silk, 2008; Easterby-Smith et al., 2008; Guba,
                  automated activity. DCS tools embody algorithmic                                                  1981; Lincoln & Guba, 1985). Put differently, the “degree of
                  assumptions and moves that can remain opaque even to expert                                       transparency here is not set by the demands for replication
                  users, thus complicating accountability (cf., Constantiou et al.,                                 but is more broadly set by the degree to which authors can
                  2023; Lebovitz et al., 2021; Waardenburg et al., 2022).                                           convince the reader that they have been honest in how their
                                                                                                                    research has been carried out” (Pratt et al., 2020, p. 12).
                  What further complicates generic transparency guidance is                                         Trustworthiness also goes beyond accountability because it
                  that in DCS research, knowledge is created through an                                             is not primarily achieved by reporting standardized
                  iterative process in which researchers are both guided by and                                     knowledge production processes or templates but by
                  actively shape algorithmic outputs. Here, Grodal et al.’s                                         encouraging researchers to devise “analytical moves tailored
                  (2021) “active-categorization” perspective is instructive:                                        to their research objectives” (Pratt et al., 2022, p. 212).
                  theory building proceeds through purposeful sequences of
                  moves—asking questions, focusing on puzzles, and dropping,                                        This view aligns with the idea that rigor “does not reside in
                  merging, splitting, relating, and sequencing categories for                                       protocolized techniques or methods but in the very process
                  theory development. DCS research naturally instantiates this                                      of researchers reasoning about their use of particular
                  logic, but with a twist: category structures emerge through a                                     techniques or methods and reporting such reflections in their
                  reflexive relationship between the researcher and the                                             articles” (Harley & Cornelissen, 2022, p. 240). Accordingly,
                  algorithm(s) (Günther et al., 2023; Lindberg, 2020). Thus,                                        we treat analytical moves as methodological reasoning,
                  extant transparency prescriptions are unfit to guide                                              encompassing both methodological conduct (how to design
                  researchers, either because they demand sameness where                                            and enact research practices) and disclosure (what to report
                  multiple defensible choices exist, or because they emphasize                                      and how). Previous scholarship on trustworthiness makes
                  standardized reporting that obscures how specific moves                                           this move-centered logic explicit by tying confidence in
                                                                                                                    claims to concrete practices and their documentation—e.g.,
                  shaped and were shaped by algorithmic outputs.
                                                                                                                    triangulation, prolonged engagement, peer debriefing,
                                                                                                                    member checks, and audit trails—rather than to compliance
                                                                                                                    with a single reporting template (Guba, 1981; Locke &
                  Recasting Transparency as a Means To Foster                                                       Ramakrishna Velamuri, 2009). More recent methodological
                  Trustworthiness in DCS Research                                                                   work similarly frames transparency devices (e.g., structured
                                                                                                                    tables) as means of making analytic reasoning inspectable in
                  To move beyond these impasses, we argue for recasting                                             ways that can strengthen trustworthiness without reducing
                  transparency as a means to foster trustworthiness. We argue                                       qualitative work to procedural box-checking (Cloutier &
                  that the community may not benefit from trying to develop                                         Ravasi, 2021; O’Kane et al., 2021). Thus, fostering
                  generic transparency guidelines for DCS research. This is                                         trustworthiness does not involve DCS scholars forcing their
                  because what seems to be lost in existing debates on                                              analyses into inherited transparency templates; rather, it
                  replicability and accountability is the important role of                                         encourages methodological bricolage and analytical, move-
                  transparency in accelerating knowledge production through                                         centric reasoning aligned with research objectives (Harley &
                  reflexivity (Günther et al., 2023). In the spirit of cumulative                                   Cornelissen, 2022; O’Kane et al., 2021; Pratt et al., 2022).
                  tradition, researchers should reflect on different scenarios and                                  Yet fostering trustworthiness in DCS research also brings
                  choices and the applicability of different practices to their own                                 unique tensions for researchers, which we explain next.
                  research (Harley & Cornelissen, 2022; Pratt et al., 2022).

                  We thus turn to the construct of trustworthiness (Pratt et al.,
                  2020, 2022). It allows us not to conceive transparency as an
                                                                                                                    Tensions in Fostering Trustworthiness In
                  end in itself but as something to be calibrated to the study’s                                    DCS Research
                  research objectives and practices, i.e., the specific research
                  choices one makes in terms of which methods to apply and                                          We highlight recurring tensions in how DCS researchers
                  how, and the purpose of employing specific research                                               conduct and disclose their analytical moves—and how these
                  practices in specific contexts (Monteiro et al., 2022; Pratt et                                   choices shape what readers can reasonably treat as
                  al., 2020, 2022). This orientation is consistent with                                             trustworthy. We surfaced these tensions by drawing on (1) a
                                                                                                                    methodological review of studies using topic modeling, one
                  foundational arguments in qualitative research: Evaluative



                   854       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 5 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  of the most commonly employed DCS tools in IS,                                                    We uncovered three recurring trustworthiness tensions: (1)
                  management, and organizational research, and (2) interviews                                       prioritizing objective versus customized data work, (2)
                  with authors who have published DCS research in these                                             seeking stability versus variance in model building, and (3)
                  domains.4 The review revealed wide divergence in how                                              benchmarking against ground truth versus accounting for
                  choices during data work, model building, and validation are                                      interpretations in validation. For each tension, we explain
                  justified and disclosed; the interviews helped us understand                                      why it arises in DCS research and how either side can be
                  why those choices were made and why some were emphasized                                          trustworthy. Table 1 summarizes these tensions; the
                  in published articles while others were not. More details on                                      subsections below elaborate on the tensions and motivate the
                  this review and on the interviews are available in the                                            framework that follows in the next section.
                  transparency materials.

                      Table 1. Trustworthiness Tensions in DCS Research
                      Tension                       Explanation                                                                                     Salience in DCS research

                      Data work:                    Objectivity can foster trustworthiness because it constrains                                    DCS tools are often used on
                      Prioritizing                  researchers’ discretion, so surfaced patterns can be attributable                               unstructured textual data; sampling
                      objectivity versus            to the data, and the path from corpus to model can be auditable                                 and preparation tasks (e.g.,
                      customization                 via concise, standard descriptions.                                                             tokenization, removal of stopwords,
                                                                                                                                                    lemmatization or stemming,
                                                    Customization can foster trustworthiness because it enables                                     constructing n-grams, weighting)
                                                    giving voice to the data, and thereby the phenomenon under                                      are more complex and
                                                    study, and helps to explicate rare expressions that might                                       substantively shape downstream
                                                    otherwise be missed, improving semantic fidelity and producing                                  categories and dimensions.
                                                    interpretable categories supported by snippets from the data.

                      Model building:               Stability can foster trustworthiness because researchers can                                    DCS tools can be sensitive to
                      Seeking stability             claim that patterns survive reasonable perturbations and                                        different choices made during data
                      versus variance               demonstrate targeted sensitivity checks with focused evidence                                   work and model building; models
                                                    for evaluation.                                                                                 may change with seemingly minor
                                                                                                                                                    changes and slight parameter
                                                    Variance can foster trustworthiness because researchers can                                     tuning; running the same algorithm
                                                    leverage sensitivity as a signal to surface informative                                         with the same configurations may
                                                    alternatives and document what iterations taught about the                                      still differ because the models may
                                                    phenomenon with concrete examples from raw data.                                                represent locally optimal solutions.

                      Validation:                   Benchmarking against ground truth can foster trustworthiness                                    There is often a lack of ground
                      Benchmarking                  by validating the extent to which labels and subsequent patterns                                truth in DCS research, and DCS
                      against ground                represent the reality of the world represented by the data,                                     tools are unsupervised, opaque,
                      truth versus                  including through independent labeling and intercoder reliability                               and unstable; establishing
                      accounting for                or comparison to accepted theoretical frameworks, established                                   contribution and rigor hinges on
                      interpretations               methods, accepted metrics, or industry benchmarks.                                              how models are validated.
                                                    Accounting for interpretations can foster trustworthiness by
                                                    showing that the interpretations by the researcher make sense
                                                    and can be explained, treating surfaced categories as first-order
                                                    codes, explaining coding procedures, visualizing data
                                                    structures, and moving back and forth between model results
                                                    and the original data to assess fit.




                  4
                    We conducted the methodological review and author interviews as part of a                       purpose of this study, our focus is limited to only those studies where researchers
                  bigger project; hence, our review and interviews included researchers employing                   employed DCS tools interpretively for constructing theories, i.e., studies within
                  and designing DCS tools for constructing as well as testing theories. For the                     the CTC community.




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026             855



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 6 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Data Work: Prioritizing                                   Objectivity               vs.           On the other hand, we also learned that some DCS
                  Customization                                                                                     researchers choose customization in their data work as a path
                                                                                                                    to trustworthiness because they want to engage more closely
                  DCS researchers spend considerable time collecting and                                            with the data. While closer engagement with data may
                  preprocessing texts into a machine-readable format, an                                            introduce bias and perhaps make the results less objective, it
                  activity we refer to as data work. Unlike traditional statistical                                 does help researchers to justify their choices in relation to
                  analyses on structured data (e.g., regression), DCS work                                          the specific research context. For example, one interviewee
                  typically begins with unstructured texts, where guidance is                                       explained how their data preparation choices were based on
                  abstract. Researchers’ choices (e.g., sampling, filtering                                         an understanding of the data and the context:
                  words, and normalizing) materially shape the categories and
                  dimensions that are later surfaced. This is because                                                    It’s a choice informed by how you understand the
                  “seemingly minor changes such as preprocessing or changes                                              phenomenon, how you understand the data. I think
                  in the underlying data” may change the model outputs                                                   this [bias-free] picture is, from my perspective, a bit
                  (Grimmer et al., 2022, p. 227). The core tension is whether                                            naive; it’s just a choice that you make, and what I see
                  to foster trustworthiness by aiming for objectivity—                                                   as my duty as a researcher is to make this choice
                  constraining discretionary preprocessing and relying on                                                transparent and available to the others for
                  standard rules and thresholds—or by pursuing                                                           assessment. (Interviewee 3)
                  customization—tailoring preprocessing to the phenomenon
                  to preserve semantic fidelity.                                                                    In making these choices, however, DCS researchers may
                                                                                                                    face challenges in predicting how choices influence model
                  On the one hand, some DCS researchers choose objectivity                                          outcomes, causing them to engage in creative
                  as a path to trustworthiness by limiting the amount of                                            experimentation rather than following rigorous templates.
                  processing they do, following commonly accepted data                                              For example, one interviewee explained how they iterated
                  preparation steps (e.g., only removing “common” stop                                              with different preprocessing steps to see how these choices
                  words), and utilizing computational metrics to objectify                                          influenced the emerging categories:
                  decisions related to data work (e.g., cutoff points based on
                  frequency). As explained by one interviewee, such practices                                            I spent a lot of time choosing which words to kick out
                  can facilitate objectivity while avoiding researcher biases.                                           and which words to keep in, trying to keep in as much
                                                                                                                         as possible, but running some different models to see
                        Of course, you can run different topic models with                                               what keeping a very common word might do. So, in
                        different sets of stop words. It’s something that I think                                        that preprocessing stage is where I think a lot of the
                        we have also done to some extent when running those                                              choices I make—and it’s hard to say that there’s like
                        different topic models. But ... we rather didn’t include                                         a hard and fast rule on this right. I think this is where
                        too many [or] didn’t exclude too many words so that                                              we make lots of choices as researchers in our studies.
                        we did not have a bias in the results. (Interviewee 1)                                           (Interviewee 2)

                  Scholars also minimize upfront data preprocessing and                                             Overall, DCS researchers are often torn between two
                  prefer to remove non-meaningful categories only after                                             competing approaches to fostering trustworthiness in their
                  having built the model, thereby “letting the data speak for                                       data work: either through the path of objectivity or through
                  themselves,” as several interviewees explained. Again, the                                        customization. Both approaches are valid. Objectivity
                  belief is that by minimizing researcher intervention and                                          facilitates trustworthiness because it constrains the
                  therefore bias, results become more objective. For example,                                       researchers’ discretion; hence, surfaced patterns can be
                  one interviewee explained how reviewers questioned the                                            attributed to the data (conduct), and researchers can thus
                  objectivity of the results:                                                                       make the path from corpus to model auditable via concise,
                                                                                                                    standard descriptions (disclosure). At the same time,
                        We were addressing this potential concern of “we                                            customization also facilitates trustworthiness because it
                        weren’t being objective as researchers,” which is                                           allows for explicating rare expressions in data that might
                        kind of like a hard thing to hear, right, like your                                         otherwise be missed, improving semantic fidelity (conduct)
                        reviewers are essentially challenging your integrity,                                       and producing interpretable categories supported by snippets
                        like, “you lied to us in your initial submission.”                                          from the data (disclosure). Absent guidance, authors struggle
                        (Interviewee 2)                                                                             in deciding which path to prefer and how to convincingly
                                                                                                                    report their choices.




                   856       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 7 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Model Building: Seeking Stability vs. Variance                                                    was only minimally reported on in the documents that they
                                                                                                                    were analyzing but was potentially relevant for improving
                  DCS researchers face a central dilemma in model building:                                         the understanding of their specific phenomenon. These
                  seeking stability versus variance. Again, this challenge is                                       models and results were not considered stable enough, as
                  prominent in DCS research because model outputs tend to                                           using alternative configurations would make the specific
                  be very sensitive to the choices of algorithms and parameter                                      category disappear. But this example illustrates how
                  tuning (Belford et al., 2018; Grimmer et al., 2022). Given                                        experimenting with different configurations can enable
                  this sensitivity, deciding whether to foreground robustness                                       researchers to explore alternative explanations and
                  checks or use variability as an exploratory probe is, in itself,                                  categorizations, some of which might be insightful. Another
                  a consequential choice for fostering trustworthiness.                                             interviewee highlighted how it is then up to the researcher to
                                                                                                                    interpret the explanatory value of alternative models and
                  DCS researchers may pursue stability in model building                                            reflect on their choices:
                  because they may conceive sensitivity as a bug that needs
                  fixing (Schooler, 2014), and doing so creates a path to                                                To convince me also as a reviewer, people should, for
                  trustworthiness. Thus, researchers may actively ascertain                                              example, mention that they did some iterations, you
                  how the choices they make in building their models                                                     know, that they did not just use the first topic model
                  influence the model output through performing sensitivity                                              that the algorithm gave them. And actually, if they
                  tests. Examples of sensitivity analyses include varying                                                report about some challenges that they experienced
                  parameter values or weighting schemes (e.g., Haans, 2019;                                              while doing it, I would trust them more than if they
                  Lowry et al., 2013), using left-out samples or different data                                          just left out the challenges. (Interviewee 1)
                  sources (e.g., Geva et al., 2019; Gong et al., 2018), changing
                  the modeling algorithms (e.g., Bao & Datta, 2014; Larsen &                                        Overall, sensitivity appears to be a double-edged sword for
                  Bong, 2016), or running the same model with multiple                                              DCS researchers. Stability fosters trustworthiness by
                  random seeds (Belford et al., 2018). Performing such                                              demonstrating robustness (conduct) and presenting focused
                  sensitivity tests allows researchers to claim that their model                                    sensitivity evidence (disclosure). Variance fosters
                  output is not sensitive to specific choices they made in                                          trustworthiness by using perturbations to explore alternative
                  building the model. Following this standard practice, DCS                                         explanations (conduct) and documenting interpretive
                  researchers also increasingly rely on and report sensitivity                                      iterations with concrete text-level examples (disclosure).
                  analyses to demonstrate that the model and the results are                                        Due to the lack of guidance specific to DCS research,
                  stable across choices that have been made in the different                                        scholars tend to be conflicted in deciding which path to
                  research phases. This rationale reflects the thoughts of                                          trustworthiness they should choose.
                  several interviewees, as expressed in the following quote:

                        And usually what we do is ... we try [to see] how                                           Validation: Benchmarking Against Ground
                        sensitive this choice is. We can’t always do this for                                       Truth vs. Accounting for Interpretations
                        all the parameters, of course. But as often as we can,
                        this is what we try to do and to see whether, how                                           Establishing validity is one of the most important aspects of
                        much this parameter weighs in shaping the results.                                          DCS research, given the unsupervised approaches to model
                        (Interviewee 3)                                                                             building: “the primary justification for using text analysis
                                                                                                                    methods is empirical” (Grimmer et al., 2022, p. 30).
                  DCS tools are not only sensitive to choices but are also                                          Accordingly, establishing a theoretical contribution
                  inherently sensitive, because running the same algorithm                                          becomes very much a question of fostering trustworthiness
                  using the same configurations on the same data could lead to                                      in how the models, through which the patterns are surfaced,
                  different results (Belford et al., 2018; Grimmer et al., 2022).                                   are validated. DCS researchers need to make a choice in
                  In response, scholars have responded by developing more                                           terms of what kind of validation practices to prioritize
                  stable tools—such as Yang and Subramanyam’s (2023)                                                (DiMaggio et al., 2013), where some practices are driven by
                  stable topic model—to mitigate instability that can produce                                       the pursuit of ground truth to benchmark against and others
                  inconsistent, irreproducible results.                                                             by the pursuit of researchers’ interpretations to account for.

                  Alternatively, a model’s sensitivity may also help in                                             Many DCS researchers demonstrate the internal validity of
                  demonstrating trustworthiness, as opposed to pointing to a                                        their models by focusing on how well the model captures
                  bug. For example, one interviewee explained how, while                                            distinct categories or dimensions and to what extent the
                  experimenting with different configurations, some                                                 researcher’s interpretation is fitting. Researchers typically
                  intermediate models enabled them to capture an event that                                         examine the surfaced categories based on the top words and



                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   857



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 8 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  assign a label to each category in an attempt to validate the                                     procedures and visualizing clear data structures. For
                  usefulness of categories in identifying distinct concepts: “I                                     example, one interviewee noted how trustworthiness
                  think a common practice across all topic modeling work is                                         expectations in some CTC studies may be similar to those in
                  coming up with labels for topics” (Interviewee 4). When                                           qualitative studies:
                  driven by the pursuit of ground truth, researchers tend to
                  focus on validating the extent to which those labels and                                               I would tend to think that a [qualitative research]
                  subsequent patterns actually represent the reality of the                                              paper that’s doing a grounded theory or a Gioia
                  phenomenon. They can do so in different ways. For example,                                             technique, you absolutely need to show your data
                  researchers may come up with labels independently and                                                  structure. But you know, if you think about [example
                  subsequently compare them to minimize subjectivity. The                                                DCS paper], you know their first-order codes were
                  idea is that minimizing interpretative variety aids in                                                 topics. (Interviewee 4)
                  facilitating trustworthiness by identifying patterns that can
                  be considered a form of ground truth. For example, one                                                 If you’re just doing a study where you’re isolating
                  interviewee explained how they were pushed by reviewers                                                one topic, then you know it is helpful to the reader to
                  to consider intercoder reliability:                                                                    at least have an appendix to get a sense of what the
                                                                                                                         other topics were, so that they could potentially
                        ... this definitely came from reviewers. They wanted                                             argue with your selection of that topic versus
                        us to confirm this [our interpretation]. This was not                                            another. (Interviewee 4)
                        our idea. ... And I can see why they wanted this
                        because, indeed, there can be a lot of, you know,                                           The challenge for DCS researchers then is that it may not
                        subjectivity in it. (Interviewee 5)                                                         always be clear why or how patterns surface as a result of
                                                                                                                    applying certain algorithms and whether the researcher’s
                  Another validation approach in the pursuit of ground truth is                                     interpretations actually align with the assumptions built into
                  to compare model output with accepted theoretical                                                 those algorithms. As a consequence, DCS researchers may
                  frameworks and measures, as they have already been proven                                         find themselves constantly going back and forth between
                  and observed in similar studies. Similarly, researchers may                                       model results and the original, underlying data. For example,
                  compare their results to those of studies that apply more                                         one interviewee argued that it is crucial to make sure that the
                  established methods or accepted metrics, or to industry                                           interpretation of topics aligns with what is present in the data:
                  benchmarks. Such external validation practices help to
                  illustrate that emerging patterns represent some ground truth.                                         Assuming you’re not just like throwing an algorithm
                  However, interviewees also acknowledged that these forms                                               at something, you still have to be very careful with
                  of validation may be very difficult in the case of DCS tools,                                          how you’re choosing your topics and how you’re
                  due to their unsupervised nature and the inherent lack of                                              validating your model and going back to your text
                  ground truth:                                                                                          data. ... How does it map? Does it make sense? And
                                                                                                                         then once you do those checks, which is still
                        We kind of used the deductive approach. So now we                                                considerable work, it acts as another point to
                        had a theory and tried to map topics to this theory,                                             validate. (Interviewee 2)
                        but then you have kind of a contradiction, actually,
                        right? Because topic modeling is unsupervised and                                           Thus, both benchmarking against ground truth and
                        inductive, and [the approach is deductive]. You see                                         accounting for interpretations can ground validity and
                        what I’m talking about. And that’s difficult to resolve,                                    thereby foster trustworthiness while justifying different
                        right? (Interviewee 1)                                                                      kinds of claims and evidence. Absent guidance, authors
                                                                                                                    sometimes try to do everything, combining approaches that
                  Thus, DCS researchers may also lean towards fostering                                             pull in opposite directions and leaving DCS researchers,
                  trustworthiness through accounting for their interpretations.                                     reviewers, and editors unsure which evidentiary logic should
                  The focus in this case is less on showing that patterns reflect                                   carry the most weight.
                  some ground truth than on showing that the interpretations
                  by the researcher make sense and that the researcher can
                  explain the interpretations. Oftentimes, researchers treat                                        Synthesis of Tensions
                  categories resulting from their models as something akin to
                  first-order codes in grounded theorizing and ultimately                                           A key thread that runs across data work, model building, and
                  exclude or combine categories under more general second-                                          validation is that DCS research cannot follow a generic
                  order or aggregate themes. In such cases, researchers strive                                      approach in fostering trustworthiness. This is because DCS
                  to demonstrate trustworthiness by explaining their coding                                         research blurs the boundaries between quantitative (including



                   858       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 9 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  computational) and qualitative approaches; however, it is                                         expectations for burden of proof and minimum disclosures.
                  neither qualitative nor quantitative nor even a mixed method                                      The first choice concerns whether DCS researchers give
                  (Berente et al., 2019; Lindberg, 2020). As one of our                                             primacy to either theoretical lexicons (i.e., starting with theory)
                  interviewees explained: “I feel that’s the risk of using [DCS                                     or practice lexicons (i.e., starting with the phenomenon),
                  tools], which you can use in both qual and quant. And if you                                      creating two pathways of DCS work. The second choice
                  then don’t get people [in the review process] who are open-                                       concerns whether the content of texts (i.e., meaning-bearing
                  minded to something that’s not either perfectly qual or                                           distinctions) or the structure of the corpus (i.e., attributes of the
                  perfectly quant, ... as I’ve experienced, this can be really                                      text corpus) carries the theoretical load. In our framework
                  tough” (Interviewee 6). Prioritizing objective versus                                             below (see Figure 1), we organize expectations for conduct and
                  customized preprocessing in data work, seeking stability                                          disclosure across the three phases discussed in Table 1.
                  versus variance in model building, and benchmarking against
                  ground truth versus accounting for interpretations in
                                                                                                                    We use select DCS studies from IS, management, and
                  validation can each foster trustworthiness, but for different
                                                                                                                    organizational research—including Hacker et al. (2020),
                  reasons. These tensions motivate our framework, which
                  specifies how research objectives can inform those reasons.                                       Hannigan et al. (2022), Karanović et al. (2021), Croidieu and
                                                                                                                    Kim (2018), Giorgi et al. (2019), and Miranda et al. (2022b)—
                                                                                                                    as illustrative examples to explain our framework. Table 2
                                                                                                                    summarizes the trustworthiness moves by these studies. The
                  A Framework for Fostering Trustworthiness                                                         first column locates each study within the two dimensions of
                  in DCS Research                                                                                   our framework, the second column documents how the study
                                                                                                                    uses DCS tools to explicate the focal phenomenon, the third
                  We propose a framework to help DCS researchers navigate                                           column summarizes the trustworthiness moves the study
                  trustworthiness tensions. We clarify trustworthiness                                              performs well, and the final column highlights additional
                  expectations across two research design choices that set                                          trustworthiness moves that our framework would recommend.




                     Figure 1. Framework for Fostering Trustworthiness in DCS Research




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   859



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 10 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                    Table 2. Trustworthiness Moves in the Illustrative Studies
                    Exemplar study                                                                                                       Additional trustworthiness
                                                   Focal phenomenon                         Trustworthiness moves already
                    & design                                                                                                             moves recommended based on
                                                   and role of DCS tools                    done well by exemplar study
                    choices                                                                                                              framework

                    Hacker et al.                  Examine how web                          - Using affordance theory to script          - Justifying preparation steps by
                    (2020)                         conferencing systems                       sampling; Targeted cleaning while            more explicitly relating them to
                                                   (WCS) were used during                     preserving lexical detail to                 the theory of affordances and the
                    Primacy:                       COVID-19; use topic                        distinguish affordances.                     focus on semantic meaning.
                    Theoretical                    modeling on tweets to
                    lexicons                       surface topics                           - Choosing algorithms that have              - Treating parameters beyond the
                                                   interpreted as WCS                         proven to do well on tweets.                 number of topics and reporting
                    Focus:                                                                    Exploring alternative numbers of             and justifying them in relation to
                    Content of texts               affordances.
                                                                                              topics.                                      their ability to surface
                                                                                                                                           affordances.
                                                                                            - Facilitating face validity of topics
                                                                                              interpreted as affordances.                - Offering a theory-grounded
                                                                                                                                           rationale for dropped models and
                                                                                                                                           topics, showing that their
                                                                                                                                           exclusion does not undercut
                                                                                                                                           claims about WCS affordances.

                    Hannigan et al.                Map how culture                          - Using cultural theory to guide             - Specifying preprocessing beyond
                    (2022)                         manifests in an                            sampling focused on capturing                lemmatization and linking it
                                                   entrepreneurial                            ecosystem talk during a formative            explicitly to the structural mapping
                    Primacy:                       ecosystem; apply topic                     period. Preprocessing with the               aim.
                    Theoretical                    modeling to social-media                   aim to capture associations and
                    lexicons                       talk to analyze cultural                   trajectories.                              - Reporting parameter
                                                   patterns and trajectories.                                                              experimentation and showing
                    Focus:                                                                  - Choosing an algorithm more                   attribute invariance under
                    Structure of                                                              suited than default choice, for              reasonable perturbations.
                    corpus                                                                    documents with a small number
                                                                                              of words.                                  - Tying structural shifts more
                                                                                                                                           explicitly to recognizable field or
                                                                                            - Strengthening internal validity by           ecosystem episodes.
                                                                                              having observers independently
                                                                                              code topics and reconcile to
                                                                                              consensus.

                    Karanović et al.               Study how resource                       - Using resource dependence                  - Considering preprocessing steps
                    (2021)                         dependence conditions                      theory to anchor sampling                    beyond tool defaults, justifying
                                                   platform workers’                          choices and theory-driven                    them in terms of comparability vs
                    Primacy:                       responses across                           stratification.                              interpretability across cities and
                    Theoretical                    regulatory regimes; use                                                                 time.
                    lexicons                       topic modeling on forum                  - Choosing an algorithm enabling
                                                   posts to compare                           structural comparison, with city           - Treating parameters beyond the
                    Focus:                                                                    and date as prevalence                       number of topics and reporting
                    Structure of                   patterns across
                                                   cities/regimes.                            covariates so topic prevalence is            and justifying them depending on
                    corpus                                                                    directly tied to regulatory context.         their ability to surface structural
                                                                                                                                           resource differences.
                                                                                            - Assessing reliability of topic
                                                                                              interpretations by recruiting              - Emphasizing robustness of
                                                                                              independent coders. Bolstering               structural findings by showing
                                                                                              external validity through                    city/date effects and whether key
                                                                                              triangulation of multiple data               patterns persist across nearby
                                                                                              sources on workers’ responses                configurations.
                                                                                              across regulatory structures over
                                                                                              time.




                   860       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 11 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                    Croidieu and                   Trace how amateur and                    - Using phenomenon-driven                              - Making explicit how the
                    Kim (2018)                     lay expertise became                       sampling through dropping                              phenomenon motivated specific
                                                   legitimized in the                         peripheral material, relating                          preprocessing steps and
                    Primacy:                       amateur radio field; use                   different sources, and sequencing                      split/merge decisions.
                    Practice lexicons              topic modeling to surface                  episodes to track shifts in
                                                   and follow shifting                        amateur. Preprocessing focused                       - Building on topic stability checks
                    Focus:                                                                                                                           by reflecting on the revelatory
                    Content of texts               articulations of amateur.                  on retaining meaning.
                                                                                                                                                     value of excluded topics and why
                                                                                            - Choosing the algorithm that                            they were set aside.
                                                                                              addresses the polysemy of
                                                                                              “amateur” and has proven useful
                                                                                              for analyzing historic texts.
                                                                                              Exploring different configurations
                                                                                              of parameters and disclosing
                                                                                              choices leading to the final model.
                                                                                            - Designing and reporting on
                                                                                              coding procedure and visualizing
                                                                                              code structure. Providing quotes
                                                                                              to substantiate arguments and
                                                                                              enable interpretation.

                    Giorgi et al.                  Reconstruct how firms                    - Assembling a heterogeneous                           - Justifying preprocessing steps in
                    (2019)                         responded to the 1966                      corpus on firms’ responses to the                      relation to claims about safety
                                                   Automotive Safety Act;                     Safety Act to build a revelatory                       discourse rather than positioning
                    Primacy:                       use topic modeling to                      case grounded in practice.                             it as a “standard” procedure.
                    Practice lexicons              organize heterogeneous
                                                   safety-related materials.                - Choosing an algorithm that                           - Treating parameters beyond the
                    Focus:                                                                    addresses polysemy in historical                       number of topics and reporting
                    Content of texts                                                          contexts. Reporting on the                             and justifying them depending on
                                                                                              specific tool used. Exploring                          their ability to reconstruct firms’
                                                                                              alternative numbers of topics.                         responses.
                                                                                            - Triangulating qualitative and                        - Exploring if alternative choices
                                                                                              quantitative analysis. Designing a                     lead to alternative frames and
                                                                                              coding process based on                                assessing their explanatory value.
                                                                                              independent coding. Anchoring
                                                                                              topics in genre-specific texts with
                                                                                              quotes.

                    Miranda et al.                 Examine how field-level                  - Constructing a corpus of                             - Making lexicon provenance
                    (2022b)                        blockchain discourse                       blockchain discourse across                            explicit: clarify how they ensured
                                                   evolves in diversity and                   heterogeneous outlets and actors                       they did not miss any sources
                    Primacy:                       coherence; use topic                       through phenomenon-driven                              beyond the theory-informed
                    Practice lexicons              modeling and                               sampling. Data preparation                             sampling.
                    Focus:                         diversity/coherence                        focused on retaining meaning
                                                   measures on a field-level                  while improving structural                           - Highlighting the revelatory value
                    Structure of                                                                                                                     of the chosen model vis-à-vis
                    corpus                         corpus.                                    comparison.
                                                                                                                                                     alternatives.
                                                                                            - Using algorithms that support
                                                                                              surfacing meaning structures and
                                                                                              computing diversity/coherence
                                                                                              over time. Reporting on the tool
                                                                                              and specific parameter settings
                                                                                              leading to the final model.
                                                                                            - Supporting validation with
                                                                                              synchronic/diachronic visuals and
                                                                                              quotes.




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026    861



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 12 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Giving Primacy to Theoretical Lexicons                                                            between regulatory structures” (p. 6). Accordingly, they bound
                                                                                                                    observations by jurisdiction and time to capture variation
                  When researchers give primacy to theoretical lexicons, their                                      aligned with theorized dependencies. They also drew on prior
                  research questions are anchored in a prior theory, and the                                        work (e.g., Tzur, 2019) to justify the salience of regulation for
                  ensuing choices across phases are guided by what that theory                                      transport network companies and motivate forums as data
                  renders salient. The aim is to unpack how a particular                                            sources that have proven to be “valuable sources of insight into
                  theoretical lens illuminates a focal phenomenon (see Table 2):                                    workers’ experiences” (Karanović et al., 2021, p. 2). This helps
                  for example, how cultural theory can explain entrepreneurial                                      explain why they did not include venues and threads unrelated
                  ecosystems (Hannigan et al., 2022), how resource dependence                                       to ride-hailing work. In asking which WCS affordances were
                  theory can explain the gig economy (Karanović et al., 2021), or                                   actualized during COVID-19, Hacker et al. (2020) sampled
                  how affordance theory can explain the use of web-conferencing                                     tweets about WCS use. Affordance theory guided their data
                  systems (WCS) during the COVID-19 pandemic (Hacker et al.,                                        work, while they remained open to emergent themes.
                  2020). Yet this aim can be achieved by focusing either on the                                     Consistent with the theoretical focus on WCS affordances
                  content of texts or on the structure of the entire corpus. Hacker                                 during the crisis, they dropped off-topic chatter and bound the
                  et al. (2020) privileged content because category meanings bear                                   observation window to the crisis period. In each of these studies,
                  the theoretical load (i.e., categories representing affordances),                                 the guiding theory anchored the sampling frame and justified
                  whereas Karanović et al. (2021) and, to a large extent, Hannigan                                  early dropping, relating, and sequencing moves as part of
                  et al. (2022) privileged structure in their respective focus on                                   theory-driven data work.
                  distributions across regulatory contexts and associations and
                  trajectories in cultural discourse.                                                               Theory also steers data preparation as active categorization (see
                                                                                                                    Grodal et al., 2021). To an extent, this is visible in how scholars
                  In the following, we articulate how researchers can facilitate                                    prepare data in line with some agreed-upon standards and
                  trustworthiness when giving primacy to theoretical lexicons                                       practices associated with the chosen theory. In practice, this
                  through theory-driven data work, surfacing theoretically robust                                   entails various moves in processing data that dictate the
                  patterns, and validating patterns against existing theory. We                                     categories that will eventually surface, such as filtering non-
                  also explain how lexical alignment can be achieved through                                        substantive lexical material (e.g., stopwords, usernames/URLs,
                  iterative sensemaking.                                                                            numbers, punctuation), and normalizing lexical variants (e.g.,
                                                                                                                    lemmatization, synonym handling, and preserving salient n-
                                                                                                                    grams). For example, Hannigan et al. (2022) specified what tool
                  Theory-Driven Data Work                                                                           they used for lemmatizing tweets, and Hacker et al. (2020)
                                                                                                                    reported removing usernames, URLs, numbers, and
                  When DCS researchers give primacy to theoretical lexicons,                                        punctuation, applying bi-gram tokenization, extending stoplists
                  data work reflects a theory-driven orientation. Because other                                     with domain-uninformative terms, and lemmatizing. Across
                  studies may already have analyzed related phenomena under                                         these cases, the guiding theory shaped which preparation
                  similar theoretical framings, DCS researchers can use them as                                     choices were emphasized and why, and the authors explicitly
                  starting points for maneuvering theory-consistent data work                                       reported on theory-motivated steps so that readers could see
                  choices, beginning with sampling.                                                                 how early decisions set up downstream DCS work.

                  In theory-driven sampling, theory-anchored research questions                                     The initial research questions and theoretical orientation also
                  implicitly or explicitly script analytical moves in data work:                                    shape data work by clarifying whether category content is
                  dropping sources that do not speak to the theorized mechanism,                                    expected to carry the theoretical load or whether structure is
                  relating focal actors and contexts into a purposive sampling                                      central. When the study is content-focused, sampling
                  frame, and sequencing observations to align with expected                                         foregrounds texts that narrate concrete actions tied to focal
                  dynamics. For instance, in asking how culture manifests in an                                     constructs, and data preparation preserves semantic
                  entrepreneurial ecosystem, Hannigan et al. (2022) defined the                                     distinctiveness. For example, given that the theory of
                  unit of analysis as ecosystem members’ public talk (posts on                                      affordances is about how people use technology, Hacker et al.’s
                  Twitter, now X). They excluded non-ecosystem discourse and                                        (2020) data work centered on the content of texts. They applied
                  bound the observation window to the ecosystem’s formative                                         targeted cleaning (e.g., removing usernames) while retaining
                  period so that cultural fluctuations could be observed. In asking                                 the lexical material needed to differentiate affordance
                  how resource dependence conditions platform workers’                                              meanings. When the structure of the corpus is in focus—e.g.,
                  responses across regulatory regimes, Karanović et al. (2021)                                      the theory targets associations among categories or
                  defined strata by the city-level regulatory context and sample                                    documents—data work prioritizes the structural signal and
                  posts from uberpeople.net. They argued that platform “workers’                                    comparability. Researchers sample in a balanced manner across
                  responses to new organizing solutions are likely to vary                                          theory-implicated strata (e.g., cities, periods, roles) and capture



                   862       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 13 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  rich metadata to support later relating and sequencing.                                           around both decisions (algorithms and parameters) and what
                  Researchers may also stick to tool defaults to keep                                               would (or would not) change under nearby specifications. We
                  preprocessing uniform across strata (e.g., the same language                                      elaborate on these choices below.
                  filters and stop-word lists) (Karanović et al., 2021) and avoid
                  content-motivated pruning that differentially thins or                                            First, giving primacy to theoretical lexicons demands selecting
                  collapses groups or time periods.                                                                 algorithms and configuration norms from prior studies with
                                                                                                                    similar contexts, theories, and data so that results are
                  Using our framework, the illustrative studies’ choices in                                         comparable and knowledge can be accumulated. For example,
                  theory-driven data work can be complemented with certain                                          Hacker et al. (2020) used the MineMyText online tool, which
                  analytical moves and disclosures that strengthen                                                  relies on the latent Dirichlet allocation (LDA) (see Blei et al.,
                  trustworthiness. For instance, Hannigan et al. (2022) could                                       2003), because “it is well-researched from both the technical
                  have specified whether any preparation beyond lemmatization                                       and the application perspectives, [including] its use in analyzing
                  was undertaken and why, so that readers can see how
                                                                                                                    tweets” (p. 566). Yet, researchers still ought to be mindful of the
                  preprocessing aligns with their theoretical aims. Karanović et
                                                                                                                    underlying assumptions inscribed in those algorithms.
                  al. (2021) could have considered steps beyond tool defaults.
                                                                                                                    Trustworthiness is facilitated by carefully explaining how the
                  For example, they could have explicitly stated whether they
                  used stemming or lemmatization and justified that choice                                          chosen algorithms and underlying assumptions fit the research
                  given their aim of comparing structural variation across                                          context and considering potential deviations when the data and
                  regulatory contexts (where stronger normalization aids                                            theory require it. For example, Hannigan et al. (2022) explained
                  comparability but may reduce interpretability). All studies                                       why they rely on bi-term analysis instead of the standard LDA:
                  could have also reflected on what constitutes data and made                                       “When each document (i.e., a tweet, in our current case) has a
                  their decisions about data more explicit to their readers. For                                    small number of words, LDA is not optimal. The distribution of
                  this, DCS researchers can draw inspiration from some studies                                      topics across the documents was too sparse, making estimation
                  that use DCS tools to operationalize constructs. For instance,                                    of the LDA parameters for a document particularly difficult” (p.
                  Safadi et al.’s (2021) study on Stack Exchange is a useful case                                   7). Karanović et al. (2021) adopted the structural topic model
                  for theory-driven data work in clarifying what counts as data:                                    (STM) (see Roberts et al, 2014), so topic prevalence can be
                  They treated the contribution text as the data (one post—                                         related to city- and date-level metadata during estimation,
                  question, answer, or comment—constitutes a document) and                                          matching a resource-dependence argument about regulatory
                  explicitly rejected member-selected tags as content proxies                                       conditioning. These examples illustrate why researchers should
                  because tags appear only on questions, reflect author                                             explain the reason for choosing a specific algorithm for the
                  idiosyncrasies, vary by community, and can be auto-                                               intended purpose, explain the core assumptions that come with
                  suggested. Such clarifications are important for addressing the                                   that algorithm, and indicate how reasonable alternatives would
                  risk that the practices a given study follows are assumed to be                                   be expected to change (or not) the patterns central to the theory-
                  “best practices” even when they are not meant to be best                                          led questions.
                  practices by the authors who introduce them. To mitigate this
                  risk, we encourage researchers to disclose and justify                                            Second, parameters are the levers that enact active
                  preparation steps in relation to the specific theory they are                                     categorization. Parameter choices are not mere technicalities;
                  focusing on.
                                                                                                                    they are concrete means by which theory-driven research
                                                                                                                    questions are rendered into model behavior. Researchers can
                  Surfacing Theoretically Robust Patterns                                                           start near established defaults, then explore nearby settings to
                                                                                                                    select a configuration that is both theoretically meaningful and
                  After theory-driven data work, model building turns on two                                        empirically robust. For example, Hacker et al. (2020)
                  decisions: (1) the choice of algorithmic family and (2)                                           qualitatively compared models with 20, 30, 50, and 60 topics
                  parameter settings. The choice of the number of categories                                        and chose 50 because it improved differentiation without
                  governs splitting versus merging of categories, priors, and                                       adding empty complexity. While the other illustrative papers
                  regularization shape how sharply categories are expressed,                                        also experimented with the number of topics, they could have
                  initialization and random seeds test whether salient patterns                                     explained how this may have influenced the patterns observed
                  reappear, and assignment thresholds or prevalence cutoffs                                         and if this also led to patterns that could not be explained with
                  implement disciplined dropping of borderline memberships                                          the help of the existing theory.
                  that would otherwise blur patterns. Through these choices,
                  researchers identify patterns that are analytically robust and                                    When the study is content-focused, researchers can choose
                  interpretively meaningful for the chosen theory.                                                  settings that enable more precise category splitting, with
                  Trustworthiness rests on showing reasonable alternatives                                          robustness centering on whether content labels persist under




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   863



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 14 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  nearby choices of number of categories, priors, or seeds. By                                      reconciliation. For example, in Hannigan et al. (2022), three
                  contrast, when a structural attribute carries the theoretical load,                               observers independently coded topics and resolved differences
                  researchers can favor algorithms and parameter settings that                                      based on consensus.
                  emphasize relating categories and documents to covariates and
                  sequencing them over time or interaction (e.g., STM to relate                                     Face validity is necessary but not sufficient, especially when the
                  prevalence to city/date). Researchers in such cases should be                                     focus is on the content of texts. In this case, authors can show
                  cautious about how parameterization affects prevalence or co-                                     label persistence and exemplar stability under a varying number
                  occurrence in the structure of the corpus. In short, in terms of                                  of categories, seeds/initializations, and priors. Internal
                  fostering trustworthiness, theory-led questions determine                                         validation can also make explicit the active categorization at
                  whether model building primarily entails analytical moves to                                      stake: how labels reflect splitting/merging decisions, what (if
                  refine meanings (focus on content) or to preserve and                                             anything) is dropped as noise, and how categories are related.
                  interrogate attributes (focus on structure).                                                      Such computational-interpretive triangulation and robustness
                                                                                                                    testing can clarify how far theory-led interpretations travel and
                  Viewed through our framework, the illustrative studies could                                      support cumulative knowledge. When the theory targets a
                  have experimented (and disclosed experimentation) with                                            structural attribute, face validity can be paired with checks to
                  parameter configurations beyond the most obvious ones. For                                        confirm that structural metrics are invariant to reasonable
                  instance, in the case of topic modeling, in addition to the                                       perturbations and denominator integrity is preserved.
                  number of topics, concentration priors (α, β) materially shape
                  granularity and sparsity, and should be reported and justified to                                 Second, external validation of DCS output under the primacy of
                  enable knowledge accumulation. DCS researchers giving                                             theoretical lexicons strengthens the claim that theory-led
                  primacy to theoretical lexicons could clearly link their                                          interpretations travel beyond the modeling setup. One route is
                  justification to the theory that guides their analysis. For                                       triangulation with independent data or methods. For example,
                  example, in the case of Hacker et al. (2020), had they chosen a                                   Karanović et al. (2021) triangulated different data sources “to
                  lower value for β, they may have uncovered more fine-grained                                      compare workers’ responses under different regulatory
                  topics that they could then have interpreted through an                                           structures and analyse these responses over time” (p. 2). In a
                  affordances lens. Similarly, Karanović et al. (2021) could have                                   similar spirit, studies can complement model outputs with
                  reported that the direction and magnitude of city/date effects on                                 category-sequencing and event anchoring—showing that local
                  topic prevalence persisted across nearby configurations. Thus,                                    discourse reacts to field-level developments (e.g., salient AI
                  DCS researchers can draw inspiration from scholars who use                                        milestones or policy shifts) in theoretically coherent ways.
                  DCS tools for measuring deductively developed constructs,                                         Following our framework, Hannigan et al. (2022) could have
                  e.g., how Kaplan and Vakili (2015) considered different values                                    made this link explicit by demonstrating that the model’s
                  of β, and how Mousavi and Gu (2024) experimented with                                             cultural associations co-moved with recognizable inflection
                  different algorithms, including BERT, LSTM, and a dictionary                                      points in the broader AI landscape.
                  method, before settling for a fine-tuned BERT for the rest of
                  their analysis. These analytical moves (conduct and disclosure)                                   The other route is construct alignment: comparing surfaced
                  help other researchers to interpret parameters in studies relying                                 categories and dimensions to preexisting theoretical
                  on similar theories, thereby fostering trustworthiness.                                           frameworks or taxonomies to assess convergent/discriminant
                                                                                                                    validity and the value-add of DCS (e.g., new subcategories or
                                                                                                                    clearer boundaries). For example, after completing a literature
                  Validating Patterns Against Existing Theory
                                                                                                                    review and under the guidance of the theory of technology
                                                                                                                    affordances in organizations, Hacker et al. (2020) decided to
                  After surfacing patterns through model building, researchers
                                                                                                                    drop topics that were difficult to interpret or did not align with
                  need to validate the emergent patterns against the chosen
                                                                                                                    the chosen theoretical framework. When such dropping occurs,
                  theories. Validation rests on two pillars: internal and external
                                                                                                                    authors can justify it in theoretical terms and show that it does
                  validity. First, internal validity under the primacy of theoretical
                                                                                                                    not undercut the claims they make later.
                  lexicons establishes that the category system faithfully
                  instantiates the guiding theoretical constructs (or their theory-
                  relevant attributes) and that the resulting patterns are not merely                               Lexical Alignment Through Iterative Sensemaking
                  artifacts of modeling choices. A first step is face validity—Do
                  outputs look reasonable in the language of the theory? This                                       So far, we have explained how researchers employing DCS
                  typically includes visualizing categories (top words and top                                      tools in constructing theories with primacy given to theoretical
                  documents) with provisional, theory-anchored labels.                                              lexicons can continue to maintain proximity to theoretical
                  Intersubjective interpretability can be strengthened with                                         lexicons within each research phase. But we have also argued
                  multiple coders using a brief, theory-informed codebook and                                       that researchers align their theoretical and practice lexicons




                   864       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 15 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  across phases iteratively. These iterations can render theory-                                    topic modeling to a wide range of materials on firms’
                  led questions analytically tractable. Our framework asks                                          responses to the 1966 Automotive Safety Act to assemble a
                  authors to report a concise iteration trace: (1) the theoretical                                  “revelatory case in which the processes of theoretical interest
                  motivation for returning to an earlier phase, (2) the specific                                    were ‘transparently observable’ and could be thoroughly
                  move enacted (e.g., added domain stopwords; changed                                               reconstructed” (p. 807). Likewise, Miranda et al. (2022b)
                  number of categories/priors), (3) the observed effect on                                          constructed a field-level corpus to study discursive dynamics,
                  content (labels/exemplars) or structure (prevalence/                                              relating heterogeneous outlets and voices that constitute the
                  associations/ trajectories), and (4) why the post-iteration state                                 arena and sequencing materials over periods salient to field
                  better instantiates the theory. Making these cycles explicit                                      evolution. In each case, the phenomenon anchors the sampling
                  shows not only where the analysis lands but also                                                  frame and justifies these early moves as part of phenomenon-
                  demonstrates, step by step, how theory and practice lexicons                                      driven data work.
                  are brought into correspondence.
                                                                                                                    Data preparation and preprocessing are acts of sensemaking
                                                                                                                    rather than applications of standards. In this pathway, active
                  Giving Primacy to Practice Lexicons                                                               categorization involves a set of ex ante moves—relating,
                                                                                                                    sequencing, and merging—that renders practice-rooted
                  An alternative research design choice in DCS research is                                          distinctions legible before any modeling. Because theoretical
                  giving primacy to practice lexicons. When researchers give                                        lexicons have not yet been stabilized, preparation emphasizes
                  primacy to practice lexicons, their research questions are                                        preserving lexical richness while documenting the micro-
                  anchored in a focal phenomenon and the vocabularies through                                       moves that shape what can eventually be surfaced. What
                  which actors themselves make it intelligible. The ensuing                                         counts as noise versus meaningful data is grounded in the
                  choices across phases are guided by what the phenomenon’s                                         researchers’ understanding of the phenomenon, which guides
                  vernacular renders salient. The aim is to surface meanings and                                    dropping and merging decisions. In Croidieu and Kim (2018,
                  mechanisms inherent in practice and only subsequently                                             Appendix p. 1), tracing the meaning of the word “amateur”
                  stabilize them in dialogue with theory (see Table 2): for                                         implies keeping local context windows, identifying field
                  example, how amateurs’ discourse comes to be recognized as                                        actors to relate voices across episodes, and omitting “words
                  lay expertise in an emerging field (Croidieu & Kim, 2018),                                        considered to be non-meaningful.” In Miranda et al. (2022b),
                  how firms and other actors reshape the cultural terms through                                     field-level discourse dynamics required retaining semantic
                  which legal issues are debated (Giorgi et al., 2019), or how                                      units in the form of bi-grams and performing lemmatization,
                  blockchain discourse becomes simultaneously diverse and                                           while also sequencing stable time bins so that the later
                  coherent across multiple discursive fields (Miranda et al.,                                       diversity and coherence measures were comparable. Our
                  2022b). However, this aim can be achieved by focusing either                                      recommendation is to treat these choices as provisional
                  on the content of texts or on the structure of the corpus. In the                                 knowledge claims about the phenomenon: Document each
                  following, we articulate how DCS researchers giving primacy                                       action (what was dropped or kept, how synonyms were
                  to practice lexicons can foster trustworthiness through                                           merged, which metadata were related, how periods were
                  phenomenon-driven data work—surfacing empirically                                                 sequenced), revisit after an initial rendering, and justify
                  revelatory patterns and validating novel theoretical patterns—                                    adjustments in terms of how they clarify the phenomenon
                  followed by an explanation of lexical alignment through                                           under study.
                  iterative sensemaking.
                                                                                                                    When content is central—as in Croidieu and Kim (2018) on
                                                                                                                    the shifting senses of amateur and, to a large extent, Giorgi et
                  Phenomenon-Driven Data Work                                                                       al. (2019) on safety discourse—DCS researchers engage in
                                                                                                                    sampling that foregrounds texts that narrate concrete
                  When DCS researchers give primacy to practice lexicons,                                           meaning-bearing practices and discourses, and in
                  their data work ought to be phenomenon driven. Researchers                                        preprocessing that preserves semantic meaning so subsequent
                  sample the corpus by iteratively unpacking the focal                                              category splitting and judicious merging are possible. When
                  phenomenon: They select sources that speak to the                                                 structure is central—as in Miranda et al. (2022b), where
                  phenomenon under study and relate actors, venues, and arenas                                      diversity, coherence, or related field attributes do the
                  into a purposive frame that captures its contours. For instance,                                  explanatory work—data work protects structural signal and
                  Croidieu and Kim (2018) built a historical, multi-actor archive                                   comparability. In such cases, DCS researchers relate outlets,
                  around the rise of amateur radio, relating regulators,                                            periods, and actor types via rich metadata, put sequence
                  associations, and media to situate the practice in its field, and                                 observations in revelatory bins aligned with field episodes,
                  sequencing documents across key episodes to observe shifts                                        and apply cleaning so that structural measures reflect the
                  in how “amateur” was articulated. Giorgi et al. (2019) applied                                    arena. Across both aims, the phenomenon anchors which



                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   865



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 16 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  moves are appropriate.                                                                            demonstrate this with concrete examples to foster
                                                                                                                    trustworthiness.
                  Using our framework, the illustrative studies could have
                  enhanced trustworthiness by tweaking some analytical                                              Second, parameterization here means theorizing by
                  moves. For instance, Giorgi et al. (2019) noted that they                                         rendering. Hence, the final model may be chosen based on
                  “followed a standard procedure” (p. 824), citing Croidieu                                         the meaningfulness of categories, dimensions, and their
                  and Kim (2018). Yet the two studies confront different                                            relationships for capturing the phenomenon of interest.
                  corpora, genres, and phenomena, so a shared “standard”                                            Researchers begin with sensible defaults, but in this case,
                  risks obscuring phenomenon-specific needs. Our framework                                          probe nearby specifications to see which rendition most
                  suggests that studies that give primacy to practice lexicons                                      clearly exposes the phenomenon. For example, Giorgi et al.
                  should treat preprocessing as provisional theorizing and                                          (2019) started from a default value, as recommended by the
                  document it as such. Concretely, Croidieu and Kim (2018)                                          tool, and proceeded to rely on metrics to find an optimal
                  could have made explicit whether their historical context and                                     range of topics. Their final choice was, however, based on
                  polysemy of words warranted their decision to stem words,                                         manual inspection of the surfaced topics. This shows how
                                                                                                                    computational metrics might be helpful to determine an
                  or if lemmatizing would have been more applicable, given
                                                                                                                    adequate range of values for parameters, but the final choice
                  their focus on content and interpretation as well. Giorgi et al.
                                                                                                                    is informed by the researchers’ interpretation. This is
                  (2019) could have leveraged and justified context-aware
                                                                                                                    important because models that score well on computational
                  stoplists, showing how these moves clarified safety                                               metrics may not always be interpretable, and vice versa
                  discourse and demonstrating that preprocessing did not                                            (Chang et al., 2009). This is also evident in how Miranda et
                  undermine dissenting voices. Miranda et al. (2022b) already                                       al. (2022b) explained their choice of parameters through a
                  documented preprocessing and sampling in depth; one                                               sequence of steps. For instance, in explaining their choice
                  further step could have clarified how they ensured that                                           among alternative models, they explained why they selected
                  relevant discursive strands outside of their theory-informed                                      “a 23-topics model spanning four thematic quadrants” (p.
                  sampling were not missed. Overall, researchers operating                                          1425), elaborating why they did not just follow “fit metrics
                  close to practice lexicons can foster trustworthiness by                                          such as log-likelihood and perplexity” (p. 1446).
                  reflecting on how choices help them understand the                                                Additionally, they utilized multidimensional scaling that
                  phenomenon and describing the iterative sense-making                                              enabled abductive sensemaking to foster trustworthiness.
                  through which these choices are refined so that they avoid
                  taking “standards” for granted.                                                                   Again, the focus on content versus structure matters in
                                                                                                                    modeling choices. When content is central, researchers should
                                                                                                                    choose models and settings that expose fine-grained meanings
                  Surfacing Empirically Revelatory Patterns                                                         (e.g., a higher number of categories when warranted, tighter
                                                                                                                    word-in-topic priors), preserve informative phrases and local
                  When researchers give primacy to the practice lexicons, after                                     context, and apply conservative normalization so that verbs,
                  phenomenon-driven data work, model building aims to                                               objects, and named entities remain legible. When structural
                  surface revelatory patterns—those that open new concepts or                                       attributes carry the theoretical claim, researchers should favor
                  mechanisms and remain credible under reasonable                                                   representations that explicate association structure and
                  perturbations. Again, two central decisions include                                               comparability across sources and demonstrate attribute
                  algorithms and parameters. First, the choice of algorithmic                                       revelatory potential. Researchers should pick the specification
                  family functions as a lens to give voice to the phenomenon.                                       that allows for the most revelatory ordering, dispersion, and
                  For instance, Croidieu and Kim (2018) chose LDA because                                           trajectory patterns among alternatives.
                  it distinguishes cases in which a word’s meaning shifts by
                  context, thus allowing for capturing polysemy. Giorgi et al.                                      Accordingly, studies giving primacy to practice lexicons
                  (2019) implemented LDA to render an interpretable                                                 report alternatives to illuminate revelatory variance rather
                  discursive architecture and because it enables capturing                                          than merely to confirm stability. For example, Croidieu and
                  polysemy. Miranda et al. (2022b) explained that they                                              Kim (2018) were aware of the sensitivity of the algorithm
                  followed their choice of using LDA to render topics with                                          and tested topic stability across multiple runs. While they
                  “multidimensional scaling (MDS), which surfaces                                                   aimed to demonstrate stability, our framework invites
                  underlying meaning structures by positioning related topics                                       reflection on the revelatory value of excluded models and
                  next to each other in two-dimensional space” (p. 1425). Our                                       topics as well. In this spirit, DCS researchers can draw
                  guidance here is that researchers should choose the family of                                     inspiration from Sidorova et al. (2008), who utilized LSA to
                  algorithms that makes the phenomenon legible and should                                           discover the intellectual core of the IS discipline. Although
                                                                                                                    their goal was not necessarily to construct a theory, their



                   866       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 17 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  analytical moves are inspirational in how they surfaced                                           interpretations of those patterns and their importance. To this
                  revelatory patterns. While they applied LSA on abstracts                                          end, visualizations are often supported by examples from the
                  from articles published in IS journals, they tested models                                        data in the form of raw quotes. When the focus is on the content,
                  with different numbers of factors, not to show stability per                                      these quotes directly demonstrate the theorized categories. For
                  se, but to enable more detailed analyses and theorizing. This                                     instance, to validate their claims Croidieu and Kim (2018)
                  illustrates reflexivity when it comes to interpreting different                                   provided several quotes from their raw data, thereby enabling
                  varieties of models while still acknowledging that varieties                                      readers to assess their interpretations of emerging categories.
                  exist and reporting on them.                                                                      Alternatively, when the focus is on the structure of the text,
                                                                                                                    direct quotes can demonstrate structural similarities or
                  Because interpretations and decisions during model building                                       differences. Miranda et al. (2022b) explicitly compared two
                  are driven by the researchers’ understanding of the                                               illustrative data excerpts from two actors: a journalist for the
                  phenomenon, this often also requires extensive domain                                             Financial Times and an IBM blockchain business development
                  expertise. Researchers giving primacy to practice lexicons are                                    leader and social influencer, to compare the frames these actors
                  therefore more likely to complement the use of DCS tools with                                     used in their discourse on blockchain. Such reflection is
                  fieldwork or collaborate with domain experts. For example,                                        especially important for studies giving primacy to practice
                  Giorgi et al. (2019) relied on a strategy “that featured a                                        lexicons because these diverse interpretations are potentially
                  triangulation of qualitative and quantitative analyses (a                                         theoretically novel. Researchers need to convince readers that
                  historical case study coupled with computational quantitative                                     emerging categories or dimensions are indicative of a new
                  text analysis) to develop grounded theorizing” (p. 808). To                                       theoretical concept.
                  facilitate trustworthiness, researchers can report on not only
                  how different approaches complement each other (as in a                                           Second, while the main focus for researchers giving primacy to
                  mixed methods study) but also how the research design shapes                                      practice lexicons may be on internal validity, there are still ways
                  the use of DCS tools.                                                                             in which they can also illustrate external validity. One route is
                                                                                                                    category sequencing with event anchoring—linking shifts in
                                                                                                                    categories or attributes to recognizable field episodes (e.g.,
                  Validating Novel Theoretical Patterns
                                                                                                                    regulatory actions, product launches, scandals). A second route is
                                                                                                                    to compare emerging patterns with existing measures, patterns,
                  After rendering an initial model under the primacy of practice                                    or trends associated with the phenomenon. For example, Croidieu
                  lexicons, validation moves ask whether the new categories,                                        and Kim (2018) compared their own results with two established
                  relations, and claims credibly capture the phenomenon and offer                                   measurement approaches to show that amateur radio operators
                  novel theoretical insights. First, in establishing internal validity,                             became legitimized over time, similar to what they observed
                  trustworthiness starts by making the path from data to construct                                  based on their own analysis. While their main contribution lies in
                  inspectable—i.e., face validity in the language of the practice,                                  providing “new explanations to understand the growing
                  with provisional, practice-anchored labels. Researchers can                                       acceptance of non-professional expertise” (p. 2) in the form of
                  show: (1) compact examples anchoring each category (top                                           what they call “lay-expertise legitimation,” this analysis did help
                  words and top documents), (2) how ambiguous cases were                                            them validate their interpretations of legitimacy and, hence, the
                  handled, (3) where splitting or merging of categories was                                         phenomenon under focus.
                  enacted, and (4) why categories were dropped. For instance,
                  Croidieu and Kim (2018) explained their coding procedure and
                  visualized the mapping from topics to first-order concepts,                                       Lexical Alignment Through Iterative Sensemaking
                  second-order themes, and aggregate dimensions. Giorgi et al.
                  (2019) dropped topics based on their understanding of the                                         As with studies with primacy to theoretical lexicons, studies
                  practice lexicon, strengthened internal validity through a                                        giving primacy to practice lexicons align practice and
                  systematic coding procedure (two independent coders), and                                         theoretical lexicons iteratively across data work, model
                  provided genre-aware anchors (quotes from hearing exchanges                                       building and pattern surfacing, and validation and theorizing.
                  and corporate passages). Miranda et al. (2022b) provided                                          The difference is emphasis: Researchers hold onto practice
                  visuals for both synchronic and diachronic analyses. In all these                                 lexicons as the anchor and progressively construct theoretical
                  cases, interpretive analytical moves such as independent                                          lexicons that align with them. After an initial cycle,
                  memoing and reconciliation among authors are useful to                                            researchers can find that surfaced patterns largely reproduce
                  demonstrate trustworthiness.                                                                      established dimensions yet hint at novel ones. In such cases,
                                                                                                                    they can return to data work (e.g., purposefully sampling cases
                  The goal of such illustrations is not only to provide proof that a                                that speak to the new pattern) or revisit model building (e.g.,
                  certain category, dimension, or distribution can be considered
                                                                                                                    probe a nearby number of categories/priors or switch
                  explanatory, but also to invite readers to the qualitative
                                                                                                                    algorithms) to give voice to practice-anchored meanings.



                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   867



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 18 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  These returns are not distractions; they are how abductive                                        route is fundamentally better, and objectivity versus
                  sensemaking renders the phenomenon analytically tractable.                                        customization depends on research design choices. Hence,
                  Our framework asks authors to report a concise iteration trace:                                   theory-primacy studies are expected to condition data work to
                  (1) what practice-anchored cue motivated a return, (2) the                                        the theoretical lens and theoretical standards, whereas
                  specific move enacted, (3) the observed effect on content or                                      practice-primacy studies are expected to preserve vernacular
                  structure, and (4) why the post-iteration state better captures                                   usage and corpus-specific expressions. In parallel, our
                  the phenomenon and how the theoretical lexicons were                                              framework distinguishes when content-focused studies should
                  updated. Making these cycles visible shows not only where                                         favor customization that preserves meaning, and when
                  the analysis landed but how practice and theory were brought                                      structure-focused studies should use uniform preprocessing
                  into correspondence step by step.                                                                 and stable windows for structural comparability.

                                                                                                                    Similarly, in model building, researchers are often torn
                                                                                                                    between seeking stability or variance. DCS tools can be tuned
                  Discussion                                                                                        to become more stable (e.g., Yang & Subramanyam, 2023)
                                                                                                                    but can also be leveraged to explore diverse categorizations to
                  In this methods article, we developed a framework for                                             reflect upon. Our framework helps navigate this tension by
                  fostering trustworthiness in DCS research, where scholars                                         arguing that theory-primacy studies should prioritize evidence
                  construct theories by leveraging computational tools for                                          correspondence to the guiding theoretical lexicon and pursue
                  dimensionalization and category surfacing. As shown in                                            theoretical robustness, whereas practice-primacy studies
                  Figure 1, the framework turns on two key research design                                          should prioritize fidelity to practice lexicons while exploring
                  choices that govern both conduct and disclosure of                                                revelatory models. Simultaneously, it highlights that choices
                  corresponding analytical moves: (1) whether a study gives                                         should favor semantic distinctiveness when content is in
                  primacy to theoretical or to practice lexicons, and (2) whether                                   focus, versus comparability and associations when structure is
                  the content of texts or the structure of the corpus is central to                                 in focus. In all cases, researchers are encouraged to reflect on
                  theorizing. Conduct concerns how researchers design and                                           how patterns persist or shift under nearby configurations.
                  enact data work, model building and pattern surfacing,
                  validation and theorizing, and iterative sensemaking;                                             Finally, for validation and theorizing, our framework offers
                  disclosure concerns the proportionate reporting of those                                          guidance for authors who struggle to validate models by either
                  moves. By placing trustworthiness at the center, the                                              benchmarking against ground truth or accounting for
                  framework provides a structured way for authors, reviewers,                                       interpretations. We recommend that theory-primacy studies
                  and editors to assess the fit between objectives, analytical                                      validate in correspondence with extant constructs and
                  moves, and evidence in DCS research. Trustworthiness rests                                        theoretical frameworks, while practice-primacy studies
                  on researchers’ reasoning about why particular moves are fit                                      validate against corpus-grounded meanings and practice
                  for purpose and in proportionate disclosure of that reasoning;                                    accounts. In parallel, our framework clarifies when
                  it invites methodological bricolage oriented to the study’s                                       interpretive alignment should carry the evidentiary burden
                  aims (Harley & Cornelissen, 2022; Lincoln & Guba, 1985;                                           (focus on content) versus when structural patterns should be
                  Pratt et al., 2020, 2022) and aligns with active categorization                                   the focus of validation (focus on structure).
                  as a core engine of theory building (Grodal et al., 2021).
                                                                                                                    Overall, our framework encourages aligning conduct and
                  Our framework helps DCS researchers navigate the                                                  disclosure to the study’s objective, as shown in Figure 1.
                  trustworthiness tensions that we identified earlier (see Table                                    Further, Table 3 consolidates these recommendations into
                  1). We clarify that rather than inherently favoring one side                                      guidance for authors, editors, and reviewers. In the following,
                  over the other, each tension should be navigated depending on                                     we first discuss the specific implications for DCS researchers
                  the study’s research design. What constitutes trustworthy                                         before concluding with the implications for the CTC
                  conduct and disclosure in each phase depends on whether a                                         community more broadly.
                  study gives primacy to theoretical versus practice lexicons,
                  and on whether the content of texts versus the structure of the
                  corpus is central to theorizing.                                                                  Implications for DCS Research

                  In data work, researchers strive to foster trustworthiness                                        Implications for Researchers
                  through rigorous practices but face a key dilemma as to
                  whether to prioritize objectivity or customization in crafting                                    Our study offers several implications for researchers leveraging
                  these analytical moves. Our framework suggests that neither                                       DCS tools to build theory by helping them navigate




                   868       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 19 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  trustworthiness. First, the framework legitimizes distinct yet                                    Third, our framework foregrounds the inherently iterative
                  equally valid research designs when leveraging DCS tools to                                       character of DCS research. To ensure ease of understanding,
                  construe theories, and clarifies how to justify practices within                                  we have presented our framework in a format that
                  each. Prior research catalogues recommended practices (e.g.,                                      researchers can relate to as they move through research
                  Aceves & Evans, 2023; Hannigan et al., 2019; Kobayashi et al.,                                    phases of data work, model building and pattern surfacing,
                  2018; Schmiedel et al., 2019), but researchers may lack                                           and validation and theorizing. Yet we have argued and
                  guidance on how to choose among those practices. By grouping                                      demonstrated that the process of theory construction using
                  those practices under higher-order analytical moves and linking                                   DCS tools is an inherently iterative endeavor. Theory
                  these moves to a study’s pathway (primacy of theoretical vs.                                      construction does not happen merely at the last stage of
                  practice lexicons) and focus (on content of texts or structure of                                 research; it is simply a milestone that marks completion of
                  the corpus), the framework can help researchers make informed
                                                                                                                    an iteration and triggers the next iteration in the process of
                  choices. For each type of design, the framework provides
                                                                                                                    knowledge production. Iterations are fundamental for
                  specific guidelines for conduct and disclosure.
                                                                                                                    researchers dealing with the challenges of the lack of ground
                                                                                                                    truth in and the opacity of DCS research until they achieve
                  Second, the framework establishes links between achieving rigor
                  and fostering trustworthiness in DCS research. While existing                                     their goals of theory construction (see Miranda et al., 2022a
                  journal guidelines on transparency have strengthened rigor in                                     for a discussion on stopping rules). Our framework offers a
                  scholarship (e.g., Burton-Jones et al., 2021; DeCelles et al.,                                    glimpse of what such iterations within and across the phases
                  2021), they take for granted the distinctive trustworthiness                                      will look like and encourages researchers to be reflexive
                  tensions faced by DCS researchers. Thus, instead of thinking of                                   about them. DCS researchers should embrace these
                  our framework as a template, we encourage researchers to                                          iterations, consider how they may have shaped their theory
                  leverage it as a “canvas” that explains how different pieces of a                                 construction processes, and report on those iterations that
                  puzzle come together (Dorobantu et al., 2024). Trustworthiness                                    were consequential to the theory they ended up constructing.
                  is achieved by demonstrating that the enacted moves are                                           This will help to foster trustworthiness not only during the
                  commensurate with the chosen research design and by providing                                     review process but also for the readers who draw on these
                  just enough evidence to make the reasoning inspectable. In other                                  studies for the purpose of knowledge building.
                  words, our framework is an invitation to researchers to construct
                  their own methods such that the community recognizes such
                  methodological bricolage as legitimate.


                    Table 3. Guidance for Fostering Trustworthiness in DCS Research
                    Giving primacy to theoretical lexicons                                                         Giving primacy to practice lexicons

                    Theory-driven data work                                                                        Phenomenon-driven data work
                    Conduct (overall)                                                                              Conduct (overall)
                    - Use theory-anchored research questions to script sampling                                    - Use research questions grounded in focal phenomenon to
                      and perform preprocessing as pre-analysis active                                               script sampling and perform preprocessing based on
                      categorization.                                                                                understanding of practice lexicon.
                    Conduct (content versus structure focus)
                    - Foreground texts that narrate concrete meanings tied to focal                                Conduct (content versus structure focus)
                      constructs while preserving semantic distinctiveness in data                                 - Foreground texts that narrate concrete meaning-bearing
                      preprocessing (when content in focus); prioritize structural                                   practices and discourses, while preserving semantic
                      signal and comparability via balanced sampling and theory-                                     distinctiveness in preprocessing (when content in focus);
                      implicated data preprocessing (when structure in focus).                                       protect structural signal and comparability while relating rich
                                                                                                                     metadata to data preprocessing (when structure in focus).
                    Disclosure
                    - Specify and justify all preparation steps in relation to                                     Disclosure
                      theoretical aims, explicitly reflecting on what constitutes data,                            - Specify and justify all preparation steps in relation to how
                      and distinguish theory-motivated steps from tool defaults.                                     they clarify the phenomenon under study, explicitly reflecting
                                                                                                                     on what constitutes data, and make explicit how
                                                                                                                     phenomenon-specific needs depart from generic
                                                                                                                     preprocessing standards.




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   869



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 20 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                    Surfacing theoretically robust patterns                                                        Surfacing empirically revelatory patterns
                    Conduct (overall)                                                                              Conduct (overall)
                    - Select algorithms from prior studies with similar contexts,                                  - Choose algorithms that make the phenomenon legible,
                      theories, and data, being mindful of underlying assumptions                                    often leveraging domain expertise, being mindful of
                      inscribed in those algorithms and selecting configurations that                                underlying assumptions inscribed in those algorithms and
                      are theoretically meaningful.                                                                  selecting the rendition that most clearly reveals the
                                                                                                                     phenomenon.
                    Conduct (content versus structure focus)
                    - Favor precise semantic splitting to preserve distinct theoretical                            Conduct (content versus structure focus)
                      meanings (when content in focus); favor relating categories to                               - Favor models and settings that expose fine-grained,
                      covariates to maintain comparability across strata and                                         practice-rooted meanings (when content in focus); use
                      alignment with theory (when structure in focus).                                               representations that explicate association structure yielding
                                                                                                                     the most revelatory patterns among alternatives (when
                    Disclosure                                                                                       structure in focus).
                    - Explain why the chosen algorithm family fits the intended
                      purpose and how theoretical assumptions are aligned; report                                    Disclosure
                      and justify parameter choices beyond the obvious;                                            - Show why the chosen algorithmic approach illuminates the
                      demonstrate how patterns persist or shift under nearby                                         focal dynamic; report informative parameter specifications to
                      configurations.                                                                                illuminate revelatory variance; reflect on the revelatory value
                                                                                                                     of included and excluded models and categories.

                    Validating patterns against existing theory                                                    Validating novel theoretical patterns
                     - Conduct (overall)                                                                           Conduct (overall)
                       Establish internal validity by showing that the category system                             - Establish internal validity by making the path from data to
                       instantiates theoretical constructs through face validity;                                    construct inspectable through face validity; strengthen
                       strengthen external validity via triangulation with independent                               external validity via category-sequencing with event
                       data/methods, category-sequencing with event anchoring,                                       anchoring or comparisons of emerging patterns to existing
                       and construct alignment with preexisting frameworks.                                          phenomenon-linked measures.
                    Conduct (content versus structure focus)                                                       Conduct (content versus structure focus)
                    - Show label/interpretation stability under reasonable                                         - Use raw quotes that directly demonstrate the theorized
                      alternatives and anchor in text, then compare to established                                   categories and invite qualitative interpretation of their
                      constructs/taxonomies (when content in focus); demonstrate                                     relevance for novel concepts (when content in focus); use
                      attribute invariance and document that alternatives do not                                     direct evidence and link shifts in categories/attributes to
                      alter the structural signal (when structure in focus).                                         recognizable field episodes to validate structural patterns
                                                                                                                     (when structure in focus).
                    Disclosure
                    - Visualize top words and documents with provisional, theory-                                  Disclosure
                      anchored labels; report intersubjective interpretability; add                                - Visualize the mapping from categories to aggregate
                      quotes to justify theory-informed interpretation; show structural                              theoretical dimensions; provide examples and raw quotes
                      metrics invariance under reasonable perturbations.                                             anchoring each category; show how ambiguous cases were
                                                                                                                     handled and where categories were split, merged, or
                                                                                                                     dropped; support visuals that demonstrate theorized
                                                                                                                     categories or structural patterns; and use memoing and
                                                                                                                     author reconciliation to demonstrate interpretive
                                                                                                                     trustworthiness.


                  Implications for Reviewers                                                                        research does not merely depend on expertise in specific tools;
                                                                                                                    rather, it should focus on whether the analytical moves enacted
                  The framework also serves as a sensitizing device for                                             by authors are fit for the study’s stated objective.
                  reviewers tasked with evaluating papers using DCS tools for
                  theory construction. We recognize that on many occasions,                                         The framework is especially useful for reviewers who know
                  reviewers are invited to serve on a DCS manuscript because                                        the tools but do not use them for constructing theory, or who
                  of their proficiency with computational tools, either through                                     have approached theory construction with DCS tools from
                  their own use or contributions to tool development. Given                                         only specific research designs in their own research (as
                  their expertise with specific tools, such reviewers bring                                         summarized in Table 2). In practice, this means reading for a
                  valuable methodological insights. Yet evaluation in DCS                                           clear sense of the research objective of a given study and then



                   870       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 21 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  asking whether the evidence matches the burden implied by                                         not possible (which is more likely given the nascent nature of
                  that objective. Reviewers should, for example, ascertain:                                         the community), editors can use our framework to educate
                  When content is in focus, do the authors establish face-valid                                     reviewers on their expectations, both up front and during the
                  labels anchored in text and show how meanings persist or vary                                     ongoing exchanges between reviewers and researchers. We
                  under reasonable nearby choices? When structure carries the                                       encourage editors to intervene whenever they see reviewers
                  load, do they keep the basis of comparison the same across                                        pushing researchers in the wrong direction or researchers
                  groups or time (same corpus boundaries, units, preprocessing,                                     failing to leverage the power of computational tools in
                  windows) and anchor patterns to recognizable events where                                         constructing theory. In other words, by using our framework,
                  appropriate? Reviewers should avoid pushing authors toward                                        editors can make sure that authors follow appropriate
                  conflicting analytical moves—for example, holding a study                                         analytical moves in line with their chosen objectives and that
                                                                                                                    reviewers do not fall into the trap of the binary distinctions.
                  that prioritizes practice lexicons (aimed at discovering novel
                                                                                                                    The key objective would be to foster trustworthiness in the
                  theoretical patterns) to the same robustness rituals as a study
                                                                                                                    review process.
                  that prioritizes theoretical lexicons (aimed at explaining a
                  phenomenon through a chosen theory) is unfitting and
                                                                                                                    At the field level, our framework speaks to editors’ broader
                  unlikely to produce a developmental review.                                                       responsibility to manage the transparency agenda within their
                                                                                                                    journals, considering the potential costs and dysfunctional
                  The framework thus invites reviewers to recognize different                                       side effects that rigid policies might impose, such as
                  approaches—giving primacy to theoretical lexicons versus                                          marginalizing certain research communities or methods. By
                  practice lexicons and focusing on content versus structure—                                       adopting a framework tailored to the specific family of DCS
                  as legitimate routes to interpretive, iterative theory                                            research, editors can advance trustworthiness without
                  construction with DCS tools. Methodological pluralism                                             inadvertently hindering the development of this important
                  remains the standard, but rigor is calibrated: assess whether                                     research area. They can encourage in-depth discussion
                  the enacted moves and the evidence shown are                                                      sections, where researchers reflect honestly on what was
                  commensurate with the stated objectives, not whether the                                          learned. As the field evolves, editors can adapt their policies
                  paper mirrors rituals from other genres. A clear iteration                                        based on learnings from researchers, reviewers, and the
                  trace should make consequential iterations visible (why the                                       experiences of other journals. Our framework provides a
                  authors went back, which move changed, what shifted in                                            foundational step in characterizing what fostering
                  content or structure, and why the new state better instantiates                                   trustworthiness means in DCS research. Our hope is that
                  the theory or captures the phenomenon).                                                           future editorials about rigor, trustworthiness, or transparency
                                                                                                                    in leading journals will conceive CTC as a unique research
                  Finally, reviewers should evaluate DCS research on its own                                        genre (and DCS research as a unique method in that genre)
                  terms—a specific method family within the CTC research                                            that requires specific guidelines of its own.
                  genre that is neither purely quantitative nor qualitative, neither
                  purely theory- nor phenomenon-driven, and neither purely
                  content- nor structure-focused (Berente et al., 2019; Miranda
                                                                                                                    Implications for Maneuvering Hybrid Designs
                  et al., 2022a). We invite reviewers to use the framework as a
                  canvas for developmental feedback that advances                                                   and Switching Moves
                  trustworthiness rather than defaulting to checklists borrowed
                  from other traditions.                                                                            Our framework assumes that DCS studies fit into unique
                                                                                                                    combinations of the two axes—primacy of theoretical versus
                                                                                                                    practice lexicons, and focus on the content of texts versus the
                  Implications for Editors                                                                          structure of the corpus. We made this distinction for analytical
                                                                                                                    purposes. In reality, it is possible that DCS studies could be
                  Our framework also has implications for the senior and                                            more hybrid. First, researchers may pursue both category
                  associate editors handling DCS research-based manuscripts;                                        meanings rooted in content and corpus-level structure—using
                  these editors not only shape discourses at the level of the                                       surfaced categories to interpret meaning while also leveraging
                  manuscript but also at the field level, in the spirit of                                          distributions, associations, or trajectories to make comparative
                  cumulative knowledge building in DCS research. At the                                             or temporal claims. Second, as analysis unfolds, researchers
                  microlevel, our framework may help in several ways. For                                           may iterate not only across research phases but also across the
                  instance, editors can use our framework to orchestrate the                                        framework’s two axes—shifting between the primacy of
                  matching process between researchers and reviewers. Ideally,                                      theoretical lexicons and the primacy of practice lexicons, and,
                  editors would assign submitted studies to reviewers who are                                       at times, shifting between a focus on content and a focus on
                  likely to follow a similar approach to constructing theory in                                     structure. Our framework treats hybridity and switching as
                  their own research. But, even when such an ideal matching is



                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   871



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 22 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  legitimate features of DCS research, but it also clarifies their                                  More research is required on hybridity and switching in DCS
                  implications for trustworthiness: They change what ought to                                       studies—particularly on how often such switches occur,
                  be demonstrated and disclosed. A basic discipline is therefore                                    what triggers them, and how they reshape the burden of
                  required. Authors should be explicit about what carries the                                       proof across data work, model building, and validating.
                  theoretical load in the focal claim—whether the claim relies                                      Future work could also examine whether some switching
                  primarily on category meanings or on corpus-level structure—                                      patterns become routinized within research communities,
                  and avoid validating one kind of claim with the evidentiary                                       and how to strengthen trustworthiness in these studies
                  logic of the other. When a study advances both kinds of                                           without having to write prohibitively lengthy manuscripts.
                  claims, authors should either specify which claim is primary
                  and treat the other as corroborative evidence, or treat them as
                  distinct claims with distinct validation targets; in either case,                                 Implications for the Broader CTC                         and
                  conduct and disclosure should be aligned to the evidentiary                                       Computational Research Communities
                  logic of each rather than blended in ways that make the
                  contribution difficult to evaluate.                                                               Our framework speaks most directly to researchers who use
                                                                                                                    DCS tools with an interpretive orientation to construct theory
                  Relatedly, researchers should be aware that iterations can take                                   from text. In developing the framework, we have already
                  shape between the pathways of primacy to theoretical and                                          explained how interpretive DCS research may draw
                  practice lexicons, and can also involve shifts in whether the                                     inspiration from adjacent research that leveraged DCS tools
                  study is content-focused or structure-focused. For example,                                       for other purposes. At the same time, several of the core ideas
                  researchers may start by granting primacy to theoretical                                          of our framework travel beyond the specific domain of DCS
                  lexicons by engaging in theory-driven data work and building                                      research and open avenues for future work on the use of
                  models intended to surface theoretically meaningful                                               computational tools in research more generally. The
                  categories. In the process, however, patterns may emerge that                                     underlying principle is to make research objectives, analytical
                  do not align with the initial theoretical lexicons. At this stage,                                moves, and proportionate disclosure commensurate—
                  researchers may decide to bracket those patterns and continue                                     whatever the specific tool—so that claims are rendered
                  pursuing the original objective, or they may decide to switch                                     trustworthy for the purpose at hand. Here, we discuss such
                  and give primacy to practice lexicons to explore the                                              implications and opportunities for future research within the
                  phenomenon in depth. Similarly, researchers may begin with                                        broader CTC and computational research communities.
                  a content focus (treating category meanings as load bearing)
                  and later realize that the theoretical contribution rests more                                    A first implication concerns the use of large language models
                                                                                                                    (LLMs), a specific class of generative AI models that can
                  plausibly on corpus-level structure (or vice versa), prompting
                                                                                                                    process and generate text, in constructing theories. LLMs are
                  changes to sampling, preprocessing, parameterization, and
                                                                                                                    similar to the DCS tools we have discussed in that they operate
                  validation. In such scenarios, switching often entails redoing
                                                                                                                    on text and are powered by ML algorithms, but they are
                  earlier phases—especially data work and model building—
                                                                                                                    importantly different: They arrive as pretrained, ready-to-
                  and, crucially, respecifying the burden of proof by stating
                                                                                                                    hand, generative models, rather than as algorithms that
                  what now carries the theoretical load and what validation                                         researchers use from scratch to build context-specific models.
                  targets follow from that choice. We note that such switching                                      Hence, the question is what happens when some choices that
                  is not hypothetical; our interviewees described multiple                                          researchers make in constructing their models using DCS
                  narratives of switching in DCS research. Yet in final published                                   algorithms are now prebuilt, in the case of LLMs?
                  versions of manuscripts, these shifts are often underreported.
                  Based on our framework, we encourage authors to disclose                                          There are several considerations for trustworthiness if
                  how, when, and why they switched and to walk readers                                              researchers use prebuilt LLMs instead of the typical DCS
                  through the narrative of respecifying aims and realigning                                         tools. For example, the use of LLMs would shift the weight of
                  analytical moves. One practical way to do so is to include a                                      choices and thereby trustworthiness to different activities.
                  brief switch trace that states the trigger for the switch, what                                   With such prebuilt models, researchers need to grapple with
                  axis shifted (lexicon primacy and/or content/structure focus),                                    an ensemble of algorithms where some of the key choices that
                  what analytical moves were revised in respective phases, what                                     researchers used to make in data work and model building—
                  changed in the surfaced output, and why the post-switch                                           e.g., data preprocessing, selection of algorithms,
                  configuration better supports the study’s focal claim.                                            hyperparameter tuning—are now pre-crafted in a ready-to-use
                  Accordingly, where a manuscript reports a mid-project switch                                      model. These choices still happen, but in the background,
                  or hybrid approach, reviewers should look for a clear account                                     often without the control or knowledge of the researcher.
                  of the trigger, the rescoped data-work rules, and how the                                         Hence, the weight of trustworthiness shifts from
                  alignment between aims, moves, and evidence was restored.                                         preprocessing data and building models to tweaking model



                   872       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 23 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  inputs and outputs and crafting prompts. This has parallels                                       analytical moves differ depending on those objectives.
                  with the concept of envelopment, where the researchers may                                        Researchers could then engage in a more in-depth empirical
                  control the context, inputs, and outputs, but the inner workings                                  analysis of what those analytical moves are exactly (as we did
                  of the model may remain black-boxed (see Floridi, 2011).                                          through our methodological review and interviews). For
                  Additionally, validating surfaced patterns becomes more                                           instance, one could use computational simulations to
                  important than ever, due to the increased opacity and lack of                                     formalize theories in two ways: either by formalizing
                  control over how the model has been trained.                                                      theoretical insights generated inductively from observed data
                                                                                                                    or by formalizing a deductively developed verbal theory and
                  Further, the use of LLMs is likely to expand the scope of                                         creating synthetic data. Both objectives are feasible, both will
                  expectations for research activities that require                                                 entail construction relationships through computational
                  trustworthiness. Our framework focuses on fostering                                               simulations, but both will require a different set of analytical
                  trustworthiness in CTC across the phases of data work, model                                      moves and hence distinct expectations for fostering
                  building and pattern surfacing, and validation and theorizing.                                    trustworthiness.
                  If researchers start using LLMs, we may need to expand the
                  trustworthiness expectations to other research activities,                                        Our final implication is for computational studies that
                  including how and whether LLMs were used for idea                                                 primarily test theories using DCS tools. Given that our
                  generation, summarizing the literature, and writing the                                           framework only speaks to the use of DCS tools for theory
                  manuscript, among others. The question then is not only about                                     construction, we left out theory testing objectives. Yet we
                  whether the knowledge claims in a particular study are reliable                                   argue that these studies may still benefit from our framework.
                  and valid but also whether the knowledge claims are original.                                     Consider the study by Kaplan and Vakili (2015), in which the
                  It would be a very interesting and important avenue for future                                    authors used topic modeling to operationalize a construct of
                  research as we enter the new age of computational tools. The                                      breakthrough innovation. Their primary aim in using the DCS
                  CTC community will benefit from cumulative attempts at                                            tool was that it afforded a measurement of a construct in the
                  proposing new ways of thinking about these issues. In this                                        service of theory testing. We contend that such studies are
                  spirit, our framework is a starting point, perhaps a first step, in                               close to the pathway of giving primacy to theoretical lexicons,
                  helping characterize what fostering trustworthiness means in                                      as per our framework. Even though their goal is to test
                  CTC research.                                                                                     theories, it is likely that unexpected patterns will surface due
                                                                                                                    to the unsupervised nature of the tools they use. Such patterns
                  It is important to note that we recognize the growing debate                                      may not fit with their predefined theoretical constructs but
                  around whether researchers should use LLMs and other                                              may help them further develop their theory. Hence, they may
                  generative AI applications for their research (see Bechky &                                       switch from the original idea of theory testing to incorporate
                  Davis, 2025; Davison, 2025; Gopal et al., 2025; Kulkarni et                                       some elements of theory construction with DCS tools. If they
                  al., 2024; Susarla et al., 2023). This debate is beyond the scope                                 do so, they may be able to leverage our framework in
                  of our study. We do not take a position on whether researchers                                    demonstrating trustworthiness. A good example of this
                  should use these tools; rather, we clarify how the core logic of                                  possibility is Bao and Datta (2014). They employed topic
                  our framework may still help researchers in fostering                                             modeling for quantifying risk types from textual risk
                  trustworthiness if they do.                                                                       disclosures to test their theory, but in doing so, they were also
                                                                                                                    open to discovering novel risk types. Their paper started with
                  The second implication concerns computational tools that go                                       the primacy of theoretical lexicons. But when they witnessed
                  beyond text-centric DCS tools. Theories can be constructed                                        novel patterns surfacing from the practice lexicons, instead of
                  by leveraging computational tools that may not require the                                        ignoring those patterns, they embraced them. They were able
                  analysis of textual data—for example, analytical modeling                                         to fit these two approaches into one manuscript and offer a
                  (Sahaym et al., 2023), relational event modeling (Lindberg et                                     methodological contribution.
                  al., 2024), and computational simulations (Reider et al., 2024).
                  Such tools and associated research designs are much different                                     We call for researchers to embrace this possibility of
                  from the use of DCS tools that our framework explains. We                                         simultaneous theory testing and construction in their empirical
                  argue that in such cases of CTC research, the community will                                      papers, and our framework may offer some insights on how to
                  still benefit from embracing trustworthiness instead of                                           do that. Our guidance here is simple: If a switch occurs,
                  transparency, although what aspects of research require                                           document the trigger, the rescoped analytical moves for data
                  trustworthiness and how to foster trustworthiness in those                                        work and modeling, and how the alignment among aims,
                  aspects will need more work. Our framework will first need to                                     moves, and evidence was restored. Doing so lets a single
                  be extended before it is applied to these contexts. Further                                       manuscript host both testing and construction without
                  research could build on our key argument that there are                                           conflating their evidentiary burdens, and it renders the
                  different objectives for using the same family of tools and that                                  resulting contribution trustworthy on its own terms.



                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   873



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 24 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Conclusion                                                                                        Aguinis, H., Li, Z. A., & Der Foo, M. (2024). The research
                                                                                                                        transparency index. The Leadership Quarterly, 35(4), Article
                                                                                                                        101809. https://doi.org/10.1016/j.leaqua.2024.101809
                  CTC is a new and emergent research genre, and DCS research                                        Aguinis, H., Ramani, R. S., & Alabduljader, N. (2018). What you see
                  is a prominent method family within CTC. What we do in the                                            is what you get? Enhancing methodological transparency in
                  community today is going to have a lasting influence on how                                           management research. Academy of Management Annals, 12(1),
                  we, as CTC researchers, contribute to IS, management, and                                             83-110. https://doi.org/10.5465/annals.2016.0011
                  organizational scholarship. The initial manuscripts that are                                      Aguinis, H., & Solarino, A. M. (2019). Transparency and replicability
                  being published now are going to shape the field for decades.                                         in qualitative research: The case of interviews with elite
                  At this crucial juncture, it is important to take a step back and                                     informants. Strategic Management Journal, 40(8), 1291-1315.
                  reflect on how we conduct our research practices and how we                                           https://doi.org/10.1002/smj.3015
                  disclose our choices in published manuscripts. Our study is an                                    Amis, J. M., & Silk, M. L. (2008). The philosophy and politics of
                  attempt in this direction, wherein we propose trustworthiness—                                        quality in qualitative organizational research. Organizational
                  rather than inherited transparency checklists—as the evaluative                                       Research Methods, 11(3), 456-480. https://doi.org/10.1177/
                  anchor for theory construction with DCS tools. Our framework                                          1094428107300341
                  advances shared evaluative logic for researchers, reviewers, and                                  Bao, Y., & Datta, A. (2014). Simultaneously discovering and
                  editors that preserves methodological pluralism while enabling                                        quantifying risk types from textual risk disclosures. Management
                                                                                                                        Science, 60(6), 1371-1391. https://doi.org/10.1287/mnsc.2014.
                  cumulative theorizing. Rather than aspiring to a single correct
                                                                                                                        1930
                  rendering, the field can converge on a simple commitment:
                                                                                                                    Bechky, B. A., & Davis, G. F. (2025). Resisting the algorithmic
                  declare what kind of claim is being made, enact moves that are                                        management of science: Craft and community after generative AI.
                  fit for that claim, and provide proportionate evidence that the                                       Administrative       Science       Quarterly,      70(1),      1-22.
                  claim holds under reasonable alternatives. We are hopeful that                                        https://doi.org/10.1177/00018392241304403
                  our framework will meaningfully inform further CTC research                                       Belford, M., Mac Namee, B., & Greene, D. (2018). Stability of topic
                  in IS, management, and organizational scholarship.                                                    modeling via matrix factorization. Expert Systems with
                                                                                                                        Applications, 91, 159-169. https://doi.org/10.1016/j.eswa. 2017.
                                                                                                                        08.047
                  Acknowledgments                                                                                   Berente, N., Seidel, S., & Safadi, H. (2019). Research commentary—
                                                                                                                        Data-driven computationally intensive theory development.
                  We thank Shaila Miranda (senior editor), Hani Safadi (associate                                       Information Systems Research, 30(1), 50-64. https://doi.org/
                  editor), and the three anonymous reviewers for their constructive and                                 10.1287/isre.2018.0774
                  developmental feedback throughout the review process, which                                       Blei, D. M., Ng, A. Y., & Jordan, M. I. (2003). Latent Dirichlet
                  substantially strengthened this manuscript. We are grateful to our                                    allocation. Journal of Machine Learning Research, 3, 993-1022.
                  interviewees for generously sharing their time and insights. Earlier                              Burton-Jones, A., Boh, W. F., Oborn, E., & Padmanabhan, B. (2021).
                  versions of this work benefited from feedback and discussions at the                                  Editor’s comments: Advancing research transparency at MIS
                  KIN Center for Digital Innovation, the Work Tech writing group                                        Quarterly: A pluralistic approach. MIS Quarterly, 45(2), iii-xviii.
                  workshop, and the MIS Quarterly paper development workshop, as                                        https://doi.org/10.25300/MISQ/2021/452E1
                  well as from conference presentations at AOM 2022, the Global                                     Chang, J., Boyd-Graber, J. L., Gerrish, S., Wang, C., & Blei, D. M.
                  Transparency Conference 2022, EGOS 2020, and ICIS 2020. We                                            (2009). Reading tea leaves: How humans interpret topic models. In
                  also thank Joey van Angeren, Malmi Amadorou, Francesco Balocco,                                       Proceedings of the 23rd International Conference on Neural
                  Nick Berente, Andrew Burton-Jones, Kasper Trolle Elmholdt, Vern                                       Information Processing Systems (pp. 288-296).
                  Glaser, Tim Hannigan, Stijn Heldens, Maximilian Heimstädt,                                        Cloutier, C., & Ravasi, D. (2021). Using tables to enhance
                  Ruthanne Huising, Marleen Huysman, Tomi Kolijonen, Elina                                              trustworthiness in qualitative research. Strategic Organization,
                  Mäkinen, Balaji Padmanabhan, Pauli Pakarinen, Andrew Sarta, and                                       19(1), 113-133. https://doi.org/10.1177/1476127020979329
                  Jason Thatcher for their thoughtful comments on various aspects of                                Constantinides, P., Chiasson, M. W., & Introna, L. D. (2012). The ends
                  the manuscript. We dedicate this paper to the memory of Jovana                                        of information systems research: A pragmatic framework. MIS
                  Karanović, whom we will deeply miss. This research was supported                                      Quarterly, 36(1), 1-20. https://doi.org/10.2307/41410403
                  in part by funding from the Social Sciences and Humanities Research                               Constantiou, I., Joshi, M., & Stelmaszak, M. (2023). Organizations as
                  Council (SSHRC) Grant #430-2024-01156 to Mayur Joshi.
                                                                                                                        digital enactment systems: A theory of replacement of humans by
                                                                                                                        digital technologies in organizational scanning, interpretation, and
                                                                                                                        learning. Journal of the Association for Information Systems,
                  References                                                                                            24(6), 1770-1798. https://doi.org/10.17705/1jais.00833
                                                                                                                    Croidieu, G., & Kim, P. H. (2018). Labor of love: Amateurs and lay-
                  Aceves, P., & Evans, J. A. (2023). Mobilizing conceptual spaces: How                                  expertise legitimation in the early U.S. radio field, Administrative
                     word embedding models can inform measurement and theory                                            Science Quarterly, 63(1), 1-42. https://doi.org/10.1177/000183
                     within organization science. Organization Science, 35(3), 788-814.                                 9216686531
                     https://doi.org/10.1287/orsc.2023.1686                                                         Davison, R. M. (2025). Why you should write a cover letter.
                                                                                                                        Information Systems Journal, 35(5), 1309-1310. https://doi. org/



                   874       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 25 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                       10.1111/isj.12590                                                                                homogeneous versus heterogeneous categories. Strategic
                  DeCelles, K. A., Howard-Grenville, J., & Tihanyi, L. (2021). From the                                 Management Journal, 40(1), 3-27. https://doi.org/10.1002/smj.
                       editors—Improving the transparency of empirical research                                         2978
                       published in AMJ. Academy of Management Journal, 64(4), 1009-                                Hacker, J., vom Brocke, J., Handali, J., Otto, M., & Schneider, J.
                       1015. https://doi.org/10.5465/amj.2021.4004                                                      (2020). Virtually in this together—How web-conferencing
                  DiMaggio, P., Nag, M., & Blei, D. (2013). Exploiting affinities                                       systems enabled a new virtual togetherness during the COVID-19
                       between topic modeling and the sociological perspective on                                       crisis. European Journal of Information Systems, 29(5), 563-584.
                       culture: Application to newspaper coverage of US government arts                                 https://doi.org/10.1080/0960085X.2020.1814680
                       funding. Poetics, 41(6), 570-606. https://doi.org/10.1016/                                   Hannigan, T. R., Briggs, A. R., Valadao, R., Seidel, M.-D. L., &
                       j.poetic.2013.08.004                                                                             Jennings, P. D. (2022). A new tool for policymakers: Mapping
                  Dorobantu, S., Gruber, M., Ravasi, D., & Wellman, N. (2024). The                                      cultural possibilities in an emerging AI entrepreneurial ecosystem.
                       AMJ management research canvas: A tool for conducting and                                        Research Policy, 51(9), 1-18. https://doi.org/10.1016/j.respol.
                       reporting empirical research. Academy of Management Journal,                                     2021.104315
                       67(5), 1163-1174. https://doi.org/10.5465/amj.2024. 4005                                     Hannigan, T. R., Haans, R. F. J., Vakili, K., Tchalian, H., Glaser, V. L.,
                  Easterby-Smith, M., Golden-Biddle, K., & Locke, K. (2008). Working                                    Wang, M. S., Kaplan, S., & Jennings, P. D. (2019). Topic modeling
                       with pluralism: determining quality in qualitative research.                                     in management research: Rendering new theory from textual data.
                       Organizational Research Methods, 11(3), 419-429. https://doi.org/                                Academy of Management Annals, 13(2), 586-632. https://doi.org/
                       10.1177/1094428108315858                                                                         10.5465/annals.2017.0099
                  Elliott, K. C. (2022). A taxonomy of transparency in science. Canadian                            Harley, B., & Cornelissen, J. (2022). Rigor with or without templates?
                       Journal of Philosophy, 52(3), 342-355. https://doi. org/10.1017/                                 The pursuit of methodological rigor in qualitative research.
                       can.2020.21                                                                                      Organizational Research Methods, 25(2), 239-261. https://doi.
                  Floridi, L. (2011). Children of the fourth revolution. Philosophy &                                   org/10.1177/1094428120937786
                       Technology, 24(3), 227-232. https://doi.org/10.1007/s13347-011-                              Jacobs, A. M., Büthe, T., Arjona, A., Arriola, L. R., Bellin, E., Bennett,
                       0042-7                                                                                           A., Björkman, L., Bleich, E., Elkins, Z., Fairfield, T., Gaikwad, N.,
                  Geva, H., Oestreicher-Singer, G., & Saar-Tsechansky, M. (2019).                                       Greitens, S. C., Hawkesworth, M., Herrera, V., Herrera, Y. M.,
                       Using retweets when shaping our online persona: Topic modeling                                   Johnson, K. S., Karakoç, E., Koivu, K., Kreuzer, M., … Yashar,
                       approach. MIS Quarterly, 43(2), 501-524. https://doi.org/                                        D. J. (2021). The qualitative transparency deliberations: Insights
                       10.25300/MISQ/2019/14346                                                                         and implications. Perspectives on Politics, 19(1), 171-208.
                  Giorgi, S., Maoret, M., & J. Zajac, E. (2019). On the relationship between                            https://doi.org/10.1017/S1537592720001164
                       firms and their legal environment: The role of cultural consonance.                          Kaplan, S., & Vakili, K. (2015). The double-edged sword of
                       Organization      Science,     30(4),     803-830.      https://doi.org/                         recombination in breakthrough innovation. Strategic Management
                       10.1287/orsc.2018.1250                                                                           Journal, 36(10), 1435-1457. https://doi.org/10.1002/smj.2294
                  Gong, J., Abhishek, V., & Li, B. (2018). Examining the impact of                                  Karanović, J., Berends, H., & Engel, Y. (2021). Regulated dependence:
                       keyword ambiguity on search advertising performance: A topic                                     Platform workers’ responses to new forms of organizing. Journal
                       model approach. MIS Quarterly, 42(3), 805-829. https://doi.                                      of Management Studies, 58(4), 1070-1106. https://doi.org/
                       org/10.25300/misq/2018/14042                                                                     10.1111/joms.12577
                  Gopal, R. D., Li, J., Riemer, K., Sarker, S., Singh, P. V., Susarla, A.,                          Kobayashi, V. B., Mol, S. T., Berkers, H. A., Kismihók, G., & Den
                       Bichler, M., & Thatcher, J. B. (2025). Inventing with Machines:                                  Hartog, D. N. (2018). Text mining in organizational research.
                       Generative AI and the evolving landscape of IS research.                                         Organizational        Research     Methods,       21(3),     733-765.
                       Information Systems Research, 36(4), 1949-1967. https://doi.org/                                 https://doi.org/10.1177/1094428117722619
                       10.1287/isre.2025.editorial.v36.n4                                                           Kulkarni, M., Mantere, S., Vaara, E., van den Broek, E., Pachidi, S.,
                  Grimmer, J., Roberts, M. E., & Stewart, B. M. (2022). Text as data: A                                 Glaser, V. L., Gehman, J., Petriglieri, G., Lindebaum, D.,
                       new framework for machine learning and the social sciences.                                      Cameron, L. D., Rahman, H. A., Islam, G., & Greenwood, M.
                       Princeton University Press.                                                                      (2024). The future of research in an artificial intelligence-driven
                  Grodal, S., Anteby, M., & Holm, A. L. (2021). Achieving rigor in                                      world. Journal of Management Inquiry, 33(3), 207-229.
                       qualitative analysis: The role of active categorization in theory                                https://doi.org/10.1177/10564926231219622
                       building. Academy of Management Review, 46(3), 591-612.                                      Larsen, K. R., & Bong, C. H. (2016). A tool for addressing construct
                       https://doi.org/10.5465/amr.2018.0482                                                            identity in literature reviews and meta-analyses. MIS Quarterly,
                  Guba, E. G. (1981). Criteria for assessing the trustworthiness of                                     40(3), 529-A20. https://doi.org/10.25300/MISQ/2016/40.3.01
                       naturalistic inquiries. Educational Communication and                                        Lebovitz, S., Levina, N., & Lifshitz-Assaf, H. (2021). Is AI ground
                       Technology, 29(2), 75-91. https://doi.org/10.1007/BF02766777                                     truth really “true”? The dangers of training and evaluating AI tools
                  Günther, W. A., Thompson, M., Joshi, M. P., & Polykarpou, S. (2023).                                  based on experts’ know-what. MIS Quarterly, 45(3), 1501-1525.
                       Algorithms as co-researchers: Exploring meaning and bias in                                      https://doi.org/10.25300/MISQ/2021/16564
                       qualitative research. In B. Simeonova & R. D. Galliers                                       Lincoln, Y. S., & Guba, E. (1985). Naturalistic inquiry. SAGE.
                       (Eds.), Cambridge handbook of qualitative digital research (pp.                              Lindberg, A. (2020). Developing theory through integrating human and
                       211-228). Cambridge University Press.                                                            machine pattern recognition. Journal of the Association for
                  Haans, R. F. J. (2019). What’s the value of being different when                                      Information Systems, 21(1), 90-116. https://doi.org/10.17705/1jais.
                       everyone is? The effects of distinctiveness on performance in                                    00593



                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026    875



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 26 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  Lindberg, A., Schecter, A., Berente, N., Hennel, P., & Lyytinen, K.                                   ajps.12103
                      (2024). The entrainment of task allocation and release cycles in                              Safadi, H., Johnson, S. L., & Faraj, S. (2021). Who contributes
                      open source software development. MIS Quarterly, 48(1), 67-93.                                    knowledge? Core-periphery tension in online innovation
                      https://doi.org/10.25300/MISQ/2023/16789                                                          communities. Organization Science, 32(3), 752-775. https://doi.org/
                  Locke, K., & Ramakrishna Velamuri, S. (2009). The design of member                                    10.1287/orsc.2020.1364
                      review: Showing what to organization members and why.                                         Sahaym, A., Vithayathil, J., Sarker, S., Sarker, S., & Bjørn-Andersen,
                      Organizational Research Methods, 12(3), 488-509. https://doi.org/                                 N. (2023). Value destruction in information technology
                      10.1177/1094428108320235                                                                          ecosystems: A mixed-method investigation with interpretive case
                  Lowry, P. B., Gaskin, J., Humpherys, S. L., Moody, G. D., Galletta, D.                                study and analytical modeling. Information Systems Research,
                      F., Barlow, J. B., & Wilson, D. W. (2013). Evaluating journal                                     34(2), 508-531. https://doi.org/10.1287/isre.2022.1119
                      quality and the Association for Information Systems Senior                                    Sarker, S., Xiao, X., & Beaulieu, T. (2013). Guest editorial—
                      Scholars’ Journal Basket via bibliometric measures: Do expert                                     Qualitative studies in information systems: A critical review and
                      journal assessments add value? MIS Quarterly, 37(4), 993-1012.                                    some guiding principles. MIS Quarterly, 37(4), iii-xviii.
                      https://doi.org/10.25300/MISQ/2013/37.4.01                                                        https://doi.org/10.25300/MISQ/2013/37.4.E0
                  Marshall, J. D., Yammarino, F. J., Parameswaran, S., & Cheong, M.                                 Schmiedel, T., Müller, O., & vom Brocke, J. (2019). Topic modeling
                      (2023). Using CATA and machine learning to operationalize old                                     as a strategy of inquiry in organizational research: A tutorial with
                      constructs in new ways: An illustration using U.S. Governors’                                     an application example on organizational culture. Organizational
                      COVID-19 press briefings. Organizational Research Methods,                                        Research Methods, 22(4), 941-968. https://doi.org/10.1177/
                      26(4), 705-750. https://doi.org/10.1177/10944281221098607                                         1094428118773858
                  Miranda, S., Berente, N., Seidel, S., Safadi, H., & Burton-Jones, A.                              Schooler, J. W. (2014). Metascience could rescue the “replication
                      (2022a). Computationally intensive theory construction: A primer                                  crisis.” Nature, 515(7525), Article 9. https://doi.org/10.1038/
                      for authors and reviewers. MIS Quarterly, 46(2), iii-xviii.                                       515009a
                      https://doi.org/10.25300/MISQ/2022/462E1                                                      Sidorova, A., Evangelopoulos, N., Valacich, J. S., & Ramakrishnan, T.
                  Miranda, S. M., Wang, D., & Tian, C. (2022b). Discursive fields and                                   (2008). Uncovering the intellectual core of the information systems
                      the diversity-coherence paradox: An ecological perspective on the                                 discipline. MIS Quarterly, 32(3), 467-482.           https://doi.org/
                      blockchain community discourse. MIS Quarterly, 46(3), 1421-
                                                                                                                        10.2307/25148852
                      1452. https://doi.org/10.25300/MISQ/2022/15736
                                                                                                                    Simeonova, B., & Galliers, R. D. (Eds.). (2023). Cambridge handbook
                  Monteiro, E., Constantinides, P., Scott, S., Shaikh, M., & Burton-Jones,
                                                                                                                        of qualitative digital research. Cambridge University Press.
                      A. (2022). Editor’s comments—Qualitative research methods in
                                                                                                                    Strauss, A. L., & Corbin, J. M. (1990). Basics of qualitative research.
                      information systems: A call for phenomenon-focused
                                                                                                                        SAGE.
                      problematization. MIS Quarterly, 46(4), iii-xix. https://doi.org/
                                                                                                                    Susarla, A., Gopal, R., Thatcher, J. B., & Sarker, S. (2023). The Janus
                      10.25300/MISQ/2022/464E1
                                                                                                                        effect of generative AI: Charting the path for responsible conduct
                  Mousavi, R., & Gu, B. (2024). Resilience messaging: The effect of
                                                                                                                        of scholarly activities in information systems. Information Systems
                      governors’ social media communications on community
                                                                                                                        Research, 34(2), 399-408. https://doi.org/10.1287/isre.2023.ed.
                      compliance during a public health crisis. Information Systems
                      Research, 35(2), 505-527. https://doi.org/10.1287/isre.2021.0599                                  v34.n2
                  O’Kane, P., Smith, A., & Lerman, M. P. (2021). Building transparency                              Tremblay, M., Kohli, R., & Forsgren, N. (2021). Theories in flux:
                      and trustworthiness in inductive research through computer-aided                                  Reimagining theory building in the age of machine learning. MIS
                      qualitative data analysis software. Organizational Research                                       Quarterly, 45(1), 455-459. https://doi.org/10.25300/MISQ/2021/
                      Methods, 24(1), 104-139. https://doi.org/10.1177/10944281198                                      15434.1.1
                      65016                                                                                         Tzur, A. (2019). Uber Über regulation? Regulatory change following
                  Pratt, M. G., Kaplan, S., & Whittington, R. (2020). Editorial essay—                                  the emergence of new technologies in the taxi market. Regulation
                      The tumult over transparency: Decoupling transparency from                                        & Governance, 13(3), Article 340361. https://doi.org/10.1111/
                      replication in establishing trustworthy qualitative research.                                     rego.12170
                      Administrative Science Quarterly, 65(1), 1-19. https://doi.org/                               Valtonen, L., Mäkinen, S. J., & Kirjavainen, J. (2024). Advancing
                      10.1177/0001839219887663                                                                          reproducibility and accountability of unsupervised machine
                  Pratt, M. G., Sonenshein, S., & Feldman, M. S. (2022). Moving beyond                                  learning in text mining: Importance of transparency in reporting
                      templates: A bricolage approach to conducting trustworthy                                         preprocessing and algorithm selection. Organizational Research
                      qualitative research. Organizational Research Methods, 25(2),                                     Methods, 27(1), 88-113. https://doi.org/10.1177/1094428122
                      211-238. https://doi.org/10.1177/1094428120927466                                                 1124947
                  Reider, A., Chakravorty, S., Goyal, S., & Berndt, D. (2024). A critical                           Waardenburg, L., Huysman, M., & Sergeeva, A. V. (2022). In the land
                      realist approach to agent-based modeling: Unlocking prediction in                                 of the blind, the one-eyed man is king: Knowledge brokerage in
                      non-positivist paradigms, Journal of Information Technology,                                      the age of learning algorithms. Organization Science, 33(1), 59-82.
                      40(2), 122-139. https://doi.org/10.1177/02683962241280657                                         https://doi.org/10.1287/orsc.2021.1544
                  Roberts, M. E., Stewart, B. M., Tingley, D., Lucas, C., Leder-Luis, J.,                           Yang, Y., & Subramanyam, R. (2023). Extracting actionable insights
                      Gadarian, S. K., Albertson, B., & Rand, D. G. (2014). Structural                                  from text data: A stable topic model approach. MIS Quarterly,
                      topic models for open-ended survey responses, American Journal                                    47(3), 923-954. https://doi.org/10.25300/MISQ/2022/16957
                      of Political Science, 58(4), 1064–1082. https://doi.org/10.1111/



                   876       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 27 ---

Günther et al. / Trustworthiness in Computational Theory Construction




                  About the Authors                                                                                 strategies of organizing, with recent work focusing on AI. His
                                                                                                                    research has appeared in the Journal of the Association for
                  Wendy Arianne Günther is a researcher affiliated with the KIN                                     Information Systems, Journal of Management Studies, MIT Sloan
                  Center for Digital Innovation, Vrije Universiteit Amsterdam (VU).                                 Management Review, and Research in the Sociology of
                  She holds a bachelor’s degree in computer science from the                                        Organizations, among other outlets. He has also co-edited the
                  University of Amsterdam, a master’s diploma in “ICT in Business”                                  Research Handbook on AI and Decision-Making in Organizations.
                  from Leiden University, and a Ph.D. from the VU School of                                         He is a recipient of the AIS Outreach Practice Publication Award.
                  Business and Economics. Her research focuses on the effective and                                 ORCID: 0000-0003-2916-5282
                  responsible development and implementation of data-driven
                  solutions, including machine learning models and artificial                                       Panos Constantinides is a professor of digital innovation at
                  intelligence. In doing so, she combines qualitative research with                                 Alliance Manchester Business School, a visiting professor at the
                  algorithmic approaches, while remaining reflexive on the                                          Stockholm School of Economics and a Fellow of the Cambridge
                  implications of such tools. She recently started working as an AI                                 Digital Innovation Centre. Panos is also one of the co-founders of
                  strategy consultant. ORCID: 0000-0002-1995-8572                                                   the European Digital Platforms Research Network (EU-
                                                                                                                    DPRN). His research examines human-AI collaboration, the
                  Mayur Joshi is an assistant professor of technology and organizing                                strategy and governance of digital platform ecosystems, as well as
                  at the Telfer School of Management, University of Ottawa, Canada.                                 their sociotechnical impact. His research has appeared in
                  He earned his Ph.D. in information systems from Ivey Business                                     Information Systems Research, MIS Quarterly, Journal of the
                  School at Western University. At the intersection of information                                  Association of Information Systems, and Journal of Business
                  systems and organization theory, his research unpacks how digital                                 Venturing, among other outlets. ORCID: 0000-0003-2728-8975
                  technologies shape and are shaped by the practices, processes, and




                                                                                                                                         MIS Quarterly Vol. 50 No. 3 / September 2026   877



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026

--- page 28 ---

878       MIS Quarterly Vol. 50 No. 3 / September 2026



Downloaded from misq.​umn.​edu/​misq/​article-pdf/​50/​3/​851/​20851/​02_ma_10.​25300_misq_2026_18511.​pdf by guest on 04 October 2026
