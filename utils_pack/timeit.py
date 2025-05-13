"""
Module with time execution related functionalities.

DESOKI Hany
"""

from typing import Callable, Any, Union
import time
import functools


def timer(func: Callable) -> Callable:
    """
    Simple decorator that will display the execution time for each call.
    """
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        try:
            print(f"{func.__name__} execution time: {end_time - start_time} s")
        except AttributeError:
            print(f"{func} execution time: {end_time - start_time} s")

        return result

    return wrapper


class TimeReport:

    function_cumulated_times = {}
    context_cumulated_times = {}

    def __init__(self, *args: Union[Callable, str]):
        """
        Decorator and Context manager that allow to time functions or code section 
        and display a report (using report method) that show for each the mean time execution.
        - Use as decorator on function or method:

        
        @TimeReport

        def load_model():
            ...

        - Use as context manager on any code section:

        with TimeReport("Image processing"):
            ...

        This allow to store de execution time on each call/pass in the class itself.

        When its finished, we can use the class method TimeReport.report and print the result.
        It will display the average time for each function / context:

            print(TimeReport.report())

        >>> Mean time execution for each functions and contexts:

            load_model ------------- 0.465 s (1 call)

            Image processing ------- 0.31 s (624 calls)
        

        To make sure to print the report, you can wrap the whole script in a try/finally block and
        call the report method in the finally block so it can still display the report even when 
        the code raise an exception like a KeyboardInterrupt for example (ctrl c).
        """
        self.func = None
        self.context_name = None
        self.start_time = None

        if callable(args[0]):
            self.func = args[0]
            TimeReport.function_cumulated_times[self.func] = {
                "cumulated_time": 0,
                "number_of_calls": 0
            }

        elif isinstance(args[0], str):
            self.context_name = args[0]
            if self.context_name not in TimeReport.context_cumulated_times:
                TimeReport.context_cumulated_times[self.context_name] = {
                    "cumulated_time": 0,
                    "number_of_calls": 0
                }

    def __get__(self, obj, type=None):
        return functools.partial(self, obj)

    def __call__(self, *args, **kwargs) -> Any:
        if not hasattr(self, 'func'):
            self.func = args[0]
            return self

        start_time = time.perf_counter()
        result = self.func(*args, **kwargs)
        end_time = time.perf_counter()

        self._add_func_time(self.func, start_time, end_time)

        return result

    def __enter__(self) -> "TimeReport":
        if self.context_name is None:
            raise TypeError("TimeReport constructor used as context manager must have a string as a parameter")

        self.start_time = time.perf_counter()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.perf_counter()

        self._add_context_time(self.context_name, self.start_time, end_time)
        self.start_time = None

    @classmethod
    def report(cls) -> str:
        """
        Call this class method to get as string the average execution time report of all
        calls / contexts. 
        """
        report_result = "Mean time execution for each functions and contexts:\n\n"
        for func, cumulated_times in cls.function_cumulated_times.items():
            try:
                func_name = func.__name__
            except AttributeError:
                func_name = func

            try:
                report_result += f"{func_name :-<30}: \
                {cumulated_times['cumulated_time'] / cumulated_times['number_of_calls']  :->30} s\
                 ({cumulated_times['number_of_calls']} call(s))\n"
            except ZeroDivisionError:
                report_result += f"{func_name :-<30}: \
                {'No calls':->30}\n"

        for context_name, cumulated_times in cls.context_cumulated_times.items():

            try:
                report_result += f"{context_name :-<30}: \
                {cumulated_times['cumulated_time'] / cumulated_times['number_of_calls']  :->30} s\
                 ({cumulated_times['number_of_calls']} call(s))\n"
            except ZeroDivisionError:
                report_result += f"{context_name :-<30}: \
                {'No calls':->30}\n"

        return report_result

    @classmethod
    def _add_func_time(cls, func: Callable, start_time: float, end_time: float) -> None:
        cls.function_cumulated_times[func]["cumulated_time"] += end_time - start_time
        cls.function_cumulated_times[func]["number_of_calls"] += 1

    @classmethod
    def _add_context_time(cls, context_name: str, start_time: float, end_time: float) -> None:
        cls.context_cumulated_times[context_name]["cumulated_time"] += end_time - start_time
        cls.context_cumulated_times[context_name]["number_of_calls"] += 1


# This example show a performance test between builtin and custom python functions
if __name__ == "__main__":

    @TimeReport
    def initiate_list(n: int) -> list:
        return list(range(n))
    
    @TimeReport
    def is_in_array(arr: list, element) -> bool:
        for e in arr:
            if e == element:
                return True
            
        return False
    
    @TimeReport
    def custom_sum(arr) -> float:
        result = 0
        for e in arr:
            result += e

        return result
    

    for _ in range(100):
        l = initiate_list(10000)

        isin_cust = is_in_array(l, 11000)

        with TimeReport("Builtin python 'in'"):
            isin_builtin = 11000 in l

        with TimeReport("Builtin sum"):
            builtin_sum = sum(l)

        cust_sum = custom_sum(l)

    print(TimeReport.report())
