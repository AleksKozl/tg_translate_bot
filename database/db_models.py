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

    tg_user_id = IntegerField(primary_key=True)
    tg_chat_id = IntegerField(unique=True)
    tg_user_name = CharField(max_length=30)
    user_state = CharField(max_length=30)
    user_selected_language = CharField(max_length=10)

    class Meta:
        db_table = 'Users'


class Word(BaseModel):
    word_id = AutoField(primary_key=True, unique=True)
    word = CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'Words'


class Translation(BaseModel):

    translation_id = AutoField(primary_key=True, unique=True)
    word_id = ForeignKeyField(Word.word_id)
    translation_language = CharField(max_length=10)
    translation_word = CharField(max_length=150)
    translation_translit = CharField(max_length=50)
    translation_translate = CharField(max_length=150)

    class Meta:
        db_table = 'Translations'


class Synonym(BaseModel):

    synonym_id = AutoField(primary_key=True, unique=True)
    translation_id = ForeignKeyField(Word)
    synonym_word = CharField(max_length=150)
    synonym_translit = CharField(max_length=50)
    synonym_translate = CharField(max_length=150)

    class Meta:
        db_table = 'Synonyms'
