# Prompt Template: Validation Against Published Results

**Purpose**: Extract published DE results and validate reproduction accuracy
**Reference**: README.md Steps 7-8
**Paper Provides Explicit Prompt**: NO

---

## Context

The final step: extract the paper's published differential expression results and compare to your re-analysis. This validates that the reproduction is accurate.

**Requirements**:
- Deterministic validation (no LLM shortcuts)
- Clear metrics (correlation, R², scatter plots)
- Document any discrepancies

---

## Step 7: Extract Published Results

### Prompt Template (Plan Mode)

```
You need to extract published differential expression results from the paper supplement.

Context:
- Dataset: <DATASET_NAME>
- Supplement file: papers/<SUPPLEMENT_NAME>.<xlsx|pdf>
- Paper: papers/<PAPER_NAME>.pdf

Task (PLAN ONLY):
1) Identify which supplement table(s) contain differential expression results:
   - Gene identifiers
   - Log2 fold change values
   - P-values or adjusted p-values (if available)
   - Which comparison they represent

2) Extract the published data into a clean CSV:
   - Format: gene_id,log2fc,padj (if available)
   - Use gene ID format as published (note if old annotation)
   - Document which supplement sheet/table/rows used
   - Handle multiple comparisons (one file per comparison if needed)

3) Save to: artifacts/published_tables/<DATASET>_<COMPARISON>_published_log2fc.csv

4) Document extraction process for reproducibility

Do not execute yet.
```

### Expected Output

**File**: `artifacts/published_tables/<DATASET>_<COMPARISON>_published_log2fc.csv`

**Format**:
```csv
gene_id,log2fc,padj
gene_1,2.34,0.001
gene_2,-1.87,0.023
gene_3,0.45,0.234
...
```

**Metadata**: Document in file header or separate .txt:
- Source: supplement file name, sheet name, table number
- Comparison represented
- Number of genes
- Gene ID format (if old annotation version)
- Any filtering applied by paper (e.g., only significant genes reported)

---

## Step 8: Validation Analysis

### Prompt Template (Plan Mode)

```
You need to validate your DESeq2 re-analysis results against the published results.

Context:
- Your DESeq2 results: Galaxy dataset <DATASET_ID>
- Published results: artifacts/published_tables/<DATASET>_<COMPARISON>_published_log2fc.csv
- Gene ID mapping (if needed): artifacts/gene_id_maps/<DATASET>_old_to_new_gene_id_map.tsv

Task (PLAN ONLY):
1) Create a validation notebook/script that:
   a) Loads your DESeq2 results (gene_id, log2FoldChange, padj)
   b) Loads published results
   c) Applies gene ID mapping if annotation versions differ
   d) Merges datasets on gene_id
   e) Computes validation metrics:
      - Pearson correlation (r)
      - Spearman correlation (rho)
      - R² value
      - Mean absolute error (MAE)
      - Root mean squared error (RMSE)
   f) Creates visualizations:
      - Scatter plot: published log2FC (x) vs re-analysis log2FC (y)
      - Residual plot
      - Histogram of differences
   g) Identifies outliers:
      - Genes with large discrepancies (|difference| > threshold)
      - Possible reasons for discrepancies

2) Save outputs to: artifacts/validation/<DATASET>_<COMPARISON>/
   - validation_metrics.txt (correlation, R², etc.)
   - scatter_plot.png
   - residual_plot.png
   - outliers.csv (if any)
   - validation_notebook.ipynb (or .py script)

3) Requirements:
   - NO LLM inference of gene mappings from expression patterns
   - Use only authoritative gene ID mapping from Step 6
   - Deterministic, reproducible analysis
   - Clear documentation of any data filtering

Do not execute yet.
```

### Expected Outputs

**Directory**: `artifacts/validation/<DATASET>_<COMPARISON>/`

**Files**:
1. `validation_metrics.txt`:
   ```
   Dataset: santana
   Comparison: treated_vs_control

   Genes compared: 15432
   Pearson r: 0.94
   Spearman rho: 0.92
   R²: 0.88
   MAE: 0.23
   RMSE: 0.41

   Interpretation: Strong agreement between published and re-analysis results
   ```

2. `scatter_plot.png`: Published vs re-analysis log2FC scatter plot with:
   - Identity line (x=y)
   - Regression line
   - Correlation coefficient in title/legend
   - Axis labels

3. `outliers.csv`: Genes with large discrepancies (if any)
   ```csv
   gene_id,published_log2fc,reanalysis_log2fc,difference,notes
   gene_123,3.45,0.12,3.33,Possible annotation issue
   gene_456,-2.11,0.89,-3.00,Check mapping
   ```

4. `validation_notebook.ipynb`: Full analysis code

---

## Interpretation Guidelines

### Good Agreement
- Pearson r > 0.85
- R² > 0.70
- Few outliers

**Interpretation**: Successful reproduction

### Moderate Agreement
- Pearson r: 0.70-0.85
- R² : 0.50-0.70
- Some systematic bias visible

**Interpretation**: Investigate discrepancies (annotation differences, tool versions, filtering)

### Poor Agreement
- Pearson r < 0.70
- R² < 0.50
- Many outliers or systematic errors

**Interpretation**: Likely issue with:
- Gene ID mapping (verify using authoritative source)
- Wrong comparison matched
- Different filtering applied
- Annotation version mismatch not properly handled

---

## Common Issues

### Issue: Suspiciously Perfect Correlation (r > 0.99)
**Likely cause**: Wrong join key (e.g., joined on row number instead of gene ID)
**Action**: Verify gene IDs match explicitly

### Issue: Very Low Correlation (r < 0.3)
**Likely cause**:
- Compared wrong comparisons (e.g., treated_vs_control in paper vs treated_vs_baseline in re-analysis)
- Gene ID mapping failed (wrong attribute used)
**Action**: Verify comparison match and gene mapping

### Issue: Good Correlation But Systematic Shift
**Likely cause**: Different normalization or dispersion estimation
**Action**: Document, acceptable if correlation is strong

---

## Logging

Document in logs/:
- Extraction prompt used
- Validation prompt used
- Which supplement tables extracted
- Gene ID mapping applied (if any)
- Validation metrics achieved
- Outliers identified
- Interpretation of results
- Any issues and resolutions

---

## Final Deliverable

Create: `artifacts/validation/<DATASET>/repro_summary.md`

Include:
- Galaxy history URL(s)
- Workflow invocation IDs
- Tool versions used
- Run-to-condition mapping file
- Gene ID mapping file (if used)
- Validation metrics for each comparison
- Overall assessment: reproduction successful? issues identified?
- Recommendations for improvements

---

## Next Steps

If validation successful:
- [ ] Archive artifacts, logs, and Galaxy histories
- [ ] Document any improvements identified for future work
- [ ] Consider extracting Galaxy workflow for sharing

If validation has issues:
- [ ] Investigate discrepancies systematically
- [ ] Verify each step (mapping, filtering, tool parameters)
- [ ] Document findings and iterate
