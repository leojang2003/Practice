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

