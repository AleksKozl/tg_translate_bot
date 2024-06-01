def cut(translate_json):
    text = dict()
    for i_def in translate_json['def']:

        for i_trans in i_def['tr']:

            try:
                text[i_trans['text']] = dict()

                means = [i_means['text'] for i_means in i_trans['mean']]
                text[i_trans['text']]['means'] = '; '.join(means)

                synonyms = [i_synonym['text'] for i_synonym in i_trans['syn']]
                text[i_trans['text']]['synonyms'] = '; '.join(synonyms)

            except KeyError:
                continue

    return text


def pretty_translate(translate_json):
    buf_dict = cut(translate_json)

    text = 'Варианты перевода:\n'

    for i_key in buf_dict.keys():
        try:
            text += f'    {i_key} - {buf_dict[i_key]['means']}\n'
            text += f'        Синонимы: {buf_dict[i_key]['synonyms']}\n'
        except KeyError:
            continue

    return text
