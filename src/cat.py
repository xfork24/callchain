#!./bin/python
import copy
import datetime
import json
import logging
import random
import time
import requests
import re
import csv
import graphviz
from tabulate import tabulate
import jsonpath_ng as jp
import pandas as pd
from bs4 import BeautifulSoup
from define import *
from rule import *

"""
    {refined}: return refined callchain
    {sample}: get one sampled information
    {callchain}: return callchain information
    {with_links}: return callchain with links
"""


class CatDataManager:
    def __init__(self, output_path='./output',
                 extra_callchain=None,
                 extra_rules=None,
                 links=None):
        random.seed(time.time())
        self.parsed_links = set()
        self.parsed_calls = set()
        self.calls = list()
        self.call_map = {}
        self.index = 0
        self.output_path = output_path
        self.extra_callchain = list() if extra_callchain is None else extra_callchain
        self.extra_rules = [None, None, None, None, None] if extra_rules is None else extra_rules
        self.links = CALLCHAIN_LINK_RULES if links is None else links

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
        msg_paths = list()
        msg_paths.append(
            '$.m_machines.All.m_types."{0}".m_names."{1}".m_statusDists."0".m_sampleMessages'.format(cat_type,
                                                                                                     cat_name))
        msg_paths.append('$.m_machines.All.m_types."{0}".m_statusDists."0".m_sampleMessages'.format(cat_type))
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
        if samples is None:
            return None
        return samples[random.randrange(0, len(samples) - 1)]

    def get_sample_message_report(self, cat_domain, cat_type, cat_name, cat_date=None, to_root=True):
        message_id = self.get_sample_message(cat_domain, cat_type, cat_name, cat_date)
        log.info('sample message Id: {0}'.format(message_id))
        if message_id is None:
            return None
        return self.get_message_report(message_id, to_root)

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
            all_callchain += [self.get_call_overwrite('-', 'External', root_frame_name, root_call_name, '', '')]
            all_callchain += self.parse_callchain(root_df, root_frame_name)
        return all_callchain

    def parse_root_frame_name(self, frame):
        root_frame_name = frame[1].tolist()[0]
        root_frame_call = frame[2].tolist()[0]
        return root_frame_name, root_frame_call

    def get_callchain_with_links(self, cat_domain, cat_type, cat_name, sample_count=1, link_sample_count=10,
                                 cat_date=None, to_root=True, region='ID'):
        all_callchain = self.get_callchain(cat_domain, cat_type, cat_name, sample_count, cat_date, to_root)
        all_callchain += self.extra_callchain
        for i in range(CALLCHAIN_LINK_ANALYSIS_LIMIT):
            all_callchain += self.parse_callchain_link(all_callchain, link_sample_count, cat_date, region)
        return all_callchain

    def get_callchain_and_report_with_links(self, cat_domain, cat_type, cat_name, sample_count=1, link_sample_count=10,
                                            cat_date=None, to_root=True, region='ID'):
        original_callchain = self.get_callchain_with_links(cat_domain, cat_type, cat_name, sample_count,
                                                           link_sample_count, cat_date, to_root, region)
        return original_callchain, self.calls

    def get_message_report(self, message_id, to_root=True):
        url = CAT_API_ENDPOINT + CAT_MESSAGE_SUB_URL.format(message_id)
        headers = self.build_headers()
        response = self.get_cat_url(url, headers)
        if response is None:
            return None
        df = self.parse_message_report(response.text)
        header = df[0].iloc[[0]][0]
        root_id = header.split(' ')[-3]
        if root_id == 'null' or not to_root:
            # already in root message or we don't go to root
            return df.iloc[1:]
        else:
            url = CAT_API_ENDPOINT + CAT_MESSAGE_SUB_URL.format(root_id)
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
        callchain = CallChainParser(*self.extra_rules).refine_callchain(callchain)
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
                    parsed = self.get_call_overwrite('-', rule[9], rule[10], rule[11], None, None)
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
                            txts = td.findAll(text=True, recursive=True)
                            for txt in txts:
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
        columns = [0, 1, 2, 3, 4]
        return pd.DataFrame(data=records, columns=columns)

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
                if self.call_map[key] > ENDPOINT_DEFAULT_CALL_LIMIT:
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


class CallChainParser:
    def __init__(self, extra_node_overwrite_rules=None, extra_edge_overwrite_rules=None, extra_rename_rules=None,
                 extra_combine_rules=None, extra_delete_rules=None):
        self.extra_node_overwrite_rules = {} if extra_node_overwrite_rules is None else extra_node_overwrite_rules
        self.extra_edge_overwrite_rules = {} if extra_edge_overwrite_rules is None else extra_edge_overwrite_rules
        self.extra_rename_rules = list() if extra_rename_rules is None else extra_rename_rules
        self.extra_combine_rules = list() if extra_combine_rules is None else extra_combine_rules
        self.extra_delete_rules = list() if extra_delete_rules is None else extra_delete_rules

    def parse_call_count(self, calls):
        call_map = {}
        for call in calls:
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

    def parse_stack_count(self, stacks):
        stack_map = {}
        for stack in stacks:
            stack_key = ''
            for call in stack:
                caller = call[0]
                api = call[1]
                if api is None:
                    stack_key += '{0}'.format(caller)
                else:
                    stack_key += '{0}-{1}->'.format(caller, api)
            if stack_key not in stack_map:
                stack_map[stack_key] = 1
            else:
                stack_map[stack_key] = stack_map[stack_key] + 1
        return stack_map

    def parse_stack_count_v2(self, stacks):
        stack_map = {}
        for stack in stacks:
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

    def refine_callchain(self, callchain):
        callchain = self.refine_node_overwrite_rules(callchain)
        callchain = self.refine_edge_overwrite_rules(callchain)
        callchain = self.refine_rename_rules(callchain)
        callchain = self.refine_combine_rules(callchain)
        callchain = self.refine_delete_rules(callchain)
        callchain = self.refine_remove_duplicate(callchain)
        callchain = self.refine_remove_reentry(callchain)
        callchain = self.refine_hide_infra_delete_rules(callchain)
        return callchain

    def refine_calls(self, calls):
        refined_calls = list()
        for call in calls:
            record = self.refine_single_call(call)
            if record is not None:
                refined_calls.append(record)
        return refined_calls

    def parse_stacks(self, callchain):
        stacks = list()
        cur_stack = list()
        for cc in callchain:
            if len(cur_stack) > 0:
                if cc[1] in CALLSTACK_END_RULES:
                    stacks.append(copy.deepcopy(cur_stack))
                    cur_stack = list()
                    cur_stack.append((cc[1], cc[3]))
                    cur_stack.append((cc[2], None))
                elif cc[1] == cur_stack[-1][0]:
                    cur_stack[-1] = (cc[1], cc[3])
                    cur_stack.append((cc[2], None))
                else:
                    stacks.append(copy.deepcopy(cur_stack))
                    while len(cur_stack) > 0 and cur_stack[-1][0] != cc[1]:
                        cur_stack = cur_stack[:-1]
                    if len(cur_stack) > 0:
                        cur_stack[-1] = (cc[1], cc[3])
                    cur_stack.append((cc[2], None))
            else:
                cur_stack.append((cc[1], cc[3]))
                cur_stack.append((cc[2], None))
        return stacks

    def parse_stacks_v2(self, callchain):
        stacks = list()
        cur_stack = list()
        for cc in callchain:
            if len(cur_stack) > 0:
                if cc[1] in CALLSTACK_END_RULES:
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

    def parse_highlight_stacks(self, stacks, highlights):
        highlight_stacks = list()
        for highlight in highlights:
            for stack in stacks:
                match = False
                for item in stack:
                    caller, callee, api = item
                    if api == highlight:
                        match = True
                        break
                if match:
                    highlight_stacks.append(stack)
        return highlight_stacks

    def parse_service_groups(self, callchain, sg_definitions):
        service_groups = {}
        for name, services in sg_definitions.items():
            for cc in callchain:
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

    def refine_single_call(self, callchain):
        callchain = [callchain]
        callchain = self.refine_node_overwrite_rules(callchain)
        callchain = self.refine_edge_overwrite_rules(callchain)
        callchain = self.refine_rename_rules(callchain)
        callchain = self.refine_delete_rules(callchain)
        callchain = self.refine_remove_reentry(callchain)
        callchain = self.refine_hide_infra_delete_rules(callchain)
        return callchain[0] if len(callchain) != 0 else None

    def refine_node_overwrite_rules(self, callchain):
        refined = callchain
        for rules in [self.extra_node_overwrite_rules, CALLCHAIN_NODE_OVERWRITE_RULES]:
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
        for rules in [self.extra_edge_overwrite_rules, CALLCHAIN_EDGE_OVERWRITE_RULES]:
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
        for rules in [self.extra_rename_rules, CALLCHAIN_RENAME_RULES]:
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
                            index, new_name = part.split(':')
                            cc_new[int(index)] = new_name
                        refined.append(cc_new)
                    else:
                        refined.append(cc)
                callchain = refined
        return refined

    def refine_combine_rules(self, callchain):
        refined = callchain
        for rules in [self.extra_combine_rules, CALLCHAIN_COMBINE_RULES]:
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
        for rules in [self.extra_delete_rules, CALLCHAIN_DELETE_RULES]:
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

    def refine_hide_infra_delete_rules(self, callchain):
        refined = callchain
        for rule in CALLCHAIN_HIDE_INFRA_DELETE_RULES:
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


class CallChainRender:
    def __init__(self, callchain, calls, highlights=None, graph_name='sample', region='ID', output_path=None,
                 load_exist=False, load_original=True, extra_rules=None):
        self.callchain = callchain
        self.calls = calls
        self.manual_highlight = highlights is not None
        self.highlights = list() if highlights is None else highlights
        self.graph_name = graph_name
        self.region = region
        sub_folder = '../{0}/{1}/{2}/'.format(DEFAULT_OUTPUT_SUB_FOLDER_NAME, region,
                                              graph_name) if output_path is None else output_path
        # original files
        self.original_callchain_file_name = sub_folder + 'original_callchain.txt'
        self.original_calls_file_name = sub_folder + 'original_calls.txt'
        # parsed files
        self.callchain_file_name = sub_folder + 'callchain.txt'
        self.calls_file_name = sub_folder + 'calls.txt'
        self.stacks_file_name = sub_folder + 'stacks.txt'
        self.highlight_stack_file_name = sub_folder + 'highlight_stacks.txt'
        # report files
        self.callchain_dot_name = sub_folder + 'callchain.dot'
        self.calls_dot_name = sub_folder + 'calls.dot'
        self.calls_report_name = sub_folder + 'calls.report.txt'
        self.highlight_stack_report_name = sub_folder + 'highlight_stacks.report.txt'
        self.puml_file_name = sub_folder + 'sequence.puml'
        self.rule_violation_report_name = sub_folder + 'rules.report.txt'
        # configuration files
        self.service_definition_file_name = '../services.csv'
        self.domain_definition_file_name = '../domains.csv'
        self.api_definition_file_name = '../apis.csv'
        self.rule_definition_file_name = '../rules.csv'
        self.load_exist = load_exist
        self.load_original = load_original
        self.extra_rules = (None, None, None) if extra_rules is None else extra_rules
        if self.load_exist:
            self.callchain = CallChainParser(*self.extra_rules).refine_callchain(self.load_exist_callchain())
            self.calls = CallChainParser(*self.extra_rules).refine_calls(self.load_exist_calls())
        self.stacks = CallChainParser(*self.extra_rules).parse_stacks_v2(self.callchain)
        self.highlight_stacks = CallChainParser(*self.extra_rules).parse_highlight_stacks(self.stacks, self.highlights)
        self.service_domains, self.service_definitions, self.domain_definitions, self.api_definitions = self.load_service_domains()
        self.callchain_rules = self.load_callchain_rules()
        self.index = 0

    def generate_plantuml_script(self):
        service_groups = CallChainParser(self.extra_rules).parse_service_groups(self.callchain, SLS_SERVICE_GROUPS)
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
                if cur_stack[-1][1] in CALLSTACK_END_RULES:
                    f.write('return\n')
                    cur_stack = cur_stack[:-1]
            f.write('return\n\n')
            f.write('@enduml\n')

    def render_plantuml_call(self, stack):
        caller, callee, api = stack[-1]
        pcaller, pcallee, papi = self.get_prev_call_frame(stack, (caller, callee, api))
        compliance, tags = self.parse_call_frame_v2(caller, callee, api, pcaller, pcallee, papi)
        hclr = CRITICAL_CALL_HIGHLIGHT_COLOR
        if compliance:
            return '"{0}" -> "{1}" ++ : {2}{3}\n'.format(caller, callee, api, tags)
        else:
            return '"{0}" -[#{3}]-> "{1}" ++ #{3}: <font color={3}>{2}{4}</font>\n'.format(caller, callee, api, hclr, tags)

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
            if cur_stack[-1][1] in CALLSTACK_END_RULES:
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
            compliance, tags = self.parse_call_frame_v2(cc[1], cc[2], cc[3], pcaller, pcallee, papi)
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
        parsed_stacks = CallChainParser(self.extra_rules).parse_stack_count_v2(self.stacks)
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

    def render_calls_v2(self):
        parsed_calls = CallChainParser(self.extra_rules).parse_call_count(self.calls)
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

    def render_calls(self):
        g = graphviz.Digraph(self.graph_name + '_calls', filename=self.calls_dot_name)
        g.format = 'svg'
        parsed_calls = CallChainParser(self.extra_rules).parse_call_count(self.calls)
        for caller, details in parsed_calls.items():
            sub = graphviz.Digraph(caller)
            sub.engine = 'twopi'
            n1 = self.gen_node_name()
            sub.node(n1, label=caller, shape='box')
            for callee, detail in details.items():
                table = list()
                for api, count in detail.items():
                    table.append([api, count])
                label = tabulate(table, ['API', 'Count'], tablefmt="simple")
                n2 = self.gen_node_name()
                sub.node(n2, label=label, shape='box')
                sub.edge(n1, n2)
            g.subgraph(sub)
        return g, self.calls

    def parse_call_frame(self, caller, callee, api, pcaller=None, pcallee=None, papi=None):
        tags = ''
        if self.manual_highlight:
            compliance = True
            for stack in self.highlight_stacks:
                for call in stack:
                    caller, callee, api = call
                    if caller == caller and callee == callee and api == api:
                        compliance = False
                        break
        else:
            pdomain = self.parse_service_domain(pcallee, papi)
            domain = self.parse_service_domain(callee, api)
            if self.validate_service_level_rules(caller, callee) and \
                    self.validate_domain_level_rules(callee, domain, pcallee, pdomain) and \
                    self.validate_api_level_rules(callee, domain, api, pcallee, pdomain, papi) and \
                    self.validate_tag_level_rules(callee, domain, api, pcallee, pdomain, papi):
                compliance = True
            else:
                compliance = False
        if not compliance and not self.manual_highlight:
            tags += 'x'
        if self.is_critical_api(callee, api):
            tags += 'c'
        if tags != '':
            tags = '[{0}]'.format(tags)
        return compliance, tags

    def parse_call_frame_v2(self, caller, callee, api, pcaller=None, pcallee=None, papi=None):
        tags = ''
        if self.manual_highlight:
            compliance = True
            for stack in self.highlight_stacks:
                for call in stack:
                    caller, callee, api = call
                    if caller == caller and callee == callee and api == api:
                        compliance = False
                        break
        else:
            pdomain = self.parse_service_domain(pcallee, papi)
            domain = self.parse_service_domain(callee, api)
            pkey = '{0}:{1}'.format(pcallee, papi)
            key = '{0}:{1}'.format(callee, api)
            ptags = self.api_definitions[pkey]['tags'] if pkey in self.api_definitions else list()
            tags = self.api_definitions[key]['tags'] if key in self.api_definitions else list()
            compliance, tags = self.validate_callchain_rules(callee, domain, api, tags, pcallee, pdomain, papi, ptags)
            if compliance:
                compliance = True
            else:
                compliance = False
        if tags != '':
            tags = '[{0}]'.format(tags)
        return compliance, tags

    def get_prev_call_frame(self, stack, frame):
        copied_stack = copy.deepcopy(stack)
        copied_stack = copied_stack[:-1]
        if len(copied_stack) == 0:
            return None, None, None
        while len(copied_stack) > 0 and copied_stack[-1][1] != frame[0]:
            copied_stack = copied_stack[:-1]
        return copied_stack[-1] if len(copied_stack) > 0 else (None, None, None)

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

    def validate_service_level_rules(self, s1, s2):
        if s1 is None or s2 is None:
            return True
        matched, key = self.re_key_in_col(s1, SERVICE_LEVEL_COMPLIANCE_RULES)
        if matched:
            callees = SERVICE_LEVEL_COMPLIANCE_RULES[key]
            matched, _ = self.re_key_in_col(s2, callees)
            if not matched:
                return False
        matched, key = self.re_key_in_col(s1, SERVICE_LEVEL_VIOLATION_RULES)
        if matched:
            callees = SERVICE_LEVEL_VIOLATION_RULES[key]
            matched, _ = self.re_key_in_col(s2, callees)
            if matched:
                return False
        return True

    def validate_domain_level_rules(self, callee, domain, pcallee, pdomain):
        if pcallee is None or pdomain is None or callee is None or domain is None:
            return True
        rule_defined, rule_passed = False, False
        pkey = '{0}:{1}'.format(pcallee, pdomain)
        key = '{0}:{1}'.format(callee, domain)
        for item in DOMAIN_LEVEL_COMPLIANCE_RULES:
            if re.match(re.compile(pkey), item[0]) is not None or re.match(re.compile(key), item[1]) is not None:
                rule_defined = True
                if re.match(re.compile(pkey), item[0]) is not None and re.match(re.compile(key), item[1]) is not None:
                    rule_passed = True
                    break
        if rule_defined and not rule_passed:
            return False
        for item in DOMAIN_LEVEL_VIOLATION_RULES:
            if re.match(re.compile(pkey), item[0]) is not None and re.match(re.compile(key), item[1]) is not None:
                return False
        return True

    def validate_api_level_rules(self, callee, domain, api, pcallee, pdomain, papi):
        if pcallee is None or pdomain is None or papi is None or callee is None or domain is None or api is None:
            return True
        rule_defined, rule_passed = False, False
        pkey = '{0}:{1}:{2}'.format(pcallee, pdomain, papi)
        key = '{0}:{1}:{2}'.format(callee, domain, api)
        for item in API_LEVEL_COMPLIANCE_RULES:
            if re.match(re.compile(pkey), item[0]) is not None or re.match(re.compile(key), item[1]) is not None:
                rule_defined = True
                if re.match(re.compile(pkey), item[0]) is not None and re.match(re.compile(key), item[1]) is not None:
                    rule_passed = True
        if rule_defined and not rule_passed:
            return False
        for item in API_LEVEL_VIOLATION_RULES:
            if re.match(re.compile(pkey), item[0]) is not None and re.match(re.compile(key), item[1]) is not None:
                return False
        return True

    def validate_tag_level_rules(self, callee, domain, api, pcallee, pdomain, papi):
        if callee is None or domain is None or api is None or pcallee is None or pdomain is None or papi is None:
            return True
        rule_defined, rule_passed = False, False
        pkey = '{0}:{1}'.format(pcallee, papi)
        key = '{0}:{1}'.format(callee, api)
        ptags = self.api_definitions[pkey]['tags'] if pkey in self.api_definitions else None
        tags = self.api_definitions[key]['tags'] if key in self.api_definitions else None
        if ptags is None or tags is None:
            return True
        for item in TAG_LEVEL_COMPLIANCE_RULES:
            if item[0] in ptags or item[1] in tags:
                rule_defined = True
                if item[0] in ptags and item[1] in tags:
                    rule_passed = True
        if rule_defined and not rule_passed:
            return False
        for item in TAG_LEVEL_VIOLATION_RULES:
            if item[0] in ptags and item[1] in tags:
                return False
        return True

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
            if len(tags) == 0 and len(ptags) == 0:
                caller_key = '{0}:{1}:{2}:*'.format(pcallee, pdomain, papi).replace('None', '*')
                callee_key = '{0}:{1}:{2}:*'.format(callee, domain, api).replace('None', '*')
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

    def re_key_in_col(self, key, col):
        match = False
        matched_key = ''
        for k in col:
            regexp = re.compile('^{0}$'.format(k))
            if re.match(regexp, key):
                match = True
                matched_key = k
                break
        return match, matched_key

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
        first_row = True
        with open(self.rule_definition_file_name) as f:
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
        return callchain_rules

    def load_service_domains(self):
        service_domains = {}
        service_definitions = {}
        domain_definitions = {}
        api_definitions = {}

        # parse service definitions
        first_row = True
        with open(self.service_definition_file_name) as f:
            csv_reader = csv.reader(f, delimiter=',')
            for row in csv_reader:
                if first_row:
                    first_row = False
                    continue
                service, group, tags, scope = row
                if service == '' or group == '':
                    continue
                if service not in service_definitions:
                    service_definitions[service] = {
                        'group': group,
                        'tags': [x.strip() for x in tags.split(';') if x.strip() != ''],
                        'scope': scope
                    }
        # parse domain definitions
        first_row = True
        with open(self.domain_definition_file_name) as f:
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
                    domain_definitions[service][domain] = {
                        'tags': [x.strip() for x in tags.split(';') if x.strip() != ''],
                        'scope': scope
                    }
        # parse api definitions
        first_row = True
        with open(self.api_definition_file_name) as f:
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
                    api_definitions[key] = {
                        'critical': True if critical == 'Y' else False,
                        'tags': [x.strip() for x in tags.split(';') if x.strip() != ''],
                        'link': link,
                        'scope': scope
                    }
        return service_domains, service_definitions, domain_definitions, api_definitions

