# app/word/views.py

from flask import abort, flash, redirect, render_template, url_for, g
from flask_login import login_required, current_user

from sqlalchemy.sql import func

from . import dic_blueprint
from ..models.Word import Word
from ..models.Text import Text
from ..models.Language import Language
from ..models.Tag import Tag
from ..models.TagText import TagText
from ..models.Lexicographer import Lexicographer

from .. import db



@dic_blueprint.route('/')
def index():

    words = get_words(None, 2)

    languages = Language.query.all()
    tags = Tag.query.all()

    return render_template('dictionary/index.html',
                           words=words,
                           languages=languages,
                           tags=tags,
                           title="Dialleto")


@dic_blueprint.route('/search', methods=['POST'])
@dic_blueprint.route('/search/<int:page>', defaults={ "term":"" }, methods=['GET',"POST"])
@dic_blueprint.route('/search/<int:page>/<string:term>', methods=['GET', "POST"])
def search(page=1, term=None):

    if term == None:
        #if not g.search_form.validate_on_submit():
        #else:
        term = g.search_form.word.data

    if term == None:
        return redirect(url_for('index'))

    words = get_words(term)

    if words.count() == 1:
        return redirect(url_for("word.word", term=words.first().word))

    pagination = words.paginate(page, 2, False)

    return render_template('dictionary/search.html',
                           words=pagination.items,
                           pagination=pagination,
                           term=term,
                           title="Dialleto")


@dic_blueprint.route('/random')
def random():
    words = get_words(None)
    return redirect(url_for("word.word", term=words.one().word))


@dic_blueprint.route('/tag/<string:tag>')
def tag(tag):
    words = query_word().filter(Tag.tag == tag)
    tag=Tag.query.filter(Tag.tag==tag).first_or_404()

    return render_template('dictionary/tag.html',
                           tag=tag.tag,
                           words=words,
                           title="Dialleto")

@dic_blueprint.route('/language/<string:language>')
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

    get_words = db.session.query(Word, Text, Language, Lexicographer)\
        .join(Text, Text.id == popular_description_id)\
        .join(Language, Language.id == Text.language_id)\
        .join(Lexicographer, Lexicographer.id == Text.created_by_id)\
        .with_entities(Word.id, Word.word, Text.timestamp, Text.text, Text.id.label("text_id"),  \
                       Language.name, Language.code, Word.created_by_id, Lexicographer.username, \
                       Text.num_ratings, Language.color)

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
