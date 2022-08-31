#!./bin/python

# Execution Order: NODE_OVERWRITE -> EDGE_OVERWRITE -> RENAME -> COMBINE -> DELETE
# Only `general` overwrite rules can be defined here.
CALLCHAIN_NODE_OVERWRITE_RULES = {
    '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*|API\\.sls\\-partnerintegrationservice-*)': 'PIS',
    '(API\\.api\\.sls\\.shopee\\.com\\.*|API\\.api\\.sls\\.shopee\\.*)': 'SLS-Logistics',
    '(API\\.lcs\\-electronicproofgrpc\\-*)': 'EP-Service',
    '(API\\.tracking\\-grpc\\-*)': 'LTS',
    '(API\\.admin\\.shopee\\.*)': 'Admin-API',
    '(API\\.routing\\.geo\\.shopee\\.*)': 'GEO',
    '(API\\.ops\\.ssc\\.shopeemobile\\.com)': 'OPS',
    '(API\\.logistics\\-api\\.shopee\\.co\\.*|API\\.logistics\\-api\\.shopee\\.com\\.*|API\\.logistics\\-api\\.shopee\\.*)': 'LogisticsAPI',
    '(API.sls\\-rateapi\\-live\\-*|API\\.sls\\-rateapi\\-live\\-*|API\\.rate\\-checkout\\.ssc\\.shopee\\.co\\.*|API\\.rate\\.ssc\\.shopee\\.co\\.*)': 'RateAPI',
    '(API\\.sls\\-rateapioffline\\-live\\-*)': 'RateAPI-Offline',
    '(API\\.oms\\.shopee\\.co\\.id|API\\.oms\\-parcelapi\\-live\\-id|API\\.oms\\-logisticscommonset\\-live\\-*|API\\.oms\\-parcelcommonset\\-live\\-*)': 'OMS',
    '(API\\.sls\\-locationgrpc\\-live\\-*|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.co\\.*|SlsLocation|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.*|API\\.sls\\-locationgrpc\\.ssc\\.shopee\\.*)': 'SLS-Location',
    '(API\\.c\\-api\\-sellerbasicservice\\.shopeemobile\\.com)': 'SellerBasicService',
    '(URL\\.lfs\\-(api|grpc)\\-live\\-*|API\\.lfs\\-grpc\\-live\\-*|API\\.api\\.lfs\\.shopee\\.co\\.*|API\\.lfs\\-checkoutgrpc\\-*|API\\.api\\.lfs\\.shopee\\.*|API\\.lfs\\-grpc\\.ssc\\.shopee\\.co\\.*)': 'LFS',
    '(API\\.fleet\\-order\\.ssc\\.shopee\\.co\\.*|fleet_order_read_facade\\.Gray|Fleet_Order_Client)': 'FleetOrder',
    '(API\\.api\\.lps\\.shopee\\.co\\.*|URL\\.lps\\-api\\-live\\-*|API\\.lps\\-grpc\\-live\\-*|API\\.api\\.lps\\.shopee\\.*)': 'LPS',
    '(API\\.api\\-lps\\-livetest\\.ssc\\.shopee\\.com\\.*)': 'LPS-LiveTest',
    'API\\.livetest\\.ssc\\.shopee\\.co\\.*': 'LiveTestAPI',
    '(URL\\.lls\\-grpc\\-*|API\\.lls\\-grpc.ssc\\.shopee\\.co\\.*|LLSGrpc\\-*|API\\.lls\\-grpc\\-*|API\\.lls\\-fulfillment\\-*|API\\.lls\\-query\\-*|LLS\\-FULFILLMENT\\-LIVE\\-*)': 'LLS',
    '(API\\.lcos\\-grpc\\-*|URL\\.lcos\\-checkout\\-*|API\\.lcos\\-checkout\\-*|URL\\.lcos\\-grpc\\-*|API\\.lcos\\-grpc\\.shopee\\.co\\.*|LcosSdk)': 'LCOS',
    '(API\\.lcs\\-api\\.shopee\\.co\\.*|API\\.lcs\\-api\\.shopee\\.*|CHANNEL_API\\.LCS|LcsLineWayBill)': 'LCS',
    '(URL\\.wbc\\-static\\-*|WaybillCenterGRPC\\-*|API\\.wbc\\-static\\-*|API\\.wbc\\-eventbusproxy\\-*|API\\.waybillcenter\\.ssc\\.shopee\\.co\\.*)': 'WBC',
    '(API\\.spx\\.shopee\\.co\\.*|API\\.sp\\.spx\\.shopee\\.co\\.id|API\\.spx\\-container\\-service\\.ssc\\.shopee\\.co\\.*|SpRemoteApi|API\\.spx\\-smartsorting\\.ssc\\.shopee\\.co\\.*)': 'SPX',
    'API\\.smartrouting\\-grpc\\-live\\-*': 'SmartRouting',
    '(API\\.tws\\.shopeemobile\\.com|API\\.tws\\.shopeesz\\.com)': 'TWS',
    '(API\\.external2\\.shopee\\.co\\.*|API\\.shopeeapi\\-pre\\.idexpress\\.com|API\\.pickup\\.sicepat\\.com|API\\.secure\\-jk\\.jet\\.co\\.*|API\\.partner\\-api\\.grab\\.com|API\\.anteraja\\-prod\\.apigee\\.net|API\\.shopee\\.jtcargo\\.co\\.*|API\\.api\\.sentralcargo\\.co\\.*|API\\.food\\-open\\.shopee\\.co\\.*|API\\.api\\.ninjavan\\.co|API\\.ecc2c\\.presco\\.com\\.*|API\\.ecservice\\.hilife\\.com\\.*|API\\.external2\\.shopee\\.*|API\\.eservice\\.presco\\.com\\.*|API\\.schemas\\.xmlsoap\\.org)': '3PL',
    '(API\\.charge\\.ssc\\.shopeemobile\\.com)': 'Charge-API',
    'API\\.idcs\\-server\\-live\\-*': 'IDCS',
    'RabbitMQ\\.rabbitmq\\.i\\.ssc\\-2\\.ctl\\.sz\\.shopee\\.io': 'RabbitMQ',
    '(LocalCacheReport|LocalCache|LayerCache|LayeredCache|Cache|Redis\\.proxy\\.cache\\-codis[0-9]\\-ctl\\.i\\.sz\\.shopee\\.io|Redis:proxy\\.cache\\-codis[0-9]\\-ctl.i.sz.shopee.io:*|RateLimit)': 'Redis',
    '^(MySQL:*|CdtDbQueryTimes|CdtGetInfo)$': 'MySQL',
    '^(PN\\-Kafka|WBC\\-Kafka)$': 'Kafka',
    '^Es$': 'ElasticSearch',
    '(Task\\.Send|Task\\.Invoke)': 'Saturn',
    'Task\\.send': 'Celery',
}

# Only `general` overwrite rules can be defined here.
CALLCHAIN_EDGE_OVERWRITE_RULES = {
}

# High priority rules should be put in the front.
# Scenario specific renaming rules should be defined in scenario specific places because it has many possible mappings.
CALLCHAIN_RENAME_RULES = [
    # (event_id, callee, caller, api, reserved, reserved, index:rename_to)
    ("*", "PIS", "Kafka", "ProduceTrackingPushMessage", '*', '*', '2:Saturn'),
    ('*', '(OrderCreateJob|UpdateLogisticInfoToOmsJob)', 'Task\\.Retry', '(OrderCreate/OrderCreateJob|OrderTnNotify/UpdateLogisticInfoToOmsJob)', '*', '*', '2:Saturn'),
]

CALLCHAIN_COMBINE_RULES = ['Redis', 'Kafka', 'MySQL']

CALLCHAIN_DELETE_RULES = [
    # (event_id, callee, caller, api, *, *)
    ('*', 'SPX', '*', '*', '*', '*'),
    ('*', 'FleetOrder', '*', '*', '*', '*'),
    ('*', 'LogisticsAPI', '*', '*', '*', '*'),
    ('*', 'LPS\\-LiveTest', '*', '*', '*', '*'),
    ('*', 'LiveTestAPI', '*', '*', '*', '*'),
    ('*', 'API\\.smart\\-sorting\\-live\\-*', '*', '*', '*', '*'),

    ('*', '*', 'FleetOrder', '*', '*', '*'),
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
    ('*', '*', 'LogisticsAPI', '*', '*', '*'),
    ('*', '*', 'LPS\\-LiveTest', '*', '*', '*'),
    ('*', '*', 'LiveTestAPI', '*', '*', '*'),

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
    1: ('*', 'LFS', 'Saturn', 'OrderCreateJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderCreate/OrderCreateJob',
        'Saturn', 'OrderCreateJob', 'OrderCreateJob'),
    2: ('*', 'LFS', 'Saturn', 'TrackingUpdateJob', '*', "*",
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingUpdate/TrackingUpdateJob',
        'Saturn', 'TrackingUpdateJob', 'TrackingUpdateJob'),
    3: ('*', 'LFS', 'Saturn', 'WeightChangeTriggerCalcAsfJob', '*', "*",
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/WeightChangeTriggerCalcAsfJob',
        'Saturn', 'WeightChangeTriggerCalcAsfJob', 'WeightChangeTriggerCalcAsfJob'),
    4: ('*', 'LFS', 'Saturn', 'AdminTrackingUpdateJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingUpdate/AdminTrackingUpdateJob',
        'Saturn', 'AdminTrackingUpdateJob', 'AdminTrackingUpdateJob'),
    5: ('*', 'LFS', 'Saturn', 'PushOmsTrackingWithoutStatusJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
        'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    6: ('*', 'LFS', 'Saturn', 'OrderCancelJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderUpdate/OrderCancelJob',
        'Saturn', 'OrderCancelJob', 'OrderCancelJob'),
    7: ('*', 'LFS', 'Saturn', 'PushOmsTrackingJob', '*', '*',
        'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingJob',
        'Saturn', 'PushOmsTrackingJob', 'PushOmsTrackingJob'),

    10: ('*', 'OrderCreateJob', 'Saturn', 'OrderCreatedTrackingUpdateJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingUpdate/OrderCreatedTrackingUpdateJob',
         'Saturn', 'OrderCreatedTrackingUpdateJob', 'OrderCreatedTrackingUpdateJob'),
    11: ('*', 'OrderCreateJob', 'Saturn', 'UpdateLogisticInfoToOmsJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderTnNotify/UpdateLogisticInfoToOmsJob',
         'Saturn', 'UpdateLogisticInfoToOmsJob', 'UpdateLogisticInfoToOmsJob'),
    12: ('*', 'OrderCreatedTrackingUpdateJob', 'Saturn', 'PushOmsTrackingWithoutStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
         'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    13: ('*', 'OrderCreatedTrackingUpdateJob', 'Saturn', 'StatusChangeTriggerCalcAsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/StatusChangeTriggerCalcAsfJob',
         'Saturn', 'StatusChangeTriggerCalcAsfJob', 'StatusChangeTriggerCalcAsfJob'),
    14: ('*', 'OrderCreateJob', 'Saturn', 'Calc3plEsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderCreate/Calc3plEsfJob',
         'Saturn', 'Calc3plEsfJob', 'Calc3plEsfJob'),
    15: ('*', 'OrderCreateJob', 'Saturn', 'WeightChangeTriggerCalcAsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/WeightChangeTriggerCalcAsfJob',
         'Saturn', 'WeightChangeTriggerCalcAsfJob', 'WeightChangeTriggerCalcAsfJob'),
    16: ('*', 'OrderCreateJob', 'Saturn', 'ExceptionOrderCreateJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ExceptionOrder/ExceptionOrderCreateJob',
         'Saturn', 'ExceptionOrderCreateJob', 'ExceptionOrderCreateJob'),
    17: ('*', 'WeightChangeTriggerCalcAsfJob', 'Saturn', 'PushAsfToOmsJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'FlexibleNotify/PushAsfToOmsJob',
         'Saturn', 'PushAsfToOmsJob', 'PushAsfToOmsJob'),
    18: ('*', 'WeightChangeTriggerCalcAsfJob', 'Saturn', 'AsfUnreasonableChangeJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/AsfUnreasonableChangeJob',
         'Saturn', 'AsfUnreasonableChangeJob', 'AsfUnreasonableChangeJob'),
    19: ('*', 'OrderCreateJob', 'Saturn', 'DeleteExceptionOrderJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ExceptionOrder/DeleteExceptionOrderJob',
         'Saturn', 'DeleteExceptionOrderJob', 'DeleteExceptionOrderJob'),
    20: ('*', 'OrderCreatedTrackingUpdateJob', 'Saturn', 'PushOmsOrderStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderStatusNotify/PushOmsOrderStatusJob',
         'Saturn', 'PushOmsOrderStatusJob', 'PushOmsOrderStatusJob'),
    21: ('*', 'AdminTrackingUpdateJob', 'Saturn', 'PushOmsTrackingWithoutStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
         'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    22: ('*', 'TrackingUpdateJob', 'Saturn', 'UpdateTwsInboundTime', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/UpdateTwsInboundTime',
         'Saturn', 'UpdateTwsInboundTime', 'UpdateTwsInboundTime'),
    23: ('*', 'TrackingUpdateJob', 'Saturn', 'PushOmsOrderStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'OrderStatusNotify/PushOmsOrderStatusJob',
         'Saturn', 'PushOmsOrderStatusJob', 'PushOmsOrderStatusJob'),
    24: ('*', 'TrackingUpdateJob', 'Saturn', 'StatusChangeTriggerCalcAsfJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfUpdate/StatusChangeTriggerCalcAsfJob',
         'Saturn', 'StatusChangeTriggerCalcAsfJob', 'StatusChangeTriggerCalcAsfJob'),
    25: ('*', 'TrackingUpdateJob', 'Saturn', 'PushOmsTrackingWithoutStatusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/PushOmsTrackingWithoutStatusJob',
         'Saturn', 'PushOmsTrackingWithoutStatusJob', 'PushOmsTrackingWithoutStatusJob'),
    26: ('*', 'TrackingUpdateJob', 'Saturn', 'SipLogisticStatusNotifyJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'TrackingNotify/SipLogisticStatusNotifyJob',
         'Saturn', 'SipLogisticStatusNotifyJob', 'SipLogisticStatusNotifyJob'),
    27: ('*', 'PushOmsTrackingJob', 'Saturn', 'SipLogisticStatusNotifyJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfPoll/CheckDoneBatchJob',
         'Saturn', 'CheckDoneBatchJob', 'CheckDoneBatchJob'),
    28: ('*', 'PushOmsTrackingJob', 'Saturn', 'MassUpdateApprovalTaskJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'FlexibleUpdate/MassUpdateApprovalTaskJob',
         'Saturn', 'MassUpdateApprovalTaskJob', 'MassUpdateApprovalTaskJob'),
    29: ('*', 'PushOmsTrackingJob', 'Saturn', 'MassUpdateProcessJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'AsfPoll/MassUpdateProcessJob',
         'Saturn', 'MassUpdateProcessJob', 'MassUpdateProcessJob'),
    30: ('*', 'PushOmsTrackingJob', 'Saturn', 'CheckBatchStatusCronJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'CheckBatchStatusCronJob',
         'Saturn', 'CheckBatchStatusCronJob', 'CheckBatchStatusCronJob'),
    31: ('*', 'PushOmsTrackingJob', 'Saturn', 'ScheduleReportOrderStatusPrometheusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ScheduleReportOrderStatusPrometheusJob',
         'Saturn', 'ScheduleReportOrderStatusPrometheusJob', 'ScheduleReportOrderStatusPrometheusJob'),
    32: ('*', 'PushOmsTrackingJob', 'Saturn', 'ScheduleReportOrderStatusPrometheusJob', '*', '*',
         'LFS-TASK-LIVE-{0}', 'Task.Invoke', 'ScheduleReportOrderStatusPrometheusJob',
         'Saturn', 'ScheduleReportOrderStatusPrometheusJob', 'ScheduleReportOrderStatusPrometheusJob'),

    51: ('*', 'LCS', 'Celery', 'celery_task\\.celery_notify_status\\.push_weight_fee_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_weight_fee_retry',
         'Celery', 'push_weight_fee_retry_task', 'celery_task.celery_notify_status.push_weight_fee_retry'),
    52: ('*', 'LCS', 'Celery', 'celery_task\\.celery_update_status\\.update_logistic_tracking_data', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_update_status.update_logistic_tracking_data',
         'Celery', 'update_logistic_tracking_data_task', 'celery_task.celery_update_status.update_logistic_tracking_data'),
    53: ('*', 'LCS', 'Celery', 'celery_task\\.celery_tidb_update_status\\.update_logistic_tracking_data_using_tidb', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb',
         'Celery', 'update_logistic_tracking_data_using_tidb_task', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb'),
    61: ('*', 'update_logistic_tracking_data_task', 'Celery', 'celery_task.celery_notify_status.push_tracking_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_tracking_retry',
         'Celery', 'push_tracking_retry_task', 'celery_task.celery_notify_status.push_tracking_retry'),
    62: ('*', 'update_logistic_tracking_data_using_tidb_task', 'Celery', 'celery_task\\.celery_notify_status\\.push_weight_fee_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_weight_fee_retry',
         'Celery', 'push_weight_fee_retry_task', 'celery_task.celery_notify_status.push_weight_fee_retry'),
    63: ("*", "update_logistic_tracking_data_using_tidb_task", "Celery", "celery_task\\.celery_notify_status\\.push_tracking_retry", '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_tracking_retry',
         'Celery', 'push_tracking_retry_task', 'celery_task.celery_notify_status.push_tracking_retry'),
    64: ('*', 'update_logistic_tracking_data_task', 'Celery', 'celery_task\\.celery_notify_status\\.push_weight_fee_retry', '*', '*',
         'LCS-CELERY-{0}', 'Task.invoke', 'celery_task.celery_notify_status.push_weight_fee_retry',
         'Celery', 'push_weight_fee_retry_task', 'celery_task.celery_notify_status.push_weight_fee_retry'),

    101: ('*', 'PIS', 'Saturn', 'ProduceTrackingPushMessage', '*', '*',
          'pis-partnerintegrationtask-live-{0}', 'Task', 'ConsumeTrackingPushMessageJob',
          'Saturn', 'ConsumeTrackingPushMessageJob', 'ConsumeTrackingPushMessageJob'),
}

CALLSTACK_END_RULES = [
    'Saturn', 'Celery',
]

SLS_SERVICE_GROUPS = {
    'External Caller': ['Caller'],
    'Fulfillment Gateway': ['LPS'],
    'Core Fulfillment Capability': ['LFS', 'LLS', 'SmartRouting'],
    'Tracking': ['LTS', 'TrackingPN'],
    'Fundamental Capability': ['LCOS', 'WBC', 'IDCS', 'SLS\\-Location', 'EP\\-Service'],
    '3PL Gateway': ['LCS', 'PIS'],
    'Finance': ['RateAPI', 'RateAPI\\-Offline'],
    'Async Jobs': ['.*Job', '.*_task'],
    'External Dependencies': ['Saturn', 'Celery', '3PL', 'SPX', 'OMS'],
}

SERVICE_LEVEL_COMPLIANCE_RULES = {
    'LPS': ['LFS', 'SmartRouting', 'LCOS', 'RateAPI', 'Saturn'],
    'LFS': ['LLS', 'TrackingPN', 'LCOS', 'IDCS', 'RateAPI', 'SLS\\-Location', 'EP\\-Service', 'Saturn'],
    'LLS': ['TrackingPN', 'LCOS', 'IDCS', 'SLS\\-Location', 'LCS', 'PIS', 'Saturn'],
    'SmartRouting': ['LCOS', 'SLS\\-Location', 'Saturn'],
    'LTS': ['Saturn'],
    'TrackingPN': ['Saturn'],
    'LCOS': [],
    'WBC': ['RateAPI\\-Offline', 'Saturn'],
    'IDCS': [],
    'SLS\\-Location': [],
    'EP\\-Service': [],
    'LCS': ['3PL', 'SPX', 'Celery'],
    'PIS': ['3PL', 'SPX', 'Saturn'],
    'RateAPI': ['LCOS', 'Saturn'],
    'RateAPI\\-Offline': ['LCOS'],
    '3PL': ['LCS', 'PIS'],
    'SPX': ['LCS', 'PIS'],
    'OMS': ['LPS'],
    '.*Job': ['RateAPI\\-Offline', 'Saturn'],
    '.*_task': ['RateAPI\\-Offline', 'Saturn'],
}

SERVICE_LEVEL_VIOLATION_RULES = {
}

DOMAIN_LEVEL_COMPLIANCE_RULES = {
}

DOMAIN_LEVEL_VIOLATION_RULES = {
    ('LFS:Fulfillment', 'RateAPI:FeeCalculation'),
}

API_LEVEL_COMPLIANCE_RULES = {
}

API_LEVEL_VIOLATION_RULES = {
    ('LFS:Fulfillment:/api/sls/order/create', 'RateAPI:FeeCalculation:/api/sls-basic/freight/calc_esf_weight/'),
}

TAG_LEVEL_COMPLIANCE_RULES = {
}

TAG_LEVEL_VIOLATION_RULES = {
    ('order_creation', 'product_rule'),
}