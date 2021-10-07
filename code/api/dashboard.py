from flask import Blueprint
from datetime import datetime, timedelta
from functools import partial
from api.schemas import DashboardTileSchema, DashboardTileDataSchema, ObservableSchema, ActionFormParamsSchema
from api.utils import jsonify_data, get_jwt, get_json
from api.infocon import get_infocon, get_attack_summary, get_topports, get_topip

dashboard_api = Blueprint('dashboard', __name__)
get_dashboardtile_form_params = partial(get_json, schema=DashboardTileSchema())
get_dashboardtiledata_form_params = partial(get_json, schema=DashboardTileDataSchema())


def set_valid_time():
    return {
        'start_time': str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
        'end_time': str((datetime.now() + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M:%S.%fZ"))
    }
def set_observed_time(timeframe_in_sec):
    return {
        'start_time': str((datetime.now() - timedelta(seconds=timeframe_in_sec)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
        'end_time': str(datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"))

    }

def create_tile_data(threat_level, diary_name, url):
    valid_time = set_valid_time()
    observed_time = set_observed_time(86400)
    txt = '| **{}** | | [{}]({}) |'.format(threat_level, diary_name, url)
    data = []
    data.append('[SANS Internet Storm Center](https://isc.sans.edu/infocon.html)')
    data.append('&nbsp;')
    data.append('| Threat Level | &nbsp; | Dairy |')
    data.append('| -- | -- | -- |')
    data.append(txt)

    data = {
        'valid_time': valid_time,
        'hide_legend': True,
        'cache_scope': 'org',
        'observed_time': observed_time,
        'data': data
    }
    return data

def create_tile_data_reports(data_json):
    valid_time = set_valid_time()
    observed_time = set_observed_time(2592000)
    keys = [
        {
            'key': 'reports',
            'label': 'Reports'
        }
        ]
    data = {
            'valid_time': valid_time,
            'hide_legend': True,
            'cache_scope': 'org',
            'observed_time': observed_time,
            'key_type': 'timestamp',
            'keys': keys,
            'data': data_json
            }
    return data

def create_tile_data_targets(data_json):
    valid_time = set_valid_time()
    observed_time = set_observed_time(2592000)
    keys = [
        {
            'key': 'targets',
            'label': 'Targets'
        }
        ]
    data = {
            'valid_time': valid_time,
            'hide_legend': True,
            'cache_scope': 'org',
            'observed_time': observed_time,
            'key_type': 'timestamp',
            'keys': keys,
            'data': data_json
            }
    return data

def create_tile_data_sources(data_json):
    valid_time = set_valid_time()
    observed_time = set_observed_time(2592000)
    keys = [
        {
            'key': 'sources',
            'label': 'Sources'
        }
        ]
    data = {
            'valid_time': valid_time,
            'hide_legend': True,
            'cache_scope': 'org',
            'observed_time': observed_time,
            'key_type': 'timestamp',
            'keys': keys,
            'data': data_json
            }
    return data

def get_tile(description, tags, tile_type, title, tile_id):
    if tile_id == 'SANS_Infocon':
        periods = 'last_24_hours'
    elif tile_id == 'SANS_TopPorts':
        periods = 'last_24_hours'
    elif tile_id == 'SANS_Reports':
        periods = 'last_30_days'
    else:
        periods = 'last_30_days'
    return {
        'description': description,
        'periods': [
            periods
        ],
        'tags': tags,
        'type': tile_type,
        'short_description': description,
        'title': title,
        'default_period': periods,
        'id': tile_id
    }


@dashboard_api.route('/tiles', methods=['POST'])
def tiles():
    #get_jwt()
    data = []

    # Tile SANS Internet Storm Center & Diary
    title = 'SANS Internet Storm Center Threat Level and daily diary information'
    tags = ['SANS', 'Threat Level', 'Infocon']
    tile_type = 'markdown'
    description = 'SANS Internet Storm Center Infocon Threat Level & Diares'
    tile_id = 'SANS_Infocon'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    # Tile SANS Internet Storm Center Daily Reports
    title = 'SANS Internet Storm Center Daily Reports'
    tags = ['SANS', 'Threat Level', 'Reports']
    tile_type = 'vertical_bar_chart'
    description = 'SANS Internet Storm Center Daily Reports'
    tile_id = 'SANS_Reports'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    # Tile SANS Internet Storm Center Daily Summary of totals tof sources
    title = 'SANS Internet Storm Center Daily Summary of sources'
    tags = ['SANS', 'Threat Level', 'Sources']
    tile_type = 'vertical_bar_chart'
    description = 'SANS Internet Storm Center Daily Summary of sources'
    tile_id = 'SANS_Sources'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    # Tile SANS Internet Storm Center Daily Summary of totals targets
    title = 'SANS Internet Storm Center Daily Summary of targets'
    tags = ['SANS', 'Threat Level', 'Targets']
    tile_type = 'vertical_bar_chart'
    description = 'SANS Internet Storm Center Daily Summary of targets'
    tile_id = 'SANS_Targets'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    # Tile SANS Internet Storm Center Daily Top ports
    title = 'SANS Internet Storm Center Daily Top ports'
    tags = ['SANS', 'Threat Level', 'TopPorts']
    tile_type = 'horizontal_bar_chart'
    description = 'SANS Internet Storm Center Daily Top ports'
    tile_id = 'SANS_TopPorts'
    data.append(get_tile(description, tags, tile_type, title, tile_id))

    # Tile SANS Internet Storm Center Daily Top IP
    title = 'SANS Internet Storm Center Daily Top IP by attack'
    tags = ['SANS', 'Threat Level', 'TopIP']
    tile_type = 'horizontal_bar_chart'
    description = 'SANS Internet Storm Center Daily Top IP by attack '
    tile_id = 'SANS_TopIP'
    data.append(get_tile(description, tags, tile_type, title, tile_id))


    return jsonify_data(data)

@dashboard_api.route('/tiles/tile', methods=['POST'])
def tile():
    #get_jwt()
    return jsonify_data({})

@dashboard_api.route('/tiles/tile-data', methods=['POST'])
def tile_data():
    data = []
    #get_jwt()
    params = get_dashboardtiledata_form_params()
    if params['tile_id'] == 'SANS_Infocon':
        threat_level, diary_name, url = get_infocon()
        data = create_tile_data(threat_level, diary_name, url)
        return jsonify_data(data)
    elif params['tile_id'] == 'SANS_Reports':
        xml, start_day, end_day = get_attack_summary(30)
        data_json = []
        for x in xml.findall('daily'):
            day = {}
            date = datetime.strptime(x.find('date').text, "%Y-%m-%d")
            day['key'] = datetime.timestamp(date) * 1000
            day['label'] = '{}, 00:00:00'.format(
                datetime.strptime(x.find('date').text, "%Y-%m-%d").strftime('%m/%d/%Y'))
            day['value'] = int(x.find('records').text) + int(x.find('sources').text) + int(x.find('targets').text)
            values = [
                {
                    'key': 'reports',
                    'value': int(x.find('records').text),
                    'tooltip': 'Reports: {}'.format(int(x.find('records').text)),
                    'link_uri': 'https://isc.sans.edu/submissions.html?startdate={}&enddate={}&yname=sources&y2name=targets&submit=Update'.format(start_day, end_day)
                }
            ]
            day['values'] = values
            data_json.append(day)
        data = create_tile_data_reports(data_json)
        return jsonify_data(data)

    elif params['tile_id'] == 'SANS_Targets':
        xml, start_day, end_day = get_attack_summary(30)
        data_json = []
        for x in xml.findall('daily'):
            day = {}
            date = datetime.strptime(x.find('date').text, "%Y-%m-%d")
            day['key'] = datetime.timestamp(date) * 1000
            day['label'] = '{}, 00:00:00'.format(
                datetime.strptime(x.find('date').text, "%Y-%m-%d").strftime('%m/%d/%Y'))
            day['value'] = int(x.find('records').text) + int(x.find('sources').text) + int(x.find('targets').text)
            values = [
                {
                    'key': 'targets',
                    'value': int(x.find('targets').text),
                    'tooltip': 'Targets: {}'.format(int(x.find('targets').text)),
                    'link_uri': 'https://isc.sans.edu/submissions.html?startdate={}&enddate={}&yname=sources&y2name=targets&submit=Update'.format(start_day, end_day)
                }
            ]
            day['values'] = values
            data_json.append(day)
        data = create_tile_data_targets(data_json)
        return jsonify_data(data)

    elif params['tile_id'] == 'SANS_Sources':
        xml, start_day, end_day = get_attack_summary(30)
        data_json = []
        for x in xml.findall('daily'):
            day = {}
            date = datetime.strptime(x.find('date').text, "%Y-%m-%d")
            day['key'] = datetime.timestamp(date) * 1000
            day['label'] = '{}, 00:00:00'.format(
                datetime.strptime(x.find('date').text, "%Y-%m-%d").strftime('%m/%d/%Y'))
            day['value'] = int(x.find('records').text) + int(x.find('sources').text) + int(x.find('targets').text)
            values = [
                {
                    'key': 'sources',
                    'value': int(x.find('sources').text),
                    'tooltip': 'Sources: {}'.format(int(x.find('sources').text)),
                    'link_uri': 'https://isc.sans.edu/submissions.html?startdate={}&enddate={}&yname=sources&y2name=targets&submit=Update'.format(start_day, end_day)
                }
            ]
            day['values'] = values
            data_json.append(day)
        data = create_tile_data_sources(data_json)
        return jsonify_data(data)

    elif params['tile_id'] == 'SANS_TopPorts':
        json, today = get_topports()
        keys = []
        data = []
        for x in range(0, 10):
            a = {}
            a['key'] = 'Port-{}'.format(str(json[str(x)]['targetport']))
            a['label'] = 'Port-{}'.format(str(json[str(x)]['targetport']))
            keys.append(a)
            b = {}
            c = {}
            values = []
            b['key'] = 'Port-{}'.format(str(json[str(x)]['targetport']))
            b['label'] = 'Port-{}'.format(str(json[str(x)]['targetport']))
            b['value'] = json[str(x)]['records']
            c['key'] = 'Port-{}'.format(str(json[str(x)]['targetport']))
            c['tooltip'] = 'Port-{}'.format(str(json[str(x)]['targetport']))
            c['link_uri'] = 'https://isc.sans.edu/port.html?port={}'.format(str(json[str(x)]['targetport']))
            c['value'] = json[str(x)]['records']
            values.append(c)
            b['values'] = values
            data.append(b)
        valid_time = set_valid_time()
        observed_time = set_observed_time(86400)
        response = {
            'valid_time': valid_time,
            'keys': keys,
            'cache_scope': 'org',
            'hide_legend': True,
            'observed_time': observed_time,
            'key_type': 'string',
            "observable_type": False,
            'data': data
            }
        return jsonify_data(response)

    elif params['tile_id'] == 'SANS_TopIP':
        json, today = get_topip()
        keys = []
        data = []
        for x in json:
            a = {}
            a['key'] = x['ip']
            a['label'] = x['ip']
            keys.append(a)
            b = {}
            c = {}
            values = []
            b['key'] = x['ip']
            b['label'] = x['ip']
            b['value'] = x['attacks']
            c['key'] = x['ip']
            c['tooltip'] = x['ip']
            c['link_uri'] = 'https://isc.sans.edu/ipinfo.html?ip={}'.format(x['ip'])
            c['value'] = x['attacks']
            values.append(c)
            b['values'] = values
            data.append(b)
        valid_time = set_valid_time()
        observed_time = set_observed_time(86400)
        response = {
            'valid_time': valid_time,
            'keys': keys,
            'cache_scope': 'org',
            'hide_legend': True,
            'observed_time': observed_time,
            'key_type': 'string',
            "observable_type": 'ip',
            'data': data
            }
        return jsonify_data(response)


    else:
        return jsonify_data(data)

