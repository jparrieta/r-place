# Supplied proposal, 2026-09-29

Source: the vault, Projects/Working/rPlace/260929 Towards Algorithmically Grounded Theory.docx

Towards Algorithmically Grounded Theory

Organization Science's inaugural editorial called for scholars to break out of the normal science straitjacket (Daft & Lewin, 1990). Already on page 6 the mandate had boundaries. Under "heretical research methods" the editors name the longitudinal population programs, the Minnesota Innovation Research Program among them, and set them aside as "costly … and beyond the resource capacity of the typical investigator". "We are largely a science of verbal reports" (p. 3), they explained, and offered instead "a promising but less costly … strategy", clinical case research, conceding: "Building theory on the basis of in-depth understanding of a few cases is different from the traditional theory-testing goal of statistical rigor, parsimony and generalizability" (p. 6).

The editorial rethreaded boundaries set by an older conversation. In December 1966 Fritz Machlup addressed the American Economic Association as its president and revisited the marginalist controversy he had fought twenty years earlier. Hall and Hitch (1939) had interviewed businessmen about prices and reported that they did not price on marginal cost; Lester (1946) surveyed manufacturers and found the same. Machlup (1946) and Friedman (1953) defended marginal analysis. Looking back, Machlup explained why he still "find[s] it far too cumbersome in this case to go down to the level of the 'real' firms; I could probably not obtain the necessary data and, even if I did, I might not be able to rely on the composite results obtained from a firm-by-firm analysis" (p. 30). Machlup set three constraints: cost, observability, and composition. 

With time the scholars who entered the field, shared these same worries. Cost became the worry about stopping: is the data enough, and can the researcher afford to go back and check an open question? Observability became the worry about being followed: would someone else, given the same data, find the same insights, and can the process be repeated at all? Composition became the worry about generalizing: do the findings from the cases add up to a claim about the population they came from?

It need not be this way. In chapter 7 of A Behavioral Theory of the Firm, Cyert, March and C. G. Moore built a computational model from interviews with a department store’s buyers that predicted the store’s pricing decisions with accuracy in the ninety-percent range (Cyert & March, 1963, p. 128). The model broke the buyers' behavior into mechanisms that could be stated, run, and tested one at a time, and later scholars did test them one at a time; the aspiration-level search of the buyers became performance feedback theory (Greve, 2003). Once behavior is decomposed into mechanisms, cost is a budget and observation is a program. Machlup conceded the result in the speech itself and confined what it could yield: "Even if the decision-making (say, pricing) in a particular firm was sometimes satisfactorily modeled (for example, in a simulated computer program), the model has usually not been transferable to other cases, to predict decisions in other firms" (1967, p. 16). Composition was the constraint he kept, and the field let him keep it. The work was cumbersome and needed funds only GSIA had at the time (Augier & Prietula, 2007), and few programs have matched since. 

Qualitative researchers have created methods to expand their claim to composition. The Eisenhardt method gained traction due to the need of generalizing our findings to more than one case. However, as Eisenhardt (1989, p. 545) explains: with more than ten cases "it quickly becomes difficult to cope with the complexity and volume of the data" (1989, p. 545). Cases must be held together to be compared, and comparison happens in heads with similar limits. The methods that have reached higher case numbers separated coding from comparison. The Science Policy Research Unit at Sussex spent over a decade cataloguing British innovation, each identified by informants in its sector and coded on a fixed set of fields (Townsend et al., 1981). Pavitt (1984) used these to test composition via a taxonomy of sectoral patterns of technical change. But he used the coded fields, not the written records to build the taxonomy. Similarly configurational approaches reach higher case counts by reducing each case to an entry in a binary (or fuzzy) truth table (Fiss, 2011). As a field we have accepted trading qualitative knowledge about each case for a larger number of cases in the analysis (Ragin, 1987). This tradeoff has kept testing composition out of the boundaries of qualitative research.

After Cyert and March (1963), two of Machlup’s constraints were down. Cost because GSIA funded the data collection. Observability because developments in computational modeling enabled every loop, decision point, and heuristic proposed in the models to be tested and revised --- e.g., the stream of research that originated from their box on problemistic search (Posen et al.. 2018). We argue that the knowledge-aggregation capabilities of large language models are bringing our field toward a time when the constraint of population-level composition can be taken down. 

Large language models are bounded agents in themselves. As Simon (1996) argued, much of human cognition can be explained by the limits of working memory. Humans can keep about “seven chunks” (p. 66) in mind and it takes us around “eight seconds per chunk exchange” (p. 61). An LLM’s context window plays a similar role. Similar to human working memory, this is the memory the system can use to predict the next token in a decision. The context window can hold in the order of 1 million tokens and if left unstructured get muddled with time. However, LLM context windows can be virtualized and managed (Packer et al., 2023). The model need not hold everything at once. We can ask it to keep notes on what it has read. These notes can be written at varied levels of detail, crosslinked with one another, and stored outside the context window. When the agent meets a question it cannot settle from what is in the window, it writes down the question and where the answer would be found. It then empties its context window, fetches that material and settles the question. The agent can then record the answer and empty its window again before picking up where it left off. The window holds only what the current step needs; the store holds everything else, and nothing is lost to make room. Forgetting is what separates the two readers. For a human "to think is to forget differences, to generalize, to abstract" (Borges, 1944). A reader that forgets nothing has to compose by design instead. No case is dropped to make room for another. Whether a reader built this way composes knowledge across a population is the claim this proposal tests on a mostly harmless empirical example.

LLMs might allow us to break composition. Just as data science has allowed firms to gain knowledge of their individual customers, their group and regional differences. Yet, the model we are left behind is one different in nature to prior qualitative induction. A model understands the data, not necessarily us. This distance between the model and the user of the model is not new to qualitative research. But it is one, we claim will continue. Due to the aim of Organization Science to understand how organizations behave and adapt. Understanding this new viewpoint is an important contribution of testing these kinds of tools and their power to compose cases into population knowledge. 

AI lets organization researchers explore questions at an accelerating rate. This acceleration means new claims appear faster than ever. Sifting through claims needs human judgment, "the scarce input into the review process" (Gartenberg et al., 2026, p. 796). This judgement may soon run out. The editors warn that "volume will eventually overwhelm the best reviewers and editors" (p. 811). Thankfully, other fields have faced this flood before.

Biology met the flood after genomes were sequenced around 2000. Genomes produced thousands of claims about gene function (Adams et al., 2000). Each claim met a ready filter: does it hold in the fruit fly, the worm, or the mouse? The filter ran on shared databases for each animal. Databases set each new claim against everything known about that animal (Leonelli, 2016). A claim about the fruit fly meets a century of claims. A claim about an animal no one studies meets nothing. Drug firms met a similar acceleration in the 1990s. Combinatorial chemistry and high-throughput screening multiplied drug candidates. Candidates were too many to take to human trials. Yet, firms could not ignore them as rivals would test them first. A funnel was the solution: assays, cells, tissue, then animals. Each stage discarded most of what reached it. The value of a single candidate fell steadily (Scannell et al., 2012). Candidates still got sifted, because each met the same tests as those before it.

Organization science has no fruit fly and no funnel. It was not needed while the field constrained itself to "a limited number of case examples or innovative outliers" (Daft & Lewin, 1993). Outliers arrived slowly enough to judge one by one (Puranam et al., 2014). Yet when a technology changes the cost and observability of these types of studies, the field needs a new funnel. Ultimately, composition is how the field can keep pace with the flood and step beyond Machlup’s last constraint.

What we propose is a fruit fly and a first test of composition, not a proof. The instrument in the repository reads the 696 communities that organized on r/place in 2017. A fleet of agents reads each thread nad codes each community into first-order concepts and second-order themes. An aggregator composes these into one global model of how the population organized, with third- and fourth-order themes and aggregate dimensions (Gioia et al., 2013), forming categories as Grodal et al. (2021) describe. The model then goes back to each case. The agent that coded each community is resumed. The agent checks the model against its community and proposes what must be specified, elaborated or corrected for the model to explain how that community worked (Fisher & Aguinis, 2017). 

The aggregator then modifies the model in a hierarchical manner, as a multilevel model pools estimates across groups (Gelman & Hill, 2007). A correction in one community remains as is for that community. A correction found in two or more communities is replicated (Yin, 2018) and goes back into the global model, much as shared derived traits, not traits unique to one lineage, define a group in phylogenetic systematics (Hennig, 1966). The aggregator then clusters the accepted adaptations. Organizational forms emerge when different communities need similar adaptations (McKelvey, 1982; Meyer et al., 1993). Composition fails if the adaptations stay a heap of particulars and never revise the shared model. 

Yet, it would be hubris to claim that the insights in the current model are good. The model attached in the repository is the fourth try, and the first with the full data set. But just as with biology’s understanding of the fruit fly our understanding of what happened during Reddit Place 2017 will increase through time. The proposal is then an open social experiment in composition in Organization Science.

REFERENCES

Adams, M. D., Celniker, S. E., Holt, R. A., Evans, C. A., Gocayne, J. D., Amanatides, P. G., ... Venter, J. C. (2000). The genome sequence of Drosophila melanogaster. Science, 287(5461), 2185–2195. https://doi.org/10.1126/science.287.5461.2185

Augier, M., & Prietula, M. (2007). Historical roots of the A Behavioral Theory of the Firm model at GSIA. Organization Science, 18(3), 507–522. https://doi.org/10.1287/orsc.1070.0276

Borges, J. L. (1944). Funes el memorioso. In Ficciones. Sur.

Cyert, R. M., & March, J. G. (1963). A behavioral theory of the firm. Prentice-Hall.

Daft, R. L., & Lewin, A. Y. (1990). Can organization studies begin to break out of the normal science straitjacket? An editorial essay. Organization Science, 1(1), 1–9.

Daft, R. L., & Lewin, A. Y. (1993). Where are the theories for the "new" organizational forms? An editorial essay. Organization Science, 4(4), i–vi.

Eisenhardt, K. M. (1989). Building theories from case study research. Academy of Management Review, 14(4), 532–550.

Fisher, G., & Aguinis, H. (2017). Using theory elaboration to make theoretical advancements. Organizational Research Methods, 20(3), 438–464.

Fiss, P. C. (2011). Building better causal theories: A fuzzy set approach to typologies in organization research. Academy of Management Journal, 54(2), 393–420.

Friedman, M. (1953). The methodology of positive economics. In Essays in positive economics (pp. 3–43). University of Chicago Press.

Gartenberg, C., Hasan, S., Murray, A., & Pierce, L. (2026). More versus better: Artificial intelligence, incentives, and the emerging crisis in peer review. Organization Science, 37(3), 795–812.

Gelman, A., & Hill, J. (2007). Data analysis using regression and multilevel/hierarchical models. Cambridge University Press.

Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013). Seeking qualitative rigor in inductive research: Notes on the Gioia methodology. Organizational Research Methods, 16(1), 15–31.

Greve, H. R. (2003). Organizational learning from performance feedback: A behavioral perspective on innovation and change. Cambridge University Press.

Grodal, S., Anteby, M., & Holm, A. L. (2021). Achieving rigor in qualitative analysis: The role of active categorization in theory building. Academy of Management Review, 46(3), 591–612.

Hall, R. L., & Hitch, C. J. (1939). Price theory and business behaviour. Oxford Economic Papers, 2, 12–45.

Hennig, W. (1966). Phylogenetic systematics. University of Illinois Press.

Leonelli, S. (2016). Data-centric biology: A philosophical study. University of Chicago Press.

Lester, R. A. (1946). Shortcomings of marginal analysis for wage-employment problems. American Economic Review, 36(1), 63–82.

Machlup, F. (1946). Marginal analysis and empirical research. American Economic Review, 36(4), 519–554.

Machlup, F. (1967). Theories of the firm: Marginalist, behavioral, managerial. American Economic Review, 57(1), 1–33.

McKelvey, B. (1982). Organizational systematics: Taxonomy, evolution, classification. University of California Press.

Meyer, A. D., Tsui, A. S., & Hinings, C. R. (1993). Configurational approaches to organizational analysis. Academy of Management Journal, 36(6), 1175–1195.

Packer, C., Wooders, S., Lin, K., Fang, V., Patil, S. G., Stoica, I., & Gonzalez, J. E. (2023). MemGPT: Towards LLMs as operating systems (arXiv:2310.08560). arXiv. https://arxiv.org/abs/2310.08560

Pavitt, K. (1984). Sectoral patterns of technical change: Towards a taxonomy and a theory. Research Policy, 13(6), 343–373.

Posen, H. E., Keil, T., Kim, S., & Meissner, F. D. (2018). Renewing research on problemistic search: A review and research agenda. Academy of Management Annals, 12(1), 208–251.

Puranam, P., Alexy, O., & Reitzig, M. (2014). What's "new" about new forms of organizing? Academy of Management Review, 39(2), 162–180.

Ragin, C. C. (1987). The comparative method: Moving beyond qualitative and quantitative strategies. University of California Press.

Scannell, J. W., Blanckley, A., Boldon, H., & Warrington, B. (2012). Diagnosing the decline in pharmaceutical R&D efficiency. Nature Reviews Drug Discovery, 11(3), 191–200. https://doi.org/10.1038/nrd3681

Simon, H. A. (1996). The sciences of the artificial (3rd ed.). MIT Press.

Townsend, J., Henwood, F., Thomas, G., Pavitt, K., & Wyatt, S. (1981). Science and technology indicators for the UK: Innovations in Britain since 1945 (SPRU Occasional Paper No. 16). Science Policy Research Unit, University of Sussex.

Yin, R. K. (2018). Case study research and applications: Design and methods (6th ed.). SAGE.
