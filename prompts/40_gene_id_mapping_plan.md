# Prompt Template: Gene ID Mapping Across Annotation Versions

**Purpose**: Create authoritative mapping between old and new gene IDs
**Reference**: README.md Step 6
**Paper Provides Explicit Prompt**: NO

---

## Context

If your analysis uses a different genome annotation version than the published paper, gene IDs may differ. A deterministic, verifiable mapping is required.

**CRITICAL RULES** (from CLAUDE.md):
- Only use authoritative annotation-based mapping
- Never infer mappings from expression patterns
- Never let LLM guess correspondences
- Always include deterministic verification

---

## When to Use This Step

Only if:
- Paper used annotation version X (e.g., GCF_000001405.25)
- Your re-analysis uses annotation version Y (e.g., GCF_000001405.40)
- Gene IDs have changed between versions (e.g., gene_12345 → gene_67890)

If using the same annotation version, skip this step.

---

## Prerequisites

- [ ] Know which annotation version paper used
- [ ] Know which annotation version your re-analysis used
- [ ] Have access to both annotation files (GTF/GFF)
- [ ] Identified which annotation attribute provides mapping (e.g., `old_locus_tag`, `gene_synonym`)

---

## Prompt Template (Plan Mode)

```
You need to create a deterministic gene ID mapping between two genome annotation versions.

Context:
- Paper used annotation: <OLD_ANNOTATION_VERSION>
- Re-analysis used annotation: <NEW_ANNOTATION_VERSION>
- Organism: <ORGANISM_NAME>

Requirements (NON-NEGOTIABLE):
1) Mapping MUST be sourced from annotation files only
2) Use annotation attributes (e.g., old_locus_tag, gene_synonym, etc.)
3) NO inference from expression patterns or correlations
4) NO LLM guessing or "hand-waving"
5) Include deterministic verification method

Task (PLAN ONLY):
1) Identify which GTF/GFF attribute(s) provide the old→new gene ID mapping
2) Parse both annotation files to extract the mapping
3) Create output file: artifacts/gene_id_maps/<DATASET>_old_to_new_gene_id_map.tsv
   Format: old_gene_id\tnew_gene_id
4) Implement verification:
   - Sequence identity check (if feasible)
   - OR exact attribute matching validation
   - OR coordinate overlap verification
5) Report mapping statistics:
   - Total genes in old annotation
   - Total genes in new annotation
   - Successfully mapped genes
   - Unmapped genes (and why)
   - Many-to-one or one-to-many mappings (if any)

Do not execute yet.
```

---

## Review Checklist

- [ ] Mapping source clearly documented (GTF/GFF file + attribute name)
- [ ] Method is deterministic (no inference, no guessing)
- [ ] Verification method is concrete and reproducible
- [ ] Statistics make sense (high mapping rate expected for related versions)
- [ ] Ambiguous cases handled explicitly (document, don't guess)

---

## Expected Output

**File**: `artifacts/gene_id_maps/<DATASET>_old_to_new_gene_id_map.tsv`

**Format**:
```tsv
old_gene_id	new_gene_id
gene_1	gene_1	# Unchanged
gene_2	gene_2	# Unchanged
old_gene_3	new_gene_10	# Renamed
old_gene_4	new_gene_11	# Renamed
...
```

**Metadata File**: `artifacts/gene_id_maps/<DATASET>_mapping_metadata.txt`

Document:
- Old annotation version and source
- New annotation version and source
- Attribute used for mapping
- Date mapping created
- Mapping statistics
- Verification method and results
- Known issues or ambiguities

---

## Verification Requirements

Choose ONE deterministic verification method:

### Option A: Sequence Identity
- Extract gene sequences from both annotations
- Compute identity for mapped pairs
- Expect >99% identity for correct mappings

### Option B: Coordinate Overlap
- Compare genomic coordinates for mapped pairs
- Expect high overlap (>80%) for correct mappings

### Option C: Exact Attribute Matching
- Verify old_locus_tag in new annotation exactly matches old gene_id
- No fuzzy matching allowed

---

## Common Pitfalls (AVOID!)

❌ Using BLAST or sequence similarity to "guess" mappings
❌ Using expression correlation between old and new data
❌ LLM inferring mappings from gene names or descriptions
❌ Mapping based on gene order or chromosome position alone
❌ Accepting "suspiciously perfect" correlations in validation (indicates wrong join key)

---

## Logging

Document in logs/:
- Prompt used
- Annotation files used
- Attribute used for mapping
- Verification method and results
- Mapping statistics
- Any manual decisions
- Issues encountered and resolutions

---

## Next Step

Proceed to Step 7: Extract published log2FC from supplement
See prompts/50_validation_plan.md
