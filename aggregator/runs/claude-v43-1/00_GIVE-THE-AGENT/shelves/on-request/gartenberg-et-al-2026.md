# Gartenberg, Hasan, Murray and Pierce (2026), More versus better: artificial intelligence, incentives, and the emerging crisis in peer review, Organization Science 37(3)

Source: `gartenberg-et-al-2026.pdf`. Text extracted by pdftotext; layout kept, page breaks marked. A quote from this file is the extraction's, so check an odd word against the page it names.

--- page 1 ---

This article was downloaded by: [185.104.138.146] On: 24 August 2026, At: 08:19
Publisher: Institute for Operations Research and the Management Sciences (INFORMS)
INFORMS is located in Maryland, USA


                               Organization Science
                               Publication details, including instructions for authors and subscription information:
                               http://pubsonline.informs.org

                               More Versus Better: Artificial Intelligence,
                               Incentives, and the Emerging Crisis in Peer Review
                               Claudine Gartenberg, Sharique Hasan, Alex Murray, Lamar Pierce




To cite this article:
Claudine Gartenberg, Sharique Hasan, Alex Murray, Lamar Pierce (2026) More Versus Better: Artificial Intelligence,
Incentives, and the Emerging Crisis in Peer Review. Organization Science 37(3):795-812. https://doi.org/10.1287/
orsc.2026.ed.v37.n3


Full terms and conditions of use: https://pubsonline.informs.org/Publications/Librarians-Portal/PubsOnLine-
Terms-and-Conditions

  This article may be used only for the purposes of research, teaching, and/or private study. Commercial use or
systematic downloading (by robots or other automatic processes) is prohibited without explicit Publisher approval,
unless otherwise noted. For more information, contact permissions@informs.org.

  The Publisher does not warrant or guarantee the article’s accuracy, completeness, merchantability, fitness
for a particular purpose, or non-infringement. Descriptions of, or references to, products or publications, or
inclusion of an advertisement in this article, neither constitutes nor implies a guarantee, endorsement, or support
of claims made of that product, publication, or service.

  Copyright © 2026, INFORMS


Please scroll down for article—it is on subsequent pages




With 12,500 members from nearly 90 countries, INFORMS is the largest international association of operations
research (O.R.) and analytics professionals and students. INFORMS provides unique networking and learning
opportunities for individual professionals, and organizations of all types and sizes, to better understand and use
O.R. and analytics tools and methods to transform strategic visions and achieve better outcomes.
For more information on INFORMS, its publications, membership, or meetings visit http://www.informs.org

--- page 2 ---

ORGANIZATION SCIENCE
                                                                                                                                                                                                                                        Vol. 37, No. 3, May–June 2026, pp. 795–812
                                                                                                                             https://pubsonline.informs.org/journal/orsc                                                             ISSN 1047-7039 (print), ISSN 1526-5455 (online)




                                                                                                                             More Versus Better: Artificial Intelligence, Incentives,
                                                                                                                             and the Emerging Crisis in Peer Review
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             Claudine Gartenberg,a Sharique Hasan,b Alex Murray,c Lamar Pierced,*
                                                                                                                             a
                                                                                                                              The Wharton School, University of Pennsylvania, Philadelphia, Pennsylvania 19104; b Duke University, Durham, North Carolina 27708;
                                                                                                                             c
                                                                                                                              University of Oregon, Eugene, Oregon 97403; d Washington University in St. Louis, St. Louis, Missouri 63130
                                                                                                                             *Corresponding author
                                                                                                                             Contact: cgart@wharton.upenn.edu,    https://orcid.org/0000-0003-0696-7266 (CG); sharique.hasan@duke.edu,
                                                                                                                                https://orcid.org/0000-0002-8574-8610 (SH); amm16@uoregon.edu, https://orcid.org/0000-0001-6161-8363 (AM);
                                                                                                                             pierce@wustl.edu, https://orcid.org/0000-0003-0452-1391 (LP)

                                                                                                                             Received: April 2, 2026                       Abstract. As the AI Task Force for Organization Science, we provide an early account of arti­
                                                                                                                             Revised: April 2, 2026                        ficial intelligence’s (AI) impact on both submissions and reviews at a major academic jour­
                                                                                                                             Accepted: April 2, 2026                       nal. Submission volume has risen 42% since the late 2022 release of ChatGPT, while writing
                                                                                                                             Published Online in Articles in Advance:      quality has declined. The rise in AI-generated writing accounts for nearly all of these trends.
                                                                                                                             April 27, 2026                                AI-generated writing in reviews has also increased, and is characterized by lower writing
                                                                                                                                                                           quality and less topical diversity than human-generated writing. We are, to our knowledge,
                                                                                                                             https://doi.org/10.1287/orsc.2026.ed.v37.n3   the first journal to report these early impacts of AI in the review process. Conversations
                                                                                                                                                                           with editors across scientific disciplines, however, suggest that what we observe is not lim­
                                                                                                                             Copyright: © 2026 INFORMS
                                                                                                                                                                           ited to our journal or to the social sciences. At this early stage of AI adoption, we cannot
                                                                                                                                                                           make a normative assessment about appropriate or ideal levels of AI usage. We can, how­
                                                                                                                                                                           ever, conclude that the current state of AI tools, amplified by existing publish-or-perish
                                                                                                                                                                           incentives, appears to be pushing the system toward an equilibrium of more rather than bet­
                                                                                                                                                                           ter research. Reaching an equilibrium in which AI serves as a critical engine of innovation
                                                                                                                                                                           will require that our institutions and the incentive structures they create adapt.

                                                                                                                                                                           Funding: S. Hasan used research funding from Duke University’s Fuqua School of Business. C. Garten­
                                                                                                                                                                             berg used research funding from University of Pennsylvania’s Wharton School.
                                                                                                                                                                           Supplemental Material: The online appendix is available at https://doi.org/10.1287/orsc.2026.ed.v37.n3.

                                                                                                                             Keywords: Artificial Intelligence • Peer Review • Science • Innovation • Evaluation • Incentives • Generative AI

                                                                                                                             1. Introduction                                                                  commercial large language models (LLMs), in Novem­
                                                                                                                             As the AI Task Force for Organization Science, we spent                          ber 2022. We do so using the full corpus of 6,957 initial
                                                                                                                             the last several months studying how generative artificial                       submissions and 10,389 text-inputted reviews handled
                                                                                                                             intelligence (AI) is affecting the workings of our journal.                      by the journal since 2021.1 Focusing on the peer review
                                                                                                                             Our goal was not to cast judgment on what defines                                pipeline provides a distinctive perspective on AI’s
                                                                                                                             appropriate AI use, but rather to provide evidence on                            effects on scientific research. Studies of published arti­
                                                                                                                             how growing AI usage might be reshaping how we eval­                             cles conflate authors’ contributions with editorial selec­
                                                                                                                             uate and promote scientific research. A clear picture is                         tion and revision processes, whereas we can separate
                                                                                                                             emerging: AI language models, combined with strong                               these. And, because submitting to Organization Science
                                                                                                                             publish-or-perish incentives, are pushing our field to pro­                      incurs real costs in terms of elapsed time under review,
                                                                                                                             duce more rather than better research. Journal operations                        these submissions reflect authors’ beliefs about quality.
                                                                                                                             are increasingly strained by growth in low-quality AI-                           Most importantly, our access to reviewer comments and
                                                                                                                             augmented submissions, affecting volunteer editors and                           editorial outcomes allows us to observe how human
                                                                                                                             reviewers alike. While most of these submissions are                             judgment—the scarce input into the review process—
                                                                                                                             rejected, many during the initial deputy editor screen, the                      responds to the rise of AI in submissions and reviews.
                                                                                                                             burden they impose is substantial. We believe that a                                We report AI usage over a five-year window begin­
                                                                                                                             better equilibrium is possible, one in which we work                             ning in January 2021, with the first two years serving as
                                                                                                                             with AI to produce research once thought impossible.                             our “placebo” period for AI writing. We calculate an AI
                                                                                                                             Reaching this equilibrium will require more than just bet­                       writing score for each submission and review using Pan­
                                                                                                                             ter tools, however; it will require better institutions.                         gram, a widely used and validated AI detection tool. On
                                                                                                                                In this report, we analyze how submission and review                          the submission side, we use abstracts as our primary
                                                                                                                             activity at Organization Science have changed following                          text, and validate our patterns using a smaller sample of
                                                                                                                             the release of ChatGPT, the first of many modern                                 full manuscripts to ensure that AI use in abstracts is, on

                                                                                                                                                                                                        795

--- page 3 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             796                                                                Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             average, representative of its use in full submissions.           • Second, while many believe that AI improves
                                                                                                                             Finally, we use the 79% of reviews submitted in text for­      writing quality, we show that AI has led to a deteriora­
                                                                                                                             mat (rather than as PDFs).2                                    tion of prose in submitted manuscripts and reviews.
                                                                                                                                Although Pangram is regarded as the most accurate              • Third, we show that the authors who are most
                                                                                                                             AI detection tool available (Jabarian and Imas 2025),          likely to use AI in writing—research teams from non­
                                                                                                                             no statistical tool is fully reliable when applied to indi­    native English-speaking institutions and new entrants
                                                                                                                             vidual texts. Our analysis is structured accordingly:          to the field—do not benefit in the review process and,
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             we report only aggregate trends across thousands of            in fact, may be hurt when using AI for writing.
                                                                                                                             submissions and reviews, avoiding focus on individ­               • Fourth, while prior research suggests a strong
                                                                                                                             ual submissions and reviews. Also, rather than apply­          overlap between AI and human reviews, we show that
                                                                                                                             ing a binary threshold to classify texts as AI-generated       AI reviews are much narrower than human ones.
                                                                                                                             or human-written, we use Pangram’s continuous                     • Finally, and perhaps most importantly, celebrating
                                                                                                                             score to track shifts in estimates of AI prevalence over       AI as a productivity-generating technology misses its
                                                                                                                             time. Finally, we include a two-year placebo period            collision with the field’s incentive structures. When insti­
                                                                                                                             prior to ChatGPT’s release to establish a baseline             tutional incentives push “pubs” over rigorous research,
                                                                                                                             against which to measure change. Together, these               AI will be used to drive volume rather than to fulfill its
                                                                                                                             choices allow us to identify meaningful shifts in the          potential as a critical research technology.
                                                                                                                             prevalance and quality of AI writing, even as individ­            These findings suggest a complex, systemic challenge
                                                                                                                             ual-level detection remains imperfect.                         with no easy answer for journals, authors, or universities.
                                                                                                                                What we find is sobering. Submission volume has             One point is clear to us: AI has already entered academia
                                                                                                                             risen by 42% since November 2022. At the same time,            with gusto. Based on conversations with editors, both
                                                                                                                             submission writing quality also began to decline at the        inside and outside our field, the patterns we reveal at
                                                                                                                             end of 2022, with Flesch Reading Ease (a standard mea­         Organization Science are surely pervasive across the
                                                                                                                             sure of writing quality) 1.28 standard deviations (SD)         sciences (see also Naddaf 2025, Jones 2026, Munger et al.
                                                                                                                             lower in January 2026 relative to January 2021. Submis­        2026). Trends in “vibe-researching” are increasingly dis­
                                                                                                                             sions that are heavily AI-generated account for nearly         cussed on social media. NeurIPS, the premier AI confer­
                                                                                                                             all of these trends. The quality of reviews has also
                                                                                                                                                                                            ence, saw a 75% increase in research submissions in 2025
                                                                                                                             dropped sharply since November 2022, driven by an
                                                                                                                                                                                            compared with 2023, swamping its human review sys­
                                                                                                                             increase in heavily AI-generated reviews. These reviews,
                                                                                                                                                                                            tem and leading to AI-generated research being accepted
                                                                                                                             in addition to being of worse quality, are also narrower
                                                                                                                                                                                            into the program. Kusumegi et al. (2025) examine pre­
                                                                                                                             in their emphasis, focusing more on theory and less on
                                                                                                                                                                                            print production and find that authors who adopt AI
                                                                                                                             data. In short, more research is being submitted, with
                                                                                                                             more AI writing that is lower in quality—not better.           upload 36% more preprints than nonadopters across the
                                                                                                                                These trends put pressure on a system already under         three major preprint servers (arXiv, bioRxiv, and SSRN).
                                                                                                                             stress. Even before ChatGPT’s introduction, submission         Their study period ended in June 2024, and the trends
                                                                                                                             volumes were climbing, driven by high-powered incen­           have continued and now affect actual journal submis­
                                                                                                                             tives such as publication-count criteria for tenure and        sions and likely publications.
                                                                                                                             financial bonuses. Journals that appear on lists like the         If our findings are, in fact, widespread beyond Orga­
                                                                                                                             UT-Dallas (UTD) and Financial Times 50 (FT50), face            nization Science and if they signify AI usage beyond
                                                                                                                             particular pressure, as these lists define the “right” jour­   what we can observe in writing detectors, they point
                                                                                                                             nals for many schools. If these count incentives are           to a systemic need to reconsider institutions beyond
                                                                                                                             indeed fueling the post-ChatGPT rise in AI-augmented           academic journals, including how we train students,
                                                                                                                             submissions, the effect should be stronger at institutions     incentivize faculty, and judge new ideas and the peo­
                                                                                                                             where these incentives are most pronounced. This is            ple developing them. We are not alone in this conclu­
                                                                                                                             what we find. We proxy for incentive intensity using           sion (Bechky and Davis 2025). Our response cannot be
                                                                                                                             institutional responses to the launch of the UTD journal       purely technical approaches or consist solely of disclo­
                                                                                                                             list in 2005. Schools whose publishing patterns shifted        sure policies or AI “bans.” Disclosure does not solve
                                                                                                                             following the launch—which we designate as “UTD                the volume problem, and AI bans are both unrealistic
                                                                                                                             Responder” schools—exhibit a greater increase in AI-           and counterproductive to research progress. The chal­
                                                                                                                             writing in submissions after ChatGPT’s release.                lenge, therefore, is first to understand what is happen­
                                                                                                                                We believe that AI has the potential to transform           ing and then to steer the equilibrium toward better
                                                                                                                             research and our field. The findings of our task force,        rather than just more research.
                                                                                                                             however, suggest that we are not yet fulfilling this              In the end, academia requires engaged, expert judg­
                                                                                                                             potential:                                                     ment from a community of scholars who invest in
                                                                                                                                • First, the recent rise in journal submission quantity     evaluating each other’s work. If AI only amplifies
                                                                                                                             is primarily due to AI use, not organic growth in the          volume—and lowers quality in the process—we may
                                                                                                                             field or increased journal reputation.                         end up with more research but less collective

--- page 4 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                        797

                                                                                                                             knowledge. As editors who serve as the bulwark                            estimated degree of AI pervasiveness in the text. Zero
                                                                                                                             against inundating reviewers with low-quality                             indicates fully human-written, and one indicates fully
                                                                                                                             AI-driven submissions, we view the current system as                      AI-generated. Pangram segments text into approxi­
                                                                                                                             unsustainable. As our near-universal rejection rates of                   mately 400-word windows and scores each indepen­
                                                                                                                             AI-driven writing show, our human effort has so far                       dently. For multisegment texts (manuscripts), we
                                                                                                                             protected the review process from this tide. But the                      compute a word-count-weighted average across seg­
                                                                                                                             humans are getting tired.                                                 ments to approximate the proportion of text exhibiting
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                                                                       AI characteristics. For single-segment texts (abstracts),
                                                                                                                             2. Data and Measures                                                      which typically fall within a single window, the score
                                                                                                                             We analyzed AI usage across all Organization Science’s                    blends the model’s confidence that AI was used with
                                                                                                                             initial (first-round) submissions and text-inputted                       its estimate of how much of the text reflects AI involve­
                                                                                                                             reviews from January 2021 to February 2026, provid­                       ment. The score should therefore be interpreted as an
                                                                                                                             ing data on journal operations before and after the                       overall signal of AI prevalence in writing rather than
                                                                                                                             launch of ChatGPT in November 2022. For submis­                           the precise proportion of AI-generated text.
                                                                                                                             sions, we focus primarily on abstracts, using the full                       We use both this continuous score and also classify
                                                                                                                             texts of a subset of manuscripts to evaluate whether                      abstracts into four mutually exclusive categories. We
                                                                                                                                                                                                       define a score below 15% as having little to no AI writ­
                                                                                                                             AI use in abstracts is a reasonable proxy for AI use in
                                                                                                                                                                                                       ing use by the authors. A score between 15%–30%
                                                                                                                             the full texts. For peer reviews, we use the full text of
                                                                                                                                                                                                       represents a more “collaborative” use of AI in writing,
                                                                                                                             all referee reports submitted in text format directly
                                                                                                                                                                                                       where the researcher retains primary creative effort.
                                                                                                                             into the ScholarOne system (as opposed to uploaded as
                                                                                                                                                                                                       Scores between 30% and 70% cross the threshold from
                                                                                                                             PDF), which accounts for 79% of all reviews. In total,
                                                                                                                                                                                                       primary human ownership to giving the AI substan­
                                                                                                                             this consists of 6,957 submissions by 11,887 authors,
                                                                                                                                                                                                       tially more control. Finally, we view scores above 70%
                                                                                                                             reviewed 10,389 times by 2,519 unique reviewers.3
                                                                                                                                                                                                       as primarily AI-generated content. These thresholds
                                                                                                                                                                                                       are judgment calls, but different categorizations pro­
                                                                                                                             2.1. AI Detection
                                                                                                                                                                                                       duce similar findings.5 This editorial, for example,
                                                                                                                             Each text is scored by Pangram (v3.1), a deep learning
                                                                                                                                                                                                       received a Pangram score of 8.8, likely reflecting the
                                                                                                                             model trained to classify text as human- or AI-generated.
                                                                                                                                                                                                       light AI-based copyediting disclosed at the beginning.
                                                                                                                             The model is trained with asymmetric loss weighting                       We do not use these scores to define an “optimal” or
                                                                                                                             that makes false positives (human text flagged as AI)                     “appropriate” level of AI-usage in writing.
                                                                                                                             five times less likely than false negatives (AI text classi­                 It is important to make clear that under the data pro­
                                                                                                                             fied as human). Pangram reports a 99.84% accuracy rate                    cessing agreement, Pangram deleted all data after evalu­
                                                                                                                             on human-written text,4 repeatedly updating the models                    ation and did not use them to train its general model,
                                                                                                                             as new AI generations are released. Pangram cannot                        thereby complying with the INFORMS privacy policy.
                                                                                                                             detect AI-usage in nonwriting tasks such as background
                                                                                                                             research or coding, nor can we make any claims about                      2.2. Writing Quality
                                                                                                                             this usage.                                                               We calculate a set of standard writing-quality mea­
                                                                                                                                A 2025 independent AI detection tool evaluation by                     sures for each submission, including Flesch Reading
                                                                                                                             economists Jabarian and Imas (2025) found Pangram to                      Ease, Flesch-Kincaid Grade Level, FOG Index, SMOG
                                                                                                                             have a false positive rate of less than 0.001 when Pan­                   Index, Nominalization, Passive Voice, Jargon, Hedging,
                                                                                                                             gram evaluated samples written by GPT-4.1, Claude                         and Specificity. Online Appendix A4 provides a detailed
                                                                                                                             Opus 4, Claude Sonnet 4, and Gemini 2.0 Flash models,                     description of the scores calculations, which capture two
                                                                                                                             with false negative rates between 0.0045 and 0.038. We                    broad categories of information about writing quality:
                                                                                                                             are using a more advanced Pangram model updated                           (a) readability, the extent to which a text is easier or
                                                                                                                             since the most recent AI releases (e.g., Opus 4.6), pri­                  harder to read for the average person; and (b) style, the
                                                                                                                             marily applied to historical submissions created under                    extent to which certain stylistic features appear in the
                                                                                                                             older technologies, which strengthens our confidence                      text (e.g., nominalizations—where verbs and adjectives
                                                                                                                             in its accuracy. Even if the most recent papers we ana­                   are converted into nouns, passive voice, or hedging with
                                                                                                                             lyze used new advanced models, and the latest Pan­                        words such as “might”, “could”, and “suggest”).
                                                                                                                             gram update does not keep up (for which we have
                                                                                                                             no evidence), the model is trained to minimize false                      2.3. Review Topics and Emphasis
                                                                                                                             positives (human writing labeled as AI). Given that                       To understand what topics reviewers raise in their
                                                                                                                             dynamic, we might, if anything, understate the preva­                     reports, we construct a simple measure of emphasis in
                                                                                                                             lence of AI writing in 2026 submissions and reviews.                      reviews. For each report, we count the frequency of
                                                                                                                                The model outputs a continuous “AI assistance                          specific words indicating five broad foci: theory, con­
                                                                                                                             score” ranging from zero to one, representing the                         tribution, clarity, data, and empirics. Theory words

--- page 5 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             798                                                                                                  Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             include: theory, theoretical, theorize, mechanism,                        Finally, because we have full transaction data for
                                                                                                                             framework, construct, proposition, etc. Contribution                   each manuscript, we connect manuscripts to reviews
                                                                                                                             words include research gap, implications, significance,                and evaluate whether manuscript and review charac­
                                                                                                                             and contribution. Clarity words include readable, well-                teristics (e.g., AI use or author background) affect
                                                                                                                             written, rewrite, confusing, etc. Data words include                   decisions and outcomes (e.g., desk rejects or rejections
                                                                                                                             data, sample, experiment, panel, longitudinal, etc. And                after review). A table of descriptive statistics is avail­
                                                                                                                             finally, words related to empirics include regression,                 able in Online Appendix Table A1.
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             estimate, exogenous, endogenous, and identification. A
                                                                                                                             full list of words is in Online Appendix A5. The word                  3. AI in the Submission Process
                                                                                                                             counts are then converted to relative shares to account
                                                                                                                                                                                                    3.1. AI Use in Submissions is Increasing
                                                                                                                             for variation in the length of the review. To illustrate, the
                                                                                                                                                                                                    We begin by analyzing submission volume over time
                                                                                                                             variable “theory” is the relative emphasis on theory in
                                                                                                                                                                                                    at Organization Science. Like many journals, we have
                                                                                                                             the review versus “data” or “empirics.”6
                                                                                                                                                                                                    observed a substantial increase in submissions since late
                                                                                                                                                                                                    2022. Figure 1 shows this rise. For instance, if we compare
                                                                                                                             2.4. Author and Manuscript Information                                 submission volume between January 2022–November
                                                                                                                                   and Outcomes                                                     2023 (before ChatGPT, but after peak-COVID) to Janu­
                                                                                                                             We supplement these AI measures with author team                       ary 2024–November 2025 (after), we see 42% more sub­
                                                                                                                             and reviewer attributes. Specifically, we focus on two                 missions. In comparison, the COVID-19 bump in
                                                                                                                             author-team metrics. First, we construct a variable,                   submissions was 20%, half the size of the AI effect.
                                                                                                                             All non-Native English Institution Authors, that equals 1                 While there could be many reasons for the rise in
                                                                                                                             if all authors are based at institutions in nonnative                  submissions, including reduced backlogs, increased
                                                                                                                             English-speaking countries (e.g., not based in the                     scholar productivity, or journal reputation, Figure 2
                                                                                                                             United States, Canada, United Kingdom, Australia,                      suggests that the disproportionate increase in submis­
                                                                                                                             South Africa, or New Zealand) and 0 otherwise. On                      sion volume is driven by AI use. Post-ChatGPT,
                                                                                                                             average, we anticipate that such teams are less likely                 we see a marked decline in submissions flagged at
                                                                                                                             to include native English speakers and more likely to                  0%–15% AI (little to no AI use) and a corresponding
                                                                                                                             view AI as both a language and a writing assistant.                    rise in all other categories that make up the difference
                                                                                                                             This is clearly a noisy measure, as authors at such                    between the decline in human-only submissions and
                                                                                                                             institutions may be native speakers or excellent wri­                  the 42% increase in total submissions.
                                                                                                                             ters, and vice versa. Similarly, some locations, such as                  Figure 3 shows the shift in composition more clearly.
                                                                                                                             Hong Kong, have multiple official languages, includ­                   It plots the relative shares of human- and AI-authored
                                                                                                                             ing English. Second, we construct a variable, Prior OS                 abstracts over time. Prior to the launch of ChatGPT, rel­
                                                                                                                             Submissions, that counts the number of submissions to                  ative shares were flat. Nearly all submissions were
                                                                                                                             Organization Science made by members of the author                     classified as human (with some idiosyncratic noise).
                                                                                                                             team over the past 15 years.
                                                                                                                                                                                                    Figure 2. Monthly Submission Volume by AI Use Categories
                                                                                                                             Figure 1. Monthly Submission Volume at Organization Sci­               over Time
                                                                                                                             ence from January 2013 Until the End of 2025
                                                                                                                                                                                                                            200




                                                                                                                                                                                                                                             Total           ChatGPT

                                                                                                                                                                                                                                             0-15% AI
                                                                                                                                   150




                                                                                                                                                                     COVID-19     ChatGPT
                                                                                                                                                                                                                                             15%-30% AI
                                                                                                                                                                                                                                             30%-70% AI
                                                                                                                                                                                                                            150
                                                                                                                                                                                                    Number of Submissions




                                                                                                                                                                                                                                             70%+ AI
                                                                                                                                     100




                                                                                                                                                                                                                            100
                                                                                                                             Frequency




                                                                                                                                                                                                                            50
                                                                                                                                   50




                                                                                                                                                                                                                            0




                                                                                                                                                                                                                                  2021         2022         2023         2024         2025          2026
                                                                                                                                   0




                                                                                                                                     2013   2015   2017      2019      2021     2023        2025                                                              Submission Date
                                                                                                                                                           Submission Date
                                                                                                                                                                                                    Notes. Each line shows the share of first submissions’ abstracts classi­
                                                                                                                             Note. The dashed vertical line marks the launch of ChatGPT in Novem­   fied as 0%–15% AI, 15%–30%, 30%–70%, 70%+. The dashed vertical
                                                                                                                             ber 2022 and the start of the COVID-19 pandemic in March 2020.         line marks the launch of ChatGPT in November 2022.

--- page 6 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                                                                                            799

                                                                                                                             Figure 3. Trends in AI Use Categories over Time                                     Figure 4. AI Scores for Each Section of a Sample of Manu­
                                                                                                                                                                                                                 scripts Stratified by AI Scores Falling into Low (<30), Medium
                                                                                                                                                    1
                                                                                                                                                                                0-15% AI            15%-30% AI   (between 30 and 70), and High (>70) Categories
                                                                                                                                                                                30%-70% AI          70%+ AI
                                                                                                                                                                                                                                      1
                                                                                                                                                    .8
                                                                                                                             Share of Submissions




                                                                                                                                                                                                                                      .8
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                    .6

                                                                                                                                                                    ChatGPT




                                                                                                                                                                                                                  Mean AI Score
                                                                                                                                                                                                                                      .6
                                                                                                                                                    .4

                                                                                                                                                                                                                                      .4
                                                                                                                                                    .2

                                                                                                                                                                                                                                      .2

                                                                                                                                                    0
                                                                                                                                                     2021   2022   2023        2024          2025       2026
                                                                                                                                                                                                                                      0
                                                                                                                                                                     Submission Date
                                                                                                                                                                                                                                           Abstract        Intro           Theory   Methods       Results Discussion Conclusion

                                                                                                                             Notes. Each line shows the share of first-submission abstracts classi­                                                   Abstract AI < 0.30            Abstract AI 0.30-0.70           Abstract AI > 0.70
                                                                                                                             fied as 0%–15%, 15%–30%, 30%–70%, or 70%+ AI. The dashed verti­
                                                                                                                             cal line marks the launch of ChatGPT in November 2022.                              Note. Errors are larger for lower AI manuscripts because we over­
                                                                                                                                                                                                                 sampled on high AI for this analysis due to computational
                                                                                                                                                                                                                 constraints.

                                                                                                                             Immediately after the launch of the first commercial
                                                                                                                             LLM chatbots, a precipitous decline in human-only                                   (>70%) in the abstract do indeed signal high AI use
                                                                                                                             submissions began. At the same time, we observe a                                   throughout the manuscript. In particular, section-level
                                                                                                                             steady rise in all categories of AI-supported or gener­                             Pangram scores show elevated AI usage across all sec­
                                                                                                                             ated submissions. What is most striking is that by Feb­                             tions, including introduction, theory, methods, results,
                                                                                                                             ruary 2026, the majority of submissions submitted to                                discussion, and conclusion. AI scores are especially
                                                                                                                             Organization Science use AI in their writing to some                                pronounced in writing-heavy sections such as the
                                                                                                                             degree. The most striking trend is the rise of the 70%+                             introduction, theory, discussion, and conclusion, but
                                                                                                                             AI category, where text is mostly or entirely generated                             there is also meaningful AI use in the methods and
                                                                                                                             by AI. While we are reporting AI use in abstracts, this                             results sections. In contrast, manuscripts classified as
                                                                                                                             trend is also evident in the subsample of full manu­                                moderate (between 30% and 70%) and low AI (below
                                                                                                                             scripts we analyzed.

                                                                                                                             3.2. AI in Abstracts Reflects AI in Full                                            Figure 5. Scatterplot of AI Use in Abstract (x-axis) vs. AI Use
                                                                                                                                   Manuscripts                                                                   Within the Manuscript Body (Mean of AI Use in Introduction,
                                                                                                                             The prior graphs use only the abstract to compute a                                 Theory, Methods, Results, Discussion, Conclusion)
                                                                                                                             submission’s AI score. We therefore tested whether AI                                                     1
                                                                                                                             use in the abstract is a reasonable proxy for AI use in
                                                                                                                             the full manuscript. To do so, we examine the distri­
                                                                                                                                                                                                                                      .8
                                                                                                                             bution of AI scores in a strategically sampled popula­
                                                                                                                                                                                                                 Mean Body AI Score




                                                                                                                             tion of 230 manuscripts, namely those that score very
                                                                                                                             high on AI and a subset of counterfactual manuscripts                                                    .6

                                                                                                                             with medium and low AI scores. We focused on three
                                                                                                                             sets of manuscripts: (a) 104 that were flagged as below                                                  .4

                                                                                                                             30%, (b) 49 that were flagged as between 30%–70%,
                                                                                                                             and (c) 77 that were flagged at 70%+ AI. Due to com­                                                     .2
                                                                                                                             putational and cost constraints, we limited our analy­
                                                                                                                             sis to this sample. Group (a) had a mean abstract score                                                   0
                                                                                                                             of 0.123; (b) of 0.467; and (c) of 0.955.                                                                     0                .2                  .4             .6              .8                    1
                                                                                                                                                                                                                                                                                Abstract AI Score
                                                                                                                                We divide the manuscript into six sections: intro­
                                                                                                                                                                                                                                                        45-degree line                Local polynomial fit   Manuscripts (N=231)
                                                                                                                             duction, theory, methods, results, discussion, and con­
                                                                                                                             clusion, and then calculate Pangram scores for each                                 Notes. High AI use in the abstract is highly correlated with AI use
                                                                                                                                                                                                                 throughout the manuscript, but there is considerable variation at
                                                                                                                             section.
                                                                                                                                                                                                                 each level. Some manuscripts with low AI use in the abstract still
                                                                                                                                Overall, as shown in Figure 4, the full-text analysis                            have high AI use in the body, while some with high AI use in the
                                                                                                                             of sampled manuscripts indicates that high AI scores                                abstract have much lower AI use in the paper.

--- page 7 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             800                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             30%) based on the abstract show lower AI usage in                                                Figure 7. Distribution of Flesch Reading Ease by Level of AI
                                                                                                                             the abstract but still indicate high levels of AI usage                                          in the Submission Abstract
                                                                                                                             throughout, with similar patterns of relatively higher
                                                                                                                             usage in more writing-heavy sections.                                                                      .03

                                                                                                                                Overall, we feel confident that, in aggregate, AI use
                                                                                                                             in abstracts is a reasonable proxy for AI use in manu­
                                                                                                                             scripts. However, we cannot make this assertion for
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                                                                                                        .02




                                                                                                                                                                                                                              Density
                                                                                                                             any specific manuscript without directly measuring
                                                                                                                             its full text. Indeed, Figure 5 suggests that while AI
                                                                                                                             use in the abstract is a strong proxy for AI use                                                           .01

                                                                                                                             throughout the manuscript, there is considerable vari­
                                                                                                                             ation across manuscripts.
                                                                                                                                                                                                                                         0
                                                                                                                                                                                                                                              -200                              -100                    0                             100
                                                                                                                             3.3. AI is Associated with Worse Writing                                                                                                               Flesch Reading Ease
                                                                                                                             So far, our analysis shows a steady rise in submis­                                                                          Pre-ChatGPT (N=8532)           Post: 0-15% AI (N=2598)   Post: 15-30% AI (N=699)
                                                                                                                                                                                                                                                          Post: 30-70% AI (N=665)        Post: 70%+ AI (N=424)
                                                                                                                             sions, with AI-supported manuscripts dominating.
                                                                                                                             We now turn to the central question: Are these manu­                                             Note. The upper tail of writing scores is mostly all human-written
                                                                                                                             scripts higher-quality? Figure 6 plots normalized Flesch                                         text, both pre- and post-Chat GPT.
                                                                                                                             Reading Ease for every initial submission to Organiza­
                                                                                                                             tion Science from 2013 to February 2026, standardized
                                                                                                                             to a mean of zero and standard deviation of 1. We do                                             distribution of reading ease scores across AI levels.
                                                                                                                             not find much evidence that the writing quality of those                                         Higher AI levels are associated with a negative shift in
                                                                                                                             manuscripts changed meaningfully between 2013 and                                                reading ease scores.
                                                                                                                             November 2022, when ChatGPT was launched. In con­                                                   Figure 8 shows coefficient sizes for the relationship
                                                                                                                             trast, post-ChatGPT, we see a precipitous decline in the                                         between AI Scores for abstracts and various writing
                                                                                                                             average manuscript’s Reading Ease score. Indeed, AI                                              quality measures. All models include fixed effects for
                                                                                                                             scores and Flesch Reading Ease are negatively corre­                                             time (quarters) and editor; all standard errors are two-
                                                                                                                             lated (ρ � �0:4; p ≤ :001). While the prior figure reflects                                      way clustered at these levels. Online Appendix A4 con­
                                                                                                                             a significant decline in the mean reading ease across                                            tains the definitions of each of our writing quality mea­
                                                                                                                             manuscripts, Figure 7 shows a marked shift in the                                                sures. We find strong evidence that AI use is associated

                                                                                                                             Figure 6. Trends in Flesch Reading Ease (Abstracts) from 2013 to February 2026 with Markers for COVID-19 and the Launch of
                                                                                                                             ChatGPT

                                                                                                                                                                               1
                                                                                                                                                                                                                                               COVID-19                       ChatGPT
                                                                                                                                             Flesch Reading Ease (SD units)




                                                                                                                                                                              .5




                                                                                                                                                                               0




                                                                                                                                                                              -.5




                                                                                                                                                                              -1
                                                                                                                                                                                    13



                                                                                                                                                                                          14



                                                                                                                                                                                                15



                                                                                                                                                                                                      16



                                                                                                                                                                                                            17



                                                                                                                                                                                                                  18



                                                                                                                                                                                                                         19



                                                                                                                                                                                                                                        20



                                                                                                                                                                                                                                                     21



                                                                                                                                                                                                                                                                22



                                                                                                                                                                                                                                                                           23



                                                                                                                                                                                                                                                                                     24



                                                                                                                                                                                                                                                                                                25



                                                                                                                                                                                                                                                                                                          26
                                                                                                                                                                                20



                                                                                                                                                                                         20



                                                                                                                                                                                               20



                                                                                                                                                                                                     20



                                                                                                                                                                                                           20



                                                                                                                                                                                                                 20



                                                                                                                                                                                                                        20



                                                                                                                                                                                                                                20



                                                                                                                                                                                                                                                20



                                                                                                                                                                                                                                                              20



                                                                                                                                                                                                                                                                         20



                                                                                                                                                                                                                                                                                    20



                                                                                                                                                                                                                                                                                              20



                                                                                                                                                                                                                                                                                                        20




                                                                                                                                                                                                                       Submission Date

--- page 8 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                             801

                                                                                                                             Figure 8. Association Between AI Use Categories and Different Measures of Writing Quality

                                                                                                                                                   Higher = Better Quality
                                                                                                                                                             Flesch Reading Ease

                                                                                                                                                                          Specificity
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                  Higher = Worse Quality
                                                                                                                                                                       Grade Level

                                                                                                                                                                          Fog Index

                                                                                                                                                                       SMOG Index

                                                                                                                                                                     Nominalization

                                                                                                                                                                     Passive Voice

                                                                                                                                                                              Jargon

                                                                                                                                                                            Hedging

                                                                                                                                                                                        -1.5           -1        -.5            0           .5      1
                                                                                                                                                                                                            Effect of AI Score (SD units)

                                                                                                                             Note. See Online Appendix A4 for definitions of each writing measure and how it is calculated.


                                                                                                                             with lower-quality writing across most of these tradi­                         (e.g., mentioning numbers).7 Overall, AI text is more
                                                                                                                             tional measures. This result is counterintuitive. Authors                      direct and specific, but also more difficult to read.
                                                                                                                             often assume that using AI will improve their writing.
                                                                                                                             However, this is not the case, at least when authors                           3.4. AI Use and Editorial Outcomes
                                                                                                                             substantially offload their writing to it.                                     Writing metrics are only one aspect of quality. Manu­
                                                                                                                                AI prose is more difficult to read on several dimen­                        scripts also have intellectual content. However, evalu­
                                                                                                                             sions. Beyond substantially lower Flesch Reading Ease                          ating a paper’s research content is much more
                                                                                                                             scores, the grade level required to understand the text                        challenging to do algorithmically. Fortunately, in our
                                                                                                                             is higher (more multisyllabic words); the FOG and                              current academic system, journals are tasked with
                                                                                                                             SMOG indices increase, suggesting more complex text;                           exactly this effort. At Organization Science, the review
                                                                                                                             and the use of jargon increases. We also find increased                        process unfolds as follows. First, a managing editor
                                                                                                                             use of nominalizations (e.g., “conceptualization”,                             evaluates the manuscript for basic flags, including pla­
                                                                                                                             “operationalization”, or “contextualization”). We do                           giarism or any other indicator that the manuscript
                                                                                                                             see better scores in some writing measures, with less                          should not be forwarded to a deputy editor for a deci­
                                                                                                                             passive text, less hedging, and greater specificity                            sion. Manuscripts that pass the initial plagiarism check

                                                                                                                                          Table 1. Editorial Pipeline by AI Category (Post-ChatGPT)

                                                                                                                                                                                           0%–15% AI           15%–30% AI           30%–70% AI      70%+ AI

                                                                                                                                          Total Manuscripts                                    2,754               771                   717           473
                                                                                                                                          Desk Rejected                                    1,204 (43.7%)       300 (38.9%)           407 (56.8%)   329 (69.6%)
                                                                                                                                          Sent to Review                                   1,550 (56.3%)       471 (61.1%)           310 (43.2%)   144 (30.4%)
                                                                                                                                          Rejected After Review                            1,124 (72.5%)       312 (66.2%)           222 (71.6%)   83 (57.6%)
                                                                                                                                          Received R&R                                      329 (11.9%)        101 (13.1%)            40 (5.6%)     15 (3.2%)
                                                                                                                                          Overall Rejection Rate                               84.6%              79.4%                 87.7%        87.1%
                                                                                                                                          Mean Readability (std)                                0.04              �0.33                 �0.61        �1.27
                                                                                                                                          Mean Readability, std (Survivors)                     0.10              �0.30                 �0.52        �1.09
                                                                                                                                          Notes. Sample: First submissions after the launch of ChatGPT (November 30, 2022). Desk Rejected and Sent to Review
                                                                                                                                          percentages are of Total Manuscripts. Rejected After Review percentage is of those Sent to Review. R&R percentage is
                                                                                                                                          of Total Manuscripts.

--- page 9 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             802                                                                              Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                                    Table 2. Predictors of Desk Rejection

                                                                                                                                                                           Desk Reject        Desk Reject           Desk Reject          Desk Reject          Desk Reject

                                                                                                                                    Readability (std)                       �0.027***             �0.028***            �0.023***            �0.023***            �0.023***
                                                                                                                                                                             (0.008)               (0.008)              (0.007)              (0.007)              (0.007)
                                                                                                                                    AI Score                                 0.299***              0.266***             0.187***             0.188***             0.191***
                                                                                                                                                                             (0.035)               (0.025)              (0.020)              (0.021)              (0.025)
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                    All Non-Native English                                                              0.322***             0.321***             0.322***
                                                                                                                                                                                                                        (0.011)              (0.012)              (0.013)
                                                                                                                                    AI Score × Non-Native English                                                                                                 �0.006
                                                                                                                                                                                                                                                                  (0.044)
                                                                                                                                    _cons                                    0.385***             0.390***              0.282***             0.282***             0.282***
                                                                                                                                                                             (0.022)              (0.008)               (0.008)              (0.005)              (0.005)
                                                                                                                                    Observations                               6,725                6,725                6,725                6,724                6,724
                                                                                                                                    R2                                         0.034                0.058                0.154                0.163                0.163
                                                                                                                                    Quarter FE                                                       Yes                  Yes                  Yes                  Yes
                                                                                                                                    Editor FE                                                                                                  Yes                  Yes
                                                                                                                                    Notes. Standard errors in parentheses. All models use two-way clustered SE by quarter and editor.
                                                                                                                                      *p < 0:10; **p < 0:05; ***p < 0:01.


                                                                                                                             are sent to a deputy editor, who decides whether the                       & Resubmit decisions, compared with over three times
                                                                                                                             paper should go out for review and, if so, which senior                    that rate among low-AI submissions. In other words,
                                                                                                                             editor should handle it. If a manuscript moves forward,                    editors, likely without recognizing the writing as
                                                                                                                             a senior editor decides whether to send the paper out for                  AI-generated, consistently judged these manuscripts
                                                                                                                             review or desk-reject it, with these assignments more                      as lower quality and unworthy of reviewers’ time.
                                                                                                                             closely aligned with the senior editor’s expertise than                    Interestingly, submissions in the 15%–30% range show
                                                                                                                             those of the deputy editor, who operates more as a gen­                    a slight increase in success rates, possibly reflecting a
                                                                                                                             eralist within a subfield. Finally, reviewers provide writ­                more human-first collaboration mode or differences
                                                                                                                             ten feedback and a recommended decision, followed by                       in authors, topics, and other factors that we cannot
                                                                                                                             the editor’s final determination. In short, the editorial                  disentangle. Nevertheless, this slightly elevated R&R
                                                                                                                             and peer-review process is intensive and expressly                         rate from 0%–15% (11.9%) to 15%–30% (13.1%) is not
                                                                                                                             designed to assess papers on their intellectual content.                   statistically different (p � 0:387). As such, the 30%
                                                                                                                                Table 1 provides descriptive evidence of manuscript                     threshold marks a sharp divide, with manuscript pro­
                                                                                                                             outcomes by level of AI use, restricted to the post-                       spects declining steadily above it.
                                                                                                                             ChatGPT period to ensure comparability. A clear pat­                          In Tables 2 and 3, we examine the relationship
                                                                                                                             tern emerges above 30% AI use. Manuscripts crossing                        between AI use and editorial decisions at the initial
                                                                                                                             this threshold have desk rejection rates nearly 30 per­                    screen and after review, respectively. These models
                                                                                                                             centage points higher than those below it, a 60%–80%                       also include quarter and editor fixed effects, with stan­
                                                                                                                             relative increase. By the end of the editorial funnel,                     dard errors cross-clustered at these two levels. Table 2
                                                                                                                             only 3.2% of high-AI papers (70%+ AI) receive Revise                       shows that higher writing quality is associated with

                                                                                                                                               Table 3. Predictors of a Paper Being Rejected After It Is Sent Out for Review

                                                                                                                                                                                          (1)                   (2)                  (3)                  (4)
                                                                                                                                                                                         Reject                Reject               Reject               Reject

                                                                                                                                               AI Score                                  0.086***             0.075***             0.072***             0.108***
                                                                                                                                                                                         (0.023)              (0.024)              (0.023)               (0.032)
                                                                                                                                               All Non-Native English                                         0.082***             0.081***             0.099***
                                                                                                                                                                                                              (0.015)              (0.015)               (0.014)
                                                                                                                                               AI Score × Non-Native English                                                                            �0.143**
                                                                                                                                                                                                                                                         (0.066)
                                                                                                                                               _cons                                     0.715***             0.697***             0.698***             0.694***
                                                                                                                                                                                         (0.002)              (0.003)              (0.002)               (0.002)
                                                                                                                                               Observations                               3,801                3,801                3,800                3,800
                                                                                                                                               R2                                         0.148                0.154                0.160                0.161
                                                                                                                                               Editor FE                                                                             Yes                  Yes
                                                                                                                                               Notes. Standard errors in parentheses. All models include quarter FE and two-way clustered SE. Sample:
                                                                                                                                               Non-desk-rejected submissions only.
                                                                                                                                                 *p < 0:10; **p < 0:05; ***p < 0:01.

--- page 10 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                            803

                                                                                                                             lower rates of desk rejection. More importantly, manu­                    editors and senior editors—leading to higher rates of
                                                                                                                             scripts with more AI also have a significantly higher                     desk rejection and rejection after review. Furthermore,
                                                                                                                             rejection rate (+0.293 above the baseline of 0.399), inde­                given the time period we analyze, it is unlikely that edi­
                                                                                                                             pendent of writing quality. This suggests that the                        tors flagged these manuscripts as “AI.” Rather, a gen­
                                                                                                                             higher rejection rates are not due only to poor writing,                  eral quality assessment was conducted, and high-AI
                                                                                                                             but also to underlying quality issues that we cannot                      papers were deemed substantially worse, often not
                                                                                                                             observe in this analysis, but editors and reviewers do                    worth the reviewers’ time.
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             when assessing each paper on its own.
                                                                                                                                We next test whether AI use by All Non-Native English                  3.5. Are Publication Incentives Driving the
                                                                                                                             teams helps them in the review process. Many authors                            AI Surge?
                                                                                                                             use AI with the assumption that it will improve their                     The rise in low-quality AI-augmented submissions
                                                                                                                             writing, thereby making publication easier. As a base­                    raises the question: What incentives are driving this
                                                                                                                             line, we find that All Non-Native English teams do                        behavior? While academics might write more low-
                                                                                                                             indeed have an elevated desk rejection rate. The high                     quality papers for many reasons, one explanation is a
                                                                                                                             rate may be due to several factors: topic relevance, theo­                strategic response to supply-side incentives. In recent
                                                                                                                             retical framing, methods, differences in writing style,                   years, many business schools have adopted “journal
                                                                                                                             among others. Including this term decreases the “AI                       lists”—a curated set of journals that count toward ten­
                                                                                                                             score” coefficient from 0.266 to 0.187. Nevertheless,                     ure and promotion. Some schools award significant
                                                                                                                             these appear to be two distinct negative correlations in                  financial rewards to faculty publishing in these speci­
                                                                                                                             the review process. In column (5), we interact the AI                     fic outlets. A prominent example of a widely used
                                                                                                                             score and the All Non-Native English variable. We find                    journal list is compiled by UT-Dallas (hereafter, UTD)
                                                                                                                             little evidence that AI use by authors from nonnative                     and includes 24 journals, including Organization Sci­
                                                                                                                             English-speaking countries is related to more favorable                   ence. Journals on this list are used to rank the top 100
                                                                                                                             decisions. The coefficient on the interaction term is near                schools by publication output. Many schools also
                                                                                                                             zero. These effects persist even after accounting for edi­                “count” publications based on the FT50 list or the
                                                                                                                             tor fixed effects and time trends.                                        Academic Journal Guide system (or their own custom
                                                                                                                                The specific mechanisms behind these patterns are                      variants), but the UTD journals are almost universally
                                                                                                                             beyond the scope of this analysis. It is worth noting                     in the top category in all of these.
                                                                                                                             that, when the author fixed effects are included in                          Institutions do not publicly announce their publica­
                                                                                                                             Table A5, for example, using manuscripts by the same                      tion incentives; therefore, we try to infer this from differ­
                                                                                                                             author submitted with high and low-AI use, the effect                     ences in publication patterns across schools. When the
                                                                                                                             of AI becomes insignificant for manuscript decisions,
                                                                                                                                                                                                       UTD rankings were introduced in 2005, we observed a
                                                                                                                             but the effect of writing quality remains significant
                                                                                                                                                                                                       sharp discontinuity in the publication response of some
                                                                                                                             and negative as can be seen in Table A4. Nevertheless,
                                                                                                                                                                                                       schools. To identify “UTD Responder” schools, we com­
                                                                                                                             a key takeaway from this analysis is that AI writing
                                                                                                                                                                                                       pare each school’s average annual UTD publications
                                                                                                                             does not appear to benefit authors.8
                                                                                                                                                                                                       before (1990–2004) and after (2005–2020) the rankings
                                                                                                                                In Table 3, we analyze whether AI use affects the
                                                                                                                                                                                                       were introduced. We classify schools whose difference
                                                                                                                             editorial outcomes of papers sent out for review by a
                                                                                                                                                                                                       between pre- and post-UTD publication volume is
                                                                                                                             senior editor. The pattern of results is similar: greater AI
                                                                                                                                                                                                       above the median as Responders. We then match each
                                                                                                                             use is associated with higher rejection rates. We again
                                                                                                                                                                                                       responder to a nonresponder based on having an
                                                                                                                             find that All Non-Native English teams have higher rejec­
                                                                                                                                                                                                       equivalent pre-UTD (e.g., prior to 2005) publication
                                                                                                                             tion rates. However, conditional on overcoming the
                                                                                                                             desk rejection threshold, the two coefficients—of AI and                  record. Critically, the designation of a school as a
                                                                                                                             non-Native English—on rejections are reduced by                           UTD Responder is based on data generated prior to
                                                                                                                             nearly half. That is not to say that non-Native English                   ChatGPT’s launch in November 2022. In our matched
                                                                                                                             authors are helped by AI at this stage, but rather that                   sample analysis below, we have 48 schools that serve
                                                                                                                             they are not doubly hurt because they use AI. Neverthe­                   as our “control” non-Responder schools, and 48
                                                                                                                             less, the main action for heavily AI-driven manuscripts                   matched schools designated as “UTD Responders.”
                                                                                                                             is at the desk-reject stage.                                                 We use this data to test whether supply-side incen­
                                                                                                                                Together, these findings suggest that AI use in sub­                   tives drove AI adoption. We estimate the following
                                                                                                                             missions to Organization Science is of the “more” rather                  specification at the school × month level:
                                                                                                                             than “better” variety. The marginal AI submission is                                Ys, t � αs + γt + β(UTD Responders
                                                                                                                             of lower quality and is more likely to be desk-rejected.
                                                                                                                                                                                                                       × Post-ChatGPTt ) + εs, t                 (1)
                                                                                                                             AI usage appears to reflect underlying information
                                                                                                                             about the quality of the manuscript, information that is                  where αs and γt denote school and month-year fixed
                                                                                                                             being picked up in the review process by both deputy                      effects, respectively. The school fixed effects account

--- page 11 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             804                                                                        Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             for time-invariant differences in business school sub­                 researcher population and submission counts. The
                                                                                                                             mission patterns to Organization Science, while the                    results in Panel B are directionally similar.
                                                                                                                             month-year fixed effects absorb common time shocks                        In short, AI adoption—in particular, heavy reliance
                                                                                                                             such as overall submission trends (e.g., the journal pub­              on AI writing in manuscripts—is not solely a function
                                                                                                                             lishing more papers). UTD Responders equals one if                     of the introduction of language models themselves.
                                                                                                                             the school is classified as an above-median responder,                 Instead, it appears to reflect a rational response by
                                                                                                                             and Post-ChatGPTt equals one for months from                           authors to their home institution’s incentives, particu­
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             November 2022 onward. Standard errors are two-way                      larly within schools that emphasize journal lists and
                                                                                                                             clustered by school and month-year. Note that schools                  publication counts. We caution, however, that our
                                                                                                                             are included as matched pairs with equivalent pre-                     measure of school incentives is noisy. This topic
                                                                                                                             UTD (pre-2005) publication volumes but divergent                       deserves further, more rigorous analysis.
                                                                                                                             volumes afterward (until 2020). It is important to note
                                                                                                                             that the “UTD Responder” designation is fixed before
                                                                                                                             our sample period starts in January 2021.                              4. AI in the Review Process
                                                                                                                                Our dependent variables Y are calculated as the                     4.1. AI Use in Reviews over Time
                                                                                                                             number of monthly submissions each school makes                        We now turn our attention to the review side of the
                                                                                                                             to Organization Science. Specifically, we have five                    process. We again apply Pangram AI detection to the
                                                                                                                             dependent variables: total submission volume, and                      submitted reviews in Organization Science. We analyze
                                                                                                                             submission counts decomposed into four AI-intensity                    reviews entered into the system as raw text, which
                                                                                                                             bands—0%–15%, 15%–30%, 30%–70%, and 70%+ AI                            accounts for 79% of the total.
                                                                                                                             score—allowing us to identify which types of submis­                      We first analyze the proportion of reviews catego­
                                                                                                                             sions are driving any aggregate effect.                                rized in our AI-intensity bands—0%–15%, 15%–30%,
                                                                                                                                In Table 4, we test this supply-side incentive mech­                30%–70%, and 70%+ AI score. While AI use in reviews
                                                                                                                             anism. We focus our analysis on two sample popula­                     is not as pervasive as in manuscripts, over 30% of
                                                                                                                             tions. In Panel A, we include all schools in our                       reviews in Organization Science still use some degree
                                                                                                                             analysis. We find that the coefficient of interest (UTD                of AI today. The fastest growing category consists of
                                                                                                                             Responder × Post-ChatGPT) is positive and signifi­                     reviews classified as 30%–70% AI, a category that our
                                                                                                                             cant for overall volume, and all AI categories above                   experiments suggest consists of substantial use of AI
                                                                                                                             15%. UTD Responders, after ChatGPT’s launch,                           in the writing process. These results are presented in
                                                                                                                             increased their AI submissions substantially more                      Figure 9.
                                                                                                                             than schools without “counting” incentives. In Panel                      Next, in Figure 10, we report on the quality of writ­
                                                                                                                             B, we exclude schools based in Mainland China and                      ing in these reviews over time, standardized to a
                                                                                                                             Hong Kong from our analysis. This exclusion is                         mean of zero and a standard deviation of one. As with
                                                                                                                             intended to address concerns that our results are                      paper submissions, we observe a similar, marked
                                                                                                                             driven by a subset of schools with a fastest growing                   decline in the Flesch Reading Ease of the reviews

                                                                                                                                   Table 4. Do Schools That Responded to UTD Rankings Also Respond to the Availability of AI?

                                                                                                                                                                            (1)             (2)                   (3)                    (4)                   (5)
                                                                                                                                                                          Volume         0%–15% AI            15%–30% AI             30%–70% AI              70%+ AI
                                                                                                                                                                                     Panel A: All schools
                                                                                                                                   UTD Responder × Post-ChatGPT            0.101**          �0.005               0.060***               0.032***              0.014*
                                                                                                                                                                           (0.040)          (0.029)              (0.016)                (0.010)               (0.008)
                                                                                                                                   Observations                             6,048           6,048                 6,048                   6,048                6,048
                                                                                                                                   R2                                       0.250           0.185                 0.109                   0.076                0.074
                                                                                                                                   School FE                                 Yes             Yes                   Yes                     Yes                  Yes
                                                                                                                                   Month FE                                  Yes             Yes                   Yes                     Yes                  Yes
                                                                                                                                                                    Panel B: Excluding Chinese Mainland and Hong Kong
                                                                                                                                   UTD Responder × Post-ChatGPT            0.067*           �0.009               0.048***                0.024**               0.007
                                                                                                                                                                           (0.036)          (0.027)              (0.015)                 (0.009)              (0.006)
                                                                                                                                   Observations                             5,796           5,796                 5,796                   5,796                5,796
                                                                                                                                   R2                                       0.231           0.171                 0.103                   0.071                0.061
                                                                                                                                   School FE                                 Yes             Yes                   Yes                     Yes                  Yes
                                                                                                                                   Month FE                                  Yes             Yes                   Yes                     Yes                  Yes
                                                                                                                                   Notes. Two-way clustered SE by school and month-year. 1:1 nearest-neighbor matched on pre-2005 publication levels (no
                                                                                                                                   replacement). Classification uses 1990–2020 data only (pre-ChatGPT). 0%–15% AI: <0.15; 15%–30% AI: 0.15–0.30; 30%–70% AI:
                                                                                                                                   0.3–0.7; 70%+ AI: >0.7.

--- page 12 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                                                                   805

                                                                                                                             Figure 9. AI Use in Reviews Over Time

                                                                                                                                                                                   1
                                                                                                                                                                                                                                                    0-15% AI                            15%-30% AI

                                                                                                                                                                                   .9                                                               30%-70% AI                          70%+ AI


                                                                                                                                                                                   .8
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                                                   .7
                                                                                                                                                    Share of Reviews




                                                                                                                                                                                   .6

                                                                                                                                                                                   .5                                           ChatGPT



                                                                                                                                                                                   .4

                                                                                                                                                                                   .3

                                                                                                                                                                                   .2

                                                                                                                                                                                   .1

                                                                                                                                                                                   0
                                                                                                                                                                                   2021                   2022              2023        2024                           2025                     2026
                                                                                                                                                                                                                           Review Submission Date
                                                                                                                             Notes. The figure shows the share of reviews classified as AI across different thresholds from 2021 through early 2026. The dashed vertical line
                                                                                                                             marks the launch of ChatGPT in November 2022.


                                                                                                                             submitted to Organization Science following the launch                                                         writing quality measures, as shown in Figure 11.
                                                                                                                             of ChatGPT.                                                                                                    Reviews that use AI are harder to read, with more
                                                                                                                                Similarly, we find a concerning pattern of degrada­                                                         complex word choice, more nominalization, and more
                                                                                                                             tion in the written reviews across nearly all of our                                                           jargon.

                                                                                                                             Figure 10. Trends in Flesch Reading Ease (Reviews) from 2013 to February 2026 with Markers for COVID-19 and the Launch of
                                                                                                                             ChatGPT

                                                                                                                                                                                    1
                                                                                                                                                                                                                                                    COVID-19                  ChatGPT
                                                                                                                                                  Flesch Reading Ease (SD units)




                                                                                                                                                                                   .5




                                                                                                                                                                                    0




                                                                                                                                                                                   -.5




                                                                                                                                                                                   -1
                                                                                                                                                                                         3


                                                                                                                                                                                                14



                                                                                                                                                                                                      15



                                                                                                                                                                                                              6


                                                                                                                                                                                                                      17



                                                                                                                                                                                                                            18



                                                                                                                                                                                                                                       19



                                                                                                                                                                                                                                               20



                                                                                                                                                                                                                                                       21



                                                                                                                                                                                                                                                                  22



                                                                                                                                                                                                                                                                         23



                                                                                                                                                                                                                                                                                  24



                                                                                                                                                                                                                                                                                           25



                                                                                                                                                                                                                                                                                                  26
                                                                                                                                                                                        1




                                                                                                                                                                                                               1
                                                                                                                                                                                     20



                                                                                                                                                                                             20



                                                                                                                                                                                                     20



                                                                                                                                                                                                            20



                                                                                                                                                                                                                   20



                                                                                                                                                                                                                           20



                                                                                                                                                                                                                                    20



                                                                                                                                                                                                                                            20



                                                                                                                                                                                                                                                     20



                                                                                                                                                                                                                                                               20



                                                                                                                                                                                                                                                                       20



                                                                                                                                                                                                                                                                                 20



                                                                                                                                                                                                                                                                                         20



                                                                                                                                                                                                                                                                                                 20




                                                                                                                                                                                                                           Review Submission Date

--- page 13 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             806                                                                                  Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             Figure 11. Association Between AI Use in Reviews and Review Writing Quality

                                                                                                                                                  Higher = Better Quality
                                                                                                                                                            Flesch Reading Ease

                                                                                                                                                                        Specificity
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                 Higher = Worse Quality
                                                                                                                                                                     Grade Level

                                                                                                                                                                        Fog Index

                                                                                                                                                                     SMOG Index

                                                                                                                                                                   Nominalization

                                                                                                                                                                    Passive Voice

                                                                                                                                                                           Jargon

                                                                                                                                                                          Hedging

                                                                                                                                                                                        -3              -2          -1             0              1              2
                                                                                                                                                                                                             Effect of AI Score (SD units)

                                                                                                                             Notes. The figure displays regression coefficients from a model predicting a standardized writing quality index as a function of AI use category indica­
                                                                                                                             tors, with quarter and editor fixed effects. Online Appendix A4 contains the definitions of each measure and descriptions of how they are calculated.

                                                                                                                               Overall, these trends suggest that the growth of AI                           theory, contribution, clarity of the argument and writ­
                                                                                                                             reviews will make it harder for both editors and                                ing, data, and empirics. In Table 5, we regress each
                                                                                                                             authors to act upon reviewer feedback. This increases                           topic’s relative share of attention in a review as a func­
                                                                                                                             the work of editors, who now have to spend more                                 tion of that review’s AI score. These models also
                                                                                                                             time understanding reviews, and of authors, who                                 include fixed effects for the manuscript. This allows us
                                                                                                                             must interpret and respond to reviewers’ requests                               to compare two reviews for the same manuscript while
                                                                                                                             and recommendations.                                                            holding constant differences in the nature and content
                                                                                                                                                                                                             of a specific research paper. Furthermore, we include
                                                                                                                             4.2. AI Use and Topics Raised in Reviews                                        reviewer fixed effects. Different reviewers may empha­
                                                                                                                             A decline in writing quality is only one dimension                              size different aspects of the manuscript, potentially bias­
                                                                                                                             where AI might affect the review process. Reviews                               ing the relationship between topic emphasis and AI
                                                                                                                             also provide authors with feedback on specific aspects                          score. This specification gives us an ideal basis for com­
                                                                                                                             of their manuscripts that are weak or need further                              parison, as we can partial out both of these factors. We
                                                                                                                             development. Reviewers often focus on five areas:                               find strong shifts in emphasis even with these fixed

                                                                                                                             Table 5. Are AI Reviews Different than Human Reviews? (Reviewer Fixed Effects)

                                                                                                                                                       (1)               (2)                    (3)                (4)             (5)                   (6)                 (7)
                                                                                                                                                     Theory          Contribution             Clarity             Data           Empirics             Readability         Word Count

                                                                                                                             AI Score                0.251**             0.127                �0.016            �0.279**          �0.102              �2.388***               26.623
                                                                                                                                                     (0.106)            (0.116)               (0.104)            (0.109)          (0.108)              (0.111)               (48.236)
                                                                                                                             Constant                 0.005            �0.023***             �0.021***          0.050***          �0.014*              0.108***            1119.770***
                                                                                                                                                     (0.008)            (0.008)               (0.007)            (0.008)          (0.008)              (0.008)                (3.511)
                                                                                                                             Observations             7,208              7,208                 7,208             7,208              7,208                7,570                7,570
                                                                                                                             R2                       0.743              0.727                 0.741             0.741              0.737                0.839                0.806
                                                                                                                             Manuscript FE             Yes                Yes                   Yes               Yes                Yes                  Yes                  Yes
                                                                                                                             Reviewer FE               Yes                Yes                   Yes               Yes                Yes                  Yes                  Yes
                                                                                                                             Notes. Standard errors in parentheses. Cols 1–5: DV is topic share normalized to SD from pre-ChatGPT mean. Col 6: Flesch Reading Ease
                                                                                                                             (standardized, mean 0, SD 1; higher � more readable). Col 7: Review word count. Standard errors clustered at the manuscript level.
                                                                                                                                *p < 0:10; **p < 0:05; ***p < 0:01.

--- page 14 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                                              807

                                                                                                                             Figure 12. Are AI Reviews Different from Human Reviews?
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             Notes. This represents a narrowing of the types of topics these reviews cover. Each data point represents one review. The x-axis plots the first principal
                                                                                                                             component and the y-axis plots the second principal component. See text for description of how the principal component analysis was conducted.


                                                                                                                             effects. AI use biases reviews toward a “theory” focus                         five review topic categories and then plot each review as
                                                                                                                             and away from a “data” focus. Moreover, AI-generated                           a point on the graph. The x-axis shows a point’s location
                                                                                                                             reviews are of lower writing quality, even after control­                      on the PC1 axis representing the Data/Empirics versus
                                                                                                                             ling for differences among reviewers. AI is substantively                      Theory distinction. Points to the right represent reviews
                                                                                                                             changing the content of the reviews, shifting the focus of                     with a greater emphasis on Theory, whereas points
                                                                                                                             editors and authors, and potentially affecting manuscript                      to the left represent reviews with a greater emphasis on
                                                                                                                             quality as papers are revised in response to these nar­                        Data/Empirics. The y-axis, PC2, represents the Theory/
                                                                                                                             rower concerns.                                                                Data (substance) versus Clarity/Contribution (presenta­
                                                                                                                                Finally, Figure 12 provides a visual depiction of this                      tion) axis. Reviews higher on the y-axis focus more on
                                                                                                                             narrowing of review reports. To produce this figure, we                        presentation; lower on substance.
                                                                                                                             conduct Principal Component Analysis (PCA) on our                                 The plus signs (orange) are reviews with 0% AI
                                                                                                                                                                                                            detected after the launch of ChatGPT; the dots (teal)
                                                                                                                             Table 6. Do AI Reviews Increase the Likelihood That a                          ones are 70%+ AI reviews during this same period.
                                                                                                                             Paper Is Rejected?                                                             Each ellipse encompasses the 95% boundary for each
                                                                                                                                                                                                            review type. When AI is used for reviews, these
                                                                                                                                                                 (1)              (2)             (3)
                                                                                                                                                                Reject           Reject          Reject     reviews cover a narrower evaluative range. That is,
                                                                                                                                                                                                            review diversity systematically decreases. The results
                                                                                                                             Mean Review AI Score               0.033            0.037           0.046
                                                                                                                                                                                                            are exactly the same if we limit the number of 0% AI
                                                                                                                                                               (0.061)          (0.061)         (0.065)
                                                                                                                             Manuscript AI Score               0.109***         0.103***        0.113***    reviews to a random n � 118, as can be seen in Online
                                                                                                                                                               (0.027)          (0.024)         (0.035)     Appendix Figure A1.
                                                                                                                             Constant                          0.746***         0.746***        0.744***
                                                                                                                                                               (0.004)          (0.003)         (0.002)
                                                                                                                                                                                                            4.3. AI Reviews and Editorial Decisions
                                                                                                                             Observations                       3,470            3,469            3,461     We next test whether AI reviews are systematically
                                                                                                                             R2                                 0.061            0.067            0.120
                                                                                                                             EIC FE                                               Yes              Yes
                                                                                                                                                                                                            shifting editorial decision-making. In Table 6, we find
                                                                                                                             Senior Editor FE                                                      Yes      little evidence that having AI-supported reviews is
                                                                                                                                                                                                            affecting the decision to reject a manuscript or move it
                                                                                                                             Notes. Standard errors in parentheses. All models include quarter FE
                                                                                                                             and clustered SE. Sample: Non-desk-rejected submissions only.                  forward in the process. It is very likely that editors are
                                                                                                                               *p < 0:10; **p < 0:05; ***p < 0:01.                                          ignoring these reviews and substituting them with

--- page 15 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             808                                                                                                                     Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             Figure 13. Trends in AI Usage Among Articles Published in                                                           active editorial load (for SEs)—even though our sub­
                                                                                                                             Organization Science                                                                                                mission volume has increased by over 40%. A much
                                                                                                                                                                                                                                                 larger number of DEs are handling a growing number
                                                                                                                                                             30




                                                                                                                                                                               Total
                                                                                                                                                                               0-15% AI
                                                                                                                                                                                                   ChatGPT
                                                                                                                                                                                                                                                 of submissions that need to be desk-rejected, with some
                                                                                                                                                                               15%-30% AI                                                        DEs having annual loads of over 250 manuscripts.10
                                                                                                                                                             25




                                                                                                                                                                               30%-70% AI
                                                                                                                              Number of Published Articles




                                                                                                                                                                               70%+ AI
                                                                                                                                                                                                                                                 4.4. What Appears in Press?
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                                                             20




                                                                                                                                                                                                                                                 While it is too early to tell how the recent rise in AI sub­
                                                                                                                                                                                                                                                 missions will translate into publications, we examined
                                                                                                                                                             15




                                                                                                                                                                                                                                                 how many of Organization Science’s eventual publica­
                                                                                                                                                                                                                                                 tions contain detectable levels of AI. We downloaded
                                                                                                                                                             10




                                                                                                                                                                                                                                                 all Organization Science publications in the OpenAlex
                                                                                                                                                                                                                                                 database and scored these using Pangram. These results
                                                                                                                                                             5




                                                                                                                                                                                                                                                 are presented in Figure 13. The vast majority of pub­
                                                                                                                                                                                                                                                 lished papers are human-generated (<15% AI score),
                                                                                                                                                             0




                                                                                                                                                                  2021           2022             2023           2024        2025         2026   with a few showing AI collaboration (15%–30% score)
                                                                                                                                                                                                    Publication Date
                                                                                                                                                                                                                                                 in the writing of the abstract. This is reassuring, but it
                                                                                                                             Notes. Each line shows the share of published article abstracts classi­                                             also suggests that the editorial process puts consider­
                                                                                                                             fied as 0%–15% AI, 15%–30%, 30%–70%, 70%+. The dashed vertical                                                      able effort into weeding out low-quality papers, many
                                                                                                                             line marks the launch of ChatGPT in November 2022.
                                                                                                                                                                                                                                                 of which rely heavily on AI.
                                                                                                                                                                                                                                                    Finally, in Figure 14, we tracked the outcomes of
                                                                                                                             their own judgment or relying more on the comments                                                                  manuscripts rejected at Organization Science. The vast
                                                                                                                             of the other, human, reviewers.9 Human expert judg­                                                                 majority of these papers could not be found on pre­
                                                                                                                             ment is still limiting any adverse effects of AI on what                                                            print servers, in proceedings, or in other academic
                                                                                                                             we publish, but is doing so at the cost of increased                                                                journals, likely because many of the rejected articles
                                                                                                                             effort. Figure A8 shows the average number of Deputy                                                                are still under review elsewhere. However, the pattern
                                                                                                                             Editors, Senior Editors, and Reviewers handling manu­                                                               of results among those we were able to track is infor­
                                                                                                                             scripts over time from 2021 to 2026. To address the                                                                 mative. Manuscripts with very low AI scores
                                                                                                                             growing volume of submissions, the journal increased                                                                (0%–15%) were most likely to be published in any
                                                                                                                             the number of Deputy editors from six to eleven.                                                                    journal (many of which are well-respected journals),
                                                                                                                             The number of active senior editors has also increased                                                              and some were published in the very best journals in
                                                                                                                             from approximately 30 in the preperiod to 60 in the
                                                                                                                                                                                                                                                 our field. Publication rates are substantially lower for
                                                                                                                             postperiod. This large jump in effort by volunteer edi­
                                                                                                                                                                                                                                                 articles with AI scores between 15% and 70%. What is
                                                                                                                             tors has allowed Organization Science to maintain (for
                                                                                                                                                                                                                                                 surprising is that, while no articles with an AI score of
                                                                                                                             DEs and reviewers) or, in some cases, decrease the
                                                                                                                                                                                                                                                 70% were eventually found in “top” or otherwise
                                                                                                                                                                                                                                                 selective journals, these manuscripts are the most
                                                                                                                             Figure 14. Distribution of Publication Outcomes for Articles                                                        likely to appear in print at any journal, at a rate of
                                                                                                                             Rejected at Organization Science, by AI Score                                                                       1.9% (versus 0.8% of papers with an AI score of <15%
                                                                                                                                                                                                                                                 AI. This pattern suggests that heavily AI papers can
                                                                                                                                                             140
                                                                                                                                                                               Any Journal                      FT50/UTD24                       find publication homes at peer-reviewed outlets.
                                                                                                                                                                               Preprints/Proceedings
                                                                                                                                                             120
                                                                                                                                                                                                                                                 5. What Comes Next?
                                                                                                                                                             100                                                                                 Our evidence shows how AI-based writing is flooding
                                                                                                                             Number of Manuscripts




                                                                                                                                                                                                                                                 Organization Science with a high volume of low-
                                                                                                                                                              80
                                                                                                                                                                                                                                                 quality papers. Institutional incentives—particularly
                                                                                                                                                              60
                                                                                                                                                                                                                                                 when careers depend on publication counts in specific
                                                                                                                                                                                                                                                 journal lists—appear to be accelerating this trend.
                                                                                                                                                              40                                                                                 This surge has strained the volunteer labor that evalu­
                                                                                                                                                                                                                                                 ates research, which might partly explain the high
                                                                                                                                                              20                                                                                 percentage of reviews with AI-generated signatures
                                                                                                                                                                                                                                                 we observe. Like AI-generated manuscripts, these AI
                                                                                                                                                                  0
                                                                                                                                                                         0-15% AI            15-30% AI          30-70% AI           70%+ AI      reviews are less well-written and narrower in scope.
                                                                                                                                                                         (N=4180)             (N=702)            (N=639)            (N=412)      In short, AI is placing the peer-review system under
                                                                                                                             Note. Preprint servers and Proceedings include SSRN, arXiv, as well                                                 stress that shows no signs of decreasing. Although
                                                                                                                             as the Academy of Management Proceedings.                                                                           ours is the first comprehensive study of a journal’s

--- page 16 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                           809

                                                                                                                             full submissions corpus, it is hard to imagine that                       prose can compensate for actual time spent working
                                                                                                                             Organization Science is alone in this regard. Our conver­                 on the manuscript. The second may be what Shaw
                                                                                                                             sations with editors at other journals reveal anecdotal                   and Nave (2026) term “cognitive surrender,” the ten­
                                                                                                                             accounts of these same patterns; these are simply the                     dency to adopt AI outputs with minimal scrutiny,
                                                                                                                             first data to confirm them.                                               bypassing the deliberative reasoning that careful aca­
                                                                                                                                Importantly, our findings temper some of the opti­                     demic writing demands.13
                                                                                                                             mistic predictions about how AI changes academic                             These mechanisms have different implications. For
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             research by showing:                                                      those tempted by the strategic approach, the data are
                                                                                                                                • AI is not improving writing quality in aggregate.                    clear: heavily AI-generated submissions are usually
                                                                                                                             Our evidence suggests that the written quality of manu­                   rejected. And for all of us, it is critical to evaluate when
                                                                                                                             scripts and reviews is in decline. This is not to say that                engaging with AI sharpens thinking and when it
                                                                                                                             AI cannot improve writing quality, but so far, the                        replaces it.
                                                                                                                             systems-level effects have been negative.
                                                                                                                                • AI is not leveling the playing field. All non-Native                 5.2. Toward a Better Equilibrium
                                                                                                                             English Institution author teams and new field entrants                   These individual choices matter, but they alone will
                                                                                                                             who expect AI to strengthen writing receive little bene­                  not resolve the systemic pressures driving AI adop­
                                                                                                                             fit in terms of increased publication likelihood.                         tion. Steering toward a “better” versus “more” equi­
                                                                                                                                • AI reviews are not equivalent to (or better than)                    librium requires institutional change.
                                                                                                                             human reviews. They are less well-written and nar­                           Moving toward a “better” equilibrium requires
                                                                                                                             rower in systematic ways.                                                 reframing of AI’s role in academic research. Most
                                                                                                                                • AI adoption is not a purely technical phenomenon                     authors and reviewers are using AI to compress time,
                                                                                                                             or institutionally agnostic. Instead, it appears to be cor­               perhaps unaware of the degradation in quality. A
                                                                                                                             related with career incentives that pressure researchers                  paper can now be written in days, not weeks or
                                                                                                                             to increase their publication output.                                     months. Reviews can be submitted in minutes instead
                                                                                                                                                                                                       of hours. The same dynamic extends to empirical
                                                                                                                                                                                                       analysis, where AI-guided coding accelerates data
                                                                                                                             5.1. Does AI Use Necessarily Make
                                                                                                                                                                                                       cleaning and estimation but may erode the nuance
                                                                                                                                   Writing Worse?
                                                                                                                                                                                                       and judgment that careful empirical work demands.
                                                                                                                             Before considering how institutions might respond, we
                                                                                                                                                                                                       Future AI models may reduce this concern, but our
                                                                                                                             should clarify our position on the deterioration in writ­
                                                                                                                                                                                                       analysis shows the importance of measuring this pro­
                                                                                                                             ing quality.11 We do not see the deterioration in writing                 gress rather than assuming it. The writing quality
                                                                                                                             quality that we document as an inevitable consequence                     needed to publish in strong journals such as Organiza­
                                                                                                                             of AI use. The worst outcomes likely reflect how                          tion Science is currently beyond what Dell’Acqua et al.
                                                                                                                             authors and reviewers use the tools today—as a substi­                    (2026) call “the jagged frontier” of even the latest AI.
                                                                                                                             tute for their writing and human editing rather than a                    Tracking this frontier is essential, both to address the
                                                                                                                             complement.                                                               apparent overconfidence scholars display in their
                                                                                                                                Indeed, we used AI in preparing this essay. On the                     AI-generated content (Leonardi and Leavell 2026)
                                                                                                                             back end, it helped write the code to generate the                        and to guard against applying algorithmic tools with­
                                                                                                                             figures and tables. In writing, we used AI to help us                     out understanding how or how well they work
                                                                                                                             outline sections, find better phrasing, and compare our                   (Anthony 2021).
                                                                                                                             essay to prior research, among various other uses. The                       We also recognize that while we measure one dimen­
                                                                                                                             manual revisions and copyediting by our author team                       sion of research outcome quality, many elements of pro­
                                                                                                                             and other human readers, however, were extensive.                         cess quality remain important for research progress but
                                                                                                                                Even with considerable AI use in its production,                       are not directly observable in our data. Many scholars
                                                                                                                             this editorial received a Pangram score of 8.8%.12 It                     consider research to be a craft: a lifelong practice of
                                                                                                                             was classified as “100% Human” by both Pangram                            learning to engage the world, interacting with other
                                                                                                                             and our own 15% or 30% cut-offs for human-first                           scholars, reading deeply, and refining our cognitive
                                                                                                                             papers. Given our own use of AI, it has forced us to                      schemas through the work itself (Bechky and Davis
                                                                                                                             reflect on what higher scores, for instance 30% or                        2025). This craft develops through the struggle of doing,
                                                                                                                             more, say about a manuscript’s production. Submitted                      whether that means iterating on an empirical strategy,
                                                                                                                             manuscripts with scores below 30% receive editorial                       immersing in a field site, or wrestling a theory into
                                                                                                                             outcomes that are indistinguishable from those with a                     coherent form. If researchers systematically delegate
                                                                                                                             score near 0%. Above it, outcomes deteriorate.                            these processes to AI, we risk eroding the very capaci­
                                                                                                                                At least two mechanisms may be driving this. The                       ties that enable us to recognize meaningful empirical
                                                                                                                             first is strategic: authors with weaker manuscripts                       puzzles, draw novel connections, and generate collec­
                                                                                                                             may turn to AI as a last resort, hoping that polished                     tive knowledge at the frontier.

--- page 17 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             810                                                               Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             5.3. Peer Review: Potential Scenarios                         ingenuity and the evolving capabilities of AI models.
                                                                                                                             The institution of peer review is younger than we             But we see three general categories of work emerging.
                                                                                                                             generally assume. Although informal refereeing dates             The first is our ability to apply better methods to
                                                                                                                             back centuries, the modern system of anonymous peer           existing questions. This includes using AI in creative
                                                                                                                             review did not become standard until well into the sec­       and new ways to tackle critical questions in our field
                                                                                                                             ond half of the twentieth century. Nature did not require     for which we historically had limited tools or data. In
                                                                                                                             external peer review for all submitted articles until 1973;   this way, AI is like the many historical and emerging
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             The Lancet followed in 1976. The system that emerged          technologies and data sources we’ve already incorpo­
                                                                                                                             was built on a specific social contract: anonymous            rated into our research. AI could help us better ana­
                                                                                                                             volunteers would donate their expertise for the good of       lyze large-scale text, video, audio, and images at a
                                                                                                                             the field, in exchange for the trust that their judgments     scale previously infeasible.
                                                                                                                             would shape what counted as legitimate science.                  The second is to use AI to identify new and impor­
                                                                                                                                That system has evolved several times, from edito­         tant questions that were not visible because they existed
                                                                                                                             rial discretion to formal refereeing to the institutional­    in the gaps between research fields. AI, with its ability
                                                                                                                             ized peer review we recognize today, and it will              to find connections in seemingly disparate domains and
                                                                                                                             surely evolve again—the question is toward what.              fields—across data forms such as images and text and
                                                                                                                             Whether we get to better or stay on a trajectory toward       across languages—may reveal those gaps in theory
                                                                                                                             more is not clear. We present three possible scenarios        and evidence more readily than any human would. The
                                                                                                                             for how the system may evolve, based on what we               potential for AI to bridge knowledge silos is particularly
                                                                                                                             observe today.                                                exciting for our diverse field (Dell’Acqua et al. 2026).
                                                                                                                                In scenario one, our findings could represent a tran­      Humans may continue to hold the key to answering
                                                                                                                             sitory phase. AI-generated papers are faring poorly in        these questions, possibly with conventional methods; it
                                                                                                                             the review process, and it is very likely that, as detec­     could be the machine’s ability to span vast amounts of
                                                                                                                             tion improves, even more of this type of work will be         knowledge that creates the opportunity.
                                                                                                                             filtered out of the system. But if the deeper cause is           Finally, the most ambitious category consists of
                                                                                                                             strategic institutional behavior and the incentives are       both new questions and new methods. As researchers
                                                                                                                             deeply ingrained, we may be facing more of the same           experiment with AI, they will discover things that are
                                                                                                                             for some time.                                                unfamiliar and imperfect by conventional standards.
                                                                                                                                Scenario two is a further erosion of the field as the      While these efforts are risky and time-consuming,
                                                                                                                             trends we report here continue. Volume will eventually        they can also change the field.
                                                                                                                             overwhelm the best reviewers and editors, who will
                                                                                                                             understandably withdraw from increasingly exhaust­            5.4.1. Making the System Sustainable and the Research
                                                                                                                             ing volunteer work. This might leave AI review agents         Stronger. The most immediate operational challenge is
                                                                                                                             evaluating authors’ AI-generated submissions, hollow­         the rise in volume. Our evidence implies that the sharp
                                                                                                                             ing out the shared intellectual community we know             rise in submission rates at Organization Science since late
                                                                                                                             advances science. This may be the most likely path if         2022 was driven by AI. If this trajectory continues, the
                                                                                                                             conservative academic journals and universities fail to       volunteer-based review system will be unable to keep
                                                                                                                             address this potential outcome.                               pace. This poses an important organizational design
                                                                                                                                A scenario three also exists, however, in which            challenge (Hasan et al. 2025). Journals need tools and
                                                                                                                             institutional changes and technological improvements          policies that maintain volume at sustainable levels or
                                                                                                                             in artificial intelligence lead to a “better” equilibrium     facilitate low-cost rejections of low-quality AI-driven
                                                                                                                             where AI enables better research questions, theory, and       research. We emphasize that the goal is not to screen
                                                                                                                             data analysis. Rather than evolving inevitably, this bet­     out research enabled by AI, since our objective is to
                                                                                                                             ter equilibrium entails deliberate choices that extend        refine and promote great research on organizations.
                                                                                                                             well beyond journals. It is the hardest path and the one      Artificial intelligence provides powerful tools for con­
                                                                                                                             most worth steering toward. That steering requires            ducting research, many of which we as authors use to
                                                                                                                             changing what the two institutions that most shape            support our own work. Our data show that AI use in
                                                                                                                             scholarly incentives—journals and universities—               aggregate is not currently producing high-quality writ­
                                                                                                                             choose to reward.                                             ing, but that does not mean it cannot in the right hands
                                                                                                                                                                                           or with further advances in technology.
                                                                                                                             5.4. What Does Better Look Like?                                 AI detection tools such as Pangram can also play a
                                                                                                                             Before considering how institutions should adjust             role here, used as additional flags that help editors
                                                                                                                             what they reward, it is important to consider what            understand how a manuscript was produced and
                                                                                                                             “better” research may look like. It is hard to predict        evaluate it in context. We do not advocate for detec­
                                                                                                                             exactly how better research in collaboration with AI          tion as a gatekeeper—automated desk-reject decisions
                                                                                                                             will evolve. This will depend heavily on researchers’         based on AI scores would be premature and invite

--- page 18 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS                                                            811

                                                                                                                             gaming behavior—and we are uncomfortable making                           the aspiration, it is now a necessity. Many schools balk
                                                                                                                             normative assessments about appropriate levels of AI                      at more subjective evaluations because of legitimate
                                                                                                                             in submissions. But detection data can inform editorial                   equity concerns and legal risks, but rewarding “A”
                                                                                                                             triage, flagging submissions that warrant closer scrutiny                 (count) while hoping for “B” (quality) will only become
                                                                                                                             before reviewers are asked to invest their time. It will be               a bigger problem as the costs of “A” continue to fall.
                                                                                                                             crucial for studies like ours to be frequently repeated as                   Leadership at the department, school, and univer­
                                                                                                                             technology advances and researchers’ behaviors adapt.                     sity levels must also create the conditions for these
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             The AI-driven writing we are detecting through Pan­                       shifts to take hold through the recruitment and hiring
                                                                                                                             gram in March 2026 sends a strong signal of lower                         process. If the hiring process continues to elevate pub­
                                                                                                                             quality, but that signal is noisy and may change if                       lication counts and journal rankings as the currency of
                                                                                                                             leading-edge models advance their writing skills.                         academic success, committees will optimize accord­
                                                                                                                                Journals should also consider whether appropri­                        ingly, regardless of what any editorial or task force
                                                                                                                             ately designed submission fees can help internalize                       recommends. Increased expectations that doctoral stu­
                                                                                                                             the costs that high-volume submitters impose on the                       dents have top publications when first entering the job
                                                                                                                             review system. A nonlinear fee structure that escalates                   market set the wrong norm at the beginning of careers,
                                                                                                                             costs for authors with simultaneous submissions could                     particularly when the quality of solo-authored job
                                                                                                                             specifically target the volume incentive that AI-generated                market papers (and the signal they send) suffers. As
                                                                                                                             manuscripts exploit, while imposing minimal burden on                     we teach our students, during periods of systemic
                                                                                                                             authors submitting at typical rates. Such fees would need                 change, over-anchoring on hard metrics risks diverting
                                                                                                                             to incorporate equity considerations for those with lim­                  scholars from ambitious, frontier-expanding work to
                                                                                                                             ited resources, and we are also wary of taxing researchers                more derivative papers.
                                                                                                                             who are truly producing a volume of high-quality work.                       Given our evidence that AI-generated writing is
                                                                                                                             We raise these options as possibilities worth serious dis­                making papers worse, authors need to consider the
                                                                                                                             cussion, not as settled recommendations.                                  ethics of knowingly submitting more inferior papers
                                                                                                                                Reducing submission volume is necessary but insuf­                     rather than dedicating time to producing a single bet­
                                                                                                                             ficient if the research that does get published is not                    ter manuscript. There is a real human cost to evaluat­
                                                                                                                             improving. Editors and reviewers must explicitly signal                   ing the growing volume of low-quality papers.
                                                                                                                             that they are looking for work that pushes the frontier,
                                                                                                                             even when that work is messier or less immediately                        5.5. Conclusion
                                                                                                                             comparable to established approaches.                                     Our analysis of Organization Science shows that, at least
                                                                                                                                Universities. The imbalance between quantity and                       in our corner of the social and behavioral sciences, we
                                                                                                                             quality cannot be fully addressed by journals them­                       are heading toward a “more” rather than a “better”
                                                                                                                             selves if universities continue to primarily reward vol­                  equilibrium as we integrate AI into our field. However,
                                                                                                                             ume in career progression. Volume incentives                              as researchers whose own work has been reshaped by
                                                                                                                             originate not at the journals but at the universities                     AI over the past year, we also see the potential of
                                                                                                                             themselves, and even more so at those that reward                         a “better” equilibrium in which new, more difficult
                                                                                                                             simple publication counts and offer financial bonuses                     questions are asked, new methods are applied in imag­
                                                                                                                             for placement in designated “A” journals. While these                     inative ways, or both. We are encouraged by this
                                                                                                                             incentives have always been distortionary, the falling                    potential, but concerned about the field’s current trajec­
                                                                                                                             cost of producing submissions will exacerbate the                         tory. Whether our field evolves toward “more” or
                                                                                                                             problem. At a minimum, institutions should be trans­                      “better” is an institutional question, and will require us
                                                                                                                             parent about these incentive structures. Disclosure of                    to adapt the incentives and culture that have allowed
                                                                                                                             publication bonuses and explicit journal-list-based                       academics to thrive to this point.
                                                                                                                             rewards would allow the field to see the scope of the
                                                                                                                             problem and begin to design responses.                                    Acknowledgments
                                                                                                                                This requires institutional changes at each major                      Author names are in alphabetical order. All authors con­
                                                                                                                             stage of the academic career ladder. Tenure and promo­                    tributed equally to the letter. Gartenberg and Murray are
                                                                                                                             tion decisions carry the highest stakes and demand the                    Senior Editors, Hasan is a Deputy Editor, and Pierce is
                                                                                                                             most significant shift. At a minimum, existing norms                      Editor-in-Chief of Organization Science. Hasan served as
                                                                                                                                                                                                       Chair of the journal’s AI Task Force. The authors grate­
                                                                                                                             and rules regarding the exact count of publications
                                                                                                                                                                                                       fully acknowledge support from the Wharton School at
                                                                                                                             required to define someone as sufficiently “productive”
                                                                                                                                                                                                       the University of Pennsylvania and the Fuqua School of
                                                                                                                             will be outdated; the more fundamental change will                        Business at Duke University that enabled this analysis.
                                                                                                                             require rewarding exceptional quality over quantity.                      The authors also thank Pangram for providing research
                                                                                                                             Committees must do the hard work of actually reading                      credits and technical support during this effort. The article
                                                                                                                             papers and assessing intellectual contribution rather                     benefited from the comments of Seth Carnahan, Scott Dyreng,
                                                                                                                             than counting publications. While this has always been                    Frank Levy, Andrew Nelson, Oren Reshef, Christopher Tang,

--- page 19 ---

Gartenberg et al.: AI and Peer Review
                                                                                                                             812                                                                          Organization Science, 2026, vol. 37, no. 3, pp. 795–812, © 2026 INFORMS


                                                                                                                             Shirley Tang, and Matthew Walls. This project was submitted             proposed a range of alternative explanations. For instance: The mea­
                                                                                                                             to the Duke University Institutional Review Board (IRB) for             sures we use are poor proxies for writing quality; poor writing
                                                                                                                             review, which ruled that it does not constitute human subjects          reflects on the authors, not the AI; AI improves writing for non-
                                                                                                                                                                                                     Native speakers but not others; and so on. What is clear is that all tra­
                                                                                                                             research, as it is intended for institutional improvement.
                                                                                                                                                                                                     ditional writing quality metrics show a significant decline with the
                                                                                                                             INFORMS legal counsel verified that the authors fully com­
                                                                                                                                                                                                     use of AI. This appears to bump up against a very strong prior in
                                                                                                                             plied with the INFORMS Privacy Policy. AI was used in the               our field that AI improves writing quality. This is a mismatch
                                                                                                                             following ways: Claude Code helped write Python scripts to              between priors and data worth exploring further, but it may be out­
Downloaded from informs.org by [185.104.138.146] on 24 August 2026, at 08:19 . For personal use only, all rights reserved.




                                                                                                                             merge data, calculate readability metrics, send batches to Pan­         side the scope of this article.
                                                                                                                             gram, and parse manuscripts into sections. Claude Code also             12
                                                                                                                                                                                                        Much of this high score is driven by the AI-generated writeup of
                                                                                                                             helped write the Stata code for the analysis, particularly the          definitions of the writing quality scores, which described the calcu­
                                                                                                                             figures. All code was reviewed by the authors before finalizing         lations made by the Python code.
                                                                                                                             the analyses in the paper. Finally, the authors used Claude.AI          13
                                                                                                                                                                                                        Their experimental evidence shows that AI use inflates authors’
                                                                                                                             to outline the discussion section and smooth out awkward                confidence regardless of actual quality. This is particularly concern­
                                                                                                                             phrasing. Grammarly was used for limited copyediting. All               ing in an academic context, where the iterative struggle of writing is
                                                                                                                             errors belong to the authors.                                           itself a form of thinking. When authors cede that process to AI, they
                                                                                                                                                                                                     may not realize that the resulting text, while fluent, lacks coherence
                                                                                                                                                                                                     and depth. This dynamic may be what we are capturing in manu­
                                                                                                                             Endnotes
                                                                                                                                                                                                     scripts and reviews with Pangram scores above 30%.
                                                                                                                             1
                                                                                                                              We report only highly aggregated results in accordance with
                                                                                                                             INFORMS data confidentiality and privacy policies.
                                                                                                                             2
                                                                                                                               The ScholarOne database in which these are stored does not allow      References
                                                                                                                             for automated downloads of the nearly 20,000 PDF documents nec­         Anthony C (2021) When knowledge work and analytical technolo­
                                                                                                                             essary to evaluate all full-texts and reviews. In addition, the token        gies collide: The practices and consequences of black boxing
                                                                                                                             usage for such a task would require an additional budget of $10,000.         algorithmic technologies. Admin. Sci. Quart. 66(4):1173–1212.
                                                                                                                             3
                                                                                                                              Complete descriptive statistics for the analysis sample are in         Bechky BA, Davis GF (2025) Resisting the algorithmic management
                                                                                                                             Online Appendix A1.                                                          of science: Craft and community after generative AI. Admin.
                                                                                                                             4                                                                            Sci. Quart. 70(1):1–22.
                                                                                                                               See https://www.pangram.com/research/model-card/pangram-
                                                                                                                                                                                                     Dell’Acqua F, Ayoubi C, Lifshitz H, Sadun R, Mollick E, Mollick L,
                                                                                                                             3-1.
                                                                                                                                                                                                          Han Y, et al. (2026) The cybernetic teammate: A field experi­
                                                                                                                             5
                                                                                                                               Some prior research (Liang et al. 2025) suggests that AI detection         ment on generative AI and teamwork. Organ. Sci. Forthcoming.
                                                                                                                             algorithms mis-classify text written by non-native English speakers     Dell’Acqua F, McFowland E III, Mollick E, Lifshitz H, Kellogg KC,
                                                                                                                             at higher rates. We find little evidence of this in a supplementary          Rajendran S, Krayer L, Candelon F, Lakhani KR (2026) Navigat­
                                                                                                                             test in Online Appendix A2. Pre-ChatGPT texts are almost uni­                ing the jagged technological frontier: Field experimental evidence
                                                                                                                             formly classified as “low AI” regardless of author origin, barring           of the effects of artificial intelligence on knowledge worker pro­
                                                                                                                             some small amount of model noise.                                            ductivity and quality. Organ. Sci. 37(2):403–423.
                                                                                                                             6
                                                                                                                               Figure A2 in the Online Appendix shows a histogram of topic dis­      Hasan S, Oettl A, Samila S (2025) From model design to organiza­
                                                                                                                             tributions for reviews flagged as low- versus high-AI usage.                 tional design: Complexity redistribution and trade-offs in gen­
                                                                                                                             7                                                                            erative AI. Preprint, submitted June 10, https://arxiv.org/abs/
                                                                                                                              Though one could interpret less hedging and more active writing
                                                                                                                                                                                                          2506.22440.
                                                                                                                             as overconfidence in the context of academic writing.
                                                                                                                                                                                                     Jabarian B, Imas A (2025) Artificial writing and automated detec­
                                                                                                                             8
                                                                                                                               This suggests that while AI use predicts desk rejection cross-             tion. NBER Working Paper No. 34223, National Bureau of Eco­
                                                                                                                             sectionally, this effect disappears with author fixed effects. These         nomic Research, Cambridge, MA.
                                                                                                                             two estimates are confounded. Authors who rely on AI may do so          Jones N (2026) Leading preprint server clamps down on AI slop.
                                                                                                                             to address problems with inherently lower-quality papers, making             Science 391(6784):432–433.
                                                                                                                             it impossible to distinguish the effect of AI use from that of an       Kusumegi K, Yang X, Ginsparg P, de Vaan M, Stuart T, Yin Y
                                                                                                                             author’s manuscript quality, or from potential bias in decisions             (2025) Scientific production in the era of large language models.
                                                                                                                             based on author identity. Nevertheless, the question of whether              Science 390(6779):1240–1243.
                                                                                                                             AI’s effect on rejection rates reflects the technology itself or the    Leonardi PM, Leavell V (2026) Knowing enough to be dangerous: The
                                                                                                                             types of authors who adopt it yields similar consequences for the            problem of “artificial certainty” for expert authority when using
                                                                                                                             journal: Organization Science is receiving too many AI submissions.          AI for decision making and planning. Organ. Sci. 37(2):516–543.
                                                                                                                             9
                                                                                                                               In further robustness tests, we found that the results remained       Liang W, Zhang Y, Wu Z, Lepp H, Ji W, Zhao X, Cao H, et al.
                                                                                                                             similar if we used an indicator for whether a manuscript received at         (2025) Quantifying large language model usage in scientific
                                                                                                                             least one 70%+ AI review. Thus, even the most AI-reliant reviews             papers. Nature Human Behav. 9:2599–2609.
                                                                                                                             do not appear to be meaningfully shifting editorial decisions.          Munger K, Bakker B, Berinsky A, Giger N, Guess A, Just N, Law­
                                                                                                                             10                                                                           rence R, Tenenboim-Weinblatt K, van de Rijt A (2026) Peer
                                                                                                                                While AI reduced the cost of writing manuscripts for the journal,         review 2027: Scenarios for academic publishing in the age of
                                                                                                                             the total cost of evaluating them has increased. This redistribution         AI. Preprint, submitted January 27, https://doi.org/10.31235/
                                                                                                                             of complexity problem, as argued by Hasan et al. (2025), is what             osf.io/594zj_v1.
                                                                                                                             many organizations implementing or contending with AI will have         Naddaf M (2025) Major AI conference flooded with peer reviews
                                                                                                                             to manage as AI shifts effort across tasks inside organizations.             written fully by AI. Nature 648(8093):256–257.
                                                                                                                             11
                                                                                                                               Interestingly, the issue of whether we are actually measuring         Shaw SD, Nave G (2026) Thinking-fast, slow, and artificial: How AI
                                                                                                                             “writing quality” came up in nearly all of the reviews we received in        is reshaping human reasoning and the rise of cognitive surren­
                                                                                                                             preparing this manuscript. Readers were surprised by the marked              der. Preprint, submitted January 11, https://doi.org/10.2139/
                                                                                                                             decline in writing quality scores after the launch of ChatGPT and            ssrn.6097646.
