# Веб-сервис с загрузкой изображения и информацией о цветах изображения #

Сервис поддерживает загрузку изображений через веб-форму (или post-запросом), _(синхронно - место для улучшения)_ вычисляет количество пикселей уникальных цветов и хранит информацию в базе данных. Логи ответов пишет в консоль.
Умеет сообщать:
- Каких пикселей больше - чёрных или белых?
- Сколько пикселей конкретного цвета?

## Запуск ##

### Установка и запуск через Docker ###

Скачайте код с GitHub и перейдите в папку с проектом.

  ```sh
  git clone https://github.com/n1k0din/pixel-hunter
  ```

Запустите и наслаждайтесь по адресу сервера, порт 8000.

  ```sh
  docker-compose up --build
  ```

### Установка и запуск вручную ###

#### Установка файлов проекта ####

Скачайте код с GitHub и перейдите в папку с проектом.

  ```sh
  git clone https://github.com/n1k0din/pixel-hunter
  ```

Установите вирт. окружение.
  ```sh
  python -m venv venv
  ```

Активируйте.
  ```sh
  venv\Scripts\activate.bat
  ```
  или
  ```bash
  source venv/bin/activate
  ```

Установите необходимые пакеты.
  ```sh
  pip install -r requirements.txt
  ```

#### Создание и инициализация БД ####

- Создайте базу данных `postgresql` и пользователя `pixelhunter` (по-умолчанию) (или укажите uri к существующей в конфигурационном файле `local.yaml`).

- При помощи `psql`, `pgadmin` и т.п. создайте таблицу в БД (`init.sql`):
  ```sql
  CREATE TABLE public.image_color
  (
      id character varying(224) COLLATE pg_catalog."default" NOT NULL,
      colors json NOT NULL,
      CONSTRAINT image_color_pkey PRIMARY KEY (id)
  )

  TABLESPACE pg_default;

  ALTER TABLE public.image_color
      OWNER to pixelhunter;
  ```


## Конфигурация ##

### Параметры командной строки ###

- `--host` адрес хоста, `0.0.0.0` по-умолчанию
- `--port` порт, `8080` по-умолчанию
- `-c` или `--config` путь к локальному `yaml` файлу конфигурации

### Файлы конфигруации ###
Настройки по-умолчанию хранятся в `pixel_hunter/config.yaml`, путь к локальному можно указать в параметре командной строки.
Параметры файлов конфигурации.

- `db_uri`
  ```
  db_uri: postgresql://pixelhunter:pixelhunter@db/pixelhunter
  ```

- `static_dir` - локальный путь к папке со статикой - если нужен `bootstrap` и `colorpicker`.

#### Запуск ####

```sh
python entry.py
```

```sh
python entry.py --host localhost --port 8000 -c local.yaml
```



## Цели проекта
Вступительное задание в в школу Информационных и Финансовых Технологий «ШИФТ» ЦФТ.
