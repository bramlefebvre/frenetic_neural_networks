import json
import os
import uuid

def add_data(new_data, filename):
    existing_data = read_data(filename)
    _check_ids(existing_data, new_data)
    add_ids_if_not_present(new_data)
    updated_data = existing_data + new_data
    write_array(updated_data, filename)

def add_data_no_id(new_data, filename):
    existing_data = read_data(filename)
    updated_data = existing_data + new_data
    write_array(updated_data, filename)

def add_data_no_duplicates(original_new_data, filename):
    new_data = original_new_data.copy()
    existing_data = read_data(filename)
    stripped_existing_data = copy_data_and_strip_ids(existing_data)
    _remove_objects_already_present(new_data, stripped_existing_data)
    _check_ids(existing_data, new_data)
    add_ids_if_not_present(new_data)
    updated_data = existing_data + new_data
    write_array(updated_data, filename)

def add_single_entry_no_duplicates(new_entry, filename):
    add_data_no_duplicates([new_entry], filename)

def read_entry(id, filename):
    array = read_data(filename)
    for entry in array:
        if entry['id'] == id:
            return entry

def read_data(filename):
    filepath = _to_path(filename)
    array = []
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as f:
            array = json.load(f)
    return array

def write_array(array, filename):
    filepath = _to_path(filename)
    with open(filepath, 'w') as f:
        json.dump(array, f)

def _check_ids(existing_data, new_data):
    ids_existing_data = _get_ids(existing_data)
    ids_new_data = _get_ids(new_data)
    all_ids = ids_existing_data + ids_new_data
    for index_1, id_1 in enumerate(all_ids):
        for index_2, id_2 in enumerate(all_ids):
            if index_1 != index_2 and id_1 == id_2:
                raise ValueError('duplicate id found')


def _get_ids(data):
    return list(map(lambda x: x['id'], filter(lambda x: 'id' in x, data)))

def _to_path(filename):
    return filename + '.json'

def add_ids_if_not_present(iterable_of_maps):
    for map in iterable_of_maps:
        if 'id' not in map:
            map['id'] = str(uuid.uuid4())

def copy_data_and_strip_ids(iterable_of_maps_with_id_field):
    return list(map(_copy_and_remove_id_field, iterable_of_maps_with_id_field))

def _copy_and_remove_id_field(map_with_id_field):
    copy = map_with_id_field.copy()
    del copy['id']
    return copy

def _remove_objects_already_present(new_data, objects_already_present):
    for object_already_present in objects_already_present:
        index = _index_of_object_in_list(new_data, object_already_present)
        if index is not None:
            del new_data[index]

def append_if_not_present(data, object):
    ids_already_present = _get_ids(data)
    object_copy = object.copy()
    if 'id' in object_copy:
        for id in ids_already_present:
            if id == object_copy['id']:
                raise ValueError('duplicate id found')
        del object_copy['id']
    if _index_of_object_in_list(data, object_copy) is None:
        data.append(object)

def _index_of_object_in_list(data, object):
    for index, element in enumerate(data):
        if 'id' in element:
            element = element.copy()
            del element['id']
        if element == object:
            return index
