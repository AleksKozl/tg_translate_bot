from peewee import (
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    AutoField
)

from database.db_control import db_sqlite


class BaseModel(Model):
    class Meta:
        database = db_sqlite


class User(BaseModel):

    """
    Модель для хранения информации о пользователе

    Attributes:
        tg_user_id (int) - UserID
        tg_chat_id (int) - ChatID
        tg_user_name (str) - Имя (First name) пользователя
        user_state (str) - Поле для хранения текущего состояния пользователя (используется для отслеживания ошибок)
        user_selected_language (str) - Выбранный пользователем язык (направление) перевода

    """

    tg_user_id = IntegerField(primary_key=True)
    tg_chat_id = IntegerField(unique=True)
    tg_user_name = CharField(max_length=30)
    user_state = CharField(max_length=30)
    user_selected_language = CharField(max_length=10)

    class Meta:
        db_table = 'Users'


class Word(BaseModel):

    """
    Модель для хранения переводимых слов

    Attributes:
        word_id (int) - ID слова
        word (str) - Слово

    """

    word_id = AutoField(primary_key=True, unique=True)
    word = CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Words'


class Translation(BaseModel):

    """
    Модель для хранения переводов слов

    Attributes:
        translation_id (int) - ID перевода
        word_id (int) - ID слова <class Word> к которому относится перевод
        translation_language (str) - Язык (направление) перевода
        translation_word (str) - Перевод пользовательского слова <class Word>
        translation_translit (str) - Транскрипция (если есть) или "Транскрипции не нашлось :("
        translation_translate (str) - Значение перевода (если есть) или введённое пользователем слово <class Word>


    """

    translation_id = AutoField(primary_key=True, unique=True)
    word_id = ForeignKeyField(Word.word_id)
    translation_language = CharField(max_length=10)
    translation_word = CharField(max_length=150)
    translation_translit = CharField(max_length=50)
    translation_translate = CharField(max_length=150)

    class Meta:
        db_table = 'Translations'


class Synonym(BaseModel):

    """
    Модель для хранения синонимов переводов

    Attributes:
        synonym_id (int) - ID синонима
        translation_id (int) - ID перевода <class Translation> к которому относится синоним
        synonym_word (str) - Синоним перевода <class Translation>
        synonym_translit (str) - Транскрипция (если есть) или "Транскрипции не нашлось :("
        synonym_translate (str) - Значение синонима (если есть) или введённое пользователем слово <class Word>


    """

    synonym_id = AutoField(primary_key=True, unique=True)
    translation_id = ForeignKeyField(Word)
    synonym_word = CharField(max_length=150)
    synonym_translit = CharField(max_length=50)
    synonym_translate = CharField(max_length=150)

    class Meta:
        db_table = 'Synonyms'
