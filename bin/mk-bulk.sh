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

set -e

if [ -z $1 ] || [ -z $2 ]; then
    echo "usage: $0 <base_thingname> <num_things>"
    exit 1
fi

thing_name=$1
num_things=$2

date_time=$(date "+%Y-%m-%d_%H-%M-%S")

out_dir=$thing_name-$date_time
mkdir $out_dir || exit 1


for i in $(seq 1 $num_things) ; do
  openssl req -new -newkey rsa:2048 -nodes -keyout $out_dir/$thing_name$i.key -out $out_dir/$thing_name$i.csr -subj "/C=DE/ST=Berlin/L=Berlin/O=AWS/CN=Big Orchestra"

  one_line_csr=$(awk 'NF {sub(/\r/, ""); printf "%s\\n",$0;}' $out_dir/$thing_name$i.csr)

  echo "{\"ThingName\": \"$thing_name$i\", \"SerialNumber\": \"$i\", \"CSR\": \"$one_line_csr\"}" >> $out_dir/bulk.json
done

echo "output written to $out_dir/bulk.json"
