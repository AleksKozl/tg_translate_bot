import database.db_func as db_func


def cut(translate_json):
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


def to_database(word, language, translate_json):
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


def pretty_text(word, language, translate_json):
    to_database(word, language, translate_json)

    text = f'Ваш перевод готов! \n'
    text += '    Варианты перевода: \n'

    for i_translation in db_func.db_get_all_translation(word=word, language=language):
        text += '        {translation_word}/(|{translation_translit}|) - {translation_translate}\n'.format(
            translation_word=i_translation.translation_word,
            translation_translit=i_translation.translation_translit,
            translation_translate=i_translation.translation_translate
        )

        for i_synonym in db_func.db_get_all_synonyms(
                translation_word=i_translation.translation_word,
                language=i_translation.translation_language
        ):
            text += ('        Синонимы:\n'
                     '                {synonym_word}/(|{synonym_translit}|) - {synonym_translate}\n').format(
                synonym_word=i_synonym.synonym_word,
                synonym_translit=i_synonym.synonym_translit,
                synonym_translate=i_synonym.synonym_translate
            )

    return text
