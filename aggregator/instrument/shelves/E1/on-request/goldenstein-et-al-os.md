# Goldenstein, Jancsary, Grodal, Forgues and Jennings, Studying culture and meaning through interpretative computational methods, Organization Studies special issue introduction (accepted manuscript; year not checked)

Source: `intepretive_computational_methods_AAM.pdf`. Text extracted by pdftotext; layout kept, page breaks marked. A quote from this file is the extraction's, so check an odd word against the page it names.

--- page 1 ---

Introduction to the Special Issue

   Studying Culture and Meaning through Interpretative Computational Methods:

                                        From Theory to Method and Back


                                                   Jan Goldenstein (corresponding author)
                                                      Friedrich Schiller University Jena
                                                        jan.goldenstein@uni-jena.de


                                                           Dennis Jancsary
                    University of Liverpool Management School & WU Vienna University of Economics and Business
                                                   dennis.jancsary@liverpool.ac.uk


                                                                 Stine Grodal
                                                            Northeastern University
                                                          s.grodal@northeastern.edu


                                                              Bernard Forgues
                                                           emlyon business school
                                                           forgues@em-lyon.com


                                                        P. Devereaux (Dev) Jennings
                                                            University of Alberta
                                                              dj1@ualberta.ca




Declaration of conflicting interests
The author(s) declared no potential conflicts of interest with respect to the research, authorship, and/or publication of this article.

Acknowledgement
We are grateful to Organization Studies Editors-in-Chief Tammar Zilber and Paolo Quattrone for their valuable guidance in
compiling this special issue and for their supportive comments on earlier drafts of this manuscript. We also thank former Editor-
in-Chief Renate E. Meyer for her thoughtful recommendations and support in making this methodologically oriented issue possible.
Finally, we appreciate the efforts of the anonymous reviewers, whose constructive feedback provided invaluable support to the
authors of the articles in this special issue.

Funding
Jan Goldenstein declares that this work was supported by the Deutsche Forschungsgemeinschaft under Grant GO 3213/3-1.



This paper is the Author Accepted Manuscript (AAM), not the Copy of Record, and may therefore not exactly replicate the

final, authoritative version of the article. Please do not copy or cite without authors' permission. The final article is available

via its DOI: https://doi.org/10.1177/01708406251410383

--- page 2 ---

Introduction to the Special Issue

  Studying Culture and Meaning through Interpretative Computational Methods:

                              From Theory to Method and Back

Abstract

The convergence of expanded data availability, technological breakthroughs, and evolving societal

dynamics has rekindled scholarly interest in culture and meaning. Accompanying computational

methods are advancing rapidly across natural language processing, digital image processing,

machine learning, neural networks, and artificial intelligence, which creates unprecedented

opportunities for cultural meaning analysis. The introduction to this special issue advances

abductive theorizing and reflexive rendering to explore the dynamic interplay of theory generation,

measurement, and interpretation, highlighting common themes across its five articles. Our analysis

unfolds in three stages. We begin with an abductive examination of the culture and meaning

theories covered in the articles, exploring how they shape data selection and preparation, as well

as research designs for addressing theoretical questions. Next, we engage in reflexive rendering,

scrutinizing data characteristics and representations, methodological approaches, computational

methods, and the theoretical artifacts that emerge to advance theory development. Finally, we

discuss possible contributions, challenges, and concerns when organizational research examines

culture and meaning using computational methods.



Keywords: culture, meaning, organization theory, research methods, abduction, natural language

processing, digital image processing, artificial intelligence




                                                     1

--- page 3 ---

Setting the Scene

      The study of culture and meaning has been fundamental to the social sciences and the

development of modern organization theory (Bendix, 1956/2001; Hinings & Meyer, 2018;

Lounsbury & Gehman, 2024; Scott, 1981). “Culture consists of such symbolic vehicles of

meaning, including beliefs, ritual practices, art forms, and ceremonies, as well as informal cultural

practices such as language, gossip, stories, and rituals of daily life” (Swidler, 1986, p. 273). As a

multifaceted phenomenon, culture thus encompasses, “not only the environment that enables the

meaningfulness of social life but also a more specific set of scripts, narratives, embodied practices,

and schemas” (Mohr et al. 2020, p. 3). In this special issue, we focus on how our understanding of

culture and meaning can be augmented by utilizing computational methods.

      Culture establishes symbolic, moral and social boundaries (Lamont & Molnár, 2002).

Through symbolic boundaries, culture defines institutionalized and internally structured lenses

through which different communities of actors render the world understandable (Meyer, Jancsary,

& Höllerer, 2021), contour classification and orient practices (Goldenstein & Walgenbach, 2024;

2021). Culture’s moral boundaries determine which aspects of social and organizational life are

infused with value and delineate between the sacred and the profane (Durkheim, 1912/1995;

Douglas, 1966/2001). Culture also creates social boundaries, which divide social groups and

provide differential access to resources (Grodal, 2018). Social groups vary in their perceptions of

culture and meaning, which shape the boundaries which they create and the degree to which culture

is publicly shared or held as private beliefs (Valentino & Vaisey, 2022; Starr, 2021). However,

cultural boundaries are themselves shaped by how they are expressed and enacted by people

(Lounsbury & Ventresca, 2003; Mohr et al., 2020). Culture is thus not monolithic, instead social

groups create and are shaped by multiple and differentiated field logics (Thornton, Ocasio, &


                                                     2

--- page 4 ---

Lounsbury, 2012; Meyer & Höllerer, 2010), within which meanings are recursively and

symbolically related to practices, objects, temporalities, and spaces (Friedland, 2009; Goldenstein

& Walgenbach, 2024; Meyer, Leixnering, Kornberger, Jancsary, & Höllerer, 2024).

     Culture is intricately related to meaning in organizations (Giorgi, Lockwood, & Glynn,

2015). Organizations, just like other social actors, are both producers and products of culture

(Berger & Luckmann, 1966): they classify and evaluate but are also classified and evaluated; they

establish symbolic, morel, and social boundaries and are impacted by them; and they develop

meaning but exist as social actors only by virtue of certain meaning structures. Organizational and

managerial concepts and practices diffuse and are translated within and across fields and their

underlying logics (Boxenbaum & Jonsson, 2017; Sahlin-Andersson & Engwall, 2002).

     Accordingly, organizational analyses of culture and meaning require a sense of how cultural

boundaries are constructed in different historical, temporal, and local contexts. As fundamental

and powerful as the analysis of culture and meaning has been in the course of organizational

research, recent changes in society and technology are challenging them and require that we reflect

on our theories and methods (Bailey, Faraj, Hinds, Leonardi & von Krogh, 2022; Bechky & Davis,

2025). Technological advances, in particular the digitalization of verbal and visual forms of

communication, the proliferation of digital platforms, and the emergence of generative AI (Schildt,

2020), have created a vast, complex web of virtual linkages and activities across people,

organizations, societies and even AI agents (Vergne, 2020; Murray, Rhymer & Sirmon, 2021).

These changes are influencing how culture and meaning is constructed. The rate of communication

and the diffusion of ideas happen much quicker, with less scrutiny, and more frequently along

decentralized paths (Vosoughi, Roy & Aral, 2018).

     These changes have shaped who participates in the construction of culture and meaning by



                                                   3

--- page 5 ---

democratizing access to communication tools and reshuffling the traditional power position of

information gatekeepers such as professional organizations, media organizations, and elected

politicians while giving rise to others (Faik, Barrett & Oborn, 2020; Phillips, Kalvapalle &

Kennedy, 2024). Digitalization and the proliferation of platforms have created the possibility of

greater virtual freedom and coordination through greater participation in cultural construction

(Seidel, 2018); yet they have also enabled the centralized creation and control of culture and

meaning by technology firms and governments as part of “surveillance society” (Zuboff, 2022).

      The new participants and processes of cultural and meaning construction have consequences

for organizational research methods. Methods about culture and meaning have traditionally been

sensitive to interpretation via fine-grained, localized ethnographic techniques (Giorgi et al., 2015;

Langley et al., 2023). More recently, computational methods for studying culture and meaning

(e.g., Goldenstein & Poschmann, 2019; Friedland, Mohr, Roose, & Gardinali, 2014; Jancsary,

Meyer, Höllerer, & Barberio, 2017; Meyer & Höllerer, 2010; Poschmann & Goldenstein, 2022;

Wruk, Oberg, Klutt, & Maurer, 2019) have started to build on big and thick data on organizational

phenomena made possible by new forms of data and sharing of information in the digitization era

(DiMaggio, 2013; Kitchen & McArdle, 2016).

      Computational methodologies are now increasingly being further extended and refined

through natural language processing (NLP) and digital image processing (DIP), as well as recent

large language models and neural net-based transformers (e.g., BERTs and GPTs), which allow

for the processing of verbal and visual data in quicker, more impactful fashion than prior data

gathering, organizing, and analysis techniques (Nelson, Burk, Knudsen, & McCall, 2021; Than,

Fan, Law, Nelson, & McCall, 2025). This helps create broad, multi-modal data that grows or is

replaced with high velocity, hallmarks of “big data” (Kitchin & McArdle, 2016). The spread of



                                                    4

--- page 6 ---

open-source programming languages such as Python and R, make it possible to analyze big data

via powerful new techniques sensitive to language, visuals, and context (Bornakke & Due, 2018).

Such analyses include the utilization of word embeddings and topic modeling (Aceves & Evans,

2024; Hannigan et al., 2019; Poschmann, Goldenstein, Büchel, & Hahn, 2024), new forms of social

network analysis (Tonidandel, King & Cortina, 2018), discourse and sentiment analysis (Chen &

Mankad, 2024), or the algorithmic processing of digital images (Sgourev, Aaadland, & Formilan,

2023). Collectively, these new types of data, collection methods and forms of analysis can be

broadly understood as computational methods (Edelmann, Wolff, Montagne, & Bail, 2020).

      This special issue’s call has been for studies investigating culture and meaning in and around

organizations using computational methods (Goldenstein, Jancsary, Grodal, Forgues, & Jennings,

2022) to take stock of the evolving methodological landscape. Some previous and forthcoming

special issues, editorials, and key articles have discussed how the availability of massive data and

development of analysis methods are changing both how organizations operate and how we do

empirical research. Examples include the Organization Studies forthcoming special issue on

algorithmic organizing (Glaser, Moser, D’Adderio, Hannigan, & Pozner, 2024), the Academy of

Management Review’s special topic forum on theory in management research including Leavitt,

Schabram, Hariharan, & Barnes’ (2021) paper on machine learning, and the Academy of

Management Journal’s editorial on research opportunities with AI (von Krogh, Roberson &

Gruber, 2023). But there is still a paucity of work on ways to conjoin contemporary organization

theory on culture and meaning and established organizational methodologies with new forms of

big data and computational methods (Murray et al., 2021; Raisch & Krakowski, 2021). There is

also a lack of benchmarking for these computational analyses that can help establish protocols akin

to those for reliability and validity (Krakowski, Luger & Raisch, 2023). We propose that this



                                                    5

--- page 7 ---

benchmarking needs to be done through continuous human reflection about empirical endeavors

(Zilber, 2020), where researchers iteratively move between computational analysis and in-depth

qualitative understanding of the data to assess the contextual and theoretical significance of the

computational findings. Researchers thus need to resist the rampant automation of cultural and

meaning analysis if they are to create inspiring and novel theories which will move our

understandings of organizations forward (Bechky & Davis, 2025). Organizational scholarship

requires deep engagement and “concrete interaction with the world,” as well as community

through “both tacit and relational, originating in social interaction with our more experienced

colleagues” (Bechky & Davis, 2025, p. 11). The loss of the human interpretive craft would not

merely be a methodological issue; it would represent the erosion of the very mechanism through

which culture and meaning within general and scientific knowledge evolve.

      The variety of articles in this special issue showcases ways in which new data, new

methodology, and new tools can be combined with organizational theories and established

methodological approaches to apply and develop new benchmarks. Our orderings of the five

articles are meant to interrogate the relationships between theory (generation), measurement, and

interpretation, focusing on interfaces that we find particularly consequential. In other words, we

do not exhaustively discuss each article in turn but rather draw connecting lines across them to

highlight similarities and differences and enable insights on a more general level. To do so, we

rely on notions of abductive theorizing (Befar & Okhuysen, 2018; Mantere & Ketokivi, 2013), and

of iterative and reflexive rendering of data, models and theoretical artifacts (Hannigan et al., 2019;

Schmiedel, Müller, & vom Brocke, 2019) as fundamental to research design. Abduction starts with

the identification of an anomaly, that is an observation which cannot be explained by existing

theories (Behfar & Okhuysen, 2018; Sætre & van de Ven, 2021). Subsequently, researchers draw



                                                     6

--- page 8 ---

on their data to generate explanations for the occurrence of the anomaly (Mantere & Ketokivi,

2013). Lastly, researchers choose between the explanations to identify the one which is both

lovely—it fulfills the theoretical virtues of generalizability, parsimoniousness, and coherence—

and likely—it is consilient and consistent (Pillai, Goldfarb, & Kirsch, 2024). Practically,

researchers can use rendering to move between data and theory as part of the abductive process.

Rendering is “a three-part [computational] process of generating provisional knowledge by

iterating between selecting and trimming raw data, applying algorithms and fitting criteria to

surface measured constructs, and creating theoretical artifacts, such as processes, causal links, or

measures” (Hannigan et al., 2019, p. 591).

      In the first section—From Theory to Methods—we start with the theories of culture and

meaning (see Giorgi et al., 2015 for a review) covered in the special issue, and their implications

for assembling data and possible research designs to address their key research questions (Mohr et

al., 2020). In the following section—From Methods to Theory—we consider the details of the data

and their representations, the methods deployed, and the theoretical artifacts created that can help

to address the respective research questions and to build new theory. In the final section—

Contribution, Challenges, and Concerns—we close with a discussion of contributions, challenges,

and concerns for organizational research on culture and meaning with computational methods and

point to important areas for future research.



From Theory to Method

      To move from theory to method, we emphasize the importance of starting with an explicit

understanding of culture and meaning that allows for the precise definition of theory-based

constructs that can be adequately measured using computational methods (Poschmann et al.,


                                                    7

--- page 9 ---

2024). Accordingly, using abductive theorizing (Behfar & Okhuysen, 2018; Mantere & Ketokivi,

2013) and reflexive rendering (Hannigan et al., 2019; Zilber, 2020) as a lens, we organize the

articles in this special issue initially along the path from research questions based on real-world

problems or theoretical issues, through the undergirding theories and theory-based constructs

involving culture and meaning, to the chosen research design, in the rows of Table 1. The last row

of the table raises rendering challenges in each paper, which are discussed throughout the

subsections and in the final section of our introduction. In the columns of Table 1, we sort articles

based on the different domains of culture and meaning in which organizational settings and

dynamics are located within the respective articles. The vast diversity of domains and forms in

which culture and meaning become relevant for organizations and management have been

excellently covered by Mohr and colleagues (2020). In our reading, the articles in our special issue

focus on (societal) fields, skilled occupations, and industry categories.



                                     --- Insert Table 1 about here ---



Frames and institutions as cultural features of fields

      In the first article, Etchanchu, Aranda, Harmon, and Ansari (2025) focus on a comparison of

national field-level debates on shale gas and fracking in Germany versus France to investigate “if

(and how) unique historical differences between countries might influence the emergence of field-

level frames”. Field-level frames act as orienting devices that enable actors to make sense of

contentious issues and coalesce around meaningful action (e.g., Benford & Snow, 2000;

Cornelissen & Werner, 2014). Etchanchu and colleagues argue that previous work has neglected

to deeply engage with where frames come from, in both symbolic and material terms. Doing so



                                                     8

--- page 10 ---

comparatively allows researchers to investigate these early versus latter field moments. They show

that issues such as fracking are first historically positioned in wider conversations and prior

policies, including those about national politics and energy. Issue labelling is then used as a

mechanism to shift the issue and create new frames that allow some form of bounded mobilization.

      The authors’ research design constitutes an interesting use case of how discursive data

covering two language communities over a five-year period can be analyzed with structural topic

modeling (STM) with temporal covariates to determine the contour of field-level frames. It also

shows how such analysis can be complemented with rich interview data to explain why historical

context shapes the emergence of different field-level frames. However, one very difficult reflexive

rendering problem was to convincingly link mechanisms (i.e., historical positioning, issue

labelling, and bounded mobilization) to each country’s framing debate in a way that can illuminate

commonalities and differences between each field’s cultural responses. To do so, the authors

demonstrate the early rise of regulatory framing of fracking in France compared to the later, more

environmental framing in Germany, which implies that frames did not follow lock-step diffusion

patterns; rather, the frame evolutions were consistent with each country’s history and political

context. In a sense, this implies stronger societal bounds on fields than usually implied by reviews

of framing (Cornelissen & Werner, 2014; Gray et al., 2015).

      In the second field-level article, Brandtner, Ashur, and Desikan (2025) examine institutional

dynamics within a single cultural context, but over a longer period and with more historical depth

than can be achieved across multiple cases: the municipality of Vienna and the institution of public

housing from 1867 to 2009. They seek to “model the persistence of institutions [like public

housing] while honoring earlier insights that institutions change with varying pace, quality, and

connections to the wider institutional context.” Like Etchanchu and colleagues (2025), the authors



                                                    9

--- page 11 ---

maintain that the history and broader political context of the municipality can be analytically

distinguished from the evolution of its central institutions such as public housing. This analytical

move allows the researchers to analyze the dynamics of public housing against the background of

broader societal changes, showing that while the concrete instantiations of the institution changed

over time, the institution’s core still proved persistent.

      However, the article faces a considerable reflexive rendering challenge when theorizing a

dynamic model containing so many fluid and interdependent cultural elements. To address the

challenge, the authors develop dynamic modeling of discourse (DMD) as a theory-method

package, adapting historical topic modeling of a large, longitudinal data set to address their

research question. A key theoretical move that makes their case suitable for computational analysis

is to maintain that in each period, instantiations of institutions reflect their key attributes in

discursive terms; that is, in vocabulary that includes terms such as “flats,” “rents,” and “subsidies.”

These terms represent different approaches to public housing, such as found in different formative

historical periods of the city. Together, the differing instantiations and yet enduring nature of the

institution show its dynamic persistence (see also Colyvas & Powell, 2006; Haveman & Rao, 1997;

Leixnering, Meyer, & Doralt, 2022), which has so far been difficult to demonstrate convincingly

due to the need to study large amounts of data in detail over the longue durée.



Cultural dynamics of skilled occupations

      Turning to dynamics in skilled occupations, Efthymiou, Kackovic, Rudinac, Wijnberg, &

Worring (2025) ask to what extent the visual originality of artists at the time of their artworks’

creation predicts their long-term evaluations and canonical standing. After all, we are all aware of

artists who were less recognized in their era than some of their contemporaries (Duchamp and



                                                      10

--- page 12 ---

Picasso, respectively), yet who later gained substantial recognition and are considered even more

avantgarde in hindsight. This article expands the study of culture and meaning to visual text (e.g.,

Meyer, Höllerer, Jancsary, & Van Leeuwen, 2013) and relies on notions of materiality and

aesthetics (Boxenbaum et al., 2018; Baldessarelli, Stigliani, & Elsbach, 2022), the sociology of

evaluation (Lamont, 2012), and work related to the originality of cultural products (Banerjee, Cole,

& Ingram, 2023). Efthymiou and colleagues hypothesize positive effects of visual originality on

artists’ standings in the three different evaluation systems––expert, peer, and market. This allows

for artists’ standing to cascade across all evaluation systems, or to be initially restricted to one

system (yet later become more manifest in others). The theoretical framework’s flexibility in

handling meaning across different cultural milieus and indices of evaluation fits well with modern

views of creativity in cultural sociology, which embrace both Bourdieu’s (1984) cultural capital

views as well as market approaches (Godart, Seong, & Phillips, 2020).

      A strength of this article is that it not only illustrates computational methods for the analysis

of visual material but also showcases how theory and methodology need to be considered in

tandem to design a compelling approach to capturing the visual originality of an artwork in relative

terms, considering both relations to immediately preceding eras and concurrent stylistic

movements. Accordingly, a strong reflexive challenge is capturing the in-situ originality and

relative standing as viewed by historical participants at the time, plus developing a theory that is

robust enough about changes in notions of aesthetics (Krabbe & Grodal, 2023). For this purpose,

the study employed neural-net processing to construct an originality measure of each artwork

relative to previous works and within the stylistic movement, generates rankings with the help of

large language models (LLMs), and then runs OLS regression of originality on artists’ standing in

the three different evaluation systems.



                                                     11

--- page 13 ---

In the second article on skilled occupations, Santana and Kim (2025) contrast Efthymiou and

colleagues’ (2025) external, social evaluation focus by asking “how an occupational community

with diverse ethical values comes to agree on a shared code of ethics” in the context of software

engineering. Research on occupations and professions has examined the development and

institutionalization of occupations, with ethical codes playing an important role as published

documents that are intended to set standards for appropriate behavior in an occupation and reflect

deeper moral values (Abbott, 1983; Gehman, Treviño & Garud, 2013). Recent work, such as by

Evans (2021) on stem cells, has looked at the expression of values in codes. However, the

discursive dynamics of how occupations negotiate and eventually agree on the inscription of

specific values in codes have not been examined in much depth.

      This article demonstrated how multiple computational analyses can be combined and

enhanced with contextual information to both show and theorize discursive dynamics. The authors

draw on a remarkable data set––the entire corpus of emails exchanged by members of the task

force drafting the code of ethics––which documents the codification process. A key challenge was

to establish a link between dynamic changes in the dominant vocabulary within email exchanges

and the code of ethics that was ultimately agreed on. To do so, the authors argue that emails capture

sociolects, that is, specific languages used by a group of professionals, and thus reflect ethical

subcultures and internal struggles to establish shared values. These sociolects are reconstructed

through semantic network analysis (e.g., Höllerer, Jancsary, Barberio, & Meyer, 2020; Mohr,

1998), while topic modeling (e.g., Hannigan et al., 2019; Goldenstein & Poschmann, 2019) was

employed for reconstructing dynamics of convergence toward and divergence away from

agreement on values over time. The semantic structure of the email discourse in different periods

is compared to that of the eventually adopted code. Prior ethnographic accounts of the research



                                                    12

--- page 14 ---

case are mobilized to contextualize the findings and capture how task force members used their

power and status to influence the codification. Santana and Kim (2025) focus on the discursive

moves around debates about the code of ethics that helps fine-tune earlier work, such as that of

O’Mahony and Ferraro (2007) about the role of authority and power in communities, because they

address the question of how values become ensconced even when the community itself is not yet

well-formed.



Category positioning as cultural conformity and uniqueness

      The special issue’s final article on category outliers––firms participating in markets that

stand out through their extreme and ambiguous performance––by Gouvard and Durand (2024)

concerns firms and industries. The authors ask “how prototype similarity and outlier similarity

simultaneously affect how investors value an issuing firm in the initial public offering (IPO)

market”. In some ways, this is an extension of Efthymiou and colleagues’ (2025) considerations

about social evaluations, where positioning and value are associated and based as much on the

audience as on the producer. Gouvard and Durand (2024), however, employ a categories approach.

Categories are a structuring feature of culture and embody patterns of meaning by summarizing

information on symbolic and material attributes of products and firms. Categories are defined by

their prototypes and serve as reference point to define new firms’ positions relative to them (Negro,

Koçak, & Hsu, 2010).

      The authors argue that while an IPO in a prototype industry category is inherently uncertain

and risky, if investors are familiar with the industry and features of a firm, they should be able to

do a better job of pricing (i.e., not underpricing the firm). In contrast, new offerings similar to high

performing category outliers––i.e., “unicorns”––from the previous year will garner even more



                                                      13

--- page 15 ---

attention, but there will be less certain information about these outliers, leading to underpricing.

The authors use trained word-embedding models on large numbers of IPOs across multiple

industries over time to set up the category system and the positioning of firms within it (also see

Wry, Lounsbury, & Jennings, 2014). Fixed effect regression models with many industry and firm

controls are used to demonstrate how both prototype and outlier positioning jointly play out in

terms of underpricing. The key rendering challenge here was to show that outliers identified by a

complex multi-category measure actually capture category outliers, not just a salient (bandwagon)

effect of prior year’s success.



Learnings from the theory to method path

      In accordance with abductive theorizing, we distil several learnings from the five articles in

our special issue. These learnings concern the move from a theoretical research question about

culture and meaning in a specific research context to the research design of the study.

      First, based on our cross-sectional reading of the various articles, we emphasize the

importance of clearly situating issues of culture and meaning in the theoretical positioning and

empirics. Without a proper understanding and definition of what culture and meaning are and

where they reside (see also Mohr et al., 2020), it will not be possible to usefully design methods

and empirics. The options to define culture and meaning are manyfold, but they need to be clearly

argued and justified. For instance, Etchanchu and colleagues (2025) theoretically discuss why

historical trajectories of national cultural contexts restrict options for the generation of meanings

(in form of field-level frames) in the present. Santana and Kim (2025) understand codes of ethics

as a normative guideline for an occupation’s legitimate cultural practices, therefore reflections of

shared meanings. In Gouvard and Durand's (2024) study, market categories serve as cultural-



                                                    14

--- page 16 ---

cognitive carriers of meaning, as they transport shared understandings of symbolic and material

attributes and distinguish between entities.

      Second, we highlight that, based on the clarification of culture and meaning, scholars need

to develop theory-based constructs suitable for computational analysis. This step already requires

thinking in terms of methods and measurement (e.g., Mohr, 1998). Importantly, however, to move

convincingly from theory to method, the decisive factor should not be the envisioned

computational method but the research question and the respective definition of culture and

meaning. In this spirit, Brandtner and colleagues (2025) adopt a theoretical approach that

distinguishes institutions from their instantiations, where the malleability of the meanings of the

latter is directly observable, making it conducive to measurement. In a similar vein, Efthymiou

and colleagues (2025) make the construct of visual originality observable by arguing that

originality assesses the “novelty of an artwork compared to its most similar predecessor, which

may even be one from the distant past.” The two articles thus illustrate the move from theory to

method, starting with coherent definitions of culture and meaning, through the linking of these

definitions to theory-based constructs, to operationalization and measurement.

      Third, moving from theory to method also involves considering potential limitations of

computational approaches for addressing the research question at an early stage, as studies of

culture and meaning––in the tradition represented in this special issue––regularly require

triangulation, interpretation and iteration (e.g., Nelson, 2020). One learning is that the output of a

particular computational method often needs to be complemented with additional data and

supplementary analyses to answer the research questions exhaustively and validly. The limitations

of computational methods may necessitate the search for more complex theoretical inferences,

such as the mechanisms that explain why history influences field-level frames (Etchanchu et al.,



                                                    15

--- page 17 ---

2025) or the rich and distinct historical context of an occupation that shapes the discourse on codes

of ethics (Santana & Kim, 2025). Examining such early on helps ensure that computational

methods are understood as tools designed for specific purposes rather than a substitute for

interpretive engagement with the data and the relevant context.



From Method to Theory

      In this section, we emphasize the path from data selection and preparation to (computational)

methods and measures to fully rendered theoretical artifacts for the development of new theory

(Poschmann et al., 2024; Edelmann et al., 2020; Hannigan et al., 2019; Schmiedel et al., 2019).

Compared to conventional operationalization and modeling approaches, the use of computational

methods for an analysis of culture and meaning, as presented in our special issue, requires more

analytical steps, including several recursive interpretative loops (Mohr et al., 2020). Just as

important as the definition of theory-based constructs (see the previous section) are the next steps

to ensure empirical reliability and validity. These steps include (a) data selection and pre-

processing, (b) selecting computational methods/tools for text or visual analysis and the creation

of theory-based measures, and (c) generating theoretical artifacts for new theoretical insights

(Poschmann et al., 2024). We propose that these steps allow us to build new computationally

informed theory about culture and meaning in organizational domains, such as fields, occupations,

and industries.

      The analytical steps are displayed in the rows of Table 2. We will address each row

separately to illustrate and compare how the five articles deal with the respective analytical steps.



                                     --- Insert Table 2 about here ---


                                                    16

--- page 18 ---

Data selection and pre-processing

     The environments of organizations, and, more specifically, the complex social spaces within

which organizations are situated––such as fields and national contexts––are typical focal points

for analyses of culture and meaning (Giorgi et al., 2015; Goldenstein, Poschmann, & Hunoldt,

2023; Zietsma, Groenewegen, Logue, & Hinings, 2017). These types of analysis require thick

data––high-quality, context-rich data that enables in-depth, domain-specific inquiry (Bornakke &

Due, 2018; Mohr et al., 2020). For example, scraping the Web, accessing large organizational

archives, and application programming interfaces (APIs) can provide relevant domain information

(George, Osinga, Lavie, & Scott, 2016). While thick data does not necessarily have to be “big”

data in terms of volume, variety, and velocity of generation (Kitchin & McArdle, 2016), the five

studies illustrate that thick data need to be (and can be) more representative and complete than

ever before. In this sense, the quest to analyze thick data with computational methods requires

researchers to consider what type of data best represents the unit of analysis and how data must be

pre-processed to become high-quality and relevant for a given research question.

     To study how historical context shapes the construction of cultural frames in public debates,

Etchanchu and colleagues (2025) draw on data that covers the public sphere and provides nuanced

insights into the mechanisms that explain the dynamics within fields. Specifically, they collected

15,886 French (2006-2015) and 13,434 German (2007-2015) newspaper articles. Additionally,

they supplemented these articles with 78 interviews with industrialists, environmentalists, and

politicians to deepen insights gained from their computational analysis of public discourse.

Similarly, Brandtner and colleagues (2025), to investigate the meaning evolution of the public

housing institution in Vienna, analyze municipal yearbooks regularly published by the city. As



                                                   17

--- page 19 ---

public housing has always been a political issue, this is an appropriate data source. The authors

back up insights from yearbooks with further archival documents to help confirm the twist and

turns in the meaningful instantiations of the public housing institution.

      Both studies not only use impressive data sets that adequately capture their theory-based

constructs (i.e., cultural frames, public housing institution) but also supplement or cross-check the

results obtained from one data source with data from another source. Moreover, the size of the two

datasets pushed the authors to either select theoretically representative slices of the data (i.e., five

years of intense debate) and buttress the findings using traditional methods (interviews in

Etchanchu et al., 2025) or to focus the data on critical language artefacts (176k tokens in Brandtner

et al., 2025). This shows that even in times of computational methods and availability of large

datasets, triangulation of multiple sources remains important.

      The two articles on skilled occupations rely on datasets similar to, yet distinct from, the

articles focusing on fields. Studying recognized art over the very long period of 600 years requires

Efthymiou and colleagues (2025) to focus their analysis on excerpts of the art field’s evolution to

remain representative and complete enough when tracking the social evaluations of artwork. That

is, the authors analyze 60,011 artworks but focus on only 942 high-end painters. The selection of

key painters and their corresponding creative periods reduces the analytical effort and makes

theoretical conclusions more convincing. The authors then draw upon online sources to capture

expert, peer, and market evaluations of these paintings in more recent years (see also Banerjee et

al., 2023). As a result, dataset curation enables the authors to examine the current painter/artwork

standings in relation to the evolution of their cultural meanings. The article by Santana and Kim

(2025) on the development of a code of ethics in the Software Engineering Ethics and Professional

Practice Committee over a period of eight years has a much narrower focus. The corpus of email



                                                      18

--- page 20 ---

correspondence between committee members forms the core data (N=613). Further, the emails are

supplemented by highly proximate ethnographies to help contextualize the exchanged messages.

Whether and how exactly a shared set of professional or occupational values (i.e., as represented

in the code of ethics) emerges from these emails cannot be fully documented with email data alone,

but such data are useful for capturing that early process of professionalization and

institutionalization of key values in occupations (Barley & Kunda, 2011).

      In contrast to the previously discussed works, the article by Gouvard and Durand (2024)

relies on more established units and levels of analysis: 3-digit SIC classified firms and firm

operations as detailed in Platinum, CRISP, and COMPUSTAT databases. Due to an extensive

sample of 2,488 SEC-registered IPOs and 33,308 established firms within approximately 200

industries from 1996 to 2015, the authors were prepared to easily convince readers of the corpora’s

representativeness and completeness. Setting up the analysis, however, resulted in a huge database

containing financial and text information: a pre-processing, reducing move was needed. The data

is focused on establishing category prototypes and outlier similarities, which is based on cleaning

and parsing the data down to the 10,000 most frequently used words.

      In summary, the selection of data and pre-processing were important issues for all articles in

our special issue. Solving both issues is crucial to creating a suitable foundation for the subsequent

analytical steps. As textual or visual pre-processing decisions (e.g., removing visual tags, using

stop words or lemmatizing words) are highly dependent on the data and often are highly technical

in nature, we cannot go into detail here but instead recommend following established guidelines

to ensure the validity of pre-processing (Hickman, Thapa, Tay, Cao, & Padmini, 2022).



Selection of computational methods and the creation of theory-based measures



                                                    19

--- page 21 ---

The selection of computational methods, theory-based measures, and the tools to create them

deserves particular attention. In selecting computational methods for verbal and visual analysis, a

crucial requirement is to justify the fit between the use case of the method (i.e., what it is

technically designed to do), the definition of the theory-based constructs, and its linguistic or visual

manifestation (Edelmann & Mohr, 2018; Poschmann et al., 2024). In this sense, researchers need

to choose carefully the computational methods that help build up their study’s central storyline

(Nelson, 2019).

      The two articles on fields (Etchanchu et al., 2025; Brandtner et al, 2025) employ variants of

topic modeling, a computational method building on unsupervised machine learning. Topic models

detect numbers of distinct topics according to linguistic-based distributions, particularly the

exponential nature of high versus low probability words in discourse, plus the ability to parse

words in documents into single, separable words while retaining the word’s meaning (Blei, Ng &

Jordan, 2003). Topic modeling allows for cultural devices that transport and shape meaning, such

as frames and institutional instantiations, to be identified, proxied, and related to each other

(Hannigan et al., 2019) or to underlying structural lattices (Mohr et al., 2020). As both studies

require a computational method that allows meaning to be measured as word clusters that either

represent directly the vocabulary of frames or, when their composition is considered, reflect how

linguistic manifestations of institutions shift, topic modeling is well suited.

      There is some variation in types of topic modeling, which has additional implications for

uncovering meaning and detailing culture associated with organizational contexts. Standard Latent

Dirichlet Allocation (LDA) is most flexible for eliciting topics, their keywords, and associated

authored documents; but structural topic modeling (STM) as employed in the article by Etchanchu

and colleagues (2025), via the computation of meta-data from the corpus, allows researchers to



                                                      20

--- page 22 ---

correlate topics with covariates such as time or actor characteristics. Dynamic topic modeling

(DTM), as used by Brandtner and colleagues (2025), goes further, slicing time in the LDA,

showing topic evolution, plus allowing for associated structural topic modelling; of course, it also

requires more fine-grained textual data (Grimmer, Roberts, & Stewart, 2022).

      Next, we turn to the articles on skilled occupations. In the article by Efthymiou and

colleagues (2025) we see somewhat advanced mathematical versions of computational methods.

The study, even for pre-processing steps, relied on a convolutional neural network analysis of

pixels-based RGB vectors from ImageNet. This program is powerful, but its workings are not

transparent and are only supervised in terms of tuning steps: the training data, iterations, and

chosen outputs. The same can be said of the RoBERTa algorithm being used for named entity

recognition (NER) in the same article. Hence, one of the main points for interpretive data science

supervision is in the construction and assessment of the measures themselves. The cosine distance

measures and their meaning in terms of artwork originality––just like rank measures for

evaluation––are adjustable. Assessing originality requires choosing the number of comparators,

the time period, and deciding where a movement cuts off (and whether the qualitative data fit that

measure). Creating rankings by period and audience requires similar decisions. The authors offer

some description of the measures and choices, and more details in their methods appendix.

      As for Santana and Kim (2025), they ran a semantic network analysis by applying a

community detection algorithm––the Louvain method––to identify actor sub-communities (called

sociolects) and then measured consensus through semantic distances in discourse. Semantic

network analyses are excellently suited to inferring meanings from co-occurrence patterns among

words/concepts within texts (Carley, 1994; Jones et al., 2012). On the level of the individual word,

such method can, for instance, assess the centrality of a specific word in the discourse based on



                                                   21

--- page 23 ---

the strength and number of incoming and outgoing ties, or the role of a word in bridging otherwise

unconnected parts of the discourse (in analogy to people bridging structural holes in social

networks; see Burt, 1992; Korff, Oberg, & Powell, 2015). Santana and Kim (2025) focus on the

level of the entire network, using community detection to study dynamics in the modularity of the

discourse (i.e., the prevalence of word clusters that are more densely connected internally than to

words outside the cluster; see also Höllerer et al., 2020). This allows the authors to assess whether

debates lead to convergence (decreasing modularity through merging clusters/sociolects) or

divergence    (increasing    modularity     through        strengthening   of   boundaries   between

clusters/sociolects) of competing values.

      The article on category outliers also relies on a similarity measure. Gouvard and Durand

(2024) trained a document embedding model to measure similarity between documents (annual

reports). The tool to obtain document embeddings is Doc2Vec (short for Document-to-Vector),

available in both R and Python. Through the documents they issue, firms are located in a

multidimensional semantic space, resulting in a vector of firm embedding (for a general discussion

of multidimensional semantic spaces, see Aceves & Evans, 2024; Poschmann et al., 2024). As the

authors define product categories as symbolic attributes of firms, they focus on semantic similarity

of organizational self-representations in annual reports. Averaging firm embeddings in a given

industry reveals the industry prototype. To measure how similar a firm is to the industry prototype

or to the most salient prototype of the previous year, they use the standard cosine distance. An

interesting avenue for future work relying on such complex measure creation is to compare with

other computational methods to establish benchmarks. For example, similarity between firms

could be calculated using the output of topic modeling as input for vector spaces (e.g., Haans,

2019).



                                                      22

--- page 24 ---

Theoretical artifacts and theoretical insights

      Theoretical artifacts are computational outputs that can be translated or transformed into

quantitative or visual representations of theory-based constructs. Examples include

multidimensional maps, word clusters, visual tags, and similarity measures. For example, the

standard output of LDA topic modeling is a distribution of topics represented by clusters of words.

While researchers could already use this distribution of topics as a theoretical artifact, the output

of topic modeling enables the generation of even more advanced artifacts, which, however,

requires further processing steps. Topics can be used to construct two-dimensional maps using

principal component analysis or serve as the basis for correlational networks in which topics are

related to each other based on the similarity of their word clusters. Structural topic modeling (STM)

can further construct graphs showing, for example, how topics vary over time, by place, or actor

(Hannigan et al., 2019; Goldenstein & Poschmann, 2019; Schmiedel et al. 2019; Grimmer et al.,

2022). The display of topics, their composite key words, and their labels are a theoretical artifact,

akin to a Gioia thematic coding diagram (Gioia, Corley, & Hamilton, 2013). Finally, the output of

topic modeling can be used to create similarity measures as theoretical artifacts. In this context,

the relative frequencies of topics serve as dimensions that can be used to compare entities such as

organizations (Haans, 2019; Poschmann et al., 2024).

      Regardless of how scholars use the output of topic modeling, it offers a wide range of

possibilities for capturing interesting theory-based constructs and thereby allows for complex

theory building. In our special issue, both Etchanchu and colleagues (2025) and Brandtner and

colleagues (2025) employ some of the aforementioned opportunities of topic modeling, examining

how topics and their composition denote either frames or institutional shifts over time. Etchanchu



                                                    23

--- page 25 ---

and colleagues (2025) focus more on documenting how meaning varies by national contexts (i.e.,

countries as overtime covariates). Using a correlational network of topics as theoretical artefact

allows them to draw insights about which framing of shale gas extraction was prevalent where and

how a frame was tied to others as part of fracking’s translation and elaboration. Brandtner and

colleagues (2025) focus on shifting compositions within the word clusters that represent public

housing topics to capture changes in instantiations of the persistent institution of public housing.

The article also displays topic proximities and a heatmap of the relevance of topics over time to

show the enduring yet increasingly entangled and complex nature of the public housing institution.

      For Efthymiou and colleagues (2025), the theoretical artifact is a similarity measure that

captures the distance between the feature vectors of artworks. The authors construct feature vectors

using visual information as dimensions and compare their presence or absence in different

artworks. They use their similarity measure to compute the visual originality of artworks in a

specific time period relative to prior and current work (and/or style). Additionally, the authors

compute artists’ rankings as theoretical artefacts from named-entity recognition counts, which they

compare over time and across artists to operationalize artists’ standings. Such ranking methods

and the meaning of rankings as a theoretical artefact are well established in the literature (Sharkey,

Kovács, & Hsu, 2023). Santana and Kim (2025) focus attention on sociolects, a concept which the

authors mobilize to theorize the cliquing of committee members across emails. The authors trace

the dynamics of these sociolects based on the theoretical artefact of semantic communities (i.e.,

sociolects as word clusters) in a network of communication participants. As the discourse shifted

from multiple competing sociolects to a more unified narrative, the occupation’s values became

ensconced in the code of ethics.

      Finally, Gouvard and Durand (2024), like the article on originality in art, use a similarity



                                                     24

--- page 26 ---

measure as theoretical artefact. The authors use this measure to capture whether an organization is

more similar to prototypical category members or category outliers.



Learnings from the method to theory path

      According to the logic of reflexive rendering (Hannigan et al., 2019; Schmiedel et al., 2019),

it would seem useful to view the path from method to theory as a logical continuation of and

closely linked to the respective path from theory to method. We do see fit of the two paths across

our Tables 1 and 2, but not as tightly as one would find in a “theory-method package” (Gehman et

al., 2018), with the notable exception of Brandtner and colleagues (2025). However, we find a

configurational, contingent relationship of theories of culture and meaning in and around

organizations to computational methods and their interpreted results across the respective studies.

From our cross-sectional reading, we can, again, distil general learnings, which resonate with

previous work (Poschmann et al., 2024).

      First, the five studies highlight the importance of the selection of data and suitable pre-

processing as part of researchers’ interpretive effort. Big and thick data often provides an

overabundance of information. While computational methods are uniquely able to deal with such

amount and complexity of data, the art lies in decisions about what parts of the data are conducive

to and required for the respective research aims (e.g., Efthymiou et al., 2025). Furthermore, the

reduction of ‘noise’ is a crucial step and, we would argue, part of interpretive engagement with the

data, as these decisions cannot always be fully automated. Accordingly, we see how most authors

in this special issue, as well as others employing computational analysis, start the pre-processing

of their corpora by cleaning parts of it manually to familiarize themselves with the data and set up

adequate cleaning protocols (Schmiedel et al., 2019; Hickman et al., 2022). For instance, Gouvard



                                                   25

--- page 27 ---

and Durand (2024), on top of standard pre-processing steps like removal of punctuation, digits,

and stop words, also decided to remove technical terms of SEC filings to increase the

meaningfulness of the list of tokens used for analysis. Brandtner and colleagues (2025) not only

proofread large parts of their topic modeling output to fix systematic and idiosyncratic spelling

errors but also invested considerable effort into defining suitable periods based on approximately

3,000 pages from their data.

      Second, the five studies are good examples of how important it is to make well-informed

decisions about suitable computational methods for the theoretical framework and data at hand.

While this requirement does not need much explanation, it is far from straightforward. As a rule,

the intended use of computational methods must match the definition of theory-based constructs

and their manifestation in text or visuals. For example, Santana and Kim (2025) argue that

sociolects reveal groupings of ethical values in communities through similarities in language use.

Accordingly, the authors can theoretically justify the use of an algorithm for community detection

in semantic networks. Efthymiou and colleagues (2025) theoretically justify that artworks can be

technically represented as collections of visual tags that specify the objects in the artwork. To

predict the appearance of these tags on artworks, the application of convolutional neural networks

(CNNs) is appropriate because CNNs are currently state-of-the-art to classify and detect visual

content.

      However, the existing set of computational methods––including the different

implementations of some approaches like grammatical parsing, topic modeling, or word

embedding––has reached a considerable breadth and diversity. At least for interpretive endeavors,

it is important to emphasize that there are no hard and fast rules about what implementation is best

suited for any endeavor. While guidance exists in the literature (e.g., Grimmer et al., 2022;



                                                   26

--- page 28 ---

Poschmann et al., 2024), no guidelines can replace in-depth engagement with the requirements of

the specific research question, the respective understanding of meaning and culture, as well as

theoretical mechanisms under investigation. For example, to measure theoretically conceived field

dynamics, our special issue authors select different topic modeling implementations to account for

the specificities of their definitions of culture and meaning, as well as their research setting.

Etchanchu and colleagues (2025) apply structural topic modeling (STM) because this

implementation is well-suited for comparative frame analyses by using the two different national

contexts as covariates. In contrast, as their aim is to capture instantiations of an institution over

time, Brandtner and colleagues (2025) develop a theory-method package that allows them to

measure the dynamic composition of topics via dynamic topic modeling (DTM). Efthymiou and

colleagues (2025), in turn, employ architecture for tag prediction that was specifically developed

for fine art analysis and focuses entirely on the artworks’ visual surface. Across all studies, fine-

tuning computational models for the specificities of the research is key.

      Third, a crucial challenge is how to develop novel theory from the theoretical artefacts

generated by computational methods. There is an important connection to the theory-to-method

pathway implied here: computational methods can produce output relevant for theory building

only if culture and meaning are appropriately defined and concretized through theory-based

constructs. Additionally, the selected computational methods must meaningfully capture the

theory-based constructs at hand. Again, we can identify configurational patterns in the five articles

in our special issue. One pattern is around theorizing the meaning of cultural entities such as

artworks (Efthymiou et al., 2025) or products (Gouvard & Durand, 2024) to operationalize their

distinctiveness by calculating degrees of similarity. Another pattern relates to the degree of

abductive or deductive theorizing that guides the research (Mantere & Ketokivi, 2013). More



                                                    27

--- page 29 ---

abductive theorizing, which we see in the articles by Etchanchu et al. (2025), Brandtner et al.

(2025), and Santana and Kim (2025), requires theory building about processes, mechanisms, and

outcomes, and compelling arguments on how computational methods can help make that link. The

main contingency of the three articles is to align theory building with an abductive approach to

methodology and vice versa, and to motivate such research design from the beginning. In more

deductive research, in contrast, theory-based constructs like visual originality (Efthymiou et al.,

2025) and category outliers (Gouvard & Durand, 2024) can be theorized and then computed

somewhat independently from the host of factors that affect them. Then, these operationalized

theory-based constructs can be used as dependent and independent variables. Such insights clearly

illustrate that theory building on culture and meaning needs to be the connecting thread across the

entire research project, from the development of theory-based constructs to the choice and

adaptation of computational methods, to the generation and interpretation of theoretical artefacts.

      Fourth and last, although this has not been discussed in detail in our essay so far, the articles

in the special issue are cautious to employ relevant robustness and validation checks to enhance

the plausibility of theoretical insights, even if these checks cannot replace plausibility with

certainty. Indeed, there is the risk that the output of computational methods is regarded as

“statistical objectivity [that masks] the subjective decisions that are necessary to measure meaning

in big data” (Nelson, 2019, p. 140). Mindful of the inherently interpretative nature of

computational models, researchers can use a variety of techniques that we can broadly categorize

as grounding and sensitivity approaches. Grounding refers to ways in which researchers gauge the

output of computational methods against data and qualitative evidence, thereby enabling

triangulation of findings across multiple data sources. For example, Santana and Kim (2025)

integrate semantic networks with qualitative historical analysis, thereby verifying that results



                                                     28

--- page 30 ---

obtained with different methods were consistent. Sensitivity refers to statistical techniques where

researchers vary parameters (including those based on subjective decisions) or settings to check

how this impact results. For example, Gouvard and Durand (2024) use different specifications for

Doc2Vec––which changed their independent variables––and verify that results replicated

satisfactorily. Efthymiou and colleagues (2025) offer another example. The authors compute

distances between artworks created in different time windows and find that their results are robust.

More generally, we argue that robustness and validation checks are crucial because computational

methods are inherently interpretative, evolve rapidly, and do not necessarily meet established

criteria for validity and reliability, as they were not designed exclusively for research in the social

and organizational sciences.



Contributions, Challenges, and Concerns

      Our introduction to this special issue and reprise of the articles in terms of pathways from

theory to method and from method back to theory has shown how culture and meaning (a) are

defined and situated in different domains––fields, skilled occupations, and industry categories––

and (b) have inspired research designs that employ big and thick data and computational methods

in order to generate theoretical artifacts that enable novel theoretical insights. Each major section

of this introduction discussed how the various articles rendered theory and method, including

summaries of central learnings for how to set up computational analyses in organizational research.

In the concluding section, we briefly outline what we see as the main contributions of

computational methods to the study of culture and meaning, provide thoughts on enduring

methodological challenges, and share broader concerns about the application of computational

methods.


                                                     29

--- page 31 ---

Contributions to the study of culture and meaning

      An obvious contribution of computational methods to the study of culture and meaning is

the ability to analyze millions of data points automatically and with increasing technical validity,

thereby affording opportunities to benefit from the availability of big and thick data. However, we

would like to stress that the quantity of data by itself is not sufficient argument for the use of

computational methods; rather the analysis of this data must also offer the prospect of enhanced

theoretical insights. This is the case, for instance, when computational methods are used to conduct

previously unavailable comparative and longitudinal studies across multiple cultural contexts (e.g.,

Etchanchu et al., 2025) and over long periods of time (e.g., Brandtner et al., 2025; Efthymiou et

al., 2025), which require substantial amounts of data to support robust insights. However, as the

article by Santana and Kim (2025) show, powerful computational methods can also be usefully

applied to smaller datasets. In this sense, we argue that the ability of computational methods to

process data deeply is necessary when studies aim at measuring latent theory-based constructs that

are hidden in meaning structures such as the similarity of vocabulary or visual features (e.g.,

Efthymiou et al., 2025; Gouvard & Durand, 2024). We argue that theory-based constructs of this

kind are difficult to capture on a large scale with traditional quantitative methods such as surveys.

At the very least, computational methods provide an additional valid option for capturing theory-

based constructs based on different data types, thereby increasing robustness.

      Moreover, computational methods are particularly useful for identifying and reconstructing

patterns of meaning that are inaccessible to traditional interpretive analyses—especially when such

patterns are latent, embedded in complex structured and unstructured data, or only become

apparent across large volumes of data or extended timeframes (Edelmann & Mohr, 2018). In this



                                                    30

--- page 32 ---

context, computational methods allow patterns to emerge from the data without researchers’ initial

intuitions and preliminary theoretical considerations. This includes, for instance, the detection of

semantic communities across entire discourses (e.g., Santana & Kim, 2025), or structured and

directly measurable object detection in images at scale (e.g., Efthymiou et al., 2025). More

advanced forms of topic modeling go beyond the simple reconstruction of topics as clusters of

words by offering insights into topic dynamics and by including meta-information (e.g., Brandtner

et al., 2025; Etchanchu et al., 2025). In this sense, computational methods allow for the generation

of theoretical artefacts that are more immediately relevant for theorizing. We therefore see

computational methods as excellent complements to more traditional interpretive research on

culture and meaning, rather than a substitute (Nelson, 2020). For some research endeavors, it may

be beneficial to combine computational methods with more qualitative analysis (e.g., Etchanchu

et al., 2025; Santana & Kim, 2025). The future of research on culture and meaning may lie in

further integration and realization of synergies across computational and non-computational

methods, which highlights challenges and possibilities.

      Further, we see that the articles in our special issue rely on relational views (Lounsbury &

Gehman, 2024) sensitive to entwined macro-micro processes (Furnari, 2014; Mohr et al., 2020).

Computational methods appear as one way to avoid the classical macro-to-micro or micro-to-

macro level approaches of the past (Dacin, Goodstein & Scott, 2002; Thornton et al, 2012). The

articles in our special issue embrace a more relational, dynamic view of culture and meaning,

seeking not only to uncover causal mechanisms from one level of analysis to another, but also to

describe the recursive processes across levels. For example, both articles by Brandner et al. (2025)

and Etchanchu et al. (2025) concerning fields are socio-historical studies that build on the tradition

of situated field analysis and theoretically consider the co-constitutive relationship of macro



                                                     31

--- page 33 ---

(society) and meso (public housing) or even micro (framing mechanisms) levels. In the

occupation-focused articles on artworks (Efthymiou et al., 2025) and ethics (Santana & Kim,

2025), community-based constructions of meaning are confined and focused on temporality,

geography, and entangled meanings. Yet, this allows the authors to elucidate more domain-specific

and localized understanding and evaluation processes. The article on industry categories (Gouvard

& Durand, 2024) represents a combination of a field and situated meaning analysis by considering

the industrial domain in which culture and meaning are embedded. The authors argue that both

proximate, clearer meanings within a prototype category––plus salient, yet ambiguous outlier

meanings––jointly determine the fate of new firms.



Challenges in the use of computational methods in cultural and meaning analysis

      In this section, we wrestle with theoretical and empirical challenges concerning

computational methods for examining culture and meaning. In both Tables 1 and 2, the bottom

row summarizes the main rendering challenges faced by each article in our special issue. As with

most challenges, we think that they offer opportunities for future research.

      Opportunities for theory building. Theoretically, the field domain articles have many

moving parts––actors, processes, mechanisms, outcomes by period and field––all which scholars

have already theorized partly in previous work but are not truly universally valid in an ontological

sense within organization studies. Accordingly, most dynamics in fields require situated, relational

explanations. This means that there is still much to be done on the epistemological side to

substantiate that theorizing. Empirically, Etchanchu and colleagues (2025) have to show three

mechanisms at work in two different national contexts, documenting both similarity and

difference, and then combine these results with the output of computational methods. Brandtner



                                                   32

--- page 34 ---

and colleagues (2025) have to demonstrate different institutional instantiations over time, yet also

the persistence of the institution of public housing, along with a shifting wider societal context.

Theoretical moving parts, new computational methods, and unique big and thick data require

considerable space for explanations, methodological justifications, empirical support, and

extensive appendices (e.g., Efthymiou et al., 2025). This is a serious challenge for authors (and

readers).

      One solution is to rely on established theory, as we see in the context of institutions,

evaluations, professions, and categories. However, relying on established theory is only acceptable

for purely methodological articles as this deductive approach to theorizing does not lend itself well

to the development of novel theories. For our special issue, all authors faced reviewer requests for

stronger theoretical advancement. To develop new theory with novel computational methods

requires covering established theoretical assumptions briefly while complementing them with new

theorizations (of theory-based constructs, processes, outcomes, or mechanisms), along with the

implementation and fine-tuning of computational methods for that specific purpose. The reviewers

and we, the guest editors, pushed all authors to move in this direction, and then to trim their

manuscript––hence appendices––to deliver an article fitting the demands of Organization Studies.

We expect that other solutions will emerge, such as adopting an abductive style of paper structure,

in which key theoretical considerations are used as a stepping stone to identify anomalies in the

data, which scholars subsequently seek answers to in their data (Timmermans & Tavory, 2022).

The computational tool is thus used iteratively to identify both anomalies and explanations in a

reflexive process that still leaves the human at the center of the theorizing process.

      Methodological Opportunities. Computational-based research designs and methods are

evolving rapidly, due to more forms of data and data assembly methods, increased computing



                                                    33

--- page 35 ---

power, a larger community of analysts, and the advent of generative AI. This means that the

techniques represented in the articles for this special issue have evolved since they were under

review. Over the last five years, for instance, grammatical parsing and topic modeling have moved

from being relatively new to mature techniques (Grimmer et al., 2022; Goldenstein & Poschmann,

2019; Hannigan et al., 2019). Therefore, further advancement will consist in the development of

new model implementations, more refined applications, or entirely new computational approaches.

For example, Etchanchu and colleagues (2025) compare two national fields and mobilize meta-

data covariates via structural topic modeling (STM). Brandtner and colleagues (2025) rely on the

yet infrequently used dynamic topic modeling (DTM), and a narrative approach linking changes

in the meaning of public housing to actual public housing construction, among other things. We

believe that research opportunities lie in tying outcome data, like housing construction or policy

changes on fracking, to field dynamics through the interpretative usage of computational methods,

while retaining a more abductive paper structure.

      Interestingly, the use of topic modeling by Santana and Kim (2025), while drawing on

standard LDA, links to the surrounding arena of committee members by looking at the probabilistic

distributions of topics-per-document (theta) and of per-topic word (beta), and how they fit with

time and the different sociolects. This provides a consistent, systematic point of contact between

network and topic modeling techniques. The article by Efthymiou and colleagues (2025) is an

example of tying localized and overarching meaning systems systematically by considering a wide

variety of art and artist data over time and capturing their rankings and standings. Gouvard and

Durand (2024) bound culture and meaning by focusing on prototype and outlier similarities within

industries and their impact on firms’ evaluation. The authors then leverage established financial

databases to construct measures for their statistical analysis. All three studies had to address face



                                                    34

--- page 36 ---

validity considerations: Do codes of ethics actually reflect emergent and enduring practices? How

is the aesthetic of art itself (not just type or fashion) affecting meaning and rankings? And how are

investors themselves viewing categories at the time? Questions such as these open up possibilities

to combine research around meaning and culture with field or online experiments to ground further

prior claims, or to delve into generalizability questions.



Concerns of increasing automation of data analysis

      As a final statement, we would like to revisit the current hype surrounding computational

methods, such as topic modeling, convolutional neural network, or generative AI, which could

tempt researchers to consider these as a simple path to automated data analysis that requires little

interpretation. Such aspirations probably arise because computational methods are becoming more

intuitive to use, faster, and cheaper, and seem to solve difficult problems at an advanced level

(Mollick, 2024; Schildt, 2020). All authors and guest editors of this special issue are, in fact, using

them in a variety of research projects. Moreover, some organization theorists have argued for

analyzing practical or theoretical problems by using computational methods such as AI in more

rather than less automated ways, based on contingencies that fit with such use (Murray et al.,

2021), or by drawing creatively on the automation-augmentation paradox (Raisch & Krakowski,

2021).

      The automated use of computational methods for testing and building theories is appropriate

if issues of transparency, reproducibility, and validity have been explicitly addressed. However, in

domains such as culture and meaning, we believe that additional care is required. For example, the

articles by Etchanchu and colleagues (2025) and Efthymiou and colleagues (2025) underscore that

large language and image archives can be used more creatively, such as for assessing more than



                                                     35

--- page 37 ---

one field or one period to capture the meaning of ideas in translation. Nevertheless, when it comes

to modeling discourse and constructing theoretical artifacts for theory-building, articles in the

special issue stick to corpora in their domains (for the most part) and use additional data to induce

cultural meanings. This leads to more careful rendering of theoretical artefacts via computational

methods, plus the use of within sample periods, temporal or structural covariates and dynamics to

carefully build up researcher interpretations. To be clear, we are not against unsupervised

computational methods such as topic modeling or automation in research. Rather, we believe that

computational methods should neither guide rendering moves nor decide interpretations (Bechky

& Davis, 2025; Hannigan et al., 2019; 2022). Cultural and meaning are situated within domains

such as fields, occupations, or industries. Accordingly, even if the automation of data collection

and analysis in research becomes more common in the near future, computational approaches for

assessing culture and meaning, such as those presented in this special issue, are likely to be

invaluable as benchmarks and ways to creatively deal with the automation-augmentation paradox.



Acknowledgement

We are grateful to Organization Studies Editors-in-Chief Tammar Zilber and Paolo Quattrone for

their valuable guidance in compiling this special issue and for their supportive comments on earlier

drafts of this manuscript. We also thank former Editor-in-Chief Renate E. Meyer for her thoughtful

recommendations and support in making this methodologically oriented issue possible. Finally,

we appreciate the efforts of the anonymous reviewers, whose constructive feedback provided

invaluable support to the authors of the articles in this special issue.




                                                     36

--- page 38 ---

References

Abbott, Andrew (1983). Professional ethics. American Journal of Sociology, 88, 855–885.

Aceves, Pedro, & Evans, James A. (2024). Mobilizing conceptual spaces: how word embedding

     models can inform measurement and theory within organization science. Organization

     Science, 35, 788–814.

Bailey, Diane E., Faraj, Samer, Hinds, Pamela J., Leonardi, Paul M., & von Krogh, Georg (2022).

     We are all theorists of technology now: A relational perspective on emerging technology

     and organizing. Organization Science, 33, 1–18.

Baldessarelli, Giada, Stigliani, Ileana, & Elsbach, Kimberly D. (2022). The aesthetic dimension of

     organizing: A review and research agenda. Academy of Management Annals, 16, 217–257.

Banerjee, Mitali, Cole, Benjamin M., & Ingram, Paul (2023). “Distinctive from what? And for

     whom?” Deep learning-based product distinctiveness, social structure, and third-party

     certifications. Academy of Management Journal, 66, 1016–1041.

Barley, Stephen R. & Kunda, Gideon (2011). Gurus, hired guns, and warm bodies: itinerant

     experts in a knowledge economy. Princeton: Princeton University Press.

Bechky, Beth A., & Davis, Gerald F. (2025). Resisting the algorithmic management of science:

     craft and community after generative AI. Administrative Science Quarterly, 70, 1–22.

Behfar, Kristin, & Okhuysen, Gerardo A. (2018). Perspective—Discovery within validation logic:

     Deliberately surfacing, complementing, and substituting abductive reasoning in hypothetico-

     deductive inquiry. Organization Science, 29, 323–340.

Bendix, Reinhard (2001). Work and authority in industry: Managerial ideologies in the course of

     industrialization. New York: Routledge. (Original work published 1956).

Benford, Robert D., & Snow, David A. (2000). Framing processes and social movements: An


                                                  37

--- page 39 ---

overview and assessment. Annual Review of Sociology, 26, 611–639.

Berger, Peter L., & Luckmann, Thomas (1966). The social construction of reality: a treatise in the

      sociology of knowledge. New York: Anchor.

Blei, David M., Ng, Andrew Y., & Jordan, Michael I. (2003). Latent Dirichlet allocation. Journal

      of Machine Learning Research, 3, 993–1022.

Bornakke, Tobias, & Due, Brian L. (2018). Big–thick blending: a method for mixing analytical

      insights from big and thick data sources. Big Data & Society, 5(1), 2053951718765026.

Bourdieu, Pierre (1984). Distinction: a social critique of the judgement of taste (R. Nice, Trans.).

      Cambridge, MA: Harvard University Press.

Boxenbaum, Eva, & Jonsson, Stefan (2017). Isomorphism, diffusion and decoupling: concept

      evolution and theoretical challenges. In Royston Greenwood, Christine Oliver, Thomas B.

      Lawrence, & Renate E. Meyer (Eds.), The SAGE Handbook of Organizational

      Institutionalism (2nd ed., pp. 79–104). Los Angeles: Sage.

Boxenbaum, Eva, Jones, Candace, Meyer, Renate E., & Svejenova, Silviya (2018). Towards an

      articulation of the material and visual turn in organization studies. Organization Studies, 39,

      597–616.

Brandtner, Christof, Ashur, Parham, & Srinivasa Desikan, Bhargav (2025). Dynamic persistence

      of institutions: modeling the historical endurance of Red Vienna’s public housing utopia.

      Organization Studies. https://doi.org/10.1177/01708406251317258.

Burt, Ronald S. (1992). Structural Holes: The Social Structure of Competition. Cambridge, MA:

      Harvard University Press.

Carley, Kathleen (1994). Extracting culture through textual analysis. Poetics, 22, 291–312.

Chen, Li, & Mankad, Shawn (2024). A structural topic and sentiment-discourse model for text



                                                    38

--- page 40 ---

analysis. Management Science. https://doi.org/10.1287/mnsc.2022.00261.

Colyvas, Jeannette A., & Powell, Walter W. (2006). Roads to institutionalization: the remaking of

      boundaries between public and private science. Research in Organizational Behavior, 27,

      305–353.

Cornelissen, J. P., & Werner, M. D. (2014). Putting framing in perspective: A review of framing

      and frame analysis across the management and organizational literature. Academy of

      Management Annals, 8, 181–235.

Dacin, M. Tina, Goodstein, Jerry, & Scott, W. Richard (2002). Institutional theory and institutional

      change: Introduction to the special research forum. Academy of Management Journal, 45,

      45–56.

DiMaggio, Paul (2013) The Internet’s influence on the production and consumption of culture:

      creative destruction and new opportunities. In Change: 19 key essays on how the Internet is

      changing our lives (pp. 364–394). Madrid: BBVA

Douglas, Mary (2001). Purity and danger: An analysis of the concepts of pollution and taboo.

      London: Routledge. (Original work published 1966).

Durkheim, Emile (1995). The elementary forms of religious life (K. E. Fields, Trans.). New York:

      Free Press. (Original work published 1912).

Edelmann, Achim, & Mohr, John W. (2018). Formal studies of culture: Issues, challenges, and

      current trends. Poetics, 68, 1–9.

Edelmann, Achim, Wolff, Tom, Montagne, Danielle, & Bail, Christopher A. (2020).

      Computational social science and sociology. Annual Review of Sociology, 46, 61–81.

Efthymiou, Athanasios, Kackovic, Monika, Rudinac, Stevan, Worring, Marcel, & Wijnberg,

      Naochem M. (2025). Being ranked in a material world: the visual originality of an artwork



                                                    39

--- page 41 ---

and its effects on the artist’s canonization. Organization Studies.

Etchanchu, Helen, Aranda, Ana M., Harmon, Derek, & Ansari, Shaz (2025). How historical

      context shapes the construction of field-level frames: a comparative study of France and

      Germany’s           shale          gas         debates.         Organization           Studies.

      https://doi.org/10.1177/0170840625135783.

Evans, Joelle (2021). How professionals construct moral authority: expanding boundaries of expert

      authority in stem cell science. Administrative Science Quarterly, 66, 989–1036.

Faik, Isam, Barrett, Michael, & Oborn, Eivor (2020). How information technology matters in

      societal change: an affordance-based institutional perspective. MIS Quarterly, 44, 1359–

      1390.

Friedland, Roger (2009). Institution, practice, and ontology: toward a religious sociology. In

      Renate E. Meyer, Kerstin Sahlin, Marc Ventresca, & Peter Walgenbach (Eds.), Research in

      the Sociology of Organizations: Vol. 27: Institutions and Ideology (pp. 45–83). Emerald.

Friedland, Roger, Mohr, John W., Roose, Henk, & Gardinali, Paolo (2014). The institutional logics

      of love: measuring intimate life. Theory and Society, 43, 333-370.

Furnari, Santi (2014). Interstitial spaces: microinteraction settings and the genesis of new practices

      between institutional fields. Academy of Management Review, 39, 439–462.

Gehman, Joel, Glaser, Vern L., Eisenhardt, Kathleen M., Gioia, Denny, Langley, Ann, & Corley,

      Kevin G. (2018). Finding theory-method fit: a comparison of three qualitative approaches to

      theory building. Journal of Management Inquiry, 27, 284–300.

Gehman, Joel, Treviño, Linda K., & Garud, Raghu (2013). Values work: a process study of the

      emergence and performance of organizational values practices. Academy of Management

      Journal, 56, 84–112.



                                                    40

--- page 42 ---

George, Gerard, Osinga, Ernst C., Lavie, Dovev, & Scott, Brent A. (2016). Big data and data

     science methods for management research. Academy of Management Journal, 59, 1493–

     1507.

Gioia, Dennis A., Corley, Kevin G., & Hamilton, Aimee L. (2013). Seeking qualitative rigor in

     inductive research: notes on the Gioia methodology. Organizational Research Methods, 16,

     15–31.

Giorgi, Simona, Lockwood, Christi, & Glynn, Mary A. (2015). The many faces of culture: making

     sense of 30 years of research on culture in organization studies. The Academy of

     Management Annals, 9, 1–54.

Glaser, Vern; Moser, Christine; D’Adderio, Luciana; Hannigan, Timothy; Pozner, Jo-Ellen (2024).

     Special issue on algorithmic organizing: Exploring the pervasive impact of algorithms on

     organizations and society. Organization Studies.

Godart, Frédéric, Seong, Sorah, & Phillips, Damon J. (2020). The sociology of creativity:

     elements, structures, and audiences. Annual Review of Sociology, 46, 489–510.

Goldenstein, Jan, Jancsary, Dennis, Grodal, Stine, Forgues, Bernard, & Jennings, P. Devereaux

     (2022). Enhancing Organizations Research Involving Meaning and Culture Using

     Computational Text and Image Analyses. Organization Studies Special Issue Call for

     Papers.                                                   https://journals.sagepub.com/pb-

     assets/cmscontent/OSS/CfP_Enhancing_Organizations_Research-converted-

     1652697168.pdf.

Goldenstein, Jan, & Poschmann, Philipp (2019). Analyzing meaning in big data: performing a map

     analysis using grammatical parsing and topic modeling. Sociological Methodology, 49, 83–

     131.



                                                 41

--- page 43 ---

Goldenstein, Jan, Poschmann, Philipp, & Hunoldt, Michael (2023). The global orientation of

     organizations: An analysis of the effects of global cultural rationalization and national

     institutional traditions. Journal of Management Studies, 60, 1584–1623.

Goldenstein, Jan, & Walgenbach, Peter (2024). Sayings and doings in practices: enhancing

     practice-driven institutionalism with insights from the philosophy of embodiment.

     Organization Studies, 45, 1373–1398.

Goldenstein, Jan, & Walgenbach, Peter (2021): “How on earth did this happen?” The relationship

     of practical consciousness and institutional evolution. Organization Theory, 2, 1–22.

Gouvard, Paul, & Durand, Rodolphe (2024). Clearing up confusion: the effect of outlier similarity

     on IPO underpricing. Organization Studies. https://doi.org/10.1177/01708406241286287

Gray, Barbara, Purdy, Jill M., & Ansari, Shahzad (Shaz) (2015). From interactions to institutions:

     microprocesses of framing and mechanisms for the structuring of institutional fields.

     Academy of Management Review, 40, 115–143.

Grimmer, Justin, Roberts, Margaret E., & Stewart, Brandon M. (2022). Text as data: A new

     framework for machine learning and the social sciences. Princeton: Princeton University

     Press.

Grodal, Stine (2018). Field expansion and contraction: how communities shape social and

     symbolic boundaries. Administrative Science Quarterly, 63(4), 783-818.

Haans, Richard F. J. (2019). What’s the value of being different when everyone is? The effects of

     distinctiveness on performance in homogeneous versus heterogeneous categories. Strategic

     Management Journal, 40, 3–27.

Hannigan, Timothy, Haans, Richard F. J., Vakili, Keyvan, Tchalian, Hovig, Glaser, Vern, Wang,

     Milo, Kaplan, Sarah, & Jennings, P. Devereaux (2019). Topic modeling in management



                                                  42

--- page 44 ---

research: Rendering new theory from textual data. Academy of Management Annals, 13,

     586–632.

Haveman, Heather A., & Rao, Hayagreeva (1997). Structuring a theory of moral sentiments:

     institutional and organizational coevolution in the early thrift industry. American Journal of

     Sociology, 102, 1606–1651.

Hickman, Louis, Thapa, Stuti, Tay, Louis, Cao, Mengyang, & Srinivasan, Padmini (2022). Text

     pre-processing for text mining in organizational research: review and recommendations.

     Organizational Research Methods, 25, 114–146.

Hinings, Bob, & Meyer, Renate (2018). Starting points: Intellectual and institutional foundations

     of organization theory. Cambridge: Cambridge University Press.

Höllerer, Marcus A., Jancsary, Dennis, Barberio, Vitaliano, & Meyer, Renate E. (2020). The

     interlinking theorization of management concepts: cohesion and semantic equivalence in

     management knowledge. Organization Studies, 41, 284–1310.

Jancsary, Dennis, Meyer, Renate E., Höllerer, Markus A., & Barberio, Vitaliano (2017). Toward

     a   structural    model   of        organizational-level        institutional   pluralism   and    logic

     interconnectedness. Organization Science, 28, 1150–1167.

Jones, Candace, Maoret, Massimo, Massa, Felipe G., & Svejenova, Silviya (2012). Rebels with a

     cause: formation, contestation, and expansion of the de novo category “modern

     architecture,” 1870–1975. Organization Science, 23, 1523–1545.

Kitchin, Rob, & McArdle, Gavin (2016). What makes big data, big data? Exploring the ontological

     characteristics     of         26        datasets.        Big        Data       &       Society,      3,

     https://doi.org/10.1177/2053951716631130.

Korff, Valeska P., Oberg, Achim, & Powell, Walter W. (2015). Interstitial organizations as



                                                          43

--- page 45 ---

conversational bridges. Bulletin of the Association for Information Science and Technology,

     41, 34–38.

Krabbe, Anders, & Grodal, Stine (2023). The aesthetic evolution of product categories.

     Administrative Science Quarterly, 68, 734–780.

Krakowski, Sebastian, Luger, Johannes, & Raisch, Sebastian (2023). Artificial intelligence and the

     changing sources of competitive advantage. Strategic Management Journal, 44, 1425–1452.

Lamont, Michèle (2012). Toward a comparative sociology of valuation and evaluation. Annual

     Review of Sociology, 38, 201–221.

Lamont, Michèle, & Molnár, Virag (2002). The study of boundaries in the social sciences. Annual

     Review of Sociology, 28, 167–195.

Langley, Ann, Bell, Emma, Bliese, Paul, LeBaron, Curtis, & Gruber, Marc (2023). Opening up

     AMJ’s research methods repertoire. Academy of Management Journal, 66, 711-719.

Leavitt, Keith, Schabram, Kira, Hariharan, Prashanth, & Barnes, Christopher M. (2021). Ghost in

     the machine: on organizational theory in the age of machine learning. Academy of

     Management Review, 46, 750–777.

Leixnering, Stephan, Meyer, Renate E., & Doralt, Peter (2022). The past as prologue: purpose

     dynamics in the history of the Aktiengesellschaft. In Renate E. Meyer, Stephan Leixnering,

     & Jeroen Veldman (Eds.), Research in the Sociology of Organizations: Vol. 78: The

     corporation: rethinking the iconic form of business organization (pp. 97–120). Emerald.

Lounsbury, Michael, & Gehman, Joel (2024). Concise introduction to organization theory: from

     ontological differences to robust identities. Cheltenham, UK: Edward Elgar.

Lounsbury, Michael, & Ventresca, Marc (2003). The new structuralism in organizational theory.

     Organization, 10, 457–480.



                                                  44

--- page 46 ---

Mantere, Saku, & Ketokivi, Mikko (2013). Reasoning in organization science. Academy of

     Management Review, 38, 70–89.

Meyer, Renate E., & Höllerer, Markus A. (2010). Meaning structures in a contested issue field: A

     topographic map of shareholder value in Austria. Academy of Management Journal, 53,

     1241–1262.

Meyer, Renate E., Höllerer, Markus A., Jancsary, Dennis, & Van Leeuwen, Theo (2013). The

     visual dimension in organizing, organization, and organization research. Academy of

     Management Annals, 7, 487–553.

Meyer, Renate E., Jancsary, Dennis, & Höllerer, Markus A. (2021). Zones of meaning, Leitideen,

     institutional logics – and practices: a phenomenological institutional perspective on shared

     meaning structures. In Michael Lounsbury, Deborah A. Anderson, & Paul Spee (Eds.),

     Research in the Sociology of Organizations: Vol. 70: On practice and institution: theorizing

     the interface (pp. 161–186). Emerald.

Meyer, Renate E., Leixnering, Stephan, Kornberger, Martin, Jancsary, Dennis, & Höllerer, Markus

     A. (2024). Ernst Cassirer and the symbolic foundation of institutions. Journal of

     Management Studies, 61, 3824–3842.

Mohr, John W. (1998). Measuring meaning structures. Annual Review of Sociology, 24, 345–370.

Mohr, John W., Bail, Christopher A., Frye, Margaret, Lena, Jennifer C., Lizardo, Omar,

     McDonnell, Terence E., Mische, Ann, Tavory, Iddo, & Wherry, Frederick F. (2020).

     Measuring culture: universality and identity politics. New York: Columbia University Press.

Mollick, Ethan (2024). Reinventing the organization for GenAI and LLMs. MIT Sloan

     Management       Review     (Online),   https://sloanreview.mit.edu/article/reinventing-the-

     organization-for-genai-and-llms/ [accessed 17 June 2025].



                                                 45

--- page 47 ---

Murray, Alex, Rhymer, Jen, & Sirmon, David G. (2021). Humans and technology: forms of

     conjoined agency in organizations. Academy of Management Review, 46, 552–571.

Negro, Giacomo, Özgecan Koçak, and Greta Hsu. Research on categories in the sociology of

     organizations." Categories in markets: Origins and evolution. Emerald Group Publishing

     Limited, 2010. 3-35.

Nelson, Laura K. (2019). To measure meaning in big data, don’t give me a map, give me

     transparency and reproducibility. Sociological Methodology, 49, 139–143.

Nelson, Laura K. (2020). Computational grounded theory: a methodological framework.

     Sociological Methods & Research, 49, 3–42.

Nelson, Laura K., Burk, Derek, Knudsen, Marcel, & McCall, Leslie (2021). The future of coding:

     a comparison of hand-coding and three types of computer-assisted text analysis methods.

     Sociological Methods & Research, 50, 202–237.

O’Mahony, Siobhán, & Ferraro, Fabrizio (2007). The emergence of governance in an open source

     community. Academy of Management Journal, 50, 1079–1106.

Phillips, Nelson, Kalvapalle, Sai, & Kennedy, Mark (2024). Beyond the Turing test: exploring the

     implications of generative AI for category construction. Organization Theory, 5,

     https://doi.org/10.1177/26317877241275113.

Pillai, Sandeep Devanatha, Brent Goldfarb, and David Kirsch. (2024). Lovely and likely: using

     historical methods to improve inference to the best explanation in strategy. Strategic

     Management Journal, 45, 1539–1566

Poschmann, Philipp, & Goldenstein, Jan (2022). Disambiguating and specifying social actors in

     big data: using Wikipedia as a data source for demographic information. Sociological

     Methods & Research, 51, 887–925.



                                                 46

--- page 48 ---

Poschmann, Philipp, Goldenstein, Jan, Büchel, Sven, & Hahn, Udo (2024). A vector space

     approach for measuring relationality and multidimensionality of meaning in large text

     collections. Organizational Research Methods, 27, 650–680.

Raisch, Sebastian, & Krakowski, Sebastian. (2021). Artificial intelligence and management: The

     automation-augmentation paradox. Academy of Management Review, 46, 192–210.

Sætre, Alf Steiner, and Van de Ven, Andrew (2021). Generating theory by abduction. Academy of

     Management Review, 46, 684–701.

Sahlin-Andersson, Kerstin, & Engwall, Lars (Eds). 2002. The expansion of management

     knowledge: carriers, flows, and sources, Stanford: Stanford University Press.

Santana, Jessica J., & Kim, Seonghoon (2025). From values to codes: a computational text analysis

     of     the       codification   of     occupational     ethics.    Organization      Studies.

     https://doi.org/10.1177/01708406251317255.

Schildt, Henri (2020). The data imperative: how digitalization is reshaping management,

     organizing, and work. Oxford: Oxford University Press.

Schmiedel, Theresa, Müller, Oliver, & vom Brocke, Jan (2019). Topic modeling as a strategy of

     inquiry in organizational research: A tutorial with an application example on organizational

     culture. Organizational Research Methods, 22, 941–968.

Scott, Richard (1981). Organizations: rational, natural and open systems. Englewood Cliffs, NJ:

     Prentice-Hall.

Seidel, Marc-David L. (2018). Questioning centralized organizations in a time of distributed trust.

     Journal of Management Inquiry, 27, 40–44.

Sgourev, Stoyan V., Aadland, Erik, & Formilan, Giovanni (2023). Relations in aesthetic space:

     how color enables market positioning. Administrative Science Quarterly, 68, 146–185.



                                                   47

--- page 49 ---

Sharkey, Amanda, Hsu, Greta, & Kovács, Balázs (2023). Expert critics, rankings, and review

     aggregators: the changing nature of intermediation and the rise of markets with multiple

     intermediaries. Academy of Management Annals, 17, 1–36.

Starr, Paul (2021). The relational public. Sociological Theory, 39, 57–80.

Swidler, A. (1986). Culture in action: symbols and strategies. American Sociological Review, 51,

     273–286.

Than, Nga, Fan, Leanne, Law, Tina, Nelson, Laura K., & McCall, Leslie (2025). Updating “the

     future of coding”: qualitative coding with generative large language models. Sociological

     Methods & Research. https://doi.org/10.1177/00491241251339188.

Thornton, Patricia H., Ocasio, William, & Lounsbury, Michael (2012). The institutional logics

     perspective: a new approach to culture, structure and process. Oxford: Oxford University

     Press.

Timmermans, Stefan, and Iddo Tavory (2022). Data analysis in qualitative research: theorizing

     with abductive analysis. University of Chicago Press.

Tonidandel, Scott, King, Eden B., & Cortina, Jose M. (2018). Big data methods: Leveraging

     modern data analytic techniques to build organizational science. Organizational Research

     Methods, 21, 525–547.

Valentino, Lauren, & Vaisey, Stephen (2022). Culture and durable inequality. Annual Review of

     Sociology, 48, 109-129.

Vergne, Jean-Philippe (2020). Decentralized vs. distributed organization: blockchain, machine

     learning    and    the    future   of   the   digital   platform. Organization   Theory, 1,

     https://doi.org/10.1177/2631787720977052.

Von Krogh, Georg, Roberson, Quinetta, & Gruber, Marc (2023). Recognizing and utilizing novel



                                                   48

--- page 50 ---

research opportunities with artificial intelligence. Academy of Management Journal, 66,

     367–373.

Vosoughi, S., Roy, D., & Aral, S. (2018). The spread of true and false news online. Science,

     359(6380), 1146-1151.

Wruk, Dominika, Oberg, Achim, Klutt, Jennifer, & Maurer, Indre (2019). The presentation of self

     as good and right: how value propositions and business model features are linked in the

     sharing economy. Journal of Business Ethics, 159, 997–1021.

Wry, Tyler, Lounsbury, Michael, & Jennings, P. Devereaux (2014). Hybrid vigor: securing venture

     capital by spanning categories in nanotechnology. Academy of Management Journal, 57,

     1309–1333.

Zietsma, Charlene, Groenewegen, Peter, Logue, Danielle M., & Hinings, C. R. (Bob) (2017). Field

     or fields? Building the scaffolding for cumulation of research on institutional fields.

     Academy of Management Annals, 11, 391–450.

Zilber, Tammar B. (2020). The methodology/theory interface: Ethnography and the

     microfoundations         of       institutions.      Organization         Theory,        1,

     https://doi.org/10.1177/2631787720919439.

Zuboff, S. (2022). Surveillance capitalism or democracy? The death match of institutional orders

     and the politics of knowledge in our information civilization. Organization Theory, 3,

     https://doi.org/10.1177/26317877221129290.




                                                  49

--- page 51 ---

Author Biographies

Jan Goldenstein is research associate at the Chair of Organization, Leadership, and Human

Resource Management at Friedrich Schiller University Jena, Germany. He is co-founder of the

Group for Jena Computational Organizational Research Applications (JenCORA). His research

interests include institutional theory, category research, social evaluation, market entry decisions,

comparative international studies and methodological research. He is particularly interested in

developing measures for the large-scale, quantitative analysis of dynamic relationships between

organizations, social spaces, and their environments, incorporating human interpretations to

preserve contextual nuances.



Dennis Jancsary is Chair in Organisation Studies at the University of Liverpool Management

School. He is also a senior research fellow at WU Vienna, where he received his PhD in business

administration. His work draws on institutional organization theory and highlights the crucial

importance of socio-cultural environments for the dynamics of organizational forms and practices.

He is particularly interested in innovative methodologies for textual and discourse analysis,

including visual and multimodal analysis.



Stine Grodal is Distinguished Professor at Northeastern University D'Amore-McKim School of

Business in Entrepreneurship and Innovation. She received her PhD from Stanford University in

Management Science and Engineering. Her research examines the emergence and evolution of

technologies, markets, and industries. She is especially interested in how firms can shape and

exploit the socio-cognitive elements of markets during different stages of industry evolution. She

uses a plurality of empirical approaches but is particularly passionate about increasing the rigor


                                                    50

--- page 52 ---

and breath of qualitative methods.



Bernard Forgues is Professor of Organization Theory at emlyon business school, where he is also

the Head of STORM, the school's research center in strategy and organization. He is a former chair

of EGOS. Bernard's current research interests include social evaluation, institutions, and

materiality, which he studies in contexts of hospitality and craft, among others.



P. Devereaux (Dev) Jennings is a Professor of Strategy, Entrepreneurship and Management at the

Alberta School of Business. He currently co-coordinates the Interpretive Data Science (IDeaS)

group and works on Future Energy System (FES) products and start ups at the University of

Alberta. He is also the former Director of the university’s Canadian Centre for Corporate Social

Responsibility (CCCSR). Dev received his Ph.D. and M.A. from Stanford University and his A.B.

from Dartmouth College.




                                                   51

--- page 53 ---

Tables

Table 1. From organization theory to computational methods


   DOMAIN                          SOCIETAL FIELDS                                             SKILLED OCCUPATIONS                            INDUSTRY CATEGORIES
  ARTICLES/               Fracking                     Red Vienna                   Art Novelty and               Occupational Values                  Category Outliers
 RENDERING             Issue Fields                  Public Housing                  Artist Standing                    and Codes                        Among IPOs
 Research       Do historical differences       How do instantiations allow      Does visual originality at    How does an occupational       How do prototype similarity and

 Question       between countries influence     institutions to persist amidst   the time of creation          community with diverse         outlier similarity simultaneously
                the emergence of field-level    changes in their wider           predict artists’ long-term    ethical values come to agree   affect how investors value an
                frames (and how)?               institutional context?           canonical standing?           on a shared code of ethics?    issuing firm in the IPO market?
 Organization   Framing theory.                 Institutional theory and         Sociology of valuation        Occupations, professions,      Market categories and

 Theory         Field-level frames are          persistence.                     and evaluation.               and values.                    institutional dynamics.
                orienting devices that          Institutions, despite their      Materiality, innovation       Codes are objective,           Categories summarize
                enable actors to influence      universal and enduring           and evaluation are all part   normative embodiments of       information on symbolic and
                and make sense of               character, manifest              of selection systems.         values to guide practice.      material attributes of products,
                contentious issues.             differently through evolving     Visual originality in a       Discursive communities         firms.
                Historical positioning, issue   instantiations—the               system as basis for artists   (sociolects) use their power   Launching firms in an established
                labeling, and bounded           institution’s attributes in a    and their work secures        to influence the final code.   category with similar attributes to
                mobilization are                particular time and place.       historical standing.          Codes meanings shift and       category prototype can be
                mechanisms for frame                                                                           then are stabilized.           accurately priced by investors.
                change.                                                                                                                       Similarity to a successful outlier,
                                                                                                                                              across category space, creates
                                                                                                                                              ambiguity and leads to
                                                                                                                                              underpricing.


 Culture &      History as culture. It          Culture consists of wider,       The aesthetics of domain      Values constitute a key        Categories are neo-structural

 Meaning        provides context for frames,    evolving meaning structures      are tied to key material      component of occupational      features of culture and embody
                                                in which an institution is                                     or professional culture.       patterns of meaning.

--- page 54 ---

key issues to be framed, and    embedded as “a                   artifacts in the domain      Codes represent the            Across-category performance
             framing materials.              combination of cultural          and those producing them.    objectification of key         outliners lose salience quite
             Frames as shared meanings.      schemas”.                        The rank ordering of         practices and values.          quickly, whereas the prototype
                                             Structural basis of meaning      artists and their works      Discourse among sociolects     industry does not.
                                             as we see with the term          establishes a hierarchy of   carries meanings and
                                             “public housing”, itself an      meaningful work.             sharpens codes.
                                             institution.
Research     Historical topic modeling of    Historical topic modeling of     Neural net assessment of     Within occupation,             Trained document embedding

Design       large, longitudinal data sets   large, longitudinal data set     visual originality over      semantic network and           model to measure the features of
             with structural topic           with dynamic topic               time and by style, then      community detection            categories across industries, then
             modeling (STM) of               modeling (DTM) of                associated via linear        related to each other, then    linear models with fixed effects to
             discourse in two countries      discourse of the culturally      models with creator          topic modeling to capture      show the impact on IPO.
             around a framed issue.          embedded institution.            standing captured via text   meanings over time.
                                                                              analysis of recognition.
Reflexive    Linking the three               Theorizing many fluid,           Capturing in-situ            Establishing link between      Convincing researchers that the

Rendering    mechanisms in each              interdependent constructs -      originality and relative     semantic network of            outliers identified by a complex

Challenges   country’s framing debates       wider culture and meaning,       standing, plus creating a    meanings promoted by           multi-category measure captures
             to show commonality and         institutions, instantiations -   theory that is robust        different sociolects and the   unicorns and not just a salient
             difference between the          to show where and how            enough about the changes     eventual code created –plus    (bandwagon) effect of the prior
             societies.                      change occurs and is             in notions of aesthetics.    that codes matter.             year’s success, thus it is worth
                                             stabilized.                                                                                  paying more attention to the
                                                                                                                                          unicorn than an industry’s
                                                                                                                                          prototype.




                                                                                    53

--- page 55 ---

Table 2. Computational methods to theory-building artifacts


 DOMAINS                            SOCIETAL FIELDS                                             SKILLED OCCUPATIONS                         INDUSTRY CATEGORIES

 ARTICLES/                    Fracking                Red Vienna              Artwork Novelty and               Occupational Codes                  Category Outliers
 RENDERING                Issue Fields              Public Housing                Artist Standing                     and Values                      Among IPOs
 Data selection   15,886 French (2006-2015)     City of Vienna yearbooks     60,011 paintings over 600      613 emails exchanged            2,488 IPO prospectuses and

 & pre-           and 13,434 German (2007-      between 1867 and 2009.       years by 942 artists           between committee members       159,216 annual reports by 33,308

 Processing       2015) newspaper articles      Extensive data cleaning      prepared for use with          (1991-1998)                     established firms (1996 to 2015)
                  from Factiva.                 (automated and manual).      ImageNet and ResNet-152.       Ethnographic account by         from Platinum new issues
                  78 interviews conducted in    Use of an NLP Porter         English textual corpora (art   Michael Davis (2009) to         database; stock data for firms
                  2013 and 2014 with actors.    stemmer to create 178,872    history books, 4000 critical   provide context.                from CRSP, fundamental data
                  Corpora translated into       unique words recorded on     art NYTimes reviews,           Little preliminary pre-         from Compustat.
                  English, then pre-processed   46,093 pages of 98           online Wikipedia artist        processing. Preprocessing       Extract and clean main text from
                  with NLP. Created a pooled    yearbooks.                   pages, 1,000 art history       performed during the            each S‑1 and 10‑K, keeping
                  data set.                     Corpus pre-processing in     books). Use of RoBERTa         application of the              10,000 most frequent words.
                                                German, results translated   for parsing and organizing     computational tool.
                                                into English.                relevant text.
 Selection of     STM analysis with country     DTM and post-rendering       Artwork pre-processed          Semantic network analysis for   Trained document embedding

 computational    and year as covariates        using STM with temporal      Convolutional Neural           discourse variance around       model to measure firms’

 methods          Interview data to “develop    covariates to benchmark      Networks via ResNet-152        codes and identification of     prototype and outlier similarities.
                  three potential mechanisms    temporal change.             (pre-trained on ImageNet).     sub-communities (sociolects).   Similarities between firms based
                  that seek to theorize how     14 periods based on          Variable creation algorithms   Jaccard and cosine similarity   on their document embeddings.
                  France and Germany’s          history, with 32 topics      (see “Key Measures”            of semantic clusters and code   OLS regression with multiple
                  unique histories … could      Within and between topic     below).                        of ethics terms by document.    fixed effects and clustered
                  have shaped these             distances to measure         OLS with control variables     Topic modeling (LDA) for        standard errors on pooled panel
                  differences”                  change and persistence in    for 942 artists.               rhetorical (meaning) shifts     data.
                                                topics over time.                                           around dominant ethical value
                                                                                                            topics.

--- page 56 ---

Measures for   30 topics to 8 issue frames,     Topics prevalence and         Visual originality as            Ethical consensus as low           Prototypes as centroid of 10‑K

Theory-based   then to field frame (aligned,    clustering to represent       distance of a painting to its    modularity of semantic             embeddings within each

Constructs     conflicting, both).              institutions and              nearest neighbor.                network (Louvain method).          3‑digit SIC/year frame.
               Correlation network among        instantiations.               Expert ranking based on          Community (di)convergence          Outlier similarity as similarity of
               topics as indicators of field-   Within and between topic      mentions in various sources.     as modularity and topic            IPO with highest underpricing in
               level frame alignment for        distances to measure          Peer ranking based on            modeling changes by quarter.       preceding year, irrespective of
               Germany vs. France.              change and persistence in     artist-painting-year network     Topics per document () for        industry.
               Covariates of country and        topics over time.             node degree.                     distinctive topics in a quarter,   Underpricing as difference
               year to capture shifts in key    Focus on topic 21             Market ranking based on          and per topic word probability     between end of first-day market
               frames.                          (“housing”) and its top 100   number of Wiki page hits         (β) for values of                  price and offer price, divided by
                                                words as meaning in each      (2015-21), Google Trends,        standardization.                   offer price.
                                                of 14 periods.                and Artprice activity.
Main           eTranslation.                    DTM as part of a “theory-     ImageNet (pre-trained);          Quanteda package (in R) for        Doc2Vec.

Tools          NLP cleaning.                    method” package.              ResNet-152 for image             semantic network analysis.         Linear panel regression
               STM in R.                        Implemented using either      processing.                      Topic modeling (LDA).              modeling.
                                                Gensim and Mallet, or by      RoBERTa for mentions of          Linear associations (in R).        Coarsened Grain Matching
                                                using Dynamic Topic           artist in narrative.                                                (CEM).
                                                Models from original C++.     Linear modeling package.
Theoretical    Grid of topics to issues to      Grid of main topic            Tag prediction diagram and       Co-occurrence network maps         Prototype and outlier category

Artifacts      field frame alignment.           associated words by period    process from ResNet.             to show sociolects by period.      similarity mapping process.
               Correlation of topic clusters    to capture meaning shifts.    Process for computing            Semantic network key               Interactions of prototype
               to display clustered             Graphs of key topics by       visual originality relative to   measures table by quarter.         similarity outside/within high
               alignment by country.            country by time.              prior and current work           Topic word probability (β) for     tech, and of outlier similarity by
               Graphs of key topics by          Heatmap of institutional      (and/or style).                  words around standardization.      time.
               country by time.                 topics by time.               Process for creating artist’s    vs. educational values by
                                                                              standing by year as cosine       quarter.
                                                                              rank relative to others’
                                                                              ranks.




                                                                                       55

--- page 57 ---

Theoretical   Countries have different         Importance of Red Vienna       Visual originality affects       Centralized leadership frames     Where prototypes are informative

Insights      topic clusters and topics        period for public housing      ranking in all three selection   values during                     about category members,
              often did not align over time:   start; legacy in the form of   systems. Style stage             institutionalization. Iterative   prototype similarity reduces
              France being more regulative     persistence.                   typically lowers rankings.       codification results in focused   underpricing, but the opposite
              and about society and            Increased institutional        Artists with longer careers      discourse.                        happens within high tech
              Germany about the                density and complexity.        have better standings.                                             industries. Outliers lead to more
              environment and economy.                                                                                                           underpricing, but this effect
                                                                                                                                                 decreases over time.
Reflexive     Integrating STM results with     Demonstrating within a         Showing that visual              Demonstration that                Showing that IPO investors

Rendering     historical narratives on two     single field that societal     originality measures relate      quantitative tools (network       actually consider IPO prototype

Challenges    different countries’ issue       culture itself is changing,    to aesthetic appreciation,       analysis and topic modelling)     and outlier similarities in their
              field to show how                not just housing regimes,      and that an artist’s standing    with narrative of change can      decisions, plus that they do so
              mechanisms worked in each.       and that a field’s culture     in a period is an outcome        do more than a narrative built    consistently with categorization
                                               has theoretical and            (not cause) of that effect;      on content analysis of the 613    theory processes.
                                               empirical implications for     pooling many years and           emails with some historical
                                               other fields.                  artists in one associational     embedding.
                                                                              model.




                                                                                    56
