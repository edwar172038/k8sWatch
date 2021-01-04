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
check_port = 6300


def _add_pod(namespace, podname, container_name, image, ip, start_at, class_dump):
    url = 'http://coverage.test.cyclone.com/coverageApi/k8s/pod'
    params = {
        'namespace': namespace,
        'podname': podname,
        'container_name': container_name,
        'image': image,
        'ip': ip,
        'start_at': start_at,
        'class_dump': class_dump
    }
    requests.post(url, json=params)


def _delete_pod(namespace, podname, class_dump, ip=''):
    url = 'http://coverage.test.cyclone.com/coverageApi/k8s/pod'
    params = {
        'namespace': namespace,
        'podname': podname,
        'class_dump': class_dump,
        'ip': ip,
    }
    requests.delete(url, json=params)


w = watch.Watch()
for event in w.stream(v1.list_pod_for_all_namespaces, _request_timeout=0):
    metadata = event['object'].metadata
    annotations = metadata.annotations
    spec = event['object'].spec
    status = event['object'].status

    port_list = []
    if '_ports' in spec.containers[0].__dict__ and spec.containers[0].ports:
        for port in spec.containers[0].ports:
            port_list.append(str(port.container_port))

    if '6300' in port_list:
        is_jacoco = True
    else:
        is_jacoco = False

    namespace = metadata.namespace
    podname = spec.containers[0].name
    container_name = metadata.name

    if event['type'] == 'DELETED':
        if namespace == 'jacoco' and podname == 'jacoco':
            print('Event[{time}]: {type} {namespace}/{podname}/{container_name} {ip}'.format(
                time=(metadata.creation_timestamp + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                type=event['type'],
                namespace=namespace,
                podname=podname,
                container_name=metadata.name,
                ip=ip))
            ip = status.pod_ip
            _delete_pod(namespace, podname, '', ip)
            continue

    if is_jacoco and event['type'] == 'DELETED' and dump_path:
        print('Event[{time}]: {type} {namespace}/{podname}/{container_name} {dump_path}'.format(
            time=(metadata.creation_timestamp + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
            type=event['type'],
            namespace=namespace,
            podname=podname,
            container_name=metadata.name,
            dump_path=dump_path))
        _delete_pod(namespace, podname, dump_path)
        continue

    if not status.container_statuses:
        continue
    container_statuses = status.container_statuses[0]
    if container_statuses.ready and container_statuses.started:
        ip = status.pod_ip
        start_at = container_statuses.state.running.started_at
    else:
        continue

    if is_jacoco:
        dump_path = '{podname}-{ip}'.format(podname=podname, ip=ip)
        image = spec.containers[0].image
        ip = ip
        start_at = start_at.strftime('%Y-%m-%d %H:%M:%S')
        print(
            'Event[{time}]: {type} {namespace}/{podname}/{container_name} {ip} {image} {hasPort} {start_at} {dump_path}'.format(
                time=(metadata.creation_timestamp + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S'),
                type=event['type'],
                namespace=namespace,
                podname=podname,
                container_name=container_name,
                ip=ip,
                image=image,
                hasPort=is_jacoco,
                start_at=start_at,
                dump_path=dump_path
            ))
        _add_pod(namespace, podname, container_name, image, ip, start_at, dump_path)
