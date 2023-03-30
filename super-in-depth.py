# help(super)
# 
# class super(object)
# |  super() -> same as super(__class__, <first argument>)
# |  super(type) -> unbound super object
# |  super(type, obj) -> bound super object; requires isinstance(obj, type)
# |  super(type, type2) -> bound super object; requires issubclass(type2, type)
# |  Typical use to call a cooperative superclass method:
# |  class C(B):
# |      def meth(self, arg):
# |          super().meth(arg)
# |  This works for class methods too:
# |  class C(B):
# |      @classmethod
# |      def cmeth(cls, arg):
# |          super().cmeth(arg)
# |
# |  Methods defined here:
# |
# |  __get__(self, instance, owner, /)
# |      Return an attribute of instance, which is of type owner.
# |
# |  __getattribute__(self, name, /)
# |      Return getattr(self, name).
# |
# |  __init__(self, /, *args, **kwargs)
# |      Initialize self.  See help(type(self)) for accurate signature.
# |
# |  __repr__(self, /)
# |      Return repr(self).
# |
# |  ----------------------------------------------------------------------
# |  Static methods defined here:
# |
# |  __new__(*args, **kwargs) from builtins.type
# |      Create and return a new object.  See help(type) for accurate signature.
# |
# |  ----------------------------------------------------------------------
# |  Data descriptors defined here:
# |
# |  __self__
# |      the instance invoking super(); may be None
# |
# |  __self_class__
# |      the type of the instance invoking super(); may be None
# |
# |  __thisclass__
# |      the class invoking super()
def prints(count):
    for i in range(count):
        print('')

import types
# super() 的用途是在解決 inheritance diamond 用的
# 也就是
#     A
#    / \
#   B   C
#    \ /
#     D 

# 如果沒有 super() 的情況下 

class A:
    def __init__(self):
        print('A.__init__')
        super(A, self).__init__()
        
class B(A):
    def __init__(self):
        print('B.__init__')        
        A.__init__(self) 
        # 沒有呼叫 super() 直接呼叫 A.__init__()
        
class C(A):
    def __init__(self):
        print('C.__init__')
        super(C, self).__init__()
   
class D(B, C):
    def __init__(self):        
        super(D, self).__init__()

print(D.__mro__)



# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
# MRO : D > B > C > A
        
d = D()
# D.__init__
# B.__init__
# A.__init__

# 因為 class B 的 __init__ 沒有呼叫 super() 所以我們可看到 class C 的 __init__ 沒有呼叫到

prints(6)

class A:
    def __init__(self):
        print('A.__init__')
        super(A, self).__init__()
        
class B(A):
    def __init__(self):
        print('B.__init__')        
        A.__init__(self) 
        # 沒有呼叫 super() 直接呼叫 A.__init__()
        
class C(A):
    def __init__(self):
        print('C.__init__')
        super(C, self).__init__()

# 調整繼承的順序，B        
class D(C, B):
    def __init__(self):
        print('D.__init__')
        super(D, self).__init__()

print(D.__mro__)
d = D()
# (<class '__main__.D'>, <class '__main__.C'>, <class '__main__.B'>, <class '__main__.A'>, <class 'object'>)
# D.__init__
# C.__init__
# B.__init__
# A.__init__

# 如果我們調整 class D 的繼承順序，改成 C、B，則 MRO 變成 D > C > B > A，剛好沒問題。為了避免一開始的情況，class B 要改成呼叫 super().__init__() 如下

prints(6)

class A:
    def __init__(self):
        print('A.__init__')
        super(A, self).__init__()
        
class B(A):
    def __init__(self):
        print('B.__init__')        
        super(B, self).__init__()
        
class C(A):
    def __init__(self):
        print('C.__init__')
        super(C, self).__init__()
   
class D(B, C):
    def __init__(self):
        print('D.__init__')
        super(D, self).__init__()

print(D.__mro__)
d = D()

# super() 的 signature 如下
# class super(type, object_or_type=None)
# super()回傳一個 proxy object 委派 method call 給 type 的 parent 或 sibling class
# object_or_type 決定 MRO 找尋的順序，會從 type 的下一個 class 開始

class A:
    def __init__(self):
        print('A.__init__')
        super(A, self).__init__()
            
    def lock(self):
        print('A locked')
        
class B(A):
    def __init__(self):
        print('B.__init__')        
        super(B, self).__init__()        
    
    def lock(self):
        print('B locked')
        
class C(A):
    def __init__(self):
        print('C.__init__')
        super(C, self).__init__()
    
    def lock(self):
        print('C locked')
    
   
class D(B, C):
    def __init__(self):
        print('D.__init__')      
        super(B, self).__init__()
    

print(D.__mro__)
# MRO D > B > C > A > object
d = D()
# 因為我們在 D 的 __init__ 呼叫 super(B, self).__init__()，所以在 MRO 中，會呼叫 B class 的下一個 C class 的 __init__，最後執行結果如下
# D.__init__
# C.__init__
# A.__init__

# 如果 super() 第二個參數為空，則回傳的 super 物件是 unbounded

prints(6)

class D(C, B):
    def __init__(self):        
        print(super())      # <super: <class 'D'>, <D object>>
        # 根據 help(super) 等同 same as super(__class__, <first argument>)
        
        print(super(__class__))
        super().lock()      # C locked   
                
        print('☆☆', super(D)) # <super: <class 'D'>, NULL> 
        
        print('☆☆☆', super(D,D).__getattribute__(self, 'lock'))
        # <bound method C.lock of <__main__.D object at ...>>
        
        print('☆☆☆☆', super(D,self).__getattribute__('lock'))
        # <bound method C.lock of <__main__.D object at ...>>
        try:
            super().__dict__['lock'] # KeyError: 'lock'
        except:
            pass
        
        print(super(D,D).lock)     
        # <function C.lock at 0x000002C099A945E0>
        
        
        print(super(D,D))   # <super: <class 'D'>, <D object>>
        
        try:
            super(D, D).lock()  # TypeError: C.lock() missing 1 required positional argument: 'self'
        except:
            pass
            
        super(D, D).lock(self) # C locked   
                
        print(super(D,self))# <super: <class 'D'>, <D object>>
        super(D, self).lock()# C locked        
        
        print(super().__init__)      # <bound method B.__init__ of <__main__.D object at 0x000002A84945B340>>
        print(super(D).__init__)     # <method-wrapper '__init__' of super object at 0x000002A849463080>    
        print(super(D,D).__init__)   # <function B.__init__ at 0x000002A84944B400>  
        print(super(D,self).__init__)# <bound method B.__init__ of <__main__.D object at 0x000002A84945B340>>
        
        # super(D,self).__init__()
        print(super(D).__init__())
        print('end')
    
    def funcX():
        pass
    
    def funcY(self):
        pass
        
d = D()

prints(6)

# print('d.__get__', d.__ge__())

# 如果第二個參數是物件，則須滿足 isinstance(obj, type)
# object.__get__(self, instance, owner=None)
# 呼叫取得 onwer class 的 attribute (AKA class attribute access)，或是 owner class 的 instance (instance attribute access)，

class Slave:
    
    def __get__(self, instance, owner):
        print('slave self', self)
        print('slave instance', instance)
        print('slave owner', owner)
        
        return 3
        
        pass
        
class Owner:
    slave = Slave()
    
    def __init__(self):
        pass

print(' ')
        
leo = Owner()
Owner.__dict__ 
print('Owner.__dict__', Owner.__dict__)  
print('Owner.__dict__', Owner.__dict__['slave'].__get__(None, A))
print('Owner.__dict__', Owner.__dict__['slave'].__get__(leo, A))    

print(' ')
        
class D(B, C):
    def __init__(self):
        print('D.__init__')
        print(isinstance(self, B)) # True
        super(B, self).__init__()

# 如果第二個參數是 type，則須滿足 issubclass(type2, type)

# 額外說明 method-wrapper :
# method-wrapper 物件是 wrapping 一個 C 方法 

class Test:
        
    def method_one(self):
        print('method one')
        pass
    
    def method_two():
        print('method two')
        pass

# 額外說明 Bound Method :
# 如果一個 function 是 class 的 attribute，且可以透過 instance 存取，我們稱之為 bound method。
# 另外 bound method 的第一個參數為 self，bound method 也稱作 instance method。

try:    
    test = Test()
    test.method_one() # 會被轉成 Test.method_one(test)
    test.method_two() 
    # TypeError: Test.method_two() takes 0 positional arguments but 1 was given
except:
    pass

# 改法如下

class Test:
        
    def method_one(self):
        print('method one')
        pass
    
    # 此 decorator 告訴 metaclass type 不要替 method_two 建立 bound method
    @staticmethod
    def method_two():
        print('method two')
        pass
        
test = Test()        
test.method_two() #method two

# 額外說明 Unbound Method :
# 第一個參數沒有 instance 的 method 稱為 unbound method，現在稱為 function
# Python 3 以後移除了 unbound Method

# 假設我們現在有一個 class 如下

class C(object):
    def foo(self):
        print('foo')
        pass

try:
    print(C.foo) 
    # <function C.foo at 0x0000021B4272BB50> 
    # Python 2.0 以前的說法這是一個 unbound method    
except:
    pass

c = C()
print('******************')    
print(C.__dict__['foo']) # <function C.foo at 0x000002315B42BA30>
print(C.__dict__['foo'].__get__(Owner, C)) # <function C.foo at 0x000002315B42BA30>
print('******************')
# 上面兩個是一樣的
# function 因為有 __get__ 所以是 descriptor
  
print(C.__dict__['foo'].__get__(C)) # <bound method C.foo of <class '__main__.C'>>
print(C.__dict__['foo'].__get__(c)) # <bound method C.foo of <__main__.C object at 0x000001267B02B040>>    

# 注意上面我們分別傳入類別與物件

# 如果我們不要 class 的方法變成 method，可以使用 @staticmethod 修飾

class C(object):
    @staticmethod
    def foo():
        print('foo')
        pass   

print(C.__dict__['foo']) # <staticmethod(<function C.foo at 0x000001BA6B39BB50>)>     
print(C.__dict__['foo'].__get__(C))  # <function C.foo at 0x000001642408BAC0>
print(C.__dict__['foo'].__get__(c))  # <function C.foo at 0x000001642408BAC0>

class Car:
    
    def __get__(self, instance, owner):
        print('get')
        print(self)
        print(instance)
        print(owner)
        return self.model
        
    def __set__(self, instance, value):
        self.model = value
        
class Carfax:

    car = Car()
    
    def __init__(self):        
        pass
        
carfax = Carfax();
carfax.car = 'Scion'
print(carfax.car)

# 只要是有以下方法的'物件'就是 'descriptor'
# __get__ non-data descriptor method, for example on a method/function
# __set__ for example on a property instance or slot
# __delete for example on a property instance or slot
# 這三個也是俗稱的 'descriptor methods'

# '只'定義 __set__ 的 稱為 data descriptor
# 有定義 __set__, __delete 也稱為 data descriptor

# 這些 descriptor 物件在其他的 class 中是 'attribute'
# 換句話說，他們活在 class object 的 __dict__ 中

# function/method, bound method, property, classmethod, staticmethod 都是 descriptor，都使用上述的 'special method' 

# data descriptor 像是 property，可以允許 lazy evaluation

# 另外一個 data descriptor，像是 __slot__ 建立的 member_descriptor，有 memory saving 與 faster lookup 的功效，class 藉由將資料存在 mutable tupe-like 的資料結構，而不是較彈性但較占空間的 __dict__

# Non-data descriptor 像是 instance method / class method，implicitly 取得第一個參數(通常是 self 或是 cls) 透過 Non-data descriptor method __get__，這也是 static method 知道不有 implicit first argument 的原因。

print(classmethod.__get__) # 只有 __get__
# print(classmethod.__set__)
# print(classmethod.__delete__)
print(staticmethod.__get__) # 只有 __get__
# print(staticmethod.__set__)
# print(staticmethod.__delete__)

class Ten:
    def __get__(self, obj, objtype=None):
        return 10

class C(object):
    
    x = 5
    ten = Ten()
    
    def foo(self):
        print('foo')
        pass
        
c = C()
ten = Ten()

print(C.__dict__)

print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')

def talk():
    print('talk')
print(dir(talk)) 
ten.edge = talk
print(dir(ten.edge))    
#print(ten.edge.__func__)
# 以下將 C.foo 'binding' 到 ten 物件
ten.edge = types.MethodType(C.foo, ten)
ten.edge() # foo 
print(dir(ten.edge)) 
print(ten.edge.__self__)
print(ten.edge.__func__)
print(types.MethodType(C.foo, c))
print(ten.edge)


# MethodType 類似
# class MethodType:
    # "Emulate PyMethod_Type in Objects/classobject.c"

    # def __init__(self, func, obj):
        # self.__func__ = func
        # self.__self__ = obj

    # def __call__(self, *args, **kwargs):
        # func = self.__func__
        # obj = self.__self__
        # return func(obj, *args, **kwargs)

# class Function:
    # ...

    # def __get__(self, obj, objtype=None):
        # "Simulate func_descr_get() in Objects/funcobject.c"
        # if obj is None:
            # return self
        # return MethodType(self, obj)
