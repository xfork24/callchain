#!./bin/python

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
        'reload': False,
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
        'reload': False,
        'enabled': True,
    },
}
