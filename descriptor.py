# Managed attributes / 管理屬性
# descriptors 一個常用的用途是在管理存取 instance 資料。一個 descriptor 指派到 public attribute 在 class dictionary 中，而實際的資料是儲存在 instance dictionary 中的 private attribute。當 public attribute 存取時，descriptor 的 __get__() and __set__() methods 會觸發

import logging

logging.basicConfig(level=logging.INFO)

class LoggedAgeAccess:
    
    def __init__(self):
        print('init called')
    
    def __get__(self, obj, objtype=None):
        value = obj._age
        logging.info('Accessing %r giving %r', 'age', value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', 'age', value)
        obj._age = value

class Person:
    
    gender = ''
    age = LoggedAgeAccess()             # Descriptor instance

    def __init__(self, name, age):
        self.name = name                # Regular instance attribute
        self.age = age                  # 呼叫 __set__()

    def birthday(self):
        self.age += 1                   # 同時呼叫 __get__() / __set__()
        
try:
    print(Person.age)
    # AttributeError: 'NoneType' object has no attribute '_age'
    # 因為傳入 __get__ 的 obj 是 None， None 沒有 _age 
except:
    pass

print(Person.__dict__)
#{
#    '__module__': '__main__', 
#    'gender': ''   
#    'age': <__main__.LoggedAgeAccess object at 0x000001C540EEF7F0>, 
#    '__init__': <function Person.__init__ at 0x000001C5411D9240>, 
#    'birthday': <function Person.birthday at 0x000001C5411D92D0>, 
#    '__dict__': <attribute '__dict__' of 'Person' objects>, 
#    '__weakref__': <attribute '__weakref__' of 'Person' objects>, 
#    '__doc__': None
#}
        
mary = Person('Mary M', 30)         

# mary 的 instance dict 如下，實際資料存在 _age
print(vars(mary))                          
print(mary.__dict__) # 等同 vars(mary)
# {'name': 'Mary M', '_age': 30}
  
# 客製化 name #
# 當 class 建立時，type.__new__() 會檢視 class variables 並 callback 有 __set_name__() hook 的 class variables
# class A:
#     x = C() # 自動呼叫 x.__set_name__(A, 'x')

class LoggedAccess:

    def __set_name__(self, owner, name):
        print('self=', self, 'owner=', owner, 'name=', name)
        self.public_name = name
        self.private_name = '_' + name
        print(self.private_name)

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)
        logging.info('Accessing %r giving %r', self.public_name, value)
        return value

    def __set__(self, obj, value):
        logging.info('Updating %r to %r', self.public_name, value)
        setattr(obj, self.private_name, value)

class Person:

    name = LoggedAccess()                # First descriptor instance
    age = LoggedAccess()                 # Second descriptor instance
    height = 100
    
    def __init__(self, name, age):
        self.name = name                 # Calls the first descriptor
        self.age = age                   # Calls the second descriptor

    def birthday(self):
        self.age += 1  

# self= <__main__.LoggedAccess object at 0x000001D7127B32B0> owner= <class '__main__.Person'> name= name
# self= <__main__.LoggedAccess object at 0x000001D7127B31F0> owner= <class '__main__.Person'> name= age        
        
print(vars(LoggedAccess))
#{
#    '__module__'   : '__main__', 
#    '__set_name__' : <function LoggedAccess.__set_name__ at 0x0000027CAAECDA20>, 
#    '__get__'      : <function LoggedAccess.__get__ at 0x0000027CAAECDAB0>, 
#    '__set__'      : <function LoggedAccess.__set__ at 0x0000027CAAECDB40>, 
#    '__dict__'     : <attribute '__dict__' of 'LoggedAccess' objects>, 
#    '__weakref__'  : <attribute '__weakref__' of 'LoggedAccess' objects>, 
#    '__doc__'      : None
#}

print(vars(Person))

#{
#    '__module__'   : '__main__', 
#    'name'         : <__main__.LoggedAccess object at 0x000001D5731F32B0>, 
#    'age'          : <__main__.LoggedAccess object at 0x000001D5731F31F0>, 
#    'height'       : 100, 
#    '__init__'     : <function Person.__init__ at 0x000001D5734C1BD0>, 
#    'birthday'     : <function Person.birthday at 0x000001D5734C1C60>, 
#    '__dict__'     : <attribute '__dict__' of 'Person' objects>, 
#    '__weakref__'  : <attribute '__weakref__' of 'Person' objects>, 
#    '__doc__'      : None
#}

print(vars(Person)['name']) # <__main__.LoggedAccess object at 0x000001C0691632B0>
print(vars(vars(Person)['name']))
# {'public_name': 'name', 'private_name': '_name'}

p1 = Person('Bia', 20)
print(vars(p1))
# {'_name': 'Bia', '_age': 20}

# descriptor 的 __set_name__() 方法有兩個情境
# 1. descriptor 需要知道他的 owner class
# 2. descriptor 需要知道自己是被 assign 到 owner class 的哪個 class variable

class Slave:
    
    def __init__(self):        
        pass
    
    def __set_name__(self, owner, name):
        print(owner.__dict__)
        self.owner_class = owner
        self.owner_var_name = name

    def __get__(self, obj, objtype=None):
        value = getattr(obj, self.private_name)        
        return value

    def __set__(self, obj, value):        
        setattr(obj, self.private_name, value)

class Owner:

    q = Slave()                # First descriptor instance   
    
    def __init__(self, name, age):
        self.q = name                 # Calls the first descriptor

print(vars(vars(Owner)['q']))        
# {'owner_class': <class '__main__.Owner'>, 'owner_var_name': 'q'}
# 上述的兩個情境


# descriptor 只有作為 class variable 時有效，作為 instance variable 時無效
# descriptor 的主要動機是提供一個 hook 允許物件儲存在 class variable 中，以控制在 attribute lookup 發生的事
# 傳統上，calling class 控制 lookup 時會發生的事，但 descriptor 反轉此事，


       
