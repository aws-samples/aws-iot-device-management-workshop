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
# lambda function for just-in-time registration
#

#required libraries
import boto3
import logging
import os

# configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def create_thing(c_iot, thing_name):
    try:
        response = c_iot.create_thing(thingName='jitr-' + thing_name)
        logger.info("create_thing: response: {}".format(response))
    except Exception as e:
        logger.error("create_thing: {}".format(e))

def create_iot_policy(c_iot, policy_name):
    try:
        response = c_iot.create_policy(
            policyName=policy_name,
            policyDocument='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Action": "iot:*","Resource":"*"}]}'
        )
        logger.info("create_iot_policy: response: {}".format(response))
    except Exception as e:
        logger.error("create_iot_policy: {}".format(e))

def activate_certificate(c_iot, certificate_id):
    try:
        response = c_iot.update_certificate(
            certificateId=certificate_id,
            newStatus='ACTIVE'
        )
        logger.info("activate_cert: response: {}".format(response))
    except Exception as e:
        logger.error("activate_certificate: {}".format(e))

def attach_policy(c_iot, certificate_id):
    try:
        response = c_iot.describe_certificate(
            certificateId=certificate_id
        )
        #logger.info("describe_certificate: response: {}".format(response))
        certificate_arn = response['certificateDescription']['certificateArn']
        logger.info("certificate_arn: {}".format(certificate_arn))

        response = c_iot.attach_thing_principal(
            thingName='jitr-' + certificate_id,
            principal=certificate_arn
        )
        logger.info("attach_thing_principal: response: {}".format(response))

        response = c_iot.attach_policy(
            policyName=certificate_id,
            target=certificate_arn
        )
        logger.info("attach_policy: response: {}".format(response))
    except Exception as e:
        logger.error("attach_policy: {}".format(e))

def lambda_handler(event, context):
    logger.info("event:\n" + str(event))

    region = os.environ["AWS_REGION"]
    logger.info("region: {}".format(region))

    ca_certificate_id = event['caCertificateId']
    certificate_id = event['certificateId']
    certificate_status = event['certificateStatus']

    logger.info("ca_certificate_id: " + ca_certificate_id)
    logger.info("certificate_id: " + certificate_id)
    logger.info("certificate_status: " + certificate_status)

    c_iot = boto3.client('iot')
    create_thing(c_iot, certificate_id)
    create_iot_policy(c_iot, certificate_id)
    activate_certificate(c_iot, certificate_id)
    attach_policy(c_iot, certificate_id)


    #for k in os.environ.keys():
    #    logger.info("{}: {}".format(k, os.environ[k]))

    return True
