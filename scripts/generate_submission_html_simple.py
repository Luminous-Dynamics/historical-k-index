#!/usr/bin/env python3
"""
Generate Professional HTML Documents for Nature Submission (No Dependencies)
============================================================================

Creates print-ready HTML documents that can be easily converted to PDF.
Uses only Python standard library - no external dependencies.
"""

import os
from pathlib import Path
from datetime import datetime
import re

# Base directory
BASE_DIR = Path("/srv/luminous-dynamics/historical-k-index")
OUTPUT_DIR = BASE_DIR / "submission_html"
OUTPUT_DIR.mkdir(exist_ok=True)

# CSS for professional print-ready documents
PROFESSIONAL_CSS = """
<style>
    @media print {
        @page {
            margin: 1in;
            size: letter;
        }
        body {
            font-family: 'Times New Roman', Times, serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }
        .no-print {
            display: none;
        }
        a {
            color: #000;
            text-decoration: none;
        }
        h1 {
            page-break-before: always;
            font-size: 18pt;
            margin-top: 0;
        }
        h1:first-child {
            page-break-before: avoid;
        }
        h2 {
            font-size: 14pt;
            margin-top: 24pt;
        }
        h3 {
            font-size: 12pt;
            margin-top: 18pt;
        }
        code {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 1px 3px;
        }
        pre {
            font-family: 'Courier New', monospace;
            font-size: 9pt;
            background: #f5f5f5;
            padding: 10px;
            border: 1px solid #ddd;
            page-break-inside: avoid;
            white-space: pre-wrap;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 12pt 0;
            page-break-inside: avoid;
        }
        th, td {
            border: 1px solid #000;
            padding: 6pt;
            text-align: left;
            font-size: 10pt;
        }
        th {
            background: #f0f0f0;
            font-weight: bold;
        }
    }
    @media screen {
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 16px;
            line-height: 1.6;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 40px;
            background: #f9f9f9;
        }
        .document {
            background: white;
            padding: 1in;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .print-button {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #0066cc;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        .print-button:hover {
            background: #0052a3;
        }
        h1 {
            color: #1a1a1a;
            font-size: 28px;
            border-bottom: 2px solid #0066cc;
            padding-bottom: 8px;
        }
        h2 {
            color: #333;
            font-size: 22px;
            margin-top: 30px;
        }
        h3 {
            color: #555;
            font-size: 18px;
            margin-top: 24px;
        }
        code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Menlo', monospace;
            font-size: 14px;
        }
        pre {
            background: #f5f5f5;
            padding: 16px;
            border-radius: 6px;
            border-left: 4px solid #0066cc;
            overflow-x: auto;
        }
        pre code {
            background: none;
            padding: 0;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background: #f0f0f0;
            font-weight: bold;
        }
        tr:hover {
            background: #f9f9f9;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        .metadata {
            color: #666;
            font-style: italic;
            margin-bottom: 30px;
            padding: 15px;
            background: #f9f9f9;
            border-left: 4px solid #0066cc;
        }
        .check {
            color: #28a745;
        }
    }
</style>
<script>
function printDocument() {
    window.print();
}
</script>
"""

def markdown_to_html(text):
    """Simple markdown to HTML converter using only regex."""
    # Escape HTML
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    # Code blocks
    text = re.sub(r'```([^\n]*)\n(.*?)```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)

    # Inline code
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)

    # Headers
    text = re.sub(r'^### (.+)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.+)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.+)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)

    # Bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)

    # Links
    text = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', text)

    # Lists
    text = re.sub(r'^\- (.+)$', r'<li>\1</li>', text, flags=re.MULTILINE)
    text = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', text, flags=re.DOTALL)
    text = re.sub(r'</ul>\s*<ul>', '', text)

    # Checkboxes
    text = text.replace('- [x]', '<li class="check">✓')
    text = text.replace('- [ ]', '<li>☐')

    # Paragraphs
    text = re.sub(r'\n\n+', '</p><p>', text)
    text = f'<p>{text}</p>'

    # Clean up
    text = text.replace('<p><h', '<h').replace('</h1></p>', '</h1>')
    text = text.replace('</h2></p>', '</h2>').replace('</h3></p>', '</h3>')
    text = text.replace('<p></p>', '')
    text = text.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')
    text = text.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')

    return text

def create_html_document(title, content_md, output_file, subtitle=None):
    """Create professional HTML document from markdown content."""

    # Convert markdown to HTML
    html_content = markdown_to_html(content_md)

    # Create metadata
    metadata_html = ""
    if subtitle:
        metadata_html = f"""
        <div class="metadata">
            <strong>{subtitle}</strong><br>
            Generated: {datetime.now().strftime("%B %d, %Y")}
        </div>
        """

    # Create full HTML document
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    {PROFESSIONAL_CSS}
</head>
<body>
    <button class="print-button no-print" onclick="printDocument()">
        🖨️ Print / Save as PDF
    </button>
    <div class="document">
        <h1>{title}</h1>
        {metadata_html}
        {html_content}
    </div>
</body>
</html>
"""

    output_file.write_text(full_html, encoding='utf-8')
    size_kb = output_file.stat().st_size / 1024
    print(f"  ✓ Created: {output_file.name} ({size_kb:.1f} KB)")
    return True

def create_all_documents():
    """Create all submission HTML documents."""
    print("\n" + "="*80)
    print("HTML Generation for Nature Submission")
    print("="*80)
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Date: {datetime.now().strftime('%B %d, %Y')}")
    print("\nThese HTML documents are print-ready and can be saved as PDF from any browser.")

    results = []

    # 1. Supplementary Materials
    print("\n" + "="*80)
    print("1. Creating Supplementary Materials HTML")
    print("="*80)
    supp_methods = (BASE_DIR / "manuscript/supplementary/SUPPLEMENTARY_METHODS.md").read_text()
    supp_tables = (BASE_DIR / "manuscript/supplementary/SUPPLEMENTARY_TABLES.md").read_text()
    combined = f"{supp_methods}\n\n{supp_tables}"
    results.append(("Supplementary Materials", create_html_document(
        "Supplementary Materials: Validated H₇ (Evolutionary Progression) Component",
        combined,
        OUTPUT_DIR / "H7_Supplementary_Materials.html",
        subtitle="For Nature Submission"
    )))

    # 2. Executive Summary
    print("\n" + "="*80)
    print("2. Creating Executive Summary HTML")
    print("="*80)
    content = (BASE_DIR / "EXECUTIVE_SUMMARY_ONE_PAGE.md").read_text()
    results.append(("Executive Summary", create_html_document(
        "H₇ Evolutionary Progression: Executive Summary",
        content,
        OUTPUT_DIR / "H7_Executive_Summary.html",
        subtitle="Quick Reference Guide"
    )))

    # 3. Manuscript Sections
    print("\n" + "="*80)
    print("3. Creating H₇ Manuscript Sections HTML")
    print("="*80)
    methods = (BASE_DIR / "manuscript/H7_METHODS_SECTION_TEXT.md").read_text()
    results_md = (BASE_DIR / "manuscript/H7_RESULTS_SECTION_TEXT.md").read_text()
    discussion = (BASE_DIR / "manuscript/H7_DISCUSSION_SECTION_TEXT.md").read_text()
    combined = f"""# H₇ Manuscript Sections

## Instructions for Integration

These sections are ready to insert into your manuscript:

- **Methods**: Insert after H₆ methodology section
- **Results**: Insert after main K(t) results
- **Discussion**: Insert in appropriate Discussion subsection

Choose the version (Full/Concise/Minimal) that fits your word limit.

---

{methods}

---

{results_md}

---

{discussion}
"""
    results.append(("Manuscript Sections", create_html_document(
        "H₇ Manuscript Sections for Integration",
        combined,
        OUTPUT_DIR / "H7_Manuscript_Sections.html",
        subtitle="Ready for Copy-Paste into Main Manuscript"
    )))

    # 4. Cover Letter
    print("\n" + "="*80)
    print("4. Creating Cover Letter Template HTML")
    print("="*80)
    cover_letter = f"""# Cover Letter: Validated H₇ Component for Historical K(t) Index

**To**: Editor, *Nature*
**Date**: {datetime.now().strftime("%B %d, %Y")}
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

**[Author Name]**
**[Affiliation]**
**[Email]**

---

## Customization Instructions

Please customize this template with:

- Your authorship details (name, affiliation, email)
- All co-authors information
- Specific manuscript title (if different)
- Any additional relevant context
"""
    results.append(("Cover Letter", create_html_document(
        "Cover Letter Template for Nature Submission",
        cover_letter,
        OUTPUT_DIR / "Cover_Letter_Template.html",
        subtitle="Customize before submission"
    )))

    # 5. Complete Documentation
    print("\n" + "="*80)
    print("5. Creating Complete Documentation HTML")
    print("="*80)
    docs_combined = ""
    for filename in ["START_HERE.md", "H7_README.md", "AUTHOR_QUICK_START.md"]:
        content = (BASE_DIR / filename).read_text()
        docs_combined += f"\n\n{content}\n\n---\n\n"

    results.append(("Complete Documentation", create_html_document(
        "H₇ Evolutionary Progression: Complete Documentation",
        docs_combined,
        OUTPUT_DIR / "H7_Complete_Documentation.html",
        subtitle="Comprehensive Technical Reference"
    )))

    # Summary
    print("\n" + "="*80)
    print("Generation Summary")
    print("="*80)

    for name, success in results:
        status = "✓" if success else "✗"
        print(f"  {status} {name}")

    successful = sum(1 for _, success in results if success)
    print(f"\nCompleted: {successful}/{len(results)} HTML documents generated")

    if successful == len(results):
        print("\n✅ All HTML documents generated successfully!")
        print(f"\nLocation: {OUTPUT_DIR}")
        print("\nGenerated files:")
        for html_file in sorted(OUTPUT_DIR.glob("*.html")):
            size_kb = html_file.stat().st_size / 1024
            print(f"  - {html_file.name} ({size_kb:.1f} KB)")

        print("\n📝 How to convert to PDF:")
        print("  1. Open any HTML file in your web browser")
        print("  2. Click 'Print / Save as PDF' button (top right)")
        print("  3. Or use browser's Print function (Ctrl+P / Cmd+P) → Save as PDF")

        print(f"\n🌐 Start here: file://{OUTPUT_DIR.absolute()}/H7_Executive_Summary.html")
    else:
        print("\n⚠️ Some HTML documents failed to generate. Check errors above.")

    return successful == len(results)

if __name__ == "__main__":
    import sys
    success = create_all_documents()
    sys.exit(0 if success else 1)
