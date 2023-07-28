import time

from pymongo import MongoClient
from settings import MONGO_HOST

_client = MongoClient(MONGO_HOST, 27017)


def drop_db():
    _client.drop_database('WSD')


def save_sensor_data(device, value):
    _db = _client['WSD']
    _col = _db[device]
    value.update({'ts': time.time().__int__()})
    _col.insert_one(value)


def avg(ll):
    """
    Get average of a list
    :param ll:
    :return:
    """
    return round(sum(ll) / float(len(ll)), 2)


def get_sensor_data(device):
    return group_data(get_raw_sensor_data(device))


def group_data(raw_data):
    # Group items by `potentiometer` value

    raw_data = sorted(raw_data, key=lambda v: v['potentiometer'])

    cur_value = None
    tmp = []
    g_data = []
    for d in raw_data:
        if d['potentiometer'] != cur_value:
            cur_value = d['potentiometer']
            if tmp:
                g_data.append(tmp)
            tmp = [d]
        else:
            tmp.append(d)
    # Add the last remaining group
    g_data.append(tmp)

    # Get average value of each group and compose a list
    avg_data = []
    for d in g_data:
        if d:
            avg_data.append(dict(
                potentiometer=d[0]['potentiometer'],
                weight_wheel=avg([k['weight_wheel'] for k in d]),
                weight_bs=avg([k['weight_bs'] for k in d]),
                ts=d[len(d) / 2]['ts']
            ))

    data = sorted(avg_data, key=lambda v: v['ts'])
    return data


def get_raw_sensor_data(device):
    _db = _client['WSD']
    _col = _db[device]
    raw_data = list(_col.find())
    return raw_data
