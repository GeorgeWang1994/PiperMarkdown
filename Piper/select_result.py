import os, re, io


def get_config_item_path(dir, name):
    default_dir = os.path.join(dir, name)
    return default_dir


def read_file(filepath):
    with io.open(filepath, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(filepath, content):
    with io.open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)