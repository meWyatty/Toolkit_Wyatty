# 🛠️ Wyatty Suite
> Набор инструментов для ленивого (в хорошем смысле) программиста.

Эта коллекция библиотек автоматизирует рутину, чтобы вы могли сосредоточиться на логике, а не на написании геттеров.

---

## 🐍 lombok_wyatty.py
**Python-реализация концепции Project Lombok.**

### ✨ Основные возможности:
* 💎 `@Data` — Авто-создание `__init__`, геттеров, сеттеров и `ToString`.
* 🏗️ `@AllArgsConstructor` — Конструктор для всех аннотированных полей.
* 🔒 **Инкапсуляция** — Все поля автоматически становятся приватными (`__field`).
* 🖼️ `@ToString` — Красивый вывод объекта: `User(name='Nicolaus', age=13)`.
* 📦 **Configuration** — Автоматическая привязка классов к файлам настроек.

### 📋 Список декораторов модуля


| Декоратор | Иконка | Что делает? | Результат |
| :--- | :---: | :--- | :--- |
| **@DataClass** | 💎 | Комбо-декоратор | `init`, `get`, `set` и `ToString` |
| **@AllArgsConstructor** | 🏗️ | Конструктор | Генерирует `__init__` для полей |
| **@Getter** | 🔍 | Доступ на чтение | Создает методы `get_имя_поля()` |
| **@Setter** | ✍️ | Доступ на запись | Создает методы `set_имя_поля(val)` |
| **@GetterSetter** | 🔄 | Полный доступ | Геттеры и сеттеры сразу |
| **@ToString** | 🖼️ | Визуализация | Красивый `print(obj)` |
| **@UniqueIdentifier** | 🔑 | ID Класса | Добавляет неизменяемый `unique_id` |
| **@ConfigurationPackage** | 📦 | Авто-конфиг | Загружает данные из файла при старте |
| **@ConfigurationArgsPackage**| 💾 | Живой конфиг | Загрузка + метод `.save()` для записи |
| **@Validated** | 🛡️ | Строгая типизация | Сеттеры проверяют тип данных (int, str...) |
| **@Singleton** | 🔄 | Один экземпляр | Гарантирует создание только одного объекта |
| **@LogExecution** | ⏱️ | Логирование | Пишет в консоль время и аргументы вызова |
| **@Deprecated** | 🛑 | Устаревший код | Выводит предупреждение при вызове метода |
| **@Secret** | 🔒 | Скрывает данные | Маскирует поле *** в ToString и логах |
| **@Final** | 🛑 | Запрет наследования | Запрещает создавать подклассы от этого класса |

---

## 🛠️ Примеры новых инструментов

### 🛡️ @Validated (Безопасность типов)
Теперь нельзя случайно записать строку в поле для чисел.
```python
@Validated
@Data
class Profile:
    Age: int

p = Profile(Age=20)
p.set_Age("Тридцать")  # 🚨 Ошибка: TypeError (ожидался int)
```

### 🔄 @Singleton (Единство данных)
Идеально для подключения к БД или глобальных настроек.
```python
@Singleton
class Database:
    def __init__(self):
        self.connection = "Connected"

db1 = Database()
db2 = Database()
print(db1 is db2)  # ✅ True (это один и тот же объект)
```

### 🔒 @Secret (Безопасность логов)
Теперь пароли и токены не утекут в консоль при обычном print().
```python
@Data
class Connection:
    Host: str = "127.0.0.1"
    @Secret('Password')
    Password: str = "admin_qwerty"

# Вывод: Connection(Host='127.0.0.1', Password='********')
```

### 🛑 @Final (Защита архитектуры)
Гарантирует, что никто не сможет изменить логику базового конфига через наследование.
```python
@Final
class SecureConfig:
    pass

class MyConfig(SecureConfig): # 🚨 Ошибка: TypeError!
    pass
```

### ⏱️ @LogExecution (Отладка)
Автоматически отслеживает работу ваших методов.
```python
class TaskManager:
    @LogExecution
    def process_data(self, data):
        # В консоли: 🚀 Вызов: process_data | Аргументы: ('some_data',)
        return len(data)
```

### 🛑 @Deprecated (Уведомления)
Помогает плавно обновлять код, не ломая его сразу.
```python
@Deprecated("используйте новый метод fast_save()")
def old_save_method():
    pass
# ⚠️ При вызове появится предупреждение в консоли
```

## 📦 Пример работы с конфигурацией

Теперь вы можете превратить любой класс в файл настроек одной строчкой:

```python
from lombok_wyatty import ConfigurationArgsPackage, Data

# Декоратор сам создаст файл, если его нет, и загрузит данные, если он есть
@ConfigurationArgsPackage(auto_create=True, FileName='settings.package')
@Data
class AppConfig:
    Index: int = 1
    NameProfile: str = "Wyatty_User"

# Данные подтянутся из файла автоматически!
print(AppConfig.get_NameProfile()) 

# Изменяем значения в коде
AppConfig.set_Index(100)

# Сохраняем изменения обратно в файл settings.package
AppConfig.save()
``` 

## ⚙️ Установка и использование
Скачайте нужный файл (например, lombok_wyatty.py).
Положите его в корень вашего проекта.
Импортируйте функции:
```python
from lombok_wyatty import Data

@Data
class Hero:
    name: str
    power: int
```

## 🗄️ database_wyatty.py (In Progress)
**Легкая обертка для работы с БД.**
* ⚡ Подключение в одну строку.
* 🛡️ Безопасные запросы без SQL-инъекций.