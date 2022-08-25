#!./bin/python

CUSTOM_SCENARIOS = {
    'create_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/order/create', 1, 1),
        ],
        'extra_callchain': [
        ],
        'extra_rename_rules': [
            ('*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*|API\\.sls\\-partnerintegrationservice-*)', '*', '*', '*', '*', '1:PIS'),
            ('*', '*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*|API\\.sls\\-partnerintegrationservice-*)', '*', '*', '*', '2:PIS'),
            ('*', 'PIS', '*', 'https://waybillcenter\\.ssc\\.shopee\\.co\\.*', '*', '*', '2:WBC'),
            ('*', 'PIS', '*', 'https://spx\\.shopee\\.co\\.*', '*', '*', '2:SPX'),
        ],
        'extra_delete_rules': [
            ('*', 'SmartRouting', 'SelectLane', '*', '*', '*'),
            ('*', '*', 'TrackingOperate|TrackingAssemble', '*', '*', '*'),
            ('*', '*', 'GetTrackingFromLTS|ActualShippingFee', '*', '*', '*'),
            ('*', '*', 'ResourceAPI', '*', '*', '*'),
            ('*', 'OMS', '*', '*', '*', '*'),
        ],
        'filter_stack': ['/api/sls-basic/freight/calc_esf_weight/', 'calculateWeightBySdk'],
        'puml_head': """
@startuml

box "SLS"
participant LPS
participant LFS
participant LLS
participant LCOS
participant PIS
participant RateAPI
participant LCS
participant IDCS
participant WBC
participant TrackingPN
end box

box "SLS Async"
participant OrderCreateJob
participant UpdateLogisticInfoToOmsJob
participant PushOmsTrackingWithoutStatusJob
participant OrderCreatedTrackingUpdateJob
participant StatusChangeTriggerCalcAsfJob
participant Calc3plEsfJob
end box

box "External"
participant Saturn
participant SPX
participant OMS
end box
""",
        'puml_tail': """
@enduml
""",
        'name': 'create_order',
        'region': 'ID',
        'reload': False,
        'enabled': True,
    },
    'StatusChangeTriggerCalcAsfJob': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'Task.Send', 'StatusChangeTriggerCalcAsfJob', 20, 20),
        ],
        'extra_rename_rules': [
            ('*', 'Task\\.invoke', '*', '*', '*', '*', '1:Task.Invoke'),
        ],
        'extra_combine_rules': [],
        'extra_delete_rules': [
            ('*', '*', 'FleetOrder', '*', '*', '*'),
            ('*', '*', 'InvokeGrpcWithHttp', '*', '*', '*'),
        ],
        'filter_stack': ['StatusChangeTriggerCalcAsfJob'],
        'name': 'StatusChangeTriggerCalcAsfJob',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'WeightChangeTriggerCalcAsfJob': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'Task.Send', 'WeightChangeTriggerCalcAsfJob', 20, 20),
        ],
        'extra_rename_rules': [
        ],
        'extra_combine_rules': [],
        'extra_delete_rules': [
            ('*', '*', 'FleetOrder', '*', '*', '*'),
        ],
        'filter_stack': ['WeightChangeTriggerCalcAsfJob'],
        'name': 'WeightChangeTriggerCalcAsfJob',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'lps_processing_routing_log': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LPS-TASK-ID-LIVE', 'SaturnMsgJob', 'lps.shopee.id.process_routing_log', 20, 20),
        ],
        'extra_rename_rules': [
        ],
        'extra_combine_rules': [],
        'extra_delete_rules': [

        ],
        'name': 'lps_processing_routing_log',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'can_update_order_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/sls/check_order_can_update', 20, 20),
        ],
        'extra_rename_rules': [
        ],
        'extra_combine_rules': [],
        'extra_delete_rules': [
            ('*', 'OMS', '*', '*', '*', '*'),
        ],
        'name': 'lfs_can_update_order',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },
    'update_order_tw': {
       'entrypoints': [
           # (cat_domain, cat_type, cat_name, sample_count, link_count)
           ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/sls/order/update', 20, 20),
       ],
       'extra_rename_rules': [
       ],
       'extra_combine_rules': ['3PL'],
       'extra_delete_rules': [
           ('*', 'OMS', '*', '*', '*', '*'),
           ('*', '*', 'SOAP\\.TWL_OKMART_FM_LM_C2C', '*', '*', '*'),
       ],
       'name': 'lfs_update_order',
       'region': 'TW',
       'reload': False,
       'enabled': False,
    },
}

PRE_FULFILLMENT_BUSINESS_SCENARIOS = {
    'pre_fulfillment_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/channels/get/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/shop/channels/batch/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/buyer/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/shop/info/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/pdp/integration/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/checkout/integration/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/channels/batch_validate_checkout_items_shipped/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/address/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/lps/logistic/shipping_channels/service_types/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/holidays/get/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/address/batch_can_cod_pickup/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/payment/batch_cod_check/', 10, 10),
            ('lps-api-live-id', 'URL.lps-api-live-id', '/api/logistics/item/batch_check_item_ship_to_new/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '^URL$', '*', '*', '*', '*', '1:SLS-API'),
            ('*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)', 'HttpRequest', '*', '*', '*', '2:3PL'),
        ],
        'extra_delete_rules': [
            ('*', 'SLS\\-API', '*', '*', '*', '*'),
        ],
        'name': 'pre_fulfillment',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'pre_fulfillment_br': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/channels/get/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/shop/channels/batch/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/buyer/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/shop/info/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/pdp/integration/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/checkout/integration/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/channels/batch_validate_checkout_items_shipped/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/address/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/lps/logistic/shipping_channels/service_types/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/holidays/get/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/address/batch_can_cod_pickup/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/payment/batch_cod_check/', 10, 10),
            ('lps-api-live-br', 'URL.lps-api-live-br', '/api/logistics/item/batch_check_item_ship_to_new/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '^URL$', '*', '*', '*', '*', '1:SLS-API'),
            ('*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)', 'HttpRequest', '*', '*', '*', '2:3PL'),
            ('*', '*', 'SLS\\-API\\.URL', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', 'SLS\\-API', '*', '*', '*', '*'),
            ('*', 'SLS\\-Logistics', '*', '*', '*', '*'),
        ],
        'name': 'pre_fulfillment',
        'region': 'BR',
        'reload': False,
        'enabled': False,
    },
    'pre_fulfillment_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/channels/get/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/shop/channels/batch/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/buyer/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/shop/info/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/pdp/integration/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/checkout/integration/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/channels/batch_validate_checkout_items_shipped/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/address/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/lps/logistic/shipping_channels/service_types/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/holidays/get/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/address/batch_can_cod_pickup/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/payment/batch_cod_check/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/logistics/item/batch_check_item_ship_to_new/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '^URL$', '*', '*', '*', '*', '1:SLS-API'),
            ('*', '(API\\.partner\\-integration\\.ssc\\.shopee\\.co\\.*|API\\.lpis\\-checkout\\.ssc\\.shopee\\.*)', 'HttpRequest', '*', '*', '*', '2:3PL'),
        ],
        'extra_delete_rules': [
            ('*', 'SLS\\-API', '*', '*', '*', '*'),
            ('*', 'SLS\\-Logistics', '*', '*', '*', '*'),
        ],
        'name': 'pre_fulfillment',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },
}

FULFILLMENT_BUSINESS_SCENARIOS = {
    # check order
    'check_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-id', 'URL.lps-api-live-id', '/api/sls/check_order/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'name': 'check_order',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'check_order_br': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-br', 'URL.lps-api-live-br', '/api/sls/check_order/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'name': 'check_order',
        'region': 'BR',
        'reload': False,
        'enabled': False,
    },
    'check_order_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/sls/check_order/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'name': 'check_order',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },

    # update order
    'update_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-id', 'URL.lps-api-live-id', '/api/sls/check_order_can_update/', 10, 10),
            ('lps-api-live-id', 'URL.lps-api-live-id', '/api/sls/update_order/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '^URL$', '*', '*', '*', '*', '1:SLS-API'),
        ],
        'extra_delete_rules': [
            ('*', '*', 'Order\\.Update', '*', '*', '*'),
        ],
        'name': 'update_order',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },

    # BR doesn't support order update.

    'update_order_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/sls/check_order_can_update/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/sls/update_order/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '^URL$', '*', '*', '*', '*', '1:SLS-API'),
        ],
        'extra_delete_rules': [
            ('*', 'SLS\\-Logistics', '*', '*', '*', '*'),
            ('*', 'OMS', '*', '*', '*', '*'),
        ],
        'name': 'update_order',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },

    # cancel order
    'cancel_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/check_order_can_cancel/', 10, 10),
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/cancel_orders/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '(TWS|OMS)', '*', '*', '*', '*'),
            ('*', '*', 'Order\\.Cancel', '*', '*', '*'),
        ],
        'name': 'cancel_order',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'cancel_order_br': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-BR', 'URL.lfs-api-live-br', '/api/sls/check_order_can_cancel/', 10, 10),
            ('LFS-API-LIVE-BR', 'URL.lfs-api-live-br', '/api/sls/cancel_orders/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '*', 'Order\\.Cancel', '*', '*', '*'),
            ('*', '*', 'API\\.openapi\\.superbpost\\.com:*', '*', '*', '*'),
            ('*', '^(OMS|TWS)$', '*', '*', '*', '*'),
            ('*', 'PushOmsTrackingJob', '(ScheduleRetryTask|ExceptionOrderManager|ActualShippingFee|RateAPI)', '*', '*', '*'),
            ('*', 'PushOmsTrackingJob', 'Task\\.Invoke', '*', '*', '*'),
            ('*', 'ScheduleReportOrderStatusPrometheusJob', 'Task\\.Invoke', '*', '*', '*'),
            ('*', '*', 'ScheduleReportOrderStatusPrometheusJob', '*', '*', '*'),
            ('*', '*', 'CreateOrder', '*', '*', '*'),
        ],
        'name': 'cancel_order',
        'region': 'BR',
        'reload': False,
        'enabled': False,
    },
    'cancel_order_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/sls/check_order_can_cancel/', 10, 10),
            ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/sls/cancel_orders/', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '*', 'https://lcs\\-api\\.shopee\\.*', '*', '*', '*', '2:LCS'),
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '(TWS|OMS)', '*', '*', '*', '*'),
            ('*', 'PushOmsTrackingJob', '(ScheduleRetryTask|ExceptionOrderManager|ActualShippingFee|RateAPI)', '*', '*', '*'),
            ('*', 'PushOmsTrackingJob', 'Task\\.Invoke', '*', '*', '*'),
            ('*', 'CheckBatchStatusCronJob', 'Task\\.Invoke', '*', '*', '*'),
            ('*', 'ScheduleReportOrderStatusPrometheusJob', 'Task\\.Invoke', '*', '*', '*'),
            ('*', '*', 'ScheduleReportOrderStatusPrometheusJob', '*', '*', '*'),
            ('*', '*', 'CreateOrder', '*', '*', '*'),
            ('*', '*', 'Order\\.Cancel', '*', '*', '*'),
            ('*', '*', 'API\\.openapi\\.superbpost\\.com', '*', '*', '*'),
        ],
        'name': 'cancel_order',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },

    # create order
    'create_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/order/create', 10, 10),
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/logistic/batch_get_label_data/', 10, 10),
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/logistic/batch_check_print_label/', 10, 10),
        ],
        'extra_callchain': [
            # (cat_evt, cat_type, cat_name, api_call, '', '')
            ['-', 'API.lcs-api.shopee.co.id', 'Task.send', 'celery_task.celery_notify_status.push_weight_fee_retry', '', ''],
            ['-', 'API.lcs-api.shopee.co.id', 'Task.send', 'celery_task.celery_update_status.update_logistic_tracking_data', '', ''],
            ['-', 'API.lcs-api.shopee.co.id', 'Task.send', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb', '', ''],
            ['-', 'OrderCreateJob', 'Task.Send', 'WeightChangeTriggerCalcAsfJob', '', '']
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '(API\\.spx\\.shopee\\.*|API\\.fleet\\-order\\.ssc\\.shopee\\.*|FacadeDict|FleetOrder|API\\.fleet\\-order\\.ssc\\.shopee\\.*)', '*', '*', '*', '*'),
            ('*', '*', 'API\\.spx\\.shopee\\.*', '*', '*', '*'),
            ('*', '*', 'ShippingLabel', '*', '*', '*'),
            ('*', '*', 'ActualShippingFee', '*', '*', '*'),
        ],
        'name': 'create_order',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'create_order_br': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-BR', 'URL.lfs-api-live-br', '/api/sls/order/create', 10, 10),
            ('LFS-API-LIVE-BR', 'URL.lfs-api-live-br', '/api/logistic/batch_get_label_data/', 10, 10),
            ('LFS-API-LIVE-BR', 'URL.lfs-api-live-br', '/api/logistic/batch_check_print_label/', 10, 10),
        ],
        'extra_callchain': [
            # (cat_evt, cat_type, cat_name, api_call, '', '')
            ['-', 'API.lcs-api.shopee.co.br', 'Task.send', 'celery_task.celery_notify_status.push_weight_fee_retry', '', ''],
            ['-', 'API.lcs-api.shopee.co.br', 'Task.send', 'celery_task.celery_update_status.update_logistic_tracking_data', '', ''],
            ['-', 'API.lcs-api.shopee.co.br', 'Task.send', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb', '', ''],
            ['-', 'OrderCreateJob', 'Task.Send', 'WeightChangeTriggerCalcAsfJob', '', ''],
            ['-', 'LLS-FULFILLMENT-LIVE-BR', 'LLSGrpc-BR', '/lls_protobuf.WaybillCreateService/CreateLineWaybill', '', '']
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '(API\\.spx\\.shopee\\.*|API\\.fleet\\-order\\.ssc\\.shopee\\.*|FacadeDict|FleetOrder|API\\.fleet\\-order\\.ssc\\.shopee\\.*)', '*', '*', '*', '*'),
            ('*', '*', 'API\\.spx\\.shopee\\.*', '*', '*', '*'),
            ('*', '*', 'ShippingLabel', '*', '*', '*'),
            ('*', '*', 'ActualShippingFee', '*', '*', '*'),
        ],
        'name': 'create_order',
        'region': 'BR',
        'reload': False,
        'enabled': False,
    },
    'create_order_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/sls/order/create', 10, 10),
            ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/logistic/batch_get_label_data/', 10, 10),
            ('LFS-API-LIVE-TW', 'URL.lfs-api-live-tw', '/api/logistic/batch_check_print_label/', 10, 10),
        ],
        'extra_callchain': [
            # (cat_evt, cat_type, cat_name, api_call, '', '')
            ['-', 'API.lcs-api.shopee.co.tw', 'Task.send', 'celery_task.celery_notify_status.push_weight_fee_retry', '', ''],
            ['-', 'API.lcs-api.shopee.co.tw', 'Task.send', 'celery_task.celery_update_status.update_logistic_tracking_data', '', ''],
            ['-', 'API.lcs-api.shopee.co.tw', 'Task.send', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb', '', ''],
            ['-', 'OrderCreateJob', 'Task.Send', 'WeightChangeTriggerCalcAsfJob', '', '']
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '(API\\.spx\\.shopee\\.*|API\\.fleet\\-order\\.ssc\\.shopee\\.*|FacadeDict|FleetOrder|API\\.fleet\\-order\\.ssc\\.shopee\\.*)', '*', '*', '*', '*'),
            ('*', '*', 'API\\.spx\\.shopee\\.*', '*', '*', '*'),
            ('*', '*', 'ShippingLabel', '*', '*', '*'),
            ('*', '*', 'ActualShippingFee', '*', '*', '*'),
        ],
        'name': 'create_order',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },

    # push tracking
    'push_tracking_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LCS-TRACKINGAPI-ID', 'URL', '/api/webhook/update_status/local_jnt', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'name': 'push_tracking',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'push_tracking_br': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LCS-TRACKINGAPI-BR', 'URL', '/api/webhook/update_status/loggi', 10, 10),
            ('SLS-TRACKINGGRPC-LIVE-BR', 'URL.tracking-grpc-br', '/protocol.UpdateTrackingService/UpdateSiteTrackingWithString', 10, 10),
            ('SLS-TRACKINGGRPC-LIVE-BR', 'URL.tracking-grpc-br', '/protocol.UpdateTrackingService/UpdateTrackingWithString', 10, 10),
            ('LLS-FULFILLMENT-LIVE-BR', 'LLSGrpc-BR', '/lls_protobuf.WaybillTrackingService/UpdateWeightFee', 10, 10),
            ('LLS-FULFILLMENT-LIVE-BR', 'LLSGrpc-BR', '/lls_protobuf.WaybillTrackingService/NotifyPickUp', 10, 10),
        ],
        'extra_callchain': [
            # (cat_evt, cat_type, cat_name, api_call, '', '')
            ['-', 'API.lcs-api.shopee.co.br', 'Task.send', 'celery_task.celery_tidb_update_status.update_logistic_tracking_data_using_tidb', '', ''],
            ['-', 'ConsumeTrackingPushMessage', 'LLS', 'GetWaybillTrackingParamInfo', '', ''],
            ['-', 'ConsumeTrackingPushMessage', 'LTS', '/protocol.UpdateTrackingService/UpdateTrackingWithString', '', ''],
            ['-', 'ConsumeTrackingPushMessage', 'LTS', '/protocol.UpdateTrackingService/UpdateSiteTrackingWithString', '', ''],
            ['-', 'ConsumeTrackingPushMessage', 'LLS', '/lls_protobuf.WaybillTrackingService/UpdateWeightFee', '', ''],
            ['-', 'ConsumeTrackingPushMessage', 'LLS', '/lls_protobuf.WaybillTrackingService/NotifyPickUp', '', ''],
        ],
        'extra_rename_rules': [
            ('*', 'URL', '*', '*', '*', '*', '1:LCS'),
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', 'SaturnJob', '*', '*', '*', '*'),
            ('*', '(LLS|LTS|API\\.sls\\-partnerintegrationservice\\-br)', '*', '*', '*', '*'),
            ('*', '*', '(API|TWS|ResourceAPI)', '*', '*', '*'),
        ],
        'name': 'push_tracking',
        'region': 'BR',
        'reload': False,
        'enabled': False,
    },
    'push_tracking_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LCS-TRACKINGAPI-TW', 'URL', '/api/webhook/update_status/seven_c2c/notify_pickup', 10, 10),
        ],
        'extra_rename_rules': [
            ('*', '*', 'https://lcs\\-api\\.shopee\\.*', '*', '*', '*', '2:LCS'),
            ('*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '*', '1:RateAPI'),
            ('*', '*', 'API\\.sls\\.shopeemobile\\.com', '*', '*', '*', '2:RateAPI'),
        ],
        'extra_delete_rules': [
            ('*', '*', 'https', '*', '*', '*'),
        ],
        'name': 'push_tracking',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },

    # seller get pickup time
    'get_pickup_time_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/pickup/days/', 10, 10),
            ('SLS-API-LIVE-ID', 'URL', '/api/v3/logistics/return/pickup/days/', 10, 10),
        ],
        'name': 'get_pickup_time',
        'region': 'ID',
        'reload': False,
        'enabled': False,
    },
    'get_pickup_time_br': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/pickup/days/', 10, 10),
            ('SLS-API-LIVE-BR', 'URL', '/api/v3/logistics/return/pickup/days/', 10, 10),
        ],
        'name': 'get_pickup_time',
        'region': 'BR',
        'reload': False,
        'enabled': False,
    },
    'get_pickup_time_tw': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/pickup/days/', 10, 10),
            ('lps-api-live-tw', 'URL.lps-api-live-tw', '/api/v3/logistics/return/pickup/days/', 10, 10),
        ],
        'name': 'get_pickup_time',
        'region': 'TW',
        'reload': False,
        'enabled': False,
    },
}
