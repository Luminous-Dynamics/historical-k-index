# 🏷️ Create GitHub Release for Zenodo DOI

**Status**: Zenodo sync enabled ✅
**Next Step**: Create v1.0.0 release
**Result**: Automatic DOI generation

---

## ✅ Prerequisites (Already Done)

1. ✅ Repository synced to Zenodo
2. ✅ All materials committed and pushed
3. ✅ Repository clean and organized

---

## 🚀 Step-by-Step Release Process

### Step 1: Verify Current Status

Before creating release, verify everything is ready:

```bash
cd /srv/luminous-dynamics/historical-k-index-repo

# Check current branch and status
git status
git log --oneline -5

# Verify all files are committed
git diff HEAD

# List what will be in the release
ls -R
```

**Checklist**:
- [ ] All files committed
- [ ] No uncommitted changes
- [ ] Latest changes pushed to GitHub
- [ ] Repository builds without errors

---

### Step 2: Create GitHub Release

**Option A: Via GitHub Web Interface** (Recommended)

1. **Go to repository**: https://github.com/Luminous-Dynamics/historical-k-index

2. **Click "Releases"** (right sidebar)

3. **Click "Create a new release"**

4. **Fill in release details**:

   **Tag version**: `v1.0.0`

   **Release title**: `v1.0.0 - Historical K-Index Initial Release`

   **Description**:
   ```markdown
   # Historical K-Index v1.0.0 - Nature Sustainability Submission

   ## 📊 Dataset Release

   Complete replication package for manuscript:
   > "Global Coordination Infrastructure 1810-2020: A Multi-Harmonic Index of
   > Civilizational Coherence and Climate Vulnerability"

   **Submitted to**: Nature Sustainability

   ## 📦 What's Included

   ### Data (191,913 data points)
   - ✅ 8 raw data sources (World Bank, WIPO, Barro-Lee, V-Dem, KOF, HYDE, Seshat)
   - ✅ 4 processed datasets (H₇, K(t), rankings)
   - ✅ 159 countries, 1810-2020 coverage

   ### Code (28 scripts)
   - ✅ Complete data collection pipeline (7 scripts)
   - ✅ Processing & ETL (11 scripts)
   - ✅ Analysis & robustness tests (5 scripts)
   - ✅ Visualization (2 scripts)
   - ✅ Validation (3 scripts)

   ### Manuscript Materials
   - ✅ Main manuscript (LaTeX + PDF)
   - ✅ Supplementary Information (LaTeX + PDF)
   - ✅ All figures (23 @ 300 DPI)
   - ✅ All tables (4 tables, CSV + LaTeX)

   ### Documentation
   - ✅ Replication guide (6-minute reproduction)
   - ✅ Data availability statement
   - ✅ H₇ methodology documentation
   - ✅ Computational requirements

   ## 🔬 Key Results

   - **Six-fold K(t) increase**: 0.13 (1810) → 0.78 (2020)
   - **Validated H₇ component**: 2,352 observations, -7.0% conservative
   - **Post-1990 imbalance**: H₅ grew 35%, H₃ lagged at 12%
   - **Climate vulnerability**: Coordination capacity insufficient for climate action

   ## 📖 Citation

   ```bibtex
   @misc{stoltz2025historical,
     author = {Stoltz, Tristan},
     title = {Historical K-Index Dataset (1810-2020)},
     year = {2025},
     publisher = {Zenodo},
     doi = {10.5281/zenodo.XXXXXXX},
     url = {https://github.com/Luminous-Dynamics/historical-k-index}
   }
   ```

   ## 🔄 Reproducibility

   Complete reproduction in 6 minutes:
   ```bash
   git clone https://github.com/Luminous-Dynamics/historical-k-index.git
   cd historical-k-index
   nix develop
   poetry install
   poetry run python scripts/data_collection/00_download_worldbank_patents.py
   # ... (see REPLICATION_GUIDE.md)
   ```

   ## 📊 Validation

   - External validation: log-GDP r=0.98, HDI r=0.70
   - Bootstrap 95% CI: All results robust
   - Component correlations: r=0.62-0.78 (p<0.001)

   ## 🙏 Acknowledgments

   Data sources: World Bank, WIPO, Barro-Lee, V-Dem, KOF, HYDE, Seshat

   ---

   **For manuscript**: See `manuscript/k_index_manuscript.pdf`
   **For replication**: See `docs/REPLICATION_GUIDE.md`
   **For data**: See `data/processed/`
   ```

5. **Choose release type**:
   - ✅ **Set as latest release** (checked)
   - ✅ **Create a discussion for this release** (optional)

6. **Click "Publish release"** 🎉

---

**Option B: Via Command Line** (Alternative)

```bash
# Install GitHub CLI if needed
# nix-shell -p gh

# Authenticate
gh auth login

# Create release
gh release create v1.0.0 \
  --title "v1.0.0 - Historical K-Index Initial Release" \
  --notes-file RELEASE_NOTES.md \
  --latest

# Upload specific files (optional)
gh release upload v1.0.0 \
  manuscript/k_index_manuscript.pdf \
  manuscript/Supplementary_Materials.pdf
```

---

### Step 3: Verify Zenodo Sync

**Immediate (< 5 minutes)**:

1. Go to https://zenodo.org/account/settings/github/

2. Find "Luminous-Dynamics/historical-k-index"

3. You should see:
   - ✅ "Enabled" badge
   - ✅ New version badge (may take a few minutes)

**Within 1 hour**:

4. Zenodo creates DOI automatically

5. Check repository page on Zenodo:
   - Go to https://zenodo.org/
   - Search for "historical k-index" or your GitHub username
   - You should see the new deposit

6. **Copy the DOI badge code** (appears next to repository)

---

### Step 4: Add DOI Badge to README

Once Zenodo generates the DOI, update README.md:

**DOI Badge** (top of README.md):
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

**Replace XXXXXXX** with your actual DOI number from Zenodo!

**Example**:
```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.8475.svg)](https://doi.org/10.5281/zenodo.8475)
```

---

### Step 5: Update CITATION.cff

Update the DOI in `CITATION.cff`:

```yaml
cff-version: 1.2.0
title: "Historical K-Index: Global Civilizational Coordination Infrastructure Dataset (1810-2020)"
message: "If you use this dataset, please cite it using these metadata."
type: dataset
authors:
  - family-names: "Stoltz"
    given-names: "Tristan"
    email: "tristan.stoltz@luminousdynamics.org"
    orcid: "https://orcid.org/YOUR-ORCID"  # Add if you have one
identifiers:
  - type: doi
    value: 10.5281/zenodo.XXXXXXX  # ← Update with real DOI
    description: "Dataset DOI"
repository-code: "https://github.com/Luminous-Dynamics/historical-k-index"
url: "https://github.com/Luminous-Dynamics/historical-k-index"
license: CC-BY-4.0
version: 1.0.0
date-released: 2025-12-03
```

---

### Step 6: Update Manuscript with DOI

**Add to manuscript** (k_index_manuscript.tex):

In the "Data Availability" section:
```latex
\section{Data Availability}

All data and code are available at:
\url{https://github.com/Luminous-Dynamics/historical-k-index}

Persistent DOI: \url{https://doi.org/10.5281/zenodo.XXXXXXX}

Complete replication package includes:
\begin{itemize}
  \item Raw data from 8 sources (191,913 data points)
  \item Processing scripts (28 Python scripts)
  \item Analysis-ready datasets (4 files)
  \item Supplementary materials (4 tables, 4 figures)
  \item Replication guide (6-minute reproduction)
\end{itemize}
```

---

## 📋 Complete Checklist

### Before Release
- [ ] All files committed and pushed
- [ ] Repository clean (no uncommitted changes)
- [ ] README.md up to date
- [ ] CITATION.cff has placeholder for DOI
- [ ] Manuscript references GitHub repository

### Create Release
- [ ] Go to GitHub repository
- [ ] Click "Releases" → "Create a new release"
- [ ] Tag: `v1.0.0`
- [ ] Title: `v1.0.0 - Historical K-Index Initial Release`
- [ ] Description: Complete (use template above)
- [ ] Publish release

### After Release (within 1 hour)
- [ ] Verify Zenodo created deposit
- [ ] Copy DOI from Zenodo
- [ ] Add DOI badge to README.md
- [ ] Update CITATION.cff with DOI
- [ ] Update manuscript with DOI
- [ ] Commit and push DOI updates
- [ ] Verify badge displays correctly

### Final Verification
- [ ] Click DOI badge → goes to Zenodo page
- [ ] Zenodo page shows correct files
- [ ] Zenodo page has correct metadata
- [ ] Citation export works (BibTeX, RIS, etc.)

---

## 🎯 Expected Timeline

| Step | Time | Status |
|------|------|--------|
| Create GitHub release | 5 minutes | ⏳ Pending |
| Zenodo processes release | 5-60 minutes | ⏳ Auto |
| DOI badge appears | Immediately after | ⏳ Auto |
| Update README/CITATION | 5 minutes | ⏳ Pending |
| Update manuscript | 10 minutes | ⏳ Pending |
| Final verification | 5 minutes | ⏳ Pending |

**Total active time**: ~25 minutes
**Total wait time**: Up to 1 hour (Zenodo processing)

---

## 🚨 Troubleshooting

### DOI doesn't appear after 1 hour
1. Check Zenodo sync status: https://zenodo.org/account/settings/github/
2. Verify repository is "Enabled"
3. Check for errors in Zenodo dashboard
4. Try disabling and re-enabling sync
5. Contact Zenodo support if still failing

### Badge link broken
- Wait 5-10 more minutes (CDN propagation)
- Clear browser cache
- Verify DOI number is correct

### Want to update release after publishing
- You can edit the release description anytime
- Zenodo DOI remains the same
- For major changes, create v1.0.1

---

## ✅ Success Criteria

You'll know everything worked when:

1. ✅ GitHub shows v1.0.0 release
2. ✅ Zenodo shows deposit with DOI
3. ✅ DOI badge displays in README
4. ✅ Clicking badge goes to Zenodo page
5. ✅ Zenodo page has all files
6. ✅ BibTeX export works
7. ✅ Manuscript references correct DOI

---

## 🎉 After DOI is Live

**Celebrate!** You now have:
- ✅ Permanent, citable dataset
- ✅ Nature Sustainability requirement satisfied
- ✅ Professional research infrastructure
- ✅ Easy collaboration and replication

**Next**: Submit manuscript to Nature Sustainability! 🚀

---

*This DOI will persist forever, even if GitHub disappears. That's the power of Zenodo!*
