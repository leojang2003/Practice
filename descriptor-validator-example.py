# 用以下 doc 的實際範例示範 descriptor 的用法

from abc import ABC, abstractmethod

class Validator(ABC):

    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        print('__get__ self=', self, 'obj=', obj, 'objtype=', objtype)
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        print('__set__ self=', self, 'obj=', obj, 'value=', value)
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        print('abstractmethod validate')
        pass
        
class OneOf(Validator):

    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value!r} to be one of {self.options!r}')
            
class Component:

    kind = OneOf('wood', 'metal', 'plastic')
    
    def __init__(self, name, kind, quantity):
        self.name = name
        self.kind = kind
        self.quantity = quantity
        
print(vars(Component))
# {
#     '__module__': '__main__', 
#     'kind': <__main__.OneOf object at 0x0000029E243BBA90>, 
#     '__init__': <function Component.__init__ at 0x0000029E243DB010>, 
#     '__dict__': <attribute '__dict__' of 'Component' objects>, 
#     '__weakref__': <attribute '__weakref__' of 'Component' objects>, 
#     '__doc__': None
# }
print(vars(Component)['kind']) # <__main__.OneOf object at 0x0000020C46F7BA90>

try:
    print(Component.kind) 
    # 因為 OneOf 是 descriptor，所以呼叫 .kind 時會觸發 Validator 的 __get__()，log 如下
    # __get__ self= <__main__.OneOf object at 0x000001D437643FD0> obj= None objtype= <class '__main__.Component'>
    # 因為 NoneType 沒有 self.private_name 也就是 _kind 的屬性，所以會回傳錯誤如下
    # AttributeError: 'NoneType' object has no attribute '_kind'
except:
    pass

Component('Widget', 'qrita', 5) 
# Component 的 __init__ 會呼叫 self.kind = kind 觸發 descriptor 的 __set__
# __set__ self= <__main__.OneOf object at 0x000001ECDCD03FD0> 
# obj= <__main__.Component object at 0x000001ECDCD03D30> value= qrita
# Expected 'qrita' to be one of {'metal', 'plastic', 'wood'}     
