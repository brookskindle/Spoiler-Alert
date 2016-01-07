# --------------------------------------------------------------------------
# ----------------------------------FORMS-----------------------------------
# --------------------------------------------------------------------------


class PostForm(Form):
    """
    A form for submitting a spoiler post.
    """
    post = TextField("Give us a spoiler!", validators=[DataRequired()])
    submit = SubmitField("Submit")


class LoginForm(Form):
    """
    A form to allow users to log in.
    """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class RegisterForm(Form):
    """
    A form that people can use to register an account.
    """
    username = StringField("Create a username", validators=[DataRequired()])
    password = PasswordField("Create a password", validators=[DataRequired(),
                EqualTo('password_repeat', message="Passwords must match")])
    password_repeat = PasswordField("Repeat password",
                                    validators=[DataRequired()])
    submit = SubmitField("Register")
