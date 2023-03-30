# Class methods
#與 static methods 不同, class methods 在呼叫 function 前將 class reference 添加到 argument list 前面。

class F:
    @classmethod
    def f(cls, x):
        return cls.__name__, x

print(F.f(3)) # ('F', 3)

print(F().f(3)) # ('F', 3)

print(F())

# class method 的用途在於當我們的 method 只需要 class reference 而不需要特定 instance 的資料。一個 class methods 的用途為建立 alternate class constructor。舉例來說，classmethod dict.fromkeys() 從 key 的 list 建立一個新的 dictionary。Python 程式如下

class Dict(dict):
    @classmethod
    def fromkeys(cls, iterable, value=None):
        "Emulate dict_fromkeys() in Objects/dictobject.c"
        print(iterable)
        d = cls()
        for key in iterable:
            d[key] = value
        return d

d = Dict.fromkeys('abracadabra')
print(type(d) is Dict) # True
print(d) #{'a': None, 'b': None, 'r': None, 'c': None, 'd': None}

# 使用 non-data descriptor protocol，Python 版的 classmethod() 如下:

class ClassMethod:
    "Emulate PyClassMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        if hasattr(type(self.f), '__get__'):
            return self.f.__get__(cls, cls)
        return MethodType(self.f, cls)

# Python 3.9 加入程式 hasattr(type(self.f), '__get__') 讓 classmethod 可以支援 chain decorator，舉例來說，@classmethod 與 @property 可以同時裝飾方法:

class G:
    @classmethod
    @property
    def __doc__(cls):
        return f'A doc for {cls.__name__!r}'

G.__doc__
# "A doc for 'G'"
