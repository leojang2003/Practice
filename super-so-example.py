# super 是回傳 proxy object

# super(Foo, self).bar() 會尋訪 Foo 的 parent class 直到找到 bar 這個 attribute，如果 bar 是物件的話表示是個 descriptor，self 會 bound 到該 descriptor。呼叫 bar() 則會呼叫 bound method，實則呼叫 function 傳入參數 self 如 bar(self)。

# super() 物件將 class (第一參數) , self (第二參數) 用來 bind，第二個參數 self 的 type，分別儲存於 attribute __thisclass__, __self__ 與 __self_class__ 中:

class Aoo:
    
    def __init__(self):
        print('Aoo.__init__')
        super(Aoo, self).__init__()

    def bar(self):
        print('bar on Aoo')
        
class Goo(Aoo):

    def __init__(self):
        print('Goo.__init__')
        super(Goo, self).__init__()
    
    def bar(self):
        print('bar on Goo')

class Foo(Aoo):

    def __init__(self):
        print('Foo.__init__')
        Aoo.__init__(self)
    
    def bar(self):
        print('bar on Foo')       

class Spam(Foo, Goo):
    
    def __init__(self):
        print('Spam.__init__')
        super(Spam, self).__init__()

    def bar(self):
        print('bar on Spam')
      
        
spam = Spam()
# Spam.__init__
# Foo.__init__
# Aoo.__init__

print(super(Aoo, spam))                 # <super: <class 'Aoo'>, <Spam object>>
print(super(Aoo, spam).__thisclass__)   # <class '__main__.Aoo'>
print(super(Aoo, spam).__self__)        # <__main__.Spam object at 0x107195c10>
print(super(Aoo, spam).__self_class__)  # <class '__main__.Spam'>


# 當 looking up attributes 時，會找尋 __self_class__ attribute 的  __mro__ attribute，從 __thisclass__ 的下個開始，並將結果 bound 起來

# 傳入一個參數的 super() 的 __self__ 與 __self_class__ attributes 會被設為 None 且不能做 lookup:

print('  x   ')

print(super(Aoo))                 # <super: <class 'Aoo'>, NULL>
print(super(Aoo).__thisclass__)   # <class '__main__.Aoo'>
print(super(Aoo).__self__)        # None
print(super(Aoo).__self_class__)  # None
try:
    print(super(Aoo).bar)
    #AttributeError: 'super' object has no attribute 'bar'
except:
    pass

# 因為 object 支援 descriptor protocol，所以我們可以用 bind method 的方式來 bind super()

print(super(Spam).__get__(spam, Spam))          #<super: <class 'Spam'>, <Spam object>>
print(super(Spam).__get__(spam, Spam).bar())    #'bar on Foo'

# 我們可以將 super 存到物件，來尋訪 parent 的 method

class Eggs(Spam):
    pass

Eggs.parent = super(Eggs)
eggs = Eggs()
print(eggs.parent)          # <super: <class 'Eggs'>, <Eggs object>>
print(eggs.parent.bar())    #'bar on Spam'

# 這裡主要是為了簡化每次需傳兩個參數給 super() 的這種作法

class Foo:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        # class-private attribute so subclasses don’t clobber one another
        setattr(cls, f'_{cls.__name__}__parent', super(cls))

    def bar(self):
        return 'bar on Foo'

class Spam(Foo):
    def bar(self):
        return 'spammed: ' + self.__parent.bar()
        
# but that breaks when using a class method (since cls.__parent won’t bind) and has been superseded by Python 3’s super() with zero arguments which picks up the class from a closure:

class Foo:
    def bar(self):
        return 'bar on Foo'

class Spam(Foo):
    def bar(self):
        return 'spammed: ' + super().bar()

# 繼續探索

print(vars(super).keys())

# dict_keys(
#   ['__new__', 
#   '__repr__', 
#   '__getattribute__', 
#   '__get__', 
#   '__init__', 
#   '__thisclass__', 
#   '__self__', 
#   '__self_class__', 
#   '__doc__'])

# super 是覆寫 __getattribute__ 的 class，super 的 instance 提供一個 proxy 物件存取 MRO 中的 methods

class B(object):
    def __repr__(self):
        return "<instance of %s" % self.__class__.__name__
        
class C(B):
    pass
    
class D(C):
    pass
    
d = D()
    
print(super(C,d).__repr__) # <bound method B.__repr__ of <instance of D>
print(super(C,D).__repr__) # <function B.__repr__ at 0x000001838B27B400>

super(C,D).__repr__()
