from typing import Any, Union, List

def union_check(var_union, var_type):
    return isinstance(var_union, var_type.__args__)

def list_check(var_list, var_type):
    for var in var_list:
        if not isinstance(var, var_type.__dict__["__args__"]):
            return False
    return True
    
def static():
    def decorator(func):
        def wrapper(*args, **kwargs):
            variables = args+tuple(kwargs.values())

            for var, var_type, var_name in zip(variables, \
                            tuple(func.__annotations__.values()), \
                            tuple(func.__annotations__.keys())):
                

                if var_type == Any: continue
                
                try:
                    if var_type.__origin__ is Union:
                        if union_check(var, var_type):
                            continue
                        raise TypeError(f'in function "{func.__name__}" variable {var_name} != {var_type}')
                except AttributeError: pass # если переменная не Union то мы обратимся к несуществующиму полю
                
                try:
                    if var_type.__dict__["__origin__"] is list:
                        if list_check(var, var_type):
                            continue
                        raise TypeError(f'in function "{func.__name__}" variable {var_name} != {var_type}')
                except KeyError: pass
                
                if not isinstance(var, var_type):
                    raise TypeError(f'in function "{func.__name__}" variable {var_name} != {var_type}')
                
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator    

if __name__ == "__main__":
    @static()
    def fn(x:List[int], y: int, z: str, v: Union[int, float] = 0): pass  
    fn([1,2,3], 5, z="15", v=1.1) # ok
    fn([1,2,3, "4"], "5", z=15, v=[1.1, 1.2]) # error
