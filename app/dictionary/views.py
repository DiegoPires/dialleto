# app/home/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import dictionary
from ..models.Word import Word
from .. import db
from .forms import WordForm

@dictionary.route('/')
def index():
    """
    Render the homepage template on the / route
    """

    words = Word.query.all()

    return render_template('dictionary/index.html',
                           words=words,
                           title="Welcome")

@dictionary.route('/word/<string:definition>')
def word(definition):

    word = Word.query.filter_by(definition=definition).first

    if word is None:
        abort(404)

    return render_template('dictionary/word.html',
                           word=word,
                           title="Word")

# @dictionary.route('/word/add', methods=['GET', 'POST'])
# @login_required
# def add_word():
#
#     form = WordForm()
#
#     if form.validate_on_submit():
#
#         word = Word(word=form.word.data,
#                     definition=form.definition.data)
#
#         try:
#
#             db.session.add(word)
#             db.session.commit()
#             flash("Word added!")
#
#         except:
#             flash("Error")
#
#         return redirect(url_for("dictionary/word",definition=word.definition))
#
#     return render_template('dictionary/word.html', title="Add Department")
