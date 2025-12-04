#!/usr/bin/env python3
"""
Generate PDF Documents for Nature Submission
=============================================

Creates professional PDFs from markdown documentation:
1. Supplementary Materials PDF (complete package)
2. Executive Summary PDF (2-page polished)
3. H₇ Manuscript Sections PDF (ready for insertion)
4. Cover Letter template PDF

Uses pandoc for high-quality PDF generation.
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

# Base directory
BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")
OUTPUT_DIR = BASE_DIR / "submission_pdfs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Pandoc settings for Nature-quality PDFs
PANDOC_COMMON_ARGS = [
    "--pdf-engine=xelatex",
    "--variable=geometry:margin=1in",
    "--variable=fontsize:11pt",
    "--variable=documentclass:article",
    "--number-sections",
    "--toc",
    "--highlight-style=tango",
]

def run_pandoc(input_files, output_file, title, additional_args=None):
    """Run pandoc to generate PDF."""
    args = [
        "pandoc",
        *input_files,
        "-o", str(output_file),
        f"--metadata=title:{title}",
        f"--metadata=date:{datetime.now().strftime('%B %d, %Y')}",
        *PANDOC_COMMON_ARGS,
    ]

    if additional_args:
        args.extend(additional_args)

    print(f"Generating: {output_file.name}")
    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode == 0:
        size_mb = output_file.stat().st_size / (1024 * 1024)
        print(f"  ✓ Created: {output_file.name} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"  ✗ Error: {result.stderr}")
        return False

def create_supplementary_materials_pdf():
    """Create comprehensive supplementary materials PDF."""
    print("\n" + "="*80)
    print("1. Creating Supplementary Materials PDF")
    print("="*80)

    # Combine supplementary materials
    input_files = [
        str(BASE_DIR / "manuscript/supplementary/SUPPLEMENTARY_METHODS.md"),
        str(BASE_DIR / "manuscript/supplementary/SUPPLEMENTARY_TABLES.md"),
    ]

    output_file = OUTPUT_DIR / "H7_Supplementary_Materials.pdf"

    return run_pandoc(
        input_files,
        output_file,
        "Supplementary Materials: Validated H₇ (Evolutionary Progression) Component",
        additional_args=["--variable=fontsize:10pt"]  # Smaller font for supplement
    )

def create_executive_summary_pdf():
    """Create polished 2-page executive summary PDF."""
    print("\n" + "="*80)
    print("2. Creating Executive Summary PDF")
    print("="*80)

    input_files = [str(BASE_DIR / "EXECUTIVE_SUMMARY_ONE_PAGE.md")]
    output_file = OUTPUT_DIR / "H7_Executive_Summary.pdf"

    return run_pandoc(
        input_files,
        output_file,
        "H₇ Evolutionary Progression: Executive Summary",
        additional_args=["--variable=fontsize:11pt"]
    )

def create_manuscript_sections_pdf():
    """Create PDF with H₇ manuscript sections ready for insertion."""
    print("\n" + "="*80)
    print("3. Creating H₇ Manuscript Sections PDF")
    print("="*80)

    input_files = [
        str(BASE_DIR / "manuscript/H7_METHODS_SECTION_TEXT.md"),
        str(BASE_DIR / "manuscript/H7_RESULTS_SECTION_TEXT.md"),
        str(BASE_DIR / "manuscript/H7_DISCUSSION_SECTION_TEXT.md"),
    ]

    output_file = OUTPUT_DIR / "H7_Manuscript_Sections.pdf"

    return run_pandoc(
        input_files,
        output_file,
        "H₇ Manuscript Sections for Integration",
        additional_args=["--variable=fontsize:12pt"]
    )

def create_cover_letter_pdf():
    """Create Nature cover letter template PDF."""
    print("\n" + "="*80)
    print("4. Creating Cover Letter Template PDF")
    print("="*80)

    # Create cover letter markdown
    cover_letter_md = OUTPUT_DIR / "cover_letter_template.md"

    cover_letter_content = """# Cover Letter: Validated H₇ Component for Historical K(t) Index

**To**: Editor, *Nature*
**Date**: {date}
**Subject**: Submission of "Historical K(t) Index for Civilizational Coherence (1810-2020)"

Dear Editor,

We are pleased to submit our manuscript on the historical K(t) coherence index, featuring a validated empirical operationalization of the H₇ (Evolutionary Progression) component.

## Key Innovation

Our validated H₇ component represents a significant methodological advancement: we replace demographic proxies with **direct empirical measures** integrating education, innovation (patents), infrastructure, and governance. Critically, this validation reveals a **more conservative assessment** than previous approaches—validated H₇ produces 7.0% lower K(t) than synthetic methods—demonstrating our commitment to empirical rigor over methodological optimism.

## Significance

This work advances understanding of civilizational coherence through:

1. **Empirical Validation**: Strong component correlations (r = 0.62–0.78, all p < 0.001)
2. **Comprehensive Coverage**: 159 countries, 191,913 data points from World Bank
3. **Transparent Methodology**: Conservative findings strengthen scientific credibility
4. **Complete Reproducibility**: Full automation, open data, locked dependencies

## Data and Code Availability

All data (191,913 points, World Bank CC-BY-4.0) and code will be made publicly available upon publication. Complete reproducibility achieved through Nix environment (6-minute runtime).

## Anticipated Reviewer Questions

We have prepared detailed responses to anticipated questions:

**Q: Why not extend H₇ further back?**
A: We prioritize four-component consistency. WGI limitation (1996+) is fundamental. Our dual formulation strategy (six-harmony for 1810-1995, seven-harmony for 1996-2021) is methodologically sound.

**Q: Are component weights arbitrary?**
A: Weights are conceptually justified and empirically robust (±10% variation produces <5% impact).

**Q: Why geometric mean?**
A: Standard in composite indices (HDI uses geometric mean), prevents compensation, empirically validated.

## Suitable for Nature

This work:
- Addresses fundamental questions about societal development
- Provides novel empirical validation of theoretical constructs
- Demonstrates methodological transparency and scientific honesty
- Offers complete reproducibility and open science

We believe this manuscript is well-suited for *Nature* and will be of broad interest to researchers studying societal evolution, development economics, and sustainability.

Thank you for considering our submission.

Sincerely,

[Author Name]
[Affiliation]
[Email]

---

**Note**: This is a template. Please customize with:
- Your authorship details
- Specific manuscript title
- Any additional context
- Co-author information
""".format(date=datetime.now().strftime("%B %d, %Y"))

    cover_letter_md.write_text(cover_letter_content)

    output_file = OUTPUT_DIR / "Cover_Letter_Template.pdf"

    return run_pandoc(
        [str(cover_letter_md)],
        output_file,
        "Cover Letter Template",
        additional_args=["--variable=fontsize:12pt"]
    )

def create_complete_documentation_pdf():
    """Create comprehensive technical documentation PDF."""
    print("\n" + "="*80)
    print("5. Creating Complete Documentation PDF")
    print("="*80)

    # Major documentation files
    input_files = [
        str(BASE_DIR / "START_HERE.md"),
        str(BASE_DIR / "EXECUTIVE_SUMMARY_ONE_PAGE.md"),
        str(BASE_DIR / "PUBLICATION_READINESS_VERIFICATION.md"),
        str(BASE_DIR / "H7_README.md"),
        str(BASE_DIR / "AUTHOR_QUICK_START.md"),
        str(BASE_DIR / "NATURE_SUBMISSION_CHECKLIST.md"),
    ]

    output_file = OUTPUT_DIR / "H7_Complete_Documentation.pdf"

    return run_pandoc(
        input_files,
        output_file,
        "H₇ Evolutionary Progression: Complete Documentation",
        additional_args=[
            "--variable=fontsize:10pt",
            "--variable=geometry:margin=0.75in"
        ]
    )

def main():
    """Generate all submission PDFs."""
    print("\n" + "="*80)
    print("PDF Generation for Nature Submission")
    print("="*80)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")

    results = []

    # Create PDFs in priority order
    results.append(("Supplementary Materials", create_supplementary_materials_pdf()))
    results.append(("Executive Summary", create_executive_summary_pdf()))
    results.append(("Manuscript Sections", create_manuscript_sections_pdf()))
    results.append(("Cover Letter Template", create_cover_letter_pdf()))
    results.append(("Complete Documentation", create_complete_documentation_pdf()))

    # Summary
    print("\n" + "="*80)
    print("Generation Summary")
    print("="*80)

    for name, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")

    successful = sum(1 for _, success in results if success)
    print(f"\nCompleted: {successful}/{len(results)} PDFs generated")

    if successful == len(results):
        print("\n✅ All PDFs generated successfully!")
        print(f"\nLocation: {OUTPUT_DIR}")
        print("\nFiles ready for Nature submission:")
        for pdf_file in sorted(OUTPUT_DIR.glob("*.pdf")):
            size_mb = pdf_file.stat().st_size / (1024 * 1024)
            print(f"  - {pdf_file.name} ({size_mb:.2f} MB)")
    else:
        print("\n⚠️ Some PDFs failed to generate. Check errors above.")

    return successful == len(results)

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
