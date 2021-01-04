#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : xinlong
# @File : watchEvent.py
# @Time : 2020/11/19 18:13

import re
import json
import requests
import datetime
from kubernetes import client, config, watch

config.load_incluster_config()

v1 = client.CoreV1Api()

w = watch.Watch()
for event in w.stream(v1.list_pod_for_all_namespaces, _request_timeout=0):
    metadata = event['object'].metadata
    annotations = metadata.annotations
    spec = event['object'].spec
    status = event['object'].status
