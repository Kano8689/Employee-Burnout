import os
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PKL_PATH = os.path.join(BASE_DIR, 'burnout_model.pkl')
CSV_PATH = os.path.join(BASE_DIR, 'burnout_dataset.csv')
ENC_PATH = os.path.join(BASE_DIR, 'encoders.json')
SCL_PATH = os.path.join(BASE_DIR, 'scaler.json')

CAT_COLS = ['Gender', 'Company_Type', 'WFH_Setup_Available']
NUM_COLS = ['Designation', 'Resource_Allocation', 'Mental_Fatigue_Score']
ALL_FEATURES = CAT_COLS + NUM_COLS
TARGET = 'Burn_Rate'


def validate_csv(path):
    """Check CSV exists & has required columns."""
    if not os.path.exists(path):
        return False
    try:
        df = pd.read_csv(path)
        if df.empty:
            return False
        required = set(ALL_FEATURES + [TARGET])
        return required.issubset(set(df.columns))
    except Exception:
        return False


class BurnoutPredictor:
    def __init__(self):
        self.model = None
        self.encoders = {}
        self.scaler = StandardScaler()

    # ── encode categoricals ──
    def _encode(self, df, fit=False):
        df = df.copy()
        for col in CAT_COLS:
            if col not in df.columns:
                continue
            if fit:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.encoders[col] = le
            else:
                if col in self.encoders:
                    le = self.encoders[col]
                    df[col] = df[col].astype(str).apply(
                        lambda x: x if x in le.classes_ else le.classes_[0]
                    )
                    df[col] = le.transform(df[col].astype(str))
                else:
                    df[col] = 0
        return df

    # ── scale numerics ──
    def _scale(self, df, fit=False):
        present = [c for c in NUM_COLS if c in df.columns]
        if not present:
            return df
        if fit:
            df[present] = self.scaler.fit_transform(df[present].values.astype(float))
        else:
            df[present] = self.scaler.transform(df[present].values.astype(float))
        return df

    # ── prepare ──
    def _prepare(self, df, fit=True):
        df = df.copy()
        df = df.drop(columns=['Employee_ID'], errors='ignore')
        y = df.pop(TARGET) if TARGET in df.columns else None
        df = self._encode(df, fit)
        df = self._scale(df, fit)
        df = df[ALL_FEATURES]            # enforce column order
        return df, y

    # ── train ──
    def train(self, csv_path=None):
        if csv_path is None:
            csv_path = CSV_PATH

        df = pd.read_csv(csv_path)
        X, y = self._prepare(df, fit=True)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )

        self.model = RandomForestRegressor(
            n_estimators=200, max_depth=12,
            min_samples_split=5, min_samples_leaf=2,
            random_state=42, n_jobs=-1
        )
        self.model.fit(X_train, y_train)

        y_pred = np.clip(self.model.predict(X_test), 0, 1)
        metrics = {
            'r2':         round(r2_score(y_test, y_pred), 4),
            'rmse':       round(float(np.sqrt(mean_squared_error(y_test, y_pred))), 4),
            'mae':        round(float(mean_absolute_error(y_test, y_pred)), 4),
            'train_rows': len(X_train),
            'test_rows':  len(X_test),
            'total_rows': len(df),
            'n_features': X.shape[1],
        }

        importance = {}
        for i, fn in enumerate(ALL_FEATURES):
            importance[fn] = round(float(self.model.feature_importances_[i]), 4)
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

        self.save()
        print(f"[OK] Trained. R2={metrics['r2']} RMSE={metrics['rmse']}")
        return metrics, importance

    # ── predict ──
    def predict_single(self, data):
        if self.model is None:
            raise RuntimeError("Model not trained!")
        df = pd.DataFrame([data])
        X, _ = self._prepare(df, fit=False)
        pred = float(np.clip(self.model.predict(X)[0], 0, 1))

        contributions = {}
        for i, fn in enumerate(ALL_FEATURES):
            contributions[fn] = round(float(self.model.feature_importances_[i]), 4)
        return pred, contributions

    # ── save ──
    def save(self):
        with open(PKL_PATH, 'wb') as f:
            pickle.dump(self.model, f)

        enc = {col: le.classes_.tolist() for col, le in self.encoders.items()}
        with open(ENC_PATH, 'w') as f:
            json.dump(enc, f)

        scl = {
            'mean':  self.scaler.mean_.tolist(),
            'scale': self.scaler.scale_.tolist(),
            'var':   self.scaler.var_.tolist(),
            'n_in':  int(self.scaler.n_features_in_),
        }
        with open(SCL_PATH, 'w') as f:
            json.dump(scl, f)
        print("[OK] Model + encoders + scaler saved.")

    # ── load ──
    def load(self):
        try:
            with open(PKL_PATH, 'rb') as f:
                self.model = pickle.load(f)

            if os.path.exists(ENC_PATH):
                with open(ENC_PATH) as f:
                    enc = json.load(f)
                self.encoders = {}
                for col, classes in enc.items():
                    le = LabelEncoder()
                    le.classes_ = np.array(classes)
                    self.encoders[col] = le

            if os.path.exists(SCL_PATH):
                with open(SCL_PATH) as f:
                    s = json.load(f)
                self.scaler = StandardScaler()
                self.scaler.mean_ = np.array(s['mean'])
                self.scaler.scale_ = np.array(s['scale'])
                self.scaler.var_ = np.array(s['var'])
                self.scaler.n_features_in_ = s['n_in']

            print("[OK] Model loaded.")
            return True
        except Exception as e:
            print(f"[ERR] Load failed: {e}")
            return False