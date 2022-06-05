import json
import os

def add_data(new_data, filename):
    existing_data = read_data(filename)
    _check_ids(existing_data, new_data)
    updated_data = existing_data + new_data
    _write_data(updated_data, filename)

def add_data_ignore_id(new_data, filename):
    existing_data = read_data(filename)
    updated_data = existing_data + new_data
    _write_data(updated_data, filename)

def add_single_entry(new_entry, filename):
    add_data([new_entry], filename)

def read_entry(id, filename):
    data = read_data(filename)
    for entry in data:
        if entry['id'] == id:
            return entry

def read_data(filename):
    filepath = _to_path(filename)
    data = []
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as f:
            data = json.load(f)
    return data

def _write_data(data, filename):
    filepath = _to_path(filename)
    with open(filepath, 'w') as f:
        json.dump(data, f)

def _check_ids(existing_data, new_data):
    _check_ids_are_present(existing_data, new_data)
    _check_for_duplicate_ids(existing_data, new_data)

def _check_ids_are_present(existing_data, new_data):
    if not all(map(lambda entry: 'id' in entry, existing_data)):
        raise ValueError('entry without id in existing data')
    if not all(map(lambda entry: 'id' in entry, new_data)):
        raise ValueError('entry without id in new data')

def _check_for_duplicate_ids(existing_data, new_data):
    ids_new_data_list = _get_ids(new_data)
    ids_new_data = set(ids_new_data_list)
    if len(ids_new_data) != len(ids_new_data):
        raise ValueError('duplicate id in new data')
    ids_existing_data = set(_get_ids(existing_data))
    for id_new_data in ids_new_data:
        if id_new_data in ids_existing_data:
            raise ValueError('object with id already present')
    
def _get_ids(data):
    return list(map(lambda x: x['id'], data))

def _to_path(filename):
    return filename + '.json'
