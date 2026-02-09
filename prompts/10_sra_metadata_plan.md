# Prompt Template: SRA Metadata Acquisition & Run-to-Condition Mapping

**Purpose**: Download SRA metadata and create deterministic run-to-condition mapping
**Reference**: README.md Step 1
**Paper Provides Explicit Prompt**: YES (for collection splitting, not metadata acquisition)

---

## Context

This step creates the foundational mapping between SRA run accessions (SRR*/ERR*) and experimental conditions as described in the paper's supplementary materials.

**Critical Requirement**: The mapping must be deterministic, auditable, and match the paper's stated sample organization.

---

## Inputs Required

Before prompting, gather:

1. **Dataset identifier**: `santana` or `wang`
2. **BioProject accession**: From config/datasets.yml
3. **Paper PDF**: Location in papers/ directory
4. **Supplement file**: Location in papers/ directory (XLSX or PDF)

---

## Prompt Template (Plan Mode)

```
You are reproducing a published RNA-seq re-analysis in Galaxy end-to-end.

Inputs:
- Manuscript PDF: ./papers/<PAPER_NAME>.pdf
- Supplement file: ./papers/<SUPPLEMENT_NAME>.<xlsx|pdf>
- BioProject: <PRJNA######>
- Dataset name: <DATASET_NAME>

Task (PLAN ONLY, do not execute):
1) Download SRA run metadata for BioProject <PRJNA######>
2) Parse the supplement/manuscript to identify:
   - Sample identifiers used in the paper
   - Experimental conditions/groups/treatments
   - Which SRA runs correspond to which conditions
3) Create a mapping table with columns:
   run_accession,sample_id,condition,label
4) Save proposed mapping to:
   artifacts/run_condition_maps/<DATASET_NAME>_run_condition_map.csv
5) Provide a QA checklist for me to validate before proceeding

Requirements:
- Mapping must be deterministic and reproducible
- All run accessions from the BioProject must be accounted for
- Condition labels must match those used in paper figures/tables
- Document any ambiguities or assumptions
```

---

## Review Checklist

Before approving execution:

- [ ] Run count matches paper's stated sample count
- [ ] Condition labels match paper's nomenclature
- [ ] All SRA accessions mapped (no orphans)
- [ ] Mapping is unambiguous (no guesses)
- [ ] Sample replicates properly identified
- [ ] Any technical vs biological replicates distinguished

---

## Expected Output

**File**: `artifacts/run_condition_maps/<DATASET_NAME>_run_condition_map.csv`

**Format**:
```csv
run_accession,sample_id,condition,label
SRR12345678,sample_1,control,control_rep1
SRR12345679,sample_2,control,control_rep2
SRR12345680,sample_3,treated,treated_rep1
...
```

---

## Logging

After completion, document in logs/:
- Prompt used (if modified from template)
- Any ambiguities resolved
- Manual decisions made
- Link to SRA metadata source
- Verification results

---

## Next Step

Proceed to Step 2: SRA to FASTQ ingestion (requires Galaxy operations)
