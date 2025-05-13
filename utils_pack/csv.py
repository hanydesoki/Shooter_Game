from typing import Union, Callable
import os


class FileNotOpenedError(Exception):
    pass


class CSVWriter:

    def __init__(self, path: str,
                 mode: str = "w",
                 sep: str = ",",
                 none_value: Union[int, float, str] = "",
                 has_header: bool = True,
                 encoding: str = None
                 ):

        if not os.path.exists(path):
            raise FileNotFoundError(f"File {path} does not exist.")
        self.path = path

        if mode not in ["w", "a"]:
            raise ValueError(f"opening mode should only be 'w' (write) or 'a' (append). Got {mode} instead")
        
        self.mode = mode
        self.sep = sep
        self.none_value = str(none_value)
        self.has_header = has_header
        self.encoding = encoding

        self.f = None
        self.header_list = None
        self.num_cols = None

    def write(self, *args, **kwargs) -> None:

        # Check if file is opened
        if self.f is None:
            raise FileNotOpenedError(f"File {self.path} not opened yet. Please use the 'with' statement to open it.")

        # Add header if first write and store header list
        if self.header_list is None and self.has_header:
            self.header_list = list(kwargs.keys())
            self.f.write(self.sep.join(self.header_list) + "\n")

        elif self.num_cols is None and not self.has_header:
            self.num_cols = len(args)

        # Check if there is an unknown header
        if self.has_header:
            if len(kwargs) == 0:
                raise ValueError("write method need keyword arguments that match header if 'has_header' param is True")
            for header in list(kwargs.keys()):
                if header not in self.header_list:
                    raise ValueError(
                        f"Cannot add a new header '{header}' after initializing it. Original headers are {self.header_list}.")

            # Write data in the right order
            self.f.write(self.sep.join(map(lambda h: str(kwargs.get(h, self.none_value)), self.header_list)) + "\n")
        else:
            if len(args) == 0:
                raise ValueError("write method need positional arguments that match the number of columns if 'has_header' param is False")
            if len(args) > self.num_cols:
                raise ValueError(f"To much value given. Got {len(args)} values while data have {self.num_cols} columns.")
            elif len(args) < self.num_cols:
                line_list = []
                for i in range(self.num_cols):
                    try:
                        line_list.append(str(args[i]))
                    except IndexError:
                        line_list.append(self.none_value)
                self.f.write(self.sep.join(line_list) + "\n")
            else:
                self.f.write(self.sep.join(map(str, args)) + "\n")

    def __enter__(self) -> "CSVWriter":

        if self.mode == "a":
            if os.path.exists(self.path):
                with open(self.path, "r", encoding=self.encoding) as f:
                    header_line = f.readline().strip()

                header_list = header_line.split(self.sep)

                if len(header_list) > 0:
                    if self.has_header:
                        self.header_list = header_list
                    else:
                        self.num_cols = len(header_list)

        self.f = open(self.path, self.mode, encoding=self.encoding)

        return self

    def __exit__(self, type_, value, traceback) -> None:
        self.f.close()


def read_csv(path: str,
              sep=",",
              has_header: bool = True,
              encoding: str = None,
              **map_casts: Callable) -> dict:
    data = {}

    with open(path, "r", encoding=encoding) as f:
        for i, line in enumerate(f.readlines()):
            if i == 0:
                header_list = line.strip().split(sep)

                for k, header in enumerate(header_list):
                    data[header if has_header else f"{k}"] = []

                if has_header:
                    continue

            for header, value in zip(data.keys(), line.strip().split(sep)):
                data[header].append(map_casts.get(header, lambda x: x)(value))

    return data


