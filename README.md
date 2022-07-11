[![Yamdb-final-workflow](https://github.com/ananatereshonok/yamdb_final/workflows/YAMDB-workflow/badge.svg)](https://github.com/ananatereshonok/yamdb_final/actions)

# REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. 

Проект YaMDb собирает отзывы (*Review*) пользователей на произведения (*Title*). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (*Category*) может быть расширен (например, можно добавить категорию *«Изобразительное искусство»* или *«Ювелирка»*).

Сами произведения в YaMDb не хранятся, **здесь нельзя посмотреть фильм или послушать музыку**.

В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха. Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.

Благодарные или возмущённые читатели оставляют к произведениям текстовые отзывы (*Review*) и выставляют произведению рейтинг (оценку в диапазоне от одного до десяти). Из множества оценок автоматически высчитывается средняя оценка произведения.

## Начало работы

1. Клонируйте репозиторий на локальную машину.
```
git clone git@github.com:ananatereshonok/yamdb_final.git
```
2. Для работы с проектом локально - зайдите в папку с проектом, установите вирутальное окружение и восстановите зависимости.
```
python -m venv venv
pip install -r api_yamdb/requirements.txt 
```
### Подготовка удаленного сервера для развертывания приложения

Для работы с проектом на удаленном сервере должен быть установлен Docker и [docker-compose](https://docs.docker.com/engine/install/ubuntu/).

### Подготовка репозитория на GitHub

Для использования Continuous Integration и Continuous Deployment необходимо в репозитории на GitHub прописать Secrets - переменные доступа к вашим сервисам.
Переменые прописаны в workflows/yamdb_workflow.yaml

* DOCKER_PASSWORD, DOCKER_USERNAME, DOCKER_REPOSITORY - для загрузки и скачивания образа с репозитория DockerHub 
* DB_ENGINE, DB_HOST, DB_NAME, DB_PORT, POSTGRES_PASSWORD, POSTGRES_USER - для подключения к базе данных 
* SECRET_KEY проекта
* SSH_KEY, USER, HOST, PASSPHRASE, SSH_KEY - для подключения к удаленному серверу 
* TELEGRAM_TO, TELEGRAM_TOKEN - для отправки сообщений в Telegram

## Технологии используемые в проекте
Python, Django, Django REST Framework, PostgreSQL, Nginx, Docker, GitHub Actions

## Адреса приложения

* [http://ip/api/v1/](http://51.250.99.140/api/v1/)
* [http://ip/admin](http://51.250.99.140/admin/)
* [http://51.250.99.140/redoc/](http://51.250.99.140/redoc/)
