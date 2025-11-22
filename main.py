from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import collections

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
	grouped_wine = collections.defaultdict(list)

	excel_wine = pandas.read_excel('wine3.xlsx')
	excel_wine = excel_wine.fillna('')
	wine = excel_wine.to_dict(orient='records')

	for i in wine:
		kategoria = i["Категория"]
		grouped_wine[kategoria].append(i)

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
		wines=grouped_wine
	)

	with open("index.html", "w", encoding="utf-8") as file:
	    file.write(rendered)

	server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
	server.serve_forever()

if __name__ == '__main__':
	main()


