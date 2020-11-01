import abc
import datetime
import json
from datetime import date
from typing import Dict

from quickbase_client.orm.table import QuickBaseTable


class QuickBaseJsonEncoder(json.JSONEncoder):

    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, date):
            return o.isoformat()
        return super().default(o)  # pragma: no cover


class RecordSerializer(abc.ABC):

    @abc.abstractmethod
    def serialize(self, record: 'QuickBaseTable'):
        pass  # pragma: no cover

    @abc.abstractmethod
    def deserialize(self, data):
        pass  # pragma: no cover


class RecordJsonSerializer(RecordSerializer):

    def serialize(self, record: 'QuickBaseTable') -> Dict:
        o = {}
        for attr, v in record.__dict__.items():
            if attr[0] == '_' or v is None:
                continue
            field_info = record.get_field_info(attr)
            o[field_info.fid] = {'value': v}
        return o

    def deserialize(self, data):
        pass  # pragma: no cover
