### Запуск
Для запуска необходимо выполнить следующую команду:

`python ip_masks.py [путь до файла]`

`python ip_masks.py ipv4\test_case_one`

### Тесты
Для того, чтобы запустить тесты, необходимо установить следующие модули:

`pip install pytest`

`pip install pytest-cov`  (для оценки покрытия кода тестами)

Запустить тесты можно следующим образом:

`pytest --cov=ip_masks`

На данный момент покрытие составляет 88%, так как нет необходимости тестировать код в main.


Также код был собран в модуль при помощи setuptools. Собран был в отдельной папке, setup.py оставлен для наглядности.

