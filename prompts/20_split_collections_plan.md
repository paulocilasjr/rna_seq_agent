# Prompt Template: Split Count Matrix Collection by Condition

**Purpose**: Transform Galaxy count matrix collection into condition-specific collections
**Reference**: README.md Step 4
**Paper Provides Explicit Prompt**: YES (see below)

---

## Context

This is the core "agentic collection transformation" step described in the paper. It uses the run-to-condition mapping created in Step 1 to organize count data by experimental condition.

**Critical Requirement**: Must use Galaxy collection transformation tools (not direct API edits) to preserve provenance.

---

## Prerequisites

Before this step:
- [ ] Count matrix collection exists in Galaxy history
- [ ] run_condition_map.csv exists and is validated
- [ ] Collection ID is known
- [ ] Galaxy history ID is known

---

## Paper-Provided Prompt 1: Plan Only

**Use in Plan Mode** (or with "PLAN ONLY" instruction)

```
I need to split Galaxy dataset collection #<COLLECTION_ID> into several collections corresponding to experimental
conditions described in the manuscript (check manuscript pdf and supplemental materials xlsx files in this directory).
In order to do this you need to download metadata for sequencing runs for bioproject <PRJNA######> to obtain accessions
and metadata. You should then figure out how SRA accessions correspond to experimental conditions described in the paper.
You should then present these finding to me, so that I can tell you what to do next.
```

**Placeholders to fill**:
- `<COLLECTION_ID>`: Galaxy collection ID (e.g., `f2db41e1fa331b3e`)
- `<PRJNA######>`: BioProject accession (from config/datasets.yml)

---

## Review Plan

After CCA presents its plan:

1. **Verify mapping**:
   - [ ] Mapping matches your validated run_condition_map.csv
   - [ ] All samples accounted for
   - [ ] Conditions correctly identified

2. **Verify approach**:
   - [ ] Uses Galaxy collection tools (not direct API manipulation)
   - [ ] Mentions specific tool IDs (__FILTER_FROM_FILE__, __APPLY_RULES__, etc.)
   - [ ] Will create separate collections per condition
   - [ ] Preserves provenance in Galaxy history

3. **Clarify uncertainties**:
   - Ask CCA to resolve any ambiguities before proceeding

---

## Paper-Provided Prompt 2: Execute

**Only after approving the plan**

```
Go ahead and execute the plan. Once you are done please add name tags to dataset collection containing data we need to used
for DeSeq2 analysis. E.g., label collections with names tags such as <COND_A>, <COND_B>, and <COND_C>.
```

**Placeholders to fill**:
- `<COND_A>`, `<COND_B>`, `<COND_C>`: Actual condition names from your mapping (e.g., "control", "treated", "high_salt")

---

## Expected Outputs

1. **Galaxy History**: New collection transformation tool invocations visible in history
2. **Named Collections**: One collection per condition with appropriate tags
3. **Collection IDs**: CCA should report the collection ID for each condition-specific collection

---

## Verification

After execution:

1. **Check Galaxy history**:
   - [ ] Collection transformation tools visible (not just API calls)
   - [ ] Each tool invocation has clear name/label
   - [ ] No errors in tool execution

2. **Verify collections**:
   - [ ] Number of collections = number of conditions
   - [ ] Each collection contains expected number of samples
   - [ ] Collection element identifiers are meaningful
   - [ ] Name tags applied correctly

3. **Document**:
   - Galaxy history URL
   - Collection IDs for each condition
   - Any manual adjustments made

---

## Using `/galaxy-transform-collection` Slash Command

**Alternative approach**: Instead of the paper's prompts, you can use the custom slash command:

```
/galaxy-transform-collection Split collection <COLLECTION_ID> in history <HISTORY_ID>
into condition-specific collections using the mapping in artifacts/run_condition_maps/<DATASET>_run_condition_map.csv
```

This command has built-in knowledge of Galaxy collection tool best practices and common pitfalls.

---

## Logging

Document in logs/:
- Prompts used (paper prompt or custom)
- Plan presented by CCA
- Your review notes
- Execution results
- Galaxy history URL
- Collection IDs created
- Any issues encountered

---

## Next Step

Proceed to Step 5: DESeq2 differential expression analysis (see prompts/30_deseq2_plan.md)
