# Wang validation

Inputs needed:
- DESeq2 TSVs from Galaxy for in vitro and in vivo AR0382 vs AR0387
- Published log2FC CSV (to be created once supplementary XLSX are available)
- Mapping TSV: artifacts/gene_id_maps/wang_old_to_new_gene_id_map.tsv

Use artifacts/validation/validate_log2fc.py with --comparison set to in_vitro or in_vivo.
