#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time

__author__ = 'xuebk'

import rancher
import argparse
from k8s_yaml import  _get_yaml, get_images_text, _get_artifact_info, _get_namespaceId, _get_nginx_yaml

HEADERS = {'Accept': 'application/json'}
client = rancher.Client(url='你 rancher 的 url',
                        access_key='生成的 access',
                        secret_key='生成的 secret')


def _get_workloads_url():
    workloads = client._get_response(Project_Data['data'][0]['links']['workloads']).json()
    # return work_


def Judge_workload(ARTIFACTID, info=False):
    """
        判断是否存在相应 项目
    :param ARTIFACTID:
    :return:
    """
    try:
        workloads = client._get_response(Project_Data['data'][0]['links']['workloads']).json()
    except:
        return False
    for workload in workloads['data']:
        if workload['name'] == ARTIFACTID:
            if info:
                return workload
            else:
                return True
    if info:
        return {}
    else:
        return False


def work_updata(ARTIFACTID, BUILD_ID, ENV_EnvIronMent, Types):
    """
        更新方法
    :return:
    """
    image = get_images_text(ARTIFACTID, BUILD_ID, ENV_EnvIronMent, Types)
    # 获取相应内容
    workload = Judge_workload(ARTIFACTID, True)
    _yaml = client._get_response(workload['links']['yaml']).json()
    _yaml['spec']['template']['spec']['containers'][0]['image'] = image
    # pprint.pprint(_yaml)
    update = workload['links']['yaml']
    # 进行更新
    client._put(update, _yaml)
    # 获取最新值
    image_new = client._get_response(workload['links']['yaml']).json()['spec']['template']['spec']['containers'][0][
        'image']
    if image == image_new:
        print("更新成功")
    else:
        print("更新失败")


def work_create(ARTIFACTID, BUILD_ID, ENV_EnvIronMent, Types):
    _yaml_data = _get_yaml(ARTIFACTID, BUILD_ID, ENV_EnvIronMent, Types)
    client._post(Project_Data['data'][0]['links']['workloads'], _yaml_data)
    print("创建成功")


def work_del(ARTIFACTID):
    try:
        workload = Judge_workload(ARTIFACTID, True)
        remove = workload['links']['remove']
        client._delete(remove)
        print('删除成功.')
    except :
        pass


def _work_create_base(ENV_EnvIronMent):
    print("创建基础 base 成功")


def MyParser():
    """
        本地 测试方法
    :return:
    """
    # #### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### ##### #####
    parser = argparse.ArgumentParser()
    parser.add_argument("-ARTIFACTID", help="ARTIFACTID", default=None)
    parser.add_argument("-BUILD_P", help="jenkins", default=None)
    parser.add_argument("-BUILD_ID", help="jenkins", default=None)
    parser.add_argument("-ENV_EnvIronMent", help="环境", default=None)
    parser.add_argument("-ENV_host_region", help="所在环境", default='aliyun')
    parser.add_argument("-Types", help="项目类型", default=None)
    parser.add_argument("-delete", help="项目类型", default=False)
    # parser.add_argument("-commitid", help="commitid", default=None)
    args, argv = parser.parse_known_args()
    return parser


if __name__ == "__main__":
    parser = MyParser()
    args, argv = parser.parse_known_args()
    Project_Data = client.list_project(name=args.ENV_EnvIronMent, clusterId="这里是 clusterId")
    # _work_create_base(args.ENV_EnvIronMent) # 初始化 base 专用. 没事的时候不需要打开.打开后.后面全部东西都需要注释.
    # updata
    ARTIFACTID_info = _get_artifact_info(args.ARTIFACTID)
    if args.delete:
        work_del(args.ARTIFACTID)
        time.sleep(5)
    if Judge_workload(ARTIFACTID_info.get("artfactid")):
        work_updata(args.ARTIFACTID, args.BUILD_ID, args.ENV_EnvIronMent, args.Types)
    else:
        work_create(args.ARTIFACTID, args.BUILD_ID, args.ENV_EnvIronMent, args.Types)
