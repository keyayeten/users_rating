# users_rating

API для написания постов.

Реализовано:
- регистрация
- написание постов
- голосование и рейтинг постов

Запуск локально:
1) Создать .env файл с доступами для базы Postgre
2) Запуск docker compose -f docker-compose.production.yml up
3) Выполнить миграции docker compose -f docker-compose.production.yml exec backend python manage.py migrate
4) Собрать статику docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
