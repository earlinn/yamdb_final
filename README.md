# yamdb_final (API YaMDb)

![yamdb_final workflow](https://github.com/earlinn/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## _API интернет-сервиса YaMDB для хранения рецензий на произведения_

### Описание проекта API YaMDB:

Проект YaMDb собирает рецензии пользователей на произведения. Произведения
делятся на категории: «Книги», «Фильмы», «Музыка» и другие, также произведениям
могут быть присвоены жанры. Сами произведения в YaMDb не хранятся, здесь нельзя
посмотреть фильм или послушать музыку. Зарегистрированные пользователи могут
оставить к произведениям текстовые отзывы и поставить произведению оценку в
диапазоне от одного до десяти, из пользовательских оценок формируется рейтинг
произведения. На одно произведение пользователь может оставить только один
отзыв. Также пользователи могут комментировать отзывы о произведениях.
Предусмотрен функционал для модерирования отзывов и комментариев к отзывам.
Анонимные пользователи могут просматривать описания произведений, читать отзывы
и комментарии.

Стек: Python 3.7, Django, DRF, Simple-JWT, PostgreSQL, Docker, nginx, gunicorn, 
GitHub Actions (CI/CD).

### Разработчики проекта

- [Белобоков Михаил (тимлид, разработка ресурсов Auth и Users)](https://github.com/Belobokovm)
- [Волкова Галина (разработка ресурсов Categories, Genres и Titles)](https://github.com/earlinn)
- [Гукасова Анна (разработка ресурсов Review и Comments)](https://github.com/gukasius)

### Локальный запуск приложения в контейнерах

_Важно: при работе в Linux или через терминал WSL2 все команды нужно выполнять от суперпользователя — начинайте каждую команду с sudo._

Клонировать репозиторий и перейти в корневую папку:
```
git clone git@github.com:earlinn/yamdb_final.git
cd yamdb_final
```

Перейти в папку yamdb_final/infra и создать в ней файл .env с 
переменными окружения, необходимыми для работы приложения.
```
cd infra/
```

Пример содержимого файла:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=key
EMAIL=insert_your_email@yandex.ru  # почта должна быть именно на yandex.ru
PASSWORD=your_email_password
```

Запустить docker-compose: 
```
docker-compose up -d
```
Будут созданы и запущены в фоновом режиме необходимые для работы приложения 
контейнеры (db, web, nginx).

Внутри контейнера web выполнить миграции, создать 
суперпользователя и собрать статику:
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input 
```
После этого проект должен быть доступен по адресу http://localhost/. 

### Заполнение базы данных

Файл с резервной копией базы данных находится по адресу 
yamdb_final/api_yamdb/fixtures.json
Для заполнения базы данных данными из него нужно выполнить команду:
```
docker-compose exec web python manage.py loaddata fixtures.json
```

Можно также зайти на на http://localhost/admin/, авторизоваться от имени 
суперпользователя и внести записи в базу данных через админку.

Новую резервную копию базы данных можно создать командой
```
docker-compose exec web python manage.py dumpdata > fixtures.json 
```

### Остановка контейнеров

Для остановки работы приложения можно набрать в терминале команду Ctrl+C 
либо открыть второй терминал и воспользоваться командой
```
docker-compose stop 
```
Также можно запустить контейнеры без их создания заново командой
```
docker-compose start 
```

### Документация в формате Redoc:

Чтобы посмотреть документацию API в формате Redoc, нужно локально запустить 
проект и перейти на страницу http://localhost/redoc/

### Пользовательские роли

- __Аноним__ — может просматривать описания произведений, читать отзывы 
и комментарии.
- __Аутентифицированный пользователь (user)__ — может читать всё, как и Аноним,
может публиковать отзывы и ставить оценки произведениям, может комментировать 
отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать 
свои оценки произведений. Эта роль присваивается по умолчанию каждому новому 
пользователю.
- __Модератор (moderator)__ — те же права, что и у Аутентифицированного 
пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- __Администратор (admin)__ — полные права на управление всем контентом 
проекта. Может создавать и удалять произведения, категории и жанры. 
Может назначать роли пользователям.
- __Суперюзер Django__ должен всегда обладать правами администратора, 
пользователя с правами admin. Даже если изменить пользовательскую роль 
суперюзера — это не лишит его прав администратора. Суперюзер — всегда 
администратор, но администратор — не обязательно суперюзер.

### Самостоятельная регистрация нового пользователя

1. Пользователь отправляет POST-запрос с параметрами email и username 
на эндпоинт /api/v1/auth/signup/.  
*Пример POST-запроса:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string"  
}

2. Сервис YaMDB отправляет письмо с кодом подтверждения (confirmation_code) 
на указанный адрес email.

3. Пользователь отправляет POST-запрос с параметрами username и 
confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос ему 
приходит token (JWT-токен).  
*Пример POST-запроса:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"confirmation_code": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"token": "string",  
}

4. После регистрации и получения токена пользователь может отправить 
PATCH-запрос на эндпоинт /api/v1/users/me/ и заполнить поля в своём 
профайле.  
*Пример POST-запроса:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}

### Создание пользователя администратором

1. Пользователя может создать администратор — через админ-зону сайта или 
через POST-запрос на специальный эндпоинт api/v1/users/. Письмо с кодом 
подтверждения пользователю отправлять не нужно.  
*Пример POST-запроса:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}

2. После этого пользователь должен самостоятельно отправить свой email 
и username на эндпоинт /api/v1/auth/signup/, в ответ ему должно прийти 
письмо с кодом подтверждения.

3. Далее пользователь отправляет POST-запрос с параметрами username и 
confirmation_code на эндпоинт /api/v1/auth/token/, в ответе на запрос 
ему приходит token (JWT-токен), как и при самостоятельной регистрации.

### Ресурсы API YaMDb

- Ресурс __auth__: аутентификация.
- Ресурс __users__: пользователи.
- Ресурс __titles__: произведения, к которым пишут отзывы (определённый фильм, 
книга или песенка).
- Ресурс __categories__: категории (типы) произведений («Фильмы», «Книги», 
«Музыка»).
- Ресурс __genres__: жанры произведений. Одно произведение может быть 
привязано к нескольким жанрам.
- Ресурс __reviews__: отзывы на произведения. Отзыв привязан к определённому 
произведению.
- Ресурс __comments__: комментарии к отзывам. Комментарий привязан к 
определённому отзыву.

### Примеры запросов к ресурсам API YaMDb

- Получение списка всех категорий  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/categories/  
Права доступа: Доступно без токена  
[  
&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"count": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"next": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"previous": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"results": []  
&nbsp;&nbsp;&nbsp;&nbsp;}  
]

- Добавление новой категории  
*Пример POST-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/categories/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
}

- Удаление категории  
*Пример DELETE-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/categories/{slug}/  
Права доступа: Администратор

- Получение списка всех жанров  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/genres/  
Права доступа: Доступно без токена  
[  
&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"count": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"next": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"previous": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"results": []  
&nbsp;&nbsp;&nbsp;&nbsp;}  
]

- Добавление жанра  
*Пример POST-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/genres/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
}

- Удаление жанра  
*Пример DELETE-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/genres/{slug}/  
Права доступа: Администратор

- Получение списка всех произведений  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/  
Права доступа: Доступно без токена  
[  
&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"count": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"next": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"previous": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"results": []  
&nbsp;&nbsp;&nbsp;&nbsp;}  
]

- Добавление произведения  
*Пример POST-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"year": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"description": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"genre": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"string"  
&nbsp;&nbsp;&nbsp;&nbsp;],  
&nbsp;&nbsp;&nbsp;&nbsp;"category": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"year": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"rating": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"description": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"genre": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}  
&nbsp;&nbsp;&nbsp;&nbsp;],  
&nbsp;&nbsp;&nbsp;&nbsp;"category": {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

- Получение информации о произведении  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{titles_id}/  
Права доступа: Доступно без токена  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"year": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"rating": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"description": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"genre": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}  
&nbsp;&nbsp;&nbsp;&nbsp;],  
&nbsp;&nbsp;&nbsp;&nbsp;"category": {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

- Частичное обновление информации о произведении  
*Пример PATCH-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{titles_id}/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"year": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"description": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"genre": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"string"  
&nbsp;&nbsp;&nbsp;&nbsp;],  
&nbsp;&nbsp;&nbsp;&nbsp;"category": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"year": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"rating": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"description": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"genre": [  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{}  
&nbsp;&nbsp;&nbsp;&nbsp;],  
&nbsp;&nbsp;&nbsp;&nbsp;"category": {  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"slug": "string"  
&nbsp;&nbsp;&nbsp;&nbsp;}  
}

- Удаление произведения  
*Пример DELETE-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{titles_id}/  
Права доступа: Администратор

- Получение списка всех отзывов  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/  
Права доступа: Доступно без токена  
[  
&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"count": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"next": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"previous": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"results": []  
&nbsp;&nbsp;&nbsp;&nbsp;}  
]

- Добавление нового отзыва  
*Пример POST-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/  
Права доступа: Аутентифицированные пользователи  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"score": 1  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"author": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"score": 1,  
&nbsp;&nbsp;&nbsp;&nbsp;"pub_date": "2019-08-24T14:15:22Z"  
}

- Получение отзыва по id  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/  
Права доступа: Доступно без токена  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"author": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"score": 1,  
&nbsp;&nbsp;&nbsp;&nbsp;"pub_date": "2019-08-24T14:15:22Z"  
}

- Частичное обновление отзыва по id  
*Пример PATCH-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/  
Права доступа: Автор отзыва, модератор или администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"score": 1  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"author": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"score": 1,  
&nbsp;&nbsp;&nbsp;&nbsp;"pub_date": "2019-08-24T14:15:22Z"  
}

- Удаление отзыва по id  
*Пример DELETE-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/  
Права доступа: Автор отзыва, модератор или администратор

- Получение списка всех комментариев к отзыву  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/  
Права доступа: Доступно без токена  
[  
&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"count": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"next": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"previous": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"results": []  
&nbsp;&nbsp;&nbsp;&nbsp;}  
]

- Добавление комментария к отзыву  
*Пример POST-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/  
Права доступа: Аутентифицированные пользователи  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"author": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"pub_date": "2019-08-24T14:15:22Z"  
}

- Получение комментария к отзыву  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/  
Права доступа: Доступно без токена  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"author": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"pub_date": "2019-08-24T14:15:22Z"  
}

- Частичное обновление комментария к отзыву  
*Пример PATCH-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/  
Права доступа: Автор комментария, модератор или администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"id": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;"text": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"author": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"pub_date": "2019-08-24T14:15:22Z"  
}

- Удаление комментария к отзыву  
*Пример DELETE-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/  
Права доступа: Автор комментария, модератор или администратор

- Получение списка всех пользователей  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/users/  
Права доступа: Администратор  
[  
&nbsp;&nbsp;&nbsp;&nbsp;{  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"count": 0,  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"next": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"previous": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"results": []  
&nbsp;&nbsp;&nbsp;&nbsp;}  
]

- Добавление пользователя  
*Пример POST-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/users/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}

- Получение пользователя по username  
*Пример ответа на GET-запрос:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/users/{username}/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}

- Изменение данных пользователя по username  
*Пример PATCH-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/users/{username}/  
Права доступа: Администратор  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}  
*Пример ответа:*  
{  
&nbsp;&nbsp;&nbsp;&nbsp;"username": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"email": "user@example.com",  
&nbsp;&nbsp;&nbsp;&nbsp;"first_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"last_name": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"bio": "string",  
&nbsp;&nbsp;&nbsp;&nbsp;"role": "user"  
}

- Удаление пользователя по username  
*Пример DELETE-запроса:*  
Эндпойнт: http://127.0.0.1:8000/api/v1/users/{username}/  
Права доступа: Администратор

### Планы про доработке проекта

Исправить:
- POST-запрос на эндпойнт http://localhost/api/v1/auth/signup/ для получения 
  confirmation code на email в случае регистрации данного пользователя админом
  (сейчас ответ: {"username":["A user with that username already exists."],"email":["email уже зарегистрирован"]})  
[Адрес для проверки работоспособности проекта](http://130.193.52.90/)
