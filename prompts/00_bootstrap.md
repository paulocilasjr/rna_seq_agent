# Prompt: Repository Bootstrap

**Date**: 2026-01-28
**Purpose**: Initial repository setup and verification
**Dataset**: N/A (infrastructure setup)

---

## Original Request

Set up the local repository to match the paper/README reproduction requirements exactly.

---

## Constraints

- Follow Plan → Review → Execute
- Do not reveal secrets (GALAXY_API_KEY)
- Do not run any Galaxy jobs yet
- Prefer idempotent actions (safe to re-run)

---

## Verification Checklist

- [x] Directory structure exists (papers/, config/, artifacts/, prompts/, logs/, .claude/commands/)
- [x] CLAUDE.md exists with repo rules
- [x] config/project_instructions.md exists
- [x] config/datasets.yml exists with santana and wang datasets
- [x] .gitignore exists
- [x] .claude/commands/galaxy-transform-collection.md exists
- [x] .env.example created
- [x] GALAXY_API_KEY status documented
- [x] Initial prompt templates created
- [x] Bootstrap log entry created

---

## Outcome

Repository structure verified and documented. Ready for workflow execution once GALAXY_API_KEY is set.

---

## Next Steps

1. User must set GALAXY_API_KEY in environment
2. Begin Step 1: SRA metadata acquisition (see prompts/10_sra_metadata_plan.md)
