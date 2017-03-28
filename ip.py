"""
This playbook executes multiple investigative actions to determine if an ip is malicious.
"""

import phantom.rules as phantom
import json
from datetime import datetime, timedelta

##############################
# Start - Global Code Block


import ipaddress
def ipfilter(ip):
    ranges =  ['192.168.0.0/24',]
    for item in ranges:
        if phantom.is_ip(ip) and ipaddress.ip_address(unicode(ip)) not in ipaddress.ip_network(unicode(item)):
            return ip
    return None

# End - Global Code block
##############################

def on_start(container):
    phantom.debug('on_start() called')
    
    # call 'filter_2' block
    filter_2(container=container)

    return

def filter_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('filter_1() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["ip_reputation_1:action_result.summary.detected_urls", ">", 0],
        ],
        name="filter_1:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        run_query_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        hunt_ip_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        whois_ip_3(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def Send_Email_Unknown(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Send_Email_Unknown() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_Unknown' call

    parameters = []
    
    # build parameters list for 'Send_Email_Unknown' call
    parameters.append({
        'body': "Please see the results of the phantom PB run",
        'to': "notifications@phantom.us",
        'from': "notifications@phantom.us",
        'attachments': "",
        'subject': "Unknown Domain Port Scan",
    })

    phantom.act("send email", parameters=parameters, assets=['smtp'], callback=set_severity_5, name="Send_Email_Unknown")    
    
    return

def whois_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('whois_domain_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'whois_domain_1' call
    passed_filtered_results_data_1 = phantom.collect2(container=container, datapath=["domain_reputation_2:filtered-action_result.parameter.domain", "domain_reputation_2:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'whois_domain_1' call
    for passed_filtered_results_item_1 in passed_filtered_results_data_1:
        if passed_filtered_results_item_1[0]:
            parameters.append({
                'domain': passed_filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': passed_filtered_results_item_1[1]},
            })

    phantom.act("whois domain", parameters=parameters, assets=['domaintools'], callback=join_Send_Email_bad_domain, name="whois_domain_1")    
    
    return

def hunt_domain_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('hunt_domain_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'hunt_domain_1' call
    passed_filtered_results_data_1 = phantom.collect2(container=container, datapath=["domain_reputation_2:filtered-action_result.parameter.domain", "domain_reputation_2:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'hunt_domain_1' call
    for passed_filtered_results_item_1 in passed_filtered_results_data_1:
        if passed_filtered_results_item_1[0]:
            parameters.append({
                'domain': passed_filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': passed_filtered_results_item_1[1]},
            })

    phantom.act("hunt domain", parameters=parameters, assets=['isightpartners'], callback=join_Send_Email_bad_domain, name="hunt_domain_1")    
    
    return

def run_query_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_query_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_query_1' call
    passed_filtered_results_data_1 = phantom.collect2(container=container, datapath=["ip_reputation_1:filtered-action_result.parameter.ip", "ip_reputation_1:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'run_query_1' call
    for passed_filtered_results_item_1 in passed_filtered_results_data_1:
        if passed_filtered_results_item_1[0]:
            parameters.append({
                'query': passed_filtered_results_item_1[0],
                'display': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': passed_filtered_results_item_1[1]},
            })

    phantom.act("run query", parameters=parameters, assets=['splunk_entr'], callback=join_Send_Email_bad_ip, name="run_query_1")    
    
    return

def filter_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('filter_3() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["domain_reputation_2:action_result.data.*.Webutation domain info.Safety score", "!=", ""],
            ["domain_reputation_2:action_result.data.*.Webutation domain info.Safety score", "<", 100],
        ],
        logical_operator='and',
        name="filter_3:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        run_query_2(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        whois_domain_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)
        hunt_domain_1(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    # collect filtered artifact ids for 'if' condition 2
    matched_artifacts_2, matched_results_2 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["domain_reputation_2:action_result.data.*.Webutation domain info.Safety score", "==", ""],
        ],
        name="filter_3:condition_2")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_2 or matched_results_2:
        Send_Email_Unknown(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_2, filtered_results=matched_results_2)

    return

def domain_reputation_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'domain_reputation_2' call
    results_data_1 = phantom.collect2(container=container, datapath=['reverse_ip_2:action_result.data.*.ip_addresses.domain_names', 'reverse_ip_2:action_result.parameter.context.artifact_id'], action_results=results)

    parameters = []
    
    # build parameters list for 'domain_reputation_2' call
    for results_item_1 in results_data_1:
        if results_item_1[0]:
            for domain in results_item_1[0]:
                if (not domain):
                    continue
                parameters.append({
                    'domain': domain,
                    # context (artifact id) is added to associate results with the artifact
                    'context': {'artifact_id': results_item_1[1]},
                })

    if parameters:
        phantom.act("domain reputation", parameters=parameters, assets=['virustotal_private'], callback=domain_reputation_2_callback, name="domain_reputation_2", parent_action=action)    
    else:
        phantom.error("'domain_reputation_2' will not be executed due to lack of parameters")
    
    return

def domain_reputation_2_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('domain_reputation_2_callback() called')
    
    filter_3(action=action, success=success, container=container, results=results, handle=handle)
    join_filter_4(action=action, success=success, container=container, results=results, handle=handle)

    return

def Send_Email_safe(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Send_Email_safe() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_safe' call

    parameters = []
    
    # build parameters list for 'Send_Email_safe' call
    parameters.append({
        'body': "A safe port scan was detected, see Phantom for details.",
        'to': "michael@phantom.us",
        'from': "admin@phantom.us",
        'attachments': "",
        'subject': "Port Scan determined safe",
    })

    phantom.act("send email", parameters=parameters, assets=['smtp'], callback=set_severity_2, name="Send_Email_safe")    
    
    return

def join_Send_Email_safe(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_Send_Email_safe() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'ip_reputation_1', 'domain_reputation_2' ]):
        
        # call connected block "Send_Email_safe"
        Send_Email_safe(container=container, handle=handle)
    
    return

def filter_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('filter_4() called')

    # collect filtered artifact ids for 'if' condition 1
    matched_artifacts_1, matched_results_1 = phantom.condition(
        container=container,
        action_results=results,
        conditions=[
            ["ip_reputation_1:action_result.summary.detected_urls", "==", 0],
            ["domain_reputation_2:action_result.data.*.Webutation domain info.Safety score", "==", 100],
        ],
        logical_operator='and',
        name="filter_4:condition_1")

    # call connected blocks if filtered artifacts or results
    if matched_artifacts_1 or matched_results_1:
        join_Send_Email_safe(action=action, success=success, container=container, results=results, handle=handle, filtered_artifacts=matched_artifacts_1, filtered_results=matched_results_1)

    return

def join_filter_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_filter_4() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'ip_reputation_1', 'domain_reputation_2' ]):
        
        # call connected block "filter_4"
        filter_4(container=container, handle=handle)
    
    return

def run_query_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('run_query_2() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'run_query_2' call
    passed_filtered_results_data_1 = phantom.collect2(container=container, datapath=["domain_reputation_2:filtered-action_result.parameter.domain", "domain_reputation_2:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'run_query_2' call
    for passed_filtered_results_item_1 in passed_filtered_results_data_1:
        if passed_filtered_results_item_1[0]:
            parameters.append({
                'query': passed_filtered_results_item_1[0],
                'display': "",
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': passed_filtered_results_item_1[1]},
            })

    phantom.act("run query", parameters=parameters, assets=['splunk_entr'], callback=join_Send_Email_bad_domain, name="run_query_2")    
    
    return

def Send_Email_bad_domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Send_Email_bad_domain() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_bad_domain' call

    parameters = []
    
    # build parameters list for 'Send_Email_bad_domain' call
    parameters.append({
        'body': "Check phantom to see output results for bad port scan.",
        'to': "notifications@phantom.us",
        'from': "notifications@phantom.us",
        'attachments': "",
        'subject': "Port Scan detected from bad domain",
    })

    phantom.act("send email", parameters=parameters, assets=['smtp'], callback=set_severity_4, name="Send_Email_bad_domain")    
    
    return

def join_Send_Email_bad_domain(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_Send_Email_bad_domain() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'run_query_2', 'whois_domain_1', 'hunt_domain_1' ]):
        
        # call connected block "Send_Email_bad_domain"
        Send_Email_bad_domain(container=container, handle=handle)
    
    return

def Send_Email_bad_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('Send_Email_bad_ip() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'Send_Email_bad_ip' call

    parameters = []
    
    # build parameters list for 'Send_Email_bad_ip' call
    parameters.append({
        'body': "Check phantom to see output results for bad port scan.",
        'to': "michael@phantom.us",
        'from': "admin@phantom.us",
        'attachments': "",
        'subject': "Port Scan detected from bad IP",
    })

    phantom.act("send email", parameters=parameters, assets=['smtp'], callback=set_severity_1, name="Send_Email_bad_ip")    
    
    return

def join_Send_Email_bad_ip(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('join_Send_Email_bad_ip() called')

    # check if all connected incoming actions are done i.e. have succeeded or failed
    if phantom.actions_done([ 'hunt_ip_1', 'run_query_1', 'whois_ip_3' ]):
        
        # call connected block "Send_Email_bad_ip"
        Send_Email_bad_ip(container=container, handle=handle)
    
    return

def hunt_ip_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('hunt_ip_1() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'hunt_ip_1' call
    passed_filtered_results_data_1 = phantom.collect2(container=container, datapath=["ip_reputation_1:filtered-action_result.parameter.ip", "ip_reputation_1:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'hunt_ip_1' call
    for passed_filtered_results_item_1 in passed_filtered_results_data_1:
        if passed_filtered_results_item_1[0]:
            parameters.append({
                'ip': passed_filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': passed_filtered_results_item_1[1]},
            })

    phantom.act("hunt ip", parameters=parameters, assets=['isightpartners'], callback=join_Send_Email_bad_ip, name="hunt_ip_1")    
    
    return

def reverse_ip_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('reverse_ip_2() called')

    # collect data for 'reverse_ip_2' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'reverse_ip_2' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("reverse ip", parameters=parameters, assets=['domaintools'], callback=domain_reputation_2, name="reverse_ip_2")    
    
    return

def whois_ip_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('whois_ip_3() called')
    
    #phantom.debug('Action: {0} {1}'.format(action['name'], ('SUCCEEDED' if success else 'FAILED')))
    
    # collect data for 'whois_ip_3' call
    passed_filtered_results_data_1 = phantom.collect2(container=container, datapath=["ip_reputation_1:filtered-action_result.parameter.ip", "ip_reputation_1:filtered-action_result.parameter.context.artifact_id"], action_results=filtered_results)

    parameters = []
    
    # build parameters list for 'whois_ip_3' call
    for passed_filtered_results_item_1 in passed_filtered_results_data_1:
        if passed_filtered_results_item_1[0]:
            parameters.append({
                'ip': passed_filtered_results_item_1[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': passed_filtered_results_item_1[1]},
            })

    phantom.act("whois ip", parameters=parameters, assets=['domaintools'], callback=join_Send_Email_bad_ip, name="whois_ip_3")    
    
    return

def filter_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):

    # collect filtered artifact ids for 'if' condition 1
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'], scope='all')
    for container_item in container_data:
        if ipfilter(container_item[0]):
            ip_reputation_1(container=container)
            reverse_ip_2(container=container)
        else:
            join_Send_Email_safe(container=container)

    return

def ip_reputation_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('ip_reputation_1() called')

    # collect data for 'ip_reputation_1' call
    container_data = phantom.collect2(container=container, datapath=['artifact:*.cef.sourceAddress', 'artifact:*.id'])

    parameters = []
    
    # build parameters list for 'ip_reputation_1' call
    for container_item in container_data:
        if container_item[0]:
            parameters.append({
                'ip': container_item[0],
                # context (artifact id) is added to associate results with the artifact
                'context': {'artifact_id': container_item[1]},
            })

    phantom.act("ip reputation", parameters=parameters, assets=['virustotal_private'], callback=ip_reputation_1_callback, name="ip_reputation_1")    
    
    return

def ip_reputation_1_callback(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('ip_reputation_1_callback() called')
    
    filter_1(action=action, success=success, container=container, results=results, handle=handle)
    join_filter_4(action=action, success=success, container=container, results=results, handle=handle)

    return

def set_severity_1(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_severity_1() called')
    
    # set container properties for: severity
    update_data = {
        "severity" : "high",
    }

    phantom.update(container, update_data)

    return

def set_severity_2(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_severity_2() called')
    
    # set container properties for: severity
    update_data = {
        "severity" : "low",
    }

    phantom.update(container, update_data)

    set_status_3(container=container)

    return

def set_status_3(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_status_3() called')
    
    # set container properties for: status
    update_data = {
        "status" : "closed",
    }

    phantom.update(container, update_data)

    return

def set_severity_4(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_severity_4() called')
    
    # set container properties for: severity
    update_data = {
        "severity" : "high",
    }

    phantom.update(container, update_data)

    return

def set_severity_5(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_severity_5() called')
    
    # set container properties for: severity
    update_data = {
        "severity" : "low",
    }

    phantom.update(container, update_data)

    set_status_6(container=container)

    return

def set_status_6(action=None, success=None, container=None, results=None, handle=None, filtered_artifacts=None, filtered_results=None):
    phantom.debug('set_status_6() called')
    
    # set container properties for: status
    update_data = {
        "status" : "closed",
    }

    phantom.update(container, update_data)

    return

def on_finish(container, summary):
    phantom.debug('on_finish() called')
    # This function is called after all actions are completed.
    # summary of all the action and/or all detals of actions 
    # can be collected here.

    # summary_json = phantom.get_summary()
    # if 'result' in summary_json:
        # for action_result in summary_json['result']:
            # if 'action_run_id' in action_result:
                # action_results = phantom.get_action_results(action_run_id=action_result['action_run_id'], result_data=False, flatten=False)
                # phantom.debug(action_results)

    return