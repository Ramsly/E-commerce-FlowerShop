# Flower shop

**Магазин на Django** 

Был реализован следующий функционал:
- Регистрация пользователя. Унаследован от AbstractBaseUser
- Добавление товара в корзину и\или избранного в БД
- Добавление товара в корзину и\или избранного с помощью Django Sessions
- Скидочная система
- Характеристики товара
- Настройка личного кабинета

## Настройка

Склонируйте проект

```bash
https://github.com/Ramil2003/E-commerce-FlowerShop.git
```

Создайте виртуальное окружение
```
python3 -m venv venv
```

Установите зависимости

```bash
pip install -r requirements.txt
```

Запустите Docker

```bash
docker-compose build
```
```bash
docker-compose up
```

Сделайте миграции

```bash
docker-compose exec web python manage.py migrate
```
