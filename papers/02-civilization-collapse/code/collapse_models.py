"""
Coordination Theory of Collapse: Core Simulation Models

This module implements the computational framework for simulating and analyzing
civilizational collapse dynamics based on the K-Index seven harmonies framework.

Author: Tristan Stoltz / Luminous Dynamics
Date: December 2025
Paper: "Coordination Collapse and Civilizational Decline" (Paper 2)
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, differential_evolution
from scipy import stats
from scipy.signal import detrend
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional, Callable
import warnings


# =============================================================================
# Constants and Default Parameters
# =============================================================================

HARMONY_NAMES = ['H1_Governance', 'H2_Economy', 'H3_Trust',
                 'H4_Complexity', 'H5_Knowledge', 'H6_Wellbeing', 'H7_Technology']

HARMONY_COLORS = {
    'H1': '#8e44ad',  # Purple - Governance
    'H2': '#27ae60',  # Green - Economy
    'H3': '#e74c3c',  # Red - Trust (highlighted)
    'H4': '#f39c12',  # Orange - Complexity
    'H5': '#3498db',  # Blue - Knowledge
    'H6': '#1abc9c',  # Teal - Wellbeing
    'H7': '#95a5a6',  # Gray - Technology
}

# Trust Threshold Hypothesis: Critical H3 value
TRUST_THRESHOLD = 0.37  # θ
TRUST_THRESHOLD_RANGE = (0.35, 0.40)  # Uncertainty range

# Trust Asymmetry: Destruction vs building rate ratio
TRUST_ASYMMETRY_RATIO = 5.0  # k⁻/k⁺ ≈ 3-10

# Complexity Exponent (Law 2: Entropy of Complexity)
COMPLEXITY_EXPONENT = 1.3  # β > 1


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class CascadeParameters:
    """Parameters for the cascade dynamics model."""

    # Sensitivity to drivers
    alpha: Dict[str, float] = field(default_factory=lambda: {
        'H1': 0.05, 'H2': 0.04, 'H3': 0.06,
        'H4': 0.03, 'H5': 0.02, 'H6': 0.03, 'H7': 0.02
    })

    # Cross-harmony coupling
    beta: Dict[str, float] = field(default_factory=lambda: {
        'H1': 0.02, 'H2': 0.015, 'H4': 0.01,
        'H5': 0.015, 'H6': 0.01
    })

    # Shock sensitivity
    gamma: Dict[str, float] = field(default_factory=lambda: {
        'H3': 0.2
    })

    # Natural decay rates
    decay: Dict[str, float] = field(default_factory=lambda: {
        'H1': 0.02, 'H2': 0.02, 'H3': 0.03,
        'H4': 0.015, 'H5': 0.01, 'H6': 0.02, 'H7': 0.01
    })

    # Threshold values
    theta: Dict[str, float] = field(default_factory=lambda: {
        'H1': 0.35, 'H2': 0.35, 'H3': TRUST_THRESHOLD,
        'H4': 0.5, 'H5': 0.4, 'H6': 0.5, 'H7': 0.5
    })

    # External shock magnitude
    external_shock: float = 0.0

    # Infrastructure investment
    infrastructure_investment: float = 0.01

    # Reference values
    S_star: float = 0.5  # Optimal stressor level
    H1_ref: float = 0.7  # Reference governance level


@dataclass
class CollapseCase:
    """Data structure for a historical collapse case study."""

    name: str
    time: np.ndarray
    harmonies: np.ndarray  # Shape: (7, n_timepoints)
    metadata: Dict = field(default_factory=dict)

    @property
    def K(self) -> np.ndarray:
        """Compute K-index as geometric mean of harmonies."""
        return np.prod(self.harmonies, axis=0) ** (1/7)

    @property
    def H3(self) -> np.ndarray:
        """Get H3 (Trust) trajectory."""
        return self.harmonies[2, :]

    def get_harmony(self, index: int) -> np.ndarray:
        """Get specific harmony trajectory."""
        return self.harmonies[index, :]


# =============================================================================
# Core Models
# =============================================================================

class CascadeSimulator:
    """
    Simulate the coupled dynamics of all seven harmonies.

    Implements the cascade dynamics equations from the theoretical framework.
    """

    def __init__(self, params: Optional[CascadeParameters] = None):
        self.params = params or CascadeParameters()

    def _dynamics(self, t: float, H: np.ndarray) -> np.ndarray:
        """
        Compute derivatives for the harmony dynamics system.

        Args:
            t: Current time
            H: Array of harmony values [H1, H2, H3, H4, H5, H6, H7]

        Returns:
            Array of derivatives [dH1/dt, dH2/dt, ..., dH7/dt]
        """
        H1, H2, H3, H4, H5, H6, H7 = np.clip(H, 0.01, 1.0)
        p = self.params

        # Trust dynamics (foundational - Law 1: Trust Primacy)
        dH3 = (p.alpha['H3'] * (H1 * H2 - p.S_star)
               - p.gamma.get('H3', 0.2) * p.external_shock
               - p.decay['H3'] * (1 - H3))

        # Governance depends on trust
        dH1 = (p.alpha['H1'] * (H3 - p.theta['H1'])
               + p.beta.get('H1', 0.02) * H4
               - p.decay['H1'] * (1 - H1))

        # Economy depends on trust and governance
        dH2 = (p.alpha['H2'] * (H3 - p.theta['H2']) * (H1 / p.H1_ref)
               + p.beta.get('H2', 0.015) * H4 * H7
               - p.decay['H2'] * (1 - H2))

        # Complexity depends on governance and economy
        dH4 = (p.alpha['H4'] * (H1 * H2 / p.theta['H4'] - 1)
               + p.beta.get('H4', 0.01) * H5 * H7
               - p.decay['H4'] * (1 - H4))

        # Knowledge depends on complexity and governance
        dH5 = (p.alpha['H5'] * (H4 - p.theta['H5'])
               + p.beta.get('H5', 0.015) * H1
               - p.decay['H5'] * (1 - H5))

        # Wellbeing depends on economy and complexity
        dH6 = (p.alpha['H6'] * (H2 * H4 / p.theta['H6'] - 1)
               + p.beta.get('H6', 0.01) * H7
               - p.decay['H6'] * (1 - H6))

        # Technology depends on complexity and knowledge (persists longest)
        dH7 = (p.alpha['H7'] * (H4 * H5 / p.theta['H7'] - 1)
               + p.infrastructure_investment
               - p.decay['H7'] * (1 - H7))

        return np.array([dH1, dH2, dH3, dH4, dH5, dH6, dH7])

    def simulate(self,
                 H0: np.ndarray,
                 t_span: Tuple[float, float],
                 t_eval: Optional[np.ndarray] = None,
                 method: str = 'RK45') -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Run simulation from initial conditions.

        Args:
            H0: Initial harmony values [H1, H2, ..., H7]
            t_span: (t_start, t_end)
            t_eval: Specific times to evaluate (optional)
            method: Integration method

        Returns:
            Tuple of (time, harmonies, K_index)
        """
        result = solve_ivp(
            self._dynamics,
            t_span,
            H0,
            t_eval=t_eval,
            method=method,
            dense_output=True
        )

        # Clip to valid range
        harmonies = np.clip(result.y, 0.01, 1.0)
        K = np.prod(harmonies, axis=0) ** (1/7)

        return result.t, harmonies, K

    def simulate_with_shock(self,
                           H0: np.ndarray,
                           t_span: Tuple[float, float],
                           shock_time: float,
                           shock_magnitude: float,
                           shock_duration: float = 10.0) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Simulate with a time-varying external shock.

        Args:
            H0: Initial conditions
            t_span: Time span
            shock_time: When shock begins
            shock_magnitude: Peak shock intensity
            shock_duration: How long shock lasts

        Returns:
            Tuple of (time, harmonies, K_index)
        """
        original_shock = self.params.external_shock

        # Simulate pre-shock
        t1, H1, K1 = self.simulate(H0, (t_span[0], shock_time))

        # Simulate during shock
        self.params.external_shock = shock_magnitude
        t2, H2, K2 = self.simulate(H1[:, -1], (shock_time, shock_time + shock_duration))

        # Simulate post-shock
        self.params.external_shock = 0.0
        t3, H3, K3 = self.simulate(H2[:, -1], (shock_time + shock_duration, t_span[1]))

        # Restore original
        self.params.external_shock = original_shock

        # Concatenate results
        t = np.concatenate([t1, t2[1:], t3[1:]])
        H = np.hstack([H1, H2[:, 1:], H3[:, 1:]])
        K = np.concatenate([K1, K2[1:], K3[1:]])

        return t, H, K

    def find_collapse_threshold(self,
                                H0: np.ndarray,
                                shock_range: Tuple[float, float] = (0, 0.5),
                                n_points: int = 50,
                                K_threshold: float = 0.3) -> List[Tuple[float, float, bool]]:
        """
        Find the critical shock magnitude that triggers collapse.

        Returns:
            List of (shock_magnitude, final_K, collapsed) tuples
        """
        results = []

        for shock in np.linspace(*shock_range, n_points):
            self.params.external_shock = shock
            t, H, K = self.simulate(H0, (0, 100))
            final_K = K[-1]
            collapsed = final_K < K_threshold
            results.append((shock, final_K, collapsed))

        self.params.external_shock = 0.0  # Reset
        return results


class PhaseTransitionDetector:
    """
    Detect early warning signals of critical transitions in H3 time series.

    Based on complexity science framework (Scheffer et al.).
    """

    def __init__(self, window_size: int = 10, step: int = 1):
        self.window_size = window_size
        self.step = step

    def compute_early_warning_signals(self,
                                       series: np.ndarray,
                                       detrend_data: bool = True) -> Dict[str, np.ndarray]:
        """
        Compute early warning indicators for a time series.

        Args:
            series: H3 time series
            detrend_data: Whether to remove trend first

        Returns:
            Dict with 'time_index', 'variance', 'autocorrelation', 'skewness'
        """
        if detrend_data:
            data = detrend(series)
        else:
            data = series

        n = len(data)
        indices = range(0, n - self.window_size, self.step)

        results = {
            'time_index': [],
            'variance': [],
            'autocorrelation': [],
            'skewness': [],
            'kurtosis': []
        }

        for i in indices:
            window = data[i:i + self.window_size]

            results['time_index'].append(i + self.window_size // 2)
            results['variance'].append(np.var(window))
            results['autocorrelation'].append(self._ar1_coefficient(window))
            results['skewness'].append(stats.skew(window))
            results['kurtosis'].append(stats.kurtosis(window))

        return {k: np.array(v) for k, v in results.items()}

    def _ar1_coefficient(self, x: np.ndarray) -> float:
        """Estimate AR(1) coefficient (lag-1 autocorrelation)."""
        if len(x) < 3:
            return np.nan
        x_lag = x[:-1]
        x_lead = x[1:]
        if np.std(x_lag) < 1e-10:
            return np.nan
        return np.corrcoef(x_lag, x_lead)[0, 1]

    def compute_csi(self,
                    H3_series: np.ndarray,
                    theta: float = TRUST_THRESHOLD,
                    weights: Tuple[float, float, float, float] = (0.4, 0.3, 0.2, 0.1)) -> np.ndarray:
        """
        Compute Coordination Stress Index (CSI).

        CSI = w₁·(θ - H₃)⁺ + w₂·|dH₃/dt|⁻ + w₃·σ²(H₃) + w₄·AR₁(H₃)

        Args:
            H3_series: Trust time series
            theta: Threshold value
            weights: (w1, w2, w3, w4)

        Returns:
            CSI time series
        """
        w1, w2, w3, w4 = weights

        # Distance below threshold
        distance_below = np.maximum(0, theta - H3_series)

        # Rate of decline
        dH3 = np.gradient(H3_series)
        decline_rate = np.abs(np.minimum(0, dH3))

        # Early warning signals
        ews = self.compute_early_warning_signals(H3_series)

        # Interpolate to match original series length
        var_interp = np.interp(
            range(len(H3_series)),
            ews['time_index'],
            ews['variance']
        )
        var_normalized = var_interp / (np.max(var_interp) + 1e-10)

        ar1_interp = np.interp(
            range(len(H3_series)),
            ews['time_index'],
            ews['autocorrelation']
        )

        # Combine into CSI
        csi = (w1 * distance_below +
               w2 * decline_rate +
               w3 * var_normalized +
               w4 * np.maximum(0, ar1_interp - 0.5))

        return csi

    def collapse_probability(self,
                             csi: float,
                             threshold: float = 0.4,
                             steepness: float = 10.0) -> float:
        """
        Estimate collapse probability from CSI using logistic model.

        P(collapse) = 1 / (1 + exp(-k*(CSI - CSI_threshold)))
        """
        return 1 / (1 + np.exp(-steepness * (csi - threshold)))

    def risk_category(self, csi: float) -> str:
        """Categorize CSI into risk levels."""
        if csi < 0.2:
            return 'LOW'
        elif csi < 0.4:
            return 'MODERATE'
        elif csi < 0.6:
            return 'HIGH'
        else:
            return 'CRITICAL'


class RecoveryAnalyzer:
    """
    Analyze post-collapse recovery dynamics.

    Implements Law 3: Asymmetry of Trust - recovery takes 3-10x longer than collapse.
    """

    def __init__(self, trust_building_rate: float = 0.02):
        self.trust_building_rate = trust_building_rate

    def estimate_recovery_time(self,
                               H3_collapsed: float,
                               H3_target: float = 0.55,
                               recovery_fraction: float = 0.95) -> Dict:
        """
        Estimate time to recover from collapsed H3 state.

        Uses exponential recovery model:
        H₃(t) = H₃_target - (H₃_target - H₃_0) × e^(-k_build × t)

        Args:
            H3_collapsed: H3 value at nadir
            H3_target: Target H3 for recovery
            recovery_fraction: Fraction of gap to close (0.95 = 95%)

        Returns:
            Dict with recovery metrics
        """
        if H3_target <= H3_collapsed:
            return {'recovery_time': 0, 'message': 'Already at target'}

        gap = H3_target - H3_collapsed

        # Time to reach specified fraction of target
        # Solve: 1 - e^(-k*t) = recovery_fraction
        recovery_time = -np.log(1 - recovery_fraction) / self.trust_building_rate

        # Scale by gap size
        recovery_time *= gap / (H3_target - TRUST_THRESHOLD)

        return {
            'h3_recovery_time': recovery_time,
            'full_recovery_time': recovery_time * 1.3,  # Other harmonies follow
            'h3_gap': gap,
            'effective_rate': self.trust_building_rate,
            'asymmetry_explanation': f"At rate {self.trust_building_rate}, trust builds "
                                     f"~{1/self.trust_building_rate:.0f}x slower than typical erosion"
        }

    def compute_asymmetry_ratio(self,
                                collapse_duration: float,
                                recovery_duration: float) -> float:
        """Compute collapse/recovery asymmetry ratio."""
        if collapse_duration <= 0:
            return float('inf')
        return recovery_duration / collapse_duration

    def analyze_historical_case(self, case: CollapseCase) -> Dict:
        """
        Analyze collapse and recovery dynamics for a historical case.

        Returns asymmetry metrics if recovery data available.
        """
        K = case.K
        H3 = case.H3
        t = case.time

        # Find peak
        peak_idx = np.argmax(K)
        peak_K = K[peak_idx]
        peak_t = t[peak_idx]

        # Find nadir (after peak)
        nadir_idx = np.argmin(K[peak_idx:]) + peak_idx
        nadir_K = K[nadir_idx]
        nadir_t = t[nadir_idx]

        collapse_duration = nadir_t - peak_t

        # Look for recovery (if data extends beyond nadir)
        if nadir_idx < len(K) - 1:
            # Define recovery as return to 50% of pre-collapse level
            recovery_threshold = nadir_K + 0.5 * (peak_K - nadir_K)
            recovery_indices = np.where(K[nadir_idx:] > recovery_threshold)[0]

            if len(recovery_indices) > 0:
                recovery_idx = recovery_indices[0] + nadir_idx
                recovery_t = t[recovery_idx]
                recovery_duration = recovery_t - nadir_t
                asymmetry = self.compute_asymmetry_ratio(collapse_duration, recovery_duration)
            else:
                recovery_duration = None
                asymmetry = None
        else:
            recovery_duration = None
            asymmetry = None

        return {
            'case': case.name,
            'peak_K': peak_K,
            'peak_t': peak_t,
            'nadir_K': nadir_K,
            'nadir_t': nadir_t,
            'collapse_duration': collapse_duration,
            'recovery_duration': recovery_duration,
            'asymmetry_ratio': asymmetry,
            'H3_at_nadir': H3[nadir_idx],
            'below_threshold': H3[nadir_idx] < TRUST_THRESHOLD
        }


class MultiCaseComparator:
    """
    Compare collapse dynamics across multiple historical cases.
    """

    def __init__(self, cases: List[CollapseCase]):
        self.cases = cases

    def compare_cascade_sequences(self) -> Dict:
        """
        Compare the order in which harmonies decline across cases.

        Returns pattern analysis with modal sequence.
        """
        results = []

        for case in self.cases:
            sequence = self._extract_decline_sequence(case)
            results.append({
                'case': case.name,
                'sequence': sequence,
                'first_to_decline': sequence[0] if sequence else None,
                'last_to_decline': sequence[-1] if sequence else None
            })

        # Find modal patterns
        all_sequences = [r['sequence'] for r in results if r['sequence']]
        first_harmonies = [s[0] for s in all_sequences if s]
        last_harmonies = [s[-1] for s in all_sequences if s]

        modal_first = stats.mode(first_harmonies, keepdims=True).mode[0] if first_harmonies else None
        modal_last = stats.mode(last_harmonies, keepdims=True).mode[0] if last_harmonies else None

        return {
            'individual_sequences': results,
            'modal_first': modal_first,
            'modal_last': modal_last,
            'H3_first_count': sum(1 for r in results if r['first_to_decline'] == 'H3'),
            'H7_last_count': sum(1 for r in results if r['last_to_decline'] == 'H7'),
            'supports_hypothesis': (modal_first == 'H3' and modal_last == 'H7')
        }

    def _extract_decline_sequence(self, case: CollapseCase) -> List[str]:
        """Extract order in which harmonies began declining."""
        sequences = []

        for i in range(7):
            series = case.harmonies[i, :]
            # Find when decline began (peak before nadir)
            peak_idx = np.argmax(series)
            if peak_idx < len(series) - 1:
                sequences.append((f'H{i+1}', peak_idx))

        # Sort by timing
        sequences.sort(key=lambda x: x[1])
        return [s[0] for s in sequences]

    def compare_H3_thresholds(self) -> Dict:
        """
        Compare H3 values at the point collapse became irreversible.

        Tests the Trust Threshold Hypothesis.
        """
        results = []

        for case in self.cases:
            K = case.K
            H3 = case.H3

            # Find inflection point (maximum decline acceleration)
            dK = np.gradient(K)
            d2K = np.gradient(dK)
            inflection_idx = np.argmin(d2K)

            H3_at_inflection = H3[inflection_idx]

            results.append({
                'case': case.name,
                'H3_at_inflection': H3_at_inflection,
                'below_threshold': H3_at_inflection < 0.40,
                'in_threshold_range': TRUST_THRESHOLD_RANGE[0] < H3_at_inflection < TRUST_THRESHOLD_RANGE[1]
            })

        H3_values = [r['H3_at_inflection'] for r in results]

        return {
            'individual_cases': results,
            'mean_H3_at_inflection': np.mean(H3_values),
            'std_H3_at_inflection': np.std(H3_values),
            'all_below_040': all(v < 0.40 for v in H3_values),
            'all_in_range': all(r['in_threshold_range'] for r in results),
            'supports_threshold_hypothesis': all(r['below_threshold'] for r in results)
        }

    def compare_speed_capacity(self) -> Dict:
        """
        Test Hypothesis 3: Higher pre-crisis K → slower collapse.
        """
        peak_Ks = []
        durations = []

        for case in self.cases:
            K = case.K
            t = case.time

            peak_idx = np.argmax(K)
            nadir_idx = np.argmin(K[peak_idx:]) + peak_idx

            peak_K = K[peak_idx]
            duration = t[nadir_idx] - t[peak_idx]

            peak_Ks.append(peak_K)
            durations.append(duration)

        correlation, p_value = stats.pearsonr(peak_Ks, durations)

        return {
            'cases': [c.name for c in self.cases],
            'peak_Ks': peak_Ks,
            'collapse_durations': durations,
            'correlation': correlation,
            'p_value': p_value,
            'supports_hypothesis': correlation > 0.3 and p_value < 0.1
        }


# =============================================================================
# Utility Functions
# =============================================================================

def compute_k_index(harmonies: np.ndarray) -> np.ndarray:
    """Compute K-index as geometric mean of harmonies."""
    return np.prod(harmonies, axis=0) ** (1/7)


def collapse_probability_function(H3: float,
                                   theta: float = TRUST_THRESHOLD,
                                   k: float = 10.0) -> float:
    """
    Compute collapse probability given H3 level.

    P(collapse) = 1 / (1 + e^(k(H₃ - θ)))
    """
    return 1 / (1 + np.exp(k * (H3 - theta)))


def trust_asymmetry_ratio(
    build_rate: float = 0.02,
    erosion_rate: float = 0.10
) -> float:
    """
    Compute trust asymmetry ratio (Law 3).

    Trust destruction rate / Trust building rate ≈ 3-10
    """
    return erosion_rate / build_rate


# =============================================================================
# Example Usage and Demonstration
# =============================================================================

def demo_cascade_simulation():
    """Demonstrate cascade dynamics simulation."""

    print("=" * 60)
    print("Cascade Dynamics Simulation Demo")
    print("=" * 60)

    # Initial conditions (stable society)
    H0 = np.array([0.7, 0.7, 0.6, 0.65, 0.6, 0.65, 0.75])

    # Create simulator
    simulator = CascadeSimulator()

    # Simulate without shock
    print("\n1. Baseline simulation (no shock):")
    t, H, K = simulator.simulate(H0, (0, 100))
    print(f"   Initial K: {K[0]:.3f}")
    print(f"   Final K: {K[-1]:.3f}")

    # Simulate with shock
    print("\n2. Simulation with external shock:")
    t_shock, H_shock, K_shock = simulator.simulate_with_shock(
        H0, (0, 150), shock_time=50, shock_magnitude=0.3, shock_duration=20
    )
    print(f"   Pre-shock K: {K_shock[45]:.3f}")
    print(f"   During shock K: {K_shock[60]:.3f}")
    print(f"   Post-shock K: {K_shock[-1]:.3f}")

    # Find collapse threshold
    print("\n3. Finding collapse threshold:")
    thresholds = simulator.find_collapse_threshold(H0, shock_range=(0, 0.5), n_points=20)
    collapse_threshold = None
    for shock, final_K, collapsed in thresholds:
        if collapsed and collapse_threshold is None:
            collapse_threshold = shock
            print(f"   Collapse threshold: shock magnitude ≈ {shock:.2f}")
            print(f"   Final K at threshold: {final_K:.3f}")
            break

    return t_shock, H_shock, K_shock


def demo_early_warning_signals():
    """Demonstrate early warning signal detection."""

    print("\n" + "=" * 60)
    print("Early Warning Signals Demo")
    print("=" * 60)

    # Create synthetic H3 trajectory with approaching transition
    np.random.seed(42)
    n = 100
    t = np.linspace(0, 100, n)

    # H3 declining toward threshold with increasing variance
    base = 0.6 - 0.003 * t  # Slow decline
    noise = np.random.randn(n) * (0.02 + 0.001 * t)  # Increasing variance
    H3 = base + noise

    # Detect early warning signals
    detector = PhaseTransitionDetector(window_size=15)
    ews = detector.compute_early_warning_signals(H3)

    print("\nEarly warning indicators over time:")
    print(f"   Initial variance: {ews['variance'][0]:.4f}")
    print(f"   Final variance: {ews['variance'][-1]:.4f}")
    print(f"   Variance increase: {(ews['variance'][-1] / ews['variance'][0] - 1) * 100:.1f}%")
    print(f"   Initial autocorrelation: {ews['autocorrelation'][0]:.3f}")
    print(f"   Final autocorrelation: {ews['autocorrelation'][-1]:.3f}")

    # Compute CSI
    csi = detector.compute_csi(H3)
    print(f"\nCoordination Stress Index:")
    print(f"   Initial CSI: {csi[0]:.3f} ({detector.risk_category(csi[0])})")
    print(f"   Final CSI: {csi[-1]:.3f} ({detector.risk_category(csi[-1])})")
    print(f"   Collapse probability: {detector.collapse_probability(csi[-1]):.1%}")

    return t, H3, csi


def demo_recovery_analysis():
    """Demonstrate recovery dynamics analysis."""

    print("\n" + "=" * 60)
    print("Recovery Dynamics Demo")
    print("=" * 60)

    analyzer = RecoveryAnalyzer()

    # Estimate recovery from collapsed state
    H3_collapsed = 0.25
    recovery = analyzer.estimate_recovery_time(H3_collapsed)

    print(f"\nRecovery from H₃ = {H3_collapsed}:")
    print(f"   H₃ gap to close: {recovery['h3_gap']:.2f}")
    print(f"   Estimated H₃ recovery time: {recovery['h3_recovery_time']:.1f} time units")
    print(f"   Full recovery time: {recovery['full_recovery_time']:.1f} time units")
    print(f"   {recovery['asymmetry_explanation']}")

    return recovery


if __name__ == "__main__":
    # Run demonstrations
    demo_cascade_simulation()
    demo_early_warning_signals()
    demo_recovery_analysis()

    print("\n" + "=" * 60)
    print("All demonstrations complete!")
    print("=" * 60)
