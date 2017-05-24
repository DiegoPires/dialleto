# app/home/views.py

from flask import abort, flash, redirect, render_template, url_for, g
from flask_login import login_required

from sqlalchemy.sql import func
from sqlalchemy import tuple_
from sqlalchemy.orm import aliased

from . import dictionary
from ..models.Word import Word
from ..models.Text import Text
from ..models.Language import Language

from .. import db
from .forms import WordForm

@dictionary.route('/')
def index():

    # take always our first word in the database: Dialleto! (unless you haven't set him up as first)
    word = Word.query.get(1)

    words = get_words(None)

    return render_template('dictionary/index.html',
                           words=words,
                           word=word,
                           title="Dialleto")

@dictionary.route('/search', methods=['POST'])
@dictionary.route('/search/<string:term>/<int:page>', methods=['POST', 'GET'])
def search(term=None,page=1):

    if term == None:
        #if not g.search_form.validate_on_submit():
        #else:
        term = g.search_form.word.data

    if term == None:
        return redirect(url_for('index'))

    words = get_words(term)

    if words.count() == 1:
        return redirect(url_for("dictionary.word", term=words.first().word))

    pagination = words.paginate(page, 2, False)

    return render_template('dictionary/search.html',
                           words=pagination.items,
                           pagination=pagination,
                           term=term,
                           title="Dialleto")


@dictionary.route('/word/<string:term>')
def word(term):

    word = Word.query.filter(Word.word.ilike(term)).first()

    if word is None:
        abort(404)

    return render_template('dictionary/word.html',
                           word=word,
                           term=term,
                           title="Word")

@dictionary.route('/word/add', methods=['GET', 'POST'])
@login_required
def add_word():

    form = WordForm()

    if form.validate_on_submit():

        word = Word(word=form.word.data,
                    definition=form.definition.data)

        try:

            db.session.add(word)
            db.session.commit()
            flash("Word added!")

        except:
            flash("Error")

        return redirect(url_for("dictionary/word",term=word.word))

    return render_template('dictionary/word.html', title="Add Word")


def get_words(term):
    # if we haven`t received a term to search, randomize the words


    PopularDescription = Text
    popular_description_id = db.session.query(PopularDescription.id)\
                    .filter(PopularDescription.word_id == Word.id)\
                    .limit(1)\
                    .correlate(Word)\
                    .as_scalar()

    get_words = db.session.query(Word, Text, Language)\
        .join(Text, Text.id == popular_description_id)\
        .join(Language, Language.id == Text.language_id)\
        .with_entities(Word.id, Word.word, Text.timestamp, Text.text, Language.name, Language.code)

    if term is None:

        return get_words.offset(
            func.floor(
                func.random() *
                db.session.query(func.count(Word.id))
            )
            ).limit(1)

    # otherwise use our term to search
    else:
        return get_words.filter(Word.word.ilike("%" + term + "%"))
