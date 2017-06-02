# app/home/views.py

from flask import abort, flash, redirect, render_template, url_for, g
from flask_login import login_required, current_user

from sqlalchemy.sql import func
from sqlalchemy import tuple_
from sqlalchemy.orm import aliased

from . import dictionary
from ..models.Word import Word
from ..models.Text import Text, TextType
from ..models.Language import Language
from ..models.Tag import Tag
from ..models.TagText import TagText

from .. import db
from .forms import WordForm

@dictionary.route('/')
def index():

    words = get_words(None, 2)

    languages = Language.query.all()
    tags = Tag.query.all()

    return render_template('dictionary/index.html',
                           words=words,
                           languages=languages,
                           tags=tags,
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

        word = Word(word=form.word.data, created_by_id=current_user.id)

        textDescription = Text(text=form.definition.data, type=TextType.Definition, language_id=1)
        textExample = Text(text=form.example.data, type=TextType.Example, language_id=1)

        word.texts.append(textDescription)
        word.texts.append(textExample)

        try:

            db.session.add(word)
            db.session.commit()
            flash("Word added!")

            return redirect(url_for("dictionary.word", term=word.word))

        except:
            flash("Error")

    return render_template('dictionary/addword.html', title="Add Word", form=form, add_word=True)


@dictionary.route('/word/delete/<string:word>', methods=['GET'])
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


@dictionary.route('/random')
def random_word():
    words = get_words(None)
    return redirect(url_for("dictionary.word", term=words.one().word))


@dictionary.route('/tag/<string:tag>')
def tag(tag):
    words = query_word().filter(Tag.tag == tag)
    tag=Tag.query.filter(Tag.tag==tag).first_or_404()

    return render_template('dictionary/tag.html',
                           tag=tag.tag,
                           words=words,
                           title="Dialleto")

@dictionary.route('/language/<string:language>')
def language(language):
    words = query_word().filter(Language.name == language)
    language = Language.query.filter(Language.name==language).first_or_404()

    return render_template('dictionary/language.html',
                           language=language,
                           words=words,
                           title="Dialleto")


def query_word():
    words = db.session.query(Word, Text, Language, TagText, Tag) \
        .join(Text, Text.word_id == Word.id) \
        .join(Language, Language.id == Text.language_id) \
        .join(TagText, Text.id == TagText.text_id) \
        .join(Tag, Tag.id == TagText.tag_id) \
        .order_by(Text.timestamp.desc()) \
        .with_entities(Word.id, Word.word, Text.timestamp, Text.text, Language.name, Language.code, Word.created_by_id)

    return words

def get_words(term, quantity=1):
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
        .with_entities(Word.id, Word.word, Text.timestamp, Text.text, Language.name, Language.code, Word.created_by_id)

    if term is None:

        return get_words.offset(
            func.floor(
                func.random() *
                db.session.query(func.count(Word.id))
            )
            ).limit(quantity)

    # otherwise use our term to search
    else:
        return get_words.filter(Word.word.ilike("%" + term + "%"))
