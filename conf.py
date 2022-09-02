#!./bin/python

import logging

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

