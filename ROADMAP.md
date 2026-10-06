# Roadmap — drug-discovery-workflows

Planning window: October 2026 – December 2027. Times will be revised after the
first complete delivery (Project 01 reproduction by a second person).

## Priorities

| Period | Priority | Verifiable milestone |
|---|---|---|
| Oct–Dec 2026 | Foundation, documentation standard, Project 01 | First data-to-report cycle reproduced by another person |
| Jan–Mar 2027 | Projects 02 and 03 | Justified target + curated chemical set with provenance |
| Apr–Jun 2027 | Project 04 and start of 05 | Prediction benchmark + initial docking protocol evaluated |
| Jul–Sep 2027 | Finish 05 and Project 06 | Docking validation + trajectory analysis with uncertainty |
| Oct–Dec 2027 | Integrative case study, external review, consolidation | Public documented version + independent reproduction report |

## Dependencies

```
01 Experimental data ──┐
02 Target evidence ────┼──► Integrative case study
03 Chemical data ──────┤
04 Predictive models ◄─┘ (uses curated data from 03)
05 Validated docking ◄── (uses target + ligands from 02/03)
06 Molecular simulation ◄── (optional enrichment of docking hypotheses)
```

Advanced extensions (expression, variants, MM/GBSA–PBSA, enhanced sampling,
QM/MM, generative chemistry) require completion and quality of their parent
modules. One extension may replace another if it better answers the central
scientific question.

## Near-term checklist

### Project 01
- [x] Repository skeleton and bilingual presentation
- [x] Simulated plate assay with planted QC failure
- [x] QC → normalization → curve fit → figures → report
- [x] Automated tests for scientific transforms
- [x] Automated clean-room reproduction (agent dry-run)
- [ ] Independent **human** reproduction recorded in `docs/research_log/`

### Project 02
- [x] CDK2 (P24941) UniProt/PDB snapshots with access dates
- [x] Ortholog conservation map
- [x] Intent-aware structure ranking + target brief
- [x] Offline NGL HTML viewer for bundled coordinates
- [x] Automated tests

### Project 03
- [x] Simulated bioactivity table with planted curation pitfalls
- [x] RDKit parent standardization, unit/endpoint policies, exclusions
- [x] Descriptors + Morgan FP PCA
- [x] Automated tests

### Project 04
- [x] ChEMBL CDK2 IC50 snapshot curated to unique parents
- [x] Mean / Ridge / RF comparison
- [x] Random vs scaffold splits with overlap diagnostics
- [x] Simple fingerprint applicability-domain subgroups
- [x] Automated tests

### Project 05
- [x] 1AQ1/STU preparation with Open Babel + Vina
- [x] Redocking RMSD (Hungarian heavy-atom match)
- [x] Tiny active/decoy screen with enrichment
- [x] Explicit pose vs ranking vs affinity claim separation
- [x] Automated unit + integration tests

### Next up
- [ ] Project 06 trajectory analysis entry point
- [ ] Human independent reproduction of Project 01

## Decision log pointers

Methodological choices for each module live in that module's `docs/protocol.md`
and in `docs/research_log/`.
