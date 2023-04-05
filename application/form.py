from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class UserInputForm(FlaskForm):
    battery_type = SelectField('Battery Type', validators=[DataRequired()],
                               choices=[('Pouch', 'Pouch'),
                                        ('X', 'X'),
                                        ('Y', 'Y')
                                        ])
    run_name = StringField('Run Name', validators=[DataRequired()])
    product_id = IntegerField('Product ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    units_produced = IntegerField('Units Produced', validators=[DataRequired()])
    average_performance = IntegerField('Average Performance', validators=[DataRequired()])
    submit = SubmitField("Save")
