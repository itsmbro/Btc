import pandas as pd
import lightgbm as lgb
import optuna
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np


def optimize_lgbm(X, y):
    """Ottimizza i parametri di LightGBM usando Optuna."""
    
    def objective(trial):
        params = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'num_leaves': trial.suggest_int('num_leaves', 20, 150),
            'max_depth': trial.suggest_int('max_depth', 3, 12),
            'min_child_samples': trial.suggest_int('min_child_samples', 5, 50),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        }
        
        model = lgb.LGBMRegressor(**params)
        tscv = TimeSeriesSplit(n_splits=5)
        score = cross_val_score(model, X, y, cv=tscv, scoring='neg_root_mean_squared_error').mean()
        return -score

    study = optuna.create_study(direction='minimize')
    study.optimize(objective, n_trials=50)

    return study.best_params


def predict_with_lightgbm(df, days=7):
    """Prevede i prezzi futuri usando LightGBM con iperparametri ottimizzati."""
    
    # Prepara i dati
    df = df.dropna()
    X = df.drop('Close', axis=1)  # Features
    y = df['Close']               # Target

    # Ottimizza i parametri
    best_params = optimize_lgbm(X, y)

    # Addestra il modello
    model = lgb.LGBMRegressor(**best_params)
    model.fit(X, y)

    # Crea dati futuri (ipotizziamo che rimangano costanti le feature)
    future_dates = pd.date_range(start=df.index[-1], periods=days+1, freq='B')[1:]
    future_data = np.tile(X.iloc[-1].values, (days, 1))  # Copia l'ultima riga per simulare

    # Previsione
    forecast = model.predict(future_data)
    forecast_df = pd.DataFrame({'Date': future_dates, 'Predicted Close': forecast})

    return forecast_df
