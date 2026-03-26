import json
import os
import hashlib
import re

CACHE_FILE = "context_cache.json"


def load_cache():

    if not os.path.exists(CACHE_FILE):
        return {}

    with open(CACHE_FILE, "r") as f:
        return json.load(f)


def save_cache(data):

    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)




def normalize(text: str):

    text = text.lower()

    text = text.strip()

    text = re.sub(r"\s+", " ", text)

    return text


def make_hash(text):

    clean = normalize(text)

    return hashlib.md5(clean.encode()).hexdigest()

def get_cache(tool, text):

    data = load_cache()

    h = make_hash(text)

    key = f"{tool}:{h}"

    return data.get(key)


def set_cache(tool, text, value):

    data = load_cache()

    h = make_hash(text)

    key = f"{tool}:{h}"

    data[key] = value

    save_cache(data)
