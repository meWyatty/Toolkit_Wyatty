"""
    🐍 lombok_wyatty.py — Python-реализация концепции Project Lombok.

    ✨ Версия: 1.0
    👤 Автор: wyatty

    📦 Эта библиотека автоматизирует создание конструкторов, геттеров, сеттеров
    и строковых представлений, обеспечивая инкапсуляцию через приватные поля (__field).

    [ ----------------------------- 💎 ------------------------------- ]
    @DataClass (или @Data)
    🚀 Комбо-декоратор: создает __init__, методы ToString, Getter и Setter для всех полей.
    
    Пример:
    @DataClass
    class User:
        name: str
        age: int
    
    ⚙️ Создаст: __init__(name, age), get_name(), set_name(), get_age(), set_age(), ToString()
    
    [ ----------------------------- 🏗️ ------------------------------- ]
    @AllArgsConstructor
    🛠️ Автоматически создает конструктор __init__ на основе аннотаций типов.
    🔒 Все поля сохраняются как ПРИВАТНЫЕ (self.__field).

    Пример:
    @AllArgsConstructor
    class Test:
        name: str
        age: int
    
    ✅ Можно создать объект: test = Test('Nicolaus', 13)
    
    [ ----------------------------- 🔍 ------------------------------- ]
    @Getter(*fields)
    📖 Создает геттеры для указанных приватных полей в формате: get_field().

    Пример:
    @Getter('name', 'age')
    class Test:
        def __init__(self, name):
            self.__name = name
    
    [ ----------------------------- ✍️ ------------------------------- ]
    @Setter(*fields)
    📝 Создает сеттеры для указанных приватных полей в формате: set_field(value).

    [ ----------------------------- 🔄 ------------------------------- ]
    @GetterSetter(*fields)
    🔁 Создает и геттеры, и сеттеры для указанных полей одновременно.

    [ ----------------------------- 🖼️ ------------------------------- ]
    @ToString
    📺 Добавляет метод ToString() и поддержку print(obj), выводя содержимое всех полей.
    
    💡 Пример вывода: User(name='Nicolaus', age=13)
"""

import functools

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

def DataClass(cls):
    cls = AllArgsConstructor(cls)
    cls = ToString(cls)
    fields = list(getattr(cls, '__annotations__', {}).keys())
    return _create_methods(cls, fields, add_getter=True, add_setter=True)

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