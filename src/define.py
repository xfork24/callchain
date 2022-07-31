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

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
log = logging.getLogger('root')

# Execution Order: RENAME -> COMBINE -> DELETE
# High priority rules should be put in the front.
# SLS API related renaming rules should be defined in scenario specific places because it has many possible mappings.
CALLCHAIN_RENAME_RULES = [
    # (event_id, callee, caller, api, reserved, reserved, index:rename_to)
    ("*", "(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)", "Kafka", "ProduceTrackingPushMessage", '*', '*', '2:PIS-Saturn'),

    ('*', '(OrderCreateJob|UpdateLogisticInfoToOmsJob)', 'Task\\.Retry', '(OrderCreate/OrderCreateJob|OrderTnNotify/UpdateLogisticInfoToOmsJob)', '*', '*', '2:Saturn'),

    ('*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)', '*', '*', '*', '*', '1:PIS'),
    ('*', '*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)', '*', '*', '*', '2:PIS'),

    ('*', '(API\\.api\\.sls\\.shopee\\.com\\.*|API\\.api\\.sls\\.shopee\\.*)', '*', '*', '*', '*', '1:SLS-Logistics'),
    ('*', '*', '(API\\.api\\.sls\\.shopee\\.com\\.*|API\\.api\\.sls\\.shopee\\.*)', '*', '*', '*', '2:SLS-Logistics'),

    ('*', 'API\\.lcs\\-electronicproofgrpc\\-*', '*', '*', '*', '*', '1:EP-Service'),
    ('*', '*', 'API\\.lcs\\-electronicproofgrpc\\-*', '*', '*', '*', '2:EP-Service'),

    ('*', 'API\\.tracking\\-grpc\\-*', '*', '*', '*', '*', '1:LTS'),
    ('*', '*', 'API\\.tracking\\-grpc\\-*', '*', '*', '*', '2:LTS'),

    ('*', 'API\\.admin\\.shopee\\.*', '*', '*', '*', '*', '1:Admin-API'),
    ('*', '*', 'API\\.admin\\.shopee\\.*', '*', '*', '*', '2:Admin-API'),

    ('*', 'API\\.routing\\.geo\\.shopee\\.*', '*', '*', '*', '*', '1:GEO'),
    ('*', '*', 'API\\.routing\\.geo\\.shopee\\.*', '*', '*', '*', '2:GEO'),

    ('*', '(API\\.ops\\.ssc\\.shopeemobile\\.com)', '*', '*', '*', '*', '1:OPS'),
    ('*', '*', '(API\\.ops\\.ssc\\.shopeemobile\\.com)', '*', '*', '*', '2:OPS'),

    ('*', '(API\\.logistics\\-api\\.shopee\\.co\\.*|API\\.logistics\\-api\\.shopee\\.com\\.*|API\\.logistics\\-api\\.shopee\\.*)', '*', '*', '*', '*', '1:LogisticsAPI'),
    ('*', '*', '(API\\.logistics\\-api\\.shopee\\.co\\.*|API\\.logistics\\-api\\.shopee\\.com\\.*|API\\.logistics\\-api\\.shopee\\.*)', '*', '*', '*', '2:LogisticsAPI'),

    ('*', '(API.sls\\-rateapi\\-live\\-*|API\\.sls\\-rateapi\\-live\\-*)', '*', '*', '*', '*', '1:RateAPI'),
    ('*', '*', '(API.sls\\-rateapi\\-live\\-*|API\\.sls\\-rateapi\\-live\\-*)', '*', '*', '*', '2:RateAPI'),

    ('*', '(API\\.sls\\-rateapioffline\\-live\\-*)', '*', '*', '*', '*', '1:RateAPI-Offline'),
    ('*', '*', '(API\\.sls\\-rateapioffline\\-live\\-*)', '*', '*', '*', '2:RateAPI-Offline'),

    ('*', '(API\\.oms\\.shopee\\.co\\.id|API\\.oms\\-parcelapi\\-live\\-id)', '*', '*', '*', '*', '1:OMS'),
    ('*', '*', '(API\\.oms\\.shopee\\.co\\.id|API\\.oms\\-parcelapi\\-live\\-id)', '*', '*', '*', '2:OMS'),

    ('*', '(API\\.sls\\-locationgrpc\\-live\\-*|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.co\\.*|SlsLocation|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.*|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.*)', '*', '*', '*', '*', '1:SLS-Location'),
    ('*', '*', '(API\\.sls\\-locationgrpc\\-live\\-*|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.co\\.*|SlsLocation|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.*|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.*)', '*', '*', '*', '2:SLS-Location'),

    ('*', 'API\\.c\\-api\\-sellerbasicservice\\.shopeemobile\\.com', '*', '*', '*', '*', '1:SellerBasicService'),
    ('*', '*', 'API\\.c\\-api\\-sellerbasicservice\\.shopeemobile\\.com', '*', '*', '*', '2:SellerBasicService'),

    ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', '*', '*', '*', '*', '1:LFS'),
    ('*', '*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', '*', '*', '*', '2:LFS'),

    ('*', '(API\\.fleet\\-order\\.ssc\\.shopee\\.co\\.*|fleet_order_read_facade\\.Gray|Fleet_Order_Client)', '*', '*', '*', '*', '1:FleetOrder'),
    ('*', '*', '(API\\.fleet\\-order\\.ssc\\.shopee\\.co\\.*|fleet_order_read_facade\\.Gray|Fleet_Order_Client)', '*', '*', '*', '2:FleetOrder'),

    ('*', '(API\\.api\\.lps\\.shopee\\.co\\.*|URL\\.lps\\-api\\-live\\-*|API\\.lps\\-grpc\\-live\\-*|API\\.api\\.lps\\.shopee\\.*)', '*', '*', '*', '*', '1:LPS'),
    ('*', '*', '(API\\.api\\.lps\\.shopee\\.co\\.*|URL\\.lps\\-api\\-live\\-*|API\\.lps\\-grpc\\-live\\-*|API\\.api\\.lps\\.shopee\\.*)', '*', '*', '*', '2:LPS'),

    ('*', 'API\\.api\\-lps\\-livetest\\.ssc\\.shopee\\.com\\.*', '*', '*', '*', '*', '1:LPS-LiveTest'),
    ('*', '*', 'API\\.api\\-lps\\-livetest\\.ssc\\.shopee\\.com\\.*', '*', '*', '*', '2:LPS-LiveTest'),

    ('*', 'API\\.livetest\\.ssc\\.shopee\\.co\\.*', '*', '*', '*', '*', '1:LiveTestAPI'),
    ('*', '*', 'API\\.livetest\\.ssc\\.shopee\\.co\\.*', '*', '*', '*', '2:LiveTestAPI'),

    ('*', '(URL\\.lls\\-grpc\\-*|API\\.lls\\-grpc.ssc\\.shopee\\.co\\.*|LLSGrpc\\-*|API\\.lls\\-grpc\\-*|API\\.lls\\-fulfillment\\-*|API\\.lls\\-query\\-*|LLS\\-FULFILLMENT\\-LIVE\\-*)', '*', '*', '*', '*', '1:LLS'),
    ('*', '*', '(URL\\.lls\\-grpc\\-*|API\\.lls\\-grpc.ssc\\.shopee\\.co\\.*|LLSGrpc\\-*|API\\.lls\\-grpc\\-*|API\\.lls\\-fulfillment\\-*|API\\.lls\\-query\\-*|LLS\\-FULFILLMENT\\-LIVE\\-*)', '*', '*', '*', '2:LLS'),

    ('*', '(API\\.lcos\\-grpc\\-*|URL\\.lcos\\-checkout\\-*|API\\.lcos\\-checkout\\-*|URL\\.lcos\\-grpc\\-*|API\\.lcos\\-grpc\\.shopee\\.co\\.*|LcosSdk)', '*', '*', '*', '*', '1:LCOS'),
    ('*', '*', '(API\\.lcos\\-grpc\\-*|URL\\.lcos\\-checkout\\-*|API\\.lcos\\-checkout\\-*|URL\\.lcos\\-grpc\\-*|API\\.lcos\\-grpc\\.shopee\\.co\\.*|LcosSdk)', '*', '*', '*', '2:LCOS'),

    ('*', '(API\\.lcs\\-api\\.shopee\\.co\\.*|API\\.lcs\\-api\\.shopee\\.*|CHANNEL_API\\.LCS|LcsLineWayBill)', '*', '*', '*', '*', '1:LCS'),
    ('*', '*', '(API\\.lcs\\-api\\.shopee\\.co\\.*|API\\.lcs\\-api\\.shopee\\.*|CHANNEL_API\\.LCS|LcsLineWayBill)', '*', '*', '*', '2:LCS'),

    ('*', '(URL\\.wbc\\-static\\-*|WaybillCenterGRPC\\-*|API\\.wbc\\-static\\-*|API\\.wbc\\-eventbusproxy\\-*|API\\.waybillcenter\\.ssc\\.shopee\\.co\\.*)', '*', '*', '*', '*', '1:WBC'),
    ('*', '*', '(URL\\.wbc\\-static\\-*|WaybillCenterGRPC\\-*|API\\.wbc\\-static\\-*|API\\.wbc\\-eventbusproxy\\-*|API\\.waybillcenter\\.ssc\\.shopee\\.co\\.*)', '*', '*', '*', '2:WBC'),

    ('*', '(API\\.spx\\.shopee\\.co\\.*|API\\.sp\\.spx\\.shopee\\.co\\.id|API\\.spx\\-container\\-service\\.ssc\\.shopee\\.co\\.*|SpRemoteApi|API\\.spx\\-smartsorting\\.ssc\\.shopee\\.co\\.*)', '*', '*', '*', '*', '1:SPX'),
    ('*', '*', '(API\\.spx\\.shopee\\.co\\.*|API\\.sp\\.spx\\.shopee\\.co\\.id|API\\.spx\\-container\\-service\\.ssc\\.shopee\\.co\\.*|SpRemoteApi|API\\.spx\\-smartsorting\\.ssc\\.shopee\\.co\\.*)', '*', '*', '*', '2:SPX'),

    ('*', 'API\\.smartrouting\\-grpc\\-live\\-*', '*', '*', '*', '*', '1:SmartRouting'),
    ('*', '*', 'API\\.smartrouting\\-grpc\\-live\\-*', '*', '*', '*', '2:SmartRouting'),

    ('*', '(API\\.tws\\.shopeemobile\\.com|API\\.tws\\.shopeesz\\.com)', '*', '*', '*', '*', '1:TWS'),
    ('*', '*', '(API\\.tws\\.shopeemobile\\.com|API\\.tws\\.shopeesz\\.com)', '*', '*', '*', '2:TWS'),

    ('*', '(API\\.external2\\.shopee\\.co\\.*|API\\.shopeeapi\\-pre\\.idexpress\\.com|API\\.pickup\\.sicepat\\.com|API\\.secure\\-jk\\.jet\\.co\\.*|API\\.partner\\-api\\.grab\\.com|API\\.anteraja\\-prod\\.apigee\\.net|API\\.shopee\\.jtcargo\\.co\\.*|API\\.api\\.sentralcargo\\.co\\.*|API\\.food\\-open\\.shopee\\.co\\.*|API\\.api\\.ninjavan\\.co|API\\.ecc2c\\.presco\\.com\\.*|API\\.ecservice\\.hilife\\.com\\.*|API\\.external2\\.shopee\\.*|API\\.eservice\\.presco\\.com\\.*|API\\.schemas\\.xmlsoap\\.org)', '*', '*', '*', '*', '1:3PL'),
    ('*', '*', '(API\\.external2\\.shopee\\.co\\.*|API\\.shopeeapi\\-pre\\.idexpress\\.com|API\\.pickup\\.sicepat\\.com|API\\.secure\\-jk\\.jet\\.co\\.*|API\\.partner\\-api\\.grab\\.com|API\\.anteraja\\-prod\\.apigee\\.net|API\\.shopee\\.jtcargo\\.co\\.*|API\\.api\\.sentralcargo\\.co\\.*|API\\.food\\-open\\.shopee\\.co\\.*|API\\.api\\.ninjavan\\.co|API\\.ecc2c\\.presco\\.com\\.*|API\\.ecservice\\.hilife\\.com\\.*|API\\.external2\\.shopee\\.*|API\\.eservice\\.presco\\.com\\.*|API\\.schemas\\.xmlsoap\\.org)', '*', '*', '*', '2:3PL'),

    ('*', 'API\\.charge\\.ssc\\.shopeemobile\\.com', '*', '*', '*', '*', '1:Charge-API'),
    ('*', '*', 'API\\.charge\\.ssc\\.shopeemobile\\.com', '*', '*', '*', '2:Charge-API'),

    ('*', 'API\\.idcs\\-server\\-live\\-*', '*', '*', '*', '*', '1:IDCS'),
    ('*', '*', 'API\\.idcs\\-server\\-live\\-*', '*', '*', '*', '2:IDCS'),

    ('*', '*', 'RabbitMQ\\.rabbitmq\\.i\\.ssc\\-2\\.ctl\\.sz\\.shopee\\.io', '*', '*', '*', '2:RabbitMQ'),

    ('*', '*', '(LocalCacheReport|LocalCache|LayerCache|LayeredCache|Cache|Redis\\.proxy\\.cache\\-codis[0-9]\\-ctl\\.i\\.sz\\.shopee\\.io|Redis:proxy\\.cache\\-codis[0-9]\\-ctl.i.sz.shopee.io:*)', '*', '*', '*', '2:Redis'),
    ('*', '*', '^(MySQL:*|CdtDbQueryTimes|CdtGetInfo)$', '*', '*', '*', '2:MySQL'),
    ('*', '*', '^(PN\\-Kafka|WBC\\-Kafka)$', '*', '*', '*', '2:Kafka'),
    ('*', '*', '^Es$', '*', '*', '*', '2:ElasticSearch'),

    ('*', 'Task\\.Send', '*', '*', '*', '*', '1:Saturn'),
    ('*', '*', 'Task\\.Send', '*', '*', '*', '2:Saturn'),

    ('*', 'Task\\.send', '*', '*', '*', '*', '1:Celery'),
    ('*', '*', 'Task\\.send', '*', '*', '*', '2:Celery'),
]

CALLCHAIN_COMBINE_RULES = ['Redis', 'Kafka', 'MySQL']

CALLCHAIN_DELETE_RULES = [
    # (event_id, callee, caller, api, *, *)
    ('*', '*', 'CatOrderLPIS', '*', '*', '*'),
    ('*', '*', 'OrderDetail', '*', '*', '*'),
    ('*', '*', 'OneApi', '*', '*', '*'),
    ('*', '*', '(gRpc|GrpcApi)', '*', '*', '*'),
    ('*', '*', 'MmapLoads', '*', '*', '*'),
    ('*', '*', 'DeprecationWarning', '*', '*', '*'),
    ('*', '*', 'HTTPRequest', '*', '*', '*'),
    ('*', '*', 'CatMNCalcThreePlAsf', '*', '*', '*'),
    ('*', '*', 'MonitorApi', '*', '*', '*'),
    ('*', '*', 'ThirdParty_*', '*', '*', '*'),
    ('*', '*', 'ContainerRequest', '*', '*', '*'),
    ('*', '*', 'ExternalCall', '*', '*', '*'),
    ('*', '*', 'SyncStatus', '*', '*', '*'),
    ('*', '*', 'DgCheck', '*', '*', '*'),
    ('*', '*', 'Auth', '*', '*', '*'),
    ('*', '*', 'MMAP\\.LOADS', '*', '*', '*'),
    ('*', '*', 'LaneGrey', '*', '*', '*'),
    ('*', '*', 'RPC\\.Client', '*', '*', '*'),
    ('*', '*', 'LcosServiceableCompare', '*', '*', '*'),
    ('*', '*', 'Route\\.ID', '*', '*', '*'),
    ('*', '*', 'Lcos\\.ActualPoint', '*', '*', '*'),

    ('*', 'SPX', '*', '*', '*', '*'),
    # ('*', 'OMS', '*', '*', '*', '*'),
    ('*', 'FleetOrder', '*', '*', '*', '*'),
    ('*', 'LLS', 'GetUniqueResourceStatusTrackingFail', '*', '*', '*'),
    ('*', 'LPS', 'SmartRouting', '*', '*', '*'),

    ('*', 'LogisticsAPI', '*', '*', '*', '*'),
    ('*', '*', 'LogisticsAPI', '*', '*', '*'),
    ('*', 'LPS\\-LiveTest', '*', '*', '*', '*'),
    ('*', '*', 'LPS\\-LiveTest', '*', '*', '*'),
    ('*', 'LiveTestAPI', '*', '*', '*', '*'),
    ('*', '*', 'LiveTestAPI', '*', '*', '*'),
    ('*', '*', 'LogisticsServiceableReq\\.Validate', '*', '*', '*'),
    ('*', '*', 'API\\.%2Frun%2Fspex%2Fgateway_http\\.sock', '*', '*', '*'),
    ('*', '*', '*', 'DiffResult*', '*', '*'),
]

CALLCHAIN_HIDE_INFRA_DELETE_RULES = [
    # (event_id, callee, caller, api, *, *)
    ('*', '*', 'Kafka', '*', '*', '*'),
    ('*', '*', 'MySQL', '*', '*', '*'),
    ('*', '*', 'Redis', '*', '*', '*'),
    ('*', '*', 'RabbitMQ', '*', '*', '*'),
    ('*', '*', 'LruCache', '*', '*', '*'),
]

CALLCHAIN_LINK_RULES = {
    # (event_id, caller, callee, api, *, *, cat_domain, cat_type, cat_name, new_caller, new_callee, new_api)
    1: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'OrderCreateJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderCreate/OrderCreateJob',
        'Saturn', 'OrderCreateJob', 'OrderCreateJob'),
    2: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'TrackingUpdateJob', '*', "*",
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingUpdate/TrackingUpdateJob',
        'Saturn', 'TrackingUpdateJob', 'TrackingUpdateJob'),
    3: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'WeightChangeTriggerCalcAsfJob', '*', "*",
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/WeightChangeTriggerCalcAsfJob',
        'Saturn', 'WeightChangeTriggerCalcAsfJob', 'WeightChangeTriggerCalcAsfJob'),
    4: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'AdminTrackingUpdateJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingUpdate/AdminTrackingUpdateJob',
        'Saturn', 'AdminTrackingUpdateJob', 'AdminTrackingUpdateJob'),
    5: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'PushOmsTrackingWithoutStatusJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
        'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    6: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'OrderCancelJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderUpdate/OrderCancelJob',
        'Saturn', 'OrderCancelJob', 'OrderCancelJob'),
    7: ('*', '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*)', 'Task\\.Send', 'PushOmsTrackingJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingJob',
        'Saturn', 'PushOmsTrackingJob', 'PushOmsTrackingJob'),

    10: ('*', 'OrderCreateJob', 'Task\\.Send', 'OrderCreatedTrackingUpdateJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingUpdate/OrderCreatedTrackingUpdateJob',
         'Saturn', 'OrderCreatedTrackingUpdateJob', 'OrderCreatedTrackingUpdateJob'),
    11: ('*', 'OrderCreateJob', 'Task\\.Send', 'UpdateLogisticInfoToOmsJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderTnNotify/UpdateLogisticInfoToOmsJob',
         'Saturn', 'UpdateLogisticInfoToOmsJob', 'UpdateLogisticInfoToOmsJob'),
    12: ('*', 'OrderCreatedTrackingUpdateJob', 'Task\\.Send', 'PushOmsTrackingWithoutStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
         'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    13: ('*', 'OrderCreatedTrackingUpdateJob', 'Task\\.Send', 'StatusChangeTriggerCalcAsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/StatusChangeTriggerCalcAsfJob',
         'Saturn', 'StatusChangeTriggerCalcAsfJob', 'StatusChangeTriggerCalcAsfJob'),
    14: ('*', 'OrderCreateJob', 'Task\\.Send', 'Calc3plEsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderCreate/Calc3plEsfJob',
         'Saturn', 'Calc3plEsfJob', 'Calc3plEsfJob'),
    15: ('*', 'OrderCreateJob', 'Task\\.Send', 'WeightChangeTriggerCalcAsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/WeightChangeTriggerCalcAsfJob',
         'Saturn', 'WeightChangeTriggerCalcAsfJob', 'WeightChangeTriggerCalcAsfJob'),
    16: ('*', 'OrderCreateJob', 'Task\\.Send', 'ExceptionOrderCreateJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ExceptionOrder/ExceptionOrderCreateJob',
         'Saturn', 'ExceptionOrderCreateJob', 'ExceptionOrderCreateJob'),
    17: ('*', 'WeightChangeTriggerCalcAsfJob', 'Task\\.Send', 'PushAsfToOmsJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'FlexibleNotify/PushAsfToOmsJob',
         'Saturn', 'PushAsfToOmsJob', 'PushAsfToOmsJob'),
    18: ('*', 'WeightChangeTriggerCalcAsfJob', 'Task\\.Send', 'AsfUnreasonableChangeJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/AsfUnreasonableChangeJob',
         'Saturn', 'AsfUnreasonableChangeJob', 'AsfUnreasonableChangeJob'),
    19: ('*', 'OrderCreateJob', 'Task\\.Send', 'DeleteExceptionOrderJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ExceptionOrder/DeleteExceptionOrderJob',
         'Saturn', 'DeleteExceptionOrderJob', 'DeleteExceptionOrderJob'),
    20: ('*', 'OrderCreatedTrackingUpdateJob', 'Task\\.Send', 'PushOmsOrderStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderStatusNotify/PushOmsOrderStatusJob',
         'Saturn', 'PushOmsOrderStatusJob', 'PushOmsOrderStatusJob'),
    21: ('*', 'AdminTrackingUpdateJob', 'Task\\.Send', 'PushOmsTrackingWithoutStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
         'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    22: ('*', 'TrackingUpdateJob', 'Task\\.Send', 'UpdateTwsInboundTime', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/UpdateTwsInboundTime',
         'Saturn', 'UpdateTwsInboundTime', 'UpdateTwsInboundTime'),
    23: ('*', 'TrackingUpdateJob', 'Task\\.Send', 'PushOmsOrderStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderStatusNotify/PushOmsOrderStatusJob',
         'Saturn', 'PushOmsOrderStatusJob', 'PushOmsOrderStatusJob'),
    24: ('*', 'TrackingUpdateJob', 'Task\\.Send', 'StatusChangeTriggerCalcAsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/StatusChangeTriggerCalcAsfJob',
         'Saturn', 'StatusChangeTriggerCalcAsfJob', 'StatusChangeTriggerCalcAsfJob'),
    25: ('*', 'TrackingUpdateJob', 'Task\\.Send', 'PushOmsTrackingWithoutStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
         'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    26: ('*', 'TrackingUpdateJob', 'Task\\.Send', 'SipLogisticStatusNotifyJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/SipLogisticStatusNotifyJob',
         'Saturn', 'SipLogisticStatusNotifyJob', 'SipLogisticStatusNotifyJob'),
    27: ('*', 'PushOmsTrackingJob', 'Task\\.Send', 'SipLogisticStatusNotifyJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfPoll/CheckDoneBatchJob',
         'Saturn', 'CheckDoneBatchJob', 'CheckDoneBatchJob'),
    28: ('*', 'PushOmsTrackingJob', 'Task\\.Send', 'MassUpdateApprovalTaskJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'FlexibleUpdate/MassUpdateApprovalTaskJob',
         'Saturn', 'MassUpdateApprovalTaskJob', 'MassUpdateApprovalTaskJob'),
    29: ('*', 'PushOmsTrackingJob', 'Task\\.Send', 'MassUpdateProcessJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfPoll/MassUpdateProcessJob',
         'Saturn', 'MassUpdateProcessJob', 'MassUpdateProcessJob'),
    30: ('*', 'PushOmsTrackingJob', 'Task\\.Invoke', 'CheckBatchStatusCronJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'CheckBatchStatusCronJob',
         'Saturn', 'CheckBatchStatusCronJob', 'CheckBatchStatusCronJob'),
    31: ('*', 'PushOmsTrackingJob', 'Task\\.Invoke', 'ScheduleReportOrderStatusPrometheusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ScheduleReportOrderStatusPrometheusJob',
         'Saturn', 'ScheduleReportOrderStatusPrometheusJob', 'ScheduleReportOrderStatusPrometheusJob'),
    32: ('*', 'PushOmsTrackingJob', 'Task\\.Invoke', 'ScheduleReportOrderStatusPrometheusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ScheduleReportOrderStatusPrometheusJob',
         'Saturn', 'ScheduleReportOrderStatusPrometheusJob', 'ScheduleReportOrderStatusPrometheusJob'),

    51: ('*', '(API\\.lcs\\-api\\.shopee\\.co\\.*|API\\.lcs\\-api\\.shopee\\.*|CHANNEL_API\\.LCS|LcsLineWayBill)', 'Task\\.send', 'celery_task\\.celery_notify_status\\.push_weight_fee_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_weight_fee_retry',
         'Celery', 'push_weight_fee_retry_task', 'celery_task.celery_notify_status.push_weight_fee_retry'),
    52: ('*', '(API\\.lcs\\-api\\.shopee\\.co\\.*|API\\.lcs\\-api\\.shopee\\.*|CHANNEL_API\\.LCS|LcsLineWayBill)', 'Task\\.send', 'celery_task\\.celery_update_status\\.update_logistic_tracking_data', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_update_status.update_logistic_tracking_data',
         'Celery', 'update_logistic_tracking_data_task', 'celery_task.celery_update_status.update_logistic_tracking_data'),
    53: ('*', '(API\\.lcs\\-api\\.shopee\\.co\\.*|API\\.lcs\\-api\\.shopee\\.*|CHANNEL_API\\.LCS|LcsLineWayBill)', 'Task\\.send', 'celery_task\\.celery_tidb_update_status\\.update_logistic_tracking_data_using_tidb', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb',
         'Celery', 'update_logistic_tracking_data_using_tidb_task', 'celery_task\\.celery_tidb_update_status\\.update_logistic_tracking_data_using_tidb'),
    61: ('*', 'update_logistic_tracking_data_task', 'Task\\.send', 'celery_task.celery_notify_status.push_tracking_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_tracking_retry',
         'Celery', 'push_tracking_retry_task', 'celery_task.celery_notify_status.push_tracking_retry'),
    62: ('*', 'update_logistic_tracking_data_using_tidb_task', 'Task\\.send', 'celery_task\\.celery_notify_status\\.push_weight_fee_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_weight_fee_retry',
         'Celery', 'push_weight_fee_retry_task', 'celery_task.celery_notify_status.push_weight_fee_retry'),
    63: ("*", "update_logistic_tracking_data_using_tidb_task", "Task\\.send", "celery_task\\.celery_notify_status\\.push_tracking_retry", '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_tracking_retry',
         'Celery', 'push_tracking_retry_task', 'celery_task.celery_notify_status.push_tracking_retry'),
    64: ('*', 'update_logistic_tracking_data_task', 'Task\\.send', 'celery_task\\.celery_notify_status\\.push_weight_fee_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_weight_fee_retry',
         'Celery', 'push_weight_fee_retry_task', 'celery_task.celery_notify_status.push_weight_fee_retry'),

    101: ('*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)', 'Kafka', 'ProduceTrackingPushMessage', '*', '*',
          'pis-partnerintegrationtask-live-{0}', 'Task', 'ConsumeTrackingPushMessage',
          'PIS-Saturn', 'ConsumeTrackingPushMessage', 'ConsumeTrackingPushMessage'),
}

API_CALL_MAP = {
}
