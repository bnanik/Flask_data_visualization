import pandas as pd
import numpy as np
from application import app
from flask import render_template, flash, redirect, url_for, get_flashed_messages, request
from application.form import UserInputForm
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import json

data = []
df = pd.DataFrame

@app.route('/')
def index():  # put application's code here
    return render_template('index.html', title='index')

# ALLOWED_EXTENSIONS = set(['csv'])
# def allowed_file(filename):
#     return '.' in filename and \
#             filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global df
    form = UserInputForm()
    if request.method == 'POST':
        file = request.files['file']
        # if file and allowed_file(file.filename):
        #    filename = secure_filename(file.filename)
        #    new_filename = f'{filename.split(".")[0]}_{str(datetime.now())}.csv'
        #    file.save(os.path.join('input', new_filename))

        df = pd.read_csv(file)
        df['newdate'] = pd.to_datetime(df['Date'])
        df.sort_values(by='newdate', inplace=True)
        df['year'] = df['newdate'].dt.year
        df['quarter'] = df['newdate'].dt.quarter
        df['month'] = df['newdate'].dt.month_name(locale='English')
        flash("Uploaded Successfully!", 'success')
        return render_template('upload.html', shape=df.shape, form=form, data=df.to_html())
        # print(df)
        # return 'uploaded Successfully'
    return render_template('upload.html', title='Upload', form=form)
@app.route('/add', methods=['GET', 'POST'])
def add_data():
    global data
    form = UserInputForm()
    if form.validate_on_submit():
        battery_type = form.battery_type.data
        run_name = form.run_name.data
        product_id = form.product_id.data
        date = form.date.data
        units_produced = form.units_produced.data
        average_performance = form.average_performance.data
        data.append([product_id, battery_type, run_name, date, units_produced, average_performance])
        flash("Successful entry", 'success')
        return redirect(url_for('add_data'))
    return render_template('add.html', title='add', form=form)

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

@app.route("/dashboard")
def dashboard():
    global df
    battery_types = df['Battery Type'].value_counts()
    return render_template("dashboard.html",
                           battery_labels=json.dumps(list(battery_types.keys()), cls=NpEncoder),
                           battery_values=json.dumps(list(battery_types.values), cls=NpEncoder),
                           date_labels=json.dumps(list(df['Date']), cls=NpEncoder),
                           performance_values=json.dumps(list(df['Average Performance']), cls=NpEncoder),
                           units_values=json.dumps(list(df['Units Produced']), cls=NpEncoder),
                           run_labels=json.dumps(df.groupby(['Run Name'])['Average Performance'].mean().keys().tolist(), cls=NpEncoder),
                           run_values=json.dumps(df.groupby(['Run Name'])['Average Performance'].mean().values.tolist(), cls=NpEncoder),
                           year_date_labels=json.dumps(df.groupby(['year'])['Average Performance'].mean().keys().tolist(), cls=NpEncoder),
                           year_performance_values=json.dumps(df.groupby(['year'])['Average Performance'].mean().values.tolist(), cls=NpEncoder),
                           year_units_values=json.dumps(df.groupby(['year'])['Units Produced'].sum().values.tolist(), cls=NpEncoder),
                           quarter_date_labels=json.dumps(df.groupby(['year', 'quarter'])['Average Performance'].mean().keys().tolist(), cls=NpEncoder),
                           quarter_performance_values=json.dumps(df.groupby(['year', 'quarter'])['Average Performance'].mean().values.tolist(), cls=NpEncoder),
                           quarter_units_values=json.dumps(df.groupby(['year', 'quarter'])['Units Produced'].sum().values.tolist(), cls=NpEncoder),
                           month_date_labels=json.dumps(df.groupby(['year', 'month'])['Average Performance'].mean().keys().tolist(), cls=NpEncoder),
                           month_performance_values=json.dumps(df.groupby(['year', 'month'])['Average Performance'].mean().values.tolist(), cls=NpEncoder),
                           month_units_values=json.dumps(df.groupby(['year', 'month'])['Units Produced'].sum().values.tolist(), cls=NpEncoder),



                           )