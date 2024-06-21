# Руководство пользователя. 

# *_Текущая версия -  0.5.1_*


## 1. Общая информация.

Работает с API Telegram через библиотеку "telebot".

Данный бот предназначен для перевода отдельных слов и текста на различные языки  
посредством использования возможностей сервисов "Yandex.Dictionary" и "Yandex.Translate".

## 2. Возможности бота.

### Доступные команды/сценарии:

    1. /low - Перевод отдельного слова на выбранный язык (направление перевода)
              с выдачей определенного пользователем количества вариантов перевода. 
              Резултат выводится в следующем формате:
                Слово / (|Транскрипция|) - Перевод. (С синонимами)
                    Синонимы (формат тот же)
                Слово / (|Транскрипция|) - Перевод. (Без синонимов)

    2. /high - Перевод текста на выбраный язык.
    3. /custom (в разработке) - Озвучивание перевода (возможно распознавание текста на изображении).
    4. /history (в разработке)  - Выдача истории запросов.

## 3. Roadmap.

1. [x] v.0.1 - Эхо-бот.
- Получение токена бота.
- Реализация пробных сценариев.
- Попытка создания асинхронного бота.
- Создание общей структуры проекта.

2. [x] v.0.2 - "Yandex.Dictionary"//asyncio - перевод отдельных слов.
- Получение API-ключа "Yandex.Dictionary".
- Попытка реализации асинхронного варианта сценария перевода слов.

3. [x] v.0.3 - "Yandex.Dictionary" - перевод отдельных слов, команда/сценарий "/low".
- Отказ от асинхронного кода.
- Пересборка всего проекта.
- Корректировки в структуре сценария.

4. [x] v.0.4 - Database (SQLite3/Peewee) - реализация БД.
- Создание моделей и функционала для БД.
- Совмещение работы сценария "low" и возможностей БД.
- Корректировки в структуре и внешнем виде выдаваемых пользователю результатов перевода.
- v.0.4.1 - Добавлены inline-клавиатуры для более удобного взаимодействия с ботом.  
А также возможности смены языка "внутри" сценария и выхода в главное меню.
- v.0.4.2 - Внесение небольших корректировок, исправление багов и добавление документации.
- v.0.4.3 - Добавление возможности выбора количества выдаваемых вариантов перевода.

5. [x] v.0.5 - "Yandex.Translate" - перевод текстов, команда/сценарий "/high".
- Взаимодействие с "Yandex.Cloud", создание и регистрация сервисного аккаунта,  
создание каталога и получение IAm - токена
- Получение API-ключа "Yandex.Translate".
- Реализация команды "/high".
- v.0.5.1 - Исправление багов.

6. [x] v.0.6 - Команда/сценарий "/custom" - "Yandex.Speechkit".
- Внедрение "Yandex.Speechkit" - сервиса синтеза речи (Text-to-Speech).
- Получение соответствующего API-ключа, необходимые для взаимодействия с сервисом процедуры.
- Разработка и реализация команды как самостоятельного сценария.
- Реализация команды "/custom" в качестве дополнения в сценарии "/low" и "/high".

7. [ ] v.0.7 (ВОЗМОЖНО) - Команда/сценарий "/custom" - "Yandex.VisionOCR".
- Внедрение "Yandex.VisionOCR" - сервиса распознавания текста на изображаниях.
- Получение соответствующего API-ключа, необходимые для взаимодействия с сервисом процедуры.
- Разработка и реализация команды как самостоятельного сценария.
- Внесение изменений в структуру команды/сценария "/custom",  
внедрение нового функционала.

8. [ ] v.0.8 - Команда/сценарий "/history" - история запросов.
- Внесение необходимых изменений в структуру БД.
- Редактирование других сценариев под возможность записи информации о предыдущих запросах.
- Реализация команды "/history".

9. [ ] v.0.9 - Исправление багов, "слабых мест", замечаний. Реализация команды "/help".
- Реализация команды "/help".
- Исправление багов, "слабых мест", замечаний

10. [ ] v.1 - Финальная версия.
- Внесение корректировок / исправление багов  
по результатам тестирование бОльшим количеством пользователей.
