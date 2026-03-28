"""
    🐍 lombok_wyatty.py — Python-реализация концепции Project Lombok.

    ✨ Версия: 2.0 (Config Update)
    👤 Автор: wyatty

    📦 Эта библиотека автоматизирует создание конструкторов, геттеров, сеттеров
    и строковых представлений, а также управление файлами конфигурации.

    [ ----------------------------- 🛠️ ------------------------------- ]
    @AllArgsConstructor / @DataClass (или @Data)
    🚀 Автоматизируют создание __init__ и методов доступа. 
    🔒 Все поля преобразуются в ПРИВАТНЫЕ (self.__field) через механизм Name Mangling.
    
    [ ----------------------------- 🔍 ------------------------------- ]
    @Getter / @Setter / @GetterSetter (*fields)
    📖 Генерируют методы get_field() и set_field(value) для доступа к приватным данным.

    [ ----------------------------- 🆔 ------------------------------- ]
    @UniqueIdentifier(value)
    🔑 Добавляет классу неизменяемый уникальный идентификатор и метод get_unique_id().

    [ ----------------------------- 📄 ------------------------------- ]
    @ConfigurationPackage(auto_create=True, FileName='config.package')
    📦 Статический конфигуратор. 
    При инициализации читает файл и заполняет объект данными. 
    Если файла нет и auto_create=True — создает его с дефолтными значениями.

    Пример файла: 
    Index=1
    NameProfile="asdasd"

    [ ----------------------------- 💾 ------------------------------- ]
    @ConfigurationArgsPackage(auto_create=True, FileName='config.package')
    ⚙️ Продвинутый конфигуратор. 
    Делает то же самое, что и ConfigurationPackage, но добавляет объекту 
    метод .save(), который позволяет в любой момент сохранить текущее 
    состояние объекта обратно в файл.

    Пример:
    config = MyConfig()
    config.Index = 10
    config.save()  # Обновит файл на диске
"""

import os
import functools

from dataclasses import dataclass, fields

def _create_methods(cls, fields, add_getter=False, add_setter=False):
    original_init = cls.__init__

    @functools.wraps(original_init)
    def new_init(self, *args, **kwargs):
        original_init(self, *args, **kwargs)
        for field in fields:
            # Учитываем манглинг: _ClassName__field
            clean_name = field.lstrip('_')
            mangled_name = f"_{cls.__name__}__{clean_name}"
            
            if add_getter:
                method_name = f"get_{clean_name}"
                if not hasattr(cls, method_name):
                    setattr(cls, method_name, lambda self, name=mangled_name: getattr(self, name))
            
            if add_setter:
                method_name = f"set_{clean_name}"
                if not hasattr(cls, method_name):
                    setattr(cls, method_name, lambda self, val, name=mangled_name: setattr(self, name, val))

    cls.__init__ = new_init
    return cls

def AllArgsConstructor(cls):
    annotations = getattr(cls, '__annotations__', {})
    def __init__(self, *args, **kwargs):
        arg_names = list(annotations.keys())
        for i, value in enumerate(args):
            kwargs[arg_names[i]] = value
        for name, value in kwargs.items():
            mangled_name = f"_{cls.__name__}__{name.lstrip('_')}"
            setattr(self, mangled_name, value)
    cls.__init__ = __init__
    return cls

def ToString(cls):
    def to_string_logic(self):
        fields = getattr(cls, '__annotations__', {}).keys()
        values = []
        for f in fields:
            mangled = f"_{cls.__name__}__{f.lstrip('_')}"
            val = getattr(self, mangled, "N/A")
            values.append(f"{f}={repr(val)}")
        return f"{cls.__name__}({', '.join(values)})"
    
    cls.ToString = to_string_logic
    cls.__repr__ = to_string_logic
    cls.__str__ = to_string_logic
    return cls

def Getter(*fields): 
    return lambda cls: _create_methods(cls, fields, add_getter=True)
def Setter(*fields): 
    return lambda cls: _create_methods(cls, fields, add_setter=True)
def GetterSetter(*fields): 
    return lambda cls: _create_methods(cls, fields, add_getter=True, add_setter=True)

def UniqueIdentifier(value: str):
    def decorator(cls):
        original_init = cls.__init__

        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            mangled_name = f"_{cls.__name__}__UniqueIdentifier"
            setattr(self, mangled_name, value)
            
            if not hasattr(cls, "get_unique_id"):
                setattr(cls, "get_unique_id", lambda self, n=mangled_name: getattr(self, n))
            
            original_init(self, *args, **kwargs)

        cls.__init__ = new_init
        return cls
    return decorator

def DataClass(cls):
    cls = AllArgsConstructor(cls)
    cls = ToString(cls)
    fields = list(getattr(cls, '__annotations__', {}).keys())
    return _create_methods(cls, fields, add_getter=True, add_setter=True)

def ConfigurationPackage(auto_create=True, FileName='configuration.package'):
    def wrapper(cls):
        cls = dataclass(cls)
        
        config_data = {}
        if os.path.exists(FileName):
            with open(FileName, 'r') as f:
                for line in f:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        value = value.strip('"')
                        if key in cls.__annotations__:
                            target_type = cls.__annotations__[key]
                            config_data[key] = target_type(value)

        instance = cls(**config_data) if config_data else cls()
        
        if auto_create and not os.path.exists(FileName):
            with open(FileName, 'w') as f:
                for field in cls.__annotations__:
                    val = getattr(instance, field, None)
                    f.write(f'{field}={repr(val) if isinstance(val, str) else val}\n')
        
        return instance
    return wrapper

def ConfigurationArgsPackage(auto_create=True, FileName='configuration.package'):
    def wrapper(cls):
        cls = dataclass(cls)

        def save(self):
            with open(FileName, 'w', encoding='utf-8') as f:
                for field in fields(self):
                    val = getattr(self, field.name)
                    formatted_val = f'"{val}"' if isinstance(val, str) else val
                    f.write(f'{field.name}={formatted_val}\n')

        cls.save = save

        init_data = {}
        if os.path.exists(FileName):
            with open(FileName, 'r', encoding='utf-8') as f:
                for line in f:
                    if '=' in line:
                        key, val = map(str.strip, line.split('=', 1))
                        if key in cls.__annotations__:
                            val = val.strip('"')
                            init_data[key] = cls.__annotations__[key](val)

        instance = cls(**init_data)

        if auto_create and not os.path.exists(FileName):
            instance.save()

        return instance
    return wrapper

Data = DataClass
SetterGetter = GetterSetter

if __name__ == "__main__":
    @DataClass
    class Nicolaus:
        name: str
        age: int

    me = Nicolaus("Nicolaus", 13)
    print(me.ToString())        # Явный вызов
    me.set_age(14)              # Сеттер работает
    print(f"Happy Birthday! New age: {me.get_age()}")
    print(me)                   # Авто-вывод через __str__

    @ConfigurationArgsPackage(auto_create=True, FileName='configuration.package')
    class Configuration:
        Index: int = 0
        NameProfile: str = "default"
    
    print(Configuration.Index)
    print(Configuration.NameProfile)


    Configuration.Index=33
    Configuration.save()