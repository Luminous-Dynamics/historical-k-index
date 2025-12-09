#!/usr/bin/env python3
"""
K-Index Early Warning System (KIEWS)
=====================================

A predictive model for detecting coordination breakdown signals before
civilizational collapse occurs. Based on the K-Index framework.

This system monitors:
1. Trust-Technology Gap (Γ) - widening gap signals fragility
2. Harmony Velocity Divergence - harmonies moving in opposite directions
3. Cascade Susceptibility Index - network vulnerability to cascading failures
4. Recovery Capacity Ratio - ability to bounce back from shocks

Warning Levels:
- GREEN (0-25): Stable coordination, normal fluctuations
- YELLOW (25-50): Elevated concern, monitor closely
- ORANGE (50-75): High alert, intervention recommended
- RED (75-100): Critical, imminent coordination failure risk

Author: Tristan Stoltz <tristan.stoltz@luminousdynamics.org>
Date: December 2025
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum
import warnings


class WarningLevel(Enum):
    """Early warning severity levels."""
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


@dataclass
class EarlyWarningSignal:
    """Container for an early warning signal."""
    name: str
    value: float
    threshold: float
    level: WarningLevel
    description: str
    recommendation: str


@dataclass
class KIndexState:
    """Current state of K-Index and harmonies."""
    k_index: float
    h1_governance: float
    h2_interconnection: float
    h3_trust: float
    h4_diversity: float
    h5_knowledge: float
    h6_wellbeing: float
    h7_technology: float
    timestamp: str

    @property
    def harmonies(self) -> np.ndarray:
        return np.array([
            self.h1_governance,
            self.h2_interconnection,
            self.h3_trust,
            self.h4_diversity,
            self.h5_knowledge,
            self.h6_wellbeing,
            self.h7_technology
        ])

    @classmethod
    def from_dict(cls, data: Dict) -> 'KIndexState':
        return cls(**data)


class KIndexEarlyWarningSystem:
    """
    K-Index Early Warning System (KIEWS)

    Monitors K-Index dynamics and generates early warning signals
    for potential coordination breakdown.
    """

    # Critical thresholds from K-Index theory
    COLLAPSE_THRESHOLD = 0.382  # θ - golden ratio threshold
    MODERNIZATION_THRESHOLD = 0.72  # μ* - fragility trap threshold
    TRUST_TECHNOLOGY_GAP_CRITICAL = 0.35  # Γ critical value

    # Warning level thresholds
    YELLOW_THRESHOLD = 25
    ORANGE_THRESHOLD = 50
    RED_THRESHOLD = 75

    def __init__(self, history_window: int = 10):
        """
        Initialize the Early Warning System.

        Args:
            history_window: Number of time periods to consider for trend analysis
        """
        self.history_window = history_window
        self.state_history: List[KIndexState] = []

    def add_state(self, state: KIndexState) -> None:
        """Add a new K-Index state observation."""
        self.state_history.append(state)
        # Keep only recent history
        if len(self.state_history) > self.history_window * 2:
            self.state_history = self.state_history[-self.history_window * 2:]

    def compute_warning_score(self) -> Tuple[float, List[EarlyWarningSignal]]:
        """
        Compute the overall warning score and individual signals.

        Returns:
            Tuple of (overall_score, list_of_signals)
            Score ranges from 0 (safe) to 100 (critical)
        """
        if len(self.state_history) < 2:
            return 0.0, []

        signals = []

        # Signal 1: Trust-Technology Gap (Γ)
        signals.append(self._compute_trust_tech_gap_signal())

        # Signal 2: K-Index Distance to Threshold
        signals.append(self._compute_threshold_distance_signal())

        # Signal 3: Harmony Velocity Divergence
        signals.append(self._compute_velocity_divergence_signal())

        # Signal 4: Trust Erosion Rate
        signals.append(self._compute_trust_erosion_signal())

        # Signal 5: Cascade Susceptibility
        signals.append(self._compute_cascade_susceptibility_signal())

        # Signal 6: Recovery Capacity
        signals.append(self._compute_recovery_capacity_signal())

        # Signal 7: Modernization Paradox Risk
        signals.append(self._compute_modernization_paradox_signal())

        # Compute weighted overall score
        weights = [0.20, 0.15, 0.15, 0.20, 0.10, 0.10, 0.10]
        overall_score = sum(
            w * s.value for w, s in zip(weights, signals)
        )

        return overall_score, signals

    def _compute_trust_tech_gap_signal(self) -> EarlyWarningSignal:
        """Compute Trust-Technology Gap (Γ) warning signal."""
        current = self.state_history[-1]
        gamma = current.h7_technology - current.h3_trust

        # Normalize to 0-100 scale
        # Gap of 0.35+ is critical (100), 0 is safe (0)
        normalized = min(100, max(0, (gamma / self.TRUST_TECHNOLOGY_GAP_CRITICAL) * 100))

        level = self._score_to_level(normalized)

        return EarlyWarningSignal(
            name="Trust-Technology Gap (Γ)",
            value=normalized,
            threshold=self.TRUST_TECHNOLOGY_GAP_CRITICAL,
            level=level,
            description=f"Gap between technology (H₇={current.h7_technology:.2f}) and trust (H₃={current.h3_trust:.2f}) is Γ={gamma:.2f}",
            recommendation="Invest in trust infrastructure: deliberative forums, transparency mechanisms, community building"
        )

    def _compute_threshold_distance_signal(self) -> EarlyWarningSignal:
        """Compute distance to collapse threshold warning."""
        current = self.state_history[-1]

        # Distance above threshold (negative means below threshold!)
        distance = current.k_index - self.COLLAPSE_THRESHOLD

        # Normalize: at threshold (distance=0) = 100, at K=1 (distance=0.62) = 0
        if distance <= 0:
            normalized = 100  # At or below threshold
        else:
            normalized = max(0, 100 - (distance / 0.62) * 100)

        level = self._score_to_level(normalized)

        return EarlyWarningSignal(
            name="Collapse Threshold Distance",
            value=normalized,
            threshold=self.COLLAPSE_THRESHOLD,
            level=level,
            description=f"K-Index ({current.k_index:.3f}) is {distance:.3f} above collapse threshold (θ={self.COLLAPSE_THRESHOLD})",
            recommendation="Strengthen weakest harmonies to increase buffer above collapse threshold"
        )

    def _compute_velocity_divergence_signal(self) -> EarlyWarningSignal:
        """Compute harmony velocity divergence warning."""
        if len(self.state_history) < 3:
            return EarlyWarningSignal(
                name="Harmony Velocity Divergence",
                value=0,
                threshold=0.5,
                level=WarningLevel.GREEN,
                description="Insufficient data for velocity analysis",
                recommendation="Continue monitoring"
            )

        # Compute velocity for each harmony over recent window
        recent = self.state_history[-min(self.history_window, len(self.state_history)):]

        velocities = []
        for i in range(7):
            harmony_values = [s.harmonies[i] for s in recent]
            # Linear regression slope as velocity
            x = np.arange(len(harmony_values))
            slope = np.polyfit(x, harmony_values, 1)[0]
            velocities.append(slope)

        velocities = np.array(velocities)

        # Divergence: some harmonies rising while others falling
        # Measured as standard deviation of velocities
        divergence = np.std(velocities)

        # Also check for opposite signs (true divergence)
        signs = np.sign(velocities)
        opposite_signs = np.sum(signs > 0) > 0 and np.sum(signs < 0) > 0

        # Normalize
        normalized = min(100, divergence * 500)  # Scale factor calibrated empirically
        if opposite_signs:
            normalized = min(100, normalized * 1.5)  # Boost if truly diverging

        level = self._score_to_level(normalized)

        rising = [f"H{i+1}" for i, v in enumerate(velocities) if v > 0.001]
        falling = [f"H{i+1}" for i, v in enumerate(velocities) if v < -0.001]

        return EarlyWarningSignal(
            name="Harmony Velocity Divergence",
            value=normalized,
            threshold=0.05,
            level=level,
            description=f"Rising: {rising}, Falling: {falling}. Std dev of velocities: {divergence:.4f}",
            recommendation="Address falling harmonies while maintaining rising ones - avoid imbalanced development"
        )

    def _compute_trust_erosion_signal(self) -> EarlyWarningSignal:
        """Compute trust (H₃) erosion rate warning."""
        if len(self.state_history) < 3:
            return EarlyWarningSignal(
                name="Trust Erosion Rate",
                value=0,
                threshold=-0.01,
                level=WarningLevel.GREEN,
                description="Insufficient data for trust trend analysis",
                recommendation="Continue monitoring"
            )

        recent = self.state_history[-min(self.history_window, len(self.state_history)):]
        trust_values = [s.h3_trust for s in recent]

        # Compute erosion rate (negative slope = erosion)
        x = np.arange(len(trust_values))
        slope = np.polyfit(x, trust_values, 1)[0]

        # Negative slope is bad; normalize
        # Slope of -0.02 per period is critical
        if slope >= 0:
            normalized = 0
        else:
            normalized = min(100, abs(slope) / 0.02 * 100)

        level = self._score_to_level(normalized)

        trend = "eroding" if slope < 0 else "stable/growing"

        return EarlyWarningSignal(
            name="Trust Erosion Rate",
            value=normalized,
            threshold=-0.01,
            level=level,
            description=f"Trust (H₃) is {trend} at rate {slope:.4f} per period",
            recommendation="Implement trust-building interventions: transparency, participation, reciprocity programs"
        )

    def _compute_cascade_susceptibility_signal(self) -> EarlyWarningSignal:
        """Compute cascade susceptibility index."""
        current = self.state_history[-1]

        # Cascade susceptibility based on:
        # 1. Interconnection level (higher = faster cascades)
        # 2. Minimum harmony (weakest link)
        # 3. Harmony variance (imbalance = vulnerability)

        h2 = current.h2_interconnection
        min_h = min(current.harmonies)
        variance = np.var(current.harmonies)

        # High interconnection + low minimum + high variance = high susceptibility
        susceptibility = h2 * (1 - min_h) * (1 + variance * 5)

        # Normalize to 0-100
        normalized = min(100, susceptibility * 200)

        level = self._score_to_level(normalized)

        weakest_idx = np.argmin(current.harmonies)
        harmony_names = ["H₁ Governance", "H₂ Interconnection", "H₃ Trust",
                        "H₄ Diversity", "H₅ Knowledge", "H₆ Wellbeing", "H₇ Technology"]

        return EarlyWarningSignal(
            name="Cascade Susceptibility Index",
            value=normalized,
            threshold=0.5,
            level=level,
            description=f"Weakest harmony: {harmony_names[weakest_idx]} ({min_h:.2f}). Variance: {variance:.3f}",
            recommendation=f"Strengthen {harmony_names[weakest_idx]} to reduce cascade vulnerability"
        )

    def _compute_recovery_capacity_signal(self) -> EarlyWarningSignal:
        """Compute recovery capacity ratio."""
        current = self.state_history[-1]

        # Recovery capacity based on:
        # 1. Knowledge base (H₅) - ability to diagnose problems
        # 2. Governance quality (H₁) - ability to implement solutions
        # 3. Trust level (H₃) - social cohesion for collective action

        recovery_factors = (current.h5_knowledge + current.h1_governance + current.h3_trust) / 3

        # Fragility factors that impede recovery
        fragility = (current.h7_technology - current.h3_trust)  # Trust-tech gap

        # Net recovery capacity
        capacity = recovery_factors - fragility * 0.5

        # Invert for warning (low capacity = high warning)
        normalized = max(0, min(100, (1 - capacity) * 100))

        level = self._score_to_level(normalized)

        return EarlyWarningSignal(
            name="Recovery Capacity Deficit",
            value=normalized,
            threshold=0.5,
            level=level,
            description=f"Recovery factors: {recovery_factors:.2f}, Fragility offset: {fragility:.2f}",
            recommendation="Build recovery capacity through education, governance reform, and trust-building"
        )

    def _compute_modernization_paradox_signal(self) -> EarlyWarningSignal:
        """Compute Modernization Paradox risk."""
        current = self.state_history[-1]

        # Above modernization threshold + widening gap = high risk
        above_threshold = max(0, current.k_index - self.MODERNIZATION_THRESHOLD)
        gamma = current.h7_technology - current.h3_trust

        # Risk is multiplicative
        risk = above_threshold * gamma * 10  # Scale factor

        normalized = min(100, risk * 100)

        level = self._score_to_level(normalized)

        in_trap = "YES" if current.k_index > self.MODERNIZATION_THRESHOLD else "NO"

        return EarlyWarningSignal(
            name="Modernization Paradox Risk",
            value=normalized,
            threshold=self.MODERNIZATION_THRESHOLD,
            level=level,
            description=f"In fragility trap: {in_trap}. K={current.k_index:.2f}, μ*={self.MODERNIZATION_THRESHOLD}",
            recommendation="If above μ*, invest 2:1 in trust vs technology infrastructure"
        )

    def _score_to_level(self, score: float) -> WarningLevel:
        """Convert numeric score to warning level."""
        if score < self.YELLOW_THRESHOLD:
            return WarningLevel.GREEN
        elif score < self.ORANGE_THRESHOLD:
            return WarningLevel.YELLOW
        elif score < self.RED_THRESHOLD:
            return WarningLevel.ORANGE
        else:
            return WarningLevel.RED

    def get_overall_level(self, score: float) -> WarningLevel:
        """Get overall warning level from score."""
        return self._score_to_level(score)

    def generate_report(self) -> str:
        """Generate a human-readable warning report."""
        score, signals = self.compute_warning_score()
        level = self.get_overall_level(score)

        current = self.state_history[-1] if self.state_history else None

        report = []
        report.append("=" * 70)
        report.append("K-INDEX EARLY WARNING SYSTEM REPORT")
        report.append("=" * 70)

        if current:
            report.append(f"\nTimestamp: {current.timestamp}")
            report.append(f"Current K-Index: {current.k_index:.3f}")

        report.append(f"\n{'='*70}")
        report.append(f"OVERALL WARNING LEVEL: {level.value.upper()}")
        report.append(f"Overall Score: {score:.1f}/100")
        report.append("=" * 70)

        # Color coding explanation
        report.append("\nLegend: GREEN (<25) | YELLOW (25-50) | ORANGE (50-75) | RED (>75)")

        report.append("\n" + "-" * 70)
        report.append("INDIVIDUAL WARNING SIGNALS")
        report.append("-" * 70)

        for signal in signals:
            status_icon = {
                WarningLevel.GREEN: "🟢",
                WarningLevel.YELLOW: "🟡",
                WarningLevel.ORANGE: "🟠",
                WarningLevel.RED: "🔴"
            }[signal.level]

            report.append(f"\n{status_icon} {signal.name}: {signal.value:.1f}/100 [{signal.level.value.upper()}]")
            report.append(f"   {signal.description}")
            report.append(f"   → {signal.recommendation}")

        report.append("\n" + "=" * 70)
        report.append("PRIORITY RECOMMENDATIONS")
        report.append("=" * 70)

        # Sort signals by severity and give top recommendations
        critical_signals = sorted(signals, key=lambda s: s.value, reverse=True)[:3]
        for i, signal in enumerate(critical_signals, 1):
            if signal.value > self.YELLOW_THRESHOLD:
                report.append(f"\n{i}. [{signal.level.value.upper()}] {signal.name}")
                report.append(f"   {signal.recommendation}")

        report.append("\n" + "=" * 70)

        return "\n".join(report)


def create_sample_analysis():
    """Create a sample analysis with realistic modern data."""

    # Initialize system
    ews = KIndexEarlyWarningSystem(history_window=10)

    # Add historical states (simulating 2015-2024 trend)
    historical_data = [
        # year, K, H1, H2, H3, H4, H5, H6, H7
        (2015, 0.76, 0.68, 0.82, 0.58, 0.65, 0.72, 0.78, 0.82),
        (2016, 0.75, 0.67, 0.83, 0.56, 0.65, 0.73, 0.78, 0.83),
        (2017, 0.75, 0.66, 0.84, 0.55, 0.66, 0.74, 0.79, 0.84),
        (2018, 0.74, 0.65, 0.85, 0.53, 0.66, 0.75, 0.79, 0.85),
        (2019, 0.74, 0.64, 0.86, 0.52, 0.67, 0.76, 0.80, 0.86),
        (2020, 0.73, 0.62, 0.84, 0.50, 0.67, 0.75, 0.78, 0.87),  # COVID impact
        (2021, 0.73, 0.61, 0.85, 0.49, 0.68, 0.76, 0.79, 0.88),
        (2022, 0.72, 0.60, 0.86, 0.48, 0.68, 0.77, 0.79, 0.89),
        (2023, 0.72, 0.59, 0.87, 0.47, 0.69, 0.77, 0.80, 0.90),
        (2024, 0.71, 0.58, 0.88, 0.46, 0.69, 0.78, 0.80, 0.91),
    ]

    for year, k, h1, h2, h3, h4, h5, h6, h7 in historical_data:
        state = KIndexState(
            k_index=k,
            h1_governance=h1,
            h2_interconnection=h2,
            h3_trust=h3,
            h4_diversity=h4,
            h5_knowledge=h5,
            h6_wellbeing=h6,
            h7_technology=h7,
            timestamp=f"{year}-12-31"
        )
        ews.add_state(state)

    return ews


if __name__ == "__main__":
    print("K-Index Early Warning System (KIEWS)")
    print("=" * 50)

    # Create sample analysis
    ews = create_sample_analysis()

    # Generate report
    report = ews.generate_report()
    print(report)

    # Get numeric results
    score, signals = ews.compute_warning_score()

    print("\n" + "=" * 50)
    print("PROGRAMMATIC OUTPUT")
    print("=" * 50)
    print(f"Overall Warning Score: {score:.2f}")
    print(f"Warning Level: {ews.get_overall_level(score).value}")
    print(f"Number of signals: {len(signals)}")
    print(f"Red alerts: {sum(1 for s in signals if s.level == WarningLevel.RED)}")
    print(f"Orange alerts: {sum(1 for s in signals if s.level == WarningLevel.ORANGE)}")
