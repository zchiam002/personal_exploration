# Neuro-Symbolic AI: A Literature Review for the Entering Researcher

*Written for a data scientist with a strong ML background and no prior exposure to the field.
Literature covered through August 2026.*

---

## 0. How to read this document

This review is organised so you can stop at any depth. Section 1–2 give you the field's history and its
vocabulary — enough to read any NeSy paper's introduction. Section 3 is the technical core: eight families
of method, each with its central mechanism, its canonical papers, and the precise place it breaks.
Section 4 is what changed in 2025–26. Section 5 is the sceptical audit — read it before you believe
anything in Section 3. Sections 6–9 are practical: open problems, a reading path, runnable tooling.

**On citations.** Every reference here was checked against a bibliographic source (arXiv API, OpenAlex,
dblp, publisher pages) during preparation. Where a citation or a number could *not* be confirmed, it
carries a ⚠ and says why. Twelve metadata errors found during the audit have been corrected in place;
a few widely-repeated figures turned out to be unsupported and have been dropped rather than repeated.
Full annotated bibliography in [bibliography.md](bibliography.md).

**A warning about the field's own claims.** Neuro-symbolic AI has an unusually large gap between what its
abstracts assert and what its experiments show. This is not fraud — the community documents the gap itself,
often better than its critics do — but a newcomer who reads only the positive literature will form a badly
calibrated picture. Section 5 exists for that reason and is not optional reading.

---

## 1. The problem the field exists to solve

### 1.1 The first neural network was a logic machine

McCulloch and Pitts' 1943 [*A logical calculus of the ideas immanent in nervous activity*](https://link.springer.com/article/10.1007/BF02478259)
(Bull. Math. Biophysics 5:115–133) modelled the neuron as a threshold logic unit and showed that networks
of them realise arbitrary propositional logic. This matters rhetorically: neuro-symbolic researchers frame
their programme as *reunification*, not hybridisation. The two traditions had a common ancestor and drifted.

### 1.2 The systematicity dispute

The drift hardened into philosophy. Fodor and Pylyshyn's
[*Connectionism and cognitive architecture: A critical analysis*](https://www.sciencedirect.com/science/article/abs/pii/0010027788900315)
(Cognition 28:3–71, 1988) argued that thought is *systematic* — anyone who understands "John loves Mary"
understands "Mary loves John" — and that a network can display systematicity only by implementing a classical
symbol system, in which case it is an implementation detail rather than a cognitive theory.

Smolensky answered constructively. [*Tensor Product Variable Binding and the Representation of Symbolic
Structures in Connectionist Systems*](https://dblp.org/rec/journals/ai/Smolensky90.html) (Artificial
Intelligence 46(1–2):159–216, 1990) gave an algebra — role and filler vectors bound by outer product and
superposed — in which exact, invertible variable binding lives entirely inside a vector space. Every modern
vector-symbolic architecture descends from it, and so does a good deal of current work on binding in transformers.

**This dispute has since been adjudicated empirically, and the review literature usually forgets to say so.**
Lake and Baroni built [SCAN](https://arxiv.org/abs/1711.00350) (ICML 2018) to turn systematicity into a
measurable benchmark; seq2seq models failed it badly. Then in
[*Human-like systematic generalization through a meta-learning neural network*](https://doi.org/10.1038/s41586-023-06668-3)
(Nature 623(7985):115–121, 2023) the same authors showed that a *standard transformer*, meta-trained over a
stream of freshly generated compositional tasks, matches human systematicity head-to-head — no symbolic
machinery at all. The lesson is not that Fodor was wrong but that the requirement can be met by changing the
training distribution rather than the architecture. Any argument that systematicity *requires* symbols has to
answer this paper.

### 1.3 The engineering line

Running in parallel and largely ignoring the philosophy: Towell and Shavlik's KBANN
([Artificial Intelligence 70(1–2):119–165, 1994](https://dblp.org/rec/journals/ai/TowellS94.html))
compiled a propositional domain theory directly into a network's topology and initial weights, then refined it
by backpropagation. Every later "knowledge injection" method is a variation on KBANN.

Valiant gave the programme institutional legitimacy: *Robust logics* (Artificial Intelligence 117(2):231–253,
2000) and [*Three problems in computer science*](https://dl.acm.org/doi/10.1145/602382.602410)
(JACM 50(1):96–99, 2003) named the reconciliation of statistical learning with logical reasoning as a
foundational open problem in computing. This is the most-cited legitimacy argument in the field's introductions.

### 1.4 The third wave

The modern re-founding is largely Artur d'Avila Garcez and Luís Lamb's:
*Neural-Symbolic Cognitive Reasoning* (Springer, 2009) systematised neural encodings of modal, temporal and
epistemic logics; [*Neurosymbolic AI: The 3rd Wave*](https://arxiv.org/abs/2012.05876) (arXiv 2012.05876, 2020;
AI Review 2023) supplied the field's self-narrative and the vocabulary everyone now uses.

### 1.5 The competing programmes

You need these to understand what NeSy is arguing *against*:

| Position | Core claim | Anchor |
|---|---|---|
| **Marcus** | Scale alone will not produce robustness; need explicit cognitive models and symbol manipulation | [The Next Decade in AI](https://arxiv.org/abs/2002.06177) (2020) |
| **Bengio (System 2)** | Keep everything differentiable, but import symbolic desiderata as *inductive biases* — sparse causal mechanisms, attention as dynamic binding | [Goyal & Bengio](https://arxiv.org/abs/2011.15091), Proc. R. Soc. A 478:20210068 (2022) |
| **LeCun** | Reject both; reasoning is energy-based inference over a learned world model | [A Path Towards Autonomous Machine Intelligence](https://openreview.net/forum?id=BZ5a1r-kVsf) (2022) |
| **Chollet** | Reframe as *measurement*: intelligence is skill-acquisition efficiency relative to priors | [On the Measure of Intelligence](https://arxiv.org/abs/1911.01547) (2019) → ARC |
| **Sutton (bitter lesson)** | Hand-crafted structure loses to general methods plus compute | 2019 blog post ⚠ *(no formal venue)* |

The most serious NeSy reply to Sutton is Velasquez, **Neel Bhatt**, Topcu, Wang, Sycara, Stepputtis, Neema &
Vallabha, [*Neurosymbolic AI as an antithesis to scaling laws*](https://academic.oup.com/pnasnexus/article/4/5/pgaf117/8134151)
(PNAS Nexus 4(5):pgaf117, 2025). It concedes the history and argues that using prior knowledge and discovering
new knowledge are not exclusive. Read it — but read it noticing that its efficiency figures ("100× smaller than
GPT-3", "96.9% fewer parameters") are the authors' summaries of scattered single-domain case studies, not
general results. The audit traced them: the 100× figure is West et al. 2022 on symbolic knowledge distillation;
the 96.9% is Zhao et al. 2024 on physics-informed autonomous driving.

---

## 2. How the field maps itself

### 2.1 Kautz's six types

The organising device newcomers meet first. Presented in Henry Kautz's AAAI-2020 Engelmore Memorial Lecture,
published as [*The Third AI Summer*](https://doi.org/10.1609/aimag.v43i1.19122) (AI Magazine 43(1):93–104, 2022),
and transmitted in print by Sarker, Zhou, Eberhart & Hitzler,
[*Neuro-symbolic artificial intelligence*](https://doi.org/10.3233/aic-210084) (AI Communications 34(3):197–209, 2021).

Ordered by tightness of coupling:

1. **symbolic Neuro symbolic** — a network whose inputs and outputs are symbols (BERT/GPT over subword tokens)
2. **Symbolic[Neuro]** — a symbolic algorithm calling a neural subroutine (AlphaGo: MCTS with a learned evaluator)
3. **Neuro;Symbolic** — neural perception emits symbols consumed by a separate reasoner (NS-CL; LLM → theorem prover)
4. **Neuro:Symbolic→Neuro** — symbolic machinery generates training data for a network
5. **Neuro_{Symbolic}** — logic compiled into the network or softened into differentiable constraints (KBANN, Logic Tensor Networks)
6. **Neuro[Symbolic]** — a symbolic reasoning engine embedded inside the neural engine

Types 1 and 2 describe almost everything deployed. Types 5 and 6 are what the founders wanted. Kautz himself
notes no genuine Type 6 system exists.

> ⚠ **Citation hygiene.** The taxonomy could not be verified against Kautz's printed text (the Wiley DOI returns
> HTTP 402; the AAAI OJS article page errors). The category names and examples above come from Sarker et al. 2021
> and secondary sources. **Cite Sarker et al. 2021 for the taxonomy, not Kautz.** Notation also varies across
> secondary sources (`Neuro;Symbolic` vs `Neural | Symbolic`; `Neuro_{Symbolic}` vs `NEUROSYMBOLIC`) — don't
> quote a rendering as canonical.

### 2.2 The competitor nobody cites

The taxonomy is *contested*, and reviews that present Kautz as settled are making an interpretive move.
Van Harmelen & ten Teije, [*A Boxology of Design Patterns for Hybrid Learning and Reasoning Systems*](https://arxiv.org/abs/1905.12389)
(Journal of Web Engineering 18(1–3):97–124, 2019) gives a *compositional* grammar — boxes for models, actors,
data and symbols, wired into nestable patterns — where Kautz gives a single ordinal scale. Read both.

### 2.3 The map that will actually help you

For a reader with strong ML background, the best technical map is Marra, Dumančić, Manhaeve & De Raedt,
[*From statistical relational to neurosymbolic artificial intelligence: A survey*](https://arxiv.org/abs/2108.11451)
(Artificial Intelligence 328:104062, 2024). It positions NeSy against 25 years of statistical relational AI along
seven dimensions — semantics (proof-based vs model-based), fuzzy vs probabilistic, directed vs undirected, type of
logic, parameter vs structure learning, symbolic vs subsymbolic representation, and how logic is grounded.
It explains *why* DeepProbLog, Logic Tensor Networks, Scallop and semantic loss differ, in terms of inference and
semantics rather than block diagrams. It also quietly demonstrates that many "new" NeSy systems are re-derivations
of StarAI ideas.

Two more worth knowing: Wang, Yang & Wu, [*Towards Data- and Knowledge-Driven AI: A Survey on Neuro-Symbolic Computing*](https://arxiv.org/abs/2210.15889)
(IEEE TPAMI 2024) — the highest-visibility non-Western synthesis, which partitions the field differently and covers
the perception-heavy literature the European probabilistic-logic surveys underweight. And Hitzler, Sarker & Eberhart
(eds.), *Compendium of Neurosymbolic Artificial Intelligence* (IOS Press, FAIA vol. 369, 2023) — 24 invited chapters,
the closest thing to a handbook. *(Not open access. The "704 pp., 30 chapters" figure circulating online is wrong;
the publisher page shows 24 chapters running to page 546.)*

### 2.4 The LLM-era split

Since 2023 the useful vocabulary is Yang, Shao, Guo, Zhang, Zhou, Jia, Dai & Li,
[*Neuro-Symbolic AI: Towards Improving the Reasoning Abilities of Large Language Models*](https://arxiv.org/abs/2508.13678)
(IJCAI 2025 Survey Track), which splits the post-2023 literature three ways:

- **Symbolic→LLM** — symbolic structure shapes prompting or training
- **LLM→Symbolic** — the LLM formalises, a solver decides
- **LLM+Symbolic** — interleaved loops

Most 2026 papers assume this vocabulary. It is a taxonomy, not a controlled comparison — don't cite it for results.

### 2.5 There is no agreed formal definition

De Smet and De Raedt's [*Defining neurosymbolic AI*](https://arxiv.org/abs/2507.11127) (2025) proposes defining
neurosymbolic inference as the computation of an integral over a product of a logical function and a belief
function. Whether that covers embedding-based, LTN-style and LLM+solver systems — or quietly excludes them —
is unsettled. In practice "neurosymbolic" in 2026 is a family resemblance, not a definition, and the RAIL
position paper (§4.5) makes the boundary broader still.

---

## 3. The eight technical families

Each subsection follows the same shape: the mechanism in one paragraph, the papers, and where it breaks.

---

### 3.1 Logic as a loss — fuzzy and differentiable logic

**The mechanism.** Classical logic is discrete, so you can't backpropagate through it. Replace truth values
{0,1} with [0,1]; replace AND by a t-norm (Gödel/min, Łukasiewicz/max(0,a+b−1), or product a·b), OR by its dual,
implication by a residuum or S-implication, and the quantifiers by aggregators. Let the atoms be network outputs —
this mapping from logical symbols to tensors is called **grounding** — and a first-order formula becomes an
ordinary differentiable computation graph emitting a satisfaction score. Convert to a loss, add to cross-entropy,
done. Cost is roughly linear in formula size × batch size. No probabilistic inference, no model counting, no
combinatorial blow-up. **This is the standard on-ramp to the field.**

**The arc.** Semantic-Based Regularization (Diligenti, Gori & Saccà, [Artificial Intelligence 244:143–165](https://doi.org/10.1016/j.artint.2015.08.011),
online 2015 / print 2017) formalised "constraints as regularisers". **Logic Tensor Networks** — Serafini &
d'Avila Garcez's [2016 proposal](https://arxiv.org/abs/1606.04422), matured in Badreddine, d'Avila Garcez,
Serafini & Spranger's 68-page [AIJ 303:103649 (2022)](https://arxiv.org/abs/2012.13635) — gave the reference
formulation: *Real Logic*, in which constants ground to tensors, functions and predicates to networks, and
learning maximises satisfiability of a knowledge base. LYRICS (Marra et al., ECML-PKDD 2019) generalised SBR and
LTN into a declarative front-end. [DL2](https://files.sri.inf.ethz.ch/website/papers/icml19-dl2.pdf) (Fischer et al.,
ICML 2019) abandoned fuzzy semantics entirely, translating constraints over real-valued network quantities into a
loss that is exactly zero when satisfied — and reused the same machinery to *query* a trained net by gradient
search. IBM's [Logical Neural Networks](https://arxiv.org/abs/2006.13155) (Riegel, Gray, Luus et al., 2020) went
furthest: each neuron *is* a weighted real-valued connective carrying truth-value **bounds**, giving open-world
semantics and omnidirectional inference.

**A parallel branch relaxes structure rather than constraints.** [Neural LP](https://arxiv.org/abs/1702.08367)
(Yang, Yang & Cohen, NIPS 2017) turns chain rules over a knowledge graph into attention-weighted sparse matrix
products. [dILP](https://doi.org/10.1613/jair.5714) (Evans & Grefenstette, JAIR 61:1–64, 2018) enumerates rule
templates and learns continuous weights over candidate clauses, buying the noise robustness classical ILP lacks.
[Neural Theorem Provers](https://arxiv.org/abs/1705.11040) (Rocktäschel & Riedel, NIPS 2017) unroll Prolog
backward chaining and replace unification with an RBF kernel on symbol embeddings — beautiful, but the proof tree
explodes; Minervini, Riedel, Stenetorp, Grefenstette & Rocktäschel's
[*Learning Reasoning Strategies in End-to-End Differentiable Proving*](https://arxiv.org/abs/2007.06477)
(ICML 2020) learns a rule-selection strategy to make it tractable. *(Note: "Conditional Theorem Provers" is the
method name, not the paper title — a very common miscitation.)*

**A third branch puts logic in the architecture.** [difflogic](https://arxiv.org/abs/2210.08277) (Petersen,
Borgelt, Kuehne & Deussen, NeurIPS 2022) parameterises each neuron as a relaxed softmax over the 16 binary Boolean
gates, trains by gradient descent, then discretises to hard gates. [Convolutional difflogic](https://proceedings.neurips.cc/paper_files/paper/2024/hash/db988b089d8d97d0f159c15ed0be6a71-Abstract-Conference.html)
(NeurIPS 2024 Oral) reaches **86.29% on CIFAR-10 with 61 million logic gates, 29× smaller than prior SOTA**.
*(The widely-circulated "4 nanosecond inference" and "29×–61×" figures are not in the paper — they came from a
social-media post. Drop them.)*

**Where it breaks — and this is the most valuable thing in the sub-area.**

*Operator pathologies.* Van Krieken, Acar & van Harmelen,
[*Analyzing Differentiable Fuzzy Logic Operators*](https://arxiv.org/abs/2002.06100) (Artificial Intelligence
302:103602, 2022) differentiated the whole operator zoo and found most unusable: Gödel min/max routes gradient to
a single argument; Łukasiewicz operators have large zero-gradient plateaus; product t-norms vanish as operands
saturate; and residuated implications have a severe antecedent/consequent gradient imbalance, so the cheapest way
to "satisfy" A→B is to push A to zero and make it vacuously true. **Their headline finding: the configurations
that train best are non-standard combinations that no longer obey ordinary logical laws.** You are optimising a
logic-*shaped* surrogate, not logic.

*Reasoning shortcuts.* Even with a perfect relaxation, the constraint under-determines the concepts. Marconato,
Teso, Vergari & Passerini, [*Not All Neuro-Symbolic Concepts Are Created Equal*](https://arxiv.org/abs/2305.19951)
(NeurIPS 2023), showed a model can hit 100% task accuracy and full constraint satisfaction while grounding symbols
with entirely wrong semantics — an identifiability failure. This broke the field's central marketing claim:
*satisfying the constraint does not mean the network learned the right symbols*, so the promised interpretability
and OOD robustness do not follow.

> **Priority note.** The reasoning-shortcut literature is usually dated to 2023. It shouldn't be. Topan, Rolnick
> & Si, [*Techniques for Symbol Grounding with SATNet*](https://arxiv.org/abs/2106.11072) (2021), showed that
> SATNet's celebrated visual-Sudoku result depended on **label leakage** and that SATNet fails at symbol grounding
> without extra machinery. That is the same failure, documented two years earlier, on a headline result. It is
> also the field's cleanest replication failure and belongs in every discussion of NeSy evaluation.

The 2026 synthesis is Marconato, Bortolotti, van Krieken, Morettin, Umili, Vergari, Tsamoura, Passerini & Teso,
[*Symbol Grounding in Neuro-Symbolic AI: A Gentle Introduction to Reasoning Shortcuts*](https://arxiv.org/abs/2510.14538)
(JAIR, special track on Integration of Logical Constraints in Deep Learning).

**Status in 2026.** Almost no new *frameworks* since ~2022; the intellectual energy since 2023 has gone into the
critique literature — a field auditing itself. Two branches are healthy for opposite reasons: differentiable
logic-gate networks (an efficiency story, not a reasoning story, with a real niche in ultra-low-latency and
hardware inference), and the reasoning-shortcut/identifiability line, which now has a benchmark suite (rsbench),
complexity results, and a JAIR synthesis.

> ⚠ **A verdict I have softened.** One research thread concluded that differentiable ILP (dILP, NTP/CTP, Neural LP,
> DRUM, RNNLogic) "looks substantially superseded". That is a conclusion about one sub-community. Counter-evidence
> from an entirely separate cluster (§3.3): Gao, Inoue et al., *Differentiable Rule Induction from Raw Sequence
> Inputs* (ICLR 2025); Eiter, Inoue & Moriyama, *Neural Decision-Propagation for Answer Set Programming*
> (IJCAI-ECAI 2026, [arXiv:2605.01797](https://arxiv.org/abs/2605.01797)); Baugh et al., *Disentangling Neural
> Disjunctive Normal Form Models* (NeSy 2025); Rader & Russo on vectorised NeurASP (TPLP). The line is smaller
> than it was, not dead.

---

### 3.2 Logic as exact inference — probabilistic NeSy, weighted model counting, tractable circuits

**The whole sub-area rests on one reduction.** Take a logic program whose facts are independent Bernoulli
variables, ask for the probability that a query succeeds, and you get **weighted model counting (WMC)**: sum the
weights of all satisfying assignments of a Boolean formula. Fierens et al.,
[*Inference and learning in probabilistic logic programs using weighted Boolean formulas*](https://doi.org/10.1017/s1471068414000076)
(TPLP 15(3):358–401, 2015), made this the standard ProbLog pipeline — ground, collect proofs into a provenance
formula, compile that into a circuit, evaluate.

**WMC is #P-hard.** Everything downstream is one of three things, and if you internalise only one thing from this
section, make it this trichotomy:

1. **Compilation** — pay an exponential once, evaluate cheaply forever
2. **Approximation** — drop proofs, sample, or learn a surrogate for the count
3. **Restriction** — pick a logical fragment where counting is easy

**Why compilation makes the neural part possible.** Darwiche & Marquis'
[*A Knowledge Compilation Map*](https://arxiv.org/abs/1106.1819) (JAIR 17:229–264, 2002) organises target languages
by succinctness vs which queries they answer in polytime. Two structural properties make counting linear:
*decomposability* (an AND's children share no variables, so products factorise) and *determinism* (an OR's children
are mutually exclusive, so sums don't double-count). A compiled d-DNNF or SDD is literally an arithmetic circuit
of sums and products — **and an arithmetic circuit is differentiable.** That is the hinge the entire construction
turns on. Probabilistic circuits (sum-product networks; PSDDs) are the same object viewed as a learnable model class.

**The systems.** [DeepProbLog](https://proceedings.neurips.cc/paper_files/paper/2018/hash/dc5d637ed5e62c36ecb73b654b05ba2a-Abstract.html)
(Manhaeve, Dumančić, Kimmig, Demeester & De Raedt, NeurIPS 2018; journal version
[Artificial Intelligence 298, article 103504, 2021](https://doi.org/10.1016/j.artint.2021.103504)) introduced the
**neural predicate**: the network's softmax supplies fact probabilities, the compiled circuit computes the query
probability, gradients flow back through sums and products. **MNIST-addition** — two digit images, supervision only
on their sum — became the field's fruit fly because it isolates the hard part exactly: latent discrete concepts
supervised only through a symbolic function.

Then: [NeurASP](https://www.ijcai.org/proceedings/2020/0243.pdf) (Yang, Ishay & Lee, IJCAI 2020) swaps Prolog for
answer set programming, which is far more natural for combinatorial constraints. SLASH backs the neural predicate
with a probabilistic circuit. DeepStochLog (AAAI 2022) restricts to stochastic definite clause grammars, turning
inference into parsing. NeuPSL (IJCAI 2023) abandons discrete counting for a convex energy over continuous truth
values. Embed2Sym (KR 2022) skips differentiable reasoning entirely — cluster the embeddings, then label the
clusters with a solver. **[Scallop](https://doi.org/10.1145/3591280)** (Huang, Li, Chen, Samel, Naik, Song & Si,
NeurIPS 2021; Li, Huang & Naik, PACMPL 7(PLDI):1463–1487, 2023) generalises all of it with a **provenance semiring**,
where the differentiable top-*k*-proofs semiring gives an explicit dial trading exactness for cost.

Xu, Zhang, Friedman, Liang & Van den Broeck's [semantic loss](https://proceedings.mlr.press/v80/xu18h.html)
(ICML 2018) is the same WMC machinery used as a *regulariser* rather than an architecture — the cheapest possible
entry point for an ML practitioner: one extra loss term, no architecture change, no inference-time cost.

**Why Markov logic networks lost.** Richardson & Domingos'
[MLNs](https://link.springer.com/article/10.1007/s10994-006-5833-1) (Machine Learning 62(1–2):107–136, 2006) are the
historical precursor: weighted first-order formulas defining a ground Markov network. They lost because an
undirected model needs a global partition function over an exploding grounding, and there was no compact
differentiable computation graph to hand to autograd. Directed probabilistic-logic semantics plus knowledge
compilation give you that graph for free. This is why the neural wave built on ProbLog rather than Alchemy.

**Since 2023 the story is almost entirely scaling.** [A-NeSI](https://arxiv.org/abs/2212.12393) (van Krieken et al.,
NeurIPS 2023) replaces the counting step with learned neural surrogates, pushing MNIST-addition from ~4 digits to
15. On the systems side: [KLay](https://arxiv.org/abs/2410.11415) (ICLR 2025) restructures irregularly sparse
circuits into GPU-parallel "knowledge layers"; [Dolphin](https://arxiv.org/abs/2410.03348) (ICML 2025) vectorises
provenance on GPU, reporting **1.71×–62× speedups across 13 benchmarks** and convergence on hard benchmarks where
Scallop, ISED and IndeCateR+ fail entirely; DeepLog compiles to GPU algebraic circuits; REASON (HPCA 2026) is a
dedicated accelerator. **This shift from new formalisms to systems engineering is what a field does when its
conceptual core is settled — not what a dying field does.**

**In parallel the field turned self-critical.** Van Krieken, Minervini, Ponti & Vergari,
[*On the Independence Assumption in Neurosymbolic Learning*](https://arxiv.org/abs/2404.08458) (ICML 2024), prove
that the near-universal assumption that symbol probabilities are conditionally independent given the input biases
these systems toward overconfidence, cannot represent uncertainty over multiple valid assignments, and yields
highly disconnected non-convex minima. **This is the most important negative result here: independence is what
makes WMC factorise and therefore what makes the whole approach tractable — so the tractability trick has a real
statistical cost, not just an approximation cost.** The constructive answer is
[Neurosymbolic Diffusion Models](https://arxiv.org/abs/2505.13138) (NeurIPS 2025): discrete diffusion over the
symbol sequence, reusing independence only *within* each step.

**Honest scale.** A-NeSI's own comparison table: DeepProbLog 97.20% at N=1 digit, 95.20% at N=2, **timeout at N=4**;
DeepStochLog times out at N=15; A-NeSI reaches N=15 at **75.90% ± 2.21**. The benchmark that defines the field is
simultaneously a toy and, once scaled, unsolved. There is no published demonstration of differentiable logical
inference over a knowledge base of the size non-differentiable engines handle routinely.

---

### 3.3 Abduction and consistency — the family the Western surveys omit

**Architecturally distinct, and the largest non-Western NeSy cluster.** Zhi-Hua Zhou's Nanjing LAMDA group has run
**Abductive Learning (ABL)** since 2018. Dai, Xu, Yu & Zhou,
[*Bridging Machine Learning and Logical Reasoning by Abductive Learning*](https://papers.nips.cc/paper_files/paper/2019/hash/9c19a2aa1d84e04b0bd4bc888792bd1e-Abstract.html)
(NeurIPS 2019), is the anchor.

The mechanism: a perception model proposes pseudo-labels; a symbolic knowledge base **abduces** the most consistent
revision of those labels; the model is retrained on the revised labels; repeat. It optimises *consistency*, not a
differentiable relaxation. **No fuzzy logic, no weighted model counting, no differentiability requirement at all.**
Demonstrated on handwritten-equation decipherment where even the arithmetic operation is unknown.

Still producing: Hu, Dai, Jiang & Zhou (AAAI 2025 Oral, [arXiv:2412.08457](https://arxiv.org/abs/2412.08457));
*Curriculum Abductive Learning* (NeurIPS 2025, [arXiv:2505.12275](https://arxiv.org/abs/2505.12275)), which reports
that search over abductive revisions is itself the bottleneck.

**Why this matters for how you read the field.** The standard claim that tightly-coupled NeSy is stuck at
MNIST-plus-constraints scale is made almost entirely without engaging this line, and the standard framing that
tight coupling *requires* differentiable relaxation or WMC is falsified by it. Nobody has run ABL, DeepProbLog and
LTN on a common suite at matched supervision — that comparison is an obvious, unclaimed research contribution.

**A related and equally invisible cluster** is Japanese: Katsumi Inoue (NII), Taisuke Sato and Chiaki Sakama built
a "logic programming in vector spaces" and differentiable-ASP line — Sato/Takemura/Inoue on end-to-end ASP
computation; Gao, Inoue et al., *Differentiable Rule Induction from Raw Sequence Inputs* (ICLR 2025);
Eiter, Inoue & Moriyama, *Neural Decision-Propagation for Answer Set Programming*
([IJCAI-ECAI 2026](https://arxiv.org/abs/2605.01797)); Takemura & Inoue, *Differentiable Logic Programming to
Mitigate Reasoning Shortcuts* (ICLP 2026, EPTCS 450:29–51).

---

### 3.4 Logic as a hard guarantee — constraint layers, constrained decoding, verification

**The organising question.** If you have a specification your model must never violate — a JSON schema, a class
hierarchy, a physics equality, a safety envelope, a legal rule — *where do you put it?* There are exactly four
places, and you should learn to read any paper in this area as an answer to that question.

#### (1) In the loss — soft, no guarantee

Semantic loss, DL2, t-norm relaxations. The cost is honest and severe: a differentiable, architecture-agnostic
regulariser that improves data efficiency and often accuracy, and **guarantees nothing**. In non-convex settings
the penalised and constrained problems are not equivalent — a fixed penalty silently converts a hard requirement
into a trade-off, and tuning the coefficient changes the objective you are solving.

#### (2) In the architecture — hard at training time

- **C-HMCNN** (Giunchiglia & Lukasiewicz, NeurIPS 2020) — hierarchy constraints via a max-constraint module
- **[MultiplexNet](https://arxiv.org/abs/2111.01564)** (Hoernle, Karampatsis, Belle & Gal, AAAI 2022) — constraint in
  DNF, one output transformation per disjunct, 100% satisfaction of quantifier-free linear arithmetic. Its stated
  limitation (DNF blow-up) is exactly what the next entry fixes.
- **[Semantic Probabilistic Layers](https://arxiv.org/abs/2206.00426)** (Ahmed, Teso, Chang, Van den Broeck &
  Vergari, NeurIPS 2022) — multiply a compiled constraint circuit by an expressive probabilistic circuit,
  renormalise exactly. The product is itself tractable, so you keep a *calibrated distribution over the feasible
  set*. This is the reference guarantee layer.
- **[DC3](https://arxiv.org/abs/2104.12225)** (Donti, Rolnick & Kolter, ICLR 2021) — equality completion plus
  unrolled gradient correction for inequalities; the bridge to "learning to optimize"
- **[HardNet](https://arxiv.org/abs/2410.10807)** (Min & Azizan) — closed-form differentiable projection for
  input-dependent affine/convex constraints, **with a proof that universal approximation is retained**. This answers
  the standing objection that hard layers cost you capacity. ⚠ *arXiv only as of v4; no accepted venue listed.*

**Missing from most NeSy reviews and probably the most relevant to your day job:** the *predict-then-optimise* /
decision-focused family. Vlastelica, Paulus, Musil, Martius & Rolínek,
[*Differentiation of Blackbox Combinatorial Solvers*](https://arxiv.org/abs/1912.02175) (ICLR 2020), gives an
informative gradient for *exact* combinatorial solvers (shortest path, TSP, min-cost matching) treated as black
boxes, via implicit linear interpolation of the piecewise-constant solver output — one extra solver call per
backward pass, no relaxation. This is where routing, matching and scheduling problems live, and where the
Warcraft-shortest-path benchmark the NeSy literature keeps citing actually comes from. Its counterpart on the
"learn the constraints instead of injecting them" side is [SATNet](https://arxiv.org/abs/1905.12149) (Wang, Donti,
Wilder & Kolter, ICML 2019) — a differentiable MAXSAT layer — read together with the Topan et al. replication
failure noted in §3.1.

#### (3) At decoding time — where NeSy actually shipped

For LLMs the constraint lives in a token mask. Geng, Josifoski, Peyrard & West,
[*Grammar-Constrained Decoding for Structured NLP Tasks without Finetuning*](https://aclanthology.org/2023.emnlp-main.674/)
(EMNLP 2023), reframed "JSON mode" as a general symbolic interface. Willard & Louf's
[*Efficient Guided Generation for LLMs*](https://arxiv.org/abs/2307.09702) (outlines) made it cheap by precomputing
an FSM index over the vocabulary. [XGrammar](https://arxiv.org/abs/2411.15100) (MLSys 2025) split the vocabulary
into context-independent tokens (~99%, precomputable into bitmasks) and context-dependent tokens (~1%, runtime
pushdown-automaton stack), reporting **up to 100× over prior grammar-constrained decoding** with near-zero serving
overhead. It is the default structured-generation backend for vLLM, SGLang and TensorRT-LLM.

**This is, by deployment volume, the most widely used symbolic constraint on a neural model in the world.**
Whether it deserves the NeSy label is an interpretive question — but the mechanism is exactly type-2 Symbolic[Neuro].

**Two gotchas you must know before shipping it:**

- **Masking is not conditioning.** Park, Wang, Berg-Kirkpatrick, Polikarpova & D'Antoni,
  [*Grammar-Aligned Decoding*](https://arxiv.org/abs/2405.21047) (NeurIPS 2024), show greedy grammar-constrained
  decoding produces grammatical strings at probabilities **not** proportional to the model's own distribution
  conditioned on the grammar. Their ASAp provably converges to the correct one — at the cost of repeated sampling.
- **Over-narrow grammars destroy reasoning.** [CRANE](https://arxiv.org/abs/2502.09061) (Banerjee, Suresh, Ugare,
  Misailovic & Singh, ICML 2025) proves that a grammar admitting only syntactically valid *final answers* strips
  out the intermediate-computation strings the model needs, and recovers **up to 10 accuracy points** on
  GSM-Symbolic and FOLIO by augmenting the grammar with an unconstrained reasoning region. This is why modern
  schemas leave room for a scratchpad field.

#### (4) Outside the model — shields and verifiers

[Shielding](https://arxiv.org/abs/1708.08611) (Alshiekh, Bloem, Ehlers, Könighofer, Niekum & Topcu, AAAI 2018)
synthesises a reactive system from an LTL safety spec that overrides unsafe actions, with analysis of when it
preserves convergence. [Probabilistic logic shields](https://arxiv.org/abs/2303.03226) (Yang, Marra, Rens &
De Raedt, IJCAI 2023, distinguished paper) make the shield differentiable via probabilistic logic programming so
safety shapes the policy gradient rather than only vetoing at execution.

Formal verification proper runs [Reluplex](https://arxiv.org/abs/1702.01135) (Katz, Barrett, Dill, Julian &
Kochenderfer, CAV 2017) → Marabou 2.0 (CAV 2024) → α,β-CROWN, which won VNN-COMP 2025. **Calibrate accordingly:**
the guarantee is real, but the benchmark networks are small ONNX models and the properties are local robustness or
control envelopes — not the transformer you are shipping. Claims that this "verifies AI systems" are overstated by
roughly the gap between an ACAS Xu controller and a frontier model.

**Practical takeaway, unglamorous but well-supported:** use hard decoding constraints for format, hard layers or
projections for numeric feasibility, external shields and checkers for safety, and treat soft losses as a
data-efficiency trick — never as a guarantee.

---

### 3.5 Perception → symbols → executor

**The engineering bet:** deep nets are good at seeing and bad at long compositional inference, so split the job —
have the network emit a structured, symbol-like description of the scene, and let a classical executor reason over it.

[CLEVR](https://openaccess.thecvf.com/content_cvpr_2017/html/Johnson_CLEVR_A_Diagnostic_CVPR_2017_paper.html)
(Johnson et al., CVPR 2017) made the bet testable. [NS-VQA](https://arxiv.org/abs/1810.02338) (Yi, Wu, Gan,
Torralba, Kohli & Tenenbaum, NeurIPS 2018) ran Mask R-CNN plus an attribute CNN to build an explicit object table,
an LSTM seq2seq to parse the question into a program, then executed the program on the table: **99.8% on CLEVR**.
The transferable lesson is that symbolic execution is *length-robust* — accuracy does not decay as program depth
grows. (Read the accuracy number critically; see §5.1.)

[NS-CL](https://arxiv.org/abs/1904.12584) (Mao, Gan, Kohli, Tenenbaum & Wu, ICLR 2019) removed most of the
supervision: concepts became learned embeddings, execution became *quasi-symbolic* (soft masks over object slots)
so gradients flow, and training used only (image, question, answer) triples. **This is the architectural template
the field still uses: object-centric front-end → learned concept grounding → differentiable symbolic executor.**

Its direct ancestor, usually omitted, is [Neural Module Networks](https://arxiv.org/abs/1511.02799) (Andreas,
Rohrbach, Darrell & Klein, 2015), which parses a question into a layout and dynamically assembles a network from
reusable typed modules — and which stakes out the alternative position that the *executor itself* be neural.

**Two probes followed.** [CLEVRER](https://arxiv.org/abs/1910.01442) (ICLR 2020) added descriptive / explanatory /
predictive / counterfactual questions over collision videos; NS-DR bolted a learned dynamics predictor between
parser and executor. Its numbers are where the pipeline honestly breaks: **88.1% descriptive but 42.2%
counterfactual**. [CLEVR-Hans](https://arxiv.org/abs/2011.12854) (Stammer, Schramowski & Kersting, CVPR 2021)
deliberately confounds classes so a CNN passes validation and collapses on a de-confounded split — and shows that
intervening on a symbolic scene representation ("never use colour") fixes it while pixel saliency cannot even
*name* the bug. **That — semantic-level debuggability under confounding — is the real payoff of symbolic scene
representations, not raw accuracy.**

**The interpretability wing** runs as concept bottleneck models (Koh et al., ICML 2020): predict human-named
concepts, then predict the label only from them, which buys test-time intervention. Mahinpei, Clark, Lage,
Doshi-Velez & Pan, [*Promises and Pitfalls of Black-Box Concept Learning Models*](https://arxiv.org/abs/2106.13314)
(2021), showed the bottleneck **leaks**: soft/joint concept representations smuggle in information beyond the named
concepts. The dispute is live in 2026, with work arguing both that CBMs never had an information bottleneck and
that leakage is sometimes beneficial. There is still no agreed *measurement* of leakage.

**On the perception side**, [Slot Attention](https://proceedings.neurips.cc/paper/2020/hash/8511df98c02ab60aea1b2356c013bc0f-Abstract.html)
(Locatello et al., NeurIPS 2020) is the canonical differentiable "K exchangeable slots" module. Scaling it to real
photos required frozen self-supervised features (DINOSAUR, ICLR 2023), and slot count remains an a-priori
hyperparameter. **There is no accepted method for extracting a reliable symbol table from an arbitrary photograph
— which is what blocks this whole pipeline from leaving synthetic domains.**

**Program induction, two branches.** Bottom-up: [DreamCoder](https://dl.acm.org/doi/10.1145/3453483.3454080)
(Ellis, Wong, Nye, Sablé-Meyer, Cary, Morales, Hewitt, Solar-Lezama & Tenenbaum, PLDI 2021) alternates a wake phase
(neurally-guided enumerative search) with sleep phases that refactor solutions into a growing library of reusable
abstractions. [LILO](https://arxiv.org/abs/2310.19791) (Grand et al., ICLR 2024) replaces enumerative search with
an LLM synthesiser, keeps symbolic compression via Stitch, and auto-documents abstractions so both humans and LLMs
can reuse them. Top-down: [VisProg](https://openaccess.thecvf.com/content/CVPR2023/html/Gupta_Visual_Programming_Compositional_Visual_Reasoning_Without_Training_CVPR_2023_paper.html)
(CVPR 2023 Best Paper) and ViperGPT (ICCV 2023) let an LLM write Python over off-the-shelf vision modules with no
training at all. **That branch has essentially dissolved into LLM tool-use.**

**Abstract reasoning is the hardest testbed.** ARC (Chollet 2019) resists memorisation by construction.
[ARC-AGI-2](https://arxiv.org/abs/2505.11831) (2025) recurated it to resist brute-force program search:
1,000 training / 120 public eval / 120 semi-private / 120 private tasks, calibrated so every task was solved
pass@2 by at least two humans. At release, pure LLMs scored ~0%.

**One canonical ARC table** (from the [ARC Prize 2025 Technical Report](https://arxiv.org/abs/2601.10904),
arXiv:2601.10904, Jan 2026 — 1,455 teams, 15,154 entries, 90 paper submissions):

| System | ARC-AGI-2 | Note |
|---|---|---|
| Top Kaggle entry (NVARC) | **24%** private eval | test-time training + Tiny-Recursive-Model components ⚠ *per-team attribution and $/task are single-source (arcprize.org blog)* |
| Frontier LLM w/ refinement harness | ~54% | at roughly $30/task ⚠ *single-source; the two sources disagree on cost* |
| Tiny Recursive Model (7M params) | 8% | 45% on ARC-AGI-1; **won a paper prize at <0.01% of the parameters of the LLMs it beats** |
| Humans | not published as a single number | ⚠ *no human-baseline percentage appears in either primary source — do not quote one* |

The honest reading: **the winning entries are increasingly small transformers plus test-time training plus
synthetic data, not anything recognisably symbolic.** Chollet's report names "the refinement loop" —
per-task iterative program optimisation — as the defining methodological theme of 2025.

**A completely different route to compositionality** is vector-symbolic architectures / hyperdimensional
computing: Smolensky's tensor products (1990), Plate's Holographic Reduced Representations (1995), Kanerva (2009),
surveyed by Kleyko, Rachkovskij, Osipov & Rahimi in [ACM CSUR](https://arxiv.org/abs/2111.06077). Binding and
superposition as algebra on high-dimensional vectors, with resonator networks doing the un-binding. The flagship
result is Hersche, Zeqiri, Benini, Sebastian & Rahimi,
[*A neuro-vector-symbolic architecture for solving Raven's progressive matrices*](https://www.nature.com/articles/s42256-023-00630-8)
(Nature Machine Intelligence 2023): **87.7% on RAVEN, 88.1% on I-RAVEN**, with probabilistic reasoning two orders
of magnitude faster than comparable symbolic search. Small, coherent, mostly neuromorphic-adjacent community
(IBM Zurich, Redwood/Berkeley), real results, limited reach beyond RPM-shaped tasks.

---

### 3.6 Structure over graphs — knowledge graphs, rule learning, GNN expressiveness

**Be blunt with yourself about what is and isn't neurosymbolic here.**

The first wave — TransE (2013), DistMult (2015), [ComplEx](https://arxiv.org/abs/1606.06357) (2016), RotatE (2019) —
learns one vector per entity and relation plus a fixed scoring function. Nothing is symbolic; the "reasoning" is
bilinear algebra over a lookup table. What makes it *look* symbolic is that the algebraic form decides which
relational patterns are representable at all: TransE's translation collapses symmetric relations to a zero vector;
DistMult's diagonal bilinear form forces symmetry; ComplEx's Hermitian product buys antisymmetry; RotatE's complex
rotation buys symmetry, antisymmetry, inversion and composition at once. Gutiérrez-Basulto & Schockaert (KR 2018)
formalised the harder question — when can a vector-space representation be jointly consistent with a rule base —
with the general answer that you need region/convex semantics, not points.

**The purely symbolic line never died, and this is the most uncomfortable fact in the sub-area.**
[AMIE+](https://doi.org/10.1007/s00778-015-0394-1) mines closed Horn rules with open-world-aware confidence
measures. [AnyBURL](https://doi.org/10.24963/ijcai.2019/435) (Meilicke, Chekol, Ruffinelli & Stuckenschmidt,
IJCAI 2019; VLDB Journal 33(1):131–161, 2024) samples paths bottom-up and generalises them into rules, anytime —
**CPU-only, minutes of training, competitive with heavily tuned embedding models on FB15k-237/WN18RR, and it emits
human-readable rules.** That is either a strong argument for symbolic methods or a strong argument that the
benchmarks reward pattern memorisation. Probably both.

The genuinely neurosymbolic entries are the ones whose *output artifact has logical semantics*: Neural-LP, DRUM,
and [RNNLogic](https://arxiv.org/abs/2010.04029) (ICLR 2021), which treats rules as latent variables with an EM
loop between a rule generator and a reasoning predictor.

**The pivot: path-based GNNs.** [NBFNet](https://arxiv.org/abs/2106.06935) (Zhu, Zhang, Xhonneux & Tang,
NeurIPS 2021) neuralises the Bellman–Ford recursion — pair representations as a generalised sum over paths, each
path a generalised product of edge representations — yielding *source-conditioned* node representations with no
free entity embeddings. That makes it inductive over unseen entities and makes predictions decompose into paths,
i.e. rule-like explanations. [A*Net](https://arxiv.org/abs/2206.04798) (NeurIPS 2023) adds a learned priority
function visiting only ~10% of nodes/edges per iteration, reaching million-scale graphs.
[ULTRA](https://arxiv.org/abs/2310.04562) (Galkin, Yuan, Mostafa, Tang & Zhu, ICLR 2024) removes the last
vocabulary dependence by building relation representations from a graph of relation–relation interactions:
**one pretrained model, zero-shot link prediction on 57 KGs, often on par with or better than per-graph-trained
baselines.** Then Huang, Barceló, Bronstein, Ceylan, Galkin, Reutter & Romero Orth
([ICML 2025](https://arxiv.org/abs/2502.13339)) supply the theory: KGFM expressiveness is governed exactly by the
*motifs* used to build relation representations, and the binary motifs everyone uses are a real ceiling.

**The theory thread is the most honestly logical part.** Barceló, Kostylev, Monet, Pérez, Reutter & Silva,
[*The Logical Expressiveness of Graph Neural Networks*](https://openreview.net/forum?id=r1lZ7AEKvB) (ICLR 2020),
characterises which logical node classifiers message-passing GNNs capture and shows a trivial architectural change
(global readout) changes the logical class. Grohe's
[*The Descriptive Complexity of Graph Neural Networks*](https://arxiv.org/abs/2303.04613) (TheoretiCS vol. 3, 2024)
places GNN-computable queries in (uniform) TC⁰ and a guarded fragment of first-order logic with counting.
**Read these as bounds on what a GNN can *separate*, not as evidence that it deduces.**

**Complex query answering** (GQE → [Query2Box](https://arxiv.org/abs/2002.05969) → BetaE) makes logical operators
geometric or probabilistic. CQD (ICLR 2021) then showed you can skip that entirely: keep a plain ComplEx link
predictor, optimise continuously over the query DAG with t-norms, and gain substantially with far less training
data. **This is the clearest case in the field of symbolic structure beating a learned black box.**

**The 2024–26 mass of the field is LLM+KG, and almost none of it is neurosymbolic.**
[Pan et al.](https://arxiv.org/abs/2306.08302) (IEEE TKDE 2024) is the standard roadmap.
[GraphRAG](https://arxiv.org/abs/2404.16130) (Edge et al., 2024) builds an LLM-extracted entity graph with
community summaries; HippoRAG adds Personalized PageRank; LinkedIn's deployed KG-RAG reports +77.6% MRR and
−28.6% median ticket resolution time. **In all of it the KG is an *index*, not a theory: no inference rule is
applied, no consistency is checked, nothing is entailed.** RoG and Think-on-Graph are closer because they constrain
generation to real KG paths. By 2026 the field is openly asking whether the graph index survives agentic search at
all — see *Do We Still Need GraphRAG?* ([arXiv:2604.09666](https://arxiv.org/abs/2604.09666)), which finds agentic
search narrows the gap on standard QA while GraphRAG retains an edge on multi-hop reasoning.

**Two sub-areas usually missing from NeSy reviews:**

- **Ontology / description-logic embeddings.** Kulmanov, Liu-Wei, Yan & Hoehndorf,
  [*EL Embeddings*](https://arxiv.org/abs/1902.10499) (2019), embed EL++ ontologies into ℝⁿ so concepts become
  n-balls and *the geometry is a model of the theory* — subsumption becomes containment, so the embedding is sound
  with respect to the logic rather than merely correlated with it. Evaluated on protein-protein interaction
  prediction. Successors: Box²EL, TransBox, ALC saturation embeddings. This is simultaneously the semantic-web wing
  and the bioinformatics application.
- **Neural algorithmic reasoning.** Veličković & Blundell, [*Neural Algorithmic Reasoning*](https://arxiv.org/abs/2105.02761)
  (Patterns 2021), operationalised by the [CLRS benchmark](https://arxiv.org/abs/2205.15659) (ICML 2022, 30 classical
  algorithms): train a processor network to imitate an algorithm's step-by-step execution in latent space, then reuse
  it on noisy real inputs. **It answers the symbol-grounding bottleneck differently — don't extract symbols, extract
  the algorithm.** Active through 2025–26 (Discrete NAR, ICML 2025; Tropical Attention, NeurIPS 2025).

---

### 3.7 The LLM era — language models coupled to solvers and provers

**This is where the field's centre of gravity now sits, and where its strongest evidence lives.**

**One architectural move, repeated:** stop asking the language model to *do* the reasoning; ask it to *write down
the problem* in a formal language a sound external engine can decide. The neural part becomes a semantic parser;
the symbolic part becomes the oracle.

#### The 2023 cohort established the pattern across four formalisms

| System | Formal target | Headline |
|---|---|---|
| [Faithful CoT](https://arxiv.org/abs/2301.13379) (Lyu et al.) | mixed | splits Translation / Problem Solving so the visible chain **is by construction** what produced the answer; beats CoT on 9 of 10 benchmarks |
| [Logic-LM](https://arxiv.org/abs/2305.12295) (Pan, Albalak, Wang & Wang, EMNLP Findings 2023) | FOL / CSP / SAT via Z3, Pyke, clingo | **+39.2% over standard prompting, +18.4% over CoT** across ProofWriter, PrOntoQA, FOLIO, LogicalDeduction, AR-LSAT; introduced the solver-error-message repair loop everyone copies |
| [LINC](https://arxiv.org/abs/2310.15164) (Olausson, Gu, Lipkin et al., EMNLP 2023, Outstanding Paper) | first-order logic → Prover9 | **StarCoder+ at 15.5B beats GPT-4-with-CoT by 10 absolute points on ProofWriter** — the parser can be small if the prover is sound |
| [SatLM](https://arxiv.org/abs/2305.09656) (Ye, Chen, Dillig & Durrett, NeurIPS 2023) | declarative spec → SMT | a *declarative* spec sits closer to the problem text than a procedure does; **+23% over program-aided LMs** on a hard GSM subset |
| [LLM + ASP](https://arxiv.org/abs/2307.07696) (Yang, Ishay & Lee, Findings of ACL 2023) | answer set programming | reusable task-independent ASP modules; SOTA on bAbI, StepGame, CLUTRR, gSCAN |

**The recurring finding across all of them: once a formalisation is executable, the solver essentially never errs.
Residual failures concentrate in *translation*.** That single sentence is the most durable result in this
sub-literature.

⚠ *Directionally well supported by LINC, Logic-LM and Ishay et al.; per-category error percentages were not
independently verified, so don't cite a numeric breakdown.*

#### The program-aided line chose Python instead of logic

[PAL](https://arxiv.org/abs/2211.10435) (Gao et al.) and Program-of-Thoughts (Chen et al., TMLR 2023) offload
arithmetic to an interpreter; ToRA (ICLR 2024) trained models on interleaved tool-call trajectories; Toolformer
generalised to self-supervised API use. **By 2025–26 this quietly won: the code interpreter is the de facto
symbolic layer of deployed systems, and "tool use" is the commercial name for LLM-plus-solver.**

#### Formal mathematics — the field's strongest empirical case

- **[AlphaGeometry](https://doi.org/10.1038/s41586-023-06747-5)** (Trinh, Wu, Le, He & Luong, Nature 625(7995):476–482,
  2024): a language model trained on ~100M synthetic theorems proposes auxiliary constructions guiding a symbolic
  deduction engine. **25 of 30 olympiad geometry problems vs 10 for the prior best**, no human proof data.
  AlphaGeometry 2 raised IMO-geometry coverage from 66% to 88%.
- **[AlphaProof](https://doi.org/10.1038/s41586-025-09833-y)** (Hubert, Mehta, Sartran et al., Nature
  651(8106):607–613, epub 12 Nov 2025): AlphaZero-style RL inside Lean over ~80M auto-formalised problems
  (~80,000 TPU-days for the main RL run), with test-time RL generating and training on variants of the target
  problem. **Solved 3 of the 5 non-geometry IMO 2024 problems, including P6 which only 5 human contestants solved;
  with AlphaGeometry 2, 28/42 — silver-medal standard, the first medal-level AI performance at the IMO.**
  This is the most complete neurosymbolic system in the literature: every output is machine-checked by the Lean
  kernel, so correctness does not depend on trusting the model.

Then the open-prover race, one of the fastest benchmark climbs in ML:

| Date | System | miniF2F | PutnamBench |
|---|---|---|---|
| Aug 2024 | DeepSeek-Prover-V1.5 | 63.5% | — |
| Feb 2025 | Goedel-Prover | 57.6% pass@32 | 7 problems |
| Apr 2025 | Kimina-Prover (preview) | 80.7% pass@8192 | — |
| Apr 2025 | DeepSeek-Prover-V2-671B | 88.9% | 49 / 658 |
| Jul 2025 | Seed-Prover | saturates miniF2F | >50%; **5/6 IMO 2025 problems formally proved in Lean** |
| Aug 2025 | Goedel-Prover-V2-32B | 88.1% / 90.4% | 86 problems |
| Dec 2025 | Seed-Prover 1.5 | — | **88%**; 80% Fate-H, 33% Fate-X, 11/12 Putnam 2025 in 9 hours |
| Jun 2026 | [Goedel-Architect](https://arxiv.org/abs/2606.06468) | **99.2% pass@1** (100% w/ NL seeding) | **75.6% pass@1** (88.8%, 597/672, w/ seeding); 4/6 IMO 2025, 3/6 USAMO 2026 |

**Read this table with three caveats.** (a) PutnamBench denominators differ across papers (640 theorems / 1,692
formalisations in the original; 658 and 672 in later work) — cross-paper percentages are not strictly comparable.
(b) pass@1 vs pass@32 vs pass@8192 vs verifier-assisted pass@k are routinely conflated, and none of these numbers
is compute-normalised. (c) **miniF2F is dead as a discriminator.** The bottleneck moved upstream to
*autoformalization* — stating the theorem correctly, not proving it.

#### Are reasoning models neurosymbolic?

The pro argument: in RLVR (named in Tulu 3), the reward comes from a symbolic checker — a math answer-matcher, a
compiler, a test suite — so **the verifier is the symbolic component**. [DeepSeek-R1](https://doi.org/10.1038/s41586-025-09422-z)
(Nature 645(8081):633–638, 2025) showed reasoning behaviour emerges from pure RL against automatically checkable
rewards, with no human-annotated traces.

The contra argument is empirical, and it is worth taking seriously:

- Turpin et al. (NeurIPS 2023) and Lanham et al. show CoT is often **not a faithful account** of the computation,
  and that larger models produce *less* faithful reasoning.
- [GSM-Symbolic](https://arxiv.org/abs/2410.05229) (Mirzadeh, Alizadeh, Shahrokhi, Tuzel, Bengio & Farajtabar,
  ICLR 2025) rebuilds GSM8K from symbolic templates: accuracy varies across instantiations of the same question and
  **drops by up to 65% when one logically inert clause is added.**
- Kambhampati, Valmeekam, Guan et al., [*LLMs Can't Plan, But Can Help Planning in LLM-Modulo Frameworks*](https://arxiv.org/abs/2402.01817)
  (ICML 2024) argues autoregressive models cannot self-verify at all.
- [*The Illusion of Thinking*](https://arxiv.org/abs/2506.06941) (Shojaee, Mirzadeh, Alizadeh, Horton, Bengio &
  Farajtabar, NeurIPS 2025) finds reasoning models collapse to zero accuracy past a complexity threshold while
  *reducing* their reasoning-token budget as problems get harder.
- **And the rebuttal**: [Lawsen](https://arxiv.org/abs/2506.09250) argues the collapse is an experimental artifact —
  Tower of Hanoi failures coincide with output token limits the models explicitly acknowledge, some River Crossing
  instances are provably unsolvable yet scored as failures, and asking for a generating function instead of an
  exhaustive move list restores high accuracy. Two further rebuttals appeared within a month.

**The honest position: this argument rests on a definitional move, not on any demonstration that the model's
internal computation is symbolic, and the empirical picture is methodologically fragile in both directions.**
The Illusion-of-Thinking exchange is itself a good lesson in how brittle negative results about LLM reasoning are.

#### One thing that complicates the tidy narrative

At IMO 2025, Gemini Deep Think scored **35/42 (gold, 5 of 6 problems) end-to-end in natural language inside the
4.5-hour limit**, with no formalisation step. ⚠ *(Verified from DeepMind's blog, not peer review. A parallel OpenAI
claim at 35/42 could not be verified during preparation.)* In the *same* window, Seed-Prover formally proved 5 of
6 of the same problems in Lean. **Both facts are true.** You will see the first cited as evidence that scale beat
the hybrid and the second cited as evidence that the hybrid works; each of those is an editorial reading, not a
finding. What is not in dispute: within one year, the same lab's general model matched its own hybrid's problem
count *and removed the human formalisation step*.

---

### 3.8 RL, planning, and world models

**The unifying idea:** keep a neural network for perception and low-level control, but move the *temporal and
logical structure of the task* into a symbolic object — an automaton, a temporal-logic formula, a program, or a
PDDL domain — that can be inspected, decomposed, verified, or searched over. Four largely separate communities.

**(1) Symbolic task specification.** [Reward machines](https://arxiv.org/abs/2010.03950) (Toro Icarte, Klassen,
Valenzano & McIlraith, ICML 2018; **JAIR 73:173–208, 2022** — read the journal version) replace the opaque scalar
reward with a finite-state machine over a labelling function. Because the learner *sees* the automaton, it can do
counterfactual off-policy updates in every automaton state at once, automated reward shaping, and task
decomposition, with convergence guarantees in the tabular case. Expressive power = regular languages = LTLf/LDLf
over finite traces. LTL2Action (ICML 2021) generalises over combinatorial task sets on the order of 10³⁹ instances.
[Restraining Bolts](https://arxiv.org/abs/1807.06333) (De Giacomo, Iocchi, Favorito & Patrizi, ICAPS 2019) is
conceptually sharpest: the agent's features and the specifier's features are deliberately *different*, so an
authority can constrain an agent it did not design.

**(2) Shielding and safe RL** — covered in §3.4. The recurring cost: shield synthesis needs a symbolic model of the
dynamics and scales badly, which is why almost all evaluations are gridworlds, Pac-Man, or small safety suites.

**(3) Program-structured and relational policies.** [PIRL](https://arxiv.org/abs/1804.02477) (Verma, Murali, Singh,
Kohli & Chaudhuri, ICML 2018) searches a DSL for a program policy using a trained DRL agent as an oracle — the
"neural oracle guides symbolic search" recipe that recurs everywhere. VIPER distils a deep policy into a decision
tree so it can be model-checked. Neural Logic Machines (ICLR 2019) and [NLRL](https://arxiv.org/abs/1904.10729)
(Jiang & Luo, ICML 2019, built on dILP) make the *policy itself* relational so it generalises across object counts
never seen in training — which flat DRL policies do not.

**(4) Symbolic world models.** Classical action-model acquisition (LOCM, FAMA) learns STRIPS/PDDL operators from
traces. Since 2023 the dominant approach is LLM-assisted: Guan, Valmeekam, Sreedharan & Kambhampati
([NeurIPS 2023](https://arxiv.org/abs/2305.14909)) have GPT-4 draft PDDL for 40+ actions, repair it via validators
and human feedback, then hand it to a sound planner. **This relocates the LLM from an unsound plan generator to a
knowledge source whose output is checked by classical machinery, restoring soundness and completeness guarantees.**

**The calibration device you should read.** [PlanBench](https://arxiv.org/abs/2206.10498) (Valmeekam, Marquez,
Olmo, Sreedharan & Kambhampati, NeurIPS 2023 D&B) builds a planning benchmark from IPC domains including
*obfuscated* "Mystery" variants where predicate names are replaced by meaningless tokens — stripping away
commonsense retrieval so only actual state-space search survives. Then Valmeekam, Stechly & Kambhampati
([arXiv:2409.13373](https://arxiv.org/abs/2409.13373)):

| System | Blocksworld | Randomised Mystery Blocksworld | Cost |
|---|---|---|---|
| o1-preview | **97.8%** (587/600) | **37.3%** (224/600) | $42.12 per 100 instances |
| LLaMA 3.1 405B | 62.6% | 0.8% | — |
| Claude 3.5 Sonnet | 54.8% | 0% | — |
| **Fast Downward** (2000s-era planner) | **100%** | **100%** | 0.265 s/instance, ~free |

**These are the most trustworthy quantitative claims in the whole sub-area, precisely because they are negative
results with a classical baseline.**

**Where the symbolic boundary actually sits.** MuZero and DreamerV3 learn latent dynamics and plan inside them, but
the latents carry no compositional or relational commitment — no object identity, no operator preconditions,
nothing a verifier can consume. That, not "learned vs given", is the line. The 2024–26 frontier is precisely about
inventing predicates that cross it: [VisualPredicator](https://arxiv.org/abs/2410.23156) (ICLR 2025 Spotlight)
introduces *neuro-symbolic predicates* whose truth values are computed by calling a VLM on the raw observation, and
invents new ones online when planning fails; OneLife (ICLR 2026) learns dynamics as executable "programmatic laws"
in stochastic environments.

**Deployment reality.** Reward machines, shields, PIRL, VIPER, NLM and NLRL live in gridworlds, Crafter clones,
Atari, small MuJoCo suites and Pac-Man; no production deployment was found. What genuinely runs on hardware is the
LLM-plus-skill-library branch — [SayCan](https://arxiv.org/abs/2204.01691) (CoRL 2022: 101 instructions, 84% plan /
74% execution success on a real office-kitchen robot), [Code as Policies](https://arxiv.org/abs/2209.07753)
(ICRA 2023), and 2026 work like *Build on Priors* ([arXiv:2604.03759](https://arxiv.org/abs/2604.03759)), which
constructs a PDDL domain and matching control policies from 1–30 unannotated demonstrations and runs on a real
industrial forklift — and there the "symbolic" component is a Python program or a PDDL sketch, not anything verified.

---

## 4. State of the art, 2025–2026

**The one-sentence summary: neuro-symbolic AI stopped being mainly a research programme about *architectures* and
became mainly a research programme about *verifiers*.**

arXiv papers matching "neurosymbolic": 39 (2023) → 75 (2024) → 143 (2025) → 115 in Jan–Jul 2026.
⚠ *Keyword match on one spelling only, so it undercounts absolute volume; use it as a trend, not a census. It is
also single-source.* Real growth, decelerating, and the composition has shifted almost entirely from end-to-end
differentiable logic to "LLM proposes, symbolic engine checks."

### 4.1 Formal mathematics: proof of concept, then saturation

Covered in §3.7. In roughly eighteen months the field went from AlphaProof's silver medal to open systems reporting
99.2% pass@1 on miniF2F. **The benchmark died faster than the problem was solved.** The bottleneck is now
autoformalization: ITPEval reports 29.1% pass@1 for statement translation and 10.5% for proof translation, and
miniF2F-Lean itself was audited and found flawed. ⚠ *These two 2026 arXiv IDs could not be independently
re-verified; treat as directional.*

### 4.2 ARC as the public scoreboard

Covered in §3.5. ARC-AGI-3 (launched March 2026) moves to *interactive* environments with no stated goals, testing
exploration, memory and self-set subgoals. Reported humans ~100%, frontier AI <1%. ⚠ *Single-source (arcprize.org).*
Nothing in the current neurosymbolic toolkit — program executors, concept bottlenecks, VSAs — obviously transfers to
that setting, and the refinement-loop trick that carried ARC-AGI-2 does not obviously apply to environments you must
first explore.

### 4.3 The theory wing consolidated on one problem

Reasoning shortcuts is now the most *cumulative* sub-area in the field:

- van Krieken et al. (NeSy 2025) prove the independence assumption means a model **cannot represent uncertainty
  over the concept combinations where shortcuts live — so it cannot even detect that it is taking one.**
- Neurosymbolic Diffusion Models (NeurIPS 2025) is the constructive answer.
- Takemura et al. (KR 2026) formalise shortcut-freeness as a CSP and prove deciding it is **coNP-complete**
  (counting them #P-complete). ⚠ *arXiv:2604.23377 verified only via its abstract page; the KR 2026 acceptance is
  as stated there.*
- [rsbench](https://arxiv.org/abs/2406.10368) (Bortolotti, Marconato, Carraro, Morettin, van Krieken, Vergari,
  Teso & Passerini) is shared benchmark infrastructure — and includes *formal verification procedures that count
  the reasoning shortcuts a given task's constraints admit*.

**A negative result with a decision procedure and a benchmark suite is what maturity looks like.** If you want a
research foothold in classical NeSy, this is where the ground is firmest.

### 4.4 The systems wing made circuits fast

KLay (ICLR 2025), Dolphin (ICML 2025), DeepLog, REASON (HPCA 2026). Note what all of these accelerate: *evaluating*
an already-compiled circuit. **Compilation itself, and the size of the ground provenance formula, are still
CPU-bound and can be exponential in the task.** That is the unattacked half.

[DeepLog](https://arxiv.org/abs/2605.10279) (Manhaeve, Colamonaco, Derkinderen, Adriaensen, Van Praet, De Raedt &
Marra, IJCAI 2026 demo) is the field's admission that a dozen incompatible prototypes was the real adoption
barrier: a PyTorch-native backend compiling multiple NeSy languages to optimised arithmetic circuits. If classical
NeSy ever gets used by ordinary ML practitioners it will be through something like this.

### 4.5 How the community now defines itself

The [RAIL principles](https://arxiv.org/abs/2608.04285) (Chiatti, Cochez, Cornelio, Dumančić, d'Avila Garcez, Lamb,
Morra, Niepert, Peharz, Speranzon, Stol, ten Teije, Thanapalasingam, van Harmelen, van Krieken, Vergari & Wang,
Aug 2026) — a 17-author community position paper proposing **R**easoning, **A**ssurances, **I**nterfacing,
**L**earning as a unified frame, deliberately broad enough to claim AlphaProof and AlphaEvolve.

Read it as both a reasonable reframing *and* a tacit admission that classical NeSy did not win on its own terms.
Where a field draws its boundary tells you where it thinks its legitimacy comes from.

### 4.6 Deployment and funding signals

- **AWS Automated Reasoning checks** in Bedrock Guardrails went GA 6 Aug 2025, claiming "up to 99% verification
  accuracy" for policy-grounded hallucination detection. ⚠ *Vendor claim, no peer review, no named solver beyond
  "SMT-LIB syntax", no named customer in the case study.*
- **Manufacturing**: CausalTrace (AAAI-26 IAAI — a track that specifically vets *deployed* applications), CausalPulse
  at a Robert Bosch plant. ⚠ *Metrics from an arXiv search summary, not fetched abstracts.*
- **Discovery**: [AlphaEvolve](https://arxiv.org/abs/2506.13131) — LLM proposes and mutates programs, an automated
  symbolic evaluator selects them; found a 48-multiplication algorithm for 4×4 complex matrix multiplication, the
  first improvement over Strassen in 56 years, plus data-centre scheduling and circuit improvements. Its
  predecessor [FunSearch](https://www.nature.com/articles/s41586-023-06924-6) (Nature 625:468–475, 2024) is the
  canonical LLM-plus-verifier discovery result. Georgiev, Gómez-Serrano, **Terence Tao** & Wagner then applied the
  loop to 67 open or semi-open problems ([arXiv:2511.02864](https://arxiv.org/abs/2511.02864)) — a working
  mathematician's audit of what neurosymbolic search actually contributes.
- **Funding**: DARPA **ANSR** (Assured Neuro Symbolic Learning and Reasoning, PM Susmit Jha, IPTO, BAA HR001122S0039)
  is the anchor US line. ⚠ *The programme page carries no 2025–26 status update, budget, or performer list.*
  No specific Horizon Europe project could be verified.

### 4.7 Institutions

- **NeSy conference** — 19th edition Sep 2025 (UC Santa Cruz, PMLR vol. 284); 20th edition Lisbon, 1–4 Sep 2026.
  The series began in 2005 as a workshop but has **not** run every year — "annual since 2005" would make 2025 the
  21st. Run by the Neurosymbolic AI Association (nesy-ai.org).
- **IJCLR** — 5th edition Surrey Sep 2025, 6th UPV Valencia Sep 2026; leans inductive logic programming.
- **NeuS** (International Conference on Neuro-symbolic Systems) held a 2026 edition — usually missed in venue lists.
- ***Neurosymbolic Artificial Intelligence*** journal (IOS Press / SAGE, ISSN 2949-8732), open access. ⚠ *Sources
  disagree on the launch year; the journal homepage shows articles from 2024–25 onward. State it carefully.*
- **NeurIPS 2025 had no neurosymbolic-branded workshop** — the reasoning workshops are LLM-centric. That is itself
  a signal about where the attention went.

---

## 5. The honest scorecard

### 5.1 Read the flagship results critically

**NS-VQA's 99.8% on CLEVR.** The strong pure-neural baseline of that era, MAC (Hudson & Manning), was already at
98.9%; FiLM at 97.7%. **So the flagship NeSy vision-reasoning win was ~0.9 points, purchased with program
annotations, on a synthetic benchmark that is now saturated.** This is the single best case study in how to read
this literature.

**MNIST-addition.** See §3.2. Toy at N=2, unsolved at N=15.

**SATNet's visual Sudoku.** Depended on label leakage (Topan, Rolnick & Si, 2021).

### 5.2 The generalization claim has the most instructive arc

SCAN (2018), CFQ (2020) and gSCAN (2020) were built to show seq2seq models fail systematically, and structured/NeSy
methods led for several years. Then neural-only methods largely dissolved them:

- **Least-to-most prompting** (Zhou et al., ICLR 2023) reached **≥99% on all SCAN splits including the length split
  using 14 exemplars**, versus 16% for chain-of-thought — while, in the authors' framing, "specialized
  neural-symbolic models required over 15,000 training examples."
- **Drozdov et al.** set CFQ state of the art at **95.0 mean over MCD1/2/3 using 1% of the training data**, beating
  LeAR's 90.9. ⚠ *Believed ICLR 2023; venue not confirmed.*
- **Lake & Baroni's MLC** (Nature 2023) matched human systematicity with a plain transformer.

**The implication a newcomer should absorb: those benchmarks were measuring a training-distribution deficiency, not
an irreducible architectural one, and the NeSy data-efficiency advantage largely evaporates once a large pretrained
model is the baseline.** Any data-efficiency argument made after 2022 has to answer this.

### 5.3 Reasoning shortcuts are pervasive — and not only in NeSy

rsbench on miniBOIA:

| Model | Label accuracy | **Concept accuracy** |
|---|---|---|
| DeepProbLog | 0.87 | **0.28** |
| Logic Tensor Networks | 0.78 | **0.35** |
| CLIP | 0.99 | **0.34** |

High task scores masking wrong concepts, in neural, neurosymbolic and foundation models alike. **The symbolic layer
does not buy correct concepts.**

### 5.4 Documented methodological problems

- **Solver choice accounts for ~50% of reported variation** in LLM+solver pipelines (Lam, Thatikonda & Shareghi,
  [arXiv:2406.00284](https://arxiv.org/abs/2406.00284)), with an almost linear correlation between tool-executable
  rate and final accuracy. This is the clearest documented case of missing evaluation controls in modern NeSy.
- **The properties the field sells are the least worked on.** Colelough & Regli's PRISMA review
  ([arXiv:2501.05435](https://arxiv.org/abs/2501.05435)) screened 1,428 papers to 167 peer-reviewed, code-backed
  ones for 2020–2024: learning/inference 63%, knowledge representation 44%, logic/reasoning 35%,
  **explainability/trustworthiness 28%, metacognition 5%.**
- **No standard evaluation protocol.** Papers pick their own tasks, baselines and solvers. Nothing analogous to
  GLUE or ImageNet exists; rsbench is the closest candidate and is two years old.
- **The independence assumption is provably harmful** (§3.2) and near-universal.
- **Two careful audits reach different conclusions about which architectural family works best** — Hamilton et al.
  (Semantic Web journal, 2022) found logic-compiled-into-network systems satisfy the most stated NeSy *goals*;
  Chatzikyriakidis & Lappin ([Frontiers in AI 9, article 1797587, 22 May 2026](https://doi.org/10.3389/frai.2026.1797587))
  report that "injective" systems gain 1–2% on general NLU while "federative" ones gain substantially
  (DSR-LM +20%, Logic-LM +39.2%). **Note carefully: these measure different quantities — goal satisfaction vs
  performance gain — so this is not strictly a disagreement.** But the uncomfortable observation stands: the field
  invests most effort in the tightly-coupled paradigms that deliver the least measured gain.

### 5.5 Where the evidence genuinely supports NeSy

Narrower and more specific than the marketing, but real:

1. **Hard constraint satisfaction by construction.** Semantic Probabilistic Layers give perfect constraint
   satisfaction. No amount of scale gives you that.
2. **Verification-in-the-loop formal reasoning.** AlphaGeometry's 25/30 vs 10 is a >2× jump on an externally
   defined problem set — the least-disputed win in the literature. AlphaProof's outputs are Lean-checked.
   Every accepted proof is *machine-verified*.
3. **Auditability and faithfulness by construction.** Faithful CoT and LINC buy faithfulness definitionally,
   for the fragment you can formalise.
4. **Semantic-level debuggability.** CLEVR-Hans: you can say "never use colour" to a symbolic scene
   representation; you cannot say it to a saliency map.
5. **Structured long-horizon control in low-data, energy-constrained regimes.** ⚠ *Suggested by a 2026 robotics
   result (95% vs 34% for a fine-tuned VLA baseline) but that is a single paper on Towers of Hanoi.*
6. **Constrained decoding.** Cheap, real, shipping everywhere.

**Notice the pattern: every item on that list is symbolic *verification or search over neural proposals*, not a
differentiable logic layer.**

### 5.6 The verdict I would give a working data scientist

Treat "neurosymbolic" in 2026 as meaning, in practice, **"put a verifier in the loop."** That pattern is genuinely
useful and now well evidenced. Treat the differentiable-logic literature as a separate, smaller, theoretically
deeper research programme whose main current value to you is its *critique* — knowing why constraint satisfaction
does not imply correct concept grounding transfers to any concept-based or constrained model you build.

And treat any claim that a differentiable logic layer will make your model more data-efficient or more
compositional than a well-prompted frontier model as **unproven until you have run the baseline yourself.**

---

## 6. Open problems worth a researcher's time

Ranked by my read of tractability × importance, with the reason each is stuck.

1. **Reasoning-shortcut mitigation at realistic supervision budgets.** Detection is coNP-complete, counting #P-complete.
   Concept supervision works but is expensive. Bayesian-ensemble (BEARS) and prototype-based approaches are
   demonstrated only at rsbench scale. **Nothing scales to open-vocabulary perception.** This is the firmest ground
   in the field — negative results, a decision procedure, a benchmark — and therefore where incremental work
   compounds.

2. **A fair three-way comparison of ABL vs DeepProbLog vs LTN at matched supervision on a common suite.**
   Nobody has run it. Abduction avoids both #P-hard counting and fuzzy-gradient pathologies by solving a
   consistency problem instead; whether it actually scales better, and why, is unknown. This is an unusually
   cheap, unusually valuable contribution.

3. **Escaping conditional independence affordably.** It is what makes WMC factorise and what makes the model
   structurally unable to flag its own shortcut. Neurosymbolic diffusion is one answer; a general recipe for
   dependent symbol posteriors that keeps inference tractable does not exist.

4. **Autoformalization fidelity.** No scalable way to certify that a generated Lean/FOL/PDDL/SMT statement *means*
   the natural-language problem. A sound prover on a wrong formalisation gives a confidently wrong verified answer.
   This is now the binding constraint on the field's best sub-area.

5. **Compilation, not evaluation.** Every 2024–26 systems paper accelerates evaluating an already-compiled circuit.
   Incremental, amortised or reusable compilation across similar queries is an open gap.

6. **Symbol grounding under noise in RL.** Reward machines, shields and PDDL operators all assume a labelling
   function mapping raw states to ground-truth propositions; in practice that is a learned detector. Recasting it
   as a POMDP is known to be the right move and known not to scale. **This is the single biggest blocker to moving
   off gridworlds.**

7. **Grounding foundation models as probabilistic relations.** Vieira (Li et al., AAAI 2024,
   [arXiv:2412.14515](https://arxiv.org/abs/2412.14515)) makes an LLM callable as a *relation* inside probabilistic
   datalog — the bridge people claim doesn't exist. But LLM probabilities are uncalibrated and mutually dependent,
   violating exactly the conditional-independence assumption WMC requires. Whether calibrated, dependency-aware
   foundation-model predicates can be built at all is the actual obstacle.

8. **Distribution-faithful constrained decoding at production latency.** ASAp converges to the correct conditional
   distribution but needs repeated sampling; GUARD proves autoregressive training alone cannot reach it. **No
   method gives XGrammar-class latency AND distributional fidelity.**

9. **Combinatorics.** Neither AlphaProof nor AlphaGeometry 2 solved either IMO 2024 combinatorics problem
   (AlphaProof: 20.3% on formal-IMO combinatorics vs 75.7% number theory). LLMs aided by symbolic solvers also do
   poorly on first-order combinatorial problems. **This is the clearest remaining gap where a genuinely new hybrid
   could matter.**

10. **Ontology reasoning at scale with sound geometry.** EL++/ALC embeddings give models that satisfy axioms by
    construction, but there is no accepted evaluation separating deductive-closure recovery from statistical link
    prediction, and none handles the expressivity real biomedical ontologies use.

11. **Composition of guarantees.** A schema-valid tool call, a shielded action and a Lean-checked lemma each hold
    locally; nothing composes them into an end-to-end guarantee over a multi-step agent trajectory. Conformal
    monitoring gives marginal coverage, which does not compose across steps.

12. **A benchmark that separates reasoning from knowledge, and is neither saturated nor contaminated.**
    Measuring the thing NeSy claims to fix is itself unsolved.

---

## 7. A reading path

**Sitting 1 — orientation (about 3 hours)**

1. Garcez & Lamb, [*Neurosymbolic AI: The 3rd Wave*](https://arxiv.org/abs/2012.05876) — the field's own account
   and its vocabulary
2. Sarker, Zhou, Eberhart & Hitzler, [*Neuro-symbolic artificial intelligence*](https://doi.org/10.3233/aic-210084)
   (AI Communications 34(3), 2021) — the citable source for Kautz's six types
3. Van Harmelen & ten Teije, [*A Boxology…*](https://arxiv.org/abs/1905.12389) — so you see the taxonomy is contested

**Sitting 2 — the technical map (one weekend)**

4. Marra, Dumančić, Manhaeve & De Raedt, [*From statistical relational to neurosymbolic AI*](https://arxiv.org/abs/2108.11451)
   — the seven-dimension design space. **For a reader with your background this is the highest-value single paper.**
5. Badreddine et al., [*Logic Tensor Networks*](https://arxiv.org/abs/2012.13635) — the complete, teachable
   exposition of logic-as-loss, from t-norms to running code
6. Manhaeve et al., [DeepProbLog](https://proceedings.neurips.cc/paper_files/paper/2018/hash/dc5d637ed5e62c36ecb73b654b05ba2a-Abstract.html)
   — the neural predicate → WMC → differentiable circuit mechanism

**Sitting 3 — the critique (read this before you believe sitting 2)**

7. van Krieken, Acar & van Harmelen, [*Analyzing Differentiable Fuzzy Logic Operators*](https://arxiv.org/abs/2002.06100)
   — which of the operators you just learned actually produce usable gradients
8. Marconato et al., [*Symbol Grounding in NeSy AI: A Gentle Introduction to Reasoning Shortcuts*](https://arxiv.org/abs/2510.14538)
   — the 2026 synthesis of why constraint satisfaction ≠ concept correctness
9. Topan, Rolnick & Si, [*Techniques for Symbol Grounding with SATNet*](https://arxiv.org/abs/2106.11072)
   — the field's cleanest replication failure
10. van Krieken et al., [A-NeSI](https://arxiv.org/abs/2212.12393) — read *the baseline table*; it is the most
    honest scalability data in the field

**Sitting 4 — the LLM era (where the field actually is)**

11. Pan et al., [Logic-LM](https://arxiv.org/abs/2305.12295) — the cleanest statement of the paradigm
12. Olausson et al., [LINC](https://arxiv.org/abs/2310.15164) — the same idea done rigorously, with the error
    analysis showing translation (not proving) is the bottleneck
13. Hubert et al., [AlphaProof](https://doi.org/10.1038/s41586-025-09833-y) (Nature 651:607–613) — the fully
    verified end state, and the compute bill
14. Yang et al., [IJCAI 2025 survey](https://arxiv.org/abs/2508.13678) — the Symbolic→LLM / LLM→Symbolic /
    LLM+Symbolic vocabulary

**Sitting 5 — calibration**

15. Valmeekam, Stechly & Kambhampati, [*LLMs Still Can't Plan; Can LRMs?*](https://arxiv.org/abs/2409.13373) —
    the 97.8%-vs-37.3%-vs-Fast-Downward's-100% table
16. Lake & Baroni, [MLC](https://doi.org/10.1038/s41586-023-06668-3) (Nature 2023) — the strongest evidence
    *against* the field's central premise, which you should be able to argue with
17. Chollet et al., [ARC Prize 2025 Technical Report](https://arxiv.org/abs/2601.10904) — verified 2026 numbers
    with costs, so you can tell hype from result

**Then pick one family from §3 and go deep.** If you want the firmest ground: reasoning shortcuts (§3.1/§4.3).
If you want the most impact: autoformalization (§3.7). If you want the least crowded: abductive learning (§3.3)
or neural algorithmic reasoning (§3.6).

---

## 8. What you can actually run

Maintenance status checked 7–8 Aug 2026 via the GitHub API (last-push dates; these overstate liveness for repos
whose only recent commits are dependency bumps).

**Actively maintained — start here**

| Tool | What it is | Status |
|---|---|---|
| [Scallop](https://github.com/scallop-lang/scallop) | Datalog-based NeSy language, Rust engine, PyTorch bindings, provenance semirings with a top-*k* dial | pushed Jun 2026, 502★, real docs at scallop-lang.org. **Try this first.** |
| [ProbLog](https://github.com/ML-KULeuven/problog) | The probabilistic logic programming substrate | Jun 2026, 416★ |
| [PyReason](https://github.com/lab-v2/pyreason) | Open-world temporal logic over knowledge graphs with explainable traces | Jul 2026, 345★ |
| [IBM LNN](https://github.com/IBM/LNN) | Logical Neural Networks | Jul 2026, 325★ |
| [PyNeuraLogic](https://github.com/LukasZahradnik/PyNeuraLogic) | Lifted relational neural networks | Aug 2026, 312★ |
| [NeurASP](https://github.com/azreasoners/NeurASP) | Neural networks inside answer set programming | Jul 2026, 54★ |
| [DomiKnowS](https://github.com/HLR/DomiKnowS) | Declarative constraint integration | Aug 2026, 50★ |

**The unbranded symbolic layer you probably already use** — Z3 (12.5k★), clingo (817★), PySAT (460★),
Lean/mathlib4 (3.8k★, daily commits), [LeanDojo](https://github.com/lean-dojo/LeanDojo) (824★, turns Lean into a
Python-callable gym), SymPy, cvc5.

**Constrained decoding — the most-deployed NeSy mechanism** — [outlines](https://github.com/dottxt-ai/outlines)
(15.5k★), [XGrammar](https://github.com/mlc-ai/xgrammar) (1.8k★, default backend for vLLM/SGLang/TensorRT-LLM),
[llguidance](https://github.com/guidance-ai/llguidance) (830★). All three pushed within days of Aug 2026.

**Reference code only — do not build on these**

DeepProbLog (last push Aug 2024, 351★ — effectively frozen; KU Leuven's effort moved to DeepLog),
LTNtorch (Oct 2024, 41★), Pylon (Jan 2024, 122★ — abandoned), UCLA Semantic-Loss (2019, 63★ — abandoned),
Logic-LM (Jun 2024, 404★ — baselines are GPT-3.5/GPT-4-era), Juice/ProbabilisticCircuits.jl (Jun 2024, 106★).

**Benchmarks worth running** — [rsbench](https://unitn-sml.github.io/rsbench/) (concept quality + shortcut
counting; run it before you believe any NeSy interpretability claim), MNIST-Addition (via DeepProbLog),
CLEVR-Hans3/7, FOLIO (1,430 examples over 487 premise sets), ProofWriter, PrOntoQA, PlanBench/Blocksworld,
ARC-AGI-2, miniF2F + PutnamBench (1,692 formalisations of 640 theorems), ZebraLogic, ROAD-R.

**Teaching material** — the [`neurosym`](https://github.com/kavigupta/neurosym-lib) library accompanying
Chaudhuri, Ellis, Polozov, Singh, Solar-Lezama & Yue's *Neurosymbolic Programming* monograph (Foundations and
Trends in Programming Languages, 2021 ⚠ *volume/pages unconfirmed — nowpublishers returns 403*); the
ScaDS.AI School on Neuro+Symbolic AI (Leipzig, June 2026).

**The honest signal in this table:** the branded NeSy libraries are thinly maintained while the tools practitioners
actually run every day are the unbranded symbolic layer. Treat the branded frameworks as research artifacts, with
Scallop, ProbLog, PyReason, PyNeuraLogic and IBM's LNN as the genuine exceptions.

---

## 9. Positioning yourself

Three observations that follow from everything above.

**The field's centre of gravity has left the field.** The highest-profile neuro-symbolic results of 2024–26 —
AlphaGeometry, AlphaProof, AlphaEvolve — came from DeepMind, not from NeSy regulars, and sit in Kautz's *loosest*
categories. Meanwhile the tightly-coupled differentiable-logic research the founders cared about is small-scale and
benchmark-bound. If you want impact, the LLM+verifier side is where it is. If you want depth and uncrowded ground,
the classical side has firmer theory and a clearer notion of what would count as progress.

**The best work in this field right now is self-critical.** Reasoning shortcuts, the independence-assumption proof,
rsbench, honest timeout tables, the SATNet replication — these came from inside the community, and they are the
results that have held up. That is what a maturing subfield looks like. It also means the highest-leverage
contribution a careful empiricist can make is often an evaluation, not a method.

**Your comparative advantage as a data scientist is the baseline.** The single most common defect in this
literature is a NeSy method compared against a from-scratch neural model on a synthetic task. Where anyone has
redone the comparison against a strong pretrained baseline — SCAN with 14 exemplars, CFQ with 1% of the data,
MLC — the advantage disappeared. **Running the baseline properly is a publishable contribution in this field,
which tells you something about the field.**

---

*Full annotated bibliography, grouped by theme with verification status: [bibliography.md](bibliography.md)*
