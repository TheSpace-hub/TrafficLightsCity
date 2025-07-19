from typing import Callable, Self


class Checker:
    _instance: Self = None

    def __init__(self):
        self.functions: dict[str, Callable[[dict, dict], tuple[bool, str]]] = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __call__(self, tfl_type):
        def decorator(func):
            self.functions[tfl_type] = func

            def wrapper(request: dict, response: dict):
                return func(request, response)

            return wrapper

        return decorator

    def check(self, tfl_type: str, request: dict, response: dict) -> tuple[bool, str] | None:
        for current_type, func in self.functions.items():
            if tfl_type == current_type:
                return func(request, response)
        return None
