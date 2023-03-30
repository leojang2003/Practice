# Functions 是存在 class dictionaries 當呼叫時會被轉為 method，Method 與一般 function 差異在於 object instance 會被添加到其他參數中，照慣例被命名為 self。

# Methods 可以使用 types.MethodType 手動建立:

class MethodType:
    "Emulate PyMethod_Type in Objects/classobject.c"

    def __init__(self, func, obj):
        self.__func__ = func
        self.__self__ = obj

    def __call__(self, *args, **kwargs):
        func = self.__func__
        obj = self.__self__
        return func(obj, *args, **kwargs)

# To support automatic creation of methods, functions include the __get__() method for binding methods during attribute access. This means that functions are non-data descriptors that return bound methods during dotted lookup from an instance. Here’s how it works:

# 重點 : 
# 為了支援自動建立 method，function 有實作 __get__() method，在 attribute access 時 bind method。這表示 function 為 non-data descriptor 在 instance 的 dotted lookup 時回傳 bound method

class Function:
    ...

    def __get__(self, obj, objtype=None):
        "Simulate func_descr_get() in Objects/funcobject.c"
        if obj is None:
            return self
        return MethodType(self, obj)


class D:
    def f(self, x):
         return x

print(D.f.__qualname__) #'D.f'

# 透過 class dictionary 存取 function 時，因為 obj 為 None，所以 __get__() 僅回傳 function object:

print(D.__dict__['f'])  # <function D.f at 0x00C45070>
print(D.f)              # <function D.f at 0x00C45070>

# 有意思的是當透過物件 dotted access 存取時，會呼叫 __get__() 並回傳 bound method object:


d = D()
print(d.f) # <bound method D.f of <__main__.D object at 0x00B18C90>>

# 內部裡，bound method 儲存底下的 function 與 bound instance:

print(d.f.__func__) # <function D.f at 0x00C45070>
print(d.f.__self__) # <__main__.D object at 0x1012e1f98>



