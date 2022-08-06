# Flower shop

**Магазин на Django** 

Был реализован следующий функционал:
- Регистрация пользователя. Унаследован от AbstractBaseUser
- Добавление товара в корзину и\или избранного в БД
- Добавление товара в корзину и\или избранного с помощью Django Sessions
- Скидочная система
- Характеристики товара
- Настройка личного кабинета
- Отзывы о товаре
- Рейтинг товара
- Отправка информации о заказе по email
- Поиск товара

## Настройка

Склонируйте проект

```bash
https://github.com/Ramil2003/E-commerce-FlowerShop.git
```

Создайте виртуальное окружение
```
python3 -m venv venv
```

Активируйте его:
```
source ./venv/bin/activate
```

Установите зависимости

```bash
pip install -r requirements.txt
```

**Создайте .env файл и укажите свои значения таким переменным как:**

- SECRET_KEY
- DEBUG
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_HOST
- POSTGRES_PORT
- EMAIL_HOST_USER
- EMAIL_HOST_PASSWORD


Запустите Docker

```bash
docker-compose up --build
```

Создайте супер юзера

```bash
docker-compose exec web python3 manage.py createsuperuser
```

Установите расширение pg_trgm
```
docker-compose exec db bash
```
```
psql -U <postgres_user>
```
```
CREATE EXTENSION pg_trgm;
```
