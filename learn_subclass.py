'''
Learn_subclass.py

instmethod --- instance-bound 

Dig into the scope and protection layers of class's _protected
and __private methods.

-- protected method: a func prefixed with "_" 
-- prrivate method: a func prefixed with "__" 

-- A child CAN access parent's protected methods as usual

-- A child can't access parent's private methods directly
   They have to be accessed by adding a prefix of 
   
   _<parent_name>

-- Parent's private methods CANNOT be overridden. Even you 
    re-defined them in child, child still run Papa's copy.

   Example: doctest.DocTestRunner.__run()

     It is called by DocTestRunner.run(). Since __run() 
     cannot be overridden, even if you re-define it in
     your subclass, .run() still use the original copy
     = DocTestRunner.__()

-- __<var>__ (flanked by double underscore) is NOT a private

#========================================================

We will also study staticmethod, classmethod etc
https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod



'''

def learn_private():
   '''
    >>> class Papa(object):
    ...    def instmethod(self): print('I am Papa.instmethod')
    ...    def _protected(self): print('I am Papa.protected') 
    ...    def __private(self): print('I am Papa.private')
    ...    def __secret__(self): print('I am Papa.secret')
    ...    def prn(self):
    ...         print('--- Running Papa prn() --- ')
    ...         self.instmethod()
    ...         self._protected()
    ...         self.__private()
    ...         self.__secret__()

    ### ===============================
    ### A simple Child
    ### ===============================

    >>> class Child(Papa):
    ...    def foo(self):
    ...        self._protected()
    ...
    ...    def bar(self):
    ...        self.__private()
    ...  
    ...    def daa(self):
    ...        self.__secret__()

    ###---------------------------
    ### Accessing Papa's protected
    ###---------------------------

    >>> c = Child()

    >>> c.foo()
    I am Papa.protected

    ==> Papa's _protected can be accessed as normal

    ###---------------------------
    ### Accessing Papa's private
    ###---------------------------

    >>> c._protected()
    I am Papa.protected

    ==> Can't access Papa's private methods directly :

    >>> c.bar()
    Traceback (most recent call last):
        File "C:\python37\lib\doctest.py", line 1329, in __run
        compileflags, 1), test.globs)
        File "<doctest __main__.learn[4]>", line 1, in <module>
        c.bar()
        File "<doctest __main__.learn[1]>", line 6, in bar
        self.__private()
    AttributeError: 'Child' object has no attribute '_Child__private'

    ==> But you can by adding a '_Parent_' prefix :

    >>> c._Papa__private()
    I am Papa.private

    ###-----------------------------
    ### Accessing Papa's __secret__
    ###-----------------------------

    >>> c.daa()
    I am Papa.secret

    ==> Papa's __secret__ can be accessed as normal


    >>> c.prn() # doctest: +NORMALIZE_WHITESPACE
    --- Running Papa prn() ---
    I am Papa.instmethod
    I am Papa.protected
    I am Papa.private
    I am Papa.secret

    ### ---------------------------------
    ### A Child override parent's methods
    ### ---------------------------------

    >>> class Child2(Papa):
    ...    def foo(self):
    ...        self._protected()
    ...
    ...    def bar(self):
    ...        self.__private()
    ...
    ...    def instmethod(self): print('I am Child.normal')
    ...    def _protected(self): print('I am Child.protected') 
    ...    def __private(self): print('I am Child.private')
    ...    def __secret__(self): print('I am Child.secret') 

    >>> c2 = Child2()

    ==> Papa's private methods CANNOT be overridden. Even you re-defined
        them, child still run Papa's copy.

    >>> c2.prn() # doctest: +NORMALIZE_WHITESPACE
    --- Running Papa prn() ---
    I am Child.normal
    I am Child.protected
    I am Papa.private
    I am Child.secret
    '''


def learn_static():
    '''
    #===========================================

    instance method --- bound to instance
    classmethod   --- bound to class
    staticmethod  --- no binding

    https://stackoverflow.com/questions/136097/difference-between-staticmethod-and-classmethod


    >>> class A(object):
    ...    def foo(self, x):
    ...        print("executing foo(%s, %s)" % (self, x))
    ...
    ...    @classmethod
    ...    def class_foo(cls, x):
    ...        print("executing class_foo(%s, %s)" % (cls, x))
    ...
    ...    @staticmethod
    ...    def static_foo(x):
    ...        print("executing static_foo(%s)" % x)    

    >>> a = A()

    >>> a.foo(1)  # doctest: +ELLIPSIS
    executing foo(<__main__.A object at ...)

    >>> a.class_foo(1)
    executing class_foo(<class '__main__.A'>, 1)

    >>> a.static_foo(1)
    executing static_foo(1)

    >>> A.static_foo('hi')
    executing static_foo(hi)

    '''


def learn_private_static():
    '''
    >>> class Papa(object):
    ...    def inst_norm(self): print('inst, normal')
    ...    def _inst_prot(self): print('inst, prot') 
    ...    def __inst_priv(self): print('inst, priv')
    ...    def __inst_norm__(self): print('inst, __normal__')
    ...
    ...    @classmethod
    ...    def cls_norm(self): print('cls, normal')
    ...    @classmethod
    ...    def _cls_prot(self): print('cls, prot') 
    ...    @classmethod
    ...    def __cls_priv(self): print('cls, priv')
    ...    @classmethod
    ...    def __cls_norm__(self): print('cls, __normal__')
    ...
    ...    @staticmethod
    ...    def stat_norm(self): print('stat, normal')
    ...    @staticmethod
    ...    def _stat_prot(self): print('stat, prot') 
    ...    @staticmethod
    ...    def __stat_priv(self): print('stat, priv')
    ...    @staticmethod
    ...    def __stat_norm__(self): print('stat, __normal__')
    
    ...    def prn(self):
    ...         print('--- Running Papa prn() --- ')
    ...         print( '... inst ...')
    ...         self.inst_norm()
    ...         self._inst_prot()
    ...         self.__inst_priv()
    ...         self.__inst_norm__() 
    ...
    ...         print( '... class ...')
    ...         self.class_norm()
    ...         self._class_prot()
    ...         self.__class_priv()
    ...         self.__class_norm__()
    ... 
    ...         print( '... static ...')
    ...         self.stat_norm()
    ...         self._stat_prot()
    ...         self.__stat_priv()
    ...         self.__stat_norm__() 

    >>> class Kid(Papa):
    ...    def inst__norm(self): self.inst_norm()
    ...    def _inst__prot(self): self._inst_prot()
    ...    def __inst__priv(self): self.__inst_priv()
    ...    def __inst__norm__(self): self.__inst_norm__()
    ...
    ...    @classmethod
    ...    def cls__norm(self): self.cls_norm()
    ...    @classmethod
    ...    def _cls__prot(self): self._cls_prot()
    ...    @classmethod
    ...    def __cls__priv(self): self.__cls_priv()
    ...    @classmethod
    ...    def __cls__norm__(self): self.__cls_norm__()
    ...
    ...    @staticmethod
    ...    def stat__norm(self): self.stat_norm()
    ...    @staticmethod
    ...    def _stat__prot(self): self._stat_prot()
    ...    @staticmethod
    ...    def __stat__priv(self): self.__stat_priv()
    ...    @staticmethod
    ...    def __stat__norm__(self): self.__stat_norm__()

    >>> kid = Kid()

    >>> kid.inst__norm()
    inst, normal
    >>> kid._inst__prot()
    inst, prot
    >>> kid.__inst__priv() # doctest: +NORMALIZE_WHITESPACE
    Exception raised:
    Traceback (most recent call last):
      File "C:\Program Files\Python38\lib\doctest.py", line 1336, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest __main__.learn_private_static[5]>", line 1, in <module>
        kid.__inst__priv()
    AttributeError: 'Kid' object has no attribute '__inst__priv'
    >>> kid.__inst__norm__()
    inst, __normal__

    >>> kid.cls__norm()
    cls, normal
    >>> kid._cls__prot()
    cls, prot
    >>> kid.__cls__priv() # doctest: +NORMALIZE_WHITESPACE
    Exception raised:
    Traceback (most recent call last):
      File "C:\Program Files\Python38\lib\doctest.py", line 1336, in __run
        exec(compile(example.source, filename, "single",
      File "<doctest __main__.learn_private_static[9]>", line 1, in <module>
        kid.__cls__priv() # doctest: +NORMALIZE_WHITESPACE
    AttributeError: 'Kid' object has no attribute '__cls__priv'
    >>> kid.__cls__norm__()
    cls, __normal__

    '''


if __name__ == '__main__':

    import doctest 
    print( '--- Doing doctest on '+ __file__+' ---')
    doctest.testmod()
    print( '--- Done ---')
    