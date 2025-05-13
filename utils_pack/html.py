from typing import Any


def generate_html(tag: str, value: Any = None, **arguments) -> str:
    value = value if value is not None else ""

    if "style" in arguments:
        if type(arguments["style"]) == dict:
            arguments["style"] = "; ".join([f"{prop}: {prop_arg}" for prop, prop_arg in arguments["style"].items()])

    for special_arg in ["_class", "_id", "class_", "id_"]:
        if special_arg in arguments:
            arguments[special_arg.strip("_")] = arguments[special_arg]
            del arguments[special_arg]

    string_arguments = " ".join([f'{param}="{arg}"' for param, arg in arguments.items() if arg is not True])
    end_arguments = " ".join([param for param, arg in arguments.items() if arg is True])

    html_string = f"<{tag} {string_arguments} {end_arguments}>{value}</{tag}>"

    return html_string

