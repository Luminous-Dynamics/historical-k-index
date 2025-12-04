#!/usr/bin/env python3
"""
Regenerate the 2 failed PDFs with full LaTeX scheme
"""

import subprocess
from pathlib import Path
from datetime import datetime

BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")
OUTPUT_DIR = BASE_DIR / "submission_pdfs"

PANDOC_ARGS = [
    "--pdf-engine=xelatex",
    "--variable=geometry:margin=1in",
    "--variable=fontsize:10pt",  # Smaller for supplement
    "--variable=documentclass:article",
    "--number-sections",
    "--toc",
]

def run_pandoc(input_files, output_file, title):
    """Run pandoc to generate PDF."""
    args = [
        "pandoc",
        *input_files,
        "-o", str(output_file),
        f"--metadata=title:{title}",
        f"--metadata=date:{datetime.now().strftime('%B %d, %Y')}",
        *PANDOC_ARGS,
    ]

    print(f"Generating: {output_file.name}")
    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode == 0:
        size_kb = output_file.stat().st_size / 1024
        print(f"  ✓ Created: {output_file.name} ({size_kb:.1f} KB)")
        return True
    else:
        print(f"  ✗ Error: {result.stderr}")
        return False

print("Regenerating failed PDFs with full LaTeX scheme...")
print("="*80)

# 1. Supplementary Materials
print("\n1. Supplementary Materials")
print("-"*80)
supp_files = [
    str(BASE_DIR / "manuscript/supplementary/SUPPLEMENTARY_METHODS.md"),
    str(BASE_DIR / "manuscript/supplementary/SUPPLEMENTARY_TABLES.md"),
]
supp_output = OUTPUT_DIR / "H7_Supplementary_Materials.pdf"
supp_success = run_pandoc(
    supp_files,
    supp_output,
    "Supplementary Materials: Validated H₇ Component"
)

# 2. Complete Documentation
print("\n2. Complete Documentation")
print("-"*80)
doc_files = [
    str(BASE_DIR / "START_HERE.md"),
    str(BASE_DIR / "EXECUTIVE_SUMMARY_ONE_PAGE.md"),
    str(BASE_DIR / "H7_README.md"),
]
doc_output = OUTPUT_DIR / "H7_Complete_Documentation.pdf"
doc_success = run_pandoc(
    doc_files,
    doc_output,
    "H₇ Complete Documentation"
)

# Summary
print("\n" + "="*80)
print("Summary:")
print(f"  {'✓' if supp_success else '✗'} Supplementary Materials")
print(f"  {'✓' if doc_success else '✗'} Complete Documentation")

if supp_success and doc_success:
    print("\n✅ All PDFs regenerated successfully!")
    print(f"\nAll 5 PDFs now available in: {OUTPUT_DIR}")
    import glob
    pdfs = sorted(glob.glob(str(OUTPUT_DIR / "*.pdf")))
    for pdf in pdfs:
        size = Path(pdf).stat().st_size / 1024
        print(f"  - {Path(pdf).name} ({size:.1f} KB)")
else:
    print("\n⚠️ Some PDFs still failed. Check errors above.")
