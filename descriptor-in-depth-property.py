#
# Properties
#
# property(fget=None, fset=None, fdel=None, doc=None) -> property
# 以下是典型的 managed attribute x 用法:

class C:
    
    def getx(self):
        print('getx')
        return self.__x
        
    def setx(self, value):
        print('setx')    
        self.__x = value
        
    def delx(self):
        print('delx')
        del self.__x
        
    x = property(getx, setx, delx, "I'm the 'x' property.")
    
c = C()
c.x = 20 # setx
print(c.x) # getx

# 利用 property() 方式

class C:
    
    def age(self):
        print('getx')
        return self.__x
    
    age = property(age)
    
    print('age.fget=', age.fget) # <function C.age at ...>
    print('age.fset=', age.fset) # None
    
# 我們可以看到 age 這個 property 物件，是有設定 fget 
    
class C:
    
    def age(self):
        print('getx')
        return self.__x
    
    age = property(age)
    
    # 這裡之所以不能叫 age，是因為 age 必須是 property 物件
    # 如果我們這邊把 setter 方法也叫 age，那們下面會出現錯誤 
    # AttributeError: 'function' object has no attribute 'setter'
    # 推測 decorator 有某種特殊的方式讓 set 方法也可以使用 age()而不出現 AttributeError
    def age_set(self, value):
        print('setx')    
        self.__x = value       
    
    age = age.setter(age_set)
    
    print('age.fget=', age.fget) # <function C.age at ...>
    print('age.fset=', age.fset) # <function C.age_set at 0x000001FC6A4BB130>
    
# 繼續設定 fset，可以看到 property 物件，是有設定 fset 

# 現在來帶入 decorator @property

class C:
    
    @property
    def age(self):
        print('getx')
        return self.__x
    
    print('age.fget=', age.fget) # <function C.age at ...>
    print('age.fset=', age.fset) # None
    
# 使用 @property 這個 decorator 可以獲得相同的結果

class C:
    
    @property
    def age(self):
        print('getx')
        return self.__x
    
    @age.setter   
    def age(self, value):
        print('setx')    
        self.__x = value
    
    print('age.fget=', age.fget) # <function C.age at ...>
    print('age.fset=', age.fset) # <function C.age at ...>
    
# 繼續使用 decorator 為 age decriptor 物件加入 setter 方法


    
# print(C.age)        
# c = C()
# c.age = 40
# print(c.age)        


# 以等同 property 實作

class Property:
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ''

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f'unreadable attribute {self._name}')
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(f"can't set attribute {self._name}")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(f"can't delete attribute {self._name}")
        self.fdel(obj)

    def getter(self, fget):
        prop = type(self)(fget, self.fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def setter(self, fset):
        prop = type(self)(self.fget, fset, self.fdel, self.__doc__)
        prop._name = self._name
        return prop

    def deleter(self, fdel):
        prop = type(self)(self.fget, self.fset, fdel, self.__doc__)
        prop._name = self._name
        return prop

