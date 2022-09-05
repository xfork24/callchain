#!./bin/python

ALL_SCENARIOS = {
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
        'extra_callchain': [],
        'extra_node_overwrite_rules': {},
        'extra_edge_overwrite_rules': {},
        'extra_rename_rules': [
        ],
        'extra_delete_rules': [
            ('*', 'SLS\\-API', '*', '*', '*', '*'),
        ],
        # 'highlights': [],
        'name': 'pre_fulfillment',
        'region': 'ID',
        'reload': True,
        'enabled': True,
    },
    'create_order_id': {  # Must: any unique key is fine
        'entrypoints': [  # Must: define the entrypoints of your scenario, it's what your service cares and doesn't need to be the root caller
            # (cat_domain, cat_type, cat_name, sample_count, link_sample_count)
            # sample count is how many samples you want to analyze from CAT, please limit it to < 50 to avoid CAT server crash.
            # link_sample_count is how many link samples you want to analyze from CAT if one `link rule` is matched, also limit it to < 50 to avoid CAT server crash.
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/order/create', 10, 10),
        ],
        'extra_callchain': [  # Optional: additional callchain you want to add to your scenario
            # (id, caller, callee, api, info1, info2)
        ],
        'extra_node_overwrite_rules': {  # Optional: additional node overwrite rules you want to apply for your scenario
            # node_pattern: replace_to
        },
        'extra_edge_overwrite_rules': {  # Optional: additional node overwrite rules you want to apply for your scenario
            # edge_pattern: replace_to
        },
        'extra_rename_rules': [  # Optional: additional rename rules you want to apply for your scenario
            # (id, caller, callee, api, info1, info2, rule)
            ('*', 'OrderCreatedTrackingUpdateJob', 'TrackingAssemble', 'TrackingAssembleSuccess', '*', '*', 'Callee:LTS;API:DoTrackingExceptionAndMapAndDesc'),
            ('*', 'PIS', '(api|ResourceAPI)', '*', '*', '*', 'Callee:3PL'),
        ],
        'extra_delete_rules': [  # Optional: additional delete rules you want to apply for your scenario
            # (id, caller, callee, api, info1, info2)
            ('*', 'OrderCreatedTrackingUpdateJob', 'GetTrackingFromLTS', '*', '*', '*'),
            ('*', 'StatusChangeTriggerCalcAsfJob', 'ActualShippingFee', 'StatusChangedTriggerASF', '*', '*'),
            ('*', '*', 'TrackingOperate', '*', '*', '*'),
            ('*', 'SmartRouting', '*', '*', '*', '*'),
            ('*', 'OMS', '*', '*', '*', '*'),
        ],
        # 'highlights': ['/api/sls-basic/freight/calc_esf_weight/', '/api/lls/create_line_waybill'],  #  Optional: highlight stacks contains specific calls
        'name': 'create_order',  # Must: the human-readable name of your scenario
        'region': 'ID',  # Must: the region of your scenario
        'reload': True,  # Must: whether you want to re-fetch samples from CAT server
        'enabled': True,  # Must: whether you want to parse this scenario
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
