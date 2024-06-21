"""

Модуль отвечает за обработку  данных (в формате JSON) полученных от запроса к 'Яндекс.Переводчику'.

Список функций:
    pretty_text - Выдает строку с переводом.

"""


def pretty_text(translate_json: dict, text_for_translation: str) -> tuple[str, str]:

    """
    Преобразует входящий словарь в более читаемый вид.

    Args:
        translate_json (dict) - Пеедаваемый словарь с результатами запроса перевода.
        text_for_translation (str) - Переводимый текст.

    Parameter:
        text (str) - Итоговая строка с переводом.

    Returns:
        str
    """

    text = f'Ваш перевод готов! \n\n'
    only_translate = ''

    for i_translate in translate_json['translations']:
        text += i_translate['text']
        only_translate += i_translate['text']
        if i_translate['text'] == text_for_translation:
            text += '\n\n        Кажется Вы указали неверный язык переводимого текста.'
        detected_language = i_translate.get('detectedLanguageCode')
        if detected_language is not None:
            text += f'\n\n        Кажется язык Вашего текста это - "{detected_language}".'

    return text, only_translate
