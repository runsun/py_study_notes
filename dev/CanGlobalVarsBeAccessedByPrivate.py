'''
During coding found that global vars don't seem to be accessible from a private func. 
Let's check

Answer: don't seem to have any problem 

'''
global Im_global
Im_global = 100

class Cls(object):
    def __private(self):
        print( 'In __private(), Im_global=', Im_global )
    def run(self):
        print( 'In run(), Im_global=', Im_global )
        self.__private()
cls = Cls()
cls.run()  


class Cls2(object):
    def __private(self, Im_global):
        print( 'In __private(), Im_global=', Im_global )
    def run(self):
        print( 'In run(), Im_global=', Im_global )
        self.__private(Im_global)
cls2 = Cls2()
cls2.run()  
