
'''
dev_eval2.py

  Describe the issues and problem solving in developing eval2()

  Follow the functions from top down, read their docs. 

  Run this file directly for doctest. 

'''

import inspect

def thisfuncname():
  return inspect.stack()[1][3]

def fname(funcname):
  return '<function %s()>'%funcname

def import_module_from_path( path ):
  '''
     to import module abc from 'C:/.../dev/abc.py', use:
     
     abc= import_module_from_path( 'C:/.../dev/abc.py' )  
  '''
  # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
  import importlib.util
  spec = importlib.util.spec_from_file_location("module.name", path)
  module = importlib.util.module_from_spec(spec)
  spec.loader.exec_module( module )
  return module

def exec_builtins( code, scope={} ):
    '''
    
    NOTE: exec() adds a '__builtins__' to scope: 
    
    >>> ret = exec_builtins( 'a="aaa"' )
    >>> ret.keys()
    dict_keys(['__builtins__', 'a'])
    
    '''
    comcode= compile( code, thisfuncname(), 'single', 0, 1)   
    exec( comcode, scope )
    return scope 
    
def exec_scope( code, scope={} ):
    '''
    
    exec seems to keep an internal copy of the
    given scope that survives across multiple runs.    
    
    
    1. scope not given. 
    
    >>> ret1 = exec_scope( 'a="aaa"' )
    >>> ret1
    {'a': 'aaa'}
    
    >>> ret11 = exec_scope( 'b="bbb"') 
    >>> ret11
    {'a': 'aaa', 'b': 'bbb'}
    
    2. scope is given
    
    >>> s2 = {}
    >>> ret2 = exec_scope( 'c="ccc"', s2 )
    >>> ret2 
    {'c': 'ccc'}
    
    >>> s2
    {'c': 'ccc'}
    
    >>> ret22 = exec_scope( 'd=c*2', s2 )
    >>> ret22 
    {'c': 'ccc', 'd': 'cccccc'}
    
    >>> ret23 = exec_scope( 'd="ddd"' )
    >>> ret23 
    {'a': 'aaa', 'b': 'bbb', 'd': 'ddd'}
    
    '''
    
    
#    '''
#    >>> s = {'s2':"sss"}
#    >>> ret3 = exec_scope( 'c="ccc"', s )
#    >>> ret3 
#    {'c': 'ccc'}
#    
#    >>> ret4 = exec_scope( 'd="ddd"', s )
#    >>> ret4 
#    {'c': 'ccc', 'd': 'ddd'}
#        
#    >>> ret5 = exec_scope( 'e="eee"')
#    >>> ret5 
#    {'a': 'aaa', 'b': 'bbb', 'e': 'eee'}
#    
#    So it's stored somewhere for exec_scope to keep adding 
#    vars into it. However, there's no where we can access it:
#    
#    >>> scope # doctest: +IGNORE_EXCEPTION_DETAIL
#    Traceback (most recent call last):
#    NameError: name 'scope' is not defined    
#    
#    >>> 'scope' in dir(exec_scope)
#    False
#    
#    >>> 'scope' in dir(exec_scope.__globals__)
#    False
#    
#    >>> getattr(exec_scope, 'scope')  # doctest: +IGNORE_EXCEPTION_DETAIL
#    Traceback (most recent call last):
#    AttributeError: 'function' object has no attribute 'scope'
#    
#    >>> 
#    '''
    comcode= compile( code, thisfuncname(), 'single', 0, 1)   
    exec( comcode, scope )
    del scope['__builtins__']
    return scope 
    
def exec_scope_cont( code, scope={} ):
    '''
    
    The internal storage of exec's scopes not only 
    survive multiple runs in one doctest namespace, 
    but also survive across multiple doctest namespaces.
    --- unless it's reset like s2 below.
    
    This seems absolutely wrong. 
    
    1. scope not given. 
    
    >>> ret1 = exec_scope( 'a=111' )
    >>> ret1   # expecting {'a': 111}    
    {'a': 111, 'b': 'bbb', 'd': 'ddd'}
    
    >>> ret11 = exec_scope( 'b=222') 
    >>> ret11  # expecting {'a': 111, 'b': 222}
    {'a': 111, 'b': 222, 'd': 'ddd'}
    
    ---------------------------------------
    2. scope is given
    
    >>> s2 = {}
    >>> ret2 = exec_scope( 'c="ccc"', s2 )
    >>> ret2 
    {'c': 'ccc'}
    
    >>> s2
    {'c': 'ccc'}
    
    >>> ret22 = exec_scope( 'd=c*2', s2 )
    >>> ret22 
    {'c': 'ccc', 'd': 'cccccc'}
    
    
    ------------------------------------------
    
    '''
    comcode= compile( code, thisfuncname(), 'exec', 0, 1)   
    exec( comcode, scope )
    del scope['__builtins__']
    return scope 
    
    
def exec_scope_copy( code, scope=None ):
    '''
    Attempt to reset the scope 
    
    1. scope not given. 
    
    >>> ret1 = exec_scope_copy( 'a=111' )
    >>> ret1   # expecting {'a': 111}    
    {'a': 111}
    
    >>> ret11 = exec_scope_copy( 'b=222') 
    >>> ret11  # expecting {'b': 222}
    {'b': 222}
     
    ---------------------------------------
    2. scope is given as {}
    
    >>> s2 = {}
    >>> ret2 = exec_scope_copy( 'c="ccc"', s2 )
    >>> ret2 
    {'c': 'ccc'}
    
    # We didn't expect this to be filled
    # s2 is to give vars, not as a storage
    >>> s2   
    {}
    
    >>> ret22 = exec_scope_copy( 'd="ddd"', s2 )
    >>> ret22 
    {'d': 'ddd'}
    
    ---------------------------------------
    3. scope is given
    
    >>> s3 = {'s':"sss"}
    >>> ret3 = exec_scope_copy( 'c="ccc"', s3 )
    >>> ret3 
    {'s': 'sss', 'c': 'ccc'}
    
    >>> s3   # We didn't expect this to be filled
    {'s': 'sss'}
    
    >>> ret33 = exec_scope_copy( 'd="ddd"', s3 )
    >>> ret33 
    {'s': 'sss', 'd': 'ddd'}
    
    {'s': 'sss'} shows up in the return, which is 
    not what we want
    ------------------------------------------
    
    '''
    
    
    if scope is None: scope = {}
    input_scope= scope.copy()
    #print( input_scope, scope )
    #print( inspect.signature(exec_scope_copy) )
    comcode= compile( code, thisfuncname(), 'single', 0, 1)   
    exec( comcode, input_scope )
    
    del input_scope['__builtins__']
    #print( input_scope, scope )
    
    return input_scope


def exec_scope_copy2( code, scope=None ):
    '''
    Attempt to reset the scope 
    
    1. scope not given. 
    
    >>> ret1 = exec_scope_copy2( 'a=111' )
    >>> ret1   # expecting {'a': 111}    
    {'a': 111}
    
    >>> ret11 = exec_scope_copy2( 'b=222') 
    >>> ret11  # expecting {'b': 222}
    {'b': 222}
     
    ---------------------------------------
    2. scope is given as {}
    
    >>> s2 = {}
    >>> ret2 = exec_scope_copy2( 'c="ccc"', s2 )
    >>> ret2 
    {'c': 'ccc'}
    
    >>> s2   # We didn't expect this to be filled
    {}
    
    >>> ret22 = exec_scope_copy2( 'd="ddd"', s2 )
    >>> ret22 
    {'d': 'ddd'}
    
    ---------------------------------------
    3. scope is given
    
    >>> s3 = {'s':"sss"}
    
    >>> ret3 = exec_scope_copy2( 'c="ccc"', s3 )
    >>> ret3 
    {'c': 'ccc'}
    
    >>> s3   # We didn't expect this to be filled
    {'s': 'sss'}
    
    >>> ret33 = exec_scope_copy2( 'd="ddd"', s3 )
    >>> ret33 
    {'d': 'ddd'}
    
    >>> ret34 = exec_scope_copy2( 'd=s', s3 )
    >>> ret34 
    {'d': 'sss'}
    
    >>> s3  # s3 unchanged
    {'s': 'sss'}
    
    >>> ret35 = exec_scope_copy2( 's=222', s3 )
    >>> ret35 
    {'s': 222}

    >>> s3         # s3 unchanged
    {'s': 'sss'}
    
    ------------------------------------------
    
    '''
    
    
    if scope is None: scope = {}
    
    input_scope= scope.copy()
    working_scope = scope.copy()
    #print( input_scope, scope )
    #print( inspect.signature(exec_scope_copy) )
    comcode= compile( code, thisfuncname(), 'single', 0, 1)   
    exec( comcode, working_scope )
    
    del working_scope['__builtins__']
    #print( input_scope, scope )
    
    # We will compare both scopes and remove 
    # unwanted. Make them into a list so is subscribable
    input_items = list(input_scope.items())
    working_items= list(working_scope.items())
    #print( scope, input_items, working_items )
    
    # Going in reversed order, delete same items
    for i in range( len(input_items)-1, -1, -1):
      if input_items[i] in working_items:
         del working_items[i]
    #print( range( len(input_items)-1, -1) )
    #print( input_items, working_items )
    
    return dict( working_items )
    
    
def exec_scope_multiple_codes( code, scope=None ):
    '''
    Attempt to reset the scope 
    
    1. scope not given. 
    
    >>> ret1 = exec_scope_multiple_codes( 'a=111;aa=222' )
    >>> ret1   # expecting {'a': 111}    
    {'a': 111, 'aa': 222}
    
    >>> ret11 = exec_scope_multiple_codes( 'b=222; bb=333') 
    >>> ret11  # expecting {'b': 222}
    {'b': 222, 'bb': 333}
     
    ---------------------------------------
    2. scope is given as {}
    
    >>> s2 = {}
    >>> ret2 = exec_scope_multiple_codes( 'c="ccc"; cc=0', s2 )
    >>> ret2 
    {'c': 'ccc', 'cc': 0}
    
    >>> s2   # We didn't expect this to be filled
    {}
    
    >>> ret22 = exec_scope_multiple_codes( 'd="ddd"; dd=1', s2 )
    >>> ret22 
    {'d': 'ddd', 'dd': 1}
    
    ---------------------------------------
    3. scope is given
    
    >>> s3 = {'s':"sss"}
    
    >>> ret3 = exec_scope_multiple_codes( 'c="ccc"; cc=2', s3 )
    >>> ret3 
    {'c': 'ccc', 'cc': 2}
    
    >>> s3   # We didn't expect this to be filled
    {'s': 'sss'}
    
    >>> ret33 = exec_scope_multiple_codes( 'd="ddd"; dd=4', s3 )
    >>> ret33 
    {'d': 'ddd', 'dd': 4}
    
    >>> ret34 = exec_scope_multiple_codes( 'd=s; dd=s', s3 )
    >>> ret34 
    {'d': 'sss', 'dd': 'sss'}
    
    >>> s3  # s3 unchanged
    {'s': 'sss'}
    
    >>> ret35 = exec_scope_multiple_codes( 's=222; ss=10', s3 )
    >>> ret35 
    {'s': 222, 'ss': 10}

    >>> s3         # s3 unchanged
    {'s': 'sss'}
    
    ------------------------------------------
    
    '''
    
    
    if scope is None: scope = {}
    
    input_scope= scope.copy()
    working_scope = scope.copy()
    #print( input_scope, scope )
    #print( inspect.signature(exec_scope_copy) )
    comcode= compile( code, thisfuncname(), 'single', 0, 1)   
    exec( comcode, working_scope )
    
    del working_scope['__builtins__']
    #print( input_scope, scope )
    
    # We will compare both scopes and remove 
    # unwanted. Make them list that is subscribable
    input_items = list(input_scope.items())
    working_items= list(working_scope.items())
    #print( scope, input_items, working_items )
    
    # Going in reversed order, delete same items
    for i in range( len(input_items)-1, -1, -1):
      if input_items[i] in working_items:
         del working_items[i]
    #print( range( len(input_items)-1, -1) )
    #print( input_items, working_items )
    
    return dict( working_items )
    
    
def exec_scope_multiple_lines( code, scope=None ):
    '''
    
    Deal with multiline codes.
    
    >>> code = """a=111
    ... aa=222"""
    
    >>> code 
    'a=111\\naa=222'
    
    >>> ret1 = exec_scope_multiple_lines( code ) 
    >>> ret1      
    {'a': 111, 'aa': 222}
    
    >>> code2= """x=3
    ... def f(a=0):
    ...   return (a+10)+x
    ... """ 
    
    >>> ret11 = exec_scope_multiple_lines( code2) 
    >>> ret11['f'](5) 
    18
     
    ---------------------------------------
    2. scope is given as {}
    
    >>> s2 = {}
    >>> ret2 = exec_scope_multiple_lines( 'c="ccc"; cc=0', s2 )
    >>> ret2 
    {'c': 'ccc', 'cc': 0}
    
    >>> s2   # We didn't expect this to be filled
    {}
    
    >>> ret22 = exec_scope_multiple_lines( 'd="ddd"; dd=1', s2 )
    >>> ret22 
    {'d': 'ddd', 'dd': 1}
    
    ---------------------------------------
    3. scope is given
    
    >>> s3 = {'s':"sss"}
    
    >>> ret3 = exec_scope_multiple_lines( 'c="ccc"; cc=2', s3 )
    >>> ret3 
    {'c': 'ccc', 'cc': 2}
    
    >>> s3   # We didn't expect this to be filled
    {'s': 'sss'}
    
    >>> ret33 = exec_scope_multiple_lines( 'd="ddd"; dd=4', s3 )
    >>> ret33 
    {'d': 'ddd', 'dd': 4}
    
    >>> ret34 = exec_scope_multiple_lines( 'd=s; dd=s', s3 )
    >>> ret34 
    {'d': 'sss', 'dd': 'sss'}
    
    >>> s3  # s3 unchanged
    {'s': 'sss'}
    
    >>> ret35 = exec_scope_multiple_lines( 's=222; ss=10', s3 )
    >>> ret35 
    {'s': 222, 'ss': 10}

    >>> s3         # s3 unchanged
    {'s': 'sss'}
    
    ------------------------------------------
    
    4. If code contains items that's already shown in scope:
    
    >>> s4 = {'s':111}
    >>> ret4 = exec_scope_multiple_lines( 's=111; ss=10; sss=s', s4 )
    >>> ret4
    {'ss': 10, 'sss': 111}
    
    Note that the s=111 is missing from the return. This is NOT what 
    we want. 
    '''
    
    
    if scope is None: scope = {}
    
    input_scope= scope.copy()
    working_scope = scope.copy()
    #print( input_scope, scope )
    #print( inspect.signature(exec_scope_copy) )
    comcode= compile( code, fname(thisfuncname()), 'exec', 0, 1)   
    exec( comcode, working_scope )
    
    del working_scope['__builtins__']
    #print( input_scope, scope )
    
    # We will compare both scopes and remove 
    # unwanted. Make them list that is subscribable
    input_items = list(input_scope.items())
    working_items= list(working_scope.items())
    #print( scope, input_items, working_items )
    
    # Going in reversed order, delete same items
    for i in range( len(input_items)-1, -1, -1):
      if input_items[i] in working_items:
         del working_items[i]
    #print( range( len(input_items)-1, -1) )
    #print( input_items, working_items )
    
    return dict( working_items )
    
         
def exec_scope_keep( code, scope=None ):
    '''
    
    This is the final version.
    
    This version keeps the items in scope iff the exact 
    same items is in the code. 
    
    >>> code = """a=111
    ... aa=222"""
    
    >>> code 
    'a=111\\naa=222'
    
    >>> ret1 = exec_scope_keep( code ) 
    >>> ret1      
    {'a': 111, 'aa': 222}
    
    >>> code2= """x=3
    ... def f(a=0):
    ...   return (a+10)+x
    ... """ 
    
    >>> ret11 = exec_scope_keep( code2) 
    >>> ret11['f'](5) 
    18
     
    ---------------------------------------
    2. scope is given as {}
    
    >>> s2 = {}
    >>> ret2 = exec_scope_keep( 'c="ccc"; cc=0', s2 )
    >>> ret2 
    {'c': 'ccc', 'cc': 0}
    
    >>> s2   # We didn't expect this to be filled
    {}
    
    >>> ret22 = exec_scope_keep( 'd="ddd"; dd=1', s2 )
    >>> ret22 
    {'d': 'ddd', 'dd': 1}
    
    ---------------------------------------
    3. scope is given
    
    >>> s3 = {'s':"sss"}
    
    >>> ret3 = exec_scope_keep( 'c="ccc"; cc=2', s3 )
    >>> ret3 
    {'c': 'ccc', 'cc': 2}
    
    >>> s3   # We didn't expect this to be filled
    {'s': 'sss'}
    
    >>> ret33 = exec_scope_keep( 'd="ddd"; dd=4', s3 )
    >>> ret33 
    {'d': 'ddd', 'dd': 4}
    
    >>> ret34 = exec_scope_keep( 'd=s; dd=s', s3 )
    >>> ret34 
    {'d': 'sss', 'dd': 'sss'}
    
    >>> s3  # s3 unchanged
    {'s': 'sss'}
    
    >>> ret35 = exec_scope_keep( 's=222; ss=10', s3 )
    >>> ret35 
    {'s': 222, 'ss': 10}

    >>> s3         # s3 unchanged
    {'s': 'sss'}
    
    ------------------------------------------
    
    4. If code contains items that's already shown in scope:
    
    >>> s4 = {'s':111}
    >>> ret4 = exec_scope_keep( 's=111; ss=10; sss=s', s4 )
    >>> ret4
    {'s': 111, 'ss': 10, 'sss': 111}
    '''
    
    # If the code is self-sufficient to run w/o scope, we 
    # skip the scope entirely to avoid the complication 
    try:
    
        _scope={}
        comcode= compile( code, fname(thisfuncname()), 'exec', 0, 1)   
        exec( comcode, _scope )
        del _scope['__builtins__']
        return _scope
        
    except:   
     
      if scope is None: scope = {}    
    
      # Make 2 local copies of scope
      input_scope= scope.copy()
      working_scope = scope.copy()
      
      # Working on one of them
      comcode= compile( code, fname(thisfuncname()), 'exec', 0, 1)   
      exec( comcode, working_scope )
    
      # Remove the key '__builtins__' injected by exec()
      del working_scope['__builtins__']
      
      # We will compare both scopes and remove items 
      # of scope from the working_scope. 
      # Make them list so is subscribable
      input_items = list(input_scope.items())
      working_items= list(working_scope.items())
      
      # Going in reversed order, delete same items
      for i in range( len(input_items)-1, -1, -1):
        if input_items[i] in working_items:
           del working_items[i]
      
      return dict( working_items )
    
def eval2( code, scope=None ):
    '''
    
    Rename the final version *exec_scope_keep* to eval2.

    An alternative of exec/eval. This version returns a dict
    containing all the {<var>:<val>} defined by code. 
    
    NOTE: 
    
    -- Unlike exec(), the scope is used to provide variables, 
       not to update. It remains the same after this exectuation.      
    
    >>> code = """a=111
    ... aa=222"""
    
    >>> code 
    'a=111\\naa=222'
    
    >>> ret1 = eval2( code ) 
    >>> ret1      
    {'a': 111, 'aa': 222}
    
    >>> code2= """x=3
    ... def f(a=0):
    ...   return (a+10)+x
    ... """ 
    
    >>> ret11 = eval2( code2) 
    >>> ret11['f'](5) 
    18
     
    ---------------------------------------
    2. scope is given as {}
    
    >>> s2 = {}
    >>> ret2 = eval2( 'c="ccc"; cc=0', s2 )
    >>> ret2 
    {'c': 'ccc', 'cc': 0}
    
    >>> s2   
    {}
    
    >>> ret22 = eval2( 'd="ddd"; dd=1', s2 )
    >>> ret22 
    {'d': 'ddd', 'dd': 1}
    
    ---------------------------------------
    3. scope is given
    
    >>> s3 = {'s':"sss"}
    
    >>> ret3 = eval2( 'c="ccc"; cc=2', s3 )
    >>> ret3 
    {'c': 'ccc', 'cc': 2}
    
    >>> s3   
    {'s': 'sss'}
    
    >>> ret33 = eval2( 'd="ddd"; dd=4', s3 )
    >>> ret33 
    {'d': 'ddd', 'dd': 4}
    
    >>> ret34 = eval2( 'd=s; dd=s', s3 )
    >>> ret34 
    {'d': 'sss', 'dd': 'sss'}
    
    >>> s3  
    {'s': 'sss'}
    
    >>> ret35 = eval2( 's=222; ss=10', s3 )
    >>> ret35 
    {'s': 222, 'ss': 10}

    >>> s3         
    {'s': 'sss'}
    
    ------------------------------------------
    
    4. If code contains items that's already shown in scope:
    
    >>> s4 = {'s':111}
    >>> ret4 = eval2( 's=111; ss=10; sss=s', s4 )
    >>> ret4
    {'s': 111, 'ss': 10, 'sss': 111}
    '''
    
    # If the code is self-sufficient to run w/o scope, we 
    # skip the scope entirely to avoid the complication 
    try:
    
        _scope={}
        comcode= compile( code, fname(thisfuncname()), 'exec', 0, 1)   
        exec( comcode, _scope )
        del _scope['__builtins__']
        return _scope
        
    except:   
     
      if scope is None: scope = {}    
    
      # Make 2 local copies of scope
      #
      input_scope= scope.copy()
      working_scope = scope.copy()
      
      # Working on one of them
      #
      comcode= compile( code, fname(thisfuncname()), 'exec', 0, 1)   
      exec( comcode, working_scope )
    
      # Remove the key '__builtins__' injected by exec()
      #
      del working_scope['__builtins__']
      
      # Compare both scopes and remove all items 
      # of input_scope from working_scope. 
      # Make them list so is subscribable
      #
      input_items = list(input_scope.items())
      working_items= list(working_scope.items())
      
      # Going in reversed order, delete same items
      #
      for i in range( len(input_items)-1, -1, -1):
        if input_items[i] in working_items:
           del working_items[i]
      
      return dict( working_items )
    
         
              
if __name__=='__main__':

 
  import os
  path= os.path.dirname(os.path.abspath(__file__))
  path = os.path.split(path)[0]
  path = os.path.join( path, 'assure', 'assure.py')  
  #print( 'path= ', path)
  
  assure = import_module_from_path( path )
  assure.testmod()      
  
  
#  print( 'Doing doctesting. If nothing else shows up, means all pass...' )
#  import doctest
#  doctest.testmod()      
