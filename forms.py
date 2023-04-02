from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email

class CommentForm(FlaskForm): 
    post_id = HiddenField('Post ID', validators=[DataRequired()]) 
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=500)])
    name = StringField('Name', validators=[Optional(), Length(max=50)])

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Search')