from src.hh_api import HHApi
from src.json_saver import JSONSaver
from src.utils import print_vacancies

text = "python"
hh = HHApi()
vacs = hh.get_vacancies(text)

js = JSONSaver()
js.write_vacancies(vacs)

vacancies = js.get_vacancies()
print_vacancies(vacancies)