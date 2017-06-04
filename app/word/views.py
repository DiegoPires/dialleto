# app/word/views.py

from flask import abort, flash, redirect, render_template, url_for, g
from flask_login import login_required, current_user

from sqlalchemy.sql import func
from sqlalchemy import tuple_
from sqlalchemy.orm import aliased

from . import word_blueprint
from ..models.Word import Word
from ..models.Text import Text
from ..models.Rating import Rating
from ..models.Language import Language

from .. import db
from .forms import WordForm


@word_blueprint.errorhandler(404)
def page_not_found(e):
    return render_template('word/404.html'), 404


@word_blueprint.route('/<string:term>', defaults={ "text_id":None, "action":None})
@word_blueprint.route('/<string:term>/<int:text_id>', defaults={ "action":None})
@word_blueprint.route('/<string:term>/<int:text_id>/<string:action>')
def word(term, text_id=None, action=None):

    if action != None and text_id != None:
        DefineRating(term,text_id,action)

    word = Word.query \
        .filter(Word.word.ilike(term)) \
        .first_or_404()

    if text_id != None:
        texts = word.texts.filter(Text.id==text_id)
        onlyText=True

        if texts.count() == 0:
            abort(404)
    else:
        texts = word.texts.order_by(Text.num_ratings.desc())
        onlyText=False

    if word is None:
        abort(404)

    return render_template('word/word.html',
                           word=word,
                           texts=texts,
                           onlyText=onlyText,
                           title="Word")


@word_blueprint.route('/add', defaults={ "term":None}, methods=['GET',"POST"])
@word_blueprint.route('/add/<string:term>', methods=['GET', 'POST'])
@login_required
def add_word(term):

    form = WordForm()
    form.language.choices=[(g.id, g.name) for g in Language.query.order_by('name')]

    word = None
    if term != None:
        word = Word.query.filter(Word.word==term).first_or_404()
        form.word.data = word.word
        form.word(disabled=True)
        form.word_id.data = word.id

    if form.validate_on_submit():

        if form.word_id.data != "":
            word = Word.query.filter(Word.id==form.word_id.data).first_or_404()
        else:
            word = Word(word=form.word.data, created_by_id=current_user.id)

        textDescription = Text(text=form.definition.data,
                               type=1,
                               language_id=form.language.data,
                               created_by_id=current_user.id)

        textExample = Text(text=form.example.data,
                           type=2,
                           language_id=form.language.data,
                           created_by_id=current_user.id)

        textDescription.sons.append(textExample)

        word.texts.append(textDescription)
        word.texts.append(textExample)

        try:

            db.session.add(word)
            db.session.commit()
            flash("Word added!")

            return redirect(url_for("word.word", term=word.word))

        except:
            flash("Error")

    return render_template('word/addword.html',
                           form=form,
                           word=word,
                           add_word=True)


@word_blueprint.route('/delete/<string:word>', methods=['GET'])
@login_required
def delete_word(word):
    word = Word.query.filter(Word.word == word).first_or_404()

    if word.created_by_id != current_user.id:
        abort(401)

    db.session.delete(word)
    db.session.commit()
    flash('You have successfully deleted the word.')

    # redirect to the roles page
    return redirect(url_for('dictionary.index'))


def DefineRating(term, text_id, action):

    exist = Rating.query.filter(Rating.text_id==text_id, Rating.created_by_id==current_user.id)
    if exist.count() != 0:

        flash("You already {0} this word".format(action))

    else:

        rating = Rating(text_id=text_id, created_by_id=current_user.id)

        if action == "like":
            rating.rating = 1
        else:
            rating.rating = -1

        try:
            db.session.add(rating)
            db.session.commit()
            flash("{0} added to text".format(action))
        except:
            flash("Error")