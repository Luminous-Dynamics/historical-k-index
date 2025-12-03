# Predictive Models: Computational Frameworks for Collapse Analysis

> **"A theory that cannot be simulated cannot be fully understood."**

---

## Overview

This document provides computational frameworks for testing the Coordination Theory of Collapse. Each model is designed to be:

1. **Implementable** in Python/Julia
2. **Calibratable** to historical data
3. **Falsifiable** against empirical observations
4. **Useful** for policy scenario analysis

---

## Model 1: The Cascade Dynamics Simulator

### Purpose
Simulate the coupled dynamics of all seven harmonies to understand cascade effects and identify intervention points.

### Mathematical Foundation

**System of Coupled ODEs**:
```python
# Harmony Dynamics System
def cascade_dynamics(t, H, params):
    """
    H = [H1, H2, H3, H4, H5, H6, H7]
    params = dict with all rate constants and thresholds
    """
    H1, H2, H3, H4, H5, H6, H7 = H

    # Trust dynamics (foundational)
    dH3 = (params['alpha3'] * (H1 * H2 - params['S_star'])
           - params['gamma3'] * params['external_shock']
           - params['decay3'] * (1 - H3))

    # Governance depends on trust
    dH1 = (params['alpha1'] * (H3 - params['theta1'])
           + params['beta1'] * H4
           - params['decay1'] * (1 - H1))

    # Economy depends on trust and governance
    dH2 = (params['alpha2'] * (H3 - params['theta2'])
           * (H1 / params['H1_ref'])
           + params['beta2'] * H4 * H7
           - params['decay2'] * (1 - H2))

    # Complexity depends on governance and economy
    dH4 = (params['alpha4'] * (H1 * H2 / params['theta4'] - 1)
           + params['beta4'] * H5 * H7
           - params['decay4'] * (1 - H4))

    # Knowledge depends on complexity and governance
    dH5 = (params['alpha5'] * (H4 - params['theta5'])
           + params['beta5'] * H1
           - params['decay5'] * (1 - H5))

    # Wellbeing depends on economy and complexity
    dH6 = (params['alpha6'] * (H2 * H4 / params['theta6'] - 1)
           + params['beta6'] * H7
           - params['decay6'] * (1 - H6))

    # Technology depends on complexity and knowledge
    dH7 = (params['alpha7'] * (H4 * H5 / params['theta7'] - 1)
           + params['I_t']  # Infrastructure investment
           - params['decay7'] * (1 - H7))

    return [dH1, dH2, dH3, dH4, dH5, dH6, dH7]
```

### Key Parameters

| Parameter | Description | Typical Range | Calibration Source |
|-----------|-------------|---------------|-------------------|
| `alpha_i` | Sensitivity to drivers | 0.01-0.10 | Historical case studies |
| `beta_i` | Cross-harmony coupling | 0.005-0.05 | Correlation analysis |
| `gamma_i` | Shock sensitivity | 0.1-0.5 | Event study analysis |
| `decay_i` | Natural entropy rate | 0.01-0.05 | Long-term trend analysis |
| `theta_i` | Threshold values | 0.3-0.5 | Collapse point identification |

### Implementation

```python
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class CascadeSimulator:
    """
    Simulate coordination cascade dynamics.
    """

    def __init__(self, params=None):
        self.params = params or self._default_params()

    def _default_params(self):
        return {
            'alpha1': 0.05, 'alpha2': 0.04, 'alpha3': 0.06,
            'alpha4': 0.03, 'alpha5': 0.02, 'alpha6': 0.03, 'alpha7': 0.02,
            'beta1': 0.02, 'beta2': 0.015, 'beta4': 0.01,
            'beta5': 0.015, 'beta6': 0.01,
            'gamma3': 0.2,
            'decay1': 0.02, 'decay2': 0.02, 'decay3': 0.03,
            'decay4': 0.015, 'decay5': 0.01, 'decay6': 0.02, 'decay7': 0.01,
            'theta1': 0.35, 'theta2': 0.35, 'theta4': 0.5,
            'theta5': 0.4, 'theta6': 0.5, 'theta7': 0.5,
            'S_star': 0.5, 'H1_ref': 0.7,
            'external_shock': 0.0, 'I_t': 0.01
        }

    def simulate(self, H0, t_span, t_eval=None, shock_times=None, shock_magnitudes=None):
        """
        Run simulation with optional shock events.

        H0: Initial harmony values [H1, H2, ..., H7]
        t_span: (t_start, t_end)
        shock_times: list of times when shocks occur
        shock_magnitudes: corresponding shock intensities
        """

        if shock_times is None:
            # Simple simulation without shocks
            result = solve_ivp(
                lambda t, H: self._dynamics(t, H),
                t_span, H0, t_eval=t_eval, method='RK45'
            )
            return result.t, result.y, self._compute_K(result.y)
        else:
            # Simulation with shock events
            return self._simulate_with_shocks(
                H0, t_span, t_eval, shock_times, shock_magnitudes
            )

    def _dynamics(self, t, H):
        """Core dynamics function."""
        return cascade_dynamics(t, H, self.params)

    def _compute_K(self, H_array):
        """Compute K-index as geometric mean."""
        return np.prod(H_array, axis=0) ** (1/7)

    def find_threshold(self, H0, shock_range=(0, 1), n_points=50):
        """
        Find the critical shock magnitude that triggers collapse.
        """
        thresholds = []
        for shock in np.linspace(*shock_range, n_points):
            self.params['external_shock'] = shock
            t, H, K = self.simulate(H0, (0, 100))
            final_K = K[-1]
            thresholds.append((shock, final_K))

        return thresholds

    def sensitivity_analysis(self, H0, param_name, param_range, n_runs=20):
        """
        Analyze sensitivity to a specific parameter.
        """
        results = []
        base_value = self.params[param_name]

        for val in np.linspace(*param_range, n_runs):
            self.params[param_name] = val
            t, H, K = self.simulate(H0, (0, 100))
            results.append({
                'param_value': val,
                'final_K': K[-1],
                'min_K': K.min(),
                'collapse_time': self._find_collapse_time(K)
            })

        self.params[param_name] = base_value  # Reset
        return results

    def _find_collapse_time(self, K, threshold=0.3):
        """Find time when K first drops below threshold."""
        below = np.where(K < threshold)[0]
        return below[0] if len(below) > 0 else None
```

---

## Model 2: The Phase Transition Detector

### Purpose
Identify early warning signals of critical transitions in harmony time series.

### Mathematical Foundation

Near a critical transition, systems exhibit:

1. **Critical Slowing Down**: Slower recovery from perturbations
2. **Increased Variance**: Larger fluctuations
3. **Increased Autocorrelation**: Longer memory
4. **Flickering**: Jumping between states

### Implementation

```python
import numpy as np
from scipy import stats
from scipy.signal import detrend

class PhaseTransitionDetector:
    """
    Detect early warning signals of critical transitions.
    """

    def __init__(self, window_size=10, step=1):
        self.window_size = window_size
        self.step = step

    def analyze(self, time_series, detrend_data=True):
        """
        Analyze time series for early warning signals.

        Returns dict with:
        - variance: rolling variance
        - autocorrelation: rolling AR(1) coefficient
        - skewness: rolling skewness
        - recovery_rate: estimated recovery rate from perturbations
        """

        if detrend_data:
            data = detrend(time_series)
        else:
            data = time_series

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
            results['autocorrelation'].append(self._ar1_coef(window))
            results['skewness'].append(stats.skew(window))
            results['kurtosis'].append(stats.kurtosis(window))

        return results

    def _ar1_coef(self, x):
        """Estimate AR(1) coefficient."""
        if len(x) < 3:
            return np.nan
        x_lag = x[:-1]
        x_lead = x[1:]
        if np.std(x_lag) == 0:
            return np.nan
        return np.corrcoef(x_lag, x_lead)[0, 1]

    def compute_csi(self, H3_series, theta=0.37, weights=(0.4, 0.3, 0.2, 0.1)):
        """
        Compute Coordination Stress Index.

        CSI = w1*(theta - H3)+ + w2*|dH3/dt|- + w3*variance + w4*autocorr
        """
        w1, w2, w3, w4 = weights

        # Distance below threshold
        distance_below = np.maximum(0, theta - H3_series)

        # Rate of decline
        dH3 = np.gradient(H3_series)
        decline_rate = np.abs(np.minimum(0, dH3))

        # Early warning signals
        ews = self.analyze(H3_series)
        var_normalized = np.interp(
            range(len(H3_series)),
            ews['time_index'],
            ews['variance']
        )
        var_normalized = var_normalized / np.max(var_normalized) if np.max(var_normalized) > 0 else var_normalized

        ar1_normalized = np.interp(
            range(len(H3_series)),
            ews['time_index'],
            ews['autocorrelation']
        )

        # Combine into CSI
        csi = (w1 * distance_below +
               w2 * decline_rate +
               w3 * var_normalized +
               w4 * np.maximum(0, ar1_normalized - 0.5))

        return csi

    def predict_collapse_probability(self, csi_current, csi_history=None):
        """
        Estimate collapse probability based on CSI.

        Uses logistic model: P(collapse) = 1 / (1 + exp(-k*(CSI - CSI_threshold)))
        """
        CSI_THRESHOLD = 0.4
        K_STEEPNESS = 10

        p_collapse = 1 / (1 + np.exp(-K_STEEPNESS * (csi_current - CSI_THRESHOLD)))

        return p_collapse
```

---

## Model 3: The Historical Calibrator

### Purpose
Calibrate model parameters to match historical collapse trajectories.

### Approach
Use Bayesian inference to estimate parameters that best reproduce observed harmony trajectories.

### Implementation

```python
import numpy as np
from scipy.optimize import minimize, differential_evolution

class HistoricalCalibrator:
    """
    Calibrate cascade model to historical data.
    """

    def __init__(self, simulator):
        self.simulator = simulator

    def calibrate(self, observed_data, param_bounds, method='differential_evolution'):
        """
        Fit model parameters to observed harmony trajectories.

        observed_data: dict with keys 't' and 'H' (7 x n array)
        param_bounds: dict mapping param names to (min, max) tuples
        """

        param_names = list(param_bounds.keys())
        bounds = [param_bounds[p] for p in param_names]

        def objective(param_values):
            # Set parameters
            for name, val in zip(param_names, param_values):
                self.simulator.params[name] = val

            # Simulate
            H0 = observed_data['H'][:, 0]
            t_obs = observed_data['t']
            try:
                t_sim, H_sim, K_sim = self.simulator.simulate(
                    H0, (t_obs[0], t_obs[-1]), t_eval=t_obs
                )
            except:
                return 1e10  # Return large value on simulation failure

            # Compute error (mean squared error across all harmonies)
            H_obs = observed_data['H']
            error = np.mean((H_sim - H_obs) ** 2)

            return error

        if method == 'differential_evolution':
            result = differential_evolution(objective, bounds, seed=42)
        else:
            x0 = [(b[0] + b[1]) / 2 for b in bounds]
            result = minimize(objective, x0, bounds=bounds, method='L-BFGS-B')

        # Extract best parameters
        best_params = {name: val for name, val in zip(param_names, result.x)}

        return {
            'params': best_params,
            'error': result.fun,
            'success': result.success
        }

    def cross_validate(self, all_cases, param_bounds, n_folds=4):
        """
        Cross-validate calibration across historical cases.

        Leave-one-out: train on 3 cases, test on 1.
        """
        results = []

        for i, test_case in enumerate(all_cases):
            train_cases = [c for j, c in enumerate(all_cases) if j != i]

            # Aggregate training data
            train_data = self._aggregate_cases(train_cases)

            # Calibrate on training data
            cal_result = self.calibrate(train_data, param_bounds)

            # Test on held-out case
            test_error = self._compute_test_error(test_case, cal_result['params'])

            results.append({
                'test_case': test_case['name'],
                'train_error': cal_result['error'],
                'test_error': test_error,
                'params': cal_result['params']
            })

        return results

    def _aggregate_cases(self, cases):
        """Combine multiple case studies into single training set."""
        # Simple concatenation (more sophisticated methods possible)
        all_t = np.concatenate([c['t'] for c in cases])
        all_H = np.hstack([c['H'] for c in cases])
        return {'t': all_t, 'H': all_H}

    def _compute_test_error(self, test_case, params):
        """Compute error on test case with given parameters."""
        for name, val in params.items():
            self.simulator.params[name] = val

        H0 = test_case['H'][:, 0]
        t_obs = test_case['t']

        try:
            t_sim, H_sim, K_sim = self.simulator.simulate(
                H0, (t_obs[0], t_obs[-1]), t_eval=t_obs
            )
            error = np.mean((H_sim - test_case['H']) ** 2)
        except:
            error = 1e10

        return error
```

---

## Model 4: The Intervention Simulator

### Purpose
Simulate counterfactual interventions to estimate what could have prevented collapse.

### Key Questions
1. At what point was collapse still preventable?
2. What intervention magnitude would have been required?
3. What would have been the cost-benefit ratio?

### Implementation

```python
class InterventionSimulator:
    """
    Simulate counterfactual interventions in collapse scenarios.
    """

    def __init__(self, simulator):
        self.simulator = simulator

    def find_intervention_window(self, H0, shock_profile, K_threshold=0.3):
        """
        Find the time window during which intervention could prevent collapse.

        Returns: (earliest_time, latest_time, confidence)
        """

        # Baseline: simulate without intervention
        t_base, H_base, K_base = self._simulate_with_shocks(H0, shock_profile)

        collapse_time = self._find_collapse_time(K_base, K_threshold)
        if collapse_time is None:
            return None  # No collapse to prevent

        # Binary search for earliest intervention point
        intervention_times = np.linspace(0, collapse_time, 20)
        results = []

        for int_time in intervention_times:
            # Simulate with intervention at this time
            success = self._test_intervention(H0, shock_profile, int_time, K_threshold)
            results.append((int_time, success))

        # Find transition point
        earliest = None
        latest = None
        for t, success in results:
            if success and earliest is None:
                earliest = t
            if success:
                latest = t

        return {
            'earliest_effective': earliest,
            'latest_effective': latest,
            'collapse_time': collapse_time,
            'window_duration': latest - earliest if (earliest and latest) else 0
        }

    def estimate_intervention_cost(self, H0, shock_profile, intervention_time,
                                   target_H3_boost=0.1, cost_per_H3_unit=1.0):
        """
        Estimate cost of intervention needed to prevent collapse.

        Returns: dict with intervention magnitude, cost, and benefit
        """

        # Find minimum intervention magnitude needed
        magnitudes = np.linspace(0, 0.3, 30)

        for mag in magnitudes:
            # Apply intervention
            H_int = H0.copy()
            H_int[2] += mag  # Boost H3

            # Simulate
            t, H, K = self._simulate_with_shocks(H_int, shock_profile,
                                                  start_time=intervention_time)

            if K[-1] > 0.4:  # Collapse averted
                cost = mag * cost_per_H3_unit
                benefit = self._compute_benefit(K, intervention_time)

                return {
                    'required_magnitude': mag,
                    'cost': cost,
                    'benefit': benefit,
                    'roi': benefit / cost if cost > 0 else float('inf'),
                    'success': True
                }

        return {
            'required_magnitude': None,
            'cost': None,
            'benefit': None,
            'roi': None,
            'success': False
        }

    def compare_intervention_strategies(self, H0, shock_profile, strategies):
        """
        Compare different intervention strategies.

        strategies: list of dicts with 'name', 'target_harmony', 'magnitude', 'timing'
        """

        results = []

        # Baseline without intervention
        t_base, H_base, K_base = self._simulate_with_shocks(H0, shock_profile)
        baseline_outcome = K_base[-1]

        for strategy in strategies:
            H_int = H0.copy()
            target_idx = strategy['target_harmony'] - 1  # 0-indexed
            H_int[target_idx] += strategy['magnitude']

            t, H, K = self._simulate_with_shocks(
                H_int, shock_profile,
                start_time=strategy['timing']
            )

            results.append({
                'strategy': strategy['name'],
                'final_K': K[-1],
                'improvement': K[-1] - baseline_outcome,
                'min_K': K.min(),
                'avoided_collapse': K.min() > 0.3
            })

        return results

    def _simulate_with_shocks(self, H0, shock_profile, start_time=0):
        """Helper: simulate with shock profile."""
        # Implementation would handle time-varying shocks
        t_span = (start_time, shock_profile.get('end_time', 100))
        return self.simulator.simulate(H0, t_span)

    def _find_collapse_time(self, K, threshold=0.3):
        """Find first time K drops below threshold."""
        below = np.where(K < threshold)[0]
        return below[0] if len(below) > 0 else None

    def _test_intervention(self, H0, shock_profile, int_time, threshold):
        """Test if intervention at given time prevents collapse."""
        # Simplified: boost H3 by standard amount
        H_int = H0.copy()
        H_int[2] += 0.1

        t, H, K = self._simulate_with_shocks(H_int, shock_profile, start_time=int_time)
        return K.min() > threshold

    def _compute_benefit(self, K, intervention_time):
        """Compute economic benefit of avoided collapse."""
        # Simplified: integrate K above collapse threshold
        benefit = np.sum(np.maximum(0, K - 0.3))
        return benefit
```

---

## Model 5: The Recovery Dynamics Analyzer

### Purpose
Model post-collapse recovery dynamics and estimate recovery times.

### Key Insight
Recovery requires rebuilding trust (H₃) from scratch, which is slow due to the Trust Asymmetry Law.

### Implementation

```python
class RecoveryAnalyzer:
    """
    Analyze and model post-collapse recovery dynamics.
    """

    def __init__(self, simulator):
        self.simulator = simulator

    def estimate_recovery_time(self, H_collapsed, H_target,
                                investment_rate=0.01, trust_building_rate=0.02):
        """
        Estimate time needed to recover from collapsed state.

        Uses trust asymmetry: building is 3-10x slower than erosion.
        """

        # Key parameter: trust building coefficient
        k_build = trust_building_rate

        # Model: dH3/dt = k_build * (H_target - H3) for recovery
        # Solution: H3(t) = H_target - (H_target - H3_0) * exp(-k_build * t)

        H3_initial = H_collapsed[2]
        H3_target = H_target[2]

        # Time to reach 95% of target
        if H3_target <= H3_initial:
            return 0

        recovery_time = -np.log(0.05) / k_build * (H3_target - H3_initial)

        return {
            'h3_recovery_time': recovery_time,
            'full_recovery_time': recovery_time * 1.3,  # Other harmonies follow
            'investment_required': recovery_time * investment_rate,
            'trust_asymmetry_factor': 1 / k_build
        }

    def compare_recovery_paths(self, H_collapsed, recovery_strategies):
        """
        Compare different recovery strategies.

        Strategies might focus on:
        - External aid (direct H injection)
        - Institution building (H1 focus)
        - Economic development (H2 focus)
        - Trust building (H3 focus)
        """

        results = []

        for strategy in recovery_strategies:
            recovery_time = self._simulate_recovery(H_collapsed, strategy)

            results.append({
                'strategy': strategy['name'],
                'recovery_time': recovery_time,
                'cost': strategy.get('cost', 0),
                'cost_effectiveness': recovery_time / strategy.get('cost', 1)
            })

        return sorted(results, key=lambda x: x['recovery_time'])

    def analyze_historical_recoveries(self, collapse_cases):
        """
        Analyze recovery times from historical data.

        For each case: collapse duration vs recovery duration
        """

        results = []

        for case in collapse_cases:
            collapse_duration = case['collapse_end'] - case['collapse_start']
            recovery_duration = case['recovery_end'] - case['recovery_start']

            asymmetry_ratio = recovery_duration / collapse_duration

            results.append({
                'case': case['name'],
                'collapse_duration': collapse_duration,
                'recovery_duration': recovery_duration,
                'asymmetry_ratio': asymmetry_ratio,
                'fits_3_10x_prediction': 3 <= asymmetry_ratio <= 10
            })

        return results

    def _simulate_recovery(self, H_collapsed, strategy):
        """Simulate recovery under given strategy."""
        # Placeholder: would integrate with cascade simulator
        base_rate = 0.02
        strategy_boost = strategy.get('efficiency', 1.0)
        effective_rate = base_rate * strategy_boost

        H3_gap = 0.7 - H_collapsed[2]  # Target H3 = 0.7
        recovery_time = H3_gap / effective_rate

        return recovery_time
```

---

## Model 6: The Multi-Case Comparator

### Purpose
Systematically compare collapse dynamics across multiple historical cases.

### Implementation

```python
class MultiCaseComparator:
    """
    Compare collapse dynamics across multiple historical cases.
    """

    def __init__(self, cases):
        """
        cases: list of dicts, each with:
        - name: case name
        - t: time array
        - H: 7 x n harmony array
        - metadata: additional info
        """
        self.cases = cases

    def compare_cascade_sequences(self):
        """
        Compare the order in which harmonies decline across cases.

        Returns the sequence of decline for each case.
        """

        results = []

        for case in self.cases:
            sequence = self._extract_decline_sequence(case)
            results.append({
                'case': case['name'],
                'sequence': sequence,
                'first_to_decline': sequence[0] if sequence else None,
                'last_to_decline': sequence[-1] if sequence else None
            })

        # Aggregate: what's the modal sequence?
        all_sequences = [r['sequence'] for r in results if r['sequence']]
        modal_first = self._find_modal(
            [s[0] for s in all_sequences if s]
        )
        modal_last = self._find_modal(
            [s[-1] for s in all_sequences if s]
        )

        return {
            'individual': results,
            'modal_first': modal_first,
            'modal_last': modal_last,
            'h3_first_count': sum(1 for r in results if r['first_to_decline'] == 'H3'),
            'h7_last_count': sum(1 for r in results if r['last_to_decline'] == 'H7')
        }

    def compare_speed(self):
        """
        Compare collapse speed (peak to nadir) across cases.
        """

        results = []

        for case in self.cases:
            K = self._compute_K(case['H'])
            peak_idx = np.argmax(K)
            nadir_idx = np.argmin(K[peak_idx:]) + peak_idx

            peak_K = K[peak_idx]
            nadir_K = K[nadir_idx]
            duration = case['t'][nadir_idx] - case['t'][peak_idx]
            rate = (peak_K - nadir_K) / duration if duration > 0 else 0

            results.append({
                'case': case['name'],
                'peak_K': peak_K,
                'nadir_K': nadir_K,
                'collapse_duration': duration,
                'decline_rate': rate
            })

        # Test hypothesis: higher peak K → slower collapse
        peak_Ks = [r['peak_K'] for r in results]
        durations = [r['collapse_duration'] for r in results]
        correlation = np.corrcoef(peak_Ks, durations)[0, 1]

        return {
            'individual': results,
            'peak_duration_correlation': correlation,
            'supports_buffer_hypothesis': correlation > 0.3
        }

    def compare_h3_thresholds(self):
        """
        Compare H3 values at the point collapse became irreversible.
        """

        results = []

        for case in self.cases:
            K = self._compute_K(case['H'])
            H3 = case['H'][2, :]  # H3 is index 2

            # Find "point of no return": where K decline accelerates
            inflection = self._find_inflection(K)

            if inflection is not None:
                H3_at_inflection = H3[inflection]
            else:
                H3_at_inflection = None

            results.append({
                'case': case['name'],
                'H3_at_inflection': H3_at_inflection,
                'below_threshold': H3_at_inflection < 0.40 if H3_at_inflection else None
            })

        H3_values = [r['H3_at_inflection'] for r in results if r['H3_at_inflection']]

        return {
            'individual': results,
            'mean_H3_at_inflection': np.mean(H3_values) if H3_values else None,
            'std_H3_at_inflection': np.std(H3_values) if H3_values else None,
            'all_below_040': all(v < 0.40 for v in H3_values) if H3_values else None,
            'supports_threshold_hypothesis': all(0.30 < v < 0.45 for v in H3_values) if H3_values else None
        }

    def _extract_decline_sequence(self, case):
        """Extract order in which harmonies began declining."""
        H = case['H']
        sequences = []

        for i in range(7):
            # Find when this harmony's decline began
            series = H[i, :]
            peak_idx = np.argmax(series)
            if peak_idx < len(series) - 1:
                sequences.append((f'H{i+1}', peak_idx))

        sequences.sort(key=lambda x: x[1])
        return [s[0] for s in sequences]

    def _compute_K(self, H):
        return np.prod(H, axis=0) ** (1/7)

    def _find_modal(self, items):
        from collections import Counter
        if not items:
            return None
        counts = Counter(items)
        return counts.most_common(1)[0][0]

    def _find_inflection(self, K):
        """Find inflection point where decline accelerates."""
        dK = np.gradient(K)
        d2K = np.gradient(dK)

        # Look for point where second derivative is most negative
        inflection = np.argmin(d2K)
        return inflection if d2K[inflection] < -0.01 else None
```

---

## Usage Example: Complete Analysis Pipeline

```python
# Example: Analyze the Bronze Age Collapse

# 1. Load historical data
bronze_age_data = load_bronze_age_harmonies()  # Returns dict with t, H

# 2. Initialize models
simulator = CascadeSimulator()
detector = PhaseTransitionDetector()
calibrator = HistoricalCalibrator(simulator)
intervention_sim = InterventionSimulator(simulator)

# 3. Calibrate model to data
param_bounds = {
    'alpha3': (0.01, 0.1),
    'gamma3': (0.1, 0.5),
    'theta1': (0.3, 0.5)
}
calibration = calibrator.calibrate(bronze_age_data, param_bounds)
print(f"Calibrated parameters: {calibration['params']}")

# 4. Detect early warning signals
H3_series = bronze_age_data['H'][2, :]
ews = detector.analyze(H3_series)
csi = detector.compute_csi(H3_series)
print(f"Peak CSI: {max(csi)}")

# 5. Identify intervention windows
shock_profile = {'magnitude': 0.3, 'end_time': 50}
window = intervention_sim.find_intervention_window(
    bronze_age_data['H'][:, 0],
    shock_profile
)
print(f"Intervention window: {window}")

# 6. Compare intervention strategies
strategies = [
    {'name': 'Trust Building', 'target_harmony': 3, 'magnitude': 0.1, 'timing': 10},
    {'name': 'Economic Aid', 'target_harmony': 2, 'magnitude': 0.1, 'timing': 10},
    {'name': 'Governance Support', 'target_harmony': 1, 'magnitude': 0.1, 'timing': 10}
]
comparison = intervention_sim.compare_intervention_strategies(
    bronze_age_data['H'][:, 0],
    shock_profile,
    strategies
)
print(f"Best strategy: {comparison[0]['strategy']}")
```

---

## Validation Protocol

### Step 1: In-Sample Fit
- Calibrate on each case individually
- Report R² and RMSE for each harmony

### Step 2: Cross-Validation
- Leave-one-out across 4 cases
- Report prediction error on held-out case

### Step 3: Control Case Validation
- Apply calibrated model to control cases
- Verify model correctly predicts non-collapse

### Step 4: Sensitivity Analysis
- Vary each parameter ±20%
- Identify parameters with largest impact

### Step 5: Predictions for Modern Cases
- Apply model to contemporary societies
- Generate CSI scores and collapse probabilities
- Identify intervention opportunities

---

## Computational Requirements

| Model | Complexity | Typical Runtime | Dependencies |
|-------|------------|-----------------|--------------|
| Cascade Simulator | O(n) | <1 sec | NumPy, SciPy |
| Phase Transition Detector | O(n²) | ~5 sec | NumPy, SciPy |
| Historical Calibrator | O(n³) | ~1 min | SciPy (optimization) |
| Intervention Simulator | O(n) | ~10 sec | NumPy, SciPy |
| Multi-Case Comparator | O(mn) | ~5 sec | NumPy |

**Total for full analysis**: ~5 minutes per case study

---

## Future Extensions

1. **Agent-Based Modeling**: Model individual actors making coordination decisions
2. **Spatial Dynamics**: Add geographic diffusion of collapse
3. **Network Analysis**: Model harmony interdependencies as network
4. **Machine Learning**: Use neural networks for pattern recognition
5. **Real-Time Monitoring**: Adapt models for contemporary data streams

---

*"Models are tools for thinking, not oracles for prediction. The goal is insight, not prophecy."*

---

**Document**: Predictive Models for Collapse Analysis
**Version**: 1.0
**Date**: December 2025
**Status**: Implementation Framework for Paper 2

