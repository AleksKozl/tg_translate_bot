from peewee import IntegrityError

from database.db_models import User, Word, Translation, Synonym
from database.db_control import db_sqlite


def db_create_tables():
    db_sqlite.create_tables([User, Word, Translation, Synonym])


def db_add_user(user_id: int, chat_id: int, user_name: str, user_state: str, language: str):
    try:
        User.get_or_create(
            tg_user_id=user_id,
            tg_chat_id=chat_id,
            tg_user_name=user_name,
            user_state=user_state,
            user_selected_language=language
        )
    except IntegrityError:
        return db_get_user(user_id=user_id)


def db_get_user(user_id: int):
    return User.get(tg_user_id=user_id)


def db_get_language(user_id: int):
    current_user = User.get(tg_user_id=user_id)
    return current_user.user_selected_language


def db_set_language(user_id: int, language: str):
    current_user = User.get(tg_user_id=user_id)
    current_user.user_selected_language = language
    current_user.save()


def db_set_state(user_id: int, state: str):
    current_user = User.get(tg_user_id=user_id)
    current_user.user_state = state
    current_user.save()


def db_add_word(word: str):
    return Word.get_or_create(word=word)

    # try:
    #     return db_get_word(word=word)
    #
    # except DoesNotExist:
    #
    #     return Word.create(word=word)


def db_get_word(word: str):
    return Word.get(word=word)


def db_get_word_by_id(word_id: int):
    return Word.get_by_id(word_id)


def db_add_translation(
        word: str,
        language: str,
        translation_word: str,
        translation_translit: str,
        translation_translate: str
):
    try:
        word_obj = db_get_word(word=word)
        Translation.create(
            word_id=word_obj.word_id,
            translation_language=language,
            translation_word=translation_word,
            translation_translit=translation_translit,
            translation_translate=translation_translate
        )
    except IntegrityError:
        return db_get_translation_by_translation_word(
            translation_word=translation_word, language=language
        )


def db_get_translation_by_id(translation_id: int):
    return Translation.get_by_id(translation_id)


def db_get_translation_by_translation_word(translation_word: str, language: str):
    translate_id = [
        i_translate.translation_id for i_translate in
        Translation.select().where(Translation.translation_word == translation_word,
                                   Translation.translation_language == language)
    ]
    return db_get_translation_by_id(translation_id=translate_id[0])


def db_get_all_translation(word: str, language: str):
    word_ogj = db_get_word(word=word)
    all_translation = [
        i_translate.translation_id for i_translate in
        Translation.select().where(Translation.word_id == word_ogj.word_id,
                                   Translation.translation_language == language
                                   )
    ]
    all_translation = [Translation.get_by_id(i_translate) for i_translate in all_translation]

    return all_translation


def db_add_synonym(
        translation_word: str,
        language: str,
        synonym_word: str,
        synonym_translit: str,
        synonym_translate: str
):
    try:
        translate_word_obj = db_get_translation_by_translation_word(
            translation_word=translation_word,
            language=language
        )

        Synonym.create(
            translation_id=translate_word_obj.translation_id,
            synonym_word=synonym_word,
            synonym_translit=synonym_translit,
            synonym_translate=synonym_translate
        )

    except IntegrityError:
        return db_get_synonym_by_synonym_word(synonym_word=synonym_word)


def db_get_synonym_by_id(synonym_id: int):
    return Synonym.get_by_id(synonym_id)


def db_get_synonym_by_synonym_word(synonym_word: str):
    return Synonym.get(synonym_word=synonym_word)


def db_get_all_synonyms(translation_word: str, language: str):
    translate_obj = db_get_translation_by_translation_word(
        translation_word=translation_word,
        language=language
    )

    all_synonym = [i_synonym.synonym_id for i_synonym in
                   Synonym.select().where(Synonym.translation_id == translate_obj.translation_id)]
    all_synonym = [Synonym.get_by_id(i_synonym) for i_synonym in all_synonym]

    return all_synonym
