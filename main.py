from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections
import argparse


FOUNDING_YEAR = 1920


def choose_year_word(age):
    last_two = age % 100
    last_one = age % 10

    if 11 <= last_two <= 14:
        return "лет"
    if last_one == 1:
        return "год"
    if 2 <= last_one <= 4:
        return "года"
    return "лет"


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument(
		"--wine", 
		default="products.xlsx"
		)
	args = parser.parse_args()

	excel_wines = pandas.read_excel(args.wine)
	excel_wines = excel_wines.fillna('')
	wines = excel_wines.to_dict(orient='records')
	grouped_wines = collections.defaultdict(list)

	for product in wines:
		kategoria = product["Категория"]
		grouped_wines[kategoria].append(product)

	today = datetime.datetime.now().year
	age = today - FOUNDING_YEAR

	env = Environment(
    	loader=FileSystemLoader('.'),
    	autoescape=select_autoescape(['html', 'xml'])
	)

	template = env.get_template('template.html')
	word = choose_year_word(age)

	rendered = template.render(
		age=age,
		year_word=word,
		wines=grouped_wines
	)

	with open("index.html", "w", encoding="utf-8") as file:
	    file.write(rendered)

	server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
	server.serve_forever()


if __name__ == '__main__':
	main()


