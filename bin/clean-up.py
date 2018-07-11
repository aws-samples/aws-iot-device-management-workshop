#!/usr/bin/python

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

#
# clean-up.py
#
# cleans up after workshop


import boto3
import os
import random
import sys
import time

#######################################################################
basenames = ['bulky', 'jitr-']
thing_names = ['my-first-thing', 'my-second-thing', 'job-agent', 'group-member', 'my-jitp-device']
thing_groups = ['building-one', 'bulk-group']
#######################################################################

def delete_thing(thing_name):
    global policy_names
    print("  DELETING {}".format(thing_name))

    try:
        r_principals = c_iot.list_thing_principals(thingName=thing_name)
    except Exception as e:
        print("ERROR listing thing principals: {}".format(e))
        r_principals = {'principals': []}

    #print("r_principals: {}".format(r_principals))
    for arn in r_principals['principals']:
        cert_id = arn.split('/')[1]
        print("  arn: {} cert_id: {}".format(arn, cert_id))

        r_detach_thing = c_iot.detach_thing_principal(thingName=thing_name,principal=arn)
        print("  DETACH THING: {}".format(r_detach_thing))

        r_upd_cert = c_iot.update_certificate(certificateId=cert_id,newStatus='INACTIVE')
        print("  INACTIVE: {}".format(r_upd_cert))

        r_policies = c_iot.list_principal_policies(principal=arn)
        #print("    r_policies: {}".format(r_policies))

        for pol in r_policies['policies']:
            pol_name = pol['policyName']
            print("    pol_name: {}".format(pol_name))
            policy_names[pol_name] = 1
            r_detach_pol = c_iot.detach_policy(policyName=pol_name,target=arn)
            print("    DETACH POL: {}".format(r_detach_pol))

        r_del_cert = c_iot.delete_certificate(certificateId=cert_id,forceDelete=True)
        print("  DEL CERT: {}".format(r_del_cert))

    r_del_thing = c_iot.delete_thing(thingName=thing_name)
    print("  DELETE THING: {}\n".format(r_del_thing))

c_iot = boto3.client('iot')
c_iot_data = boto3.client('iot-data')

for basename in basenames:
    print("BASENAME: {}".format(basename))

    query_string = "thingName:" + basename + "*"
    print("query_string: {}".format(query_string))

    # first shot
    response = c_iot.search_index(
        queryString=query_string,
    )

    print("response:\n{}".format(response))
    for thing in response["things"]:
        thing_names.append(thing["thingName"])

    while 'nextToken' in response:
        next_token = response['nextToken']
        print("next token: {}".format(next_token))
        response = c_iot.search_index(
            queryString=query_string,
            nextToken=next_token
        )
        print("response:\n{}".format(response))
        for thing in response["things"]:
            thing_names.append(thing["thingName"])

#print("END WHILE")
print("--------------------------------------\n")
print("number of things to delete: {}\n".format(len(thing_names)))
print("thing names to be DELETED:\n{}\n".format(thing_names))
print("--------------------------------------\n")

raw_input("THE DEVICES IN THE LIST ABOVE WILL BE DELETED INCLUDING CERTIFICATES AND POLICIES\n== press <enter> to continue, <ctrl+c> to abort!\n")
#sys.exit()

policy_names = {}

for thing_name in thing_names:
    print("THING NAME: {}".format(thing_name))
    delete_thing(thing_name)
    time.sleep(0.5) # avoid to run into api throttling

for thing_group in thing_groups:
    print(thing_group)
    r_del_grp = c_iot.delete_thing_group(thingGroupName=thing_group)
    print("DELETE THING GROUP: {}".format(r_del_grp))

print("detaching targets from policy {}".format(os.environ['IOT_POLICY']))
r_targets_pol = c_iot.list_targets_for_policy(policyName=os.environ['IOT_POLICY'],pageSize=250)
print(r_targets_pol)
for arn in r_targets_pol['targets']:
    print("DETACH: {}".format(arn))
    r_detach_pol = c_iot.detach_policy(policyName=os.environ['IOT_POLICY'],target=arn)
    print("r_detach_pol: {}\n".format(r_detach_pol))

for p in policy_names:
    if p == os.environ['IOT_POLICY']:
        continue
    print("DELETE policy: {}".format(p))
    try:
        r_del_pol = c_iot.delete_policy(policyName=p)
        print("r_del_pol: {}".format(r_del_pol))
    except Exception as e:
        print("ERROR: {}".format(e))
