from flask_wtf import FlaskForm
from application.user.models import User
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError


class AssignBookForm(FlaskForm):
    username = StringField(
        "UserName", validators=[DataRequired(), Length(min=2, max=30)]
    )
    book_id = IntegerField("Book id", validators=[DataRequired()])
    submit = SubmitField("Assign Book")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("That username is doesnot exists.")
