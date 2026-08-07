# Neuro-Symbolic AI — Annotated Bibliography

Companion to [neurosymbolic_ai_literature_review.md](neurosymbolic_ai_literature_review.md).
Grouped by theme, roughly chronological within each group.

**Verification convention.** Every entry was checked against a bibliographic source (arXiv API, OpenAlex, dblp,
or a publisher page). Entries carrying **⚠** have some element that could not be confirmed — the note says which.
Entries marked **[corrected]** had a metadata error in circulation that has been fixed here; the correction is
stated. Roughly 75 citations were independently adjudicated in a dedicated audit pass: **zero fabrications, zero
invented first authors, zero invented venues** were found; 12 metadata errors were.

---

## 1. Foundations and history

- **McCulloch, W.S. & Pitts, W.** (1943). *A logical calculus of the ideas immanent in nervous activity.*
  Bulletin of Mathematical Biophysics 5:115–133. [link](https://link.springer.com/article/10.1007/BF02478259)
  — Neurons as threshold logic units; networks realise arbitrary propositional logic. The first neural network was
  a logic machine, which is why NeSy frames itself as reunification.

- **Fodor, J.A. & Pylyshyn, Z.W.** (1988). *Connectionism and cognitive architecture: A critical analysis.*
  Cognition 28(1–2):3–71. [link](https://www.sciencedirect.com/science/article/abs/pii/0010027788900315)
  — The systematicity challenge. Every compositional-generalization benchmark descends from this argument.

- **Smolensky, P.** (1988). *On the proper treatment of connectionism.* Behavioral and Brain Sciences 11:1–23.

- **Smolensky, P.** (1990). *Tensor Product Variable Binding and the Representation of Symbolic Structures in
  Connectionist Systems.* Artificial Intelligence 46(1–2):159–216. [dblp](https://dblp.org/rec/journals/ai/Smolensky90.html)
  — Exact, invertible variable binding inside a vector space. Ancestor of all vector-symbolic architectures.
  *[corrected]* Title ends "Connectionist **Systems**", not "Networks" (several citation lists have this wrong).

- **Towell, G.G. & Shavlik, J.W.** (1994). *Knowledge-Based Artificial Neural Networks (KBANN).*
  Artificial Intelligence 70(1–2):119–165. [dblp](https://dblp.org/rec/journals/ai/TowellS94.html)
  — Compile a propositional domain theory into network topology and weights, then refine by backprop.
  The template for all knowledge injection.

- **Valiant, L.G.** (2000). *Robust logics.* Artificial Intelligence 117(2):231–253.
  DOI 10.1016/S0004-3702(00)00002-3. (STOC 1999 predecessor at pp. 642–651.)

- **Valiant, L.G.** (2003). *Three problems in computer science.* JACM 50(1):96–99.
  [link](https://dl.acm.org/doi/10.1145/602382.602410)
  — Names reconciling statistical learning with logical reasoning as a grand challenge. The field's
  most-cited legitimacy argument.

- **d'Avila Garcez, A., Lamb, L.C. & Gabbay, D.M.** (2009). *Neural-Symbolic Cognitive Reasoning.*
  Springer, Cognitive Technologies series. — Neural encodings of modal, temporal, epistemic and intuitionistic
  logics with a general translation-and-extraction methodology.

- **Sun, R.** (2024). *Dual-process theories, cognitive architectures, and hybrid neural-symbolic models.*
  Neurosymbolic Artificial Intelligence vol. 1. DOI 10.3233/NAI-240720. *[corrected]* OpenAlex dates this **2024**,
  not 2025. — Argues modern System-1/System-2 enthusiasm rediscovers 1990s CLARION-era principles.
  ⚠ Sun's CONSYDERR book (Wiley 1994) could not be verified and is omitted.

---

## 2. Position papers, taxonomies and surveys

- **Marcus, G.** (2018). *Deep Learning: A Critical Appraisal.* [arXiv:1801.00631](https://arxiv.org/abs/1801.00631)
- **Marcus, G.** (2020). *The Next Decade in AI: Four Steps Towards Robust Artificial Intelligence.*
  [arXiv:2002.06177](https://arxiv.org/abs/2002.06177)
- **Chollet, F.** (2019). *On the Measure of Intelligence.* [arXiv:1911.01547](https://arxiv.org/abs/1911.01547)
  — Intelligence as skill-acquisition efficiency relative to priors; introduces ARC.
- **van Harmelen, F. & ten Teije, A.** (2019). *A Boxology of Design Patterns for Hybrid Learning and Reasoning
  Systems.* Journal of Web Engineering 18(1–3):97–124. [arXiv:1905.12389](https://arxiv.org/abs/1905.12389)
  — The principal competitor to Kautz's taxonomy; compositional where Kautz is a single ordinal scale.
- **d'Avila Garcez, A. & Lamb, L.C.** (2020). *Neurosymbolic AI: The 3rd Wave.*
  [arXiv:2012.05876](https://arxiv.org/abs/2012.05876); Artificial Intelligence Review 2023,
  DOI 10.1007/s10462-023-10448-w. — The field's self-definition document.
- **Sarker, M.K., Zhou, L., Eberhart, A. & Hitzler, P.** (2021). *Neuro-symbolic artificial intelligence.*
  AI Communications 34(3):197–209. [DOI](https://doi.org/10.3233/aic-210084)
  *[corrected]* The published journal title is *Neuro-symbolic artificial intelligence*; "…: Current Trends" is the
  arXiv:2105.05330 **preprint** title only. Issue number is 3. **This is the safe citation for the Kautz taxonomy.**
- **Kautz, H.A.** (2022). *The Third AI Summer: AAAI Robert S. Engelmore Memorial Lecture.*
  AI Magazine 43(1):93–104. [DOI 10.1609/aimag.v43i1.19122](https://doi.org/10.1609/aimag.v43i1.19122)
  *[corrected]* dblp gives 43(1):**93–104**; the widely-circulated "43(1):105–125 / DOI 10.1002/aaai.12036" variant
  has the wrong page range. ⚠ **The six-type taxonomy could not be verified against the printed text** (Wiley
  returns HTTP 402; AAAI OJS errors). Cite Sarker et al. 2021 for the taxonomy itself.
- **Hamilton, K., Nayak, A., Božić, B. & Longo, L.** (2022). *Is Neuro-Symbolic AI Meeting its Promise in Natural
  Language Processing? A Structured Review.* Semantic Web journal, DOI 10.3233/SW-223228.
  [arXiv:2202.12205](https://arxiv.org/abs/2202.12205) — Audits five claimed NeSy goals against published NLP systems.
- **Giunchiglia, E., Stoian, M.C. & Lukasiewicz, T.** (2022). *Deep Learning with Logical Constraints.*
  IJCAI 2022 survey track, pp. 5478–5485. [arXiv:2205.00523](https://arxiv.org/abs/2205.00523)
  — The best map of the constraint terrain; makes the soft/hard axis explicit.
- **Goyal, A. & Bengio, Y.** (2022). *Inductive biases for deep learning of higher-level cognition.*
  Proc. R. Soc. A 478(2266):20210068. [arXiv:2011.15091](https://arxiv.org/abs/2011.15091)
  — The citable proxy for the System-1/System-2 framing. ⚠ Bengio's NeurIPS 2019 keynote has no citable published record.
- **LeCun, Y.** (2022). *A Path Towards Autonomous Machine Intelligence,* v0.9.2.
  [OpenReview](https://openreview.net/forum?id=BZ5a1r-kVsf)
- **Hitzler, P., Sarker, M.K. & Eberhart, A.** (eds.) (2023). *Compendium of Neurosymbolic Artificial Intelligence.*
  IOS Press, Frontiers in AI and Applications vol. 369. *[corrected]* The publisher page shows **24 chapters**
  running to page 546 — the "704 pp., 30 chapters" figure in circulation is unsupported. Predecessor:
  *Neuro-Symbolic Artificial Intelligence: The State of the Art,* FAIA vol. 342 ⚠ (publisher says 2021, commonly
  cited as 2022 — unresolved).
- **Chaudhuri, S., Ellis, K., Polozov, O., Singh, R., Solar-Lezama, A. & Yue, Y.** (2021). *Neurosymbolic
  Programming.* Foundations and Trends in Programming Languages 7(3):158–243. ⚠ Volume/issue/pages unverified
  (nowpublishers returns 403; not indexed under that title in OpenAlex). The monograph is real; the locator is not
  confirmed. Teaching library: `pip install neurosym`.
- **Marra, G., Dumančić, S., Manhaeve, R. & De Raedt, L.** (2024). *From statistical relational to neurosymbolic
  artificial intelligence: A survey.* Artificial Intelligence 328:104062.
  [arXiv:2108.11451](https://arxiv.org/abs/2108.11451) — **The best technical map for an ML reader.** Seven design
  dimensions. Every volume/page detail verified.
- **Wang, W., Yang, Y. & Wu, F.** (2024). *Towards Data- and Knowledge-Driven Artificial Intelligence: A Survey on
  Neuro-Symbolic Computing.* IEEE TPAMI. [arXiv:2210.15889](https://arxiv.org/abs/2210.15889)
  — The highest-visibility non-Western synthesis; partitions the field differently.
- **DeLong, L.N., Fernández Mir, R. & Fleuriot, J.D.** (2025). *Neurosymbolic AI for Reasoning over Knowledge
  Graphs: A Survey.* IEEE TNNLS 36(5):7822–7842. [arXiv:2302.07200](https://arxiv.org/abs/2302.07200)
  — Useful precisely because it forces the neurosymbolic-vs-graph-ML distinction.
- **Colelough, B.C. & Regli, W.** (2025). *Neuro-Symbolic AI in 2024: A Systematic Review.*
  [arXiv:2501.05435](https://arxiv.org/abs/2501.05435) — PRISMA review, 1,428 papers screened to 167 peer-reviewed
  and code-backed. Learning/inference 63%, KR 44%, logic/reasoning 35%, explainability/trust 28%, metacognition 5%.
- **Velasquez, A., Bhatt, N., Topcu, U., Wang, Z., Sycara, K., Stepputtis, S., Neema, S. & Vallabha, G.** (2025).
  *Neurosymbolic AI as an antithesis to scaling laws.* PNAS Nexus 4(5):pgaf117.
  [link](https://academic.oup.com/pnasnexus/article/4/5/pgaf117/8134151)
  *[corrected]* Second author is **Neel** Bhatt, not "Nikhil". Efficiency claims traced: "100× smaller than GPT-3"
  → West et al. 2022; "0.1% training time / 1% data / 96.9% fewer parameters" → Zhao et al. 2024 (physics-informed
  autonomous driving) — domain-specific, not general.
- **Yang, X.-W., Shao, J.-J., Guo, L.-Z., Zhang, B.-W., Zhou, Z., Jia, L.-H., Dai, W.-Z. & Li, Y.-F.** (2025).
  *Neuro-Symbolic Artificial Intelligence: Towards Improving the Reasoning Abilities of Large Language Models.*
  IJCAI 2025 Survey Track, pp. 10770–10778. [arXiv:2508.13678](https://arxiv.org/abs/2508.13678)
  — The Symbolic→LLM / LLM→Symbolic / LLM+Symbolic taxonomy. Companion repo: LAMDA-NeSy/Awesome-LLM-Reasoning-with-NeSy.
- **De Smet, L. & De Raedt, L.** (2025). *Defining neurosymbolic AI.*
  [arXiv:2507.11127](https://arxiv.org/abs/2507.11127)
- **Chatzikyriakidis, S. & Lappin, S.** (2026). *Neuro-symbolic NLP: taxonomy, assessment, and directions.*
  Frontiers in Artificial Intelligence, vol. 9, article 1797587, published 22 May 2026.
  [DOI](https://doi.org/10.3389/frai.2026.1797587) — Injective vs federative × five interaction modes. Reports
  injective systems gaining 1–2% on general NLU vs substantial gains for federative ones.
- **Chiatti, A., Cochez, M., Cornelio, C., Dumančić, S., d'Avila Garcez, A., Lamb, L.C., Morra, L., Niepert, M.,
  Peharz, R., Speranzon, A., Stol, M., ten Teije, A., Thanapalasingam, T., van Harmelen, F., van Krieken, E.,
  Vergari, A. & Wang, B.** (2026). *The RAIL Principles for Neurosymbolic AI.*
  [arXiv:2608.04285](https://arxiv.org/abs/2608.04285) — 17-author community position paper; deliberately broad
  enough to claim AlphaProof and AlphaEvolve.

---

## 3. Fuzzy / differentiable logic (logic as a loss or a layer)

- **Diligenti, M., Gori, M. & Saccà, C.** (2015 online / 2017 print). *Semantic-based regularization for learning
  and inference.* Artificial Intelligence 244:143–165. [DOI](https://doi.org/10.1016/j.artint.2015.08.011)
  *[corrected]* Volume and pages confirmed; the DOI stamps it **2015 online-first** — "2017" is the print-issue year.
- **Rocktäschel, T. & Riedel, S.** (2017). *End-to-End Differentiable Proving.* NIPS 2017.
  [arXiv:1705.11040](https://arxiv.org/abs/1705.11040) — Unrolls Prolog backward chaining, replaces unification with
  an RBF kernel on symbol embeddings. Beautiful; the proof tree explodes.
- **Yang, F., Yang, Z. & Cohen, W.W.** (2017). *Differentiable Learning of Logical Rules for Knowledge Base
  Reasoning (Neural LP).* NIPS 2017. [arXiv:1702.08367](https://arxiv.org/abs/1702.08367)
- **Evans, R. & Grefenstette, E.** (2018). *Learning Explanatory Rules from Noisy Data (dILP).*
  JAIR 61:1–64, [DOI 10.1613/jair.5714](https://doi.org/10.1613/jair.5714); IJCAI 2018 extended abstract
  pp. 5598–5602. Volume and pages verified.
- **Xu, J., Zhang, Z., Friedman, T., Liang, Y. & Van den Broeck, G.** (2018). *A Semantic Loss Function for Deep
  Learning with Symbolic Knowledge.* ICML 2018, PMLR 80.
  [link](https://proceedings.mlr.press/v80/xu18h.html) — The cheapest on-ramp: one extra loss term.
- **Fischer, M., Balunović, M., Drachsler-Cohen, D., Gehr, T., Zhang, C. & Vechev, M.** (2019).
  *DL2: Training and Querying Neural Networks with Logic.* ICML 2019.
  [PDF](https://files.sri.inf.ethz.ch/website/papers/icml19-dl2.pdf) — Non-fuzzy translation; loss exactly zero when
  satisfied. ⚠ PMLR page not fetched.
- **Marra, G., Giannini, F., Diligenti, M. & Gori, M.** (2019). *LYRICS: a General Interface Layer to Integrate
  Logic Inference and Deep Learning.* ECML-PKDD 2019. [arXiv:1903.07534](https://arxiv.org/abs/1903.07534)
  ⚠ Pagination unconfirmed; 2019 (conference) vs 2020 (proceedings print) ambiguous.
- **Riegel, R., Gray, A., Luus, F., Khan, N., Makondo, N., Akhalwaya, I., Qian, H., Fagin, R., Barahona, F.,
  Sharma, U., Ikbal, S., Karanam, H., Neelam, S., Likhyani, S. & Srivastava, S.** (2020). *Logical Neural Networks.*
  [arXiv:2006.13155](https://arxiv.org/abs/2006.13155) — Full 15-author list verified. The arXiv comment reads
  "In submission to NeurIPS 2020"; it was **never formally published there** — cite as arXiv 2020.
- **van Krieken, E., Acar, E. & van Harmelen, F.** (2022). *Analyzing Differentiable Fuzzy Logic Operators.*
  Artificial Intelligence 302:103602. [arXiv:2002.06100](https://arxiv.org/abs/2002.06100)
  — **The single most important negative result in the sub-area.** Most canonical operators are unusable; the
  best-performing combinations violate ordinary logical laws.
- **Serafini, L. & d'Avila Garcez, A.** (2016). *Logic Tensor Networks: Deep Learning and Logical Reasoning from
  Data and Knowledge.* [arXiv:1606.04422](https://arxiv.org/abs/1606.04422) — Verified; restore this to reading lists.
- **Badreddine, S., d'Avila Garcez, A., Serafini, L. & Spranger, M.** (2022). *Logic Tensor Networks.*
  Artificial Intelligence 303:103649. [arXiv:2012.13635](https://arxiv.org/abs/2012.13635)
  — 68 pages, worked examples across seven task types. **The definitive teachable reference.**
  PyTorch port: LTNtorch (Carraro, Serafini & Aiolli, [arXiv:2409.16045](https://arxiv.org/abs/2409.16045))
  ⚠ *[corrected]* author order is Carraro, **Serafini, Aiolli**; the claimed JMLR/MLOSS publication is unverified.
- **Petersen, F., Borgelt, C., Kuehne, H. & Deussen, O.** (2022). *Deep Differentiable Logic Gate Networks.*
  NeurIPS 2022. [arXiv:2210.08277](https://arxiv.org/abs/2210.08277) — >1M MNIST images/sec on one CPU core.
- **Ciravegna, G., Barbiero, P., Giannini, F., Gori, M., Lió, P., Maggini, M. & Melacci, S.** (2022).
  *Logic Explained Networks.* Artificial Intelligence, article 103822, DOI 10.1016/j.artint.2022.103822.
  [arXiv:2108.05149](https://arxiv.org/abs/2108.05149) *[corrected]* Year is **2022**, not 2023; full seven-author
  list confirmed verbatim.
- **Petersen, F., Kuehne, H., Borgelt, C., Welzel, J. & Ermon, S.** (2024). *Convolutional Differentiable Logic
  Gate Networks.* NeurIPS 2024 (Oral).
  [proceedings](https://proceedings.neurips.cc/paper_files/paper/2024/hash/db988b089d8d97d0f159c15ed0be6a71-Abstract-Conference.html)
  — **86.29% CIFAR-10, 61M logic gates, 29× smaller than prior SOTA** (all verbatim from the abstract).
  *[corrected]* The "4 nanosecond inference" and "29×–61×" figures are **not in the paper** — they came from a
  social-media post. Drop them.
- **Yousefi, S., Plesner, A., Aczel, T. & Wattenhofer, R.** (2025). *Mind the Gap: Removing the Discretization Gap
  in Differentiable Logic Gate Networks.* **NeurIPS 2025 (main track)** — venue upgraded during audit.
  [arXiv:2506.07500](https://arxiv.org/abs/2506.07500) ⚠ The "4.5× faster training / 98% gap reduction" figures
  remain unverified.
- **Ślusarz, N., Komendantskaya, E., Daggitt, M., Stewart, R. & Stark, K.** (2023). *Logic of Differentiable
  Logics.* LPAR 2023. [arXiv:2303.10650](https://arxiv.org/abs/2303.10650)
  — Supplies formal semantics for differentiable logics and targets *provable specification satisfaction* rather
  than accuracy — a different objective most reviews of this area never consider.
- **van Krieken, E.** (2024). *Optimisation in Neurosymbolic Learning Systems.* PhD dissertation.
  [arXiv:2401.10819](https://arxiv.org/abs/2401.10819) — Verified; safe to cite.

### Rule learning (the differentiable-ILP branch)

- **Minervini, P., Riedel, S., Stenetorp, P., Grefenstette, E. & Rocktäschel, T.** (2020). *Learning Reasoning
  Strategies in End-to-End Differentiable Proving.* ICML 2020. [arXiv:2007.06477](https://arxiv.org/abs/2007.06477)
  *[corrected]* **This is the paper title.** "Conditional Theorem Provers" is the *method* name and must not be used
  as the title — a very common miscitation. ⚠ PMLR pagination unverified.
- **Sadeghian, A., Armandpour, M., Ding, P. & Wang, D.Z.** (2019). *DRUM: End-To-End Differentiable Rule Mining on
  Knowledge Graphs.* [arXiv:1911.00055](https://arxiv.org/abs/1911.00055) ⚠ NeurIPS 2019 venue from background,
  not from the arXiv page.
- **Qu, M., Chen, J., Xhonneux, L.-P., Bengio, Y. & Tang, J.** (2021). *RNNLogic: Learning Logic Rules for Reasoning
  on Knowledge Graphs.* ICLR 2021. [arXiv:2010.04029](https://arxiv.org/abs/2010.04029)

---

## 4. Probabilistic NeSy — weighted model counting, knowledge compilation, circuits

- **Darwiche, A. & Marquis, P.** (2002). *A Knowledge Compilation Map.* JAIR 17:229–264.
  [arXiv:1106.1819](https://arxiv.org/abs/1106.1819) — Decomposability + determinism ⇒ linear-time model counting.
  **The theory that makes the whole sub-area possible.**
- **Richardson, M. & Domingos, P.** (2006). *Markov logic networks.* Machine Learning 62(1–2):107–136.
  [link](https://link.springer.com/article/10.1007/s10994-006-5833-1) — The instructive failure case: undirected,
  so no compact differentiable circuit.
- **De Raedt, L., Kimmig, A. & Toivonen, H.** (2007). *ProbLog: A Probabilistic Prolog and its Application in Link
  Discovery.* IJCAI 2007, pp. 2462–2467. — The distribution semantics everything else varies on.
- **Poon, H. & Domingos, P.** (2011). *Sum-Product Networks: A New Deep Architecture.* UAI 2011. ⚠ Not fetched.
- **Kisa, D., Van den Broeck, G., Choi, A. & Darwiche, A.** (2014). *Probabilistic Sentential Decision Diagrams.*
  KR 2014. ⚠ Not fetched.
- **Fierens, D., Van den Broeck, G., Renkens, J., Shterionov, D., Gutmann, B., Thon, I., Janssens, G. &
  De Raedt, L.** (2015). *Inference and learning in probabilistic logic programs using weighted Boolean formulas.*
  TPLP 15(3):358–401. [DOI](https://doi.org/10.1017/s1471068414000076) — Confirmed exactly as cited.
  **The single most load-bearing citation in this thread.**
- **Manhaeve, R., Dumančić, S., Kimmig, A., Demeester, T. & De Raedt, L.** (2018). *DeepProbLog: Neural
  Probabilistic Logic Programming.* NeurIPS 2018, pp. 3753–3763.
  [proceedings](https://proceedings.neurips.cc/paper_files/paper/2018/hash/dc5d637ed5e62c36ecb73b654b05ba2a-Abstract.html)
  Journal version: *Neural probabilistic logic programming in DeepProbLog,* Artificial Intelligence vol. 298,
  **article 103504** (2021), [DOI](https://doi.org/10.1016/j.artint.2021.103504).
  *[corrected]* The locator is article number **103504**, not "pages 103–504" — confirmed mangling.
  Origin of MNIST-addition.
- **Yang, Z., Ishay, A. & Lee, J.** (2020). *NeurASP: Embracing Neural Networks into Answer Set Programming.*
  IJCAI 2020. [PDF](https://www.ijcai.org/proceedings/2020/0243.pdf)
- **Huang, J., Li, Z., Chen, B., Samel, K., Naik, M., Song, L. & Si, X.** (2021). *Scallop: From Probabilistic
  Deductive Databases to Scalable Differentiable Reasoning.* NeurIPS 2021, pp. 25134–25145.
  — Top-*k*-proofs provenance. VQA margins of **+12.42%** over neural-module-network and **+21.66%** over
  transformer baselines, both verified verbatim.
- **Ahmed, K., Teso, S., Chang, K.-W., Van den Broeck, G. & Vergari, A.** (2022). *Semantic Probabilistic Layers
  for Neuro-Symbolic Learning.* NeurIPS 2022. [arXiv:2206.00426](https://arxiv.org/abs/2206.00426)
  — Constraint circuit × probabilistic circuit, exactly renormalised. **The reference guarantee layer.**
- **Winters, T., Marra, G., Manhaeve, R. & De Raedt, L.** (2022). *DeepStochLog: Neural Stochastic Logic
  Programming.* AAAI 2022 36(9):10090–10100.
- **Aspis, Y., Broda, K., Lobo, J. & Russo, A.** (2022). *Embed2Sym.* KR 2022.
- **Li, Z., Huang, J. & Naik, M.** (2023). *Scallop: A Language for Neurosymbolic Programming.*
  PACMPL 7(PLDI):**1463–1487**, [DOI 10.1145/3591280](https://doi.org/10.1145/3591280).
  *[corrected]* Pages per OpenAlex; the frequently cited "Article 166" is unverified.
  ⚠ Lead author is **Ziyang Li** (UPenn) — commonly misattributed.
- **Pryor, C., Dickens, C., Augustine, E., Albalak, A., Wang, W. & Getoor, L.** (2023). *NeuPSL: Neural
  Probabilistic Soft Logic.* IJCAI 2023. [arXiv:2205.14268](https://arxiv.org/abs/2205.14268) ⚠ Claims from abstract summary only.
- **van Krieken, E., Thanapalasingam, T., Tomczak, J.M., van Harmelen, F. & ten Teije, A.** (2023).
  *A-NeSI: A Scalable Approximate Method for Probabilistic Neurosymbolic Inference.* NeurIPS 2023.
  [arXiv:2212.12393](https://arxiv.org/abs/2212.12393) — Learned surrogates for the counting step. **Its baseline
  table is the most honest scalability data in the field:** DeepProbLog 97.20% (N=1), 95.20% (N=2), timeout (N=4);
  A-NeSI 75.90 ± 2.21 at N=15.
- **van Krieken, E., Minervini, P., Ponti, E.M. & Vergari, A.** (2024). *On the Independence Assumption in
  Neurosymbolic Learning.* ICML 2024, PMLR 235:49078–49097. [arXiv:2404.08458](https://arxiv.org/abs/2404.08458)
- **Maene, J., Derkinderen, V. & De Raedt, L.** (2024). *On the Hardness of Probabilistic Neurosymbolic Learning.*
  [arXiv:2406.04472](https://arxiv.org/abs/2406.04472) — Introduces WeightME, an unbiased gradient estimator using
  a logarithmic number of SAT calls. ⚠ Suspected ICML 2024; venue unconfirmed.
- **Liu, A., Ahmed, K. & Van den Broeck, G.** (2024). *Scaling Tractable Probabilistic Circuits: A Systems
  Perspective* (PyJuice). [arXiv:2406.00766](https://arxiv.org/abs/2406.00766) — Authors confirmed.
  ⚠ Venue and speedup figures unverified.
- **Maene, J., Derkinderen, V. & Zuidberg Dos Martires, P.** (2025). *KLay: Accelerating Arithmetic Circuits for
  Neurosymbolic AI.* ICLR 2025. [arXiv:2410.11415](https://arxiv.org/abs/2410.11415)
- **Naik, A., Liu, J., Wang, C., Sethi, A., Dutta, S., Naik, M. & Wong, E.** (2025). *Dolphin: A Programmable
  Framework for Scalable Neurosymbolic Learning.* ICML 2025, PMLR 267:45461–45483.
  [arXiv:2410.03348](https://arxiv.org/abs/2410.03348) — **1.71×–62× speedups over 13 benchmarks**; converges where
  Scallop, ISED and IndeCateR+ do not.
- **van Krieken, E., Minervini, P., Ponti, E.M. & Vergari, A.** (2025). *Neurosymbolic Diffusion Models.*
  NeurIPS 2025. [arXiv:2505.13138](https://arxiv.org/abs/2505.13138)
- **Derkinderen, V., Manhaeve, R., Adriaensen, R., Van Praet, L., De Smet, L., Marra, G. & De Raedt, L.** (2025/26).
  *The DeepLog Neurosymbolic Machine.* [arXiv:2508.13697](https://arxiv.org/abs/2508.13697); demo paper
  *DeepLog: A Software Framework for Modular Neurosymbolic AI,* IJCAI 2026,
  [arXiv:2605.10279](https://arxiv.org/abs/2605.10279).
- **Jiao, Y., Castellano Ontiveros, R., De Raedt, L., Gori, M., Giannini, F., Diligenti, M. & Marra, G.** (2026).
  *DeepProofLog: Efficient Proving in Deep Stochastic Logic Programs.* AAAI 2026 (Oral).
  [arXiv:2511.08581](https://arxiv.org/abs/2511.08581) — Recasts resolution as an MDP so DP/RL replace explicit
  provenance construction.
- **Wan, Z., Liu, C.-K., Qian, J., Yang, H., Raychowdhury, A. & Krishna, T.** (2026). *REASON: Accelerating
  Probabilistic Logical Reasoning…* IEEE HPCA 2026. [arXiv:2601.20784](https://arxiv.org/abs/2601.20784)
  — 12–50× over GPUs, 310–681× energy efficiency, 6 mm² at 2.12 W on TSMC 28 nm.
- **Li, Z., Huang, J., Liu, J., Zhu, F., Zhao, E., Dodds, W., Velingker, N., Alur, R. & Naik, M.** (2024).
  *Relational Programming with Foundation Models* (Vieira). AAAI 2024, DOI 10.1609/aaai.v38i9.28934.
  [arXiv:2412.14515](https://arxiv.org/abs/2412.14515) — **The actual bridge between probabilistic NeSy programming
  and foundation models** that most reviews claim does not exist: an LLM invoked as a *relation* inside a
  probabilistic logic program, its outputs flowing through the provenance semiring.

---

## 5. Abductive learning and differentiable ASP

- **Dai, W.-Z., Xu, Q., Yu, Y. & Zhou, Z.-H.** (2019). *Bridging Machine Learning and Logical Reasoning by
  Abductive Learning.* NeurIPS 2019.
  [proceedings](https://papers.nips.cc/paper_files/paper/2019/hash/9c19a2aa1d84e04b0bd4bc888792bd1e-Abstract.html)
  — Perception proposes pseudo-labels, a symbolic KB abduces the most consistent revision, retrain, repeat.
  **Non-differentiable, consistency-driven — an architectural family absent from most Western surveys.**
  Predecessor: [arXiv:1802.01173](https://arxiv.org/abs/1802.01173) (2018).
- **Hu, et al.** (2025). AAAI 2025 Oral. [arXiv:2412.08457](https://arxiv.org/abs/2412.08457)
- **Hu, et al.** (2025). *Curriculum Abductive Learning.* NeurIPS 2025.
  [arXiv:2505.12275](https://arxiv.org/abs/2505.12275)
- **Gao, Inoue, et al.** (2025). *Differentiable Rule Induction from Raw Sequence Inputs.* ICLR 2025.
- **Baugh, Perreault, Baugh, Dickens, Inoue & Russo** (2025). *Disentangling Neural Disjunctive Normal Form
  Models.* NeSy 2025. [arXiv:2507.10546](https://arxiv.org/abs/2507.10546)
- **Eiter, T., Inoue, K. & Moriyama, S.** (2026). *Neural Decision-Propagation for Answer Set Programming.*
  IJCAI-ECAI 2026. [arXiv:2605.01797](https://arxiv.org/abs/2605.01797)
- **Takemura, A. & Inoue, K.** (2026). *Differentiable Logic Programming to Mitigate Reasoning Shortcuts in
  Neurosymbolic Systems.* ICLP 2026, EPTCS 450:29–51. [arXiv:2607.21185](https://arxiv.org/abs/2607.21185)
- **Rader & Russo** (2026). *Accelerating NeurASP with vectorization and caching.* TPLP (ICLP 2026).
  [arXiv:2606.10787](https://arxiv.org/abs/2606.10787)

---

## 6. Hard constraints, guarantees, verification

- **Katz, G., Barrett, C., Dill, D., Julian, K. & Kochenderfer, M.** (2017). *Reluplex: An Efficient SMT Solver for
  Verifying Deep Neural Networks.* CAV 2017. [arXiv:1702.01135](https://arxiv.org/abs/1702.01135)
  Successor: Marabou 2.0, CAV 2024 ⚠ (arXiv ID 2401.14461 from an ADS listing, not fetched).
- **Alshiekh, M., Bloem, R., Ehlers, R., Könighofer, B., Niekum, S. & Topcu, U.** (2018). *Safe Reinforcement
  Learning via Shielding.* AAAI 2018, pp. 2669–2678. [arXiv:1708.08611](https://arxiv.org/abs/1708.08611)
- **Wang, P.-W., Donti, P.L., Wilder, B. & Kolter, Z.** (2019). *SATNet: Bridging deep learning and logical
  reasoning using a differentiable satisfiability solver.* ICML 2019.
  [arXiv:1905.12149](https://arxiv.org/abs/1905.12149) — **Learn the constraints** rather than inject them.
  Read with the replication failure below.
- **Topan, S., Rolnick, D. & Si, X.** (2021). *Techniques for Symbol Grounding with SATNet.*
  [arXiv:2106.11072](https://arxiv.org/abs/2106.11072) — Showed the headline visual-Sudoku result depended on
  **label leakage**. **The field's cleanest replication failure, and it predates the reasoning-shortcut literature
  by two years.** ⚠ NeurIPS 2021 venue unconfirmed.
- **Vlastelica, M., Paulus, A., Musil, V., Martius, G. & Rolínek, M.** (2020). *Differentiation of Blackbox
  Combinatorial Solvers.* ICLR 2020 (spotlight). [arXiv:1912.02175](https://arxiv.org/abs/1912.02175)
  — Informative gradients for exact solvers, one extra solver call per backward pass. Source of the
  Warcraft-shortest-path benchmark.
- **Giunchiglia, E. & Lukasiewicz, T.** (2020). *Coherent Hierarchical Multi-Label Classification Networks*
  (C-HMCNN). NeurIPS 2020.
- **Donti, P.L., Rolnick, D. & Kolter, J.Z.** (2021). *DC3: A learning method for optimization with hard
  constraints.* ICLR 2021. [arXiv:2104.12225](https://arxiv.org/abs/2104.12225)
  ⚠ The "78× faster than qpth" figure could not be confirmed on the arXiv abstract.
- **Hoernle, N., Karampatsis, R.M., Belle, V. & Gal, K.** (2022). *MultiplexNet: Towards Fully Satisfied Logical
  Constraints in Neural Networks.* AAAI 2022. [arXiv:2111.01564](https://arxiv.org/abs/2111.01564)
- **Geng, S., Josifoski, M., Peyrard, M. & West, R.** (2023). *Grammar-Constrained Decoding for Structured NLP
  Tasks without Finetuning.* EMNLP 2023, pp. 10932–10952.
  [ACL Anthology](https://aclanthology.org/2023.emnlp-main.674/)
- **Willard, B.T. & Louf, R.** (2023). *Efficient Guided Generation for Large Language Models* (Outlines).
  [arXiv:2307.09702](https://arxiv.org/abs/2307.09702) ⚠ No peer-reviewed venue found.
- **Yang, W.-C., Marra, G., Rens, G. & De Raedt, L.** (2023). *Safe Reinforcement Learning via Probabilistic Logic
  Shields.* IJCAI 2023, pp. 5739–5749 (distinguished paper).
  [arXiv:2303.03226](https://arxiv.org/abs/2303.03226)
- **Park, K., Wang, J., Berg-Kirkpatrick, T., Polikarpova, N. & D'Antoni, L.** (2024). *Grammar-Aligned Decoding.*
  NeurIPS 2024. [arXiv:2405.21047](https://arxiv.org/abs/2405.21047)
  — **The single most important gotcha paper for anyone shipping constrained decoding.** Masking is greedy local
  filtering, not Bayesian conditioning.
- **Dong, Y., Ruan, C.F., Cai, Y., Lai, R., Xu, Z., Zhao, Y. & Chen, T.** (2024/25). *XGrammar: Flexible and
  Efficient Structured Generation Engine for LLMs.* MLSys 2025.
  [arXiv:2411.15100](https://arxiv.org/abs/2411.15100) — Up to 100× over prior grammar-constrained decoding.
- **Min, Y. & Azizan, N.** (2024/25). *HardNet: Hard-Constrained Neural Networks with Universal Approximation
  Guarantees.* [arXiv:2410.10807](https://arxiv.org/abs/2410.10807) ⚠ arXiv only as of v4.
- **Banerjee, D., Suresh, T., Ugare, S., Misailovic, S. & Singh, G.** (2025). *CRANE: Reasoning with constrained
  LLM generation.* ICML 2025. [arXiv:2502.09061](https://arxiv.org/abs/2502.09061)
  — Up to 10 points on GSM-Symbolic and FOLIO by augmenting the grammar with a reasoning region.
- **Kurscheidt, et al.** (2025). *PAL: A Probabilistic Neuro-symbolic Layer for Algebraic Constraint
  Satisfaction.* UAI 2025. [arXiv:2503.19466](https://arxiv.org/abs/2503.19466)
- **Kaulen, K., Ladner, T., Bak, S., Brix, C., et al.** (2025). *The 6th International Verification of Neural
  Networks Competition (VNN-COMP 2025).* [arXiv:2512.19007](https://arxiv.org/abs/2512.19007)
  — α,β-CROWN placed first. ⚠ Detailed scores came from a third-party summary page; team/benchmark counts were
  corroborated on the arXiv abstract.
- **Pal, S. & Li, C.** (2026). *DisjunctiveNet: Neural Symbolic Learning via Differentiable Convexified
  Optimization Layers.* ICML 2026 ⚠ (venue from the author-supplied arXiv comment field).
  [arXiv:2605.30456](https://arxiv.org/abs/2605.30456)
- ⚠ **Ramirez, Hashemizadeh & Lacoste-Julien.** *Position: Adopt Constraints Over Fixed Penalties in Deep
  Learning.* [arXiv:2505.20628](https://arxiv.org/abs/2505.20628) — **Could not be confirmed to exist during the
  audit.** Verify before citing.

---

## 7. Perception, concepts, program induction, abstract reasoning

- **Andreas, J., Rohrbach, M., Darrell, T. & Klein, D.** (2015). *Neural Module Networks.*
  [arXiv:1511.02799](https://arxiv.org/abs/1511.02799) — Direct ancestor of NS-VQA/NS-CL.
  ⚠ CVPR 2016 venue not verified.
- **Johnson, J., Hariharan, B., van der Maaten, L., Fei-Fei, L., Zitnick, C.L. & Girshick, R.** (2017). *CLEVR.*
  CVPR 2017.
  [link](https://openaccess.thecvf.com/content_cvpr_2017/html/Johnson_CLEVR_A_Diagnostic_CVPR_2017_paper.html)
- **Yi, K., Wu, J., Gan, C., Torralba, A., Kohli, P. & Tenenbaum, J.B.** (2018). *Neural-Symbolic VQA.*
  NeurIPS 2018 (spotlight). [arXiv:1810.02338](https://arxiv.org/abs/1810.02338) — **99.8% on CLEVR** (verified).
- **Mao, J., Gan, C., Kohli, P., Tenenbaum, J.B. & Wu, J.** (2019). *The Neuro-Symbolic Concept Learner.*
  ICLR 2019 (Oral). [arXiv:1904.12584](https://arxiv.org/abs/1904.12584)
  ⚠ The widely-quoted 98.9% CLEVR figure does not appear in the abstract; it is unverified.
- **Yi, K., Gan, C., Li, Y., Kohli, P., Wu, J., Torralba, A. & Tenenbaum, J.B.** (2020). *CLEVRER.* ICLR 2020.
  [arXiv:1910.01442](https://arxiv.org/abs/1910.01442) — NS-DR: 88.1% descriptive, 79.6% explanatory,
  68.7% predictive, **42.2% counterfactual**.
- **Koh, P.W., Nguyen, T., Tang, Y.S., Mussmann, S., Pierson, E., Kim, B. & Liang, P.** (2020).
  *Concept Bottleneck Models.* ICML 2020.
- **Locatello, F., Weissenborn, D., Unterthiner, T., Mahendran, A., Heigold, G., Uszkoreit, J., Dosovitskiy, A. &
  Kipf, T.** (2020). *Object-Centric Learning with Slot Attention.* NeurIPS 2020.
  [proceedings](https://proceedings.neurips.cc/paper/2020/hash/8511df98c02ab60aea1b2356c013bc0f-Abstract.html)
- **Mahinpei, A., Clark, J., Lage, I., Doshi-Velez, F. & Pan, W.** (2021). *Promises and Pitfalls of Black-Box
  Concept Learning Models.* [arXiv:2106.13314](https://arxiv.org/abs/2106.13314) — Concept leakage.
  ⚠ Workshop venue unconfirmed.
- **Stammer, W., Schramowski, P. & Kersting, K.** (2021). *Right for the Right Concept.* CVPR 2021.
  [arXiv:2011.12854](https://arxiv.org/abs/2011.12854) — Introduces CLEVR-Hans3/7.
- **Ellis, K., Wong, C., Nye, M., Sablé-Meyer, M., Cary, L., Morales, L., Hewitt, L., Solar-Lezama, A. &
  Tenenbaum, J.B.** (2021). *DreamCoder.* PLDI 2021. [DOI](https://dl.acm.org/doi/10.1145/3453483.3454080)
- **Kleyko, D., Rachkovskij, D.A., Osipov, E. & Rahimi, A.** (2022/23). *A Survey on Hyperdimensional Computing
  aka Vector Symbolic Architectures,* Parts I & II. ACM Computing Surveys 55(6) art. 130 and 55(9) art. 175.
  [Part I](https://arxiv.org/abs/2111.06077) · [Part II](https://arxiv.org/abs/2112.15424)
- **Hersche, M., Zeqiri, M., Benini, L., Sebastian, A. & Rahimi, A.** (2023). *A neuro-vector-symbolic architecture
  for solving Raven's progressive matrices.* Nature Machine Intelligence.
  [link](https://www.nature.com/articles/s42256-023-00630-8) — 87.7% RAVEN, 88.1% I-RAVEN.
- **Gupta, T. & Kembhavi, A.** (2023). *Visual Programming.* CVPR 2023 (Best Paper), pp. 14953–14962.
  Concurrent: ViperGPT (Surís, Menon & Vondrick, ICCV 2023,
  [arXiv:2303.08128](https://arxiv.org/abs/2303.08128)) ⚠ *its 48.1% GQA figure was seen only in a third-party
  paper's description and is unverified.*
- **Grand, G., Wong, L., Bowers, M., Olausson, T.X., Liu, M., Tenenbaum, J.B. & Andreas, J.** (2024). *LILO.*
  ICLR 2024. [arXiv:2310.19791](https://arxiv.org/abs/2310.19791)
- **Chollet, F., Knoop, M., Kamradt, G., Landers, B. & Pinkard, H.** (2025). *ARC-AGI-2.*
  [arXiv:2505.11831](https://arxiv.org/abs/2505.11831) ⚠ **No human-baseline percentage appears in this paper or
  the 2025 technical report — do not quote one.**
- **Jolicoeur-Martineau, A.** (2025). *Less is More: Recursive Reasoning with Tiny Networks* (TRM).
  [arXiv:2510.04871](https://arxiv.org/abs/2510.04871) — 7M parameters, 45% ARC-AGI-1, 8% ARC-AGI-2.
  ARC Prize 2025 Paper Award, 1st place.
- **Pourcel, Colas & Oudeyer** (2025). *SOAR.* ICML 2025. [arXiv:2507.14172](https://arxiv.org/abs/2507.14172)
  — Evolutionary LLM program synthesis, 52% ARC-AGI-1 public test, no DSL.
- **Chollet, F., Knoop, M., Kamradt, G. & Landers, B.** (2026). *ARC Prize 2025: Technical Report.*
  [arXiv:2601.10904](https://arxiv.org/abs/2601.10904) — 1,455 teams, 15,154 entries, top private-eval **24%**,
  90 paper submissions. ⚠ Per-team names and $/task figures are single-source (arcprize.org blog) and the two
  sources disagree on cost.
- **Yang, Y., Campbell, D., Huang, K., Wang, M., Cohen, J. & Webb, T.** (2025). *Emergent Symbolic Mechanisms
  Support Abstract Reasoning in Large Language Models.* ICML 2025.
  [arXiv:2502.20332](https://arxiv.org/abs/2502.20332) — Symbol-abstraction heads → symbolic-induction heads →
  retrieval heads. **The strongest positive evidence that transformers implement symbol-like variable binding
  internally** — the empirical continuation of Smolensky's programme.

---

## 8. Knowledge graphs, rules, GNN expressiveness

- **Bordes, A., Usunier, N., García-Durán, A., Weston, J. & Yakhnenko, O.** (2013). *TransE.* NIPS 2013.
- **Yang, B., Yih, W., He, X., Gao, J. & Deng, L.** (2015). *DistMult.* ICLR 2015.
  [arXiv:1412.6575](https://arxiv.org/abs/1412.6575)
- **Trouillon, T., Welbl, J., Riedel, S., Gaussier, É. & Bouchard, G.** (2016). *Complex Embeddings for Simple
  Link Prediction.* ICML 2016. [arXiv:1606.06357](https://arxiv.org/abs/1606.06357)
- **Sun, Z., Deng, Z.-H., Nie, J.-Y. & Tang, J.** (2019). *RotatE.* ICLR 2019.
  [arXiv:1902.10197](https://arxiv.org/abs/1902.10197)
- **Galárraga, L., Teflioudi, C., Hose, K. & Suchanek, F.M.** (2015). *Fast rule mining in ontological knowledge
  bases with AMIE+.* VLDB Journal. [DOI](https://doi.org/10.1007/s00778-015-0394-1)
- **Gutiérrez-Basulto, V. & Schockaert, S.** (2018). *From Knowledge Graph Embedding to Ontology Embedding?*
  KR 2018. ⚠ Description ("point vs region semantics") from background, not a fetched abstract.
- **Meilicke, C., Chekol, M.W., Ruffinelli, D. & Stuckenschmidt, H.** (2019). *AnyBURL.* IJCAI 2019.
  [DOI](https://doi.org/10.24963/ijcai.2019/435); VLDB Journal 33(1):131–161, 2024.
  Companion: Meilicke et al., *Fine-Grained Evaluation of Rule- and Embedding-Based Systems…* ISWC 2018.
  ⚠ No specific MRR/Hits@10 numbers verified; the qualitative competitiveness claim is well established.
- **Kulmanov, M., Liu-Wei, W., Yan, Y. & Hoehndorf, R.** (2019). *EL Embeddings: Geometric construction of models
  for the Description Logic EL++.* [arXiv:1902.10499](https://arxiv.org/abs/1902.10499) ⚠ IJCAI-2019 venue unverified.
  Successors: Box²EL ([arXiv:2301.11118](https://arxiv.org/abs/2301.11118)), TransBox, ALC saturation embeddings.
- **Barceló, P., Kostylev, E.V., Monet, M., Pérez, J., Reutter, J.L. & Silva, J.P.** (2020). *The Logical
  Expressiveness of Graph Neural Networks.* ICLR 2020.
  [OpenReview](https://openreview.net/forum?id=r1lZ7AEKvB) ⚠ The graded-modal-logic / FOC2 characterisation is from
  background; OpenReview served a bot-check during verification.
- **Ren, H., Hu, W. & Leskovec, J.** (2020). *Query2box.* ICLR 2020.
  [arXiv:2002.05969](https://arxiv.org/abs/2002.05969); BetaE, NeurIPS 2020,
  [arXiv:2010.11465](https://arxiv.org/abs/2010.11465)
- **Zhu, Z., Zhang, Z., Xhonneux, L.-P. & Tang, J.** (2021). *Neural Bellman-Ford Networks.* NeurIPS 2021.
  [arXiv:2106.06935](https://arxiv.org/abs/2106.06935) — **The conceptual pivot of the sub-area.**
- **Veličković, P. & Blundell, C.** (2021). *Neural Algorithmic Reasoning.* Patterns.
  [arXiv:2105.02761](https://arxiv.org/abs/2105.02761); CLRS benchmark, ICML 2022,
  [arXiv:2205.15659](https://arxiv.org/abs/2205.15659)
- **Grohe, M.** (2023/24). *The Descriptive Complexity of Graph Neural Networks.* TheoretiCS vol. 3.
  [arXiv:2303.04613](https://arxiv.org/abs/2303.04613); readable on-ramp:
  *The Logic of Graph Neural Networks,* [arXiv:2104.14624](https://arxiv.org/abs/2104.14624)
- **Zhu, Z., Yuan, X., Galkin, M., Xhonneux, S., Zhang, M., Gazeau, M. & Tang, J.** (2023). *A\*Net.* NeurIPS 2023.
  [arXiv:2206.04798](https://arxiv.org/abs/2206.04798)
- **Galkin, M., Yuan, X., Mostafa, H., Tang, J. & Zhu, Z.** (2024). *Towards Foundation Models for Knowledge Graph
  Reasoning* (ULTRA). ICLR 2024. [arXiv:2310.04562](https://arxiv.org/abs/2310.04562) — 57 KGs zero-shot.
  Extension: UltraQuery, NeurIPS 2024, [arXiv:2404.07198](https://arxiv.org/abs/2404.07198)
- **Pan, S., Luo, L., Wang, Y., Chen, C., Wang, J. & Wu, X.** (2024). *Unifying Large Language Models and Knowledge
  Graphs: A Roadmap.* IEEE TKDE. [arXiv:2306.08302](https://arxiv.org/abs/2306.08302)
- **Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., Metropolitansky, D., Ness, R.O. &
  Larson, J.** (2024). *From Local to Global: A Graph RAG Approach…* [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
  — Read precisely to see what it is **not**: the graph is an index; no inference, no entailment, no consistency check.
- **Huang, X., Barceló, P., Bronstein, M.M., Ceylan, İ.İ., Galkin, M., Reutter, J.L. & Romero Orth, M.** (2025).
  *How Expressive are Knowledge Graph Foundation Models?* ICML 2025.
  [arXiv:2502.13339](https://arxiv.org/abs/2502.13339)
- **Fan, D., Xue, Z., Liu, S. & Tan, Q.** (2026). *Do We Still Need GraphRAG? Benchmarking RAG and GraphRAG for
  Agentic Search Systems.* [arXiv:2604.09666](https://arxiv.org/abs/2604.09666)

---

## 9. LLM + solver / prover

- **Gao, L., Madaan, A., Zhou, S., et al.** (2022). *PAL: Program-aided Language Models.*
  [arXiv:2211.10435](https://arxiv.org/abs/2211.10435) ⚠ ICML 2023 venue believed but unconfirmed.
  Concurrent twin: Program-of-Thoughts (Chen et al., TMLR 2023,
  [arXiv:2211.12588](https://arxiv.org/abs/2211.12588)).
- **Lyu, Q., Havaldar, S., Stein, A., et al.** (2023). *Faithful Chain-of-Thought Reasoning.* IJCNLP-AACL 2023.
  [arXiv:2301.13379](https://arxiv.org/abs/2301.13379)
- **Ye, X., Chen, Q., Dillig, I. & Durrett, G.** (2023). *SatLM.* NeurIPS 2023.
  [arXiv:2305.09656](https://arxiv.org/abs/2305.09656)
- **Pan, L., Albalak, A., Wang, X. & Wang, W.Y.** (2023). *Logic-LM.* Findings of EMNLP 2023.
  [arXiv:2305.12295](https://arxiv.org/abs/2305.12295) — +39.2% over standard prompting, +18.4% over CoT.
- **Olausson, T.X., Gu, A., Lipkin, B., et al.** (2023). *LINC.* EMNLP 2023 (Outstanding Paper).
  [arXiv:2310.15164](https://arxiv.org/abs/2310.15164)
- **Yang, Z., Ishay, A. & Lee, J.** (2023). *Coupling Large Language Models with Logic Programming…*
  Findings of ACL 2023, pp. 5186–5219. [arXiv:2307.07696](https://arxiv.org/abs/2307.07696);
  companion KR 2023, [arXiv:2307.07699](https://arxiv.org/abs/2307.07699)
- **Yang, K., Swope, A.M., Gu, A., Chalamala, R., Song, P., Yu, S., Godil, S., Prenger, R. & Anandkumar, A.**
  (2023). *LeanDojo.* NeurIPS 2023 D&B (oral). [arXiv:2306.15626](https://arxiv.org/abs/2306.15626)
  — 98,734 theorems from mathlib; turns Lean into a Python-callable gym.
- **Trinh, T.H., Wu, Y., Le, Q.V., He, H. & Luong, T.** (2024). *Solving olympiad geometry without human
  demonstrations* (AlphaGeometry). Nature 625(7995):476–482.
  [DOI](https://doi.org/10.1038/s41586-023-06747-5) — **25/30 vs prior best 10.** Fully confirmed against the PMC
  full text. AlphaGeometry 2: [arXiv:2502.03544](https://arxiv.org/abs/2502.03544).
- **Kambhampati, S., Valmeekam, K., Guan, L., et al.** (2024). *LLMs Can't Plan, But Can Help Planning in
  LLM-Modulo Frameworks.* ICML 2024, PMLR 235. [arXiv:2402.01817](https://arxiv.org/abs/2402.01817)
- **Mirzadeh, I., Alizadeh, K., Shahrokhi, H., Tuzel, O., Bengio, S. & Farajtabar, M.** (2024/25).
  *GSM-Symbolic.* ICLR 2025. [arXiv:2410.05229](https://arxiv.org/abs/2410.05229)
  — Up to 65% degradation from one logically inert clause. Full six-author list confirmed.
- **Lam, L.H.M., Thatikonda, R.K. & Shareghi, E.** (2024). *A Closer Look at Logical Reasoning with LLMs: The
  Choice of Tool Matters.* [arXiv:2406.00284](https://arxiv.org/abs/2406.00284) — **~50% of reported variation
  traces to solver choice.**
- **DeepSeek-AI (Guo, D., Yang, D., Zhang, H., Song, J., Wang, P., et al.)** (2025). *DeepSeek-R1 incentivizes
  reasoning in LLMs through reinforcement learning.* Nature 645(8081):633–638.
  [DOI](https://doi.org/10.1038/s41586-025-09422-z) *[corrected]* This is the **Nature** title; "DeepSeek-R1:
  Incentivizing Reasoning Capability in LLMs via Reinforcement Learning" is the arXiv:2501.12948 title.
  ⚠ The widely quoted 79.8% AIME 2024 pass@1 was not verified.
- **Shojaee, P., Mirzadeh, I., Alizadeh, K., Horton, M., Bengio, S. & Farajtabar, M.** (2025). *The Illusion of
  Thinking.* NeurIPS 2025. [arXiv:2506.06941](https://arxiv.org/abs/2506.06941)
- **Lawsen, A.** (2025). *Comment on The Illusion of Thinking.*
  [arXiv:2506.09250](https://arxiv.org/abs/2506.09250) — The methodological counterweight. Two further rebuttals
  followed within a month ([2506.18957](https://arxiv.org/abs/2506.18957),
  [2507.01231](https://arxiv.org/abs/2507.01231)).
- **Ren, Z.Z., Shao, Z., Song, J., et al. (DeepSeek-AI)** (2025). *DeepSeek-Prover-V2.*
  [arXiv:2504.21801](https://arxiv.org/abs/2504.21801) — 88.9% miniF2F-test, 49/658 PutnamBench.
  Lineage: V1.5 ([2408.08152](https://arxiv.org/abs/2408.08152)), Goedel-Prover
  ([2502.07640](https://arxiv.org/abs/2502.07640)), Kimina-Prover ([2504.11354](https://arxiv.org/abs/2504.11354)).
- **Chen, L., Gu, J., Huang, L., et al. (ByteDance Seed)** (2025). *Seed-Prover.*
  [arXiv:2507.23726](https://arxiv.org/abs/2507.23726) — **5/6 IMO 2025 problems formally proved in Lean.**
- **Hubert, T., Mehta, R., Sartran, L., … Hassabis, D., Kohli, P. & Silver, D.** (2025). *Olympiad-level formal
  mathematical reasoning with reinforcement learning* (AlphaProof). Nature **651(8106):607–613**, epub
  12 Nov 2025. [DOI](https://doi.org/10.1038/s41586-025-09833-y) — Fully confirmed via PubMed 41225005.
  3/5 non-geometry IMO 2024 problems; 28 points with AlphaGeometry 2 = silver.
  *[corrected]* Cite as **2025** (epub); the print issue is March 2026 — this is why the year appears
  inconsistently across sources.
- **Chen, J., Chen, W., Du, J., et al. (ByteDance Seed)** (2025). *Seed-Prover 1.5.*
  [arXiv:2512.17260](https://arxiv.org/abs/2512.17260) *[corrected]* The abstract states **88%** of PutnamBench —
  the circulating "87.9%" does not appear there.
- **Chung, J.-H., Cai, Z., Li, Z., … Wang, M., Chen, D., Jin, C., Fowl, L.H. & Arora, S.** (2026).
  *Goedel-Architect.* [arXiv:2606.06468](https://arxiv.org/abs/2606.06468)
  — 99.2% pass@1 miniF2F-test, 75.6% pass@1 PutnamBench; 100% / 88.8% (597/672) with NL seeding; 4/6 IMO 2025,
  11/12 Putnam 2025, 3/6 USAMO 2026, at up to 500× lower cost. **All figures confirmed verbatim in the audit.**
- **Raiyan, S.R., Kabir, M., Mahmud, H., Hasan, M.K. & Ananiadou, S.** (2026). *Artificial Intelligence for
  Mathematical Reasoning: An Integrated Survey…* [arXiv:2606.08728](https://arxiv.org/abs/2606.08728)
  — 47 pages; unusually honest about benchmark saturation, contamination and pass@k reporting mismatches.
- **Romera-Paredes, B., Barekatain, M., Novikov, A., Balog, M., Kumar, M.P., Dupont, E., Ruiz, F.J.R.,
  Ellenberg, J.S., Wang, P., Fawzi, O., Kohli, P. & Fawzi, A.** (2024). *Mathematical discoveries from program
  search with large language models* (FunSearch). Nature 625(7995):468–475.
  [link](https://www.nature.com/articles/s41586-023-06924-6) — The canonical LLM-plus-verifier discovery result and
  the direct predecessor of AlphaEvolve.
- **Novikov, A., Vũ, N., Eisenberger, M., Dupont, E., Huang, P.-S., Wagner, A.Z., et al.** (2025). *AlphaEvolve.*
  [arXiv:2506.13131](https://arxiv.org/abs/2506.13131) — 48-multiplication 4×4 complex matrix multiplication,
  first improvement over Strassen in 56 years.
- **Georgiev, B., Gómez-Serrano, J., Tao, T. & Wagner, A.Z.** (2025). *Mathematical exploration and discovery at
  scale.* [arXiv:2511.02864](https://arxiv.org/abs/2511.02864) — 67 open/semi-open problems.
- **Kordjamshidi, P., Aslan, S., Seshadri, M., Barrett, L. & Santus, E.** (2026). *Reasoners or Translators?
  Contamination-aware Evaluation and Neuro-Symbolic Robustness in Tax Law.*
  [arXiv:2605.16052](https://arxiv.org/abs/2605.16052)

⚠ **Unverified during the audit and excluded from the review's claims:** Harmonic AI's "Aristotle" IMO 2025 gold
result (no matching paper found); the OpenAI July 2025 IMO 35/42 claim (no fetchable primary source); a cluster of
2026 arXiv IDs surfaced only in search listings (2606.16541, 2607.19407, 2511.03108, 2601.14456, 2606.12594,
2605.27014, 2606.16603, 2607.23386). Re-check any of these before citing.

---

## 10. Reasoning shortcuts and evaluation critique

- **Marconato, E., Teso, S., Vergari, A. & Passerini, A.** (2023). *Not All Neuro-Symbolic Concepts Are Created
  Equal.* NeurIPS 2023. [arXiv:2305.19951](https://arxiv.org/abs/2305.19951)
- **Bortolotti, S., Marconato, E., Carraro, T., Morettin, P., van Krieken, E., Vergari, A., Teso, S. &
  Passerini, A.** (2024). *A Neuro-Symbolic Benchmark Suite for Concept Quality and Reasoning Shortcuts* (rsbench).
  [arXiv:2406.10368](https://arxiv.org/abs/2406.10368) · [site](https://unitn-sml.github.io/rsbench/)
  — miniBOIA: DeepProbLog 0.87 label / **0.28 concept**; LTN 0.78/**0.35**; CLIP 0.99/**0.34**.
  ⚠ NeurIPS 2024 D&B venue could not be confirmed from arXiv metadata; the eight-author list is confirmed verbatim.
- **van Krieken, E., Minervini, P., Ponti, E.M. & Vergari, A.** (2025). *Neurosymbolic Reasoning Shortcuts under
  the Independence Assumption.* NeSy 2025. [arXiv:2507.11357](https://arxiv.org/abs/2507.11357)
- **Marconato, E., Bortolotti, S., van Krieken, E., Morettin, P., Umili, E., Vergari, A., Tsamoura, E.,
  Passerini, A. & Teso, S.** (2025/26). *Symbol Grounding in Neuro-Symbolic AI: A Gentle Introduction to Reasoning
  Shortcuts.* JAIR (special track). [arXiv:2510.14538](https://arxiv.org/abs/2510.14538) (v3, Aug 2026)
  — Nine-author list and JAIR status confirmed. ⚠ No volume/pages assigned.
- **Takemura, A., Inoue, K. & Nishino, M.** (2026). *Constraint-Based Analysis of Reasoning Shortcuts in
  Neurosymbolic Learning.* KR 2026. [arXiv:2604.23377](https://arxiv.org/abs/2604.23377)
  — Shortcut detection coNP-complete, counting #P-complete. ⚠ Verified via abstract page only; the arXiv ID should
  be re-checked before citation.
- **Lake, B.M. & Baroni, M.** (2018). *Generalization without systematicity* (SCAN). ICML 2018.
  [arXiv:1711.00350](https://arxiv.org/abs/1711.00350)
- **Zhou, D., Schärli, N., Hou, L., Wei, J., Scales, N., Wang, X., Schuurmans, D., Cui, C., Bousquet, O., Le, Q. &
  Chi, E.** (2022/23). *Least-to-Most Prompting.* ICLR 2023.
  [arXiv:2205.10625](https://arxiv.org/abs/2205.10625) — **≥99% on all SCAN splits with 14 exemplars vs 16% CoT.**
- **Drozdov, A., Schärli, N., Akyürek, E., Scales, N., Song, X., Chen, X., Bousquet, O. & Zhou, D.** (2022).
  *Compositional Semantic Parsing with Large Language Models.*
  [arXiv:2209.15003](https://arxiv.org/abs/2209.15003) — CFQ 95.0 mean with **1%** of the training data.
  ⚠ ICLR 2023 venue unconfirmed; author list confirmed verbatim.
- **Lake, B.M. & Baroni, M.** (2023). *Human-like systematic generalization through a meta-learning neural
  network.* Nature 623(7985):115–121. [DOI](https://doi.org/10.1038/s41586-023-06668-3)
  — **The most direct empirical rebuttal of Fodor & Pylyshyn available.**
- **Turpin, M., Michael, J., Perez, E. & Bowman, S.R.** (2023). *Language Models Don't Always Say What They Think.*
  NeurIPS 2023. Companion: Lanham et al., [arXiv:2307.13702](https://arxiv.org/abs/2307.13702).
- **Ott, Ledaguenel, Hudelot & Hartwig** (2023). *How to Think About Benchmarking Neurosymbolic AI?*
  NeSy 2023, CEUR-WS Vol-3432, pp. 248–254. ⚠ PDF text not extractable; arguments not characterised here.
- **Chan, Gaizauskas & Zhao** (2026). *Position: Logical Soundness is not a Reliable Criterion for Neurosymbolic
  Fact-Checking with LLMs.* ICLR 2026 workshop. [arXiv:2604.04177](https://arxiv.org/abs/2604.04177)

---

## 11. RL, planning, world models

- **Toro Icarte, R., Klassen, T.Q., Valenzano, R. & McIlraith, S.A.** (2018). *Using Reward Machines for
  High-Level Task Specification and Decomposition in RL.* ICML 2018, PMLR 80:2107–2116.
  [link](https://proceedings.mlr.press/v80/icarte18a.html)
- **Toro Icarte, R., Klassen, T.Q., Valenzano, R. & McIlraith, S.A.** (2022). *Reward Machines: Exploiting Reward
  Function Structure in RL.* JAIR 73:173–208. [arXiv:2010.03950](https://arxiv.org/abs/2010.03950)
  — **The best self-contained entry point to neurosymbolic RL.**
- **Verma, A., Murali, V., Singh, R., Kohli, P. & Chaudhuri, S.** (2018). *Programmatically Interpretable
  Reinforcement Learning.* ICML 2018, PMLR 80:5045–5054. [arXiv:1804.02477](https://arxiv.org/abs/1804.02477)
- **Bastani, O., Pu, Y. & Solar-Lezama, A.** (2018). *Verifiable RL via Policy Extraction* (VIPER).
  [arXiv:1805.08328](https://arxiv.org/abs/1805.08328) ⚠ NeurIPS 2018 venue not confirmed from the arXiv page.
- **De Giacomo, G., Iocchi, L., Favorito, M. & Patrizi, F.** (2019). *Foundations for Restraining Bolts.*
  ICAPS 2019, pp. 128–136. [arXiv:1807.06333](https://arxiv.org/abs/1807.06333)
- **Dong, H., Mao, J., Lin, T., Wang, C., Li, L. & Zhou, D.** (2019). *Neural Logic Machines.* ICLR 2019
  ⚠ (venue from arXiv comments).
- **Jiang, Z. & Luo, S.** (2019). *Neural Logic Reinforcement Learning.* ICML 2019
  ⚠ (venue from arXiv comments). [arXiv:1904.10729](https://arxiv.org/abs/1904.10729)
- **Jansen, N., Könighofer, B., Junges, S., Serban, A. & Bloem, R.** (2020). *Safe Reinforcement Learning Using
  Probabilistic Shields (Invited Paper).* CONCUR 2020, pp. 3:1–3:16, DOI 10.4230/LIPIcs.CONCUR.2020.3.
  *[corrected]* The arXiv version (1807.06096) is titled "…via Probabilistic Shields"; cite the CONCUR record.
- **Vaezipoor, P., Li, A., Toro Icarte, R. & McIlraith, S.** (2021). *LTL2Action.* ICML 2021.
- **Ahn, M., Brohan, A., Brown, N., et al.** (2022). *Do As I Can, Not As I Say* (SayCan). CoRL 2022, pp. 287–318.
  [arXiv:2204.01691](https://arxiv.org/abs/2204.01691) — 101 instructions, 84% plan / 74% execution on a real robot.
  ⚠ Figures from the project page, not the proceedings PDF.
- **Liang, J., Huang, W., Xia, F., Xu, P., Hausman, K., Ichter, B., Florence, P. & Zeng, A.** (2023).
  *Code as Policies.* ICRA 2023, pp. 9493–9500. [arXiv:2209.07753](https://arxiv.org/abs/2209.07753)
- **Valmeekam, K., Marquez, M., Olmo, A., Sreedharan, S. & Kambhampati, S.** (2023). *PlanBench.* NeurIPS 2023 D&B.
  [arXiv:2206.10498](https://arxiv.org/abs/2206.10498) — The obfuscated "Mystery" variants are the key device.
- **Guan, L., Valmeekam, K., Sreedharan, S. & Kambhampati, S.** (2023). *Leveraging Pre-trained LLMs to Construct
  and Utilize World Models for Model-based Task Planning.* NeurIPS 2023.
  [arXiv:2305.14909](https://arxiv.org/abs/2305.14909)
- **Acharya, K., Raza, W., Dourado Jr., C.M.J.M., Velasquez, A. & Song, H.H.** (2023/24). *Neurosymbolic
  Reinforcement Learning and Planning: A Survey.* IEEE TAI 5(5):1939–1953.
  [arXiv:2309.01038](https://arxiv.org/abs/2309.01038) — Use as a map, not an authority on results.
- **Valmeekam, K., Stechly, K. & Kambhampati, S.** (2024). *LLMs Still Can't Plan; Can LRMs?*
  [arXiv:2409.13373](https://arxiv.org/abs/2409.13373) — o1-preview 97.8% Blocksworld / 37.3% randomised Mystery;
  Fast Downward 100% at 0.265 s. ⚠ Numbers from arXiv HTML v1, not cross-checked against a second source.
- **Liang, Y., Kumar, N., Tang, H., Weller, A., Tenenbaum, J.B., Silver, T., Henriques, J.F. & Ellis, K.** (2025).
  *VisualPredicator.* ICLR 2025 (Spotlight). [arXiv:2410.23156](https://arxiv.org/abs/2410.23156)
- **Khan, Z., Prasad, A., Stengel-Eskin, E., Cho, J. & Bansal, M.** (2026). *One Life to Learn* (OneLife).
  ICLR 2026. [arXiv:2510.12088](https://arxiv.org/abs/2510.12088)
- **Lorang, P., Huemer, J., Duggan, T., Goebel, K., Zips, P. & Scheutz, M.** (2026). *Build on Priors.*
  [arXiv:2604.03759](https://arxiv.org/abs/2604.03759) — Real industrial forklift and Kinova arm; PDDL domain
  synthesised via ASP from 1–30 unannotated demonstrations. ⚠ arXiv preprint, no venue.

---

## 12. Applications (domains the core NeSy literature under-covers)

⚠ *These were surfaced by a completeness sweep and verified as existing works, but their results were not
independently audited. Treat as entry points, not as endorsements.*

- **Cybersecurity** — Hakim, S.B., Adil, M., Velasquez, A., Xu, S. & Song, H.H. (2025). *Neuro-Symbolic AI for
  Cybersecurity: State of the Art, Challenges, and Opportunities.*
  [arXiv:2509.06921](https://arxiv.org/abs/2509.06921). Companions: Tran et al.
  ([2506.04454](https://arxiv.org/abs/2506.04454)), Samaddar et al. on OOD detection for neurosymbolic cyber agents
  ([2412.02875](https://arxiv.org/abs/2412.02875)). **This is where DARPA/ARL funding actually lands.**
- **Drug discovery** — MARS, [arXiv:2410.05289](https://arxiv.org/abs/2410.05289)
- **Bioinformatics / ontologies** — the EL Embeddings line (§8), Hoehndorf's KAUST group
- **Scientific discovery** — AI Feynman (Science Advances 6:eaay2631); FunSearch (Nature 625:468–475);
  AlphaEvolve (§9)
- **Manufacturing** — CausalTrace, AAAI-26 IAAI, [arXiv:2510.12033](https://arxiv.org/abs/2510.12033);
  CausalPulse ⚠ (Bosch-plant deployment claim from a search summary)
- **Clinical, legal, finance, EDA** — several 2026 arXiv entries were surfaced but could not be individually
  verified; they are deliberately not listed with IDs here.

---

## 13. Venues, institutions, community

- **NeSy** — International Conference on Neurosymbolic Learning and Reasoning. 19th edition Sep 2025
  (UC Santa Cruz, PMLR vol. 284, eds. Gilpin, Giunchiglia, Hitzler & van Krieken; keynotes Van den Broeck, Kipf,
  McGuinness); 20th edition Lisbon (FCUL), 1–4 Sep 2026. Began 2005 as a workshop series; **not annual**
  (annual since 2005 would make 2025 the 21st). Run by the Neurosymbolic AI Association (nesy-ai.org), formalised
  at a 2014 Dagstuhl seminar.
- **IJCLR** — 5th edition Surrey Sep 2025, 6th UPV Valencia 16–18 Sep 2026. Inductive-logic-programming leaning.
- **NeuS** — International Conference on Neuro-symbolic Systems, 2026 edition. Usually missing from venue lists.
- ***Neurosymbolic Artificial Intelligence*** journal — IOS Press / SAGE, ISSN 2949-8732, open access, continuous
  publication. ⚠ Sources disagree on launch year; the homepage shows articles from 2024–25.
- **Adjacent venues** — KR, ICLP, AAAI, IJCAI, NeurIPS/ICML workshops. Note: **NeurIPS 2025 had no
  neurosymbolic-branded workshop**; the reasoning workshops are LLM-centric (MATH-AI, Foundations of Reasoning in
  Language Models, Efficient Reasoning).
- **IJCAI-ECAI 2026** (Bremen, 15–17 Aug) tutorial T21, *Deep Parameterized Logics as A Foundation for
  Neurosymbolic AI* — De Raedt, Marra, Manhaeve & Derkinderen.
- **Summer schools** — ScaDS.AI School on Neuro+Symbolic AI, Leipzig, 22–26 June 2026 (speakers incl. Belle,
  Hitzler, Ilievski, Marra) — verified. ⚠ A Centaur AI Institute 2026 edition surfaced in search but its page 404'd.
- **DARPA ANSR** — Assured Neuro Symbolic Learning and Reasoning, PM Susmit Jha, IPTO, BAA HR001122S0039.
  ⚠ No 2025–26 status update, budget or performer list on the programme page.

**Groups to follow** — KU Leuven (De Raedt, Manhaeve, Marra: DeepProbLog/DeepLog) · UCLA StarAI
(Van den Broeck: circuits, semantic loss) · Edinburgh (Vergari, Minervini, van Krieken) · Trento (Teso, Passerini,
Marconato: reasoning shortcuts) · VU Amsterdam (van Harmelen) · UPenn (Naik, Li: Scallop/Dolphin) · City,
University of London (d'Avila Garcez) · Kansas State (Hitzler) · Siena (Gori, Diligenti, Melacci) · MIT/Cornell
(Tenenbaum, Ellis: program induction) · **Nanjing LAMDA (Zhou, Dai: abductive learning)** · **NII Tokyo (Inoue,
Sato: differentiable ASP)** · Arizona State (Kambhampati: planning critique; Shakarian: PyReason) · IBM Research
(LNN) · Google DeepMind (Alpha-* systems).
⚠ *Individual affiliations shift; several could not be re-verified during preparation. Check before citing anyone's institution.*
