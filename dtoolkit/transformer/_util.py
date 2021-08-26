def snake_to_camel(snake_str):
    components = snake_str.split("_")
    components = (x.title() for x in components)
    return "".join(components)
