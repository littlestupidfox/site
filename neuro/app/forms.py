from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, TextAreaField, PasswordField
from wtforms.validators import DataRequired, Length

from wtforms import FieldList, FormField, DateField

class ShootingDateForm(FlaskForm):
    date = DateField('Дата съемки', format='%Y-%m-%d', validators=[DataRequired()])

class AnnouncementForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    button_text = StringField('Текст кнопки', validators=[DataRequired()])
    dates = FieldList(FormField(ShootingDateForm), min_entries=1)

class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

class BookingForm(FlaskForm):
    client_name = StringField('ФИО', validators=[DataRequired()])
    people_count = IntegerField('Количество человек', validators=[DataRequired()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=15)])
    shooting_date = DateField('Дата съемки', format='%Y-%m-%d', validators=[DataRequired()])
    shooting_time = SelectField('Время съемки', choices=[
        ('09:00', '09:00 - 11:00'),
        ('11:00', '11:00 - 13:00'),
        ('13:00', '13:00 - 15:00'),
        ('15:00', '15:00 - 17:00'),
        ('17:00', '17:00 - 19:00')
    ], validators=[DataRequired()])

class ArticleForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Содержание', validators=[DataRequired()])
    image = StringField('URL изображения')

class EmployeeForm(FlaskForm):
    full_name = StringField('ФИО', validators=[DataRequired()])
    position = StringField('Должность', validators=[DataRequired()])
    photo = StringField('Фото (URL или имя файла)', validators=[DataRequired()])
    bio = TextAreaField('О сотруднике', validators=[DataRequired()])

class AnnouncementForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    button_text = StringField('Текст кнопки', validators=[DataRequired()])