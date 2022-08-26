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
            ('*', 'PIS', '(api|ResourceAPI)', '*', '*', '*', '2:3PL'),
        ],
        'extra_delete_rules': [
            ('*', 'OrderCreatedTrackingUpdateJob', 'GetTrackingFromLTS', '*', '*', '*'),
            ('*', 'StatusChangeTriggerCalcAsfJob', 'ActualShippingFee', 'StatusChangedTriggerASF', '*', '*'),
            ('*', '*', 'TrackingOperate', '*', '*', '*'),
            ('*', 'SmartRouting', '*', '*', '*', '*'),
            ('*', 'OMS', '*', '*', '*', '*'),
        ],
        'filter_stack': ['/api/sls-basic/freight/calc_esf_weight/', 'calculateWeightBySdk', 'CreateLineWaybill'],
        'puml_head': """
@startuml

box "SLS Synchronous API Call"
participant LPS
participant WBC
participant SmartRouting
participant LFS
participant LLS
participant LCS
participant PIS
participant LCOS
participant IDCS
participant RateAPI
participant LTS
participant TrackingPN
end box

box "SLS Asynchronous Jobs"
participant OrderCreateJob
participant UpdateLogisticInfoToOmsJob
participant PushOmsTrackingWithoutStatusJob
participant OrderCreatedTrackingUpdateJob
participant StatusChangeTriggerCalcAsfJob
participant Calc3plEsfJob
end box

box "SSC External Dependencies"
participant Saturn
participant SPX
participant OMS
end box

box "3rd-party Dependencies"
participant 3PL
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
