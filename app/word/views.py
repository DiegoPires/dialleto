# app/word/views.py

from flask import abort, flash, redirect, render_template, url_for, g
from flask_login import login_required, current_user

from sqlalchemy.sql import func
from sqlalchemy import tuple_
from sqlalchemy.orm import aliased

from . import word_blueprint
from ..models.Word import Word
from ..models.Text import Text
from ..models.Language import Language
from ..models.Tag import Tag
from ..models.TagText import TagText
from ..models.Lexicographer import Lexicographer

from .. import db
from .forms import WordForm



@word_blueprint.route('/<string:term>')
def word(term):

    word = Word.query \
        .filter(Word.word.ilike(term)) \
        .first()

    texts = word.texts.order_by(Text.num_ratings.desc())

    if word is None:
        abort(404)

    return render_template('word/word.html',
                           word=word,
                           texts=texts,
                           title="Word")

@word_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_word():

    form = WordForm()

    if form.validate_on_submit():

        word = Word(word=form.word.data, created_by_id=current_user.id)

        textDescription = Text(text=form.definition.data, type=TextType.Definition, language_id=1)
        textExample = Text(text=form.example.data, type=TextType.Example, language_id=1)

        word.texts.append(textDescription)
        word.texts.append(textExample)

        try:

            db.session.add(word)
            db.session.commit()
            flash("Word added!")

            return redirect(url_for("word.word", term=word.word))

        except:
            flash("Error")

    return render_template('dictionary/addword.html', title="Add Word", form=form, add_word=True)


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