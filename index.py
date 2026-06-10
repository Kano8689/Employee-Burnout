import os
import io
import traceback
import numpy as np
import pandas as pd
from flask import (Flask, render_template, request,
                   redirect, url_for, flash, send_file, jsonify)

from model import (BurnoutPredictor, PKL_PATH, CSV_PATH,
                   validate_csv, ALL_FEATURES)
from generate_dataset import generate_dataset

app = Flask(__name__)
app.secret_key = 'burnout-secret-2024'
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

predictor = BurnoutPredictor()


def ensure_ready():
    """
    Train the model in-memory on startup.
    Works on Vercel (read-only FS) because we never need to write/load .pkl.
    The dataset CSV is committed to the repo.
    """
    global predictor
    try:
        # Make sure dataset exists (it's committed, but generate as fallback)
        if not validate_csv(CSV_PATH):
            generate_dataset()

        # Train fresh in memory — no pickle loading, no version mismatch
        predictor.train_in_memory(CSV_PATH)
        print("[OK] Model trained in memory and ready.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[ERR] ensure_ready failed: {e}")


FEATURE_DISPLAY = {
    'Mental_Fatigue_Score': 'Mental Fatigue Score',
    'Resource_Allocation':  'Resource Allocation',
    'Designation':          'Designation Level',
    'WFH_Setup_Available':  'WFH Setup',
    'Company_Type':         'Company Type',
    'Gender':               'Gender',
}


def burnout_label(score):
    if score <= 0.30:
        return 'Low Burnout',    '#27ae60', 'Healthy work balance. Keep it up!'
    if score <= 0.60:
        return 'Medium Burnout', '#f39c12', 'Signs of moderate strain detected. Monitor task loads and offer regular breaks.'
    return 'High Burnout',   '#e74c3c', 'High burnout risk! Immediate support and workload reduction recommended.'


def fmt_contributions(contribs):
    out = [{'name': FEATURE_DISPLAY.get(k, k),
            'pct': round(v * 100, 2)} for k, v in contribs.items()]
    out.sort(key=lambda x: x['pct'], reverse=True)
    return out


# ─── Main page (single prediction, matches your UI) ───
@app.route('/', methods=['GET', 'POST'])
def predict_single():
    result = None
    if request.method == 'POST':
        try:
            data = {
                'Gender':               request.form['gender'],
                'Company_Type':         request.form['company_type'],
                'WFH_Setup_Available':  request.form['wfh_setup'],
                'Designation':          int(request.form['designation']),
                'Resource_Allocation':  int(request.form['resource_allocation']),
                'Mental_Fatigue_Score': float(request.form['mental_fatigue']),
            }
            pred, contribs = predictor.predict_single(data)
            level, color, msg = burnout_label(pred)
            result = {
                'prediction': round(pred, 2),
                'level': level,
                'color': color,
                'message': msg,
                'contributions': fmt_contributions(contribs),
                'input': data,
            }
        except Exception as e:
            traceback.print_exc()
            flash(f'Error: {e}', 'danger')

    return render_template('predict_single.html', result=result)


# ─── CSV batch prediction ───
@app.route('/predict/csv', methods=['GET', 'POST'])
def predict_csv():
    if request.method == 'GET':
        return render_template('predict_csv.html')

    f = request.files.get('csv_file')
    if not f or f.filename == '':
        flash('Please select a CSV file.', 'warning')
        return redirect(url_for('predict_csv'))
    if not f.filename.lower().endswith('.csv'):
        flash('Only .csv files allowed.', 'warning')
        return redirect(url_for('predict_csv'))

    try:
        path = os.path.join(UPLOAD_FOLDER, f.filename)
        f.save(path)
        df = pd.read_csv(path)
        if df.empty:
            flash('CSV is empty.', 'warning')
            return redirect(url_for('predict_csv'))

        results = []
        for _, row in df.iterrows():
            try:
                data = {
                    'Gender':               str(row.get('Gender', 'Male')),
                    'Company_Type':         str(row.get('Company_Type', 'Service')),
                    'WFH_Setup_Available':  str(row.get('WFH_Setup_Available', 'Yes')),
                    'Designation':          int(row.get('Designation', 2)),
                    'Resource_Allocation':  int(row.get('Resource_Allocation', 5)),
                    'Mental_Fatigue_Score': float(row.get('Mental_Fatigue_Score', 5)),
                }
                pred, _ = predictor.predict_single(data)
                level, color, _ = burnout_label(pred)
                rd = dict(data)
                rd['Predicted_Burn_Rate'] = round(pred, 2)
                rd['Burnout_Level'] = level
                rd['Color'] = color
                results.append(rd)
            except Exception:
                continue

        if not results:
            flash('No valid rows. Check CSV format.', 'warning')
            return redirect(url_for('predict_csv'))

        preds = [r['Predicted_Burn_Rate'] for r in results]
        summary = {
            'total':  len(results),
            'avg':    round(float(np.mean(preds)), 2),
            'max':    round(float(np.max(preds)), 2),
            'min':    round(float(np.min(preds)), 2),
            'low':    sum(1 for p in preds if p <= 0.30),
            'medium': sum(1 for p in preds if 0.30 < p <= 0.60),
            'high':   sum(1 for p in preds if p > 0.60),
        }

        # ── Top 5 highest-risk employees (computed in Python) ──
        top5 = sorted(results, key=lambda r: r['Predicted_Burn_Rate'], reverse=True)[:5]
        top5_scores = [float(r['Predicted_Burn_Rate']) for r in top5]

        return render_template('csv_results.html',
                               results=results,
                               summary=summary,
                               filename=f.filename,
                               top5=top5,
                               top5_scores=top5_scores)
    except Exception as e:
        traceback.print_exc()
        flash(f'CSV error: {e}', 'danger')
        return redirect(url_for('predict_csv'))

# ─── Model insights ───
@app.route('/model/info')
def model_info():
    try:
        metrics, importance = predictor.get_saved_metrics()
        imp = [{'name': FEATURE_DISPLAY.get(k, k), 'pct': round(v * 100, 2)}
               for k, v in importance.items()]

        df = pd.read_csv(CSV_PATH)
        columns_info = []
        for col in df.columns:
            dtype = str(df[col].dtype)
            friendly = ('Integer' if 'int' in dtype else
                        'Decimal' if 'float' in dtype else
                        'Text' if 'object' in dtype else dtype)
            columns_info.append({'name': col, 'dtype': dtype, 'friendly': friendly})

        ds = {
            'rows': len(df),
            'cols': len(df.columns) - 1,
            'avg':  round(df['Burn_Rate'].mean(), 3),
            'columns_info': columns_info,
        }
        return render_template('model_info.html',
                               metrics=metrics, importance=imp, ds=ds)
    except Exception as e:
        traceback.print_exc()
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('predict_single'))
    

# ─── Sample CSV download ───
@app.route('/download/sample')
def download_sample():
    if validate_csv(CSV_PATH):
        df = pd.read_csv(CSV_PATH).head(20)
        if 'Burn_Rate' in df.columns:
            df = df.drop(columns=['Burn_Rate'])
        buf = io.BytesIO()
        df.to_csv(buf, index=False)
        buf.seek(0)
        return send_file(buf, mimetype='text/csv',
                         as_attachment=True, download_name='sample_input.csv')
    flash('Dataset not ready.', 'warning')
    return redirect(url_for('predict_single'))


# ✅ CORRECT — ensure_ready() runs on BOTH local AND Vercel
ensure_ready()      # <-- moved OUTSIDE the if block (runs on import)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)