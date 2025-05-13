import os


class ContextDirectory:

    def __init__(self, target_directory: str):
        self.original_directory = os.getcwd()

        self.current_directory = self.original_directory

        self.target_directory = target_directory

    def __enter__(self):
        os.chdir(self.target_directory)

        self.current_directory = os.getcwd()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_directory)


def search_in_directory(keyword: str, path: str = None) -> None:
    search_path = path if path is not None else os.getcwd()

    with ContextDirectory(search_path) as cd:
        for name in os.listdir(cd.current_directory):
            if keyword.lower() in name.lower():
                print(os.path.join(cd.current_directory, name))

            if os.path.isdir(name):
                search_in_directory(keyword, name)
