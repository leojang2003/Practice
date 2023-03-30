class Charateristic:
    
    def __init__(self):        
        pass
    
    def __set_name__(self, owner, name):        
        self.private_name = '_' + name
        self.public_name = name

    def __get__(self, obj, objtype=None):
        print('__get__ self=', self, 'obj=', obj, 'objtype=', objtype)
        value = getattr(obj, self.private_name)        
        return value

    def __set__(self, obj, value):
        print('__get__ self=', self, 'obj=', obj, 'value=', value)    
        setattr(obj, self.private_name, value) # 在這裡設定 obj._age = 30, obj._height = 176

class Owner:

    age = Charateristic()                
    height = Charateristic()
    
    def __init__(self, age, height):
        self.age = age 
        self.height = height

me = Owner(30, 176)        
print(vars(me))
# {'_age': 30, '_height': 176}

# attribute access 首先是找 object 的 dictionary
try:
    print(me.__dict__['age']) #KeyError: 'age'
except:
    pass
    
# 接著找 type(a).__dict__['x']
print(type(me).__dict__['age']) # <__main__.Charateristic object at 0x000001265B67BCD0>

# 再來如果 looked-up value 是定義 descriptor 方法的物件如上，則 python 會覆寫預設的行為並呼叫 descriptor method 取代

# properties, methods, static methods, class methods, super() 都是運用 descriptor
# 實作__set__() 或 __delete__() 稱為 data descriptor
# 僅實作 __get__() 稱為 non data descriptor

# descriptor 可以使用 desc.__get__(obj) 或 desc.__get__(None, cls) 直接呼叫
# 但較常見的做法還是透過 attribute access 自動呼叫

# 如果 instanct dict 和 data descriptor 有相同的 name，則 data descriptor 有優先權
# 如果 instanct dict 和 non data descriptor 有相同的 name，則 dictionary entry 有優先權
# 解釋如下

# data descriptor 
class A:
    
    def __get__(self, obj, objtype=None):        
        print('get from A')

    def __set__(self, obj, value):        
        print('set from A')

# non-data descriptor        
class B:
        
    def __get__(self, obj, objtype=None):        
        print('get from B')

class C:
    
    a = A() 
    b = B()

    def __getattr__(self, name):        
        return name

c = C()

# 以下分為幾個部分
# 1. 從物件存取 descriptor
# 2. 從類別存取 descriptor

#        
# ☆ ☆ ☆ ☆ ☆ ☆ 1. 從物件存取 descriptor ☆ ☆ ☆ ☆ ☆ ☆  
#
# 當存取物件 access attribute 時，python 會自動呼叫 __getattribute__(self, name)，
# __getattribute__() 會依序呼叫 data descriptor > instance variable > non-data descriptor > class variable > 
# 最後拋出 AttributeError，程式如下

def find_name_in_mro(cls, name, default):
    "Emulate _PyType_Lookup() in Objects/typeobject.c"    
    for base in cls.__mro__:        
        if name in vars(base):
            print('vars(base)=', vars(base))
            return vars(base)[name]
    return default

def object_getattribute(obj, name):
    "模擬 PyObject_GenericGetAttr() in Objects/object.c"
    null = object()
    objtype = type(obj)    
    cls_var = find_name_in_mro(objtype, name, null)
    print('cls_var=', cls_var) # <__main__.A object at 0x00000233D89D7C10>
    
    # 先嘗試取得 descriptor 的 __get__()，此例為回傳 <function A.__get__ at ...>
    descr_get = getattr(type(cls_var), '__get__', null)
    
    # getattr(object, name default) : 回傳 object 的 named attribute 的值
        
    if descr_get is not null:
        if (hasattr(type(cls_var), '__set__')
            or hasattr(type(cls_var), '__delete__')):
            return descr_get(cls_var, obj, objtype)     # data descriptor
    if hasattr(obj, '__dict__') and name in vars(obj):
        return vars(obj)[name]                          # instance variable
    if descr_get is not null:
        return descr_get(cls_var, obj, objtype)         # non-data descriptor
    if cls_var is not null:
        return cls_var                                  # class variable
    raise AttributeError(name)
    
object_getattribute(c, 'a')

# 我們可以看到如果 attribute 找不到的話，會回傳 AttributeError，
# 但實際上 getattribute() 的呼叫被包在一個 helper 方法如下，但因為 python 的 dot operator 跟 getattr() 方法會負責在 getattribute() 回傳 AttributeError 時 會呼叫 getattr() 

def getattr_hook(obj, name):
    "Emulate slot_tp_getattr_hook() in Objects/typeobject.c"
    try:
        return obj.__getattribute__(name)
    except AttributeError:
        if not hasattr(type(obj), '__getattr__'):
            raise
    return type(obj).__getattr__(obj, name)             # __getattr__

# ☆ ☆ ☆ ☆ ☆ ☆
    


c.a # get from A
c.b # get from B

print(vars(c)) # {}

c.a = 0 # set from A
# data descriptor 有最高優先權

print(vars(c)) # {}

print(c.a) # get from A
# data descriptor 有最高優先權

c.b = 0 
# 因為 B 是 non-data descriptor 沒有 __set__() 方法，instance c 會重新 assign 一個 instance variable b 值為 0
# 證明 instance variable > non-data descriptor

print(c.b) # 0
# 不會再呼叫 B 的 __get__() 方法

# 當 obj.x lookup 時在 instance __dict__ 外找到一個 descriptor，則 __get__() 的呼叫規則，會視 obj 為 object, class, 或 instance of super 而有所不同

print(c.test) # test
# 因為我們有定義 __getattr__()，所以 __getattribute__ 會呼叫 __getattr__()，反之會傳出 AttributeError


#        
# ☆ ☆ ☆ ☆ ☆ ☆ 2. 從物件存取 descriptor ☆ ☆ ☆ ☆ ☆ ☆  
#
# A.x 使用 type.__getattribute__().與 object.__getattribute__() 相似除了 instance dictionary lookup 替換為搜尋 class 的 method resolution order. 如果有找到 descriptor，則喚起 desc.__get__(None, A).

C.a # get from A

#        
# ☆ ☆ ☆ ☆ ☆ ☆ 3. 從super()存取 descriptor ☆ ☆ ☆ ☆ ☆ ☆  
#
# super 的 dotted lookup 邏輯，在 super() 回傳物件的 __getattribute__() 方法
# 若是如 super(A, obj).m 會找尋 obj.__class__.__mro__ 找到緊鄰 A 的 base class B，並回傳 B.__dict__['m'].__get__(obj, A)

#
# ☆ ☆ ☆ ☆ ☆ ☆ invocation logic 總結 ☆ ☆ ☆ ☆ ☆ ☆ 
#
# descriptor 是被 __getattribute__() 方法 invoke
# 類別從 object, type, super() 繼承 __getattribute__ (?)
# 覆寫 __getattribute__() 方法會阻止 python 自動呼叫 descriptor，因為 descriptor 邏輯都在此方法
# object.__getattribute__() 與 type.__getattribute__() 會以不同的方式呼叫 __get__()。前者包含 instance 或是 class，後者是傳入 None 並永遠包含 class。
# data descriptor 的優先權一定在 instance dictionary 之前
# non-data descriptor 有機會被 instance dictionary 覆寫


# 有時候 descriptor 需要知道他被指派到哪個 class variable name。當建立一個新的 class，'type' 這個 metaclass 會檢視這個新 class 的 dictionary。如果有找到 descriptors 且他們有定義 __set_name__(), 則以兩個參數呼叫此 method，owner 為使用 descriptor 的 class, 而 name 為 descriptor 被指派到的 class variable。

# 實作細節在 Objects/typeobject.c 的 type_new() 與 set_names()

# 因為 type.__new__() 是在建立 class 時呼叫，所以如果是之後才加到 class 的 descriptor 是不會呼叫 __set_name__() 的，需手動呼叫

# descriptor 用途很廣，包含 Properties、bound methods、static methods、class methods、__slots__ 背後都是使用 descriptor protocol
 
