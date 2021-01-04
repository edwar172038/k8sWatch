#!/usr/bin python3
# -*- encoding: utf-8 -*-
# @Author : xinlong
# @File : editYaml.py
# @Time : 2020/12/31 17:37

import os
import yaml

filename = '.ci/deployment.yaml'
REPO = os.getenv('DRONE_REPO')
COMMIT_ID = os.getenv('DRONE_COMMIT_SHA')[:8]
image = "nexus-docker.test.cyclone.com/{REPO}:{COMMIT_ID}".format(REPO=REPO, COMMIT_ID=COMMIT_ID)

f1 = open(filename, 'r')
content = yaml.load(f1)
content['spec']['template']['spec']['containers'][0]['image'] = image
print(content)
f1.close()

f2 = open(filename, 'w')
result = yaml.dump(content)
f2.write(result)
f2.close()
