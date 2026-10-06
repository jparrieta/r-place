# Schildt (2026), Designing AI for qualitative research: predictability, transparency, and control in AI tool Skimle.com (working paper, June 2026)

Source: `ssrn-6992061.pdf`. Text extracted by pdftotext; layout kept, page breaks marked. A quote from this file is the extraction's, so check an odd word against the page it names.

--- page 1 ---

Designing AI for Qualitative Research:
                 Predictability, Transparency, and Control in AI tool Skimle.com

                                            Henri Schildt
                                   Aalto University & Skimle.com
                                        henri.schildt@aalto.fi


Working paper, June 2026



Abstract
Despite the rapidly growing capabilities of large language models (LLMs) and their adoption
across diverse forms of knowledge work, their reception in the domain of qualitative research has
been ambivalent. The same technologies that promise to let researchers work faster, draw on larger
corpora, and surface patterns that would be impractical to find by hand also raise the prospect of
analyses that are unreliable, opaque, and disconnected from the interpretive judgment. In this
article, I first set out the central criticisms and risks that attach to the use of artificial intelligence
in qualitative analysis, focusing on hallucination and the more insidious problem of cognitive
offloading, whereby tools that automate interpretation gradually erode the researcher’s own
engagement with the data. Addressing the concerns, I introduce three design criteria for AI-driven
analysis and their implementation in Skimle.com service: (1) predictable processes; (2) two-way,
end-to-end transparency between original data and conclusions; and (3) substantive researcher
control over AI-powered coding and categorization. I elaborate why these design characteristics
enhance the ability of tools to augment rather than automate expert work. Finally, I consider the
relationship between AI analysis tools and qualitative methods, arguing that a well-designed tool
should remain method-agnostic, allowing researchers to follow their chosen approach.


Keywords: AI augmentation, qualitative research, large language models, CAQAS, cognitive
offloading


Competing interest statement: The author is a co-founder of and holds a financial interest in
Skimle.com, the platform discussed in this article. The design criteria advanced here are offered
as a contribution to methodological debate, not as product endorsement.




                                                    1

--- page 2 ---

Introduction

Artificial intelligence holds great promise for qualitative research. Large language models can

read, summarize, and label text far faster than any human coder, allowing users to go through

larger datasets and apply more theoretical perspectives to analysis. This new capability to

scrutinize hundreds of interviews and tens of thousands of pages of archival material leads AI to

change the questions we can reasonably address. In short, AI promises to be a source of

methodological innovation (Gartenberg et al., 2026). In smaller studies, AI may also contribute to

the quality of our studies (Schildt, 2026), as we can revisit and recode our datasets more often,

systematically find counterevidence and contingencies, and provide an “external” perspective to

our interpretations so as to combat our biases and myopias.

Alongside this promise sits a substantial concern that AI will affect the field negatively (see e.g.

Nguyen & Welch, 2026). Although the criticism is diverse in its concerns and quality, it is clear

that without established practices and design principles, artificial intelligence can harm the quality

of our research. The academic field needs to develop shared understandings concerning adequate

tools and their appropriate uses, moving beyond the coarse architectural categories of chatbots,

workflows, and agentic systems (Schildt, 2026). This working paper asks: how should we design

AI tools for qualitative research to maximize their ability to augment human researchers while

minimizing risks to research quality? I hope that by opening up the topic, this paper can spur more

debate in academia and ultimately contribute to the devleopment of better tools and research

practices.

Concretely, I begin by reviewing the key concerns with AI use in qualitative research, emphasizing

the related isseus of cognitive offloading and opacity. I then elaborate three design goals for

qualitative analysis AI tools: predictability, transparency, and user control. These three properties


                                                  2

--- page 3 ---

are key facilitators for effective AI augmentation, allowing human experts to shape the analysis

based on their judgment. After developing each criterion, I illustrate how they can be

operationalized in practice by describing the design of Skimle.com, an analysis platform I have

been involved in developing.

Building on the final criterion of user control, I make the case that AI tools should ideally be

“methodology agnostic”; they should afford researchers to engage in diverse kinds of analysis

processes, ranging from content analysis and highly inductive coding to theory-driven

“constructivist grounded theory” that imposes a clear analytical frame on the data. The method-

agnostic approach requires both transparency and flexibility from the tools, accommodating a

variation in the balance between empirically derived patterns and researcher-defined focus in the

functioning of the AI.

I conclude this working paper by calling for further debate on the principles for designing tools

and practices for using them. My view is necessarily colored by my own experiences in doing

interpretative organizational research and more recently shaped by my role as a developer of a

commercial AI analysis tool for academic and business use. To avoid the potential pitfalls of AI

and to develop better tools to augment our research practices, it will be valuable for practitioners

of qualitative research from diverse traditions to voice their concerns, needs, and priorities that can

drive the development of better tools and research practices.




Core concerns of AI use in qualitative analysis

The criticism of AI in qualitative research has ranged from technical shortfalls of early consumer

solutions (Nguyen & Welch, 2026) to more fundamental concern over the impact of AI on research




                                                  3

--- page 4 ---

practice (Bechky & Davis, 2025; Cornelissen, 2026). The early objections towards large language

models for qualitative analysis centered on concrete problems, such as hallucination, privacy, and

lack of comprehensiveness (e.g. Nguyen & Welch, 2026). Hallucinations, or confabulations, are

terms commonly used for the tendency of generative models to produce confident text that is

clearly wrong and ungrounded in the input prompt or general human knowlwedge. These are not

coincidental errors, but inherent to the statistical manner in which LLMs work (Ji et al., 2023). In

qualitative research setting, the credibility of any analysis is destroyed if AI introduces made up

quotes that participants did not say or archival documents did not contain. Privacy concerns were

similarly acute, since qualitative data frequently consists of sensitive, identifiable accounts that

researchers are ethically and legally obliged to protect. Finally, many consumer-grade chatbots

that researchers initially use rely on opaque search algorithms to sample data from source

documents, which is then fed into the AI model, leading these tools to selectively ignore certain

documents and document segments (Schildt, 2026).

These early problems have been substantially addressed in professional-grade tools. Software tools

that verify that LLM-generated quotes exist in verbatim in source documents can effectively

eliminate hallucinations when it comes to empirical data, although there is no way to guarantee AI

will always assign sensible code and category names. The growing availability of models hosted

by reputable cloud computing providers that guarantee neither inputs nor model outputs are used

for training has gone a long way toward meeting privacy obligations. Finally, the tools designed

specifically for qualitative research incorporate determinate workflows that provide

comprehensive analysis of all data. The more significant risks are not errors, but systematic effects

tools have on our research practice, and particularly the cognitive offloading of thinking and

interpretation to AI.



                                                 4

--- page 5 ---

Cognitive offloading and opacity

The foremost of the deeper risks is the tendency of AI automation to reduce human interpretation

and involvement, a phenomenon now widely known as cognitive offloading or cognitive surrender

(Risko & Gilbert, 2016; Shaw & Nave, 2026). While delegating cognitive work to external tools,

such as notebooks, calculators, search engines, is clearly beneficial, AI models can lead to

“abdication of critical evaluation, where the user relinquishes cognitive control and adopts the AI's

judgment as their own” (Shaw & Nave, 2026: 4). In qualitative analysis, the act of coding is not

merely a means to an end. Reading transcripts closely, contemplating alternative labels and

categories, and revising emerging scheme are core activities that familiarize the researchers with

their data. Some experimental evidence suggests that heavy reliance on AI tools can be associated

with reduced critical engagement and weaker independent judgment, an effect mediated precisely

by the degree of cognitive offloading the tools invite (Gerlich, 2025). Others have warned that

once professionals begin using AI to generate content, they progressively cease to produce it

themselves, eroding both individual skill and the collective standards of the profession (Lindebaum

et al., 2025; Bechky & Davis, 2025). There is a real danger that automation will eat augmentation:

a tool intended to support the expert ends up supplanting them.

While cognitive offloading is undesirable on its own because it reduces creativity and

thoughfulness of research outputs, it is also outright dangerous because it leaves AI model biases

unchecked. Language models may contain a myriad of systematic biases, such as racism and

sexism, that can in some cases exceed those present in their training data (Hofmann et al., 2024).

While AI models can ideally help identify and counter human biases that are inevitably present

even among qualitative researchers, unchecked use of AI outputs can introduce stronger and more

systematic biases into the analysis.



                                                 5

--- page 6 ---

One of the key drivers of offloading is the opacity of AI processing that makes it difficult for

humans to engage with analyses. AI tools function as black boxes, producing categories, themes,

or summaries without exposing how those outputs were derived from the underlying text. Opacity

compounds the offloading problem, because a researcher who cannot inspect the reasoning behind

a result has no choice but to either trust the analysis or verify everything. Opacity thus undermines

the collaborative relationship that ought to exist between the human and the tool. Qualitative

analysis at its best is a dialogue between the researcher’s evolving interpretation and the material

itself. Opaque theoretical inferences and quotes detached from their context prevent researchers

from engaging with their data, thereby failing to facilitate the richer exploration of data that AI

might otherwise enhance. Cognitive offloading, amplified further by opacity, define the problem

space that the three evaluation criteria I introduce below seek to address.

Key criteria for designing AI tools: predictability, transparency, and control

The design of AI tools must facilitate researchers’ effortless engagement with their data, ranging

from exploration and initial coding to editing codes and redefining category structures. To keep

the human expert in the analytical loop, researchers must be able to effortlessly observe and

understand the tasks carried out by the AI and intervene when appropriate. The three criteria of

predictability, transparency, and control all contribute to the goal of expert augmentation rather

than opaque task automation.

Predictable coding and categorization

A tool must offer a degree of predictability, so that the user can develop an understanding of the

outcomes of their actions. There are clearly some forms of predictability that LLMs can never

accomplish due to the statistical nature of neural network processing. However, we can aim for a

less strict definition of predictability as a relatively stable relationship between researchers’ actions


                                                   6

--- page 7 ---

and the results produced by a tool. This form of predictability, where the user can learn how a tool

responds to specific behaviors allows individuals to develop expertise.

What would such predictability look in practice? Assigned to code a dataset, the result of an AI

tool should always be in the same form and, for a given set of interviews, it should create

substantively the same content. This predictability turns a tool into a useful instrument that extends

the powers of its user. For example, hammers and guitars are useful because their behavior is

consistent, enabling the user to develop tacit skills to master them.

The predictability can be enhanced by deliberately designed workflows that connect to central

qualitative research traditions, such as various iterations of grounded theory (Glaser & Strauss,

1967), thematic analysis (Braun & Clarke, 2021), or the “Gioia Method” (Gioia et al., 2013).

Clearly designed data structures and workflows have the added benefit of enforcing predictable

and uniform processes across different language models that a tool might use. Even though both

AI tools and the underlying LLMs they use inevitably evolve over time, their usefulness declines

rapidly if updates break the existing practices and procedures researchers have developed.

Ultimately, predictability comes with a cost because it restrains the AI system. Fully agentic AI

systems that operate without any predetermined structure abandon predictability (Schildt, 2026).

They can decide autonomously how to decompose a task, which steps to take, and in what order,

generating workflows afresh each time. While agentic systems promise a path towards increasingly

powerful analyses, they create unpredictable processes. These problems are amplified by the

opaqueness of the outputs from complex agentic processes.




                                                  7

--- page 8 ---

Two-way end-to-end transparency

Transparency, the second criterion, enables researchers to understand, verify, and stand behind any

results created by AI systems. There are obviously many views on what transparency ought to

mean, ranging from the ability to comprehend the functioning of the system on a low technical

level to seeing how system inputs and outputs relate to one another. The mere complexity of large

language models means that the exact process that leads to a specific output can never be fully

transparent, in the same way we can never fully understand the thinking of fellow human beings.

My suggestion is that akin to predictability, transparency ought to be conceived at the level of

system behavior rather than the inner functioning of AI systems, something unattainable in any

case. To be transparent, and AI tool should expose to the user how various input texts relate to

analysis outputs from the AI. This is also a familiar form of transparency in the research context:

reviewers and co-authors cannot see how the reasoning of a human author works, but we aspire to

show how data led to the analytical conclusions through Methods and Findings sections and

associated tables.

This sort of transparency has two directions. The first direction runs from conclusion to the source,

involving the ability to see the original quotations from which AI has derived any element of the

analysis, together with the surrounding context of the broader interview or document. In short, any

qualitative AI tool should allow a researcher to move from an abstract claims down to the specific

contextualized passages that support it. The second direction runs from source to conclusion,

providing clear visibility on how any particular piece of data was analyzed and what conclusions

were drawn. Just as importantly, this involves the ability to see what statements were ignored in

coding. Knowing the statements AI tool passed over enables researchers to assess whether the

analysis is balanced, or if oversight may have led to systematic biases. A careful review of the


                                                 8

--- page 9 ---

most central and informative interviews can go a long way in establishing confidence that AI-

augmented coding converges meaningfully with how the researcher would have interpreted texts.

Beyond the bi-directional linkages between data and simple coding lies what I call end-to-end

transparency, which becomes salient as workflows grow more complex and more agentic. When

AI engages multiple and potentially recursive stages of coding, categorization, cross-cutting

comparisons, and analytical summarization, the research risks becoming increasingly opaque. To

maintain transparency, researchers ought to be able to “travel” the path from initial analytical

choices to the final conclusions, seeing what alternative approaches were conceived by AI models

and the choices the agentic AI made. This extensive form of transparency would allow researchers

to understand the overall logic of the analysis. Solutions will probably have to offer view with

different degrees of granularity so that researchers can develop a big picture understanding of the

analyses without being overwhelmed, but also have the possibility to scrutinize specific steps in

greater detail.

User control over AI processing

The third criterion is the ability to effortlessly control how data is analyzed. This ranges from

manual coding of passages and renaming of categories to trying out alternative “theoretical

frames” to categorize observations. In short, tools should enable humans to shape the analysis

directly and easily. Only by allowing the researcher to rerun and adjust analyses, tools can provide

a sense of control and ownership over the results. Difficulties in adapting categorization, relabeling

a code, splitting a theme, or reassigning a passage can lead reseachers to step back and simply

offload the analysis to the AI tool. Without easy means to adapt the analyses, research will drift

toward whatever the model happened to produce rather than toward what the researcher judges to

be correct or insightful.


                                                  9

--- page 10 ---

Sense of control complements predictability and transparency in counteracting cognitive

offloading. If predictability allows the researcher anticipate what AI is doing and transparency

helps understand what the AI tool has actually done, control captures the ease of applying their

understanding and judgment to reshape work initially done by AI. Tools that make edits easy to

apply and reverse facilitate active engagement from researchers. This means they can develop and

try out new interpretations. In contrast, AI tools that make it difficult to adapt coding,

categorization, and summaries made by AI likely nudge researchers to too easily accept AI output

as the end product.




How AI tools can address these concerns: The case of Skimle.com

This section describes how we have thus far addressed these three criteria in the Skimle.com

analysis platform. Our design choices are neither surprising nor exceptional; I recount them to

illustrate ways in which dedicated software can address many of the challenges users encounter

with generic tools, such as ChatGPT, Claude Code, or NotebookLM.

Predictability through structured extraction and categorization

Skimle seeks to make its functioning predictable by following a generic workflow modeled after

common qualitative research practice, consisting of (1) setting focus, (2) extracting and coding

quotes, (3) developing categories, (4) assigning data to appropriate categories, and (5) developing

category summaries. The purpose of this bottom-up process is to align the AI functioning with the

traditional data-driven coding process and to create a predictable process that works similarly

every time. This allows users to develop expectations of how a set of documents will be analyzed

and how prompting shapes coding and categorization outcomes. Themes are depicted as




                                                10

--- page 11 ---

categories, and all contents corresponding to a specific theme are always assigned to exactly one

sub-category underneath it.

Initially, the user can either define the themes driving their analysis or use AI functionality to

identify interview questions and section headings in source materials to generate broad themes

inductively. Second, the software feeds the user’s data (“documents”) into a large language model

(e.g. Anthropic Claude or OpenAI GPT model) to extract any passages from text that correspond

to themes defined by the user (user can also choose the AI model to identify themes from document

contents). All the extracted quotes are given a descriptive label and verified with software to ensure

that they appear verbatim in the source text, eliminating hallucinations. The software then

leverages AI to merge thematically overlapping labels and quotes, called “insights” on our system,

in each document to minimize redundancy. Third, the LLM suggests different parsimonious

categorization schemes for the extracted quotes under each theme, and these schemes are then

combined together to reach a meaningful number of categories. We then use the LLM to reassess

the coded quotes in each theme and assign them to the most appropriate category. Optionally, steps

three and four can be repeated to form an additional layer of subcategories and increase the

granularity of the coding scheme. In the final step, our software instructs the LLM to generate a

summary of category contents.

Processing data in simple steps increases predictability for the user. In our case, the choices we

ask the LLM to make are: (1) which sentences in a given paragraph of text relate to a list of themes,

(2) what are good descriptive labels for quotes, (3) which labels and quotes overlap, (4) what

categories would parsimoniously capture the content, and (5) which category does each quote best

fit in. Only the first choice is critical, as it determines what data gets picked up for analysis. The




                                                 11

--- page 12 ---

other four decisions have more modest impact on analysis quality as long as human researchers

examine and adjust category boundaries, names, and contents.

Transparency through user interface design

Skimle pursues two-way transparency directly though the user interface. In the conclusion-to-

source direction, every code, theme, and summary is linked to the specific passages that gave rise

to it, and the researcher can move from any analytic claim to the underlying quotations and read

each quotation in the context of the full document from which it was drawn. In the reverse

direction, the interface shows utilized passages in each document as highlighted text, akin to the

classic qualitative research solutions. By surfacing both what was used and what was omitted, the

interface allows the researcher to judge whether the analysis is balanced and to notice when

potentially relevant material has gone uncoded.

While our support for agentic analysis is still at its infancy, we hope to create narrative process

maps with direct links to source materials, codes, and conclusions. This would allow the user to

follow how the analysis proceeded, understand why certain categories were chosen, and see what

type of comparative or temporal dynamics were analyzed by the AI and to what effect.

User control through editing and moving codes and restructuring categories

Skimle gives the researcher direct, low-friction control over the products of the analysis. Codes

can be edited, renamed, merged, and moved; passages can be reassigned from one code or category

to another; and the category structure itself can be reorganized when the researcher judges that a

different arrangement better captures the data. We have tried to make these interventions as quick

as possible, so that revising the AI’s output is a routine part of the analytic workflow. Most

functions can be done either by clicking with a mouse or though natural language chat interface,




                                                  12

--- page 13 ---

and nearly all commands can also be undone when needed. The intent is to position the AI-powered

analysis as a draft that the researcher is expected to reshape so that the interpretive authority

remains with the human.in

Tools should not define methods

I have encountered a presumption that since AI tools engage in symbolic processing, they follow

a specific qualitative research method. This is a reasonable assumption, but I argue that a well-

designed tool can support diverse methodological stances. A flexible tool allows the user to shift

between more data-driven “inductive” coding and categorization to more theory-informed

abductive or deductive research approaches. However, the danger that AI tools shape the

methodological approach is real: if inductive coding is effortless and theory-driven coding more

cumbersome, users may be nudged towards more data-driven analyses. A flexible tool, on the other

hand, requires the user to be aware of the different qualitative research traditions.

Inductive analysis: taking stock of and abstracting from data

The classic view of grounded theory, as espoused by Glaser (1992), emphasizes open inductive

coding and categorization of data, in which the researcher approaches the material with as few

preconceptions as possible. In this paradigm, codes and categories are assumed to emerge from

the interview transcripts in informants’ own words (Glaser & Strauss, 1967; Glaser, 1978). The

aim is to take stock of what is present in the data and to abstract upward from it, building categories

that are grounded in the material rather than imposed upon it. Skimle implements this orientation

through “automatic thematic analysis”, a form of coding that extracts key themes from the

questions asked in interviews, codes the data according to those emergent themes, and then forms

inductive categories that organize the codes into a higher-order structure. The researcher is not




                                                  13

--- page 14 ---

required to specify in advance what they expect to find; the structure arises from the data and is

then made available for inspection, revision, and abstraction.

Theory-informed analysis: imposing a researcher viewpoint on data

Most contemporary authorities in qualitative research emphasize the importance of theory-driven

coding and categorization, in which the researcher’s conceptual commitments are an explicit part

of the analysis that enables a strong contribution (Strauss & Corbin, 1990; Charmaz, 2006; Braun

& Clarke, 2006, 2019). For Charmaz (2006), coding is an interpretive act shaped by the

researcher’s perspective; for Braun and Clarke (2019), reflexive thematic analysis treats the

researcher’s active, theoretically informed approach as the engine of analysis. Skimle

accommodates theory-informed analysis in two ways. First, authors can at any point define

categories to extract from the data with theory-informed descriptions of the passages to extract.

The researcher can thus engage in AI-enabled theory-driven coding at any point in time. Second,

Skimle offers a “restructure categories” functionality that affords the researcher to choose the

theoretical logic by which insights are organized into category or subcategories. This allows the

researcher to reorganize a body of coded material to reflect different alternative conceptual

frameworks. In both cases, the researcher can easily impose their own viewpoint on the data,

enabling effortless creation of theory-informed analyses.

Agentic analyses

New agentic possibilities introduce an important and as yet unresolved tension into AI-augmented

research practice. Agentic AI enables the researcher to interact with the AI models and data to

determine, in dialogue, the most interesting approaches to coding and categorizing the data, rather

than committing to a fixed scheme at the outset. Once the analysis is running, agentic AI can spot

opportunities to direct the focus of analysis, for example by leveraging metadata variables, such


                                                14

--- page 15 ---

as the date and source of an archival document or the demographic characteristics of an

interviewee, to surface patterns in the dataset.

Yet this power comes at a cost that runs directly counter to the criteria developed earlier in this

article. The more control AI is given over the analysis, the less methodological control and

transparency the researcher potentially retains, and the greater the risk of unpredictable, opaque

processes of exactly the kind the three criteria are meant to guard against. Developing ways to

harness agentic AI while preserving predictability, transparency, and control therefore represents

one of the most important areas for future development, and it is one where, candidly, current tools

including our own have more questions than answers.

Conclusion

This article has proposed three evaluation criteria for AI-enabled qualitative research —

predictability, transparency, and control. These criteria can help ensure that AI tools augment the

researcher’s judgment rather than displacing it by automating the work. They also provide a

vocabulary for distinguishing tools that keep the expert in the loop from approaches that invite the

researcher to offload the very interpretive work that constitutes qualitative analysis. These criteria

go beyond the minimum conditions of eliminating hallucination and securing the privacy of

research data, which I consider as a minimum starting point for professional tools.

I have elaborated how Skimle seeks to account for these three criteria — through structured

extraction that makes its behavior predictable, through user interface design that makes visible the

relationships between empirical passages and analytical conclusions, and through low-friction

editing that keeps interpretive authority with the researcher. Our solution is merely an example of

an AI-enabled tool, and we will probably see more development in the future, particularly in the

agentic domain.


                                                   15

--- page 16 ---

Ideally, AI should allow researchers not only to perform existing methods more effectively but to

develop new approaches to qualitative research altogether. Any tool that is too tightly bound to a

single established method risks foreclosing methodological innovation. Skimle is intended to

accommodate diverse approaches and leave room for methodological innovation. We

accommodate this in part through MCP connection that allows powerful agentic tools, such as

Claude Code and Claude Cowork, to both read and write the data in Skimle. Ideally, our

community should engage in rich conversations concerning different tools and practices that can

faciliate new forms of qualitative research.




References

Bechky, B. A., & Davis, G. F. (2025). Resisting the algorithmic management of science: Craft
       and community after generative AI. Administrative Science Quarterly, 70(1), 1–22.
       https://doi.org/10.1177/00018392241304403

Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. Qualitative Research in
       Psychology, 3(2), 77–101.

Braun, V., & Clarke, V. (2019). Reflecting on reflexive thematic analysis. Qualitative Research
       in Sport, Exercise and Health, 11(4), 589–597.

Braun, V., & Clarke, V. (2021). Thematic analysis: A practical guide. London: Sage.

Charmaz, K. (2006). Constructing grounded theory: A practical guide through qualitative
       analysis. London: Sage.

Cornelissen, J. P. (2026). The Artificial Intelligence Con: The commodification of theory and the
new and improved credibility crisis. Organization Studies. Advance online publication.
https://doi.org/10.1177/01708406261450467




                                               16

--- page 17 ---

Gartenberg, C., Hasan, S., Murray, A., & Pierce, L. (2026). More versus better: Artificial
       intelligence, incentives, and the emerging crisis in peer review. Organization Science,
       37(3), 795–812. https://doi.org/10.1287/orsc.2026.ed.v37.n3

Gerlich, M. (2025). AI tools in society: Impacts on cognitive offloading and the future of critical
       thinking. Societies, 15(1), Article 6. https://doi.org/10.3390/soc15010006

Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013). Seeking qualitative rigor in inductive
       research: Notes on the Gioia methodology. Organizational Research Methods, 16(1), 15–
       31. https://doi.org/10.1177/1094428112452151

Glaser, B. G. (1978). Theoretical sensitivity: Advances in the methodology of grounded theory.
       Mill Valley, CA: Sociology Press.

Glaser, B. G. (1992). Basics of grounded theory analysis: Emergence vs. forcing. Mill Valley,
       CA: Sociology Press.

Glaser, B. G., & Strauss, A. L. (1967). The discovery of grounded theory: Strategies for
       qualitative research. Chicago: Aldine.

Hofmann, V., Kalluri, P. R., Jurafsky, D., & King, S. (2024). AI generates covertly racist
       decisions about people based on their dialect. Nature, 633(8028), 147–154.
       https://doi.org/10.1038/s41586-024-07856-5

Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu, Y., … Fung, P. (2023). Survey of hallucination in
       natural language generation. ACM Computing Surveys, 55(12), 1–38.
       https://doi.org/10.1145/3571730

Lindebaum, D., Nolan, E., Ashraff, M., Islam, G., & Ramirez, M. F. (2025). The transformation
       of epistemic agency and governance in higher education through large language models:
       Toward a future of organized immaturity. Organization Studies. Advance online
       publication. https://doi.org/10.1177/01708406251392002

Nguyen, D. C., & Welch, C. (2026). Generative artificial intelligence in qualitative data analysis:
       Analyzing—or just chatting? Organizational Research Methods, 29(1), 3–39.
       https://doi.org/10.1177/10944281251377154


                                                17

--- page 18 ---

Risko, E. F., & Gilbert, S. J. (2016). Cognitive offloading. Trends in Cognitive Sciences, 20(9),
       676–688.

Schildt, H. (2026). The case for artificial intelligence in qualitative research. Organization
       Studies. Advance online publication. https://doi.org/10.1177/01708406261452993

Shaw, S. D., & Nave, G. (2026). Thinking—fast, slow, and artificial: How AI is reshaping
       human reasoning and the rise of cognitive surrender [Preprint]. SSRN.
       https://ssrn.com/abstract=6097646

Strauss, A., & Corbin, J. (1990). Basics of qualitative research: Grounded theory procedures
       and techniques. Newbury Park, CA: Sage.




                                                 18
