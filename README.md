# Новое русское вино

Сайт магазина авторского вина "Новое русское вино".

## Запуск

- Скачайте код
- Установите необходимые библиотеки командой:
  ```
  pip install -r requirements.txt
  ```
- Рядом с файлом `main.py` создайте `.env`-файл с переменной окружения:
  ```
  TABLE_FILENAME=you_table.xlsx
  ```
- Скрипт берет данные из `.xlsx` таблицы. Расположите ее рядом с файлом `main.py`. В файле `wine-example.xlsx`
  можно посмотреть пример структуры таблицы.
- Файлы изображений для товаров хранятся в директории `images/`  
- Запустите сайт командой:
  ```
  python3 main.py
  ```
- Перейдите на сайт по адресу [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
