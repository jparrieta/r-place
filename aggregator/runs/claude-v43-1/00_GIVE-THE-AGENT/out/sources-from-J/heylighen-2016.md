# Heylighen (2016), Stigmergy as a universal coordination mechanism I: Definition and components

Source: Heylighen, F. (2016). Cognitive Systems Research 38, 4-13. PDF supplied by J on 2026-10-15 (StigmergyICognSystems.pdf). Text extracted by pdftotext with layout kept; page breaks marked; journal pages 4 to 13. Quote with the journal page printed in the text, and check an odd word against the page.

--- pdf page 1 ---
                                              Available online at www.sciencedirect.com

                                                        ScienceDirect
                                                 Cognitive Systems Research 38 (2016) 4–13
                                                                                                                      www.elsevier.com/locate/cogsys




       Stigmergy as a universal coordination mechanism I: Deﬁnition
                              and components

                                                           Francis Heylighen
      Evolution, Complexity and Cognition Group, Center Leo Apostel, Vrije Universiteit Brussel, Krijgskundestraat 33, B-1160 Brussels, Belgium

                                                        Available online 11 December 2015




Abstract

   The concept of stigmergy has been used to analyze self-organizing activities in an ever-widening range of domains, including social
insects, robotics, web communities and human society. Yet, it is still poorly understood and as such its full power remains underappre-
ciated. The present paper clariﬁes the issue by deﬁning stigmergy as a mechanism of indirect coordination in which the trace left by an
action in a medium stimulates subsequent actions. It then analyses the fundamental concepts used in the deﬁnition: action, agent, med-
ium, trace and coordination. It clariﬁes how stigmergy enables complex, coordinated activity without any need for planning, control,
communication, simultaneous presence, or even mutual awareness. The resulting self-organization is driven by a combination of positive
and negative feedbacks, amplifying beneﬁcial developments while suppressing errors. Thus, stigmergy is applicable to a very broad vari-
ety of cases, from chemical reactions to bodily coordination and Internet-supported collaboration in Wikipedia.
Ó 2015 Elsevier B.V. All rights reserved.


Keywords: Stigmergy; Coordination; Actions; Agents; Self-organization; Feedback




1. Past, present and future of the ‘‘stigmergy’’ concept                        The insight came from Grassé’s observation of how ter-
                                                                             mites repair their nest. He noted that initially termites wan-
   The concept of stigmergy was proposed by the French                       der around more or less randomly, carrying mud and
entomologist Pierre-Paul Grassé (Grassé, 1959) to describe                 depositing it here or there. However, the deposits that are
a mechanism of coordination used by insects. The principle                   created in this haphazard way then stimulate the insects
is that work performed by an agent leaves a trace in the                     to add more mud in the same place. Thus, the small heaps
environment that stimulates the performance of subsequent                    quickly grow into columns that eventually come together
work—by the same or other agents. This mediation via the                     to form an intricate cathedral of interlocking arches. The
environment ensures that tasks are executed in the right                     only communication between the termites is indirect: the
order, without any need for planning, control, or direct                     partially executed work of the ones provides information
interaction between the agents. The notion of stigmergy                      to the others about where to make their own contribution.
allowed Grassé to solve the ‘‘coordination paradox’’                           Another classic example of stigmergy can be found in
(Theraulaz & Bonabeau, 1999), i.e. the question of how                       the pheromone trails left by ants that come back from a
insects of very limited intelligence, without apparent com-                  food source (Sumpter & Beekman, 2003). The pheromone
munication, manage to collaboratively tackle complex pro-                    stimulates other ants to follow the same path. When they
jects, such as building a nest.                                              ﬁnd food, they too will reinforce the pheromone trail while
                                                                             following the trail back to the nest. This mechanism
                                                                             leads to the emergence of an eﬃcient network of trails
   E-mail address: fheyligh@vub.ac.be

http://dx.doi.org/10.1016/j.cogsys.2015.12.002
1389-0417/Ó 2015 Elsevier B.V. All rights reserved.
--- pdf page 2 ---
                                       F. Heylighen / Cognitive Systems Research 38 (2016) 4–13                                    5

connecting the nest via the shortest routes to all the major         of stigmergic self-organization is the ‘‘invisible hand’’ of
food sources.                                                        the market: the actions of buying and selling leave a trace
   Up to about 1990, the notion of stigmergy appears to              by aﬀecting the price of the transacted commodities. This
have remained limited to a small circle of researchers study-        price in turn stimulates further transactions. Via the related
ing the behavior of social insects. However, one of these            conceptions of distributed cognition and the extended
insect specialists, Jean-Louis Deneubourg, was also a mem-           mind, stigmergy has now also started to make its mark
ber of the ‘‘Brussels School’’ of complex systems, headed            on theories of cognition and epistemology (Marsh &
by the late Nobel Prize in chemistry, Ilya Prigogine. In this        Onof, 2008; Ricci, Omicini, Viroli, Gardelli, & Oliva,
interdisciplinary environment, it became clear that stig-            2006; Susi & Ziemke, 2001).
mergy was a prime example of spontaneous ordering or                     It is clear that since 1990, the concept of stigmergy has
self-organization (Camazine et al., 2003; Deneubourg,                undergone a rapid diﬀusion across an ever-growing num-
1977) and as such potentially applicable to complex sys-             ber of application domains. I contend in this paper that
tems other than insect societies.                                    the potential for theoretical explanation and practical
   With the advent of the agent-based paradigm in com-               application of the stigmergy concept is much larger still
puter simulation, insect societies were conceptualized as            than hitherto assumed. What (Parunak, 2006) noted about
swarms of simple agents that are able to perform complex             human institutions, that the more diﬃcult issue is to ﬁnd
tasks using various forms of self-organization and espe-             examples where stigmergy does not apply, extends to com-
cially stigmergy (Deneubourg, Theraulaz, & Beckers,                  plex systems in general. When properly deﬁned, the mech-
1992). The general ability to tackle complex problems                anism of stigmergy appears to be nearly ubiquitous and
exhibited by such self-organizing multi-agent collectives            able to illuminate a variety of conceptual problems in a
became known as swarm intelligence (Bonabeau, Dorigo,                non-trivial manner.
& Theraulaz, 1999; Kennedy, 2006). One class of stigmer-                 The matter of deﬁnition, however, is crucial to a proper
gic mechanisms in particular, so-called ant algorithms,              understanding and application. Deﬁnitions in the literature
turned out to be surprisingly powerful in tackling a variety         tend to be vague, restricted in scope and mutually incoher-
of computational problems, including the notorious travel-           ent (Dipple, Raymond, & Docherty, 2014; Shell & Mataric,
ing salesman problem (Dorigo, Bonabeau, & Theraulaz,                 2003). Misunderstandings have arisen particularly because
2000) and the optimization of packet routing along com-              of a confusion between the general notion of stigmergy and
munication networks (Kassabalidis, El-Sharkawi, Marks,               its speciﬁc instantiation in ant algorithms, i.e. the reinforce-
Arabshahi, & Gray, 2001).                                            ment with pheromones of frequently traveled paths by vir-
   Stigmergy was applied not only to software agents, but            tual ‘‘ants’’. The depositing of pheromone traces is an
to their hardware analogues: autonomous robots. Groups               example of what can be called quantitative, marker-based
of very primitive robots proved able to tackle non-trivial           stigmergy (Parunak, 2006). Stigmergy in the most general
tasks, such as clustering items in diﬀerent groupings, in a          sense does not require either markers or quantities.
way similar to ants (Beckers, Holland, & Deneubourg,                 Another, even more common misunderstanding is that
1994; Deneubourg et al., 1991; Holland & Melhuish,                   stigmergy only concerns groups or swarms consisting of
1999). These robotic implementations inspired the applica-           many agents. As we will show, stigmergy is just as impor-
tion of stigmergic models to problems of coordination and            tant for understanding the behavior of a single individual.
control in manufacturing (Valckenaers, Van Brussel,                  The present paper will clarify the meaning of stigmergy,
Kollingbaum, & Bochmann, 2006). After this expansion                 propose an unambiguous deﬁnition and summarize its ben-
of the stigmergy concept from social insects to the domains          eﬁts in explaining spontaneous forms of coordination.
of artiﬁcial life, artiﬁcial intelligence and behavior-based             Perhaps a last question to conclude this introductory
robotics, a perhaps obvious next step was computer-                  section: if stigmergy is so fundamental, ubiquitous and
supported collaboration between human agents, in particu-            explanatorily powerful, then why has it taken so long for
lar via the world-wide web (Bolici, Howison, & Crowston,             it to be recognized? The more obvious answer is that the
2009; Dron, Boyne, & Mitchell, 2001; Elliott, 2007;                  study of termites that gave rise to this conception is a very
Heylighen, 1999).                                                    speciﬁc discipline with no evident applications to other
   A prototypical example is Wikipedia, the free web ency-           sciences. Moreover, the deﬁning publication (Grassé,
clopedia which has grown to become the largest one in exis-          1959), appearing in French in a specialized journal, only
tence thanks to the fact that every reader is stimulated to          reached a limited audience. Its reach appears to have
improve and expand the writings of previous contributors             widened signiﬁcantly only after Deneubourg, a researcher
(Heylighen, 2007). A similar dynamics of contributions               active in both French and English and the domains of both
building further on previous contributions characterizes             social insects and self-organizing systems, started applying
open-source software development (Bolici et al., 2009;               the concept outside of its original context.
Robles, Merelo, & Gonzalez-Barahona, 2005). But it                       But why did not someone else come up with this simple
quickly became clear that human collaboration does not               and elegant notion? A more fundamental answer is that
need computer support to proﬁt from stigmergy (Elliott,              stigmergic interaction is by deﬁnition indirect, while our
2007; Parunak, 2006). Probably the best-known example                mind is biased to look for direct causes of the phenomena
--- pdf page 3 ---
6                                         F. Heylighen / Cognitive Systems Research 38 (2016) 4–13

we observe. If we note that agents act in a coordinated way,
our natural inclination is to seek the cause of one agent’s
behavior directly in another agent’s behavior, assuming
that there is an immediate communication from the one
to other. Failing to ﬁnd this link, we assume that the agents
are driven by the same cause, such as a shared instinct,
plan, or leader that controls their behavior. We do not
spontaneously consider the option that one agent may
drive another agent’s behavior only via the indirect route
of an unintentional trace left in a passive environment.
    This counter-intuitive aspect may explain why there is
still so much confusion surrounding the concept of stig-
mergy and why the breadth and power of its applications
                                                                                         Fig. 1. The stigmergic feedback loop.
have not yet been fully appreciated. I hope that the present
paper will help to truly clarify the mechanism and convince
researchers to further broaden their search for applications.
                                                                        3. Basic components of stigmergy
2. From etymology to definition
                                                                           Let us analyze the diﬀerent terms in this deﬁnition and
                                                                        from thereon the conceptual components necessary to
    The term ‘‘stigmergy’’ was derived by Grassé from the
                                                                        build a stigmergic process.
Greek roots, stigma, which means ‘‘mark or puncture’’
                                                                           Most primitive is the concept of action, which I interpret
(typically referring to the tattoo used to mark slaves) and
                                                                        as a causal process that produces a change in the state of
ergon which can mean ‘‘work, action, or the product of
                                                                        the world. Normally, we assume that an action is per-
work’’. Grassé motivated this derivation by interpreting
                                                                        formed by an agent, which is typically seen as an autono-
stigma as a goad, prod or spur, i.e. a stinging movement
                                                                        mous, goal-directed system. However, the concept of
(‘‘piqure’’ in the original French text) that incites activity.
                                                                        agent does not appear to be necessary for a deﬁnition of
Ergon is then the result of previous work responsible for
                                                                        stigmergy: the mechanism applies perfectly well to the
this stimulus or incitement. Thus, (Grassé, 1959) deﬁned
                                                                        coordination of actions performed by a single, unspeciﬁed
stigmergy as ‘‘the stimulation of workers by the very per-
                                                                        agent, in which case there is no need to identify diﬀerent
formances they have achieved’’ (from the original English
                                                                        agents. Moreover, further extensions of the stigmergy con-
abstract).
                                                                        cept can even do away with the notion of agent altogether
    However, in a more recent review paper, (Parunak,
                                                                        and consider the coordination of ‘‘agentless’’ actions that
2006) proposes a diﬀerent reading of the Greek etymology
                                                                        are merely events or physical processes—such as chemical
that is at least as compelling: if we interpret stigma as
                                                                        reactions (e.g. Tabony, 2006). This views ﬁts in with the
‘‘mark’’ or ‘‘sign’’ and ergon as ‘‘action’’, then stigmergy
                                                                        ontology of action (Heylighen, 2011; Turchin, 1993), which
is ‘‘the notion that an agent’s actions leave signs in the
                                                                        sees action as the primitive element from which all other
environment, signs that it and other agents sense and that
                                                                        concepts are derived. The concept of agent remains useful,
determine their subsequent actions’’. Summarizing, in
                                                                        though, in cases where we wish to distinguish diﬀerent
Grassé’s interpretation the product of work (ergon) func-
                                                                        agents able to perform diﬀerent actions.
tions as a stimulus (stigma) for action; in Parunak’s inter-
                                                                           As causal processes, actions have an antecedent or cause
pretation, action (ergon) leaves a mark (stigma). While
                                                                        and a consequent or eﬀect. In simple agent-based models
this double interpretation may seem to add to the confu-
                                                                        used in artiﬁcial intelligence the antecedent is usually called
sion, it actually provides an elegant illustration of the
                                                                        condition and the consequent simply action. The condition
bidirectional nature of stigmergy. The process described
                                                                        speciﬁes the state of the world in which the action occurs,
by both Grassé and Parunak is a feedback loop, where
                                                                        while the action speciﬁes the subsequent transformation
an action produces a mark which in turn incites an action,
                                                                        of that state. The causal relation is represented as a ‘‘pro-
which produces another mark and so on (see Fig. 1). In
                                                                        duction rule’’, which consists of the simple relation:
other words, actions stimulate their own continued execu-
tion via the intermediary of the marks they make—where
                                                                           condition ! action
a mark is a perceivable eﬀect, trace or product of an
action.
                                                                           It is to be read as:
    This brings me to my own deﬁnition:
    stigmergy is an indirect, mediated mechanism of coordina-              IF condition holds, THEN perform action
    tion between actions, in which the trace of an action left on
    a medium stimulates the performance of a subsequent                    For example, a thermostat obeys the production rule: IF
    action.                                                             the temperature is below the goal temperature, THEN
--- pdf page 4 ---
                                         F. Heylighen / Cognitive Systems Research 38 (2016) 4–13                                    7

switch on the heating (Heylighen & Joslyn, 2003). While                P ðactionjconditionÞ > P ðactionÞ;
this reading seems to imply an elementary cognitive process            where P(A) is the general probability of A occurring and P
of sensation or perception, to ascertain whether the condi-            (A|B) the conditional probability of A occurring given that
tion holds, the notation is equally applicable to agentless,           B is the case.
physical processes. For example, consider the following                    Note that in some cases, a condition may on the con-
chemical reaction:                                                     trary inhibit an action, i.e. make it less likely. For example,
NaOH þ HCl ! NaCl þ H2 O                                               the presence of a red light makes it less likely that someone
                                                                       would cross the street. In that case, we may still keep to the
   The ﬁrst part represents the necessary condition for the            deﬁnition of ‘‘stimulation’’ above, simply by considering
reaction to occur: an NaOH molecule and an HCl molecule                the opposite or negation of that condition as the stimulus:
must be simultaneously present. The second part of the                 e.g. the disappearance of a red light makes it more likely
reaction represents the product or result of the reaction:             that someone would cross the street.
the formation of an NaCl molecule together with an H2O                     We must now introduce another core component of stig-
molecule. More generally, we can write such reactions in               mergic activity, the medium. The medium is that part of the
the following form (where the ‘‘+’’ operators represents a             world that undergoes changes through the actions and
conjunction of the conditions or resources necessary for               whose states are sensed as conditions for further actions.
the process to take place):                                            The medium is a non-trivial entity, since many aspects of
a þ b þ  ! x þ y þ                                               the world are either not aﬀected by actions, or not perceiv-
                                                                       able as conditions for new actions. For example, while I
   Chemical Organization Theory (Dittrich & Fenizio,                   can clearly see the clouds in the sky, no matter how hard
2007) is a formal framework that shows how collections                 I try, I cannot change their position. Vice-versa, I have
of such simple reactions tend to become coordinated by                 the power to throw a rock in the sea, but I cannot see where
acting on a shared medium, the ‘‘reaction vessel’’, where              that rock will end up. In either case, there is no basis for a
they produce an evolving trace expressed by the concen-                stigmergic chain of actions triggering further actions. On
trations of the diﬀerent ‘‘molecules’’ (a, b, . . .). This coor-       the other hand, I can both perceive and aﬀect the arrange-
dinated pattern of activity deﬁnes an ‘‘organization’’: a              ment of sand on a beach and this allows me to build an
self-sustaining, dynamic network of interacting ‘‘mole-                intricate sand castle via a coordinated sequence of condi-
cules’’. While the inspiration for this model comes from               tion ! action pairs. Neither the sea nor the sky is a stig-
chemistry, it is equally applicable to other kinds of                  mergic medium, but the beach is.
abstract actions in which the agent is ignored—such as                     Note that most authors (e.g. Parunak, 2006) use the
political and economic interactions (Dittrich & Winter,                term ‘‘environment’’ for what I call ‘‘medium’’. This term
2005, 2008).                                                           is much less accurate, though. First, as noted, the environ-
   According to our deﬁnition, the action part of a rule               ment is not in general both perceivable and controllable.
produces a change in the state of the world. This means                Second, the environment normally denotes everything out-
that it creates a new condition, which may activate another            side the system or agent under consideration. However,
condition ! action rule and thus a new action. For exam-               stigmergy can also make use of an internal medium. For
ple, the thermostat, by switching on the heating, will even-           example, diﬀerent physiological processes in the body com-
tually produce the new condition ‘‘temperature high                    municate via the release of hormones in the bloodstream
enough’’, which in turn will trigger the new action ‘‘switch           (medium). This communication is indirect: e.g. the liver
heating oﬀ’’ (Heylighen & Joslyn, 2003). The NaCL mole-                does not directly send a message to the brain; both merely
cule may react with another molecule in the solution and               ‘‘read’’ the hormonal messages deposited in the blood that
thus produce yet another compound. This triggering of                  irrigates both. More generally, many aspects of the agent’s
an action by a previous action via the intermediary of its             own state, such as the agent’s position, speed and orienta-
result is precisely what Grassé deﬁned as stigmergy. Yet,             tion, belong to the medium, since they are controllable and
the way we arrived at this notion is so simple and general             perceivable by self and others.
that it merely requires a minimal assumption of causality.                 Finally, if we conceive the environment as that part of
In the next sections, we will need to explain how such a               the world that interacts with an agent, then diﬀerent agents
simple mechanism can produce such rich and unexpected                  live in diﬀerent environments or ‘‘Umwelts’’: not all phe-
phenomena.                                                             nomena perceivable or controllable by one agent are simi-
   First, we should note that the causal relation does not             larly perceivable and controllable by another agent. When
need to be deterministic: in general, the condition is neither         we consider stigmergic coordination between diﬀerent
necessary nor suﬃcient for the action to occur. According              agents, we need to deﬁne the medium as that part of the
to Grassé’s deﬁnition, the condition merely stimulates the            world that is controllable and perceivable by all of them.
performance of the action. This means that the presence                This is necessary to ensure that the diﬀerent agents can
of the condition makes the performance of the action more              interact via the medium. The role of the medium is to allow
probable. Formally:                                                    interaction or communication between diﬀerent actions
--- pdf page 5 ---
8                                         F. Heylighen / Cognitive Systems Research 38 (2016) 4–13

and thus, indirectly, between the agents that perform the                 (1) one action can be prerequisite for the next action: the
actions. It is this mediating function that underlies the true                product or output of the ﬁrst is a necessary condition
power of stigmergy (Heylighen, 2006).                                         or input for the second. This determines the sequen-
   A ﬁnal component of a stigmergic system is the mark or                     tial organization of the process, or workﬂow, where
trace, i.e. the perceivable change made in the medium by                      activity moves step-by-step through a sequence of
an action, which may trigger a subsequent action. I prefer                    tasks (what needs to be done next?).
the term ‘‘trace’’ because it can denote an unplanned or even             (2) two actions can require the same condition (input)
undesired side eﬀect of the action, unlike a ‘‘mark’’ which is                and/or contribute to the same eﬀect or goal (output),
normally made intentionally. Some forms of stigmergy rely                     i.e. they are performed in parallel. This determines
on intentionally made signs or signals (‘‘markers’’), but in                  the division of labor between agents (who is to do
the most general situation, this is not the case. The trace is                what?).
a consequence of the action and as such, it carries informa-
tion about the action that produced it. We might see the trace             Eﬀective coordination means that the right actions are
as a message, deposited in the medium, through which the                performed by the right agents at the right time and place.
pattern of activity communicates with itself, while maintain-           Let us consider the building of a house as an activity that
ing a continuously updated ‘‘memory’’ of its achievements.              requires coordination between its diﬀerent tasks. The task
   From the point of view of an individual agent, on the                of laying electricity obviously can only be performed once
other hand, the trace is a challenge: a situation that incites          the windows and roof are installed. Rooﬁng is therefore
action, in order to remedy a perceived problem or short-                prerequisite for laying electricity and the electricians will
coming, or to exploit an opportunity for advancement                    have to wait until the roofers are ﬁnished. Plastering the
(Heylighen, 2012). We may assume may here that agents                   interior walls, on the other hand, can only be done after
have a minimal form of intentionality. This means that                  the electrical cables and outlets have been dug into the
their actions are not random, like the mutations that                   walls. This implies the sequence: rooﬁng ! laying electric-
underlie biological evolution, but directed toward the                  ity ! plastering. On the other hand, plumbing and laying
agent’s preferred state or goal. Reaching a far-away goal,              electricity can be performed simultaneously or in parallel,
however, requires more than a minimal intelligence: this                since they both require rooﬁng and are prerequisite for
will typically necessitate a complex scheme of actions, per-            plastering, but are otherwise independent of each other.
formed according to a speciﬁc order or logic. The diﬃcul-               The dependencies or connections between these diﬀerent
ties involved in problem solving, planning and project                  processes can be represented in the following ‘‘workﬂow’’
management may remind us that there is no obvious way                   diagram (Fig. 2).
to go from elementary actions to complex activity schemes.                 This diagram represents only a small part of the com-
This brings us to the problem of coordination (Crowston,                plex of activities that is necessary to construct a building.
1997), which stigmergy appears to solve.                                Construction work and other complex activities are nor-
                                                                        mally planned in detail beforehand, using tools such as
4. Coordination                                                         project schedules and GANTT charts, to specify the
                                                                        dependencies between the diﬀerent tasks. This planning
   According to the Oxford Dictionary, coordination can                 is necessary to make sure that the work is eﬃciently per-
be deﬁned as:                                                           formed, by avoiding situations such as the plasterers turn-
                                                                        ing up when the plumbing is still going on so that they
                                                                        cannot start their work. The plan will normally specify
    the organization of the different elements of a complex body
                                                                        the beginning and end of all the actions as well as the
    or activity so as to enable them to work together effectively.
                                                                        agents that are to perform them and possibly the places
    In the case of stigmergy, the ‘‘elements’’ are the diﬀerent         or resources that the agents need to access. If everybody
actions or agents. ‘‘Eﬀectively’’ means that they achieve an            keeps to this plan, the plasterers will show up on the exact
intended eﬀect or goal. ‘‘Working together’’ means that the             time and place that the plumbers are supposed to have
actions are harmonious or synergetic, the one helping rather            ﬁnished their work.
than hindering the other. ‘‘Organization’’ can be deﬁned as                The problem with planning, of course, is that there will
structure with function (Gershenson & Heylighen, 2005).                 always be unforeseen contingencies, such as the plumbers
The function is the achievement of the intended eﬀect. A                needing an extra day to ﬁnish their work, or, on the con-
‘‘structure’’ consists of distinct elements (the actions or             trary, ﬁnishing two days early. In both cases, the work is
agents) that are connected in such a way as to form a coher-            performed less eﬃciently than it could be, either because
ent whole. This brings us to focus on the connections that              the plasterers need to go home because the plumbing is
integrate the actions into a synergetic, goal-directed whole.           not ready yet, or stay home waiting for the work to ﬁnish
    According to coordination theory (Crowston, 1997), we               when they could already have started. Contingencies dis-
can distinguish the following fundamental dependencies or               turbing carefully laid-out plans can have even worse
connections between actions or processes:                               results, as illustrated by the following joke:
--- pdf page 6 ---
                                          F. Heylighen / Cognitive Systems Research 38 (2016) 4–13                                     9




                                          Fig. 2. Parallel and sequential connections between tasks.


  A pensioner watches two city workers busy in the municipal             demand that specialized workers visit the site every day
  park. The one digs a series of deep holes at regular intervals.        while they are not yet needed. However, this can be easily
  The other one then shovels the mounds of earth carefully               tackled with modern technology, by providing a website on
  back into each hole and ﬂattens the soil. The pensioner asks           which the state of the work is registered in real time. In this
  him: “Isn't that a waste of effort what you are doing?”, to            way, the plumbers can see immediately whether they are
  which the worker replies: “No, we always work this way                 needed, without losing time traveling to the site. The web-
  and it is very efﬁcient. It is just that the third guy who plants      site plays the role of a medium providing special markers to
  the trees did not show up today.”                                      guide the execution of the work—similar to the phero-
                                                                         mones used by ants.
   One way to deal with such contingencies is to let the
                                                                            This is in essence how a community of programmers
agents communicate about their work. For example, the
                                                                         residing in diﬀerent parts of the world collaboratively
plumbers ﬁnishing early or late could call the plasterers
                                                                         develop a complex suite of open-source software: they reg-
to warn them about the diﬀerent ﬁnishing date. However,
                                                                         ularly check their shared website for new modules, updates,
this assumes that agents know all other agents that depend
                                                                         requests for features, or postings of bugs. They address
on their work and have a general notion of what these
                                                                         these challenges by writing additional code or suggesting
dependencies are so that they can improvise or reschedule
                                                                         solutions, posting these results in turn on the website for
their activity in the light of the new information. With com-
                                                                         others to see and to elaborate (Bolici et al., 2009;
plex activities, this is tricky and can easily lead to misun-
                                                                         Heylighen, 2007; Heylighen, Kostov, & Kiemen, 2013).
derstandings or confusions that make things worse. An
                                                                         Such open source development has proven to be at least
alternative is that all agents report to a supervisor, who
                                                                         as eﬀective as the traditional planned software develop-
keeps track of the plan, reschedules if need be and warns
                                                                         ment performed in large corporations (Weber, 2004), with-
everyone involved of the changes. However, such central
                                                                         out requiring any central supervision or other complicated
controller becomes a bottleneck that is even more sensitive
                                                                         arrangements (Raymond, 1999).
to disturbances, creating the risk that the whole plan falls
                                                                            Perhaps the only disadvantage compared to a perfectly
apart because the supervisor is not available to pass on
                                                                         designed and executed plan, is that the stigmergic approach
reschedules.
                                                                         does not guarantee an optimal use of the ‘‘workforce’’.
                                                                         While the roofers are working, the plumbers must either
5. The benefits of stigmergy                                             wait or perform another task. If they are busy with another
                                                                         task, there is no guarantee that it will be ﬁnished exactly
   How does stigmergy solve the problem of coordination?                 when the roofers ﬁnish their job. This suboptimal use of
In the examples above, the diﬀerent agents would regularly               workers can be minimized by creating a pool of available
check the situation at the work site and as soon as they                 workers (much) larger than needed for this particular job,
encounter the right conditions, they would start their work.             so that together they can keep track of several jobs in par-
For example, once the plumbers observe that the roof and                 allel. Assuming that the tasks do not all start at the same
windows are in place, they would start plumbing. Simulta-                time, there would always be some workers available for
neously but independently, the electricians would do their               any job that opens up, without requiring workers to wait
job. The plasterers would begin as soon as both the plumb-               long times in between jobs, or tasks to wait long for work-
ing and the electricity are ﬁnished. On the other hand, the              ers to execute them. This is the approach underlying the job
municipal worker would ﬁll a hole only on the condition                  ticketing systems used in call centers (Heylighen & Vidal,
that it contains a tree.                                                 2008; Orrick, Bauer, & McDuﬃe, 2000), but also the one
   While this approach may seem natural for termites, who                used by ants and termites. It explains why the best-
are anyway all wandering around their nest building site,                known applications of stigmergy typically rely on ‘‘massive
you might wonder whether it would not be ineﬃcient to                    parallelism’’, i.e. many agents active simultaneously
--- pdf page 7 ---
10                                     F. Heylighen / Cognitive Systems Research 38 (2016) 4–13

(Manderick & Moyson, 1988). In the case of software                     the condition and the quicker it will be to start the job;
development, there is no particular time at which a coding              in this way, tasks are automatically assigned to the most
job has to be done, so programmers can be ﬂexible in                    competent agents (Heylighen & Vidal, 2008).
deciding when to produce an improvement suggested by                   commitment: agents do no need to commit to a particu-
the stigmergic repository of tasks and products.                        lar task (in contradiction to what (Jennings, 1993)
    With such a stigmergic organization, no conﬂicts                    claims about multi-agent coordination); an agent deci-
between instructions and reality arise, no needless delays              des on the spot what work it should do, depending on
occur and no eﬀort is wasted—whatever the contingencies                 opportunity and other contingent conditions; an agent
that may disturb the plan. Moreover, this solution is per-              that quits or otherwise becomes unavailable is automat-
fectly robust and independent of any errors in communica-               ically replaced by another one.
tion or control. It also does not depend on the number of              centralized control or supervision: errors or perturbations
agents, tasks, or dependencies between tasks. This allows               are automatically corrected, as they merely create a new
it to scale up to tasks of indeﬁnite sizes. The only require-           condition stimulating new actions to deal with the chal-
ments are that the agents can recognize the right conditions            lenge; the activity is self-organizing. For example, bugs
to start their work and that they can all access the medium             in open-source software are spotted by users and
in which these conditions are registered. In summary, stig-             resolved by other contributors.
mergy provides an extremely simple and reliable solution to
a problem that is potentially unlimited in complexity.
    Compared to traditional methods of organization, stig-           6. Self-organization through negative feedback
mergy makes absolutely minimal demands on the agents.
In particular, in stigmergic collaboration there is no need              This last point deserves an elaboration. Our assumption
for:                                                                 is that agents are individually goal-directed. Cybernetics
                                                                     has shown how goal-directedness emerges from negative
 planning or anticipation: agents only need to know the             feedback: perceived deviations from the goal are compen-
  present state of the activity; the overall goal, next step         sated by counteractions (Heylighen & Joslyn, 2003;
  or end result is irrelevant for their present work. In             Rosenblueth, Wiener, & Bigelow, 1943). This most basic
  Wikipedia, there is no plan specifying which informa-              mode of steering is also called error-controlled regulation:
  tion should be added to the encyclopedia when.                     whatever the origin of the deviation or ‘‘error’’, once it is
 memory: agents do not need to remember their previous              sensed, its eﬀect is suppressed by a compensatory action.
  activity; no information about the state of the work               This control mode does not require any anticipation (feed-
  needs to be stored anywhere except in the medium.                  forward), memory, or understanding of what caused the
 communication: no information needs to be transferred              deviation. To eﬃciently control the eﬀect, it is suﬃcient
  between the agents, except via the work done in the                that the agent is able to exert an inﬂuence in the ‘‘opposite
  medium; there is in particular no need for the agents              direction’’ of any deviation, independently of its underlying
  to negotiate about who does what.                                  cause (Gershenson & Heylighen, 2005).
 mutual awareness: each agent works independently; it                   This mechanism is well understood for individual agents
  does not even need to know that others participate.                (Powers, 1973). Stigmergy illustrates how it can be
  For example, contributors to Wikipedia generally do                extended to several interacting agents. Imagine a group
  not know each other or communicate with each other.                of non-communicating agents (e.g. ants, or people who
 simultaneous presence: there is in general no need for the         do not speak a common language) pushing a large obstacle
  agents to be present at the same time or at the same               out of the way across an irregular terrain. Individually,
  place; tasks are registered in the medium so that they             each agent will correct its course based on the perceived
  can be picked up by agents whenever and wherever they              movement of the load: e.g. if it shifts too much to the left,
  are available. That is how worldwide communities can               the agent will push more toward the right. It does not mat-
  collaborate on a single software project.                          ter whether the deviation was caused by a hole in the sur-
 imposed sequence: actions are performed automatically              face, a sudden gust of wind, or the misdirected action of
  in the right order, since an action will not be started            another agent. The overall movement will be determined
  until the right condition is in place; the workﬂow                 by the sum of the actions performed by all the individuals.
  emerges spontaneously, as the completion of one task               As long as the agents push in generally the same direction,
  triggers the initiation of the next task(s).                       it is irrelevant who did what. The agents can work perfectly
 imposed division of labor: each agent will only perform            independently—perhaps even without knowing that some-
  the actions for which it has the required competence,              one else is pushing too—while still producing a coordi-
  i.e. for which it possesses adequate condition-action              nated movement.
  rules; normally, the more ‘‘conﬁdent’’ the agent is about              A similar mechanism is probably involved in bodily
  the right action (i.e. the stronger the connection between         coordination, where diﬀerent muscles, joints, tendons and
  condition and action), the more it will be stimulated by           bones need to work together eﬀectively. A complex
--- pdf page 8 ---
                                        F. Heylighen / Cognitive Systems Research 38 (2016) 4–13                                  11

movement, such as balancing on one foot, requires the                 coordinating initially independent actions into a harmo-
simultaneous contraction or relaxation of many muscles.               nious whole. Thus, the group of agents can achieve much
If the actual position deviates from the desired one, indi-           more substantial results collectively than they would if they
vidual muscles will adjust their level of contraction, upward         would work alone. It is this emergence of global order out
or downward, depending on the perceived direction of the              of local actions that constitutes the hallmark of self-
deviation. Since all muscles have simultaneous access to the          organization (Heylighen, 2001).
shared ‘‘trace’’ of their activity (the present position), they
also act on it simultaneously. The sum of their actions will
normally be suﬃcient to achieve the desired eﬀect. If not—            7. Self-organization through positive feedback
that is, if one of the muscles contributes too little or too
much—either that muscle itself or one or more complemen-                  Stigmergy exhibits another fundamental ‘‘signature’’ of
tary muscles will react in order to correct the error. The            self-organization (Heylighen, 2001; Theraulaz &
muscles do not need to communicate with each other about              Bonabeau, 1999): positive feedback. Error-controlled regu-
their intention to shift position: their actions are instantly        lation assumes negative feedback: the reduction of devia-
coordinated by their simultaneous eﬀect on the trace, just            tions away from the goal. However, goal-directed action
like the actions of the agents pushing the load are coordi-           can also make use of positive feedback: the ampliﬁcation
nated by the perceived position of the load.                          of movements toward the goal. In the cybernetic perspec-
   To ensure eﬀective collective action, the only assump-             tive, changes in the situation not controlled by the agent
tion we need to add to individual error-controlled regula-            are interpreted as perturbations, since they move the sys-
tion is that the goals of the agents are not                          tem away from a previously achieved goal state
contradictory—i.e. that error decrease for one agent does             (Heylighen & Joslyn, 2003; Maturana & Varela, 1980).
not equal error increase for another agent—because then               However, as long as no ﬁnal goal is reached—which is
the agents will be involved in a tug-of-war of opposing               the default situation in long-term, on-going projects, such
counteractions. However, note that the goals do not need              as building, extending and maintaining a termite hill—such
to be identical for coordination to occur: imagine that               contingent events may as well facilitate as hinder the fur-
one group of agents pushes the obstacle to the east, while            ther movement toward the goal. When they hinder, we will
another group pushes to the north. The net eﬀect is that              call them disturbances; when they facilitate, we may call
the load will move northeast, satisfying both groups. It is           them aﬀordances (Gibson, 1977). In the most general case,
only when one group pushes eastward and another group                 we may call them diversions, since they divert action from
westward that a conﬂict arises, without possibility for a             its on-going course, whether in a positive, negative or neu-
compromise. In this two-dimensional example, the proba-               tral way (Heylighen, 2012). Assuming that agents are goal-
bility for conﬂict still seems large. However, the larger             directed, we may infer that they will counteract the distur-
the number of aspects, components or degrees of freedom               bances and reinforce or build upon the aﬀordances.
of the problem situation, the more freedom there is for                   Let us illustrate these notions with the paradigmatic case
agents to focus on diﬀerent goals without getting in each             of termites erecting a pillar as part of their nest construc-
others’ way.                                                          tion. A bit of mud that is accidentally dropped in a partic-
   This independence of goal setting is what underlies the            ular place, either by a termite, the wind or a passing bird,
automatic division of labor: each agent spontaneously                 constitutes a diversion. In this case, the diversion consti-
focuses on the task that it deems most important (and                 tutes an aﬀordance, since it provides a foundation on which
for which it is in general most competent). Thus, a variety           a taller mud structure can be erected. Stigmergic stimulation
of agents together can potentially tackle very complex                will lead termites to add mud to the emerging heap, rather
problems that require the achievement, in sequence or in              than to the ﬂat surfaces surrounding it. The taller the heap
parallel, of many diﬀerent partial objectives. We may                 grows, the stronger the stimulus it will exert on termites
assume that agents have acquired their condition-action               passing by and therefore the faster its further growth. This
rules (and thus their implicit goals) through natural selec-          positive feedback loop results in an accelerated exploitation
tion of instinctual behavior or diﬀerential reinforcement             of the opportunity, diverting eﬀort away from less promis-
of learned behavior. This means that their condition-                 ing alternatives and thus eﬃciently allocating agents and
action rules are generally appropriate to the local environ-          resources to the most productive activities.
ment, including the other agents with which they regularly                Suppose now that a fragment of the thus erected column
interact. Rules that are frequently in conﬂict with the rules         breaks oﬀ. This constitutes a negative diversion, i.e. a dis-
of other agents or the constraints of the environment are             turbance. In this case, the perception of the missing mud
likely to be eliminated eventually (Heylighen, 2008).                 will stimulate the termites to ﬁll the hole with new mud,
   Therefore, it is plausible to assume that even very diﬀer-         thus counteracting the deviation from the ideal column
ent agents, e.g. belonging to diﬀerent species in an ecosys-          shape. Finally, a neutral diversion may arise, such as a
tem, follow rules that are potentially synergetic (Corning,           breeze blowing some termites oﬀ-course, so that they end
1995; Heylighen, 2013). Stigmergy appears to be a prime               up near a diﬀerent column than the one they were heading
mechanism through which this synergy is realized, by                  to. While making the activity deviate from the original
--- pdf page 9 ---
12                                     F. Heylighen / Cognitive Systems Research 38 (2016) 4–13

course, this event neither facilitates nor hinders the work.         supervision. Because of its non-intuitive nature, its power
Therefore, it will be neither counteracted nor reinforced.           of explanation is as yet poorly recognized. I hope that
   A similar dynamics occurs in Internet communities                 the present paper will inspire further researchers to pick
centered on a particular forum, website or page. More                up the thread and examine stigmergic mechanisms in an
activity on a particular site tends to produce more                  ever-wider range of human and non-human activities. This
interesting traces, such as discussions, wiki pages, or              should not only clarify deep theoretical issues, but suggest
comments. These attract more people and therefore more               a variety of as yet unimagined practical applications.
contributions, which in turn incite more activity. Vice
versa, less activity reduces the level of interest for the           References
products of that activity and thus the number of potential
further contributions. Thus, web communities and their               Beckers, R., Holland, O. E., & Deneubourg, J. L. (1994). From local
activities are subject to a positive feedback, where the ini-            actions to global tasks: Stigmergy and collective robotics. Artiﬁcial
tially most promising ‘‘projects’’ grow very quickly, while              Life IV, 181, 189.
                                                                     Bolici, F., Howison, J., & Crowston, K. (2009). Coordination without
the less promising ones dwindle, losing the competition                  discussion? Socio-technical congruence and stigmergy in free and open
with the others and potentially disappearing altogether.                 source software projects. In Conjunction with the international confer-
In this way, work is divided eﬃciently across a wide                     ence on software engineering, Vancouver, BC, Canada.
variety of projects, ensuring that the most promising ones           Bonabeau, E., Dorigo, M., & Theraulaz, G. (1999). Swarm intelligence:
quickly ‘‘take oﬀ’’ without dissipating too much energy in               From natural to artiﬁcial systems. Oxford: Oxford University Press.
                                                                     Camazine, S., Deneubourg, J. L., Franks, N. R., Sneyd, J., Theraula, G.,
less promising ones.                                                     & Bonabeau, E. (2003). Self-organization in biological systems.
                                                                         Princeton: Princeton University Press.
8. Conclusion                                                        Corning, P. A. (1995). Synergy and self-organization in the evolution of
                                                                         complex systems. Systems Research, 12(2), 89–122.
   Our theoretical analysis of stigmergy has illustrated how         Crowston, K. (1997). A coordination theory approach to organizational
                                                                         process design. Organization Science, 8(2), 157–175.
wide-ranging and fundamental this mechanism is. Virtually            Deneubourg, J. L. (1977). Application de l’ordre par ﬂuctuations a la
all evolved processes that require coordination between                  description de certaines etapes de la construction du nid chez les
actions seem to rely at some level on stigmergy, in the sense            termites. Insectes Sociaux, 24(2), 117–130.
that subsequent actions are stimulated by the trace left by          Deneubourg, J. L., Goss, S., Franks, N., Sendova-Franks, A., Detrain, C.,
previous actions in some observable and manipulable med-                 & Chrétien, L. (1991). The dynamics of collective sorting robot-like
                                                                         ants and ant-like robots. In Proceedings of the ﬁrst international
ium. The trace functions like a registry and map, indicating             conference on simulation of adaptive behavior on from animals to
which actions have been performed and which still need to                animats (pp. 356–363).
be performed. It is shared by all agents that have access to         Deneubourg, J. L., Theraulaz, G., & Beckers, R. (1992). Swarm-made
the medium, thus allowing them to coordinate their actions               architectures. In Toward a practice of autonomous systems: Proceedings
without need for agent-to-agent communication. It even                   of the ﬁrst European conference on artiﬁcial life.
                                                                     Dipple, A., Raymond, K., & Docherty, M. (2014). General theory of
allows the coordination of ‘‘agentless’’ actions, as investi-            stigmergy: Modelling stigma semantics. Cognitive Systems Research,
gated e.g. by Chemical Organization Theory (Dittrich &                   31–32, 61–92.
Fenizio, 2007).                                                      Dittrich, P., & Winter, L. (2005). Reaction networks as a formal
   Thus, stigmergy can be seen as a fundamental mecha-                   mechanism to explain social phenomena. In Proc. fourth int. workshop
nism of self-organization: it allows global, coordinated                 on agent-based approaches in economics and social complex systems
                                                                         (AESCS 2005) (pp. 9–13). <http://users.minet.uni-jena.de/~dittrich/
activity to emerge out of local, independent actions. Like               p/DW2005.pdf>.
self-organization in general, stigmergy relies on feedback:          Dittrich, P., & Fenizio, P. S. di (2007). Chemical organisation theory.
action elicits action, via the intermediary of the trace. This           Bulletin of Mathematical Biology, 69(4), 1199–1231.
feedback is typically positive, in that actions intensify and        Dittrich, P., & Winter, L. (2008). Chemical organizations in a toy model of
elaborate the trace, thus eliciting more intense and diverse             the political system. Advances in Complex Systems, 11(04), 609.
                                                                     Dorigo, M., Bonabeau, E., & Theraulaz, G. (2000). Ant algorithms and
further actions. The resulting virtuous cycle explains in                stigmergy. Future Generation Computing Systems, 16(8), 851–871.
part why stigmergic organization is so surprisingly eﬀec-            Dron, J., Boyne, C., & Mitchell, R. (2001). Footpaths in the stuﬀ swamp.
tive, enabling the construction of complex structures—such               <http://ﬁles.eric.ed.gov/fulltext/ED466580.pdf>.
as a termite hill, a network of trails, or a world encyclope-        Elliott, M. A. (2007). Stigmergic collaboration: A theoretical framework for
dia—in a very short time, even when starting from scratch.               mass collaboration. PhD thesis, Victorian College of the Arts,
                                                                         University of Melbourne. <http://eprints.infodiv.unimelb.edu.au/
When necessary, feedback can also be negative: errors, dis-              00003977/01/elliott_phd_pub_08.10.07.pdf>.
turbances or ‘‘overshoots’’ that make the trace deviate              Gershenson, C., & Heylighen, F. (2005). How can we think complex? In
from its ideal shape will elicit actions that correct the                K. Richardson (Ed.), Managing organizational complexity: Philosophy,
deviation.                                                               theory and application (pp. 47–61). Charlotte: Information Age
   In conclusion, the concept of stigmergy allows us to                  Publishing.
                                                                     Gibson, J. J. (1977). The theory of aﬀordances. In Perceiving, acting and
explain a broad variety of ill-understood phenomena of                   knowing: Toward an ecological psychology (pp. 67–82). Boston:
spontaneous coordination, in which some kind of appar-                   Houghton-Miﬄin.
ently intelligent activity emerges out of simple causal pro-         Grassé, P. P. (1959). La reconstruction du nid et les coordinations
cesses, without requiring direct communication or central                interindividuelles chez Bellicositermes natalensis et Cubitermes sp. La
--- pdf page 10 ---
                                                F. Heylighen / Cognitive Systems Research 38 (2016) 4–13                                               13

   théorie de la stigmergie: Essai d’interprétation du comportement des     Manderick, B., & Moyson, F. (1988). The collective behavior of ants: An
   termites constructeurs. Insectes Sociaux, 6(1), 41–80.                        example of self-organization in massive parallelism. In Proceedings of
Heylighen, F. (1999). Collective intelligence and its implementation on the      the AAAI spring symposium on parallel models of intelligence, Stanford
   web: Algorithms to develop a collective mental map. Computational             University.
   and Mathematical Organization Theory, 5(3), 253–280.                       Marsh, L., & Onof, C. (2008). Stigmergic epistemology, stigmergic
Heylighen, F. (2001). The science of self-organization and adaptivity. The       cognition. Cognitive Systems Research, 9(1), 136–149.
   Encyclopedia of Life Support Systems, 5(3), 253–280.                       Maturana, H. R., & Varela, F. J. (1980). Autopoiesis and cognition: The
Heylighen, F. (2006). Mediator evolution: A general scenario for the             realization of the living. Dordrecht: Reidel.
   origin of dynamical hierarchies. In Worldviews, science and us.            Orrick, D., Bauer, J., & McDuﬃe, E. (2000). Remedial help desk 101 at
   Singapore: World Scientiﬁc.                                                   Florida State University. In Proceedings of the 28th annual ACM
Heylighen, F. (2008). Accelerating socio-technological evolution: From           SIGUCCS conference on user services: Building the future
   ephemeralization and stigmergy to the global brain. In Globalization as       (pp. 222–226). New York: ACM.
   evolutionary process: Modeling global change (pp. 284). New York:          Parunak, H. V. D. (2006). A survey of environments and mechanisms for
   Routledge.                                                                    human–human stigmergy. In D. Weyns, H. V. D. Parunak, & F.
Heylighen, F. (2011). Self-organization of complex, intelligent systems: An      Michel (Eds.), Environments for Multi-agent systems II (pp. 163–186).
   action ontology for transdisciplinary integration. Integral Review.           Heidelberg: Springer.
Heylighen, F. (2012). A tale of challenge, adventure and mystery:             Powers, W. T. (1973). Behavior: The control of perception. Chicago: Aldine
   Towards an agent-based uniﬁcation of narrative and scientiﬁc                  Transaction.
   models of behavior. ECCO working papers no. 2012-06. Brussels,             Raymond, E. (1999). The cathedral and the bazaar. Knowledge, Technol-
   Belgium.                                                                      ogy and Policy, 12(3), 23–49.
Heylighen, F., & Joslyn, C. (2003). Cybernetics and second-order              Ricci, A., Omicini, A., Viroli, M., Gardelli, L., & Oliva, E. (2006).
   cybernetics. In R. A. Meyers (Ed.). Encyclopedia of physical science          Cognitive stigmergy: A framework based on agents and artifacts. In
   and technology (3rd ed., Vol. 4, pp. 155–169). New York: Academic             Third international workshop on environments for multiagent systems
   Press.                                                                        (E4MAS 06).
Heylighen, F., Kostov, I., & Kiemen, M. (2013). Mobilization systems:         Robles, G., Merelo, J. J., & Gonzalez-Barahona, J. M. (2005). Self-
   Technologies for motivating and coordinating human action. In M. A.           organized development in libre software: A model based on the
   Peters, T. Besley, & D. Araya (Eds.), The new development paradigm:           stigmergy concept. In Proceedings of the 6th international workshop on
   Education, knowledge economy and digital futures. New York:                   software process simulation and modeling (ProSim), 16.
   Routledge.                                                                 Rosenblueth, A., Wiener, N., & Bigelow, J. (1943). Behavior, purpose and
Heylighen, F. (2007). Why is open access development so successful?              teleology. Philosophy of Science, 10(1), 18–24.
   Stigmergic organization and the economics of information. In B.            Shell, D., & Mataric, M. (2003). On the use of the term ‘‘‘stigmergy’.’’ In
   Lutterbeck, M. Baerwolﬀ, & R. A. Gehring (Eds.), Open source                  Proceedings of the second international workshop on the mathematics
   Jahrbuch 2007 (pp. 165–180). Lehmanns Media.                                  and algorithms of social insects.
Heylighen, F. (2013). Self-organization in communicating groups: The          Sumpter, D. J., & Beekman, M. (2003). From nonlinearity to optimality:
   emergence of coordination, shared references and collective intelli-          Pheromone trail foraging by ants. Animal Behaviour, 66(2), 273–280.
   gence. In À. Massip-Bonet & A. Bastardas-Boada (Eds.), Complexity         Susi, T., & Ziemke, T. (2001). Social cognition, artefacts and stigmergy: A
   perspectives on language, communication and society (pp. 117–149).            comparative analysis of theoretical frameworks for the understanding
   Berlin: Springer.                                                             of artefact-mediated collaborative activity. Cognitive Systems
Heylighen, F., & Vidal, C. (2008). Getting things done: The science behind       Research, 2(4), 273–290.
   stress-free productivity. Long Range Planning, 41(6), 585–605.             Tabony, J. (2006). Microtubules viewed as molecular ant colonies. Biology
Holland, O., & Melhuish, C. (1999). Stigmergy, self-organization and             of the Cell, 98, 603–617.
   sorting in collective robotics. Artiﬁcial Life, 5(2), 173–202.             Theraulaz, G., & Bonabeau, E. (1999). A brief history of stigmergy.
Jennings, N. R. (1993). Commitments and conventions: The foundation of           Artiﬁcial Life, 5(2), 97–116.
   coordination in multi-agent systems. The Knowledge Engineering             Turchin, V. F. (1993). The cybernetic ontology of action. Kybernetes, 22(2),
   Review, 8(03), 223–250.                                                       10–30. http://dx.doi.org/10.1108/eb005960.
Kassabalidis, I., El-Sharkawi, M., Marks, R., Arabshahi, P., & Gray, A.       Valckenaers, P., Van Brussel, H., Kollingbaum, M., & Bochmann, O.
   (2001). Swarm intelligence for routing in communication networks. In          (2006). Multi-agent coordination and control using stigmergy applied
   Global telecommunications conference, 2001. GLOBECOM’01. IEEE                 to manufacturing control. Multi-Agent Systems and Applications,
   (Vol. 6, pp. 3613–3617).                                                      317–334.
Kennedy, J. (2006). Swarm intelligence. Handbook of nature-inspired and       Weber, S. (2004). The success of open source. Cambridge: Cambridge
   innovative computing (pp. 187–219). Heidelberg: Springer.                     University Press.
