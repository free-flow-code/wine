from http.server import HTTPServer, SimpleHTTPRequestHandler
from collections import defaultdict
import datetime
import pandas
import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')


def get_products():
    products_df = pandas.read_excel('wine.xlsx', na_values='nan', keep_default_na=False)
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
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(sorted_products)
    return sorted_products


def counting_years_from_founding():
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


worktime = counting_years_from_founding()
year_word = calculate_word(worktime)

rendered_page = template.render(
    products=get_products(),
    worktime=worktime,
    year_word=year_word
)


def main():
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
