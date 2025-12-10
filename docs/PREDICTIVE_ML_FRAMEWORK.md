# Predictive K-Index: Machine Learning Framework

**Forecasting Coordination Futures with AI**

**Version**: 1.0.0
**Created**: December 10, 2025
**Status**: Technical Specification - Ready for Implementation

---

## Executive Summary

The K-Index provides 210 years of historical coordination data. Machine learning can transform this retrospective measure into a **predictive instrument**, forecasting coordination trajectories, crisis risks, and intervention impacts.

**Goal**: Build an AI system that can:
1. Forecast K-Index 1-10 years ahead
2. Predict coordination crises before they occur
3. Estimate intervention effectiveness
4. Identify early warning signals in real-time data

---

## 1. Problem Formulation

### 1.1 Prediction Tasks

```
┌─────────────────────────────────────────────────────────────────┐
│              PREDICTION TASK HIERARCHY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   LEVEL 1: K-INDEX FORECASTING                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ Task: Predict K(t+h) given K(t), K(t-1), ..., features  │  │
│   │ Horizon: h = 1, 3, 5, 10 years                          │  │
│   │ Output: Point forecast + confidence interval            │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   LEVEL 2: CRISIS PREDICTION                                    │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ Task: P(crisis within h years | current state)          │  │
│   │ Definition: Crisis = K drops below θ or drops >20%      │  │
│   │ Output: Probability + risk factors                      │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   LEVEL 3: HARMONY DYNAMICS                                     │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ Task: Predict individual H₁-H₇ trajectories             │  │
│   │ Insight: Which harmony will change most?                │  │
│   │ Output: Per-harmony forecasts + correlations            │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   LEVEL 4: INTERVENTION IMPACT                                  │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ Task: E[ΔK | intervention I, context C]                 │  │
│   │ Counterfactual: What would K be with/without action?    │  │
│   │ Output: Expected impact + uncertainty                   │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Data Structure

**Historical Dataset**:
- 190+ countries × 210 years = 40,000+ country-year observations
- 7 harmonies × 40,000 = 280,000+ harmony observations
- 50+ underlying indicators × 40,000 = 2,000,000+ indicator observations

**Feature Categories**:

| Category | Features | Examples |
|----------|----------|----------|
| **Lagged K** | K(t), K(t-1), ..., K(t-10) | Historical trajectory |
| **Harmonies** | H₁-H₇ at time t | Current profile |
| **Harmony Dynamics** | ΔH₁, ΔH₂, ... | Rate of change |
| **Structural** | GDP, population, geography | Country characteristics |
| **Network** | Trade partners' K, neighbor K | Contagion exposure |
| **Events** | Wars, treaties, elections | Shock indicators |
| **Global** | World average K, year | Context |

---

## 2. Model Architecture

### 2.1 Baseline Models

**Model 1: ARIMA for K-Index Time Series**
```python
from statsmodels.tsa.arima.model import ARIMA

class KIndexARIMA:
    """
    Autoregressive baseline for K-Index forecasting.
    Simple but interpretable.
    """

    def __init__(self, order=(2, 1, 1)):
        self.order = order
        self.models = {}

    def fit(self, country_data: pd.DataFrame):
        """Fit ARIMA model for each country."""
        for country in country_data['country'].unique():
            series = country_data[country_data['country'] == country]['k_index']
            self.models[country] = ARIMA(series, order=self.order).fit()

    def forecast(self, country: str, horizon: int) -> np.ndarray:
        """Forecast K-Index for country h steps ahead."""
        return self.models[country].forecast(steps=horizon)
```

**Model 2: Gradient Boosting with Features**
```python
import xgboost as xgb

class KIndexGBM:
    """
    Gradient boosting with rich feature set.
    Better performance, moderate interpretability.
    """

    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=500,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8
        )

    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Create feature matrix from raw data."""
        features = pd.DataFrame()

        # Lagged K values
        for lag in range(1, 11):
            features[f'k_lag_{lag}'] = data.groupby('country')['k_index'].shift(lag)

        # Harmony values
        for h in range(1, 8):
            features[f'h{h}'] = data[f'h{h}']
            features[f'h{h}_change'] = data.groupby('country')[f'h{h}'].diff()

        # Structural features
        features['gdp_per_capita'] = data['gdp_pc']
        features['population_log'] = np.log(data['population'])

        # Network features
        features['neighbor_k_mean'] = data['neighbor_k_mean']
        features['trade_partner_k'] = data['trade_partner_k']

        return features

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Train the model."""
        self.model.fit(X, y)

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict K-Index."""
        return self.model.predict(X)

    def feature_importance(self) -> pd.Series:
        """Get feature importances."""
        return pd.Series(
            self.model.feature_importances_,
            index=self.feature_names
        ).sort_values(ascending=False)
```

### 2.2 Deep Learning Models

**Model 3: LSTM for Sequential Patterns**
```python
import torch
import torch.nn as nn

class KIndexLSTM(nn.Module):
    """
    LSTM for capturing long-term dependencies in K-Index.
    Handles sequential nature of coordination dynamics.
    """

    def __init__(self, input_dim: int, hidden_dim: int = 64, num_layers: int = 2):
        super().__init__()

        self.lstm = nn.LSTM(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=0.2
        )

        self.fc = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(32, 1)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, features) tensor

        Returns:
            (batch, 1) predictions
        """
        lstm_out, _ = self.lstm(x)
        last_hidden = lstm_out[:, -1, :]  # Take last timestep
        return self.fc(last_hidden)
```

**Model 4: Transformer for Global Patterns**
```python
class KIndexTransformer(nn.Module):
    """
    Transformer model for K-Index prediction.
    Can attend to relevant historical periods.
    """

    def __init__(
        self,
        input_dim: int,
        d_model: int = 64,
        nhead: int = 4,
        num_layers: int = 2
    ):
        super().__init__()

        self.input_projection = nn.Linear(input_dim, d_model)
        self.pos_encoding = PositionalEncoding(d_model)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=d_model * 4,
            dropout=0.1
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers)

        self.output_head = nn.Linear(d_model, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Args:
            x: (batch, seq_len, features)

        Returns:
            (batch, 1) predictions
        """
        x = self.input_projection(x)
        x = self.pos_encoding(x)
        x = self.transformer(x)
        return self.output_head(x[:, -1, :])
```

### 2.3 Graph Neural Network for Network Effects

```python
import torch_geometric as pyg
from torch_geometric.nn import GCNConv, global_mean_pool

class KIndexGNN(nn.Module):
    """
    Graph Neural Network for modeling coordination contagion.
    Countries as nodes, relationships as edges.
    """

    def __init__(self, node_features: int, hidden_dim: int = 64):
        super().__init__()

        # Graph convolution layers
        self.conv1 = GCNConv(node_features, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, hidden_dim)

        # Per-node prediction head
        self.node_predictor = nn.Sequential(
            nn.Linear(hidden_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, data: pyg.data.Data) -> torch.Tensor:
        """
        Args:
            data: PyG Data object with x, edge_index, edge_weight

        Returns:
            (num_nodes, 1) K-Index predictions
        """
        x, edge_index, edge_weight = data.x, data.edge_index, data.edge_attr

        # Message passing
        x = F.relu(self.conv1(x, edge_index, edge_weight))
        x = F.dropout(x, p=0.2, training=self.training)
        x = F.relu(self.conv2(x, edge_index, edge_weight))
        x = F.dropout(x, p=0.2, training=self.training)
        x = self.conv3(x, edge_index, edge_weight)

        # Node-level predictions
        return self.node_predictor(x)
```

---

## 3. Training Pipeline

### 3.1 Data Preparation

```python
class KIndexDataPipeline:
    """
    End-to-end data pipeline for K-Index prediction.
    """

    def __init__(self, config: dict):
        self.config = config
        self.scalers = {}

    def load_data(self) -> pd.DataFrame:
        """Load and merge all data sources."""
        # Historical K-Index
        k_data = pd.read_csv('data/processed/k_index_historical.csv')

        # Structural indicators
        structural = pd.read_csv('data/raw/world_bank_indicators.csv')

        # Network data
        trade = pd.read_csv('data/raw/bilateral_trade.csv')

        # Merge all
        data = k_data.merge(structural, on=['country', 'year'])
        data = self._add_network_features(data, trade)

        return data

    def create_sequences(
        self,
        data: pd.DataFrame,
        seq_length: int = 10,
        horizon: int = 1
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create sequences for time series models.

        Returns:
            X: (samples, seq_length, features)
            y: (samples, 1)
        """
        sequences = []
        targets = []

        for country in data['country'].unique():
            country_data = data[data['country'] == country].sort_values('year')

            for i in range(len(country_data) - seq_length - horizon + 1):
                seq = country_data.iloc[i:i+seq_length][self.feature_cols].values
                target = country_data.iloc[i+seq_length+horizon-1]['k_index']

                sequences.append(seq)
                targets.append(target)

        return np.array(sequences), np.array(targets)

    def train_test_split(
        self,
        data: pd.DataFrame,
        test_years: int = 20
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Temporal split: train on past, test on recent.
        """
        max_year = data['year'].max()
        train = data[data['year'] <= max_year - test_years]
        test = data[data['year'] > max_year - test_years]
        return train, test
```

### 3.2 Training Configuration

```python
training_config = {
    'model': {
        'type': 'transformer',  # arima, gbm, lstm, transformer, gnn
        'params': {
            'd_model': 64,
            'nhead': 4,
            'num_layers': 2
        }
    },
    'data': {
        'sequence_length': 10,
        'forecast_horizon': 5,
        'features': ['k_lag', 'harmonies', 'structural', 'network'],
        'train_test_split_year': 2000
    },
    'training': {
        'epochs': 100,
        'batch_size': 64,
        'learning_rate': 1e-3,
        'early_stopping_patience': 10,
        'weight_decay': 1e-5
    },
    'evaluation': {
        'metrics': ['mae', 'rmse', 'r2', 'directional_accuracy'],
        'bootstrap_samples': 1000
    }
}
```

### 3.3 Uncertainty Quantification

```python
class UncertaintyEstimator:
    """
    Provide prediction intervals, not just point estimates.
    """

    def __init__(self, base_model, method: str = 'ensemble'):
        self.base_model = base_model
        self.method = method

    def predict_with_uncertainty(
        self,
        X: np.ndarray,
        confidence: float = 0.95
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Returns:
            predictions: Point estimates
            lower: Lower bound of CI
            upper: Upper bound of CI
        """
        if self.method == 'ensemble':
            return self._ensemble_uncertainty(X, confidence)
        elif self.method == 'dropout':
            return self._dropout_uncertainty(X, confidence)
        elif self.method == 'quantile':
            return self._quantile_uncertainty(X, confidence)

    def _ensemble_uncertainty(
        self,
        X: np.ndarray,
        confidence: float
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Use ensemble of models for uncertainty.
        """
        predictions = []
        for model in self.ensemble_models:
            predictions.append(model.predict(X))

        predictions = np.array(predictions)
        mean_pred = predictions.mean(axis=0)

        alpha = (1 - confidence) / 2
        lower = np.percentile(predictions, 100 * alpha, axis=0)
        upper = np.percentile(predictions, 100 * (1 - alpha), axis=0)

        return mean_pred, lower, upper
```

---

## 4. Crisis Prediction System

### 4.1 Crisis Definition

```python
class CrisisDefinition:
    """
    Define what constitutes a coordination crisis.
    """

    CRISIS_TYPES = {
        'threshold_breach': {
            'condition': lambda k: k < 0.382,
            'severity': 'critical'
        },
        'rapid_decline': {
            'condition': lambda k_prev, k_curr: (k_prev - k_curr) / k_prev > 0.15,
            'severity': 'severe'
        },
        'harmony_collapse': {
            'condition': lambda harmonies: min(harmonies.values()) < 0.25,
            'severity': 'moderate'
        },
        'trust_erosion': {
            'condition': lambda h3_trajectory: h3_trajectory < -0.05,
            'severity': 'warning'
        }
    }

    @classmethod
    def identify_crises(cls, data: pd.DataFrame) -> pd.DataFrame:
        """Identify historical crises in data."""
        crises = []

        for _, row in data.iterrows():
            for crisis_type, definition in cls.CRISIS_TYPES.items():
                if cls._check_condition(row, definition['condition']):
                    crises.append({
                        'country': row['country'],
                        'year': row['year'],
                        'type': crisis_type,
                        'severity': definition['severity'],
                        'k_index': row['k_index']
                    })

        return pd.DataFrame(crises)
```

### 4.2 Crisis Prediction Model

```python
class CrisisPredictionModel:
    """
    Predict probability of crisis within horizon.
    """

    def __init__(self, horizon: int = 5):
        self.horizon = horizon
        self.model = xgb.XGBClassifier(
            n_estimators=300,
            max_depth=5,
            scale_pos_weight=10  # Handle class imbalance
        )

    def prepare_labels(self, data: pd.DataFrame) -> pd.Series:
        """
        Create binary labels: 1 if crisis within horizon, 0 otherwise.
        """
        crises = CrisisDefinition.identify_crises(data)
        labels = pd.Series(0, index=data.index)

        for _, crisis in crises.iterrows():
            # Mark years leading up to crisis
            mask = (
                (data['country'] == crisis['country']) &
                (data['year'] >= crisis['year'] - self.horizon) &
                (data['year'] < crisis['year'])
            )
            labels.loc[mask] = 1

        return labels

    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Train crisis prediction model."""
        self.model.fit(X, y)

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict crisis probability."""
        return self.model.predict_proba(X)[:, 1]

    def get_risk_factors(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Explain which features drive crisis risk.
        """
        import shap

        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(X)

        return pd.DataFrame({
            'feature': X.columns,
            'importance': np.abs(shap_values).mean(axis=0)
        }).sort_values('importance', ascending=False)
```

### 4.3 Early Warning System

```python
class EarlyWarningSystem:
    """
    Real-time monitoring and alerting for coordination risks.
    """

    def __init__(self, crisis_model: CrisisPredictionModel):
        self.crisis_model = crisis_model
        self.alert_thresholds = {
            'critical': 0.8,
            'high': 0.6,
            'elevated': 0.4,
            'moderate': 0.2
        }

    def assess_country(self, country_features: pd.DataFrame) -> dict:
        """
        Generate risk assessment for a country.
        """
        crisis_prob = self.crisis_model.predict_proba(country_features)[0]
        risk_factors = self.crisis_model.get_risk_factors(country_features)

        # Determine alert level
        alert_level = 'low'
        for level, threshold in self.alert_thresholds.items():
            if crisis_prob >= threshold:
                alert_level = level
                break

        return {
            'crisis_probability': crisis_prob,
            'alert_level': alert_level,
            'top_risk_factors': risk_factors.head(5).to_dict('records'),
            'recommendations': self._generate_recommendations(risk_factors)
        }

    def generate_global_report(self, all_features: pd.DataFrame) -> pd.DataFrame:
        """
        Generate risk assessment for all countries.
        """
        results = []

        for country in all_features['country'].unique():
            country_data = all_features[all_features['country'] == country]
            assessment = self.assess_country(country_data)
            assessment['country'] = country
            results.append(assessment)

        return pd.DataFrame(results).sort_values(
            'crisis_probability', ascending=False
        )
```

---

## 5. Intervention Impact Estimation

### 5.1 Causal Framework

```python
class InterventionImpactEstimator:
    """
    Estimate causal effect of coordination interventions.
    Uses potential outcomes framework.
    """

    def __init__(self):
        self.outcome_model = None
        self.propensity_model = None

    def estimate_ate(
        self,
        data: pd.DataFrame,
        treatment_col: str,
        outcome_col: str = 'k_index_change'
    ) -> dict:
        """
        Estimate Average Treatment Effect using doubly robust estimation.
        """
        # Fit propensity model
        self.propensity_model = LogisticRegression()
        self.propensity_model.fit(
            data[self.confounders],
            data[treatment_col]
        )
        propensity = self.propensity_model.predict_proba(
            data[self.confounders]
        )[:, 1]

        # Fit outcome model
        self.outcome_model = xgb.XGBRegressor()
        self.outcome_model.fit(
            data[self.confounders + [treatment_col]],
            data[outcome_col]
        )

        # AIPW estimator
        treated = data[treatment_col] == 1
        y = data[outcome_col]

        # Predicted outcomes
        y1_pred = self.outcome_model.predict(
            data[self.confounders].assign(**{treatment_col: 1})
        )
        y0_pred = self.outcome_model.predict(
            data[self.confounders].assign(**{treatment_col: 0})
        )

        # Doubly robust estimate
        ate = (
            (treated * (y - y1_pred) / propensity + y1_pred).mean() -
            ((1 - treated) * (y - y0_pred) / (1 - propensity) + y0_pred).mean()
        )

        return {
            'ate': ate,
            'ate_se': self._bootstrap_se(data, treatment_col, outcome_col),
            'sample_size': len(data)
        }

    def simulate_intervention(
        self,
        country: str,
        intervention_type: str,
        intensity: float
    ) -> dict:
        """
        Simulate effect of hypothetical intervention.
        """
        # Get current features
        current = self._get_current_features(country)

        # Modify features based on intervention
        counterfactual = self._apply_intervention(
            current, intervention_type, intensity
        )

        # Predict outcomes
        baseline_k = self.outcome_model.predict(current)
        intervention_k = self.outcome_model.predict(counterfactual)

        return {
            'country': country,
            'intervention': intervention_type,
            'intensity': intensity,
            'baseline_k_forecast': baseline_k,
            'intervention_k_forecast': intervention_k,
            'expected_impact': intervention_k - baseline_k
        }
```

### 5.2 Scenario Analysis

```python
class ScenarioAnalyzer:
    """
    Analyze different intervention scenarios.
    """

    INTERVENTION_CATALOG = {
        'trust_building': {
            'target_harmony': 'H3',
            'mechanism': 'Social capital programs',
            'typical_effect': 0.05,  # 5% increase in H3
            'time_to_effect': 3  # years
        },
        'institutional_reform': {
            'target_harmony': 'H1',
            'mechanism': 'Governance reforms',
            'typical_effect': 0.08,
            'time_to_effect': 5
        },
        'education_investment': {
            'target_harmony': 'H5',
            'mechanism': 'Education spending',
            'typical_effect': 0.06,
            'time_to_effect': 10
        },
        'infrastructure': {
            'target_harmony': 'H2',
            'mechanism': 'Connectivity investment',
            'typical_effect': 0.10,
            'time_to_effect': 3
        }
    }

    def run_scenario(
        self,
        country: str,
        interventions: List[str],
        horizon: int = 10
    ) -> pd.DataFrame:
        """
        Run multi-year scenario with interventions.
        """
        results = []

        # Baseline (no intervention)
        baseline = self._project_baseline(country, horizon)
        results.append({'scenario': 'baseline', **baseline})

        # With interventions
        for intervention in interventions:
            with_intervention = self._project_with_intervention(
                country, intervention, horizon
            )
            results.append({
                'scenario': intervention,
                **with_intervention
            })

        # Combined scenario
        combined = self._project_combined(country, interventions, horizon)
        results.append({'scenario': 'combined', **combined})

        return pd.DataFrame(results)
```

---

## 6. Real-Time Integration

### 6.1 Real-Time Proxy Indicators

```python
class RealTimeProxies:
    """
    Use high-frequency data to estimate current K-Index.
    """

    PROXY_SOURCES = {
        'H1_governance': [
            'World Bank governance surveys',
            'Political stability indices',
            'Corruption perception updates'
        ],
        'H2_interconnection': [
            'Trade flow data (monthly)',
            'Flight connectivity',
            'Internet traffic patterns'
        ],
        'H3_trust': [
            'Social media sentiment',
            'Survey data (Gallup)',
            'Market volatility (trust proxy)'
        ],
        'H5_knowledge': [
            'Patent applications',
            'Research output',
            'Education enrollment'
        ],
        'H7_technology': [
            'Tech adoption metrics',
            'Infrastructure spending',
            'Digital connectivity'
        ]
    }

    def estimate_current_k(self, country: str) -> dict:
        """
        Estimate current K-Index using real-time proxies.
        """
        proxy_values = {}

        for harmony, sources in self.PROXY_SOURCES.items():
            proxy_values[harmony] = self._aggregate_proxies(country, sources)

        # Use proxy model to estimate K
        k_estimate = self.proxy_model.predict(proxy_values)

        return {
            'country': country,
            'estimated_k': k_estimate,
            'proxy_values': proxy_values,
            'confidence': self._estimate_confidence(proxy_values),
            'last_updated': datetime.now()
        }
```

### 6.2 API for Live Predictions

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="K-Index Prediction API")

class PredictionRequest(BaseModel):
    country: str
    horizon: int = 5
    include_uncertainty: bool = True

class PredictionResponse(BaseModel):
    country: str
    forecast: float
    lower_bound: float
    upper_bound: float
    crisis_probability: float
    alert_level: str
    top_risk_factors: List[dict]

@app.post("/predict", response_model=PredictionResponse)
async def predict_k_index(request: PredictionRequest):
    """
    Generate K-Index forecast for a country.
    """
    features = feature_pipeline.get_features(request.country)

    forecast, lower, upper = model.predict_with_uncertainty(
        features, horizon=request.horizon
    )

    crisis_prob = crisis_model.predict_proba(features)[0]
    alert_level = early_warning.get_alert_level(crisis_prob)
    risk_factors = crisis_model.get_risk_factors(features).head(5)

    return PredictionResponse(
        country=request.country,
        forecast=forecast,
        lower_bound=lower,
        upper_bound=upper,
        crisis_probability=crisis_prob,
        alert_level=alert_level,
        top_risk_factors=risk_factors.to_dict('records')
    )
```

---

## 7. Validation Framework

### 7.1 Backtesting Protocol

```python
class BacktestingFramework:
    """
    Rigorous out-of-sample testing for predictions.
    """

    def expanding_window_backtest(
        self,
        model,
        data: pd.DataFrame,
        start_year: int = 1950,
        horizon: int = 5
    ) -> pd.DataFrame:
        """
        Test predictions with expanding training window.
        """
        results = []

        for test_year in range(start_year + 20, data['year'].max() - horizon):
            # Train on all data up to test_year
            train = data[data['year'] <= test_year]
            test = data[data['year'] == test_year + horizon]

            model.fit(train)
            predictions = model.predict(test)

            results.append({
                'test_year': test_year,
                'horizon': horizon,
                'predictions': predictions,
                'actuals': test['k_index'].values,
                'mae': np.abs(predictions - test['k_index'].values).mean(),
                'rmse': np.sqrt(((predictions - test['k_index'].values) ** 2).mean())
            })

        return pd.DataFrame(results)
```

### 7.2 Evaluation Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| MAE | Mean Absolute Error | < 0.05 |
| RMSE | Root Mean Squared Error | < 0.07 |
| R² | Coefficient of determination | > 0.6 |
| Directional Accuracy | % correct direction | > 70% |
| Crisis Recall | True positive rate for crises | > 80% |
| Crisis Precision | Precision for crisis predictions | > 50% |
| Coverage | % actual in prediction interval | ~95% |

---

## 8. Model Governance

### 8.1 Responsible AI Principles

```
┌─────────────────────────────────────────────────────────────────┐
│              RESPONSIBLE PREDICTION PRINCIPLES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. TRANSPARENCY                                               │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Full methodology published                             │  │
│   │ • Model weights and code open source                     │  │
│   │ • Feature importance always provided                     │  │
│   │ • Uncertainty quantified and communicated                │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   2. ACCOUNTABILITY                                             │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Clear ownership of predictions                         │  │
│   │ • Regular model audits                                   │  │
│   │ • Post-hoc accuracy reporting                            │  │
│   │ • Stakeholder feedback mechanisms                        │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   3. FAIRNESS                                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Equal accuracy across regions                          │  │
│   │ • No systematic bias against country types               │  │
│   │ • Regular bias audits                                    │  │
│   │ • Diverse validation datasets                            │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
│   4. HUMILITY                                                   │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │ • Models are tools, not oracles                          │  │
│   │ • Predictions are probabilistic, not certain             │  │
│   │ • Human judgment essential for interpretation            │  │
│   │ • Regular acknowledgment of limitations                  │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Months 1-3)
- [ ] Prepare comprehensive training dataset
- [ ] Implement baseline models (ARIMA, GBM)
- [ ] Set up backtesting framework
- [ ] Initial validation

### Phase 2: Advanced Models (Months 4-6)
- [ ] Implement deep learning models (LSTM, Transformer)
- [ ] Implement GNN for network effects
- [ ] Ensemble methods
- [ ] Uncertainty quantification

### Phase 3: Crisis Prediction (Months 7-9)
- [ ] Define crisis taxonomy
- [ ] Train crisis prediction models
- [ ] Build early warning system
- [ ] Validation against historical crises

### Phase 4: Deployment (Months 10-12)
- [ ] Build prediction API
- [ ] Real-time proxy integration
- [ ] Dashboard integration
- [ ] Documentation and governance

---

## Conclusion

Machine learning transforms the K-Index from a historical measure into a **predictive instrument**. By forecasting coordination trajectories and crisis risks, we enable proactive intervention rather than reactive response.

**The goal is not to replace human judgment but to augment it**—giving policymakers, researchers, and practitioners advance warning of coordination challenges and evidence for intervention effectiveness.

*"Prediction is not prophecy. It is a tool for better decisions today."*

**Last Updated**: December 10, 2025
