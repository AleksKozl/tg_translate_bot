import database.db_func as db_func


"""

Модуль отвечает за обработку  данных (в формате JSON) полученных от запроса к 'Яндекс.Словарю'.

Список функций:
    cut - 'Обрезает' лишние данные.
    to_database - Вносит полученные от функции cut() данные в БД.
    pretty_text - Выдает единую строку с переводами, транскрипциями и синонимами полученными от БД.

"""


def cut(translate_json: dict) -> dict:

    """
    Обрезает лишние данные от входящего словаря.
    Оставляет варианты перевода, их синонимы и транскрипции.


    Parameter:
        text (dict) - Возвращаемый словарь с итоговыми данными
        translations (List[str]) - Список всех вариантов перевода
        mean (List[str]) - Список значений переводов
        translit (List[str]) - Список транскрипций переводов
        synonyms (List[str]) - Список синонимов переводов
        synonyms_translit (List[str]) - Список транскрипций синонимов
        means (List[str]) - Список значений синонимов для каждого варианта перевода

    Args:
        translate_json (dict) - Пеедаваемый словарь с результатами запроса перевода

    Returns:
        dict
    """

    text = dict()

    for i_def in translate_json['def']:
        text['text'] = i_def['text']

        translations = [i_translate['text'] for i_translate in i_def['tr']]
        text['translations'] = list(dict())

        for i_word in translations:
            text['translations'].append(
                {
                    'text': i_word,
                    'translit': 'Транскрипции не нашлось :(',
                    'mean': 'Перевода не нашлось :(',
                    'synonyms': list(dict())
                }
            )

        for i_translate in text['translations']:

            try:
                mean = [
                    [i_mean['text'] for i_mean in i_trans['mean']]
                    for i_trans in i_def['tr']
                    if i_trans['text'] == i_translate['text']
                ]

                i_translate['mean'] = mean[0][0]

            except KeyError:
                continue

        for i_translate in text['translations']:

            try:
                translit = [
                    i_trans['ts']
                    for i_trans in i_def['tr']
                    if i_trans['text'] == i_translate['text']
                ]
                i_translate['translit'] = translit[0]

            except KeyError:
                continue

        for i_translate in text['translations']:

            try:

                synonyms = [
                    [i_synonym['text'] for i_synonym in i_trans['syn']]
                    for i_trans in i_def['tr']
                    if i_trans['text'] == i_translate['text']
                ]
                synonyms = synonyms[0] if isinstance(synonyms, list) else synonyms

                synonyms_translit = [
                    [i_synonym['ts'] for i_synonym in i_trans['syn']]
                    for i_trans in i_def['tr']
                    if i_trans['text'] == i_translate['text']
                ][0]

                means = [
                    [i_mean['text'] for i_mean in i_trans['mean']]
                    for i_trans in i_def['tr']
                    if i_trans['text'] == i_translate['text']
                ][0]

                if len(means) > len(synonyms):
                    means = means[1:]

                else:
                    means = means + (means * (len(synonyms) - len(means)))

                for i_count, i_synonym in enumerate(synonyms):
                    i_translate['synonyms'].append(
                        {
                            'text': i_synonym,
                            'mean': means[i_count],
                            'translit': synonyms_translit[i_count]
                        }
                    )
            except KeyError:
                continue

    return text


def to_database(word: str, language: str, translate_json: dict) -> None:

    """
    Добавляет в БД варианты перевода, их синонимы и транскрипции.

    Args:
        word (str) - Слово к которому пользователь запросил перевод
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД
        translate_json (dict) - Пеедаваемый словарь с результатами запроса перевода

    Parameter:
        text (dict) - Словарь с 'обрезанными' данными

        translate_word (str) - Вариант перевода
        translate_means (str) - Значение варианта перевода
        translate_synonyms (dict) - Словарь с синонимами для варианта перевода
        translate_translit (str) - Транскрипция варианта перевода

        synonym_word (str) - Синоним
        synonym_translate (str) - Значение синонима
        synonym_translit (str) - Транскрипция синонима

    Returns:
        None
    """

    text = cut(translate_json)

    for i_translate in text['translations']:
        translate_word = i_translate['text']
        translate_means = i_translate.get('mean', word)
        translate_synonyms = i_translate.get('synonyms')
        translate_translit = i_translate.get('translit', 'Транскрипции не нашлось :(')

        db_func.db_add_translation(
            word=word,
            language=language,
            translation_word=translate_word,
            translation_translit=translate_translit,
            translation_translate=translate_means
        )

        if len(translate_synonyms) >= 1:
            for i_synonym in translate_synonyms:
                synonym_word = i_synonym['text']
                synonym_translate = i_synonym.get('mean', 'Перевода не нашлось :(')
                synonym_translit = i_synonym.get('translit', 'Транскрипции не нашлось :(')

                db_func.db_add_synonym(
                    translation_word=translate_word,
                    language=language,
                    synonym_word=synonym_word,
                    synonym_translit=synonym_translit,
                    synonym_translate=synonym_translate
                )


def pretty_text(word: str, language: str, translate_json: dict, max_numbers_of_translations: int) -> str:

    """
    Преобразует входящий словарь в более читаемый вид.

    Args:
        word (str) - Слово к которому пользователь запросил перевод.
        language (str) - Текущий язык (направление) перевода,
                         атрибут user_selected_language (str) объекта <class User> из БД.
        translate_json (dict) - Пеедаваемый словарь с результатами запроса перевода.
        max_numbers_of_translations (int) - Максимальное количество выводимых вариантов перевода

    Parameter:
        text (str) - Итоговая строка с вариантами перевода, их синонимами и транскрипциями.
        synonyms (List[Synonym]) - Список всех объектов синонимов (<class Synonym>)
                                   относящихся к конкретному варианту перевода.

    Returns:
        str
    """

    to_database(word, language, translate_json)

    text = f'Ваш перевод готов! \n'
    text += '    Варианты перевода: \n'

    for i_count, i_translation in enumerate(db_func.db_get_all_translation(word=word, language=language)):
        text += '\n        {translation_word} / (|{translation_translit}|) - {translation_translate}\n'.format(
            translation_word=i_translation.translation_word,
            translation_translit=i_translation.translation_translit,
            translation_translate=i_translation.translation_translate
        )
        synonyms = db_func.db_get_all_synonyms(
                translation_word=i_translation.translation_word,
                language=i_translation.translation_language
        )
        if len(synonyms) > 0:
            text += '        Синонимы:\n'
            for i_synonym in synonyms:
                text += '                {synonym_word} / (|{synonym_translit}|) - {synonym_translate}\n'.format(
                    synonym_word=i_synonym.synonym_word,
                    synonym_translit=i_synonym.synonym_translit,
                    synonym_translate=i_synonym.synonym_translate
                )

        if i_count == max_numbers_of_translations - 1:
            break

    return text
