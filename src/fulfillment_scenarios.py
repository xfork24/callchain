#!./bin/python

FULFILLMENT_SCENARIOS = {
    'create_order_id': {
        'entrypoints': [
            # (cat_domain, cat_type, cat_name, sample_count, link_count)
            ('LFS-API-LIVE-ID', 'URL.lfs-api-live-id', '/api/sls/order/create', 1, 1),
        ],
        'extra_callchain': [
        ],
        'extra_rename_rules': [
            ('*', 'OrderCreatedTrackingUpdateJob', 'TrackingAssemble', 'TrackingAssembleSuccess', '*', '*', '2:LTS;3:DoTrackingExceptionAndMapAndDesc'),
        ],
        'extra_delete_rules': [
            ('*', 'OrderCreatedTrackingUpdateJob', 'GetTrackingFromLTS', '*', '*', '*'),
            ('*', 'SmartRouting', '*', '*', '*', '*'),
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
}
