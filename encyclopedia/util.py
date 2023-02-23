import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries currently saved.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    with open(filename) as file:
        new_lines = []
        contador = 0
        lineas = file.readlines()
        for linea in lineas:
            if linea.isspace():
                contador += 1
                if contador == 2:
                    contador = 1
                    continue
                new_lines.append(linea)
                continue
            else:
                new_lines.append(linea)

        with open(filename, "w") as new_file:
            for linea in new_lines:
                new_file.write(linea)
                contador = 0
    


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None. Te retorna lo que dice cada enciclopedia.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
