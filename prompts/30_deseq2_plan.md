# Prompt Template: DESeq2 Differential Expression Analysis

**Purpose**: Run pairwise DESeq2 comparisons between experimental conditions
**Reference**: README.md Step 5
**Paper Provides Explicit Prompt**: NO (describe actions only)

---

## Context

With count data organized by condition, run DESeq2 to identify differentially expressed genes. The paper describes the comparisons but does not provide explicit prompt text.

---

## Prerequisites

- [ ] Condition-specific count collections exist in Galaxy
- [ ] Know which pairwise comparisons to run (from paper)
- [ ] Know significance thresholds (padj, log2FC) if specified in paper
- [ ] Galaxy history ID

---

## Prompt Template (Plan Mode)

```
You are running differential expression analysis for a published RNA-seq reproduction.

Context:
- Dataset: <DATASET_NAME>
- Paper: papers/<PAPER_NAME>.pdf
- Condition collections created in previous step

Task (PLAN ONLY):
1) Review the paper to identify which pairwise comparisons were performed:
   - Which conditions were compared?
   - What were the biological questions?
   - Were there specific significance thresholds (padj < 0.05, |log2FC| > 1, etc.)?

2) For each comparison, plan to run DESeq2 in Galaxy:
   - Tool: DESeq2 (or equivalent)
   - Inputs: Condition-specific count collections
   - Comparison: condition_A vs condition_B
   - Parameters: Any non-default settings from paper
   - Output naming: Clear, descriptive names for each comparison

3) Specify expected outputs:
   - DESeq2 results tables (gene_id, baseMean, log2FoldChange, pvalue, padj)
   - Any plots (MA plot, volcano plot, etc.)
   - Filtered gene lists (if applying thresholds)

4) Provide a verification checklist

Do not execute yet - present the plan for review.
```

---

## Review Checklist

- [ ] Comparisons match paper's stated analyses
- [ ] All relevant pairwise comparisons included
- [ ] Significance thresholds match paper (or are documented if different)
- [ ] Output naming is clear and consistent
- [ ] Control/reference condition correctly specified for each comparison

---

## Expected Outputs

For each comparison:

1. **DESeq2 results table** with columns:
   - Gene ID
   - baseMean
   - log2FoldChange
   - lfcSE
   - stat
   - pvalue
   - padj

2. **Plots** (optional, for QC):
   - MA plot
   - PCA plot
   - Dispersion estimates plot

3. **Filtered lists** (if applying cutoffs):
   - Significant genes (padj < threshold)
   - Up-regulated genes (log2FC > threshold, padj < threshold)
   - Down-regulated genes (log2FC < -threshold, padj < threshold)

---

## Logging

Document in logs/:
- Prompt used
- Comparisons planned
- Review notes
- Execution results
- Galaxy history URL
- Dataset IDs for DESeq2 outputs
- Any parameter choices
- Tool versions (if available)

---

## Next Step

Proceed to Step 6: Gene ID mapping (if annotation versions differ)
See prompts/40_gene_id_mapping_plan.md
