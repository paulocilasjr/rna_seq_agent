# Project Instructions for Claude Code Agent (CCA)

## Core Workflow Policy

### Plan → Review → Execute
- **Always output a plan first** and wait for approval before executing
- Never make changes without explicit approval
- Major steps require explicit planning phase

## Provenance Rules (CRITICAL)

### Galaxy Collection Transformations
- **Do not modify Galaxy collections directly via API**
- **Use Galaxy's collection transformation tools** so all steps are recorded in history
- All collection operations must be visible and extractable into workflows
- Prefer the `/galaxy-transform-collection` slash command for collection operations

### Why This Matters
- Ensures reproducibility
- Makes workflows extractable and shareable
- Maintains complete provenance chain from raw data to results

## Artifact Management

### Required Outputs
Write all mapping tables and intermediate data to `artifacts/` with appropriate subdirectories:

- `artifacts/sra_metadata/` - Downloaded SRA/BioProject metadata
- `artifacts/run_condition_maps/` - Run accession to experimental condition mappings
- `artifacts/gene_id_maps/` - Gene ID mappings across annotation versions
- `artifacts/published_tables/` - Extracted data from paper supplements (e.g., published log2FC values)
- `artifacts/validation/` - Validation outputs, metrics, and plots

### File Format Requirements
- All mapping tables must include headers
- Use CSV or TSV format for tabular data
- Name files descriptively: `<dataset>_<type>_<description>.<ext>`
- Example: `santana_run_condition_map.csv`

## Gene ID Mapping Rules (CRITICAL)

When mapping gene IDs across annotation versions:

### 1. Use Authoritative Annotation-Based Mapping ONLY
- Source mappings from GTF/GFF annotation files
- Use annotation attributes (e.g., `old_locus_tag`, `gene_synonym`)
- **Never infer mappings from expression patterns or "good-looking" correlations**
- **Never allow LLM to guess or hand-wave gene ID correspondences**

### 2. Include Deterministic Verification
Every gene ID mapping must include:
- Verification method (e.g., sequence identity check, exact attribute matching)
- Documentation of mapping source and version
- Count of successfully mapped vs unmapped genes
- Quality metrics (% coverage, ambiguous mappings)

### 3. Document Everything
- Record annotation file sources and versions
- Document which attributes were used for mapping
- Note any manual decisions or ambiguities
- Save verification outputs to `artifacts/gene_id_maps/`

## Final Reproducibility Summary Checklist

After completing a dataset reproduction, produce a "Repro Summary" document containing:

### Required Information
- [ ] **Galaxy history link(s)** - Direct URLs to usegalaxy.org histories
- [ ] **Workflow invocation(s)** - Invocation IDs and workflow names
- [ ] **Tool versions** - Record when available from Galaxy history
- [ ] **Run-to-condition mapping file(s)** - Path to CSV/TSV in artifacts/
- [ ] **Gene ID mapping file(s)** - Path to mapping tables (if applicable)
- [ ] **Validation outputs and metrics** - Correlation/R² values, plots, comparison results

### Format
Save as: `artifacts/validation/<dataset>/<dataset>_repro_summary.md`

## Logging Requirements

- Log every important prompt/decision under `logs/` with timestamps
- Include full CCA transcripts for auditing and improvement
- Format: `logs/cca_transcript_YYYY-MM-DD_HHMMSS_<step>.md`

## Common Failure Modes to Avoid

1. **Suspiciously perfect correlations** → Almost always indicates bad gene ID mapping
2. **Direct API collection manipulation** → Reject and require Galaxy tools
3. **Run-condition mapping drift** → Fix immediately before downstream analysis
4. **Missing tool versions** → Always attempt to record from Galaxy history
5. **Unverified gene mappings** → Require deterministic verification step
