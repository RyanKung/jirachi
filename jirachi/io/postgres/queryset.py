from . import utils
import time
from .monitor import PostgresMonitor

__all__ = ['QuerySet', 'query', 'update', 'insert']

key = str(time.time())


async def query(sql):
    print(sql)
    return await PostgresMonitor.fetch(sql)


async def update(sql):
    print(sql)
    return await PostgresMonitor.execute(sql)


async def insert(sql):
    print(sql)
    return await PostgresMonitor.execute(sql)


class QuerySet(object):
    _sql = {
        'get_list': 'SELECT {fields} from {table} {extra} LIMIT {size} OFFSET {offset}',
        'filter': 'SELECT {fields} from {table} WHERE {rule} LIMIT {size} OFFSET {offset}',
        'count': 'SELECT COUNT({field}) FROM {table}',
        'count_on_rule': 'SELECT COUNT({field}) FROM {table} WHERE {rule}',
        'orderby': 'ORDER BY {field}',
        'nearby': 'select {fields} difference from {table} where {rule} and {value} > {column} limit 1',
        'orderby_decr': 'ORDER BY {field} DECR',
        'filter_with_orderby': "SELECT {fields} from {table} WHERE {rule} ORDER BY {sort_key} LIMIT {size} OFFSET {offset};",
        'filter_with_orderby_decr': "SELECT {fields} from {table} WHERE {rule} ORDER BY {sort_key} LIMIT {size} OFFSET {offset};",
        'filter_in': "SELECT {fields} FROM {table} WHERE {key} IN ({targets});",
        'filter_in_range': "SELECT {fields} FROM {table} WHERE {rule} and {key} <= {end} and {key} >= {start};",
        'find_in_range': "SELECT {fields} FROM {table} WHERE {key} <= {end} and {key} >= {start};",
        'find_near': "SELECT {fields} FROM {table} WHERE {key} >= {start};",
        'insert': 'INSERT INTO {table} ({keys}) VALUES ({values}) RETURNING id;',
        'replace': 'REPLACE INTO {table} ({keys}) VALUES ({values})',
        'delete': "DELETE FROM {table} WHERE {rules} RETURNING id",
        'update': "UPDATE {table} SET {key_value_pairs} WHERE {rules} RETURNING id",
        'append_array': "UPDATE {table} SET {key} = array_append({key}, {value}) WHERE id='{id}' RETURNING id",
        'get_via_id': "SELECT {fields} from {table} WHERE id='{id}'",
        'update_via_id': "UPDATE {table} SET {key_value_pairs} WHERE id='{id}' RETURNING id",
        'delete_via_id': "DELETE FROM {table} WHERE id='{id}' RETURNING id",
        'incr': "UPDATE {table} SET {key}={key}+'{num}' WHERE id='{id}' RETURNING id",
        'decr': "UPDATE {table} SET {key}={key}-'{num}' WHERE id='{id}' RETURNING id",
        'search': "SELECT {fields} FROM {table} WHERE {extra} {key} LIKE '%{value}%' LIMIT {size} OFFSET {offset}",
        'insert_or_update': "INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE {key_value_pairs};"
    }

    def __init__(self, table):
        self.table = table
        self.fields = table._fields
        self.tablename = table.__name__

    def format(self, data):
        if not isinstance(data, dict):
            return utils.escape(str(data.encode('utf8')))
        if not all(f in self.fields for f in data.keys()):
            raise Exception("Unknew Fields", set(
                data.keys()) - set(self.fields))
        try:
            res = {k: utils.escape(v) for k, v in data.items()}
            return res
        except:
            raise Exception("Series Failed")

    async def nearby(self, value, column, *args, **kwargs):
        data = self.format(kwargs)
        return await query(self._sql['nearby'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
            'value': utils.escape(value),
            'column': utils.escape(column),
            'rule': utils.get_and_seg(data)
        }))

    async def get(self, oid):
        res = await query(self._sql['get_via_id'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
            'id': oid
        }))
        return res and dict(zip(self.fields, res[0])) if res else None

    async def get_by(self, *args, **kwargs):
        data = self.format(kwargs)
        res = await query(self._sql['filter'].format(**{
            'table': self.tablename,
            'rule': utils.get_and_seg(data),
            'size': '1',
            'offset': '0',
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
        }))
        return res and dict(zip(self.fields, res[0]))

    async def search(self, key, value, start, limit, filters=''):
        return await query(self._sql['search'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
            'key': self.format(key),
            'value': self.format(value),
            'offset': str(int(start)),
            'size': str(int(limit)),
            'extra': filters and utils.get_pairs(filters) + 'and' or ''
        }))

    async def get_list(self, size=100, offset=0, sort_key='') -> list:
        if isinstance(sort_key, list):
            sort_key = utils.concat(map(utils.set_desc, sort_key))
        else:
            sort_key = sort_key and utils.set_desc(sort_key) or ''

        res = await query(self._sql['get_list'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
            'size': str(int(size)),
            'offset': str(int(offset)),
            'extra': sort_key and self._sql['orderby'].format(**{
                'field': sort_key
            }) or ''

        }))
        return [dict(zip(self.fields, r)) for r in res]

    async def find_in(self, key, targets, fields=[]) -> dict:
        return await query(self._sql['filter_in'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, fields or self.fields)),
            'key': key,
            'targets': utils.concat(map(utils.wrap_value, targets))
        }))

    async def find_near(self, key, start, end, fields=[], *args, **kwargs) -> dict:
        data = self.format(kwargs)
        res = await query(self._sql['find_near'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, fields or self.fields)),
            'key': key,
            'rule': utils.get_and_seg(data),
            'start': utils.wrap_value(start),
            'end': utils.wrap_value(end)
        }))
        return [dict(zip(self.fields, r)) for r in res]

    async def find_in_range(self, key, start, end, fields=[], *args, **kwargs) -> dict:
        data = self.format(kwargs)
        res = await query(self._sql['filter_in_range'].format(**{
            'table': self.tablename,
            'fields': utils.concat(map(utils.wrap_key, fields or self.fields)),
            'key': key,
            'rule': utils.get_and_seg(data),
            'start': utils.wrap_value(start),
            'end': utils.wrap_value(end)
        }))
        return [dict(zip(self.fields, r)) for r in res]

    async def count(self, field):
        field = utils.escape(field) or '*'
        return await query(self._sql['count'].format(**{
            'table': self.tablename,
            'field': field
        }))

    async def count_on_rule(self, field, rule):
        rule = self.format(rule)
        field = utils.escape(field)
        return await query(self._sql['count_on_rule'].format(**{
            'table': self.tablename,
            'rule': utils.get_and_seg(rule),
            'field': field
        }))

    async def filter(self, limit=100, offset=0, sort_key='', *args, **kwargs):
        data = self.format(kwargs)
        res = await query(self._sql['filter'].format(**{
            'table': self.tablename,
            'rule': utils.get_and_seg(data),
            'size': str(int(limit)),
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
            'offset': str(int(offset))
        }))
        return [dict(zip(self.fields, r)) for r in res]

    async def sortby(self, sort_key='id', offset=0, limit=100, extra="", decr=False, *args, **kwargs):
        data = self.format(kwargs)
        if isinstance(sort_key, list):
            sort_key = utils.concat(map(utils.set_desc, sort_key))
        else:
            sort_key = utils.set_desc(sort_key)
        tmpl = decr and 'filter_with_orderby_decr' or 'filter_with_orderby'
        return await query(self._sql[tmpl].format(**{
            'table': self.tablename,
            'rule': utils.get_and_seg(data),
            'size': str(int(limit)),
            'sort_key': sort_key,
            'offset': str(int(offset)),
            'fields': utils.concat(map(utils.wrap_key, self.fields)),
        }))

    async def insert(self, *args, **kwargs):
        data = self.format(kwargs)
        return await insert(self._sql['insert'].format(**{
            'table': self.tablename,
            'keys': utils.concat(map(utils.wrap_key, data.keys())),
            'values': utils.concat(map(utils.wrap_value, data.values()))
        }))

    async def replace(self, *args, **kwargs):
        data = self.format(kwargs)
        return await insert(self._sql['replace'].format(**{
            'table': self.tablename,
            'keys': utils.concat(map(utils.wrap_key, data.keys())),
            'values': utils.concat(map(utils.wrap_value, data.values()))
        }))

    async def update(self, oid, *args, **kwargs):
        data = self.format(kwargs)
        pairs = utils.get_pairs(data)
        return await update(self._sql['update_via_id'].format(**{
            'id': oid,
            'table': self.tablename,
            'key_value_pairs': pairs
        }))

    async def append_array(self, oid, key, value):
        return await update(self._sql['append_array'].format(**{
            'id': oid,
            'table': self.tablename,
            'key': key,
            'value': value
        }))

    async def insert_or_update(self, *args, **kwargs) -> dict:
        data = self.format(kwargs)
        return await insert(self._sql('insert_or_update').format(**{
            'table': self.tablename,
            'keys': utils.concat(map(utils.wrap_key, data.keys())),
            'values': utils.concat(map(utils.wrap_key, data.values())),
            'key_value_pairs': utils.get_pairs(data)
        }))

    async def update_by(self, rules, *args, **kwargs):
        data = self.format(kwargs)
        rules = self.format(rules)
        return await update(self._sql['update'].format(**{
            'table': self.tablename,
            'rules': utils.get_and_seg(rules),
            'key_value_pairs': utils.get_pairs(data)
        }))

    async def delete(self, oid):
        return await update(self._sql['delete_via_id'].format(**{
            'table': self.tablename,
            'id': oid
        }))

    async def delete_by(self, *args, **kwargs):
        data = self.format(kwargs)
        return await update(self._sql['delete'].format(**{
            'table': self.tablename,
            'rules': utils.get_and_seg(data)
        }))

    async def incr(self, oid, key, num):
        return await update(self._sql['incr'].format(**{
            'id': oid,
            'table': self.tablename,
            'key': key,
            'num': num
        }))

    async def decr(self, oid, key, num):
        return await update(self._sql['decr'].format(**{
            'id': oid,
            'table': self.tablename,
            'key': key,
            'num': num
        }))
