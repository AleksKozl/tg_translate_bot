from peewee import IntegrityError
from typing import List

from database.db_models import User, Word, Translation, Synonym, History
from database.db_control import db_sqlite

"""

Модуль реализующий команды по отношению к БД в целом и к отдельным её таблицам.

Список функций:
    db_create_tables - Создает таблицы в БД по моделям из database.db_models
    
    Относятся к модели User:
        db_add_user - Добавляет пользователя в БД
        db_get_user - Возвращает объект пользователя из БД
        db_get_language - Возвращает текущее направление перевода пользователя
        db_set_language - Устанавливает текущее направление перевода пользователя
        db_set_state - Устанавливает текущее состояние пользователя

    Относятся к модели Word:
        db_add_word - Добавляет слово в БД
        db_get_word - Возвращает объект слова из БД
        db_get_word_by_id - Возвращает объект слова из БД по id
        
    Относятся к модели Translation:
        db_add_translation - Добавляет перевод в БД
        db_get_translation_by_id - Возвращает объект перевода из БД по id
        db_get_translation_by_translation_word - Возвращает объект перевода из БД по слову-переводу и языку
        db_get_all_translation - Возвращает все объекты переводов из БД по переводимому слову и языку
        
    Относятся к модели Synonym:
        db_add_synonym - Добавляет синоним в БД
        db_get_synonym_by_id - Возвращает объект синонима из БД по id
        db_get_synonym_by_synonym_word - Возвращает объект синонима из БД по слову-синониму
        db_get_all_synonyms - Возвращает все объекты синонимов из БД по слову-переводу и языку
        
    Относятся к модели History:
        db_add_to_history - Добавляет строку в историю запросов в БД
        db_get_history - Возвращает историю запросов из БД.


"""


#
# Относятся к БД
#

def db_create_tables() -> None:
    """  Функция создающая таблицы по моделям из database.db_models в БД  """
    db_sqlite.create_tables([User, Word, Translation, Synonym, History])


#
# Относятся к модели User
#

def db_add_user(user_id: int, chat_id: int, user_name: str, user_state: str, language: str) -> User:
    """
    Функция добавляет запись в таблицу по модели User
    или, при наличие записи с такими же параметрами, возвращает имеющуюся.

    Args:
        user_id (int) - UserID
        chat_id (int) - ChatID
        user_name (str) - Имя (First name) пользователя
        user_state (str) - Текущее состояние пользователя
        language (str) - Язык (направление) перевода

    Return:
        <class User>
    """

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


def db_get_user(user_id: int) -> User:
    """ Геттер объектов <class User> из БД по атрибуту user_id (int)"""
    return User.get(tg_user_id=user_id)


def db_get_language(user_id: int) -> str:
    """
    Геттер атрибута user_selected_language (str) объекта <class User> из БД

    Parameter:
        current_user (User) - Пользователь <class User> полученный по значению атрибута tg_user_id (int)

    Args:
        user_id (int) - Передаваемое значение атрибута tg_user_id (int) пользователя <class User>

    Returns:
        User.user_selected_language (str) - Язык (направление) перевода конкретного пользователя <class User>
    """

    current_user = User.get(tg_user_id=user_id)
    return current_user.user_selected_language


def db_set_language(user_id: int, language: str) -> None:
    """
    Сеттер атрибута user_selected_language (str) объекта <class User> из БД

    Parameter:
        current_user (User) - Пользователь <class User> полученный по значению атрибута tg_user_id (int)

    Args:
        user_id (int) - Передаваемое значение атрибута tg_user_id (int) пользователя <class User>
        language (str) - Передаваемое значение для перезаписи атрибута user_selected_language (str)
                         пользователя <class User> в БД

    Returns:
        None
    """

    current_user = User.get(tg_user_id=user_id)
    current_user.user_selected_language = language
    current_user.save()


def db_set_state(user_id: int, state: str) -> None:
    """
    Сеттер атрибута user_state (str) объекта <class User> из БД

    Parameter:
        current_user (User) - Пользователь <class User> полученный по значению атрибута tg_user_id (int)

    Args:
        user_id (int) - Передаваемое значение атрибута tg_user_id (int) пользователя <class User>
        state (str) - Передаваемое значение для перезаписи атрибута state (str)
                      пользователя <class User> в БД

    Returns:
        None
    """

    current_user = User.get(tg_user_id=user_id)
    current_user.user_state = state
    current_user.save()


#
# Относятся к модели Word
#

def db_add_word(word: str) -> Word:
    """
    Добавляет слово <class Word> в БД или возвращает, если такое слово уже записанно

    Args:
        word (str) - Слово для записи в БД

    Returns:
        <class Word>
    """

    try:
        Word.create(word=word)

    except IntegrityError:

        return Word.get(word=word)


def db_get_word(word: str) -> Word:
    """
    Геттер объектов <class Word> из БД по значению атрибта word (str)

    Args:
        word (str) - Слово для поиска по БД

    Returns:
        <class Word>
    """

    return Word.get(word=word)


def db_get_word_by_id(word_id: int) -> Word:
    """
    Геттер объектов <class Word> из БД по значению атрибута word_id (int)

    Args:
        word_id (int) - Значение атрибута word_id (int) для поиска среди объектов <class Word> в БД

    Returns:
        <class Word>
    """

    return Word.get_by_id(word_id)


#
# Относятся к модели Translation
#

def db_add_translation(
        word: str,
        language: str,
        translation_word: str,
        translation_translit: str,
        translation_translate: str
) -> Translation:
    """
    Добавляет перевод <class Translation> в БД или возвращает, если такой перевод уже записан

    Parameter:
        word_obj (Word) - Слово <class Word> полученный из БД по значению атрибута word (str)

    Args:
        word (str) - Введенное пользователем слово
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД
        translation_word (str) - Перевод для найденного в БД слова,
                                 атрибута word (str) слова <class Word>
        translation_translit (str) - Транскрипция (если есть) или "Транскрипции не нашлось :("
        translation_translate (str) - Значение перевода (если есть) или слово из БД,
                                      str или атрибут word (str) слова <class Word>

    Returns:
        <class Translation>
    """

    try:
        word_obj = db_get_word(word=word)
        Translation.get_or_create(
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


def db_get_translation_by_id(translation_id: int) -> Translation:
    """
    Геттер объектов <class Translation> из БД по значению translation_id (int)

    Args:
        translation_id (int) - Значение атрибута translation_id (int)
                               для поиска среди объектов <class Translation> в БД

    Returns:
        <class Translation>
    """

    return Translation.get_by_id(translation_id)


def db_get_translation_by_translation_word(translation_word: str, language: str) -> Translation:
    """
    Геттер объектов <class Translation> из БД по значению атрибутов translation_word (str) и translation_language (str)

    Parameter:
        translate_id (List[int]) - Список атрибутов translate_id (int)
                                   для всех объектов <class Translation> с совпадающими с искомыми
                                   значениями атрибутов translation_word (str) и translation_language (str)

    Args:
        translation_word (str) - Значение атрибута translation_id (int)
                                 для поиска среди объектов <class Translation> в БД
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД

    Returns:
        <class Translation>
    """

    translate_id = [
        i_translate.translation_id for i_translate in
        Translation.select().where(Translation.translation_word == translation_word,
                                   Translation.translation_language == language)
    ]

    return db_get_translation_by_id(translation_id=translate_id[0])


def db_get_all_translation(word: str, language: str) -> List[Translation]:
    """
    Геттер всех объектов <class Translation> из БД,
    значения атрибутов translation_word (str) и translation_language (str) которых
    совпадают с передаваемыми в функцию

    Parameter:
        word_obj (Word) - Слово <class Word> полученный из БД по значению атрибута word (str)
        all_translation (List[Translation]) - Список объектов <class Translation> с совпадающими с искомыми значениями
                                              атрибутов translation_word (str) и translation_language (str)

    Args:
        word (str) - Значение атрибута translation_id (int) для поиска среди объектов <class Word> в БД
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД

    Returns:
        List[Translation]
    """

    word_ogj = db_get_word(word=word)
    all_translation = [
        i_translate.translation_id for i_translate in
        Translation.select().where(
            Translation.word_id == word_ogj.word_id,
            Translation.translation_language == language
        )
    ]
    all_translation = [Translation.get_by_id(i_translate) for i_translate in all_translation]

    return all_translation


#
# Относятся к модели Synonym
#

def db_add_synonym(
        translation_word: str,
        language: str,
        synonym_word: str,
        synonym_translit: str,
        synonym_translate: str
) -> Synonym:
    """
    Добавляет синоним <class Synonym> в БД или возвращает, если такой синоним уже записан

    Parameter:
        translate_word_obj (Translation) - Перевод <class Translation> полученный из БД по значениям
                                           атрибутов translation_word (str) и language (str)

    Args:
        translation_word (str) - Перевод <class Translation> к которому относится добавляемый синоним <class Synonym>
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД
        synonym_word (str) - Синоним для найденного в БД перевода
        synonym_translit (str) - Транскрипция (если есть) или 'Транскрипции не нашлось :('
        synonym_translate (str) - Значение перевода (если есть) или 'Перевода не нашлось :('

    Returns:
        <class Synonym>
    """

    try:
        translate_word_obj = db_get_translation_by_translation_word(
            translation_word=translation_word,
            language=language
        )

        Synonym.get_or_create(
            translation_id=translate_word_obj.translation_id,
            synonym_word=synonym_word,
            synonym_translit=synonym_translit,
            synonym_translate=synonym_translate
        )

    except IntegrityError:
        return db_get_synonym_by_synonym_word(synonym_word=synonym_word)


def db_get_synonym_by_id(synonym_id: int) -> Synonym:
    """
    Геттер объектов <class Synonym> из БД по значению synonym_id (int)

    Args:
        synonym_id (int) - Значение атрибута synonym_id (int)
                           для поиска среди объектов <class Synonym> в БД

    Returns:
        <class Synonym>
    """

    return Synonym.get_by_id(synonym_id)


def db_get_synonym_by_synonym_word(synonym_word: str) -> Synonym:
    """
    Геттер объектов <class Synonym> из БД по значению synonym_word (str)

    Args:
        synonym_word (str) - Значение атрибута synonym_word (str)
                             для поиска среди объектов <class Synonym> в БД

    Returns:
        <class Synonym>
    """

    return Synonym.get(synonym_word=synonym_word)


def db_get_all_synonyms(translation_word: str, language: str) -> List[Synonym]:
    """
    Геттер всех объектов <class Synonym> из БД,
    значения атрибутов translation_word (str) и translation_language (str) которых
    совпадают с передаваемыми в функцию

    Parameter:
        translate_obj (Translation) - Перевод <class Translation> полученный из БД
                                      по значению атрибутов translation_word (str) и language (str)
        all_synonym (List[Synonym]) - Список объектов <class Synonym> с совпадающими с искомым значением
                                      атрибута synonym_id (int)

    Args:
        translation_word (str) - Значение атрибута translation_word (str)
                                 для поиска среди объектов <class Translation> в БД
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД

    Returns:
        List[Synonym]
    """

    translate_obj = db_get_translation_by_translation_word(
        translation_word=translation_word,
        language=language
    )

    all_synonym = [
        i_synonym.synonym_id for i_synonym in
        Synonym.select().where(Synonym.translation_id == translate_obj.translation_id)
    ]
    all_synonym = [Synonym.get_by_id(i_synonym) for i_synonym in all_synonym]

    return all_synonym


#
# Относятся к модели History
#


def db_add_to_history(
        user_id: int,
        operation_type: str,
        operation_language: str,
        operation_text: str,
        operation_translate: str,
        operation_datetime: str
) -> None:

    """
    Добавляет строку в историю запросов <class History> в БД.
    Проверяет текущее количество запросов хранящихся в истории.
    При превышении лимита history_max_length (int) - удаляет самый "старый" запрос.

    Parameter:
        current_history (List[<class History>]) - Текущая история запросов пользователя
        history_max_length (int) - Максимальное количество записей в БД для каждого пользователя
        first_hist (<class History>) - Первая в списке current_history, т.е. самая старая запись

    Args:
        user_id (int) - User_id
        operation_type (str) - Сценарий ('low', 'high' или 'custom')
        operation_language (str) - Язык перевода
        operation_text (str) - Текст для перевода
        operation_translate (str) - Результат перевода
        operation_datetime (str) - Дата и время совершения действия пользователем

    Returns:
        None
    """

    current_history = db_get_history(user_id)
    history_max_length = 10

    if len(current_history) >= history_max_length:

        first_hist = current_history[0]
        first_hist.delete_instance()

    History.get_or_create(
        user_id=user_id,
        operation_type=operation_type,
        operation_language=operation_language,
        operation_text=operation_text,
        operation_translate=operation_translate,
        operation_datetime=operation_datetime
    )


def db_get_history(user_id: int) -> List[History]:

    """
    Возвращает историю запросов <class History> из БД.

    Parameter:
        all_history (List[<class History>]) - Текущая история запросов пользователя

    Args:
        user_id (int) - User_id

    Returns:
        List[History]
    """

    all_history = [
        i_hist.history_id for i_hist in
        History.select().where(History.user_id == user_id)
    ]
    all_history = [History.get_by_id(i_hist) for i_hist in all_history]

    return all_history
