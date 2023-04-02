from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Optional, Length, Email
from wtforms.validators import ValidationError
from better_profanity import profanity

def contains_profanity(text):
    return profanity.contains_profanity(text)

class NoProfanity:
    def __call__(self, form, field):
        if contains_profanity(field.data):
            raise ValidationError("Your comment contains profanity. Please remove any offensive language.")

class CommentForm(FlaskForm): 
    post_id = HiddenField('Post ID', validators=[DataRequired()]) 
    comment = TextAreaField('Comment', validators=[DataRequired(), Length(max=500), NoProfanity()])
    name = StringField('Name', validators=[Optional(), Length(max=50)])

class EmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

class SearchForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Search')