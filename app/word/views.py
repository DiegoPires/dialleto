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
from ..models.Relation import Relation

from .. import db
from .forms import WordForm, RelatedWordForm


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


@word_blueprint.route('/addrelatedword/<string:word>/<int:text_id>', methods=['GET', "POST"])
@login_required
def add_related_word(word,text_id):

    form = RelatedWordForm()

    word = Word.query.filter(Word.word==word).first_or_404()

    nottexts = db.session.query(Text, Relation) \
        .join(Relation, Text.id == Relation.text_id_to)\
        .filter(Text.id==text_id) \
        .with_entities(Relation.text_id_from)

    notwords = db.session.query(Text) \
        .filter(Text.id.in_(nottexts)) \
        .with_entities(Text.word_id)

    form.word.data = word.word
    words = db.session.query(Word, Text) \
        .join(Text, Text.word_id == Word.id) \
        .filter(Text.type != 2) \
        .filter(Text.id != text_id) \
        .filter(Word.id != word.id) \
        .filter(Word.id.notin_(notwords)) \
        .order_by(Word.word) \
        .with_entities(Text.id, (Word.word + ": " + Text.text).label("text"))

    if words.count() == 0:
        flash("No words availables to relate")
        return redirect(url_for("word.word", term=word.word))

    form.words.choices = [(g.id, g.text) for g in words]

    if form.validate_on_submit():

        try:
            for text_form in form.words.data:
                db.session.add(Relation(text_id_to=text_id, text_id_from=text_form))
                db.session.add(Relation(text_id_to=text_form, text_id_from=text_id))

            db.session.commit()
            flash("Relation added!")

        except:
            flash("Error")

        return redirect(url_for("word.word", term=form.word.data))

    return render_template('word/addrelatedword.html',
                           form=form,
                           word=word)


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

    if action == "like":
        ratingType = 1
    else:
        ratingType = -1

    execute = True

    exist = Rating.query.filter(Rating.text_id==text_id, Rating.created_by_id==current_user.id)
    if exist.count() != 0:

        if exist.first().rating != ratingType:
            db.session.delete(exist.first())
            db.session.commit()
        else:
            execute = False
            flash("You already {0} this word".format(action))

    if execute:

        rating = Rating(text_id=text_id, rating=ratingType, created_by_id=current_user.id)

        try:
            db.session.add(rating)
            db.session.commit()
            flash("{0} added to text".format(action))
        except:
            flash("Error")