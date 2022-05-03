import json
import os
import uuid

def add_data(new_data, filename):
    existing_data = read_array(filename)
    add_ids(new_data)
    updated_data = existing_data + new_data
    write_array(updated_data, filename)

def add_data_no_duplicates(new_data, filename):
    existing_data = read_array(filename)
    stripped_existing_data = strip_ids(existing_data)
    _remove_objects_from_list(new_data, stripped_existing_data)
    add_ids(new_data)
    updated_data = existing_data + new_data
    write_array(updated_data, filename)

def read_array(filename):
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

def _to_path(filename):
    return 'data/' + filename

def add_ids(iterable_of_maps):
    for map in iterable_of_maps:
        map['id'] = str(uuid.uuid4())

def strip_ids(iterable_of_maps_with_id_field):
    frozenset(map(_remove_id_field, iterable_of_maps_with_id_field))

def _remove_id_field(map_with_id_field):
    copy = map_with_id_field.copy()
    del copy['id']
    return copy

def _remove_objects_from_list(list, objects_to_remove):
    for object in objects_to_remove:
        index = _index_of_object_in_list(list, object)
        if index is not None:
            del list[index]

def append_if_not_present(list, object):
    if _index_of_object_in_list(list, object) is None:
        list.append(object)

def _index_of_object_in_list(list, object):
    for index, element in enumerate(list):
        if element == object:
            return index
