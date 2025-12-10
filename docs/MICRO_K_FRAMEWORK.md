# Micro-K Framework: Scale-Invariant Coordination Measurement

**Version**: 1.0.0
**Created**: December 10, 2025
**Paper Reference**: Paper 10 - "Scale-Invariant Coordination: The Micro-K Framework"

---

## Executive Summary

The **Micro-K Framework** extends the K-Index to measure coordination capacity at any scale - from small teams to global civilization. This document provides the theoretical foundation, measurement methodology, and practical implementation guide.

**Core Insight**: The same seven harmonies that determine civilizational coordination also determine team, organizational, and urban coordination. The formula scales.

---

## 1. Theoretical Foundation

### 1.1 Scale Invariance Principle

Just as fractal patterns repeat at different scales, coordination dynamics exhibit self-similarity:

```
K_team ≈ K_org ≈ K_city ≈ K_nation ≈ K_civilization

Where the formula:
K = [H₁ × H₂ × H₃ × H₄ × H₅ × H₆ × H₇]^(1/7)

applies at each level with scale-appropriate indicators.
```

### 1.2 Why Scale Invariance?

**Physical Basis**: Coordination is fundamentally about information flow, trust networks, and capability alignment. These follow similar mathematical patterns regardless of group size:
- Small groups: Dunbar layers (5, 15, 50, 150)
- Organizations: Hierarchical clustering
- Cities: Metcalfe's law for networks
- Nations: Institutional capacity

**Empirical Support**: Organizations with high internal coordination tend to exist in high-K nations, and vice versa. Coordination breeds coordination.

### 1.3 Scale-Specific Adaptations

| Scale | Unit | H₁ Governance | H₃ Trust | Key Challenge |
|-------|------|---------------|----------|---------------|
| **Team** | 5-15 people | Leadership clarity | Psychological safety | Personal conflict |
| **Department** | 15-50 | Management structure | Inter-team trust | Siloing |
| **Organization** | 50-5000 | Corporate governance | Culture | Bureaucracy |
| **City** | 10K-10M | Municipal govt | Civic trust | Inequality |
| **Region** | 1M-100M | State/provincial | Regional identity | Center-periphery |
| **Nation** | 1M-1B+ | National institutions | Social cohesion | Polarization |

---

## 2. Organizational Micro-K (OrgK)

### 2.1 The Seven Organizational Harmonies

```
Organizational K = [OH₁ × OH₂ × OH₃ × OH₄ × OH₅ × OH₆ × OH₇]^(1/7)
```

| Harmony | Name | What It Measures | Key Indicators |
|---------|------|------------------|----------------|
| **OH₁** | Strategic Coherence | Alignment on direction | Strategy clarity, goal alignment, decision consistency |
| **OH₂** | Communication Density | Information flow quality | Meeting effectiveness, cross-functional comms, info accessibility |
| **OH₃** | Trust & Reciprocity | Psychological safety | Peer trust, manager trust, help-seeking behavior |
| **OH₄** | Role Clarity | Clear accountabilities | Job clarity, overlap minimization, RACI adherence |
| **OH₅** | Knowledge Infrastructure | Learning capacity | Training investment, documentation, knowledge sharing |
| **OH₆** | Employee Wellbeing | Human sustainability | Satisfaction, retention, burnout rates, work-life balance |
| **OH₇** | Technical Capability | Tool effectiveness | Tech stack quality, automation level, tool satisfaction |

### 2.2 Assessment Methodology

#### 2.2.1 Data Sources

```
┌─────────────────────────────────────────────────────────────────┐
│                    DATA COLLECTION METHODS                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  SURVEYS (Primary)                                              │
│  ├── Employee engagement survey (annual/quarterly)              │
│  ├── 360-degree feedback                                        │
│  ├── Pulse surveys (weekly/monthly)                             │
│  └── Exit interviews                                            │
│                                                                  │
│  BEHAVIORAL DATA (Secondary)                                    │
│  ├── Communication patterns (email, Slack metadata)             │
│  ├── Meeting analytics (frequency, attendance, duration)        │
│  ├── Collaboration tool usage                                   │
│  ├── Code review patterns (for tech orgs)                       │
│  └── Project completion rates                                   │
│                                                                  │
│  STRUCTURAL DATA (Tertiary)                                     │
│  ├── Org chart analysis                                         │
│  ├── Reporting relationships                                    │
│  ├── Budget allocations                                         │
│  └── Policy documentation                                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### 2.2.2 Survey Instrument

**OH₁: Strategic Coherence** (5 items, 7-point Likert)
1. I understand our organization's strategic priorities
2. My team's goals clearly connect to company objectives
3. Leadership communicates a consistent vision
4. When priorities conflict, there are clear principles for resolution
5. Strategic decisions are made transparently

**OH₂: Communication Density** (5 items)
1. I can easily get information I need from other teams
2. Meetings I attend are productive and well-run
3. Important announcements reach me in a timely manner
4. Cross-functional collaboration is supported and encouraged
5. I know who to ask when I need help outside my team

**OH₃: Trust & Reciprocity** (5 items)
1. I feel safe raising concerns or admitting mistakes
2. My colleagues follow through on their commitments
3. People here help each other even when not required
4. I trust my direct manager to have my back
5. Conflicts are resolved fairly and constructively

**OH₄: Role Clarity** (5 items)
1. I clearly understand what is expected of me
2. I know who is responsible for what on my team
3. There is minimal overlap or confusion about ownership
4. Decision rights are clear and appropriate
5. I have the authority to do my job effectively

**OH₅: Knowledge Infrastructure** (5 items)
1. I have access to training and development opportunities
2. Documentation and knowledge bases are useful and up-to-date
3. We learn from our mistakes and successes systematically
4. Knowledge is shared openly across the organization
5. Onboarding effectively prepares new employees

**OH₆: Employee Wellbeing** (5 items)
1. My workload is sustainable over time
2. I can maintain healthy work-life boundaries
3. I feel valued and appreciated for my contributions
4. The organization cares about employee wellbeing
5. I would recommend this as a place to work

**OH₇: Technical Capability** (5 items)
1. Our tools and systems enable me to work effectively
2. Technical debt does not significantly slow us down
3. We adopt new technologies when they add value
4. Our tech stack is reliable and well-maintained
5. I have the equipment and software I need

### 2.3 Scoring Algorithm

```python
import numpy as np
from typing import Dict, List

class OrgKCalculator:
    """
    Calculate Organizational Micro-K score.
    """

    def __init__(self, survey_responses: Dict[str, List[float]]):
        """
        Args:
            survey_responses: Dict mapping harmony codes (OH1-OH7) to
                            list of item responses (1-7 scale)
        """
        self.responses = survey_responses

    def calculate_harmony_score(self, harmony: str) -> float:
        """
        Calculate single harmony score (0-1 scale).
        """
        items = self.responses[harmony]
        raw_mean = np.mean(items)  # 1-7 scale
        normalized = (raw_mean - 1) / 6  # 0-1 scale
        return normalized

    def calculate_org_k(self) -> Dict:
        """
        Calculate overall OrgK and harmony breakdown.

        Returns:
            Dict with 'org_k', 'harmonies', and 'weakest_link'
        """
        harmonies = {}
        for h in ['OH1', 'OH2', 'OH3', 'OH4', 'OH5', 'OH6', 'OH7']:
            harmonies[h] = self.calculate_harmony_score(h)

        # Geometric mean (same as civilization K-Index)
        harmony_values = list(harmonies.values())
        org_k = np.prod(harmony_values) ** (1/7)

        # Identify weakest harmony
        weakest = min(harmonies, key=harmonies.get)

        return {
            'org_k': org_k,
            'harmonies': harmonies,
            'weakest_link': weakest,
            'weakest_value': harmonies[weakest],
            'balance_score': 1 - np.std(harmony_values),  # Lower variance = better balance
            'interpretation': self._interpret(org_k, weakest)
        }

    def _interpret(self, org_k: float, weakest: str) -> str:
        """Generate human-readable interpretation."""
        if org_k >= 0.75:
            level = "Excellent coordination capacity"
        elif org_k >= 0.60:
            level = "Good coordination capacity"
        elif org_k >= 0.45:
            level = "Moderate coordination capacity - improvement needed"
        elif org_k >= 0.30:
            level = "Weak coordination capacity - significant intervention needed"
        else:
            level = "Critical coordination deficit - urgent action required"

        harmony_names = {
            'OH1': 'Strategic Coherence',
            'OH2': 'Communication',
            'OH3': 'Trust',
            'OH4': 'Role Clarity',
            'OH5': 'Knowledge',
            'OH6': 'Wellbeing',
            'OH7': 'Technical Capability'
        }

        return f"{level}. Priority focus: {harmony_names[weakest]}"
```

### 2.4 Benchmarks

| OrgK Score | Interpretation | Typical Characteristics |
|------------|----------------|------------------------|
| **0.80+** | World-class | High-performing tech companies, elite military units, championship sports teams |
| **0.65-0.79** | Excellent | Well-run companies, successful startups post-product-market-fit |
| **0.50-0.64** | Good | Average Fortune 500, stable mid-size companies |
| **0.35-0.49** | Struggling | Companies in decline, post-merger integration issues |
| **<0.35** | Critical | Organizations approaching failure, severe dysfunction |

### 2.5 Use Cases

#### M&A Due Diligence
```
Before acquiring:
1. Assess target company OrgK
2. Compare to acquirer OrgK
3. If target OrgK < 0.4: expect significant integration challenges
4. If target OrgK >> acquirer OrgK: risk destroying target's coordination
5. Plan integration budget based on OrgK gap
```

#### Board-Level Reporting
```
Quarterly OrgK Report to Board:
├── Overall OrgK trend (vs. previous quarter)
├── Harmony breakdown heatmap
├── Peer benchmarking (anonymized industry data)
├── Key initiatives and their impact
└── Risk areas flagged
```

#### Team Formation
```
For optimal team composition:
1. Assess individual micro-K profiles
2. Ensure diversity across harmonies (T-shaped coverage)
3. Include at least one strong H₃ (trust builder)
4. Match H₇ (technical) to project requirements
5. Designate H₁ (strategic) leader
```

---

## 3. City Micro-K (CityK)

### 3.1 Urban Harmonies Framework

```
City K = [CH₁ × CH₂ × CH₃ × CH₄ × CH₅ × CH₆ × CH₇]^(1/7)
```

| Harmony | Name | Indicators |
|---------|------|------------|
| **CH₁** | Municipal Governance | Corruption index, electoral participation, policy effectiveness |
| **CH₂** | Connectivity | Transit coverage, internet access, walkability, commute times |
| **CH₃** | Civic Trust | Social capital surveys, volunteerism, crime rates (inverse) |
| **CH₄** | Economic Diversity | Industry mix, employment distribution, business formation |
| **CH₅** | Educational Infrastructure | School quality, university presence, adult education access |
| **CH₆** | Public Health & Safety | Life expectancy, air quality, public space availability |
| **CH₇** | Innovation Ecosystem | Patents per capita, startup density, tech sector presence |

### 3.2 Data Sources for CityK

```
Available Data:
├── UN Habitat urban indicators
├── OECD Metropolitan Database
├── US Census (for US cities)
├── Numbeo quality of life data
├── Google Environmental Insights Explorer
├── Local government open data portals
├── Academic urban studies datasets
└── Satellite imagery analytics
```

### 3.3 City Rankings Concept

**"World's Most Coordinated Cities"** (Annual Publication)

```
Example Rankings (Illustrative):

Rank | City         | CityK | Strongest | Weakest
-----|--------------|-------|-----------|--------
1    | Copenhagen   | 0.82  | CH₆       | CH₇
2    | Zurich       | 0.80  | CH₁       | CH₄
3    | Singapore    | 0.79  | CH₂       | CH₃
4    | Tokyo        | 0.77  | CH₇       | CH₃
5    | Amsterdam    | 0.76  | CH₃       | CH₇
...
47   | Los Angeles  | 0.58  | CH₇       | CH₂
48   | São Paulo    | 0.55  | CH₄       | CH₆
```

**Product**: Annual report + interactive dashboard + city improvement consulting

---

## 4. Team Micro-K (TeamK)

### 4.1 Small Group Coordination

For teams of 5-15 people, the harmonies adapt:

| Harmony | Team Context | Quick Assessment |
|---------|--------------|------------------|
| **TH₁** | Goal Clarity | "Does everyone know what we're trying to achieve this sprint?" |
| **TH₂** | Information Flow | "Are standups useful? Does info reach everyone?" |
| **TH₃** | Psychological Safety | "Can people disagree openly? Admit mistakes?" |
| **TH₄** | Role Definition | "Does everyone know who does what?" |
| **TH₅** | Skill Coverage | "Do we have the capabilities we need?" |
| **TH₆** | Team Health | "Is anyone burning out? How's morale?" |
| **TH₇** | Tools & Process | "Are our tools helping or hindering?" |

### 4.2 Rapid TeamK Assessment

**5-Minute Team Check-In** (weekly)

```
Each team member rates 1-5:
1. [TH₁] I know our priorities this week
2. [TH₂] I have the info I need
3. [TH₃] I can speak up without fear
4. [TH₄] I know my responsibilities
5. [TH₅] We have the right skills
6. [TH₆] I'm not overwhelmed
7. [TH₇] Our tools work well

TeamK = geometric_mean(responses) / 5
```

### 4.3 Team Intervention Playbook

| If Low | Intervention |
|--------|-------------|
| TH₁ | Team charter workshop, OKR setting session |
| TH₂ | Communication audit, async protocol review |
| TH₃ | Psychological safety training, retrospective format change |
| TH₄ | RACI matrix exercise, role clarity workshop |
| TH₅ | Skills gap analysis, cross-training plan |
| TH₆ | Workload review, wellbeing check-ins |
| TH₇ | Tool audit, process simplification |

---

## 5. Implementation Guide

### 5.1 For Organizations

**Phase 1: Baseline Assessment** (Month 1)
1. Deploy survey instrument to all employees
2. Collect behavioral data from existing systems
3. Calculate baseline OrgK
4. Identify weakest harmonies

**Phase 2: Intervention Design** (Month 2)
1. Form cross-functional improvement team
2. Design targeted interventions for weak harmonies
3. Set improvement targets (realistic: +0.05 OrgK per quarter)
4. Allocate resources

**Phase 3: Implementation** (Months 3-6)
1. Roll out interventions
2. Pulse survey monthly to track progress
3. Adjust based on feedback
4. Document learnings

**Phase 4: Institutionalization** (Ongoing)
1. Integrate OrgK into regular reporting
2. Add OrgK targets to leadership objectives
3. Include in board materials
4. Benchmark against industry peers

### 5.2 For Cities

**Phase 1: Data Collection** (Months 1-3)
1. Identify available data sources
2. Map to CityK framework
3. Fill gaps with targeted surveys
4. Calculate baseline CityK

**Phase 2: Stakeholder Engagement** (Months 4-6)
1. Present findings to city leadership
2. Convene cross-sector working group
3. Prioritize intervention areas
4. Design pilot programs

**Phase 3: Pilot Programs** (Year 1)
1. Implement 2-3 targeted initiatives
2. Measure impact on CityK components
3. Refine approach
4. Scale successful pilots

**Phase 4: Ongoing Measurement** (Annual)
1. Annual CityK assessment
2. Public dashboard
3. Citizen engagement
4. Policy integration

### 5.3 For Teams

**Recommended Cadence**:
- **Weekly**: 5-minute check-in (TH₁-TH₇ quick pulse)
- **Monthly**: Full TeamK assessment
- **Quarterly**: Deep dive + intervention planning
- **Annually**: Comparison across teams

---

## 6. Research Agenda

### 6.1 Validation Studies Needed

1. **Predictive Validity**: Does OrgK predict org performance? (Revenue, retention, innovation)
2. **Cross-Cultural Validity**: Does framework work across cultural contexts?
3. **Temporal Stability**: How stable is OrgK over time?
4. **Intervention Effectiveness**: Which interventions improve which harmonies?
5. **Scale Relationships**: How does TeamK aggregate to OrgK?

### 6.2 Theoretical Extensions

1. **Network Analysis**: Map harmony relationships as network structure
2. **Dynamical Systems**: Model OrgK evolution with differential equations
3. **Agent-Based Models**: Simulate coordination emergence
4. **Cross-Level Effects**: How does national K affect organizational K?

### 6.3 Practical Extensions

1. **Industry Benchmarks**: Build industry-specific norms
2. **Certification Program**: "Micro-K Certified Organization"
3. **Consultant Network**: Train practitioners in framework
4. **Software Platform**: SaaS for ongoing measurement

---

## 7. Ethical Considerations

### 7.1 Privacy

- Survey responses must be confidential
- Behavioral data collection requires consent
- Aggregation rules to prevent individual identification
- No use for performance evaluation of individuals

### 7.2 Misuse Prevention

- OrgK should not be used to justify layoffs
- Low TeamK is not individual's fault
- Results should prompt support, not punishment
- Context always matters (industry, stage, crisis)

### 7.3 Limitations Disclosure

- OrgK is one metric among many
- Not a substitute for leadership judgment
- Cultural biases may affect survey responses
- Quantification has limits

---

## 8. Commercial Model

### 8.1 Product Offerings

| Product | Description | Price Point |
|---------|-------------|-------------|
| **Micro-K Assessment** | One-time OrgK calculation + report | $5,000-$25,000 |
| **Micro-K Monitor** | Ongoing SaaS platform | $99-999/month |
| **Micro-K Consulting** | Intervention design + implementation | $500-1000/hour |
| **Micro-K Certification** | Training program for practitioners | $2,500/person |
| **CityK Report** | Custom city assessment | $50,000-$200,000 |

### 8.2 Go-to-Market Strategy

**Phase 1**: Academic validation (publish in management journals)
**Phase 2**: Pilot with 5 organizations (free/reduced)
**Phase 3**: Case studies + conference presentations
**Phase 4**: Launch commercial product
**Phase 5**: Build consultant network
**Phase 6**: Scale through partnerships

---

## 9. Connection to Civilization K-Index

### 9.1 Aggregation Hypothesis

```
National K ≈ f(OrgK_distribution, CityK_distribution, Institution_Quality)
```

High-K nations should have:
- More high-OrgK organizations
- Higher-ranked cities
- Better institutions translating micro to macro

### 9.2 Research Questions

1. Does improving organizational coordination improve national coordination?
2. Are there threshold effects (minimum OrgK for org survival)?
3. How do multinational corporations affect host country K?
4. Can deliberate Micro-K improvement programs move national K?

---

## Conclusion

The Micro-K Framework demonstrates that coordination is a scale-invariant phenomenon. The same principles that determine civilizational success - governance, connectivity, trust, diversity, knowledge, wellbeing, and capability - operate at every level of human organization.

By measuring and improving coordination at the organizational and urban level, we create the building blocks for improved civilizational coordination. Every organization that raises its OrgK contributes to the collective capacity of humanity to solve coordination problems.

**The vision**: A world where coordination capacity is measured, valued, and systematically improved at every scale.

---

*"The organization is a fractal of civilization. Improve the micro, improve the macro."*

**Last Updated**: December 10, 2025
