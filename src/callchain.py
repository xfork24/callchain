#!./bin/python

from fulfillment_scenarios import FULFILLMENT_SCENARIOS

from define import log
from cat import (
    CatDataManager,
    CallChainParser,
    CallChainRender,
)
import os
import json


if __name__ == '__main__':
    # check the following two lines first before running.
    all_scenarios = [FULFILLMENT_SCENARIOS]
    sub_folder_name = 'fulfillment_scenarios'

    for scenarios in all_scenarios:
        for name, scenario in scenarios.items():
            enabled = scenario['enabled']
            if not enabled:
                log.info('Skipped scenario: {0}'.format(name))
                continue
            scenario_path = '../{0}/{1}/{2}/'.format(sub_folder_name, scenario['region'], scenario['name'])
            if not os.path.exists(scenario_path):
                os.makedirs(scenario_path, exist_ok=True)
            reload = scenario['reload']
            extra_node_overwrite_rules = scenario['extra_node_overwrite_rules'] if 'extra_node_overwrite_rules' in scenario else None
            extra_edge_overwrite_rules = scenario['extra_edge_overwrite_rules'] if 'extra_edge_overwrite_rules' in scenario else None
            extra_rename_rules = scenario['extra_rename_rules'] if 'extra_rename_rules' in scenario else None
            extra_combine_rules = scenario['extra_combine_rules'] if 'extra_combine_rules' in scenario else None
            extra_delete_rules = scenario['extra_delete_rules'] if 'extra_delete_rules' in scenario else None
            extra_rules = (extra_node_overwrite_rules, extra_edge_overwrite_rules, extra_rename_rules, extra_combine_rules, extra_delete_rules)
            extra_callchain = scenario['extra_callchain'] if 'extra_callchain' in scenario else list()
            highlights = scenario['highlights'] if 'highlights' in scenario else None
            if reload:
                log.info('Processing scenario with reload: {0}'.format(name))
                callchain = list()
                original_callchain = list()
                calls = list()
                original_calls = list()
                for entrypoint in scenario['entrypoints']:
                    occ, ocl = CatDataManager(scenario_path, extra_callchain, extra_rules).get_callchain_and_report_with_links(*entrypoint)
                    cc = CallChainParser(*extra_rules).refine_callchain(occ)
                    cl = CallChainParser(*extra_rules).refine_calls(ocl)
                    original_callchain += occ
                    original_calls += ocl
                    callchain += cc
                    calls += cl
                # only the two `originals` will be re-generated if `reload`.
                with open(scenario_path + 'original_callchain.txt', 'w') as f:
                    f.write(json.dumps(original_callchain))
                with open(scenario_path + 'original_calls.txt', 'w') as f:
                    f.write(json.dumps(original_calls))
                # reparse callchain here to combine items and remove duplicate items, no need to reparse calls
                callchain = CallChainParser(*extra_rules).refine_callchain(callchain)
                ccr = CallChainRender(callchain, calls,
                                      highlights=highlights,
                                      graph_name=scenario['name'],
                                      region=scenario['region'],
                                      output_path=scenario_path)
            else:
                log.info('Processing scenario without reload: {0}'.format(name))
                ccr = CallChainRender(None, None,
                                      highlights=highlights,
                                      graph_name=scenario['name'],
                                      region=scenario['region'],
                                      output_path=scenario_path,
                                      load_exist=True,
                                      load_original=True,
                                      extra_rules=extra_rules)
            ccr.save_callchain()
            ccr.save_calls()
            ccr.save_stacks()
            ccr.save_highlight_stacks()
            f, _ = ccr.render_callchain(show_label=True, show_order=True)
            f.render()
            ccr.generate_plantuml_script()
            ccr.render_calls_v2()
            ccr.render_highlight_stacks()
