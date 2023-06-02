from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict
from dotenv import load_dotenv
import os
import datetime
import pandas

from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_products(table_filename):
    products_df = pandas.read_excel(table_filename, na_values='nan', keep_default_na=False)
    products_df.rename(columns={
        'Категория': 'category',
        'Название': 'title',
        'Сорт': 'type',
        'Цена': 'price',
        'Картинка': 'image',
        'Акция': 'promotion'
    }, inplace=True)
    products = products_df.to_dict('records')
    sorted_products = defaultdict(list)
    for product in products:
        key = product['category']
        features = {
            'title': product['title'],
            'type': product['type'],
            'price': product['price'],
            'image': product['image'],
            'promotion': product['promotion']
        }
        sorted_products[key] += [features]
    return sorted_products


def calculate_years_from_founding():
    foundation_year = 1920
    year_now = datetime.datetime.now()
    return year_now.year - foundation_year


def calculate_word(worktime):
    exception_numbers = [11, 12, 13, 14]
    if len(str(worktime)) >= 2 and str(worktime)[-2:] in exception_numbers:
        return 'лет'
    elif str(worktime)[-1] == '1':
        return 'год'
    elif str(worktime)[-1] in ('2', '3', '4'):
        return 'года'
    else:
        return 'лет'


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    worktime = calculate_years_from_founding()
    year_word = calculate_word(worktime)
    table_filename = os.getenv('TABLE_FILENAME', default='wine-example.xlsx')

    rendered_page = template.render(
        products=get_products(table_filename),
        worktime=worktime,
        year_word=year_word
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
