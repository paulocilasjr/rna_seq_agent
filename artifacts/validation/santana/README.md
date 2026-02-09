# Santana validation

Inputs needed:
- DESeq2 TSV from Galaxy for tnSWI1 vs AR0382_WT
- DESeq2 TSV from Galaxy for AR0387_WT vs AR0382_WT
- Published log2FC CSV: artifacts/published_tables/santana_published_log2fc.csv
- Mapping TSV: artifacts/gene_id_maps/santana_old_to_new_gene_id_map.tsv

Use artifacts/validation/validate_log2fc.py with --comparison set to the pairwise comparison.
