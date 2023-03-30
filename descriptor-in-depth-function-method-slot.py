# Member objects and __slots__
# 當一個 class 定義 __slots__，他會以固定長度的陣列取代 instance dictionaries，這樣有幾個好處:

# 1. 提供立即偵測錯誤的 attribute assignment，因為只有 __slots__ 裡面定義的才允許

class Vehicle:
    __slots__ = ('id_number', 'make', 'model')
try:

    auto = Vehicle()
    auto.id_nubmer = 'VYE483814LQEX'  
    #AttributeError: 'Vehicle' object has no attribute 'id_nubmer'
except:
    pass

# 2. Helps create immutable objects where descriptors manage access to private attributes stored in __slots__:
# 2. 當 descriptor 對 __slots__ 的 private attribute 做管制時，協助建立 immutable 物件

class Immutable:

    __slots__ = ('_dept', '_name')          # Replace the instance dictionary

    def __init__(self, dept, name):
        self._dept = dept                   # Store to private attribute
        self._name = name                   # Store to private attribute
    
    @property                               # Read-only descriptor
    def dept(self):
        return self._dept

    @property
    def name(self):                         # Read-only descriptor
        return self._name

mark = Immutable('Botany', 'Mark Watney')
try:
    print(mark.__dict__)
    # AttributeError: 'Immutable' object has no attribute '__dict__'. Did you mean: '__dir__'
    # __dict__ 被取代了
except:
    pass

try:
    print(mark.dept) # 'Botany'

    # mark.dept = 'Space Pirate' # AttributeError: can't set attribute 'dept'

    mark.location = 'Mars'
    # 'Immutable' object has no attribute 'location'
    
except:
    pass
    

# 3. 節省記憶體
# 4. 提升速度
# 5. 搭配 functools.cached_property() 需要 instance dictionary 以運作:

from functools import cached_property

class CP:
    __slots__ = ()                          # Eliminates the instance dict

    @cached_property                        # Requires an instance dict
    def pi(self):
        return 4 * sum((-1.0)**n / (2.0*n + 1.0)
                       for n in reversed(range(100_000)))



try:
    CP().pi
    #TypeError: No '__dict__' attribute on 'CP' instance to cache 'pi' property.
except:
    pass
    


'''
