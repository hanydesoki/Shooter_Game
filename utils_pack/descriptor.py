from typing import Callable


class NumberAttribute:

    def __init__(self, extra_checks: list[list[Callable, str]] = None, number_type: type = None):

        if number_type not in [int, float, None]:
            raise ValueError(f"'number_type' should be either int or float. Got {repr(number_type)} instead.")
        
        self.number_types = (int, float) if number_type is None else (number_type,)

        self.extra_checks: list[list[Callable, str]] = extra_checks if extra_checks is not None else []    

    def __set_name__(self, owner, name) -> None:
        self.public_name: str = name
        self.private_name: str = "_" + name

    def __get__(self, obj, objType=None) -> float:
        return getattr(obj, self.private_name)
    
    def __set__(self, obj, value: float):
        if (not isinstance(value, self.number_types)):
            raise TypeError(
                f"{type(obj).__name__} {repr(self.public_name)} attribute should be an {' or '.join(map(lambda t: t.__name__, self.number_types))}. Got {repr(value)} instead."
            )
        
        for check, error_msg in self.extra_checks:
            if not check(value):
                raise TypeError(
                    f"{type(obj).__name__} {repr(self.public_name)} attribute {error_msg}. Got {repr(value)} instead."
                )
        
        setattr(obj, self.private_name, value)
