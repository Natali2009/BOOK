from flask_wtf import FlaskForm
from wtforms.fields import (StringField, IntegerField, DateField, PasswordField, SubmitField, TextAreaField, BooleanField, RadioField)
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed

class RegisterForm(FlaskForm):
    profile_img = FileField("პროფილის სურათი", validators=[ FileAllowed(["jpg", "png"], message="მხოლოდ JPG ან PNG ფორმატში")])
    username = StringField("სრული სახელი", validators=[DataRequired()])
    email = StringField("ელ.ფოსტა", validators=[DataRequired()])
    phone_number = IntegerField("+995 888 88 88 88",validators=[DataRequired()])
    birthdate = DateField(validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired(),  Length(min=8, max=24, message="პაროლი უნდა შეიცავდეს მინიმუმ 8 სიმბოლოს")])
    confirm_password = PasswordField("გაიმეორე პაროლი",validators=[DataRequired(), EqualTo("password", message="პაროლები არ ემთხვევა")])
    submit = SubmitField("დარეგისტრირდი")

class LoginForm(FlaskForm):
    username = StringField ("სახელი", validators=[DataRequired()])
    password = PasswordField ("პაროლი", validators=[DataRequired()])
    submit = SubmitField("შესვლა", validators=[DataRequired()])

class AddBookForm(FlaskForm):
    name = StringField("წიგნის სახელი", validators=[DataRequired()])
    price = IntegerField("ფასი", validators=[DataRequired()])
    author = StringField("ავტორი", validators=[DataRequired()])
    description = StringField ("აღწერა", validators=[DataRequired()])
    image = FileField("სურათი", validators=[FileAllowed(["jpg", "png"], message="მხოლოდ JPG და PNG ფორმატები")])
    genre = StringField("ჟანრი", validators=[DataRequired()])
    time = StringField("სიუჟეტის დრო", validators=[DataRequired()])
    character = StringField("პერსონაჟი", validators=[DataRequired()])
    ending = StringField("დასასრული", validators=[DataRequired()])
    purpose = StringField("წაკითხვის მიზანი", validators=[DataRequired()])
    is_brillant = BooleanField("ფარული მარგალიტია" )
    emotion = StringField("ემოცია", validators=[DataRequired()] )
    submit = SubmitField("დაამატე წიგნი")

class AddAuthorForm(FlaskForm):
    name = StringField("ავტორის სახელი", validators=[DataRequired()])
    bio = TextAreaField("ავტორის ბიოგრაფია", validators=[DataRequired()])
    image = FileField("ავტორის ფოტო", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("დამატება")


class TestForm(FlaskForm):
    genre = RadioField('1. რა ჟანრის წიგნები მოგწონს ყველაზე მეტად?',
                       choices=[
                           ('fantasy', 'ფენტეზი'),
                           ('romance', 'რომანი'),
                           ('thriller', 'თრილერი'),
                           ('psychology', 'ფსიქოლოგია'),
                           ('detective', 'დეტექტივი'),
                           ('adventure', 'სათავგადასავლო')
                       ],
                       validators=[DataRequired()])

    time = RadioField('2. წიგნის მოქმედება სად ვითარდებოდეს?',
                         choices=[
                             ('modern_city', 'თანამედროვე ქალაქი'),
                             ('historical_era', 'ისტორიული ეპოქა'),
                             ('fantasy_world', 'წარმოსახვითი სამყარო'),
                             ('mysterious_place', 'ბნელი და იდუმალი ადგილი')
                         ],
                         validators=[DataRequired()])

    character = RadioField('3. როგორ გმირს აირჩევდი მთავარ პერსონაჟად?',
                           choices=[
                               ('warrior', 'მებრძოლი'),
                               ('romantic', 'რომანტიკოსი'),
                               ('detective', 'გამომძიებელ'),
                               ('mysterious', 'იდუმალი'),
                               ('thinker', 'მოაზროვნე'),
                               ('dramatic', 'დრამატული'),
                               ('quiet', 'მშვიდი')
                           ],
                           validators=[DataRequired()])

    ending = RadioField('4. როგორი დასასრული გირჩევნია?',
                        choices=[
                            ('happy', 'ბედნიერი'),
                            ('tragic', 'ტრაგიკული'),
                            ('open', 'ღია დასასრული'),
                            ('twist', 'მოულოდნელი')
                        ],
                        validators=[DataRequired()])

    purpose = RadioField('5. რატომ კითხულობ წიგნებს?',
                         choices=[
                             ('escape', 'რეალობიდან გასაქცევად'),
                             ('emotion', 'მძაფრი ემოციებისთვის'),
                             ('stress_relief', 'სტრესის მოსახსნელად და დასასვენებლად'),
                             ('self_growth', 'პიროვნული განვითარებისათვის და ცოდნის მისაღებად'),
                             ('critical_thinking', 'კრიტიკული აზროვნების გასავითარებლად')
                         ],
                         validators=[DataRequired()])

    submit = SubmitField('მიიღე ჩვენი რეკომენდაცია')
