from src.hh_api import HHApi
from src.json_saver import JSONSaver
from src.utils import print_vacancies

print("1====================")
text = "python"
hh = HHApi()
vacs = hh.get_vacancies(text)
# print(vacs)

print("2====================")
js = JSONSaver()
js.write_vacancies(vacs)

print("3====================")
vacancies = js.get_vacancies()
print_vacancies(vacancies)