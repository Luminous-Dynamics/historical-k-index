# Visualization Strategy: Making Collapse Dynamics Visible

> **"A picture is worth a thousand words; a good visualization is worth a thousand statistics."**

---

## Design Philosophy

Our visualizations must accomplish three goals:

1. **Clarity**: Complex dynamics made immediately understandable
2. **Rigor**: Every element grounded in data
3. **Impact**: Visual narrative that drives home urgency

**Style**: Clean, academic, but compelling. Think Nature/Science quality.

---

## Main Text Figures (6)

### Figure 1: K-Index Collapse Trajectories (4-Panel)

**Purpose**: Show the shape of coordination collapse across cases

**Layout**: 2×2 grid, each panel one case study

```
┌─────────────────────┬─────────────────────┐
│                     │                     │
│    A. Bronze Age    │    B. Western Rome  │
│    (1300-1000 BCE)  │    (200 BCE-600 CE) │
│                     │                     │
├─────────────────────┼─────────────────────┤
│                     │                     │
│    C. Maya Classic  │    D. Soviet Union  │
│    (600-1000 CE)    │    (1970-1995)      │
│                     │                     │
└─────────────────────┴─────────────────────┘
```

**Elements per panel**:
- X-axis: Time (appropriate scale for each case)
- Y-axis: K(t) value (0-1 scale)
- Main line: K(t) trajectory with confidence band
- Horizontal dashed line: Threshold (θ ≈ 0.37)
- Shaded region: Collapse period
- Annotation: Key events marked

**Color Scheme**:
- K(t) line: Deep blue (#1a5276)
- Confidence band: Light blue with alpha
- Threshold: Red dashed (#c0392b)
- Collapse period: Gray shading (#bdc3c7)

**Code Sketch**:
```python
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

for ax, case in zip(axes.flat, cases):
    ax.plot(case['t'], case['K'], color='#1a5276', linewidth=2)
    ax.fill_between(case['t'], case['K_low'], case['K_high'],
                    alpha=0.2, color='#1a5276')
    ax.axhline(y=0.37, color='#c0392b', linestyle='--', label='Threshold')
    ax.axvspan(case['collapse_start'], case['collapse_end'],
               alpha=0.1, color='gray')
    ax.set_title(case['name'])
    ax.set_xlabel('Time')
    ax.set_ylabel('K(t)')

plt.tight_layout()
```

---

### Figure 2: Harmony Cascade Waterfall

**Purpose**: Show the sequence of harmony decline—which falls first, which persists longest

**Layout**: Horizontal stacked bars, one row per case

```
              ← Earlier                          Later →
Bronze Age:   ███H₃███ ██H₁██ ██H₂██ █H₄█ █H₅█ ███H₇███
Rome:         ███H₃███ ███H₁███ ██H₂██ █H₄█ ██H₅██ ████H₇████
Maya:         ██H₃██ ██H₁██ ███H₂███ ██H₄██ █H₅█ ███H₇███
Soviet:       █H₃█ █H₁█ ██H₂██ █H₄█ █H₅█ ██H₇██
              ─────────────────────────────────────────
              H₃ first ────────────────────→ H₇ last
```

**Elements**:
- X-axis: Relative timing (normalized)
- Y-axis: Case studies
- Bar color: Different color per harmony
- Bar start: When decline began
- Bar end: When nadir reached
- Annotation: Pattern highlight (H₃ first, H₇ last)

**Color Palette for Harmonies**:
- H₁ Governance: #8e44ad (purple)
- H₂ Economy: #27ae60 (green)
- H₃ Trust: #e74c3c (red) - highlighted
- H₄ Complexity: #f39c12 (orange)
- H₅ Knowledge: #3498db (blue)
- H₆ Wellbeing: #1abc9c (teal)
- H₇ Technology: #95a5a6 (gray)

---

### Figure 3: Speed-Capacity Scatter Plot

**Purpose**: Test Hypothesis 3 (higher pre-crisis K → slower collapse)

**Layout**: Scatter plot with regression line

```
     Collapse Duration (years)
     ▲
 200 │                              ● Rome
     │
 100 │                    ● Maya
     │
  50 │        ● Bronze
     │
  10 │  ● Soviet
     │
     └─────────────────────────────────▶
        0.5     0.6     0.7     0.8
              Pre-Crisis K(t)
```

**Elements**:
- X-axis: Peak K(t) before collapse
- Y-axis: Collapse duration (log scale)
- Points: Case studies (sized by population affected?)
- Regression line: With confidence interval
- Annotation: r value, p-value
- Control cases: Different marker (triangles?)

**Statistical Requirements**:
- Calculate Pearson/Spearman correlation
- Bootstrap confidence interval
- Include sensitivity to case inclusion

---

### Figure 4: Trust Threshold Phase Diagram

**Purpose**: Visualize the H₃ threshold as phase transition

**Layout**: Phase diagram showing stable/unstable regions

```
     Other Harmonies (avg H₁,₂,₄-₇)
     ▲
 0.9 │  ╭────────────────────────────
     │  │     STABLE COORDINATION
     │  │         (recovery possible)
 0.6 │  │
     │  │    ╱╲ Bifurcation
     │  │   ╱  ╲   Zone
 0.4 │──┼──╱────╲─────────────────────
     │  │ ╱      ╲
     │  │╱   COLLAPSE CASCADE
 0.2 │  │    (irreversible decline)
     │  │
     └──┴─────────────────────────────▶
       0.2   0.35-0.40   0.6    0.8
              H₃ (Trust)
               ▲
           Threshold
```

**Elements**:
- X-axis: H₃ value
- Y-axis: Average of other harmonies
- Regions: Colored differently (stable = green, unstable = red)
- Bifurcation zone: Hatched pattern
- Case trajectories: Arrows showing path through phase space
- Threshold zone: Highlighted (0.35-0.40)

---

### Figure 5: Recovery Asymmetry Comparison

**Purpose**: Show that recovery takes 3-10x longer than collapse

**Layout**: Butterfly/diverging bar chart

```
                  Collapse    │    Recovery
                       ◀──────┼──────▶
                              │
Bronze Age:     ████████████ │ ███████████████████████████████████
                   50 years  │  200+ years (partial)
                              │
Rome:           ████████████ │ █████████████████████████████████████████████
                   200 years │  500+ years to Carolingian
                              │
Maya:           █████████ │ ████████████████████████████████████
                  100 years  │  400+ years to Postclassic
                              │
Soviet:         ███ │ ████████████████████
                 3 years     │  30+ years (ongoing)
                              │
              ─────┴─────────┴────────────────────
            Asymmetry ratio:    3-10x
```

**Elements**:
- Center line: Collapse/recovery divide
- Left bars: Collapse duration
- Right bars: Recovery duration
- Color: Collapse = dark red, Recovery = dark blue
- Annotations: Duration in years
- Footer: Asymmetry ratio summary

---

### Figure 6: Collapse Typology Matrix

**Purpose**: Classify collapse types for modern diagnostic

**Layout**: 2×2 matrix with case positions

```
                        TRIGGER SOURCE
                  External          Internal
              ┌─────────────────┬─────────────────┐
              │                 │                 │
      Fast    │  CATASTROPHIC   │   IMPLOSION     │
              │                 │                 │
              │   ● Bronze Age  │  ● Soviet       │
  SPEED       │                 │                 │
              ├─────────────────┼─────────────────┤
              │                 │                 │
      Slow    │   EXHAUSTION    │   EROSION       │
              │                 │                 │
              │   (● Khmer?)    │   ● Rome        │
              │                 │   ○ Maya        │
              │                 │                 │
              └─────────────────┴─────────────────┘
```

**Elements**:
- Quadrant labels with descriptions
- Case positions: Circles with case names
- Characteristic patterns per quadrant
- Modern analogues suggested (faded, in discussion)

---

## Supplementary Figures (10+)

### S1-S4: Detailed Harmony Trajectories

One figure per case study showing all 7 harmonies over time:

```
     │ ─── H₁  ─── H₂  ─── H₃  ─── H₄
     │ ─── H₅  ─── H₆  ─── H₇  ─ ─ K(t)
 1.0 ├─────────────────────────────────
     │   ╭──────────╮    H₇
 0.8 │  ╱            ╲  persistence
     │ ╱              ╲
 0.6 │╱    ╭───╮  ╲    ╲
     │    ╱     ╲  ╲    ╲
 0.4 ├───╱───────╲──╲────╲────────────
     │  ╱         ╲  ╲    ╲   H₃ first
 0.2 │ ╱           ╲──╲────╲──────────
     │╱               ╲    ╲
 0.0 └─────────────────────────────────▶
         Time →
```

### S5: Sensitivity Analysis Heat Map

Show how K(t) estimates change under different scoring assumptions:

```
              Scoring Variant
         Conservative  Neutral  Optimistic
Bronze Age    0.58       0.62      0.68
Rome          0.61       0.65      0.70
Maya          0.55       0.60      0.66
Soviet        0.50       0.55      0.60

Color: Blue (lower) ──── Red (higher)
```

### S6: Control Case Comparison

Direct comparison of collapse vs. control cases:

```
              H₃ at Crisis Point
         ▼ Collapsed        ▲ Survived
Mycenae  ●──────────────────○ Egypt
W. Rome  ●──────────────────○ Byzantium
S. Maya  ●──────────────────○ N. Maya
Soviet   ●──────────────────○ China
         0.2   0.3   0.4   0.5   0.6
                     ▲
                 Threshold
```

### S7: Early Warning Signal Trends

Show EWS indicators (variance, autocorrelation) preceding collapse:

```
     Indicator Value
     │     ╭──── Collapse
 High│    ╱│
     │   ╱ │
     │  ╱  │  Variance ↑
     │ ╱   │  AR(1) ↑
 Low │╱    │
     └─────┴──────────────▶
       -50  -25   0   +25
        Years before collapse
```

### S8: CSI Time Series

Coordination Stress Index for Soviet case (quantitative validation):

```
     CSI
 0.6 ├─────────────────╭─╮─────────
     │                ╱  │ Critical
 0.4 ├───────────────╱───┼─────────
     │              ╱    │ High
 0.2 ├─────────────╱─────┼─────────
     │    ╱╲  ╱╲ ╱       │
 0.0 ├───╱──╲╱──╲────────┴─────────▶
     1970  1980  1990  1991
```

### S9: Cross-Case Pattern Matrix

Which harmonies correlate across cases:

```
         Bronze  Rome   Maya  Soviet
Bronze    1.00   0.82   0.78   0.71
Rome      0.82   1.00   0.85   0.69
Maya      0.78   0.85   1.00   0.73
Soviet    0.71   0.69   0.73   1.00
```

### S10: Modern Fragility Preview

Contemporary CSI estimates (teaser for Paper 3):

```
     Global CSI by Region

N. America  ████░░░░░░  0.18
W. Europe   ███░░░░░░░  0.12
E. Asia     ████░░░░░░  0.15
S. Asia     ███████░░░  0.28
MENA        █████████░  0.45
Sahel       ██████████  0.58
            ──────────────────
            0.0       0.6
```

---

## Technical Specifications

### Color Palette

**Primary Colors**:
- Blue (stability): #1a5276
- Red (crisis): #c0392b
- Green (recovery): #27ae60
- Gray (neutral): #95a5a6

**Harmony Colors** (consistent across all figures):
```python
HARMONY_COLORS = {
    'H1': '#8e44ad',  # Purple - Governance
    'H2': '#27ae60',  # Green - Economy
    'H3': '#e74c3c',  # Red - Trust (highlighted)
    'H4': '#f39c12',  # Orange - Complexity
    'H5': '#3498db',  # Blue - Knowledge
    'H6': '#1abc9c',  # Teal - Wellbeing
    'H7': '#95a5a6',  # Gray - Technology
}
```

### Typography

- **Titles**: 14pt, bold
- **Axis labels**: 12pt
- **Tick labels**: 10pt
- **Annotations**: 9pt, italic
- **Font**: Arial/Helvetica (standard for Nature/Science)

### Dimensions

- **Main figures**: 180mm width (full page) or 90mm (half page)
- **Resolution**: 300 DPI minimum
- **Format**: PDF (vector) for submission, PNG for review

### Accessibility

- Color-blind safe palette options
- Pattern overlays for B&W printing
- Alt-text for all figures
- High contrast for key elements

---

## Production Pipeline

### Step 1: Data Preparation
```python
# Load processed case data
cases = load_all_cases()
for case in cases:
    case['K'] = compute_k_index(case['harmonies'])
    case['K_low'], case['K_high'] = bootstrap_ci(case)
```

### Step 2: Figure Generation
```python
# Generate each figure
for fig_spec in FIGURE_SPECS:
    fig = create_figure(fig_spec)
    save_figure(fig, format='pdf', dpi=300)
```

### Step 3: Quality Check
- Visual inspection
- Data accuracy verification
- Color-blind simulation
- Print preview

### Step 4: Final Output
- PDF for journal submission
- PNG for presentations
- SVG for web/interactive

---

## Implementation Priority

| Figure | Priority | Dependencies | Estimated Time |
|--------|----------|--------------|----------------|
| Figure 1 (K trajectories) | HIGH | Case data complete | 4 hours |
| Figure 2 (Cascade waterfall) | HIGH | Sequence analysis | 6 hours |
| Figure 3 (Speed scatter) | MEDIUM | All cases scored | 2 hours |
| Figure 4 (Phase diagram) | HIGH | Theory finalized | 4 hours |
| Figure 5 (Recovery asymmetry) | MEDIUM | Recovery data | 3 hours |
| Figure 6 (Typology matrix) | LOW | Typology finalized | 2 hours |
| S1-S4 (Detailed harmonies) | MEDIUM | Case data | 8 hours |
| S5-S10 (Supplementary) | LOW | Main figures done | 6 hours |

**Total estimated time**: ~35 hours for all figures

---

## Reviewer Response Visualizations

Prepare additional figures for anticipated reviewer requests:

1. **Alternative threshold values**: Sensitivity to θ = 0.30, 0.35, 0.40, 0.45
2. **Alternative weighting schemes**: Equal vs. differential harmony weights
3. **Temporal resolution analysis**: How results change with finer/coarser periodization
4. **Case exclusion analysis**: Results with each case removed

---

*"The best figures tell a story that words alone cannot."*

---

**Document**: Visualization Strategy
**Version**: 1.0
**Date**: December 2025
**Status**: Ready for implementation after data collection

