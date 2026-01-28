# End-to-End Reproduction of the Paper’s Agentic Galaxy Workflow Using Claude Code (CCA)

This README defines an **end-to-end** reproduction of the *paper’s* process (not “start from the provided histories”).
The intent is to replicate the workflow exactly so you can **improve/extend** it afterwards.

**Core idea:** run **Claude Code Agent (CCA)** locally; CCA drives **usegalaxy.org** via a **Galaxy API key**; you enforce a strict
**Plan → Review → Execute** loop; and you preserve provenance by expressing key operations (especially **collection transforms**)
as **Galaxy tool invocations** recorded in the Galaxy history.

---

## Scope

You will reproduce the paper’s full flow:

1) **SRA → reads → count matrix (Galaxy workflow)**
2) **Supplement + SRA metadata → run-to-condition mapping (CCA)**
3) **Count matrix collection → condition-specific collections (Galaxy collection tools, orchestrated by CCA)**
4) **Condition-specific DESeq2 comparisons (Galaxy)**
5) **Gene ID mapping across annotation versions (deterministic, documented)**
6) **Validation against published log2FC (notebook-based, no LLM “hand-waving”)**

---

## Non-Negotiable Repro Principles

1. **Plan → Review → Execute**
   - Every major step must be planned first.
   - You approve/adjust before execution.

2. **Provenance first**
   - Collection manipulation must be done via **Galaxy tools** (rules/filter/relabel/apply-rules tools), not opaque API mutations.
   - Goal: every transformation is visible in the history and extractable into a workflow.

3. **Independent verification**
   - Never accept “good-looking” correlations without a deterministic gene-ID mapping and an auditable validation notebook.
---

## Where Prompts Exist (and Where the Paper Does *Not* Provide Them)

The manuscript **only shows explicit CCA prompt text** for the **collection-splitting** step (Plan-only → Execute).
For the rest of the pipeline (SRA ingestion, counting workflow, DESeq2 runs, gene-ID mapping, validation), the paper
describes the *actions* but does **not** publish the exact prompt strings.

To keep this reproduction faithful **and still usable**, this README does the following:
- **When the paper provides prompt text**: we include it verbatim (with placeholders).
- **When the paper does not provide prompt text**: we still mark *where* you would prompt (if you choose to use CCA),
  but we do **not invent** exact wording. Instead, we require you to record your local prompt in `logs/`.

### Prompt checkpoints (paper text vs. “record your own”)
| Pipeline step | Paper provides prompt text? | What to do in this repro |
|---|---:|---|
| Build run→condition mapping + split counts collection | Yes | Use the two prompts in **Prompts Actually Used in the Paper** |
| SRA→FASTQ ingestion in Galaxy | No | Run via Galaxy UI/workflow; if using CCA, write your own prompt and save it under `logs/` |
| RNA-seq counting workflow (reads→counts) | No | Run via Galaxy workflow; if using CCA, record the prompt you used under `logs/` |
| DESeq2 comparisons | No | Run via Galaxy; if using CCA, record the prompt you used under `logs/` |
| Gene-ID mapping across annotations | No | Implement deterministically; if using CCA to assist, record the prompt under `logs/` |
| Validation vs published log2FC | No | Run deterministic notebook/script; if using CCA for setup, record the prompt under `logs/` |

---


---

## Note on Citations

You may see strange tokens like `filecite...` in earlier drafts. These were **internal citation placeholders**
from the drafting environment and are **not meant to appear in your README**. They have been removed in this version.

## Prerequisites

### 1) Claude Code (CCA) installed and runnable
Install Claude Code locally (macOS/Linux/WSL). Confirm you can run it from the terminal.

### 2) A usegalaxy.org account + API key
Create an API key in:
**usegalaxy.org → User → Preferences → Manage API Key**

Export it (never commit secrets):

```bash
export GALAXY_API_KEY="YOUR_USEGALAXY_API_KEY"
```

### 3) Optional but strongly recommended
- A git repo to version prompts, mapping tables, notebooks, and notes
- A “run log” folder where you save raw CCA transcripts and Galaxy history links

---

## Suggested Local Repository Layout

```text
repro/
  papers/
    santana.pdf
    santana_supplement.xlsx
    wang.pdf
    wang_supplement.xlsx
  config/
    project_instructions.md
    datasets.yml
  artifacts/
    sra_metadata/
    run_condition_maps/
    gene_id_maps/
    published_tables/
    validation/
  prompts/
    00_bootstrap.md
    10_sra_metadata_plan.md
    20_count_workflow_plan.md
    30_split_collections_plan.md
    40_deseq2_plan.md
    50_validation_plan.md
  logs/
    cca_transcript_*.md
```

---

## Project Instructions (Put This in `config/project_instructions.md`)

Give CCA a single source of truth. Recommended rules:

- Always output a **plan first** and wait for approval.
- Do not modify Galaxy collections directly via API.
  - Use Galaxy’s **collection transformation tools** so steps are recorded in history.
- Write mapping tables with headers to `artifacts/`.
- For gene ID mapping across annotation versions:
  - Only use **authoritative annotation-based mapping** (e.g., GTF attributes such as `old_locus_tag`).
  - Include a verification method (sequence identity, exact mapping checks, etc.).
- Produce a final “Repro Summary” containing:
  - Galaxy history link(s)
  - workflow invocation(s)
  - tool versions if available
  - the run-to-condition mapping file(s)
  - gene-id mapping file(s)
  - validation outputs and metrics

---

## Dataset Targets (as in the paper)

Maintain a simple config file `config/datasets.yml` so you can run both datasets consistently.

Example (edit as needed):
```yaml
datasets:
  - name: santana
    bioproject: PRJNA904261
    # Add any paper-specific notes here (conditions, comparisons)
  - name: wang
    bioproject: PRJNA1086003
```

---

## End-to-End Workflow

---

## Prompts Actually Used in the Paper (and When to Use Them)

The manuscript shows **two explicit prompts** used with Claude Code Agent (CCA) for the key “organize data / split collection” step:

1) **Plan-only prompt (before any Galaxy actions)** — ask CCA to (a) download BioProject run metadata, (b) infer run→condition mapping from the manuscript + supplements, and (c) present a concrete plan for splitting the target Galaxy dataset collection.
2) **Execute prompt (after you review/approve the plan)** — instruct CCA to execute the approved plan and add name tags to the resulting condition-specific collections.

> **Tip (Claude Code feature):** Instead of relying on the phrase “PLAN ONLY”, you can run the **Plan-only prompt** while Claude Code is in **Plan Mode** (`⏸ plan mode on`).
> You can switch into Plan Mode during a session with **Shift+Tab** (cycle permission modes), or start directly with `claude --permission-mode plan`.

### Prompt 1 — Plan-only (paper text; fill placeholders as needed)

```text
I need to split Galaxy dataset collection #<COLLECTION_ID> into several collections corresponding to experimental
conditions described in the manuscript (check manuscript pdf and supplemental materials xlsx files in this directory).
In order to do this you need to download metadata for sequencing runs for bioproject <PRJNA...> to obtain accessions
and metadata. You should then figure out how SRA accessions correspond to experimental conditions described in the paper.
You should then present these finding to me, so that I can tell you what to do next.
```

### Prompt 2 — Execute (paper text; sent only after plan approval)

```text
Go ahead and execute the plan. Once you are done please add name tags to dataset collection containing data we need to used
for DeSeq2 analysis. E.g., label collections with names tags such as <COND_A>, <COND_B>, and <COND_C>.
```

### What the paper does *not* provide as explicit prompts

The paper describes additional steps (RNA-seq counting workflow, DESeq2 comparisons, gene-ID mapping, and validation),
but it **does not include explicit CCA prompt texts** for those steps in the main manuscript.

If you want to keep your reproduction “paper-faithful,” run those steps in Galaxy as described, and only use the two prompts
above to drive the collection-splitting portion.

---

### Step 1 — Acquire SRA metadata and build the run→condition mapping (CCA plan-first)

> Run this step in **Plan Mode** (recommended) if you want to guarantee “plan-only” behavior in Claude Code.

**Goal:** a deterministic table: `run_accession,sample_id,condition,label`

**Plan-only prompt (template):**
```text
You are reproducing a published RNA-seq re-analysis in Galaxy end-to-end.

Inputs:
- Manuscript PDF: ./papers/<paper>.pdf
- Supplement XLSX: ./papers/<supplement>.xlsx
- BioProject: <PRJNA...>

Task (PLAN ONLY, do not execute):
1) Download SRA run metadata for the BioProject and propose a mapping from run accessions (SRR/ERR) to sample identifiers.
2) Parse the supplement/manuscript to infer experimental condition/group labels used in the figures/analysis.
3) Propose a final run-to-condition mapping table:
   run_accession,sample_id,condition,label
4) Provide a QA checklist to validate the mapping before any analysis runs.
Output the plan and the draft mapping (CSV) path under:
  artifacts/run_condition_maps/<dataset>_run_condition_map.csv
```

**Review checklist (you do this):**
- Do the number of runs match the paper’s stated sample counts?
- Do condition labels match the manuscript figure captions?
- Any ambiguous samples? If yes, require CCA to resolve with citations to supplement rows.

After approval, allow CCA to execute **only** the metadata download + CSV generation locally (not Galaxy execution yet).

---

### Step 2 — Download raw reads from SRA into Galaxy (workflow-driven)

> Paper does not publish an exact CCA prompt for this step. If you use CCA anyway, **save your prompt + transcript** under `logs/`.

You must start from raw reads (FASTQ) and produce a counts matrix.

There are multiple valid Galaxy-native ways to do this (and tool availability may vary). The key requirement is:

- **All SRA → FASTQ acquisition must happen inside Galaxy** (so it is recorded and reproducible).
- The run list must be driven by your approved mapping CSV.

**Plan-only prompt (template):**
```text
PLAN ONLY. Based on the run_condition_map CSV we approved, propose the exact Galaxy steps to:
1) Ingest/download each run accession’s reads into Galaxy (paired-end if applicable).
2) Organize the resulting read datasets into a collection keyed by run accession or sample_id.
3) Ensure provenance is preserved and the history is cleanly labeled.
Do not execute yet.
```

**Execution guidance:**
- Prefer using an established Galaxy workflow that takes a list of run accessions and produces FASTQs.
- If you need an accession list input dataset, generate it from the mapping CSV and upload it to Galaxy.

---

### Step 3 — Run the RNA-seq “reads → counts” workflow in Galaxy

**Goal:** generate a **counts matrix** suitable for DESeq2, ideally as a dataset collection that preserves sample labels.

Your reproduction should:

- Use a single workflow for both datasets (unless the paper required dataset-specific adjustments)
- Record:
  - workflow name
  - tool versions (when visible)
  - key parameters (when non-default)

**Plan-only prompt (template):**
```text
PLAN ONLY. Propose how to run a Galaxy RNA-seq counting workflow on the reads collection to produce:
- per-sample counts
- a merged counts matrix or count matrix collection suitable for DESeq2
Include exact inputs/outputs and dataset naming conventions.
Do not execute yet.
```

Then execute the workflow in Galaxy (either manually or via CCA-controlled Galaxy actions), ensuring outputs are labeled by `sample_id`/`label`.

---

### Step 4 — Split/label the count matrix collection by condition using Galaxy collection tools (orchestrated by CCA)

This is the “agentic collection transformation” centerpiece. Requirements:

- Use Galaxy collection transformation tools (rules/filter/relabel/apply-rules).
- Do not “edit a collection” directly via API.
- Make the resulting condition collections clearly named/tagged.

**Plan-only prompt (template):**
```text
PLAN ONLY. Using the run_condition_map CSV, propose how to split the counts collection into
condition-specific collections using Galaxy collection transformation tools.
List:
- the Galaxy tools to use (rules/filter/relabel/apply-rules style tools)
- the intermediate mapping files needed (if any)
- final expected collections and names
Do not execute yet.
```

After approval, execute the plan and verify the history shows explicit tool steps for each transformation.

---

### Step 5 — Differential expression (DESeq2) in Galaxy

Run the paper’s pairwise comparisons.

**Plan-only prompt (template):**
```text
PLAN ONLY. Propose the DESeq2 comparisons to reproduce the paper:
- which condition-specific collections are compared
- any thresholds/filters applied to define significant DE genes
- expected outputs (tables and any plots)
Do not execute yet.
```

**Execution guidance:**
- Keep each comparison as a distinct, clearly labeled DESeq2 run.
- If the paper specifies significance/effect-size thresholds for a dataset, apply them consistently and record them.

---

### Step 6 — Gene ID mapping across annotation versions (deterministic, documented)

If the published study used an older annotation and your re-analysis uses a newer one, you must reconcile gene identifiers.

**Required approach**
- Use the annotation file(s) (GTF/GFF) to produce an authoritative mapping.
- Example pattern: mapping old IDs using an attribute like `old_locus_tag` to the new gene IDs.

**Plan-only prompt (template):**
```text
PLAN ONLY. Propose a deterministic gene ID mapping strategy across annotation versions:
- source files (GTF/GFF) and which attributes define the mapping
- the mapping output file format
- a verification method (sequence identity check or other deterministic validation)
Do not execute yet.
```

Then generate:
- `artifacts/gene_id_maps/<dataset>_old_to_new_gene_id_map.tsv`

---

### Step 7 — Extract published log2FC from supplement (CCA, local artifact)

The paper uses AI to convert supplement tables into a minimal CSV for validation:
- `gene_id,log2fc`

**Plan-only prompt (template):**
```text
PLAN ONLY. Parse the supplement XLSX and propose how to extract the published differential expression table(s)
required for validation. Output a CSV with:
  gene_id,log2fc
and document which supplement sheet/rows were used.
Do not execute yet.
```

Then execute extraction and save:
- `artifacts/published_tables/<dataset>_published_log2fc.csv`

---

### Step 8 — Validation against published results (no LLM shortcuts)

Create and run a validation notebook/script that:
1) Loads Galaxy DESeq2 output (Gene_ID, log2FoldChange, padj)
2) Loads `published_log2fc.csv`
3) Applies gene-ID mapping if needed
4) Merges and computes correlation / R²
5) Outputs plots and a metrics summary

Save outputs under:
- `artifacts/validation/<dataset>/`

**Minimal validation script outline (Python):**
- read DESeq2 TSV
- read published CSV
- apply mapping table (if needed)
- merge and compute correlation / R²
- scatter plot and save PNG

> Keep the notebook/script deterministic and fully auditable. Do not “let the LLM infer mappings” from log2FC patterns.

---

## Run Logging (So You Can Improve the Workflow Later)

To make your later “improvements” measurable, record the following per dataset:

- Galaxy history link
- workflow invocation IDs/links
- tool versions (when visible)
- run_condition_map CSV
- gene-id mapping TSV
- published log2FC CSV
- validation notebook + outputs
- the full CCA transcript (`logs/cca_transcript_*.md`)

---

## Expected Outputs Checklist

Per dataset you should have:

- [ ] `artifacts/run_condition_maps/<dataset>_run_condition_map.csv`
- [ ] A Galaxy history containing:
  - [ ] SRA → FASTQ ingestion steps
  - [ ] RNA-seq counting workflow invocation
  - [ ] collection transformations (as Galaxy tool steps)
  - [ ] DESeq2 comparisons (clearly labeled)
- [ ] `artifacts/gene_id_maps/<dataset>_old_to_new_gene_id_map.tsv` (if needed)
- [ ] `artifacts/published_tables/<dataset>_published_log2fc.csv`
- [ ] `artifacts/validation/<dataset>/` with plots + metrics

---

## Common Failure Modes (and How to Prevent Them)

1) **Run→condition mapping drift**
   - Stop early and fix the mapping CSV. Downstream results will be garbage otherwise.

2) **CCA suggests direct API collection edits**
   - Reject and restate: “Use Galaxy collection tools so the step is recorded in history.”

3) **Suspiciously perfect correlations**
   - Almost always indicates a bad join key or a non-authoritative gene-id mapping.
   - Require deterministic mapping sourced from annotation.

---