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

# creates paramter for provision-thing

if [ -z $1 ]; then
    echo "usage: $0 <thingname>"
    exit 1
fi

thing_name=$1

openssl req -new -newkey rsa:2048 -nodes -keyout $thing_name.key -out $thing_name.csr -subj "/C=DE/ST=Berlin/L=Berlin/O=AWS/CN=Big Orchestra"

one_line_csr=$(awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' $thing_name.csr)

echo "{\"ThingName\": \"$thing_name\", \"SerialNumber\": \"$RANDOM\", \"CSR\": \"$one_line_csr\"}"
