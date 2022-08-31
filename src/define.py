#!./bin/python

import logging

CAT_JWT_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJjYXQiLCJvcHRyIjoibGZzIn0.oD3U9BzjuKvomor6ASfe8yXuaov1rhMJmf5KyIZlpto'
CAT_API_ENDPOINT = 'https://cat-api.i.ssc.shopee.io'
CAT_TRANSACTION_REPORT_SUB_URL = '/cat/r/transaction_report'
CAT_MESSAGE_SUB_URL = '/cat/r/message_report/{0}'
CAT_IP = 'All'
CAT_DATA_FORMAT = 'json'
ENDPOINT_DEFAULT_CALL_LIMIT = 100
CALLCHAIN_LINK_ANALYSIS_LIMIT = 5
MAX_FILE_READ_LENGTH = 4194304
DEFAULT_OUTPUT_SUB_FOLDER_NAME = 'scenarios'
CRITICAL_CALL_HIGHLIGHT_COLOR = 'red'

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
log = logging.getLogger('root')
