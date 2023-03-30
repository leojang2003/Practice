
# Static methods 回傳底下的 function 而不作任何修改。呼叫 c.f 或 C.f 等同 object.__getattribute__(c, "f") 或 object.__getattribute__(C, "f"). 印此，不論透過 object 或 class 存取都是得到相同的 function object

# 當方法不需要使用 self variable 時，可以將方法設為靜態方法。

class E:
    @staticmethod
    def f(x):
        return x * 10
E.f(3) # 30

E().f(3) # 30

# 使用 non-data descriptor，python 版的 staticmethod() 如下:

class StaticMethod:
    "Emulate PyStaticMethod_Type() in Objects/funcobject.c"

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f

    def __call__(self, *args, **kwds):
        return self.f(*args, **kwds)
