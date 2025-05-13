from typing import Iterable, Callable, Any, Generator


class Group:

    def __init__(self, items: Iterable, by: Callable):

        self.items = items

        self.groups: dict[Any, tuple[Any]] = {}

        for item in items:
            group_key: Any = by(item)

            if group_key not in self.groups:
                self.groups[group_key] = ()

            self.groups[group_key] += (item,)

    def aggregation(self, aggregation: Callable) -> dict:
        return {key: aggregation(group) for key, group in self.groups.items()}
    
    def get_groups(self) -> dict[Any, tuple[Any]]:
        return self.groups.copy()
    
    def __getitem__(self, group_key: Any) -> tuple[Any]:
        return self.groups.get(group_key)
    
    def __iter__(self) -> Generator:
        for group_key, group in self.groups.items():
            yield group_key, group

    def __str__(self):
        return f"Group({self.groups})"
            

if __name__ == "__main__":
    # Example group people by their age
    persons: list[dict] = [
        {"age": 20},
        {"age": 12},
        {"age": 9},
        {"age": 43},
        {"age": 15},
        {"age": 48},
        {"age": 3}
    ]
    age_groups: Group = Group(
            persons,
            by=lambda p: f"{p['age'] // 10 * 10}-{p['age'] // 10 * 10 + 10}"
        )
    print(age_groups, end="\n" * 2)

    for age_range, person_group in age_groups:
        print(f"Age group {age_range} --> {person_group}")

    print()

    age_group_counts: dict[str, int] = age_groups.aggregation(len)

    print(age_group_counts)