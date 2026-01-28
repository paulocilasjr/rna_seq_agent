# RNA-Seq Agent Project

Agentic Galaxy workflow automation for RNA-seq analysis via usegalaxy.org API.

**Key Resource**: Use `/galaxy-transform-collection` slash command for collection operations (see `.claude/commands/galaxy-transform-collection.md`)

---

## Core Rules

### 1. Workflow Discipline
- **Always follow Plan → Review → Execute** for any major action
- Get approval before making significant changes

### 2. Galaxy Integration
- This project reproduces agentic Galaxy workflows using the **usegalaxy.org API**
- Galaxy API key MUST be set in environment variable:
  ```bash
  export GALAXY_API_KEY="your_key_here"
  ```
- **Never commit API keys** to version control

### 3. Provenance Requirement (CRITICAL)
- **Never manipulate Galaxy dataset collections via opaque API edits**
- Always use **Galaxy-native collection transformation tools**
- **Prefer `/galaxy-transform-collection` slash command** for all collection operations
- Ensures all steps are recorded in Galaxy history for reproducibility and workflow extraction

### 4. Logging & Artifacts
- Log every important prompt/decision under `logs/` with timestamps
- Store deterministic artifacts under `artifacts/`:
  - `gene_id_maps/` - gene ID mapping tables
  - `published_tables/` - supplementary data from papers
  - `run_condition_maps/` - experimental condition mappings
  - `sra_metadata/` - SRA/GEO metadata
  - `validation/` - verification outputs

### 5. Gene ID Mapping
- When gene IDs differ across annotation versions:
  - **Only use authoritative mapping from annotation** (e.g., `old_locus_tag` field)
  - **Never infer or guess mappings**
  - Always include a **deterministic verification step** to validate mapping accuracy
  - Document mapping source and version in artifacts

---

## Project Structure

```
├── artifacts/          # Deterministic data artifacts
├── config/            # Configuration files
├── logs/              # Timestamped decision logs
├── prompts/           # Prompt templates
├── papers/            # Reference publications
└── .claude/commands/  # Custom slash commands
```

---

## Best Practices

- All Galaxy operations must be reproducible and traceable
- Maintain provenance chain from raw data to final results
- Document all manual interventions in logs/
- Use Galaxy tools even when direct API calls seem faster (for reproducibility)
