# 模擬 types.MethodType 如下 ...

class MethodType:
    "模擬 PyMethod_Type in Objects/classobject.c"

    def __init__(self, func, obj):
        print('MethodType __init__')
        self.__func__ = func
        self.__self__ = obj

    def __call__(self, *args, **kwargs):
        func = self.__func__
        obj = self.__self__
        print('MethodType __call__')
        return func(obj, *args, **kwargs)


# 嘗試做出類似 function 的 class。如同 function，EmulateFunction 也是一個 descriptor

#import types

class EmulateFunction:
    
    def __init__(self, f):
        print('呼叫 init : self=', self, 'f=', f)
        self.f = f
        self.f.__qname__ = 'check'
    
    def __get__(self, obj, objtype=None):        
        print('呼叫 get : self=', self, 'obj=', obj)
        if obj is None:
            return self
        #return types.MethodType(self, obj)
        return MethodType(self, obj)
    
    def __call__(self, *args, **kargs):
        print('呼叫 call : called self=', self, '*args=', *args)        
        return self.f(*args, **kargs)
        
    
class Car:
    
    def check(self):
        print('check() called')
        pass
        
    check = EmulateFunction(check)

   
    
    
# 執行後出現以下 log，注意 Car 的 check 是一個 EmulateFunction 物件，我們用 EmulateFunction 來模擬 function
# 也因為 EmulateFunction 有實作 __get__() 方法，所以 check 同時也是一個 non-data descriptor，log 如下
# 呼叫 init : self= <__main__.EmulateFunction object at ...> f= <function Car.check at ...>

print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆') 

print(Car.check)
# 會呼叫 __get__() 方法，但第二個參數的 obj 為 None，log 如下
# 呼叫 get : self= <__main__.EmulateFunction object at ...> obj= None 
# 回傳的物件是 <__main__.EmulateFunction object at ...>

print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆')    
print('☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆ ☆') 

print(vars(Car.check))
# {'f': <function Car.check at ...>}
# EmulateFunction 物件有一個 function 叫 f

try:
    print(Car.check.__func__) # EmulateFunction' object has no attribute '__func__'
    print(Car.check.__self__) # EmulateFunction' object has no attribute '__self__'

    # 我們可以看到 EmulateFunction 物件是沒有 __func__ 跟 __self__ 的
    # 是 
    
    Car.check()

    # 呼叫 get : self= <__main__.EmulateFunction object at ...> obj= None
    # 呼叫 call : called self= <__main__.EmulateFunction object at ...> *args=
    # 我們可以看到 __call__最後會回傳 self.f(*args, **kargs)，但因為 *args 為空的 tuple
    # 所以會出現 TypeError: Car.check() missing 1 required positional argument: 'self'   
except:
    pass
    
car = Car()

print(car.check) # <bound method ? of <__main__.Car object at ...>>
# car.check 呼叫 EmulateFunction 的 __get__()，回傳一個 bound method

print(car.check.__func__) # <__main__.EmulateFunction object at ...>
print(car.check.__self__) # <__main__.Car object at ...>

car.check() # check() called

#
# 模擬 static method 如下 ...
#

print('模擬 static method 如下 ...')

class EmulateStaticMethod:
    "模擬 PyStaticMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        print('呼叫 init : self=', self, 'f=', f)
        self.f = f

    def __get__(self, obj, objtype=None):
        print('呼叫 get : self=', self, 'obj=', obj)
        return self.f

    def __call__(self, *args, **kwds):
        print('呼叫 call : called self=', self, '*args=', *args)      
        return self.f(*args, **kwds)
        
class Car:
    
    def check():
        print('check() called')
        pass
        
    check = EmulateStaticMethod(check)   

# 呼叫 init : self= <__main__.EmulateStaticMethod object at ...> f= <function Car.check at ...>


print(Car.check)
# 會呼叫 __get__() 方法，但第二個參數的 obj 為 None，log 如下
# 呼叫 get : self= <__main__.EmulateStaticMethod object at ...> obj= None 
# 注意這裡 get 回傳的是 self.f，也就是 <function Car.check at ...>

print(vars(Car.check))
# {} 

Car.check() # check() called

# 呼叫 get : self= <__main__.EmulateStaticMethod object at ...> obj= None
# 沒有呼叫 EmulateStaticMethod 的 __call__()，直接呼叫 function 的 __call__()
# 可以看到成功呼叫沒傳入參數的方法呼叫
  
car = Car()

print(car.check) # <function Car.check at ...>
# car.check 呼叫 EmulateStaticMethod 的 __get__()，回傳一個 function

car.check() # check() called

#
# static method 總結
# 不管是從類別或是物件都可以成功呼叫  static method 
#

#
# 使用 @EmulateStaticMethod decorator 如下 ...
#
print('使用 @EmulateStaticMethod decorator 如下 ...')

class Car:
    
    @EmulateStaticMethod
    def check():
        print('check() called')
        pass

c = Car()
Car.check() # check() called  
c.check()   # check() called  

#
# 如上，使用 decorator 也從類別或是物件成功呼叫 check
#

#
# 模擬 class method 如下 ...
#
print('模擬 class method 如下 ...')

class EmuClsMethod:
    "Emulate PyClassMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        print('呼叫 init : self=', self, 'f=', f)
        self.f = f

    def __get__(self, obj, cls=None):
        print('呼叫 get : self=', self, 'obj=', obj, 'cls=', cls)
        
        # cls 看起來不會是 None，不懂這裡的用途?
        if cls is None:
            print('cls is None')
            cls = type(obj)
        
        if hasattr(type(self.f), '__get__'):
            print('self.f=', self.f, 'type(self.f)=', type(self.f), 'has attribute __get__')            
            return self.f.__get__(cls, cls)
        
        return MethodType(self.f, cls)

class Car:
    
    def check(self):
        print('check() called')
        pass
        
    check = EmuClsMethod(check) 

# 呼叫 init : self= <__main__.EmuClsMethod object at ...> f= <function Car.check at ...>

print(Car.check)
# 呼叫 get : self= <__main__.EmuClsMethod object at ...> obj= None cls= <class '__main__.Car'>
# self.f= <function Car.check at ...> type(self.f)= <class 'function'> has attribute __get__
# <bound method Car.check of <class '__main__.Car'>>

Car.check() # check() called

print(vars(Car.check)) # {}
print(Car.check.__func__) # <function Car.check at ...>
print(Car.check.__self__) # <class '__main__.Car'>

print('從物件呼叫 class method 如下 ...')
    
car = Car()

print(car.check) # <bound method Car.check of <class '__main__.Car'>>

print(car.check.__func__) # <function Car.check at ...>
print(car.check.__self__) # <class '__main__.Car'>

car.check() # check() called

print('     ')
print('連鎖 decorator 如下 ...')
print('     ')

class Car:
    
    @EmuClsMethod
    @property    
    def check(self):
        return 20
        pass
    
print(Car.check)    # 20
print(Car().check)  # 20

print('     ')
print('連鎖 decorator 拆開如下 ...')
print('     ')

class Car:
           
    def check(self):
        return 20
        pass

    check = property(check) #    
    check = EmuClsMethod(check)    

# 執行 check = EmuClsMethod(check) 的 log 如下
# 呼叫 init : self= <__main__.EmuClsMethod object at ...> f= <property object at ...>

print('Car.check')
print(Car.check)

# 呼叫 get : self= <__main__.EmuClsMethod object at ...> obj= None cls= <class '__main__.Car'>
# self.f= <property object at ...> type(self.f)= <class 'property'> has attribute __get__

print('Car().check') 
print(Car().check)

# 呼叫 get : self= <__main__.EmuClsMethod object at ...> obj= <__main__.Car object at ...> cls= <class '__main__.Car'>
# self.f= <property object at ...> type(self.f)= <class 'property'> has attribute __get__
# 20

try:
    Car.check()     # 'int' object is not callable 
    Car().check()   # 'int' object is not callable 
except:
    pass
    
print('     ')
print('若是顛倒 decorator ... 如下')
print('     ')
    
class Car:
    
    @property
    @EmuClsMethod    
    def check(self):
        return 20
        pass
    
print(Car.check)    # 20
try:
    print(Car().check)  # 'EmuClsMethod' object is not callable
    # 因為 property 的 __get__() 會回傳 self.fget(obj)，而 fget 為 EmuClsMethod 物件
except:
    pass

print('     ')
print('若是顛倒 decorator ... 拆開如下')
print('     ')

class Car:
           
    def check(self):
        return 20
        pass

    check = EmuClsMethod(check)
    check = property(check)

# 呼叫 init : self= <__main__.EmuClsMethod object at ...> f= <function Car.check at ...>

print(Car.check)    # <property object at 0x000001EF93206CF0>
try:
    print(Car().check)  # 'EmuClsMethod' object is not callable
    # 因為 property 的 __get__() 會回傳 self.fget(obj)，而 fget 為 EmuClsMethod 物件
except:
    pass
