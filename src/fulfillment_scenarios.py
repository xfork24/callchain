#!./bin/python

FULFILLMENT_SCENARIOS = {
    'create_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/order/create', 10, 10),
        ],
        'extra_callchain': [
        ],
        'extra_node_overwrite_rules': {},
        'extra_edge_overwrite_rules': {},
        'extra_rename_rules': [
            ('*', 'OrderCreatedTrackingUpdateJob', 'TrackingAssemble', 'TrackingAssembleSuccess', '*', '*', '2:LTS;3:DoTrackingExceptionAndMapAndDesc'),
            ('*', 'PIS', '(api|ResourceAPI)', '*', '*', '*', '2:3PL'),
        ],
        'extra_delete_rules': [
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
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LCS-TRACKINGAPI-ID', 'URL', '/api/webhook/update_status/local_jnt', 10, 10),
        ],
        'extra_callchain': [
        ],
        'extra_node_overwrite_rules': {},
        'extra_edge_overwrite_rules': {},
        'extra_rename_rules': [
            ('*', 'TrackingUpdateJob', 'TrackingAssemble', 'TrackingAssembleSuccess', '*', '*', '2:LTS;3:DoTrackingExceptionAndMapAndDesc'),
            ('*', 'PIS', '(API|ResourceAPI)', '*', '*', '*', '2:3PL'),
        ],
        'extra_delete_rules': [
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
