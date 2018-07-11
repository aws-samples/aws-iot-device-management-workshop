#!/bin/bash

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

# mk-dm-ws-tar.sh
# create tar file which is used to bootstrap an EC2 instance
 
echo "create lambda zip"
cd lambda && zip lambda_function.zip lambda_function.py && cd ..

echo "create dm-ws.tar"
tar cvf dm-ws.tar templateBody.json \
    bin/ lambda/ \
    job-agent/job-agent.py job-agent/job-document.json

