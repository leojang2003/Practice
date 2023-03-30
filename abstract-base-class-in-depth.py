# abstract class 就是有 abstract method 的 class，這些 abstract method 被宣告但是沒被實作
# 簡單來說，可以將 abstract class 理解成是一個 subclass 必須要有的 framework

from abc import ABC, abstractmethod

class Employee(ABC):

    @abstractmethod
    def arrive_at_work(self):
        pass
        
# 注意這裡的 abstract method 不應該有實作，所以僅為 pass

class Manager(Employee):
    
    def show_up(self):
        print("I'm here")
    
    # 注意這裡繼承 abc 的類別必須覆寫 abstractmethod
    def arrive_at_work(self):
        print('Manager here')
        pass
        
glasscock = Manager()

class Supervisor(Employee):
        
    # 不同的子類別可以有不同的 abstractmethod 實作方式
    def arrive_at_work(self):
        print('Supervisor here')
        pass

#        
# 在 abstract method 可以定義參數
#

class Employee(ABC):
    
    # 新增參數
    @abstractmethod
    def arrive_at_work(self, time):
        pass        

class Manager(Employee):
    
    def show_up(self):
        print("I'm here")
    
    # 覆寫 abstractmethod 同樣需要參數
    def arrive_at_work(self, time):
        print('Manager here at ', time)
        pass
        
glasscock = Manager()
glasscock.arrive_at_work('08:00')

class Supervisor(Employee):
        
    # 注意 ! 子類別覆寫 abstractmethod 時，可以有額外的參數
    def arrive_at_work(self, time, viechle):
        print('Supervisor here at time', time, 'by', viechle)
        pass
        
jim = Supervisor()
jim.arrive_at_work('09:00', 'Tesla')
        
