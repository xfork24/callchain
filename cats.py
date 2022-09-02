#!./bin/python
# Auto-generated file, edit at your own risk.

import argparse
import copy
import datetime
import logging
import json
import random
import time
import os
import requests
import re
import csv
import graphviz
from tabulate import tabulate
import jsonpath_ng as jp
import pandas as pd
from bs4 import BeautifulSoup


# cat configurations
CAT_JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjYXQiLCJvcHRyIjoibGZzIn0.oD3U9BzjuKvomor6ASfe8yXuaov1rhMJmf5KyIZlpto'
CAT_API_ENDPOINT = 'https://cat-api.i.ssc.shopee.io'
CAT_TRANSACTION_REPORT_SUB_URL = '/cat/r/transaction_report'
CAT_MESSAGE_REPORT_SUB_URL = '/cat/r/message_report/{0}'
CAT_IP = 'All'
CAT_DATA_FORMAT = 'json'

# system configurations
CAT_SINGLE_ENDPOINT_CALL_LIMIT = 100
CALLCHAIN_LINK_ANALYSIS_LIMIT = 5
MAX_FILE_READ_LENGTH = 4194304  # 4MB
DEFAULT_OUTPUT_SUB_FOLDER_NAME = 'scenarios'
CRITICAL_CALL_HIGHLIGHT_COLOR = 'red'
WORKING_DIR = '.'

# root logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
log = logging.getLogger('root')

# external google sheet dependencies
DEPENDS_FOLDER = '{0}/depends/'.format(WORKING_DIR)
GS_SHEET_KEY = '1oIvViYzYYASxB-FAltpntWtj4NtU9MhfCa87JCwVKl4'
GS_SERVICE_TAB_NAME = 'Services'
GS_DOMAIN_TAB_NAME = 'Domains'
GS_API_TAB_NAME = 'APIs'
GS_RULE_TAB_NAME = 'Rules'
GS_NODE_OVERWRITE_TAB_NAME = 'NodeOverwriteRules'
GS_EDGE_OVERWRITE_TAB_NAME = 'EdgeOverwriteRules'
GS_NAME_OVERWRITE_TAB_NAME = 'NameOverwriteRules'
GS_COMBINE_TAB_NAME = 'CombineRules'
GS_DELETE_TAB_NAME = 'DeleteRules'
GS_LINK_TAB_NAME = 'LinkRules'
GS_STACK_END_TAB_NAME = 'StackEndRules'

GS_SHEET_URL = 'https://docs.google.com/spreadsheets/d/{0}/gviz/tq?tqx=out:csv&sheet={1}'

GS_SERVICE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_SERVICE_TAB_NAME)
GS_DOMAIN_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_DOMAIN_TAB_NAME)
GS_API_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_API_TAB_NAME)
GS_RULE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_RULE_TAB_NAME)
GS_NODE_OVERWRITE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_NODE_OVERWRITE_TAB_NAME)
GS_EDGE_OVERWRITE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_EDGE_OVERWRITE_TAB_NAME)
GS_NAME_OVERWRITE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_NAME_OVERWRITE_TAB_NAME)
GS_COMBINE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_COMBINE_TAB_NAME)
GS_DELETE_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_DELETE_TAB_NAME)
GS_LINK_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_LINK_TAB_NAME)
GS_STACK_END_TAB_URL = GS_SHEET_URL.format(GS_SHEET_KEY, GS_STACK_END_TAB_NAME)

# local google sheet cache files
SERVICE_DEFINITION_FILE_NAME = 'services.csv'
DOMAIN_DEFINITION_FILE_NAME = 'domains.csv'
API_DEFINITION_FILE_NAME = 'apis.csv'
RULE_DEFINITION_FILE_NAME = 'rules.csv'
NODE_OVERWRITE_RULE_FILE_NAME = 'node_overwrite_rules.csv'
EDGE_OVERWRITE_RULE_FILE_NAME = 'edge_overwrite_rules.csv'
NAME_OVERWRITE_RULE_FILE_NAME = 'name_overwrite_rules.csv'
COMBINE_RULE_FILE_NAME = 'combine_rules.csv'
DELETE_RULE_FILE_NAME = 'delete_rules.csv'
LINK_RULE_FILE_NAME = 'link_rules.csv'
STACK_END_RULE_FILE_NAME = 'stack_end_rules.csv'

# original files
ORIGINAL_CALLCHAIN_FILE_NAME = 'original_callchain.txt'
ORIGINAL_CALLS_FILE_NAME = 'original_calls.txt'

# parsed files
PARSED_CALLCHAIN_FILE_NAME = 'callchain.txt'
CALLCHAIN_DOT_FILE_NAME = 'callchain.dot'
CALLCHAIN_PLANTUML_FILE_NAME = 'sequence.puml'
PARSED_CALLS_FILE_NAME = 'calls.txt'
CALLS_REPORT_FILE_NAME = 'calls.report.txt'
PARSED_STACK_FILE_NAME = 'stacks.txt'
HIGHLIGHT_STACK_FILE_NAME = 'hstacks.txt'
HIGHLIGHT_STACK_REPORT_FILE_NAME = 'hstacks.report.txt'


ALL_SCENARIOS = {
    'create_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_sample_count)
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/order/create', 1, 1),
        ],
        'extra_callchain': [
        ],
        'extra_node_overwrite_rules': {},
        'extra_edge_overwrite_rules': {},
        'extra_rename_rules': [
            # (id, caller, callee, api, info1, info2, rule)
            ('*', 'OrderCreatedTrackingUpdateJob', 'TrackingAssemble', 'TrackingAssembleSuccess', '*', '*', 'Callee:LTS;API:DoTrackingExceptionAndMapAndDesc'),
            ('*', 'PIS', '(api|ResourceAPI)', '*', '*', '*', 'Callee:3PL'),
        ],
        'extra_delete_rules': [
            # (id, caller, callee, api, info1, info2)
            ('*', 'OrderCreatedTrackingUpdateJob', 'GetTrackingFromLTS', '*', '*', '*'),
            ('*', 'StatusChangeTriggerCalcAsfJob', 'ActualShippingFee', 'StatusChangedTriggerASF', '*', '*'),
            ('*', '*', 'TrackingOperate', '*', '*', '*'),
            ('*', 'SmartRouting', '*', '*', '*', '*'),
            ('*', 'OMS', '*', '*', '*', '*'),
        ],
        # 'highlights': ['/api/sls-basic/freight/calc_esf_weight/', '/api/lls/create_line_waybill'],
        'name': 'create_order',
        'region': 'ID',
        'reload': True,
        'enabled': True,
    },
    'push_tracking_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_sample_count)
            ('LCS-TRACKINGAPI-ID', 'URL', '/api/webhook/update_status/local_jnt', 10, 10),
        ],
        'extra_callchain': [
        ],
        'extra_node_overwrite_rules': {},
        'extra_edge_overwrite_rules': {},
        'extra_rename_rules': [
            # (id, caller, callee, api, info1, info2, rule)
            ('*', 'TrackingUpdateJob', 'TrackingAssemble', 'TrackingAssembleSuccess', '*', '*', 'Callee:LTS;API:DoTrackingExceptionAndMapAndDesc'),
            ('*', 'PIS', '(API|ResourceAPI)', '*', '*', '*', 'Callee:3PL'),
        ],
        'extra_delete_rules': [
            # (id, caller, callee, api, info1, info2)
            ('*', 'OMS', '*', '*', '*', '*'),
            ('*', '*', '(TrackingOperate|GetTrackingFromLTS|GetTrackingNotFromLTS)', '*', '*', '*'),
        ],
        # 'highlights': [],
        'name': 'push_tracking',
        'region': 'ID',
        'reload': True,
        'enabled': True,
    },
}


def initialize(init=True):
    if not init:
        log.info('Using local configurations')
        return
    else:
        log.info('Downloading latest configurations')
    if not os.path.exists(DEPENDS_FOLDER):
        os.makedirs(DEPENDS_FOLDER, exist_ok=True)
    depends = [
        (GS_SERVICE_TAB_URL, DEPENDS_FOLDER + SERVICE_DEFINITION_FILE_NAME),
        (GS_DOMAIN_TAB_URL, DEPENDS_FOLDER + DOMAIN_DEFINITION_FILE_NAME),
        (GS_API_TAB_URL, DEPENDS_FOLDER + API_DEFINITION_FILE_NAME),
        (GS_RULE_TAB_URL, DEPENDS_FOLDER + RULE_DEFINITION_FILE_NAME),
        (GS_NODE_OVERWRITE_TAB_URL, DEPENDS_FOLDER + NODE_OVERWRITE_RULE_FILE_NAME),
        (GS_EDGE_OVERWRITE_TAB_URL, DEPENDS_FOLDER + EDGE_OVERWRITE_RULE_FILE_NAME),
        (GS_NAME_OVERWRITE_TAB_URL, DEPENDS_FOLDER + NAME_OVERWRITE_RULE_FILE_NAME),
        (GS_COMBINE_TAB_URL, DEPENDS_FOLDER + COMBINE_RULE_FILE_NAME),
        (GS_DELETE_TAB_URL, DEPENDS_FOLDER + DELETE_RULE_FILE_NAME),
        (GS_LINK_TAB_URL, DEPENDS_FOLDER + LINK_RULE_FILE_NAME),
        (GS_STACK_END_TAB_URL, DEPENDS_FOLDER + STACK_END_RULE_FILE_NAME),
    ]
    for (url, file_name) in depends:
        r = requests.get(url)
        if not r.ok:
            log.error('failed to download service definition google sheet, use local instead')
        else:
            with open(file_name, 'w') as csv_f:
                csv_f.write(r.text.replace('"', ''))

class CatDataManager:
    def __init__(self, output_path='./output',
                 extra_callchain=None,
                 extra_rules=None):
        random.seed(time.time())
        self.index = 0
        self.output_path = output_path
        self.extra_callchain = extra_callchain
        self.extra_rules = extra_rules
        self.callchain = list()
        self.calls = list()
        self.links = self.load_callchain_link_rules(DEPENDS_FOLDER + LINK_RULE_FILE_NAME)
        self.parsed_links = set()
        self.parsed_calls = set()
        self.call_map = {}

    def get_sample_messages(self, cat_domain, cat_type, cat_name, cat_date=None):
        if cat_date is None:
            last_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
            cat_date = last_hour.strftime('%Y%m%d%H')
        url = CAT_API_ENDPOINT + CAT_TRANSACTION_REPORT_SUB_URL
        headers = self.build_headers()
        params = self.build_params(cat_domain, cat_type, cat_name, cat_date)
        response = self.get_cat_url(url, headers, params)
        if response is None:
            return None
        jdata = json.loads(response.content)
        msg_paths = [
            '$.m_machines.All.m_types."{0}".m_names."{1}".m_statusDists."0".m_sampleMessages'.format(cat_type, cat_name),
            '$.m_machines.All.m_types."{0}".m_statusDists."0".m_sampleMessages'.format(cat_type),
        ]
        for path in msg_paths:
            jp_expr = jp.parse(path)
            result = jp_expr.find(jdata)
            try:
                return [item for item in result[0].value if item != 'null']
            except:
                continue
        log.info('No msg_path matched, ', jdata)
        return None

    def get_sample_message(self, cat_domain, cat_type, cat_name, cat_date=None):
        samples = self.get_sample_messages(cat_domain, cat_type, cat_name, cat_date)
        return None if samples is None else samples[random.randrange(0, len(samples) - 1)]

    def get_sample_message_report(self, cat_domain, cat_type, cat_name, cat_date=None, to_root=True):
        message_id = self.get_sample_message(cat_domain, cat_type, cat_name, cat_date)
        log.info('sample message Id: {0}'.format(message_id))
        return None if message_id is None else self.get_message_report(message_id, to_root)

    def get_sample_callchain(self, cat_domain, cat_type, cat_name, cat_date=None, to_root=True):
        root_df = self.get_sample_message_report(cat_domain, cat_type, cat_name, cat_date, to_root)
        if root_df is None:
            return list()
        root_frame_name, _ = self.parse_root_frame_name(root_df.iloc[[0]])
        return self.parse_callchain(root_df, root_frame_name)

    def get_callchain(self, cat_domain, cat_type, cat_name, sample_count=1, cat_date=None, to_root=True):
        samples = self.get_sample_messages(cat_domain, cat_type, cat_name, cat_date)
        if samples is None:
            return list()
        messages = list()
        if len(samples) < sample_count:
            messages = samples
        else:
            for i in range(sample_count):
                message = samples[random.randrange(0, len(samples) - 1)]
                messages.append(message)
                samples.remove(message)
        log.info(messages)
        all_callchain = list()
        for m in messages:
            root_df = self.get_message_report(m, to_root)
            if root_df is None:
                continue
            root_frame_name, root_call_name = self.parse_root_frame_name(root_df.iloc[[0]])
            parsed = self.get_call_overwrite('-', 'External', root_frame_name, root_call_name, '', '')
            if parsed is not None:
                all_callchain += [parsed]
            all_callchain += self.parse_callchain(root_df, root_frame_name)
        return all_callchain

    def parse_callchain_with_links(self, cat_domain, cat_type, cat_name, sample_count=1, link_sample_count=10,
                                   cat_date=None, to_root=True, region='ID'):
        self.callchain = self.get_callchain(cat_domain, cat_type, cat_name, sample_count, cat_date, to_root)
        if self.extra_callchain is not None:
            self.callchain += self.extra_callchain
        for i in range(CALLCHAIN_LINK_ANALYSIS_LIMIT):
            self.callchain += self.parse_callchain_link(self.callchain, link_sample_count, cat_date, region)
        return self.callchain, self.calls

    def get_message_report(self, message_id, to_root=True):
        url = CAT_API_ENDPOINT + CAT_MESSAGE_REPORT_SUB_URL.format(message_id)
        headers = self.build_headers()
        response = self.get_cat_url(url, headers)
        if response is None:
            return None
        df = self.parse_message_report(response.text)
        header = df[0].iloc[[0]][0]
        root_id = header.split(' ')[-3]
        if root_id == 'null' or not to_root:
            # already in root message, or we don't go to root
            return df.iloc[1:]
        else:
            url = CAT_API_ENDPOINT + CAT_MESSAGE_REPORT_SUB_URL.format(root_id)
            response = self.get_cat_url(url, headers)
            if response is None:
                return None
            df = self.parse_message_report(response.text)
            return df.iloc[1:]

    def parse_callchain(self, frame_df, frame_name):
        callchain = list()
        if frame_df is None:
            return callchain
        for i in range(1, frame_df.shape[0]):  # skip first line
            row = frame_df.iloc[[i]]
            cat_event = row[0].tolist()[0]
            cat_type = row[1].tolist()[0]
            cat_name = row[2].tolist()[0]
            p3 = row[3].tolist()[0]
            p4 = row[3].tolist()[0]
            evt = cat_event[0]
            if (evt == 't' and cat_type != 'RemoteCall') or evt == 'A':
                parsed = self.get_call_overwrite(cat_event, frame_name, cat_type, cat_name, p3, p4)
                if parsed is not None:
                    callchain.append(parsed)
            elif evt == '/':
                next_frame_df = self.get_message_report(cat_type, to_root=False)
                if frame_df.iloc[[i - 1]][1].tolist()[0] == 'RemoteCall':
                    if frame_df.iloc[[i - 2]][1].tolist()[0] == 'RateLimit':
                        new_frame_name, new_call_name = self.parse_root_frame_name(frame_df.iloc[[i - 3]])
                    else:
                        new_frame_name, new_call_name = self.parse_root_frame_name(frame_df.iloc[[i - 2]])
                else:
                    new_frame_name, new_call_name = self.parse_root_frame_name(frame_df.iloc[[i - 1]])
                callchain += self.parse_callchain(next_frame_df, new_frame_name)
            elif evt == 'E' or evt == 'T':
                # ignore events and end of transactions
                continue
            else:
                known_types = ['RemoteCall', 'HeartBeat']
                if cat_type not in known_types and cat_type is not None:
                    log.info('Find unexpected cat record: {0}, {1}, {2}'.format(cat_event, cat_type, cat_name))
        return callchain

    def parse_callchain_link(self, callchain, link_sample_count=1, cat_date=None, region='ID'):
        callchain = callchain if self.extra_rules is None else CallChainParser(*self.extra_rules).refine_callchain(callchain)
        links = list()
        for rule_id, rule in self.links.items():
            for cc in callchain:
                matched = True
                for i in range(6):
                    if rule[i] == '*':
                        continue  # speed up
                    else:
                        regexp = re.compile(rule[i])
                        if re.match(regexp, cc[i]) is None:
                            matched = False
                            break
                if matched:
                    key = '{0}:{1}:{2}'.format(cc[1], cc[2], cc[3])
                    if key in self.parsed_links:
                        continue
                    self.parsed_links.add(key)
                    cat_domain = rule[6].format(region if rule[6][0] < 'a' else region.lower())
                    cat_type = rule[7]
                    cat_name = rule[8]
                    log.info('callchain link rule matched, {0}, {1}'.format(cc, rule))
                    parsed = self.get_call_overwrite(str(rule_id), rule[9], rule[10], rule[11], None, None)
                    if parsed is not None:
                        links.append(parsed)
                    samples = self.get_sample_messages(cat_domain, cat_type, cat_name, cat_date)
                    messages = list()
                    if len(samples) < link_sample_count:
                        messages = samples
                    else:
                        for i in range(link_sample_count):
                            message = samples[random.randrange(0, len(samples) - 1)]
                            messages.append(message)
                            samples.remove(message)
                    log.info(messages)
                    for m in messages:
                        link_root_df = self.get_message_report(m, False)
                        if link_root_df is None:
                            continue
                        links += self.parse_callchain(link_root_df, rule[10])
        return links

    def get_call_overwrite(self, cat_event, caller, callee, api, p3, p4):
        record = [cat_event, caller, callee, api, p3, p4, self.index]
        self.calls.append(record)
        self.index += 1
        key = '{0}:{1}:{2}'.format(caller, callee, api)
        if key in self.parsed_calls:
            return None
        self.parsed_calls.add(key)
        return record

    def parse_message_report(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        table = soup.find('table')
        records = list()
        for tr in table.findAll('tr'):
            tds = tr.findAll('td')
            if len(tds) > 0:
                record = list()
                for td in tds:
                    if td.find('a'):
                        a = td.find('a')
                        if a.text.find('RootLogview') != -1 or a.text.find('ParentLogview') != -1:
                            texts = td.findAll(text=True, recursive=True)
                            for txt in texts:
                                txt = self.parse_text(txt)
                                if txt == 'RootLogview' or txt == 'ParentLogview' or len(txt) == 0:
                                    continue
                                else:
                                    record.append(txt)
                        else:
                            record.append(a['href'])
                    elif td.find('div'):
                        div = td.find('div')
                        record.append(div['id'])
                    elif td.find('span'):
                        span = td.find('span')
                        record.append(span.text)
                    else:
                        txt = self.parse_text(td.text)
                        record.append(None if len(txt) == 0 else txt)
                records.append(record)
        return pd.DataFrame(data=records, columns=[0, 1, 2, 3, 4])

    def parse_root_frame_name(self, frame):
        root_frame_name = frame[1].tolist()[0]
        root_frame_call = frame[2].tolist()[0]
        return root_frame_name, root_frame_call

    def parse_text(self, txt):
        return txt.replace('&nbsp;', '').replace('\xa0', '').strip()

    def build_headers(self):
        headers = {
            'jwt-token': CAT_JWT_TOKEN
        }
        return headers

    def build_params(self, cat_domain, cat_type, cat_name, cat_date):
        params = {
            'domain': cat_domain,
            'ip': CAT_IP,
            'type': cat_type,
            'name': cat_name,
            'date': cat_date,
            'ft': CAT_DATA_FORMAT
        }
        return params

    def get_cat_url(self, url, headers, params=None):
        message_report_sub_url = '/cat/r/message_report/'
        if url.find(message_report_sub_url) != -1:
            tmp = url
            for i in range(3):
                tmp = tmp[:tmp.rfind('-')]
            start = tmp.find(message_report_sub_url) + len(message_report_sub_url)
            key = tmp[start:].lower()
            if key in self.call_map:
                if self.call_map[key] > CAT_SINGLE_ENDPOINT_CALL_LIMIT:
                    return None
                else:
                    self.call_map[key] = self.call_map[key] + 1
            else:
                self.call_map[key] = 0
        response = requests.get(url, headers=headers, params=params)
        if not response.ok:
            if response.reason == 'Not Found':
                log.debug('failed to call url=%s with headers=%s, params=%s, reason=%s', url, headers, params,
                          response.reason)
            else:
                log.error('failed to call url=%s with headers=%s, params=%s, reason=%s', url, headers, params,
                          response.reason)
            return None
        return response

    def load_callchain_link_rules(self, link_file_name):
        links = {}
        first_row = True
        with open(link_file_name) as f:
            csv_reader = csv.reader(f, delimiter=',')
            idx = 1
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                links[idx] = [i if i != '' else '*' for i in row]
                idx = idx + 1
        return links

class CallChainParser:
    def __init__(self, extra_node_overwrite_rules=None, extra_edge_overwrite_rules=None, extra_rename_rules=None,
                 extra_combine_rules=None, extra_delete_rules=None):

        self.extra_node_overwrite_rules = {} if extra_node_overwrite_rules is None else extra_node_overwrite_rules
        self.extra_edge_overwrite_rules = {} if extra_edge_overwrite_rules is None else extra_edge_overwrite_rules
        self.extra_rename_rules = list() if extra_rename_rules is None else extra_rename_rules
        self.extra_combine_rules = list() if extra_combine_rules is None else extra_combine_rules
        self.extra_delete_rules = list() if extra_delete_rules is None else extra_delete_rules
        self.node_overwrite_rules, self.edge_overwrite_rules, self.name_overwrite_rules, self.combine_rules, self.delete_rules, self.stack_end_rules = \
            self.load_callchain_parse_rules(
                DEPENDS_FOLDER + NODE_OVERWRITE_RULE_FILE_NAME,
                DEPENDS_FOLDER + EDGE_OVERWRITE_RULE_FILE_NAME,
                DEPENDS_FOLDER + NAME_OVERWRITE_RULE_FILE_NAME,
                DEPENDS_FOLDER + COMBINE_RULE_FILE_NAME,
                DEPENDS_FOLDER + DELETE_RULE_FILE_NAME,
                DEPENDS_FOLDER + STACK_END_RULE_FILE_NAME)

    def refine_callchain(self, callchain):
        callchain = self.refine_node_overwrite_rules(callchain)
        callchain = self.refine_edge_overwrite_rules(callchain)
        callchain = self.refine_rename_rules(callchain)
        callchain = self.refine_combine_rules(callchain)
        callchain = self.refine_delete_rules(callchain)
        callchain = self.refine_remove_duplicate(callchain)
        callchain = self.refine_remove_reentry(callchain)
        return callchain

    def refine_calls(self, calls):
        calls = self.refine_node_overwrite_rules(calls)
        calls = self.refine_edge_overwrite_rules(calls)
        calls = self.refine_rename_rules(calls)
        calls = self.refine_delete_rules(calls)
        calls = self.refine_remove_reentry(calls)
        return calls

    def refine_node_overwrite_rules(self, callchain):
        refined = callchain
        for rules in [self.extra_node_overwrite_rules, self.node_overwrite_rules]:
            for rule, overwrite in rules.items():
                refined = list()
                for cc in callchain:
                    cc_new = list(cc)
                    regexp = re.compile(rule)
                    if re.match(regexp, cc[1]) is not None:
                        cc_new[1] = overwrite
                    if re.match(regexp, cc[2]) is not None:
                        cc_new[2] = overwrite
                    refined.append(cc_new)
                callchain = refined
        return refined

    def refine_edge_overwrite_rules(self, callchain):
        refined = callchain
        for rules in [self.extra_edge_overwrite_rules, self.edge_overwrite_rules]:
            for rule, overwrite in rules.items():
                refined = list()
                for cc in callchain:
                    cc_new = list(cc)
                    regexp = re.compile(rule)
                    if re.match(regexp, cc[3]) is not None:
                        cc_new[3] = overwrite
                    refined.append(cc_new)
                callchain = refined
        return refined

    def refine_rename_rules(self, callchain):
        refined = callchain
        rename_map = {'id': 0, 'caller': 1, 'callee': 2, 'api': 3, 'info1': 4, 'info2': 5}
        for rules in [self.extra_rename_rules, self.name_overwrite_rules]:
            for rule in rules:
                refined = list()
                for cc in callchain:
                    matched = True
                    for i in range(6):
                        if rule[i] == '*':
                            continue  # speed up
                        else:
                            regexp = re.compile(rule[i])
                            if re.match(regexp, cc[i]) is None:
                                matched = False
                                break
                    if matched:
                        cc_new = list(cc)
                        parts = rule[6].split(';')
                        for part in parts:
                            key, new_name = part.split(':')
                            cc_new[rename_map[key.lower()]] = new_name
                        refined.append(cc_new)
                    else:
                        refined.append(cc)
                callchain = refined
        return refined

    def refine_combine_rules(self, callchain):
        refined = callchain
        for rules in [self.extra_combine_rules, self.combine_rules]:
            for rule in rules:
                refined = list()
                exists = set()
                for cc in callchain:
                    regexp = re.compile(rule)
                    if re.match(regexp, cc[2]) is None:
                        refined.append(cc)
                    else:
                        key = cc[1] + ':' + rule
                        if key in exists:
                            continue
                        else:
                            exists.add(key)
                            cc_new = list(cc)
                            cc_new[3] = 'MultipleCall'
                            cc_new[4] = None
                            cc_new[5] = None
                            refined.append(cc_new)
                callchain = refined
        return refined

    def refine_delete_rules(self, callchain):
        refined = callchain
        for rules in [self.extra_delete_rules, self.delete_rules]:
            for rule in rules:
                refined = list()
                for cc in callchain:
                    matched = True
                    for i in range(6):
                        if rule[i] == '*':
                            continue  # speed up
                        else:
                            regexp = re.compile(rule[i])
                            if re.match(regexp, cc[i]) is None:
                                matched = False
                                break
                    if not matched:
                        refined.append(cc)
                callchain = refined
        return refined

    def refine_remove_reentry(self, callchain):
        refined = list()
        for cc in callchain:
            if cc[1] == cc[2]:
                continue
            else:
                refined.append(cc)
        return refined

    def refine_remove_duplicate(self, callchain):
        exists = set()
        refined = list()
        for cc in callchain:
            key = '{0}:{1}:{2}'.format(cc[1], cc[2], cc[3])
            if key in exists:
                continue
            else:
                refined.append(cc)
                exists.add(key)
        return refined

    def load_callchain_parse_rules(self,
                                   node_overwrite_rule_file,
                                   edge_overwrite_rule_file,
                                   name_overwrite_rule_file,
                                   combine_rule_file,
                                   delete_rule_file,
                                   stack_end_rule_file):
        node_overwrite_rules = {}
        edge_overwrite_rules = {}
        name_overwrite_rules = list()
        combine_rules = list()
        delete_rules = list()
        stack_end_rules = list()
        first_row = True
        with open(node_overwrite_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                pattern, rename = row
                node_overwrite_rules[pattern] = rename
        with open(edge_overwrite_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                pattern, rename = row
                edge_overwrite_rules[pattern] = rename
        with open(name_overwrite_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                name_overwrite_rules.append([i if i != '' else '*' for i in row])
        with open(combine_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                node, = row
                name_overwrite_rules.append(node)
        with open(delete_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                delete_rules.append([i if i != '' else '*' for i in row])
        with open(stack_end_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                node, = row
                stack_end_rules.append(node)
        return node_overwrite_rules, edge_overwrite_rules, name_overwrite_rules, combine_rules, delete_rules, stack_end_rules

class CallChainRender:
    def __init__(self, callchain, calls, highlights=None, graph_name='sample', region='ID',
                 load_exist=False, load_original=True, extra_rules=None):
        self.callchain = callchain
        self.calls = calls
        self.manual_highlight = highlights is not None
        self.highlights = list() if highlights is None else highlights
        self.graph_name = graph_name
        self.region = region
        sub_folder = '{0}/{1}/{2}/{3}/'.format(WORKING_DIR, DEFAULT_OUTPUT_SUB_FOLDER_NAME, region, graph_name)
        # original files
        self.original_callchain_file_name = sub_folder + ORIGINAL_CALLCHAIN_FILE_NAME
        self.original_calls_file_name = sub_folder + ORIGINAL_CALLS_FILE_NAME
        # parsed files
        self.callchain_file_name = sub_folder + PARSED_CALLCHAIN_FILE_NAME
        self.calls_file_name = sub_folder + PARSED_CALLS_FILE_NAME
        self.stacks_file_name = sub_folder + PARSED_STACK_FILE_NAME
        self.highlight_stack_file_name = sub_folder + HIGHLIGHT_STACK_FILE_NAME
        # report files
        self.callchain_dot_name = sub_folder + CALLCHAIN_DOT_FILE_NAME
        self.calls_report_name = sub_folder + CALLS_REPORT_FILE_NAME
        self.highlight_stack_report_name = sub_folder + HIGHLIGHT_STACK_REPORT_FILE_NAME
        self.puml_file_name = sub_folder + CALLCHAIN_PLANTUML_FILE_NAME
        # configuration files
        depends_folder = DEPENDS_FOLDER
        self.service_definition_file = depends_folder + SERVICE_DEFINITION_FILE_NAME
        self.domain_definition_file = depends_folder + DOMAIN_DEFINITION_FILE_NAME
        self.api_definition_file = depends_folder + API_DEFINITION_FILE_NAME
        self.rule_definition_file = depends_folder + RULE_DEFINITION_FILE_NAME
        self.stack_end_rule_file = depends_folder + STACK_END_RULE_FILE_NAME
        self.load_exist = load_exist
        self.load_original = load_original
        self.extra_rules = (None, None, None, None, None) if extra_rules is None else extra_rules
        self.service_domains, self.service_definitions, self.service_groups, self.domain_definitions, self.api_definitions = self.load_service_domains()
        self.callchain_rules, self.stack_end_rules = self.load_callchain_rules()
        if self.load_exist:
            self.callchain = CallChainParser(*self.extra_rules).refine_callchain(self.load_exist_callchain())
            self.calls = CallChainParser(*self.extra_rules).refine_calls(self.load_exist_calls())
        self.stacks = self.parse_stacks()
        self.highlight_stacks = self.parse_highlight_stacks()
        self.index = 0

    def generate_plantuml_script(self):
        service_groups = self.parse_service_groups()
        with open(self.puml_file_name, 'w') as f:
            f.write('@startuml\n\n')
            for name, services in service_groups.items():
                f.write('box "{0}"\n'.format(name))
                for service in services:
                    f.write('participant "{0}"\n'.format(service))
                f.write('end box\n\n')
            cur_stack = list()
            for cc in self.callchain:
                if len(cur_stack) > 0:
                    if cc[1] == cur_stack[-1][1]:
                        cur_stack.append((cc[1], cc[2], cc[3]))
                    else:
                        while len(cur_stack) > 0 and cur_stack[-1][1] != cc[1]:
                            f.write('return\n')
                            cur_stack = cur_stack[:-1]
                        cur_stack.append((cc[1], cc[2], cc[3]))
                else:
                    cur_stack.append((cc[1], cc[2], cc[3]))
                f.write(self.render_plantuml_call(cur_stack))
                if cur_stack[-1][1] in self.stack_end_rules:
                    f.write('return\n')
                    cur_stack = cur_stack[:-1]
            f.write('return\n\n')
            f.write('@enduml\n')

    def render_plantuml_call(self, stack):
        caller, callee, api = stack[-1]
        pcaller, pcallee, papi = self.get_prev_call_frame(stack, (caller, callee, api))
        compliance, tags = self.parse_call_frame(caller, callee, api, pcaller, pcallee, papi)
        hclr = CRITICAL_CALL_HIGHLIGHT_COLOR
        if compliance:
            return '"{0}" -> "{1}" ++ : {2}{3}\n'.format(caller, callee, api, tags)
        else:
            return '"{0}" -[#{3}]> "{1}" ++ #{3}: <font color={3}>{2}{4}</font>\n'.format(caller, callee, api, hclr,
                                                                                          tags)

    def render_callchain(self, show_label=False, show_tooltip=True, show_link=True, show_order=True):
        g = graphviz.Digraph(self.graph_name + '_callchain', filename=self.callchain_dot_name)
        g.format = 'svg'
        cur_stack = list()
        for cc in self.callchain:
            # stack adjustment
            if len(cur_stack) > 0:
                if cc[1] == cur_stack[-1][1]:
                    cur_stack.append((cc[1], cc[2], cc[3]))
                else:
                    while len(cur_stack) > 0 and cur_stack[-1][1] != cc[1]:
                        cur_stack = cur_stack[:-1]
                    cur_stack.append((cc[1], cc[2], cc[3]))
            else:
                cur_stack.append((cc[1], cc[2], cc[3]))
            if cur_stack[-1][1] in self.stack_end_rules:
                cur_stack = cur_stack[:-1]
            # rendering
            edge_url = self.parse_edge_url(cc[1], cc[2], cc[3])
            if show_label and show_order:
                if len(cc) > 6:
                    label = '{0}[{1}]'.format(cc[3], cc[6])
                else:
                    label = cc[3]
            elif show_label:
                label = cc[3]
            elif show_order:
                label = str(cc[6]) if len(cc) > 6 else ''
            else:
                label = ''
            pcaller, pcallee, papi = self.get_prev_call_frame(cur_stack, (cc[1], cc[2], cc[3]))
            compliance, tags = self.parse_call_frame(cc[1], cc[2], cc[3], pcaller, pcallee, papi)
            if compliance:
                g.node(cc[1], shape='box')
                g.node(cc[2], shape='box')
                g.edge(cc[1], cc[2],
                       label='{0}{1}'.format(label, tags),
                       tooltip=cc[3] if show_tooltip else '',
                       target='_blank',
                       edgehref=edge_url if show_link else '')
            else:
                hclr = CRITICAL_CALL_HIGHLIGHT_COLOR
                g.node(cc[1], shape='box', color=hclr, fontcolor=hclr)
                g.node(cc[2], shape='box', color=hclr, fontcolor=hclr)
                g.edge(cc[1], cc[2],
                       label='{0}{1}'.format(label, tags),
                       tooltip=cc[3] if show_tooltip else '',
                       target='_blank',
                       edgehref=edge_url if show_link else '',
                       color=hclr,
                       fontcolor=hclr)
        return g, self.callchain

    def render_highlight_stacks(self):
        parsed_stacks = self.parse_stack_count()
        rule_table = list()
        for rule in self.highlights:
            stack_table = list()
            for stack_key, count in parsed_stacks.items():
                if stack_key.find(rule) != -1:
                    stack_table.append([stack_key, count])
            rule_content = tabulate(stack_table, tablefmt='plain')
            rule_table.append([rule, rule_content])
        html = tabulate(rule_table, ['Rule', 'Stack'], tablefmt='fancy_grid')
        with open(self.highlight_stack_report_name, 'w') as f:
            f.write(html)

    def render_calls(self):
        parsed_calls = self.parse_call_count()
        caller_table = list()
        for caller, details in parsed_calls.items():
            callee_table = list()
            for callee, detail in details.items():
                api_table = list()
                for api, count in detail.items():
                    api_table.append([api, count])
                api_content = tabulate(api_table, tablefmt='plain')
                callee_table.append([callee, api_content])
            callee_content = tabulate(callee_table, tablefmt='presto')
            caller_table.append([caller, callee_content])
        html = tabulate(caller_table, ['Caller', 'Details'], tablefmt='fancy_grid')
        with open(self.calls_report_name, 'w') as f:
            f.write(html)

    def parse_call_frame(self, caller, callee, api, pcaller=None, pcallee=None, papi=None):
        tags = ''
        if self.manual_highlight:
            compliance = True
            for stack in self.highlight_stacks:
                for call in stack:
                    h1, h2, h3 = call
                    if h1 == caller and h2 == callee and h3 == api:
                        compliance = False
                        break
        else:
            pdomain = self.parse_service_domain(pcallee, papi)
            domain = self.parse_service_domain(callee, api)
            ptags = self.parse_tags(pcallee, pdomain, papi)
            tags = self.parse_tags(callee, domain, api)
            compliance, tags = self.validate_callchain_rules(callee, domain, api, tags, pcallee, pdomain, papi, ptags)
        if tags != '':
            tags = '[{0}]'.format(tags)
        return compliance, tags

    def validate_callchain_rules(self, callee, domain, api, tags, pcallee, pdomain, papi, ptags):
        index = 2
        for rule in self.callchain_rules:
            caller_pattern = '{0}:{1}:{2}:{3}'.format(
                rule['caller_service'] if rule['caller_service'] != '' else '.*',
                rule['caller_domain'] if rule['caller_domain'] != '' else '.*',
                rule['caller_api'] if rule['caller_api'] != '' else '.*',
                rule['caller_tag'] if rule['caller_tag'] != '' else '.*',
            )
            callee_pattern = '{0}:{1}:{2}:{3}'.format(
                rule['callee_service'] if rule['callee_service'] != '' else '.*',
                rule['callee_domain'] if rule['callee_domain'] != '' else '.*',
                rule['callee_api'] if rule['callee_api'] != '' else '.*',
                rule['callee_tag'] if rule['callee_tag'] != '' else '.*',
            )
            for tag in tags:
                for ptag in ptags:
                    caller_key = '{0}:{1}:{2}:{3}'.format(pcallee, pdomain, papi, ptag).replace('None', '*')
                    callee_key = '{0}:{1}:{2}:{3}'.format(callee, domain, api, tag).replace('None', '*')
                    if rule['action'] == 'allow' and \
                            re.match(re.compile(caller_pattern), caller_key) and \
                            re.match(re.compile(callee_pattern), callee_key):
                        return True, index
                    if rule['action'] == 'deny' and \
                            re.match(re.compile(caller_pattern), caller_key) and \
                            re.match(re.compile(callee_pattern), callee_key):
                        return False, index
            index = index + 1
        return True, ''

    def get_prev_call_frame(self, stack, frame):
        copied_stack = copy.deepcopy(stack)
        copied_stack = copied_stack[:-1]
        if len(copied_stack) == 0:
            return None, None, None
        while len(copied_stack) > 0 and copied_stack[-1][1] != frame[0]:
            copied_stack = copied_stack[:-1]
        return copied_stack[-1] if len(copied_stack) > 0 else (None, None, None)

    def parse_call_count(self):
        call_map = {}
        for call in self.calls:
            caller = call[1]
            callee = call[2]
            api = call[3]
            if caller not in call_map:
                call_map[caller] = {}
            if callee not in call_map[caller]:
                call_map[caller][callee] = {}
            if api not in call_map[caller][callee]:
                call_map[caller][callee][api] = 1
            else:
                call_map[caller][callee][api] = call_map[caller][callee][api] + 1
        return call_map

    def parse_stacks(self):
        stacks = list()
        cur_stack = list()
        for cc in self.callchain:
            if len(cur_stack) > 0:
                if cc[1] in self.stack_end_rules:
                    stacks.append(copy.deepcopy(cur_stack))
                    cur_stack = list()
                    cur_stack.append((cc[1], cc[2], cc[3]))
                elif cc[1] == cur_stack[-1][1]:
                    cur_stack.append((cc[1], cc[2], cc[3]))
                else:
                    stacks.append(copy.deepcopy(cur_stack))
                    while len(cur_stack) > 0 and cur_stack[-1][1] != cc[1]:
                        cur_stack = cur_stack[:-1]
                    cur_stack.append((cc[1], cc[2], cc[3]))
            else:
                cur_stack.append((cc[1], cc[2], cc[3]))
        return stacks

    def parse_stack_count(self):
        stack_map = {}
        for stack in self.stacks:
            stack_key = ''
            for call in stack:
                caller = call[0]
                callee = call[1]
                api = call[2]
                if stack_key == '':
                    stack_key += '{0}-{1}->{2}'.format(caller, api, callee)
                else:
                    stack_key += '-{0}->{1}'.format(api, callee)
            if stack_key not in stack_map:
                stack_map[stack_key] = 1
            else:
                stack_map[stack_key] = stack_map[stack_key] + 1
        return stack_map

    def parse_highlight_stacks(self):
        highlight_stacks = list()
        for highlight in self.highlights:
            for stack in self.stacks:
                match = False
                for item in stack:
                    caller, callee, api = item
                    if api == highlight:
                        match = True
                        break
                if match:
                    highlight_stacks.append(stack)
        return highlight_stacks

    def is_critical_api(self, service, api):
        key = '{0}:{1}'.format(service, api)
        if key in self.api_definitions:
            return self.api_definitions[key]['critical']
        return False

    def get_api_link(self, service, api):
        key = '{0}:{1}'.format(service, api)
        if key in self.api_definitions:
            return self.api_definitions[key]['link']
        return ''

    def parse_service_groups(self):
        service_groups = {}
        for name, services in self.service_groups.items():
            for cc in self.callchain:
                for idx in range(1, 3):
                    match = False
                    for service in services:
                        regexp = re.compile('^{0}$'.format(service))
                        if re.match(regexp, cc[idx]) is not None:
                            match = True
                            break
                    if match:
                        if name not in service_groups:
                            service_groups[name] = [cc[idx]]
                        else:
                            if cc[idx] not in service_groups[name]:
                                service_groups[name].append(cc[idx])
        return service_groups

    def parse_service_domain(self, service, api):
        if service is None or api is None:
            return None
        domain = None
        for s, domains in self.service_domains.items():
            if service == s:
                for d, apis in domains.items():
                    if api in apis:
                        domain = d
        return domain

    def parse_tags(self, callee, domain, api):
        key = '{0}:{1}'.format(callee, api)
        tags = self.api_definitions[key]['tags'] if key in self.api_definitions else None
        if tags is None:
            key = '{0}:{1}'.format(callee, domain)
            tags = self.domain_definitions[key]['tags'] if key in self.domain_definitions else None
            if tags is None:
                key = '{0}'.format(callee)
                tags = self.service_definitions[key]['tags'] if key in self.service_definitions else None
                tags = tags if tags is not None else ['*']
        return tags

    def parse_edge_url(self, caller, callee, api):
        api_link = self.get_api_link(callee, api)
        return api if api_link == '' else api_link

    def gen_node_name(self):
        self.index = self.index + 1
        return 'n{0}'.format(self.index)

    def save_callchain(self):
        with open(self.callchain_file_name, 'w') as f:
            f.write(json.dumps(self.callchain))

    def save_calls(self):
        with open(self.calls_file_name, 'w') as f:
            f.write(json.dumps(self.calls))

    def save_stacks(self):
        with open(self.stacks_file_name, 'w') as f:
            f.write(json.dumps(self.stacks))

    def save_highlight_stacks(self):
        with open(self.highlight_stack_file_name, 'w') as f:
            f.write(json.dumps(self.highlight_stacks))

    def load_exist_callchain(self):
        callchain_file = self.original_callchain_file_name if self.load_original else self.callchain_file_name
        with open(callchain_file, 'r') as f:
            callchain = json.loads(f.read(MAX_FILE_READ_LENGTH))
        return callchain

    def load_exist_calls(self):
        calls_file = self.original_calls_file_name if self.load_original else self.calls_file_name
        with open(calls_file, 'r') as f:
            calls = json.loads(f.read(MAX_FILE_READ_LENGTH))
        return calls

    def load_callchain_rules(self):
        callchain_rules = list()
        stack_end_rules = list()
        first_row = True
        with open(self.rule_definition_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                action, caller_service, caller_domain, caller_api, caller_tag, callee_service, callee_domain, callee_api, callee_tag = row
                row_items = set(row)
                if len(row_items) == 1 and list(row_items)[0] == '':
                    continue
                if action.lower() != 'allow' and action.lower() != 'deny':
                    log.error('invalid rule item, `Action` must be in `Allow|Deny`: %s', row)
                    continue
                rule = {
                    'action': action.lower(),
                    'caller_service': caller_service,
                    'caller_domain': caller_domain,
                    'caller_api': caller_api,
                    'caller_tag': caller_tag,
                    'callee_service': callee_service,
                    'callee_domain': callee_domain,
                    'callee_api': caller_api,
                    'callee_tag': callee_tag,
                }
                callchain_rules.append(rule)
        with open(self.stack_end_rule_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                node, = row
                stack_end_rules.append(node)
        return callchain_rules, stack_end_rules

    def load_service_domains(self):
        service_domains = {}
        service_definitions = {}
        service_groups = {}
        domain_definitions = {}
        api_definitions = {}

        # parse service definitions
        first_row = True
        with open(self.service_definition_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                service, group, tags, scope = row
                if service == '' or group == '':
                    continue
                if service not in service_definitions:
                    tags = [x.strip() for x in tags.split(';') if x.strip() != '']
                    service_definitions[service] = {
                        'group': group,
                        'tags': tags if len(tags) > 0 else None,
                        'scope': scope
                    }
        # parse service groups
        for s, info in service_definitions.items():
            group = info['group']
            if group != '':
                if group not in service_groups:
                    service_groups[group] = list()
                service_groups[group].append(s)
        # parse domain definitions
        first_row = True
        with open(self.domain_definition_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                service, domain, tags, scope = row
                if service == '' or domain == '':
                    continue
                if service not in domain_definitions:
                    domain_definitions[service] = {}
                if domain not in domain_definitions[service]:
                    tags = [x.strip() for x in tags.split(';') if x.strip() != '']
                    domain_definitions[service][domain] = {
                        'tags': tags if len(tags) > 0 else None,
                        'scope': scope
                    }
        # parse api definitions
        first_row = True
        with open(self.api_definition_file) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                service, domain, api, critical, tags, link, scope = row
                if service == '' or domain == '' or api == '':
                    continue
                if service not in service_domains:
                    service_domains[service] = {}
                if domain not in service_domains[service]:
                    service_domains[service][domain] = set()
                if api not in service_domains[service][domain]:
                    service_domains[service][domain].add(api)
                key = '{0}:{1}'.format(service, api)
                if key not in api_definitions:
                    tags = [x.strip() for x in tags.split(';') if x.strip() != '']
                    api_definitions[key] = {
                        'critical': True if critical == 'Y' else False,
                        'tags': tags if len(tags) > 0 else None,
                        'link': link,
                        'scope': scope
                    }
        return service_domains, service_definitions, service_groups, domain_definitions, api_definitions


if __name__ == '__main__':
    # parse command line args
    parser = argparse.ArgumentParser(description='Help understand SLS system architecture.')
    parser.add_argument('-l', '--use-local-config', default=False, type=bool, dest='use_local_config', help='use local configurations instead of download from google sheet')
    parser.add_argument('-d', '--cat-datetime', default=None, type=str, dest='cat_datetime', help='cat datetime you want to parse, in "YYYYmmddHH" format')
    parser.add_argument('-r', '--cat-to-root', default=True, type=str, dest='cat_to_root', help='whether goes to cat root call frame')
    args = parser.parse_args()

    initialize(not args.use_local_config)

    # check the following two lines first before running.
    all_scenarios = [ALL_SCENARIOS]
    for scenarios in all_scenarios:
        for name, scenario in scenarios.items():
            enabled = scenario['enabled']
            if not enabled:
                log.info('Skipped scenario: {0}'.format(name))
                continue
            scenario_path = '{0}/{1}/{2}/{3}/'.format(WORKING_DIR, DEFAULT_OUTPUT_SUB_FOLDER_NAME, scenario['region'], scenario['name'])
            if not os.path.exists(scenario_path):
                os.makedirs(scenario_path, exist_ok=True)
            reload = scenario['reload']
            extra_node_overwrite_rules = scenario[
                'extra_node_overwrite_rules'] if 'extra_node_overwrite_rules' in scenario else None
            extra_edge_overwrite_rules = scenario[
                'extra_edge_overwrite_rules'] if 'extra_edge_overwrite_rules' in scenario else None
            extra_rename_rules = scenario['extra_rename_rules'] if 'extra_rename_rules' in scenario else None
            extra_combine_rules = scenario['extra_combine_rules'] if 'extra_combine_rules' in scenario else None
            extra_delete_rules = scenario['extra_delete_rules'] if 'extra_delete_rules' in scenario else None
            extra_rules = (
                extra_node_overwrite_rules,
                extra_edge_overwrite_rules,
                extra_rename_rules,
                extra_combine_rules,
                extra_delete_rules
            )
            extra_callchain = scenario['extra_callchain'] if 'extra_callchain' in scenario else list()
            highlights = scenario['highlights'] if 'highlights' in scenario else None
            if reload:
                log.info('Processing and reload scenario: {0}'.format(name))
                callchain = list()
                original_callchain = list()
                calls = list()
                original_calls = list()
                for entrypoint in scenario['entrypoints']:
                    params = entrypoint + (args.cat_datetime, args.cat_to_root, scenario['region'])
                    occ, ocl = CatDataManager(scenario_path, extra_callchain, extra_rules).parse_callchain_with_links(*params)
                    cc = CallChainParser(*extra_rules).refine_callchain(occ)
                    cl = CallChainParser(*extra_rules).refine_calls(ocl)
                    original_callchain += occ
                    original_calls += ocl
                    callchain += cc
                    calls += cl
                # only the two `originals` will be re-generated if `reload`.
                with open(scenario_path + ORIGINAL_CALLCHAIN_FILE_NAME, 'w') as f:
                    f.write(json.dumps(original_callchain))
                with open(scenario_path + ORIGINAL_CALLS_FILE_NAME, 'w') as f:
                    f.write(json.dumps(original_calls))
                # reparse callchain here to combine items and remove duplicate items, no need to reparse calls
                callchain = CallChainParser(*extra_rules).refine_callchain(callchain)
                ccr = CallChainRender(callchain, calls,
                                      highlights=highlights,
                                      graph_name=scenario['name'],
                                      region=scenario['region'])
            else:
                log.info('Processing scenario without reload: {0}'.format(name))
                ccr = CallChainRender(None, None,
                                      highlights=highlights,
                                      graph_name=scenario['name'],
                                      region=scenario['region'],
                                      load_exist=True,
                                      load_original=True,
                                      extra_rules=extra_rules)
            ccr.save_callchain()
            ccr.save_calls()
            ccr.save_stacks()
            ccr.save_highlight_stacks()
            f, _ = ccr.render_callchain(show_label=True, show_order=True)
            f.render()
            ccr.generate_plantuml_script()
            ccr.render_calls()
            ccr.render_highlight_stacks()
