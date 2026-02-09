#!/usr/bin/env python3
"""Validate DESeq2 log2FC against published values.

Usage:
  python artifacts/validation/validate_log2fc.py \
    --deseq2 <deseq2_tsv> \
    --published <published_csv> \
    --mapping <old_to_new_tsv> \
    --outdir <outdir> \
    --comparison <comparison_name>

Notes:
- DESeq2 file should include columns: gene_id (or Gene_ID) and log2FoldChange.
- Published file should include columns: gene_id and log2fc (optionally comparison/source_sheet).
- Mapping file should include columns: old_gene_id, new_gene_id.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def _normalize_cols(df: pd.DataFrame) -> pd.DataFrame:
    cols = {c.lower(): c for c in df.columns}
    # Normalize gene_id
    if 'gene_id' in cols:
        df = df.rename(columns={cols['gene_id']: 'gene_id'})
    elif 'geneid' in cols:
        df = df.rename(columns={cols['geneid']: 'gene_id'})
    # Normalize log2FC
    for key in ['log2foldchange', 'log2fc']:
        if key in cols:
            df = df.rename(columns={cols[key]: 'log2fc'})
            break
    return df


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--deseq2', required=True, help='DESeq2 TSV path')
    ap.add_argument('--published', required=True, help='Published log2fc CSV path')
    ap.add_argument('--mapping', required=False, help='old->new gene ID mapping TSV')
    ap.add_argument('--outdir', required=True, help='Output directory')
    ap.add_argument('--comparison', required=False, help='Comparison label for outputs')
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    deseq = pd.read_csv(args.deseq2, sep='\t')
    deseq = _normalize_cols(deseq)
    if 'gene_id' not in deseq.columns or 'log2fc' not in deseq.columns:
        raise SystemExit('DESeq2 file must have gene_id and log2FoldChange/log2fc columns')

    pub = pd.read_csv(args.published)
    pub = _normalize_cols(pub)
    if 'gene_id' not in pub.columns or 'log2fc' not in pub.columns:
        raise SystemExit('Published file must have gene_id and log2fc columns')

    if args.mapping:
        mapping = pd.read_csv(args.mapping, sep='\t')
        mapping = mapping.rename(columns={'old_gene_id': 'gene_id', 'new_gene_id': 'mapped_gene_id'})
        pub = pub.merge(mapping[['gene_id', 'mapped_gene_id']], on='gene_id', how='left')
        pub['merge_gene_id'] = pub['mapped_gene_id'].fillna(pub['gene_id'])
    else:
        pub['merge_gene_id'] = pub['gene_id']

    merged = pub.merge(deseq[['gene_id','log2fc']], left_on='merge_gene_id', right_on='gene_id', suffixes=('_pub','_deseq'))

    if merged.empty:
        raise SystemExit('No overlapping genes after merge. Check gene IDs and mapping.')

    x = merged['log2fc_pub'].astype(float)
    y = merged['log2fc_deseq'].astype(float)

    r = np.corrcoef(x, y)[0, 1]
    r2 = r ** 2
    direction_agree = (np.sign(x) == np.sign(y)).mean()

    comp = args.comparison or 'comparison'
    merged_out = outdir / f'{comp}_merged_log2fc.tsv'
    merged.to_csv(merged_out, sep='\t', index=False)

    fig_out = outdir / f'{comp}_log2fc_scatter.png'
    plt.figure(figsize=(6, 6))
    plt.scatter(x, y, s=8, alpha=0.6)
    lim = max(np.abs(x).max(), np.abs(y).max())
    plt.plot([-lim, lim], [-lim, lim], 'r--', linewidth=1)
    plt.xlabel('Published log2FC')
    plt.ylabel('DESeq2 log2FC')
    plt.title(f'{comp} (R²={r2:.4f}, direction={direction_agree:.3f})')
    plt.tight_layout()
    plt.savefig(fig_out, dpi=150)

    summary_out = outdir / f'{comp}_validation_summary.txt'
    summary_out.write_text(
        f'comparison\t{comp}\n'
        f'genes_compared\t{len(merged)}\n'
        f'pearson_r\t{r:.6f}\n'
        f'r2\t{r2:.6f}\n'
        f'direction_agreement\t{direction_agree:.6f}\n'
    )

    print('wrote', merged_out)
    print('wrote', fig_out)
    print('wrote', summary_out)


if __name__ == '__main__':
    main()
