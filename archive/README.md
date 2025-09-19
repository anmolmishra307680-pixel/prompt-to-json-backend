# Archive Directory

This directory contains heavy artifacts and large files that have been moved out of the main repository to keep it clean and lightweight.

## Contents

### `/logs/`
- `feedback_log.json` - RL feedback training data
- `iteration_logs.json` - RL training iteration history

### `/reports/`
- `evaluation_report_*.json` - Historical evaluation reports
- Generated evaluation results from testing and development

### `/spec_outputs/`
- `design_spec_*.json` - Historical specification outputs
- Generated specifications from testing and development

## Purpose

These files have been archived to:
- Keep the main repository lightweight for cloning and CI/CD
- Preserve historical data for analysis
- Maintain clean development environment
- Reduce repository size for faster operations

## Restoration

If you need any of these files for analysis or debugging:
1. Copy the required files back to their original locations
2. The application will continue to generate new files in the main directories
3. Use `.gitignore` patterns to prevent re-committing large files

## File Patterns Archived

- Large JSON logs and outputs (>1KB)
- Historical training data
- Development test outputs
- Temporary database files
- Coverage reports and build artifacts