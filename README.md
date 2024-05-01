# Проект API_YATUBE

Yatube это веб-приложение для обмена фотографиями и комментариями. Пользователи могут создавать посты, подписываться на других пользователей, оставлять комментарии к постам и просматривать посты других пользователей. Проект предоставляет API для работы с постами, группами, комментариями и подписками.

Проект выполнен в учебных целях

## Установка

### Клонирование репозитория

```bash
git clone git@github.com:olsafron/api_final_yatube.git
cd api_final_yatube
cd yatube_api
```

### Создание и активация виртуального окружения

```bash
python -m venv env
source env/bin/activate
```
### Установка зависимостей

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### Выполнение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```
### Запуск проекта

```bash
python manage.py runserver
```


```bash
```

### Примеры запросов API

### Получение списка постов

```bash
GET /api/posts/
```

### Создание нового поста

```bash
POST /api/posts/
{
    "text": "Текст вашего поста",
    "image": "https://example.com/image.jpg",
    "group": 1
}
```

### Получение списка подписчиков

```bash
GET /api/follow/
```
### и другие...
### подробнее смотри в документации API.