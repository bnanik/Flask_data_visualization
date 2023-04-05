from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators


class UserInputForm(FlaskForm):
    battery_type = SelectField('Battery Type', validators=[DataRequired()],
                               choices=[('Pouch', 'Pouch'),
                                        ('X', 'X'),
                                        ('Y', 'Y')
                                        ])
    run_name = StringField('Run Name', validators=[DataRequired(),
                                                   validators.Length(min=6, max=6),
                                                   validators.Regexp(regex=r"^[a-zA-Z]{2}\d{4}$", message="The name should start with 2 alphabetical characters and ends with 4 digits")])
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired(), validators.Length(min=6, max=6),
                                         validators.Regexp(regex=r"^\d{6}$", message="The product ID must be of digits")])
    units_produced = IntegerField('Units Produced', validators=[DataRequired()])
    average_performance = IntegerField('Average Performance', validators=[DataRequired()])
    submit = SubmitField("Save")
