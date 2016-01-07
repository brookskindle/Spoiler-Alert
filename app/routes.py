# --------------------------------------------------------------------------
# ----------------------------------ROUTES----------------------------------
# --------------------------------------------------------------------------


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Remove database session at end of request/when app is shut down."""
    db.session.remove()


@app.route("/")
def index():
    default_post = "We're all spoiled out. Give us a hand and tell us yours!"
    # TODO: querying the entire post table is inefficient and will not scale. A
    # better solution for this needs to be found when relevant.
    posts = Post.query.all()
    spoiler = default_post
    if posts:  # At least one spoiler post
        i = random.randrange(len(posts))
        spoiler = posts[i].content
    return render_template("index.html", content=spoiler)


@app.route("/submit/", methods=["GET", "POST"])
@login_required
def submit():
    """Adds a submitted spoiler."""
    content = None
    user_id = None
    form = PostForm()
    if form.validate_on_submit():
        user_id = current_user.get_id()
        content = form.post.data
        post = Post(user_id, content)
        db.session.add(post)
        db.session.commit()
        return redirect("/", code=302)
    return render_template("submit.html", form=form)


@app.route("/register/", methods=["GET", "POST"])
def register():
    # TODO: implement https for a production server
    form = RegisterForm()
    if form.validate_on_submit():  # POST and form data validated.
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None:  # User already exists
            flash("{} is already in use.".format(username))
        else:  # User doesn't exist, add him!
            user = User()
            user.username = username
            user.password = password
            db.session.add(user)
            db.session.commit()
            flash("Successfully registered.")
            return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    # TODO: implement https for a production server
    form = LoginForm()
    if form.validate_on_submit():  # POST request with valid form data.
        username = form.username.data
        password = form.password.data
        remember_me = form.remember.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            # Valid credentials supplied.
            login_user(user, remember=remember_me)
            # TODO: Validate the "next" argument, lest I invite an open
            # redirect security violation.
            return redirect(request.args.get("next") or url_for("index"))
        else:
            # Invalid login credentials.
            flash("Invalid username or password supplied.")
    return render_template("login.html", form=form)


@app.route("/logout/", methods=["GET"])
@login_required
def logout():
    logout_user()
    flash("You have been successfully logged out!")
    return redirect(url_for("index"))
