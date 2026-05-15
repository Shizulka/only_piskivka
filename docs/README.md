# Only Piskivka — веб-застосунок для відгуків селища Пісківка

### Короткий опис
**Only Piskivka** — це веб-застосунок для створення та перегляду відгуків про заклади та локації в селищі Пісківка. Проєкт реалізований як REST API, що дозволяє користувачам реєструватися,переглядати мапу селища Пісківка, знаходити цікаві місця та ділитися своїм досвідом через систему відгуків. Адміністратор може додавати/прибирати місця та модерувати відгуки і у випадку більше трьох попереджень користувач вимушений бути забаненим.

### Технологічний стек
* **Мова програмування:** Python
* **Framework & Server:** FastAPI та Uvicorn
* **База даних:** PostgreSQL
* **ORM:** SQLAlchemy
* **Валідація даних:** Pydantic
* **Автентифікація та безпека:** OAuth2 (Password Bearer), JWT (JSON Web Tokens) та bcrypt (через Passlib)
* **Тестування:** Pytest

### Архітектура проекту

1.  **Domain Layer (`src/domain`)**: Ядро системи. Містить бізнес-сутністі (Entities), об'єкти-значення (Value Objects), інтерфейси репозиторіїв та фабрики для створення об'єктів з перевіркою інваріантів.
2.  **Application Layer (`src/application`)**: Містить сервіси, які реалізують сценарії використання (Use Cases), такі як реєстрація користувача або створення відгуку.
3.  **Infrastructure Layer (`src/infrastructure`)**: Реалізація взаємодії з БД, ORM-моделі, схеми Pydantic, мапери для конвертації даних між шарами та конфігурація додатка.
4.  **Presentation Layer (`src/presentation`)**: API-контролери (ендпоінти), що обробляють HTTP-запити та повертають відповіді.

**Структура проекту:**
```text
only_piskivka/
├── src/
│   ├── domain/                  # Бізнес-логіка (Сутності, Value Objects, Інтерфейси)
│   │   ├── entities.py          # Доменні моделі (User, Place, Review)
│   │   ├── exceptions.py        # Доменні помилки (DomainError)
│   │   ├── factory.py           # Фабрики для створення об'єктів
│   │   ├── interfaces.py        # Порти (абстрактні репозиторії)
│   │   └── value_objects.py     # Об'єкти-значення (Email, TimeRange)
│   ├── application/             # Сервіси (Сценарії використання)
│   │   ├── service_place.py     # Use cases для локацій
│   │   ├── service_review.py    # Use cases для відгуків
│   │   └── service_user.py      # Use cases для користувачів
│   ├── infrastructure/          # Реалізація інфраструктури (Адаптери)
│   │   ├── repository/          # Реалізація репозиторіїв
│   │   │   ├── repo_place.py
│   │   │   ├── repo_review.py
│   │   │   └── repo_user.py
│   │   ├── database.py          # Налаштування SQLAlchemy та сесії
│   │   ├── dependencies.py      # Залежності FastAPI
│   │   ├── main.py              # Точка входу в додаток
│   │   ├── mappers.py           # Мапінг Domain <-> DB
│   │   ├── models.py            # ORM-моделі БД
│   │   └── schemas.py           # DTO (Pydantic схеми)
│   ├── presentation/            # API-контролери (Роутери)
│   │   ├── control_place.py     # Ендпоінти локацій
│   │   ├── control_review.py    # Ендпоінти відгуків
│   │   └── control_user.py      # Ендпоінти користувачів
│   ├── security/                # Безпека (bcrypt та JWT)
│   │   └── get_password_hash.py # Хешування та токени
│   └── tests/                    # Тести
│       ├── conftest.py           # Конфігурація та фікстури Pytest
│       ├── test_entities.py      # Тести доменних сутностей
│       ├── test_factories.py     # Тести фабрик (інваріанти)
│       ├── test_routes_place.py  # Тести API-ендпоінтів місць
│       ├── test_routes_review.py # Тести API-ендпоінтів відгуків
│       ├── test_routes_user.py   # Тести API-ендпоінтів користувачів
│       ├── test_security.py      # Тести безпеки (хешування, JWT)
│       ├── test_services.py      # Тести сервісів (Use Cases)
│       └── test_value_objects.py # Тести об'єктів-значень
├── docs/                        
├── .env                         
├── .gitignore                   
└── report.md                    
```

### Project Setup

Перед запуском проекту встановіть всі необхідні бібліотеки
1. **Встановіть залежності:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Запустіть проект:**
   ```bash
   uvicorn src.infrastructure.main:app --reload
   ```

### Запуск тестів

1. **Встановіть бібліотеку pytest для тестування:**
   ```bash
   pip install pytest
   ```

2. **Встановіть плагін для покриття коду тестами:**
   ```bash
   pip install pytest-cov
   ```

2. **Запуск самих тестів:**
   ```bash
   python -m pytest src/tests/
   ```