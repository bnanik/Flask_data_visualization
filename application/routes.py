import pandas as pd
import numpy as np
from application import app
from flask import render_template, flash, redirect, url_for, get_flashed_messages, request
from application.form import UserInputForm
from werkzeug.utils import secure_filename
import datetime
from datetime import date
import os
import json

df = pd.DataFrame

@app.route('/')
def index():  # put application's code here
    form = UserInputForm()
    return render_template('index.html', title='index', form=form)

@app.route('/view_data')
def view_data():  # put application's code here
    global df
    form = UserInputForm()
    headers = df.columns
    return render_template('view_data.html', df=df, headers=headers, form=form)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global df
    form = UserInputForm()
    if request.method == 'POST':
        files = request.files.getlist('file')
        dfs = []
        for file in files:
            csv_file = pd.read_csv(file)
            dfs.append(csv_file)
        df = pd.concat(dfs, ignore_index=True)
        df['Date'] = pd.to_datetime(df['Date'], format='%b %d %Y')
        # df.sort_values(by='Date', inplace=True)
        df['year'] = df['Date'].dt.year
        df['quarter'] = df['Date'].dt.quarter
        df['month'] = df['Date'].dt.month_name(locale='English')
        df.reset_index(inplace=True)
        # flash("Uploaded Successfully!", 'success')
        headers = df.columns
        return render_template('view_data.html', df=df, headers=headers)


        #
        # return render_template('upload.html', form=form, data=df.to_html())
        # print(df)
        # return 'uploaded Successfully'
    return render_template('index.html', title='Upload', form=form)

@app.route('/edit_data', methods=['POST'])
def edit_data():
    global df
    row_index = int(request.form['id'])
    run_name = request.form['editRunName']
    date1 = request.form['editDate']
    product_id = int(request.form['editProductId'])
    battery_type = request.form['editBatteryType']
    units_produced = int(request.form['editUnitsProduced'])
    average_performance = int(request.form['editAveragePerformance'])

    # Server side Data Validation
    errors = {}
    if not run_name[0].isalpha():
        errors['run_name'] = ["The first and second character of Run Name field should be alphabet"]

    # Update the values in the Pandas DataFrame
    df.loc[row_index, 'Run Name'] = run_name
    df.loc[row_index, 'Date'] = date1
    df.loc[row_index, 'Product ID'] = product_id
    df.loc[row_index, 'Battery Type'] = battery_type
    df.loc[row_index, 'Units Produced'] = units_produced
    df.loc[row_index, 'Average Performance'] = average_performance

    # Update Date related columns
    # df.loc[row_index, 'Date'] = pd.to_datetime(df.loc[row_index, 'Date'])
    new_date = pd.to_datetime(df.loc[row_index, 'Date'])
    df.loc[row_index, 'year'] = new_date.year
    df.loc[row_index, 'quarter'] = new_date.quarter
    df.loc[row_index, 'month'] = new_date.month_name(locale='English')

    data = df.to_dict('records')
    headers = df.columns
    return render_template('view_data.html', df=df, data=data, headers=headers)


@app.route('/add_data', methods=['POST'])
def add_data():
    global df
    run_name = request.form['run_name']
    date1 = request.form['date']
    product_id = request.form['product_id']
    battery_type = request.form['battery_type']
    units_produced = int(request.form['units_produced'])
    average_performance = int(request.form['average_performance'])

    # append the form data to the existing dataframe
    new_row = {'Run Name': run_name,
               'Date': date1,
               'Product ID': product_id,
               'Battery Type': battery_type,
               'Units Produced': units_produced,
               'Average Performance': average_performance}
    index_value = int(len(df))  # set the index value to the length of the existing dataframe
    df_new = pd.DataFrame(new_row, index=[index_value])
    df_new['Date'] = pd.to_datetime(df_new['Date'])
    df_new['year'] = df_new['Date'].dt.year
    df_new['quarter'] = df_new['Date'].dt.quarter
    df_new['month'] = df_new['Date'].dt.month_name(locale='English')
    df = df.append(df_new)

    data = df.to_dict('records')
    headers = df.columns
    return render_template('view_data.html', df=df, data=data, headers=headers)




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
                           date_labels=json.dumps(list(df['Date'].dt.strftime('%Y-%m-%d')), cls=NpEncoder),
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
                           month_date_labels=json.dumps(df.groupby(['month', 'year'])['Average Performance'].mean().keys().tolist(), cls=NpEncoder),
                           month_performance_values=json.dumps(df.groupby(['month', 'year'])['Average Performance'].mean().values.tolist(), cls=NpEncoder),
                           month_units_values=json.dumps(df.groupby(['year', 'month'])['Units Produced'].sum().values.tolist(), cls=NpEncoder),



                           )