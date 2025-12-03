# Community Governance Framework

> **How We Make Decisions Together**

---

## Vision

The Historical K-Index Research Program is a **community-driven open science initiative**. We believe the best science emerges from diverse perspectives, transparent processes, and shared ownership of knowledge.

This document establishes how we make decisions, resolve disagreements, and ensure the research program serves the global coordination science community.

---

## Core Principles

### 1. Radical Transparency
- All discussions happen in public (GitHub Discussions, Issues)
- Decision rationale is always documented
- Data, code, and methods are fully open
- Conflicts of interest are disclosed

### 2. Merit-Based Contribution
- Ideas judged on quality, not credentials
- Equal opportunity for all to propose research
- Credit generously shared
- Co-authorship based on contribution, not position

### 3. Scientific Rigor First
- Methodology trumps convenience
- Reproducibility is non-negotiable
- Peer review before major changes
- Community validation for paradigm shifts

### 4. Inclusive Participation
- Multiple ways to contribute (code, data, ideas, review)
- Clear pathways from idea to implementation
- Mentorship for newcomers
- Accessibility as a design constraint

---

## Decision-Making Structure

### Tier 1: Routine Maintenance (Fast Track)
**Examples**: Bug fixes, documentation improvements, data updates, minor enhancements

**Process**:
1. Open a Pull Request
2. Passes automated tests
3. Core maintainer review (24-48h)
4. Merge if approved

**Decision Makers**: Core Maintainers (currently: Tristan Stoltz)

**Timeline**: 1-3 days

---

### Tier 2: Significant Changes (Community Review)
**Examples**: New features, methodology adjustments, Papers 4-10 proposals

**Process**:
1. Open GitHub Issue using appropriate template
2. Community discussion (minimum 7 days)
3. Address feedback and iterate
4. Maintainer synthesis of consensus
5. Final decision with rationale documented

**Decision Makers**: Core Maintainers + Active Contributors (5+ substantive contributions)

**Timeline**: 2-4 weeks

**Consensus Criteria**:
- Majority support from Active Contributors
- No unresolved blocking concerns
- Methodology validated by domain experts
- Alignment with research program vision

---

### Tier 3: Paradigm-Level Changes (Full Community Vote)
**Examples**: Changes to core methodology (H₁-H₇ definitions), data source replacements, major theoretical pivots

**Process**:
1. Formal proposal document (minimum 5 pages)
2. Open comment period (30 days)
3. Virtual town hall meeting
4. Revision based on feedback
5. Community-wide vote
6. Implementation roadmap if approved

**Decision Makers**: All contributors with merged PRs or approved Issues

**Voting**:
- One person, one vote
- 2/3 majority required for approval
- Minimum 20 participants for quorum

**Timeline**: 2-3 months

---

## Research Proposal Process (Papers 4+)

### Phase 1: Idea Submission
**Who**: Anyone
**How**: GitHub Issue using "Research Proposal" template
**Content**:
- Research question
- Methodology outline
- Data requirements
- Expected contribution
- Proposed timeline

**Review**: Community feedback within 14 days

---

### Phase 2: Proposal Development
**Who**: Proposal author + interested collaborators
**How**: Collaborative Google Doc or GitHub Discussion
**Content**:
- Full methodology
- Literature review
- Data analysis plan
- Expected results
- Resource requirements

**Milestone**: Proposal acceptance vote (majority of Active Contributors)

---

### Phase 3: Implementation
**Who**: Approved research team
**How**: Dedicated branch in repository
**Milestones**:
- Data collection complete
- Analysis complete
- Draft manuscript
- Peer review
- Final publication

**Support**: Access to shared data, computational resources, co-author network

---

### Phase 4: Publication & Integration
**Who**: Research team + Community reviewers
**How**:
- Manuscript submitted to journal
- Preprint on ArXiv
- Code/data merged to main repository
- Results integrated into framework

**Recognition**: Co-authorship based on contribution guidelines

---

## Roles & Responsibilities

### Core Maintainers
**Current**: Tristan Stoltz (tristan.stoltz@evolvingresonantcocreationism.com)

**Responsibilities**:
- Maintain repository infrastructure
- Coordinate research program
- Final decision on Tier 1 & 2 changes
- Facilitate Tier 3 community votes
- Ensure scientific integrity
- Manage conflicts of interest

**Selection**: Appointed by existing maintainers based on sustained, high-quality contributions (minimum 1 year)

---

### Active Contributors
**Criteria**: 5+ merged PRs or approved Issues in past 12 months

**Privileges**:
- Vote on Tier 2 & 3 changes
- Propose research (Papers 4+)
- Review pull requests
- Participate in governance discussions

**Recognition**: Listed in CONTRIBUTORS.md

---

### Community Members
**Criteria**: Anyone interested in coordination science

**Privileges**:
- Open Issues
- Comment on proposals
- Submit pull requests
- Vote on Tier 3 changes (if merged contribution)

**Recognition**: All contributions acknowledged

---

## Conflict Resolution

### Level 1: Direct Discussion
- Parties discuss directly in GitHub Issue/Discussion
- Seek mutual understanding
- Document points of agreement and disagreement

---

### Level 2: Mediation
- Core Maintainer facilitates discussion
- Focus on shared goals
- Explore compromise solutions
- Document resolution

---

### Level 3: Community Arbitration
- If unresolved after 30 days
- Case presented to Active Contributors
- Advisory vote on resolution
- Core Maintainers implement decision

---

### Level 4: Fork (Last Resort)
- If irreconcilable differences
- Community can fork repository
- Both projects continue independently
- Original project retains governance

---

## Research Ethics

### Authorship Guidelines
Based on ICMJE criteria:

**Co-authorship requires**:
1. Substantial intellectual contribution
2. Drafting or critical revision of manuscript
3. Approval of final version
4. Accountability for accuracy

**Not sufficient alone**:
- Data collection only
- Funding acquisition only
- General supervision only

**Process**: Authorship discussed at project start, revisited before submission

---

### Data Ethics
- All data sources properly cited
- Privacy protections for individual-level data
- No proprietary data without explicit license
- Replication data archived permanently

---

### Conflicts of Interest
**Disclosure required for**:
- Financial relationships with entities benefiting from results
- Personal relationships affecting objectivity
- Professional positions creating bias

**Process**: Disclosed in manuscript acknowledgments

---

## Amendments to This Document

**Process**: Tier 3 (Paradigm-Level Change)
- Proposed amendments open for 30-day comment
- Community vote required
- 2/3 majority for approval

**Version History**: All changes tracked in Git

---

## Getting Started with Governance

### I want to propose a new research paper (Paper 4+)
→ Open a GitHub Issue using the "Research Proposal" template
→ See [Research Proposal Process](#research-proposal-process-papers-4)

### I found a bug or want to improve documentation
→ Open a Pull Request with the fix
→ See [Tier 1: Routine Maintenance](#tier-1-routine-maintenance-fast-track)

### I have an idea for a major methodology change
→ Open a GitHub Discussion to gauge community interest
→ If support, follow [Tier 3: Paradigm-Level Changes](#tier-3-paradigm-level-changes-full-community-vote)

### I disagree with a decision
→ Comment on the relevant Issue/Discussion
→ If unresolved, request mediation
→ See [Conflict Resolution](#conflict-resolution)

### I want to become an Active Contributor
→ Start contributing! (PRs, Issues, Reviews)
→ After 5+ merged contributions, you're automatically recognized

---

## Appendix: Governance Evolution

### Version 1.0 (Current)
- Single core maintainer (Tristan Stoltz)
- Community input via Issues/Discussions
- Three-tier decision framework

### Future Considerations
As the community grows, we may need:
- **Steering Committee**: Elected representatives from diverse domains
- **Domain Working Groups**: Specialized teams for different harmonies
- **Regional Chapters**: Local coordination science communities
- **Foundation Governance**: If sustained funding requires legal structure

**These changes will follow Tier 3 amendment process.**

---

## Questions?

- **General Governance**: Open a GitHub Discussion tagged "governance"
- **Specific Decisions**: Comment on relevant Issue/PR
- **Private Concerns**: Email core maintainers directly

---

**Current Version**: 1.0
**Last Updated**: December 3, 2025
**Next Review**: June 3, 2026 (or as needed)

---

*"The best science is done in the open, with clear rules, and shared ownership. This governance framework ensures the K-Index research program serves the global coordination science community for decades to come."*

**We coordinate to study coordination.** 🌊
