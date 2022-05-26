import daos.base_dao as base_dao

class WithOptionalField:
    def __init__(self, field, optional_field = None):
        self.field = field
        self.optional_field = optional_field

def _serialize(object):
    serialized = {
        'field': object.field
    }
    return serialized

def _deserialize(serialized):
    field = serialized['field']
    optional_field = serialized['optional_field']
    return WithOptionalField(field, optional_field)

def execute():
    obj = WithOptionalField('field')
    serialized = _serialize(obj)
    print(serialized)
    base_dao.add_data_no_id([serialized], 'data/test_optional_field')
    data = base_dao.read_data('data/test_optional_field')
    serialized = data[0]
    object = _deserialize(serialized)
    print('object:')
    print(object.field)
    print(object.optional_field)
