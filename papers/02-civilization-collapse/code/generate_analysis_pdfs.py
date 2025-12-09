#!/usr/bin/env python3
"""
Generate PDFs from Paper 2C Analysis Package markdown files.

Uses pandoc with full LaTeX scheme to convert markdown documents
to professional PDFs for distribution.

Usage:
    nix-shell -p texlive.combined.scheme-full pandoc librsvg --run \
        "python generate_analysis_pdfs.py"
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

# Configuration
ANALYSIS_DIR = Path(__file__).parent.parent / "analysis"
OUTPUT_DIR = Path(__file__).parent.parent / "analysis_pdfs"

# Documents to convert (in order of priority)
DOCUMENTS = [
    # Framework & Classification (NEW)
    ("LAWS_AND_REGULARITIES_TABLE.md", "Laws_Regularities_Classification"),
    ("COORDINATION_POLITICAL_ECONOMY.md", "Coordination_Political_Economy"),

    # Core Theory
    ("THE_17_LAWS_SUMMARY.md", "Complete_17_Laws_Reference"),
    ("LAW_15_METACOGNITIVE_COLLAPSE.md", "Law_15_Metacognitive_Collapse"),
    ("LAW_16_EVOLUTIONARY_STABILITY.md", "Law_16_Evolutionary_Stability"),
    ("LAW_17_AI_COORDINATION_PARADOX.md", "Law_17_AI_Coordination_Paradox"),

    # Cosmic Implications
    ("THE_GREAT_FILTER_RESOLUTION.md", "Great_Filter_Resolution"),
    ("WISDOM_SILENCE_HYPOTHESIS.md", "Wisdom_Silence_Hypothesis"),

    # Current Application
    ("EARTH_COORDINATION_STATUS_2025.md", "Earth_Status_2025"),
    ("COORDINATION_TECHNOLOGY_FRAMEWORK.md", "Technology_Framework"),
    ("INTERVENTION_STRATEGIES_PLAYBOOK.md", "Intervention_Playbook"),

    # Policy Briefs
    ("POLICY_BRIEF_AI_SAFETY.md", "Policy_Brief_AI_Safety"),
    ("POLICY_BRIEF_POLICYMAKERS.md", "Policy_Brief_Policymakers"),
    ("POLICY_BRIEF_TECH_INDUSTRY.md", "Policy_Brief_Tech_Industry"),
    ("POLICY_BRIEF_GENERAL_PUBLIC.md", "Policy_Brief_General_Public"),

    # Research & Extensions
    ("RESEARCH_AGENDA.md", "Research_Agenda"),
    ("THEORY_EXTENSIONS.md", "Theory_Extensions"),

    # Index
    ("README.md", "Analysis_Package_Index"),
]

# Pandoc options for professional PDF output with full Unicode support
PANDOC_OPTS = [
    "--pdf-engine=xelatex",
    "-V", "geometry:margin=1in",
    "-V", "fontsize=11pt",
    "-V", "colorlinks=true",
    "-V", "linkcolor=blue",
    "-V", "urlcolor=blue",
    "-V", "toccolor=blue",
    "--toc",
    "--toc-depth=3",
    "-V", "documentclass=article",
    "-V", "classoption=titlepage",
    "--highlight-style=tango",
    "-V", "mainfont=DejaVu Serif",
    "-V", "sansfont=DejaVu Sans",
    "-V", "monofont=DejaVu Sans Mono",
    "-V", "mathfont=DejaVu Math TeX Gyre",
]

def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def convert_to_pdf(md_file: Path, pdf_name: str) -> tuple[bool, str]:
    """Convert a markdown file to PDF using pandoc."""
    output_path = OUTPUT_DIR / f"{pdf_name}.pdf"

    cmd = [
        "pandoc",
        str(md_file),
        "-o", str(output_path),
        *PANDOC_OPTS,
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            size_kb = output_path.stat().st_size / 1024
            return True, f"Created: {pdf_name}.pdf ({size_kb:.1f} KB)"
        else:
            return False, f"Error: {result.stderr[:200]}"
    except subprocess.TimeoutExpired:
        return False, "Timeout (>120s)"
    except Exception as e:
        return False, f"Exception: {str(e)}"

def main():
    print("=" * 80)
    print("Paper 2C Analysis Package - PDF Generation")
    print("=" * 80)
    print(f"Input directory: {ANALYSIS_DIR}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print()

    ensure_output_dir()

    success_count = 0
    fail_count = 0
    results = []

    for md_filename, pdf_name in DOCUMENTS:
        md_path = ANALYSIS_DIR / md_filename

        if not md_path.exists():
            print(f"  ⚠ Skipping (not found): {md_filename}")
            continue

        print(f"  Converting: {md_filename} → {pdf_name}.pdf", end=" ... ")
        success, message = convert_to_pdf(md_path, pdf_name)

        if success:
            print(f"✓")
            success_count += 1
            results.append((pdf_name, "✓", message))
        else:
            print(f"✗")
            fail_count += 1
            results.append((pdf_name, "✗", message))

    # Summary
    print()
    print("=" * 80)
    print("Generation Summary")
    print("=" * 80)

    for pdf_name, status, message in results:
        print(f"  {status} {pdf_name}: {message}")

    print()
    print(f"Results: {success_count}/{success_count + fail_count} PDFs generated successfully")

    if success_count > 0:
        print()
        print(f"PDFs available in: {OUTPUT_DIR}")
        print()
        print("Generated files:")
        for f in sorted(OUTPUT_DIR.glob("*.pdf")):
            size_kb = f.stat().st_size / 1024
            print(f"  - {f.name} ({size_kb:.1f} KB)")

    return 0 if fail_count == 0 else 1

if __name__ == "__main__":
    exit(main())
