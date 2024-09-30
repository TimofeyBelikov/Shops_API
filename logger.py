
log_format = '{"time" : "%(asctime)s", "method" : "%(method)s", "msg" : "%(message)s"}'

def add_method_to_record(record):
    if hasattr(record, 'method'):
        return record.method
    else:
        return '-'

def add_uuid_to_record(record):
    if hasattr(record, 'uuid'):
        return record.uuid
    else:
        return '-'