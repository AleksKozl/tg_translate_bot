"""

Модуль отвечает за обработку  данных (в формате JSON) полученных от запроса к 'Яндекс.Переводчику'.

Список функций:
    pretty_text - Выдает строку с переводом.

"""


def pretty_text(translate_json: dict) -> str:
    """
    Преобразует входящий словарь в более читаемый вид.

    Args:
        translate_json (dict) - Пеедаваемый словарь с результатами запроса перевода.

    Parameter:
        text (str) - Итоговая строка с переводом.

    Returns:
        str
    """

    text = f'Ваш перевод готов! \n\n'

    for i_translate in translate_json['translations']:
        text += i_translate['text']
        detected_language = i_translate.get('detectedLanguageCode')
        if detected_language is not None:
            text += f'\n        Кажется язык Вашего текста это - "{detected_language}" '

    return text
