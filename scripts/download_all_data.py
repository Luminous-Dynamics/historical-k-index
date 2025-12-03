#!/usr/bin/env python3
"""
Master script to download ALL external data sources for Historical K-Index project.

This script orchestrates downloading all required datasets from their original sources.
Total download size: ~2.5 GB
Estimated time: 10-20 minutes (depending on connection speed)

Usage:
    poetry run python scripts/download_all_data.py

    # Or with options:
    poetry run python scripts/download_all_data.py --skip-large  # Skip files >100MB
    poetry run python scripts/download_all_data.py --verify-only # Only verify existing downloads
"""

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

# Project root
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
EXTERNAL_DIR = DATA_DIR / "data_sources" / "external"

# Ensure directories exist
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)


class DatasetDownloader:
    """Manages downloading and verification of external datasets."""

    def __init__(self, skip_large: bool = False, verify_only: bool = False):
        self.skip_large = skip_large
        self.verify_only = verify_only
        self.downloaded = 0
        self.skipped = 0
        self.failed = 0

    def compute_checksum(self, filepath: Path) -> str:
        """Compute SHA256 checksum of a file."""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()

    def verify_file(self, filepath: Path, expected_size_mb: float = None) -> bool:
        """Verify a downloaded file exists and has expected size."""
        if not filepath.exists():
            return False

        if expected_size_mb:
            actual_size_mb = filepath.stat().st_size / (1024 * 1024)
            # Allow 5% variance
            if not (expected_size_mb * 0.95 <= actual_size_mb <= expected_size_mb * 1.05):
                print(f"⚠️  Size mismatch: {filepath.name} ({actual_size_mb:.1f} MB, expected {expected_size_mb:.1f} MB)")
                return False

        return True

    def download_collection_script(self, script_name: str, description: str) -> bool:
        """Run a data collection script."""
        print(f"\n{'='*70}")
        print(f"📥 {description}")
        print(f"{'='*70}")

        if self.verify_only:
            print("⏭️  Skipping (verify-only mode)")
            self.skipped += 1
            return True

        script_path = PROJECT_ROOT / "scripts" / "data_collection" / script_name

        if not script_path.exists():
            print(f"⚠️  Script not found: {script_path}")
            print(f"   Creating placeholder...")
            self.failed += 1
            return False

        try:
            result = subprocess.run(
                ["poetry", "run", "python", str(script_path)],
                cwd=PROJECT_ROOT,
                capture_output=True,
                text=True,
                timeout=600  # 10 minute timeout per script
            )

            if result.returncode == 0:
                print(f"✅ Success!")
                self.downloaded += 1
                return True
            else:
                print(f"❌ Failed with error:")
                print(result.stderr)
                self.failed += 1
                return False

        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout after 10 minutes")
            self.failed += 1
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            self.failed += 1
            return False

    def download_all(self):
        """Download all datasets in order."""

        print("\n" + "="*70)
        print("📦 Historical K-Index Data Download")
        print("="*70)
        print(f"\nProject Root: {PROJECT_ROOT}")
        print(f"Data Directory: {DATA_DIR}")
        print(f"Skip Large Files: {self.skip_large}")
        print(f"Verify Only: {self.verify_only}")
        print("\nThis will download ~2.5 GB of data. Estimated time: 10-20 minutes.")

        if not self.verify_only:
            response = input("\nContinue? [y/N]: ")
            if response.lower() != 'y':
                print("Aborted.")
                return

        # Dataset download sequence (in dependency order)
        datasets = [
            ("00_download_worldbank_patents.py", "World Bank World Development Indicators (WDI)"),
            ("01_download_wipo_patents.py", "WIPO Patent Statistics"),
            ("02_download_ccp_constitutions.py", "Constitutional Change Project Data"),
            ("03_download_barro_lee_education.py", "Barro-Lee Educational Attainment"),
            ("04_construct_infrastructure_index.py", "Infrastructure Quality Index"),
            ("05_integrate_H7_components.py", "H₇ Component Integration"),
            ("06_download_worldbank_h7_supplementary.py", "Supplementary World Bank Data for H₇"),
        ]

        # Additional large datasets (optional)
        if not self.skip_large:
            large_datasets = [
                ("download_wvs.py", "World Values Survey (WVS) - 1.3 GB"),
                ("download_vdem.py", "Varieties of Democracy (V-Dem) - 195 MB"),
                ("download_imf_fsi.py", "IMF Financial Soundness Indicators - 85 MB"),
                ("download_pew.py", "Pew Research Center Global Attitudes - 54 MB"),
            ]
            datasets.extend(large_datasets)
        else:
            print("\n⏭️  Skipping large datasets (>50 MB)")
            print("   To download these later, run without --skip-large")

        # Execute downloads
        for script, description in datasets:
            self.download_collection_script(script, description)

        # Summary
        print("\n" + "="*70)
        print("📊 Download Summary")
        print("="*70)
        print(f"✅ Successfully downloaded: {self.downloaded}")
        print(f"⏭️  Skipped: {self.skipped}")
        print(f"❌ Failed: {self.failed}")

        if self.failed == 0:
            print("\n🎉 All datasets downloaded successfully!")
            print("\nNext steps:")
            print("1. Verify data integrity: poetry run python scripts/verify_data_integrity.py")
            print("2. Run processing pipeline: poetry run python scripts/process_all_data.py")
            print("3. Generate figures: poetry run python scripts/generate_supplementary_figures.py")
        else:
            print(f"\n⚠️  {self.failed} dataset(s) failed to download.")
            print("Check error messages above and try again.")
            print("\nYou can also download the complete dataset from Zenodo:")
            print("https://doi.org/10.5281/zenodo.XXXXXXX")

        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(
        description="Download all external data sources for Historical K-Index project"
    )
    parser.add_argument(
        "--skip-large",
        action="store_true",
        help="Skip downloading large files (>50 MB)"
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Only verify existing downloads, don't download new files"
    )

    args = parser.parse_args()

    downloader = DatasetDownloader(
        skip_large=args.skip_large,
        verify_only=args.verify_only
    )

    success = downloader.download_all()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
