import types

# 呼叫 types.MethodType 方法可以手動建立 method
# 根據文件 types.MethodType 近似於以下程式碼
#
# class MethodType:
    # "Emulate PyMethod_Type in Objects/classobject.c"

    # def __init__(self, func, obj):
        # self.__func__ = func
        # self.__self__ = obj

    # def __call__(self, *args, **kwargs):
        # func = self.__func__
        # obj = self.__self__
        # return func(obj, *args, **kwargs)

class John:
    def __get__(self, obj, objtype=None):
        print('John __get__ called self=', self, 'obj=', obj, 'objtype=', objtype)
        if(obj == None):
            return self            
        return obj.foo()
        
class Lisa:
    def __get__(self, obj, objtype=None):
        return 'Lisa'

class C(object):
    
    x = 5
    john = John()
    
    def foo(self):
        print(self, 'called foo')        
        
    def doo(self):
        print(self, 'called doo')
        
print(C.__dict__)
# {
#   '__module__': '__main__', 
#   'x': 5, 
#   'john': <__main__.John object at 0x0000019791583E20>, 
#   'foo': <function C.foo at 0x000001979157BD90>, 
#   'doo': <function C.doo at 0x000001979157BE20>, 
#   '__dict__': <attribute '__dict__' of 'C' objects>, 
#   '__weakref__': <attribute '__weakref__' of 'C' objects>, 
#   '__doc__': None
# }
# 原先 class dict 的是 'foo': <function C.foo at 0x000001979157BD90>

# class C 裡的 john 是 descriptor，如果我們呼叫如下
print(C.john)
# John __get__ called self= <__main__.John object at 0x0000028922BC3D90> obj= None objtype= <class '__main__.C'>
# 因為 obj 是 None， 所以回傳的是 self 

print('  中斷  ')
    
c = C()
print(c.__dict__)
print(c.john)
# John __get__ called self= <__main__.John object at 0x0000028922BC3D90> obj= <__main__.C object at 0x0000028922BC3C10> objtype= <class '__main__.C'>

#
# function 有一個 __get__ 方法，在 attriubte dot access 時做 method binding
#
class Function:
   ...

   def __get__(self, obj, objtype=None):
       "Simulate func_descr_get() in Objects/funcobject.c"
       if obj is None:
           return self
       return MethodType(self, obj)

# 如果 obj 是 None，則回傳 function 物件
# 如果 obj 非 None，則將 obj bind 到 function 物件
# 透過以下方式呼叫不會 invoke __get__()

print('C.foo=', C.foo)
print(C.__dict__['foo'])

# 透過物件方式呼叫則會 invoke __get__()，如下

print(c.foo)

class X():
    pass
    

print(c.foo) # <bound method C.foo of <__main__.C object at 0x000002280489BAC0>>
print(c.foo.__self__) # <__main__.C object at 0x000002280489BAC0>
print(c.foo.__func__) # <function C.foo at 0x00000228048BBBE0>

print(' ')

def talk():
    print('talk')

john = John()
john.foo2 = talk
try:
    print(john.foo2) # <function talk at 0x000001A8F4493E20>
    print(john.foo2.__self__) # AttributeError: 'function' object has no attribute '__self__'
    print(john.foo2.__func__) # AttributeError: 'function' object has no attribute '__func__'
except:
    pass

# 注意 !!!
# 以下將 C.foo 'binding' 到 john 物件
#

print('↖↗↙↘')
print('↖↗↙↘')
print('↖↗↙↘')

john.foo2 = types.MethodType(C.foo, john)
john.foo2() # <__main__.John object at 0x0000021ADF333DC0> called foo

print(john.foo2) # <bound method C.foo of <__main__.John object at 0x000001CA76ACBA90>>
print(dir(john.foo2))

# ['__call__', '__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__func__', '__ge__', '__get__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__self__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__']

# 我們可以看到 foo2 現在有 __self__ / __func__ 
 
print(john.foo2.__self__) # <__main__.John object at 0x0000027D87C7BA90>
print(john.foo2.__func__) # <function C.foo at 0x0000027D87C9BBE0>

#
# 我們將 C.foo 綁定到 c 物件
#
# print(types.MethodType(C.foo, c)) 
# <bound method C.foo of <__main__.C object at 0x0000027D87C7BAC0>>


print(c.foo.__self__) # <__main__.C object at 0x0000016478A93E20>
print(c.foo.__func__) # <function C.foo at 0x0000027D87C9BBE0>

# 注意 !!!
# 以下將 C.foo 'binding' 到 john 物件，再指派給另一個物件 lisa
#

print('↘')
print('↘')
print('↘')

lisa = Lisa()
lisa.foo3 = types.MethodType(C.foo, john)
lisa.foo3() # foo 

print(lisa.foo3) # <bound method C.foo of <__main__.John object at 0x0000026372213DF0>>
print(lisa.foo3.__self__) # <__main__.John object at 0x0000026372213DF0>
print(lisa.foo3.__func__) # <function C.foo at 0x000002637220BD90>

# 注意 !!!
# 
#

john.foo2 = types.MethodType(C.doo, john)
john.foo2()
lisa.foo3()
