# Приложение Config

Приложение для управления настраиваемыми параметрами сайта.

## Возможности

### 1. Управление никами для добавления в друзья
- Создание, редактирование и удаление ников
- Указание платформы (Fortnite, CS:GO и т.д.)
- Активация/деактивация ников
- Автоматическое отключение других ников при активации нового

### 2. Общие настройки сайта
- Гибкая система ключ-значение для любых параметров
- Описание для каждого параметра
- Отслеживание изменений

## Установка и настройка

### 1. Добавление в INSTALLED_APPS
Приложение уже добавлено в `core/settings/base.py`

### 2. Создание миграций
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Инициализация начальных данных
```bash
python manage.py init_config
```

### 4. Создание суперпользователя (если еще не создан)
```bash
python manage.py createsuperuser
```

## Использование

### В админке Django
1. Перейдите в `/admin/`
2. Войдите с учетными данными суперпользователя
3. Найдите раздел "Настройки сайта"
4. Управляйте никами и другими параметрами

### В коде Python
```python
from apps.config.models import FriendNickname, SiteConfig

# Получить активный ник
nickname = FriendNickname.get_active_nickname()
if nickname:
    print(f"Активный ник: {nickname.nickname}")

# Получить значение параметра
value = SiteConfig.get_value('some_key', 'default_value')

# Установить значение параметра
SiteConfig.set_value('some_key', 'new_value', 'Описание параметра')
```

### В API
```bash
# Получить активный ник
GET /api/config/nickname/
```

## Структура файлов

```
apps/config/
├── __init__.py
├── admin.py          # Админка Django
├── api_views.py      # API views
├── api_urls.py       # URL маршруты для API
├── apps.py           # Конфигурация приложения
├── models.py         # Модели данных
├── migrations/       # Миграции базы данных
└── management/       # Команды Django
    └── commands/
        └── init_config.py
```

## Безопасность

- Доступ к админке только для суперпользователей
- API endpoint для получения ника доступен всем (только чтение)
- Валидация данных на уровне моделей Django 