### Как запустить проект:


Клонировать репозиторий и перейти в него в командной строке:
 - Linux:
```
git clone https://github.com/kda99/api_final_yatube.git
```
 - Windows
```
venv/Scripts/activate
```
```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate # у меня windows нет
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

Часто используемые запросы:

```
GET api/v1/posts/ - Получение публикаций
POST api/v1/posts/ - Создание публикаций
GET api/v1/posts/{id}/ - Получение публикации
GET /api/v1/posts/{post_id}/comments/ - Получение комментария
POST /api/v1/posts/{post_id}/comments/ - Создание комментария
```