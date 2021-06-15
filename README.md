# Парсер сайта OLX
Скрипт парсит выбранную рубрику, сайта olx c доменами .kz и .ua, после чего сохранит все в файл "advert.txt", на рабочем столе.
### Использование
Для парсинга используется браузер Google Chrome и Selenium
* Скачать [WebDriver for Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)
* Изменить переменную ```chrome_path``` на 13 строке, указав путь к ```chromedriver.exe```
* На 16 строке, в переменную ```base_url``` вписать ссылку на рубрику, которую хотим спарсить

### Установка библиотек
* [python 3.7+](https://www.python.org/)
* ```pip install -r requirements.txt``` 

### Запуск
```python parser.py```
