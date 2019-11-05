#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'xuebk'

import pprint
from job_dict_java_dict_test import job_java_dict_test

__ENV_EnvIronMent = {
    'TEST': {
        'namespaceId': 'test'
        'eureka': '注册中心'
    }
}


def _get_artifact_info(artifact_id):
    """
        返回 全部 artifact 信息
    :return:
    """
    return job_java_dict_test.get(artifact_id)


def _get_namespaceId(ENV_EnvIronMent):
    return __ENV_EnvIronMent.get(ENV_EnvIronMent).get('namespaceId')


def _get_Dsentry_dns(ENV_EnvIronMent):
    return __ENV_EnvIronMent.get(ENV_EnvIronMent).get('dsn')


def _get_Dsentry_eureka(ENV_EnvIronMent):
    return __ENV_EnvIronMent.get(ENV_EnvIronMent).get('eureka')


def get_images_text(ARTIFACTID, BUILD_ID, ENV_EnvIronMent, Types):
    """
        获取拼接的 最新 镜像 id
    :param ARTIFACTID:
    :param BUILD_ID:
    :return:
    """
    image = "registry-vpc.cn-hongkong.aliyuncs.com/%s/%s:%s" % (
        Types,
        ARTIFACTID,
        BUILD_ID
    )
    return image

def _get_yaml(ARTIFACTID, BUILD_ID, ENV_EnvIronMent, Types):
    """
        获取最新的 yaml
    :param ARTIFACTID:
    :param BUILD_ID:
    :param ENV_EnvIronMent:
    :param Types:
    :return:
    """
    """
            创建相应方法
        :return:
        """
    # 获取相应内容
    workload = _get_artifact_info(ARTIFACTID)
    namespaceId = "%s-app" % (_get_namespaceId(ENV_EnvIronMent))
    image = get_images_text(workload['artfactid'], BUILD_ID, ENV_EnvIronMent, Types)
    ports = [
        int(workload['ports']),
    ]
    defaultZone = _get_Dsentry_eureka(ENV_EnvIronMent)
    ymal_data = {
        'hostIPC': False,
        'hostNetwork': False,
        'hostPID': False,
        'paused': False,
        'type': 'workload',
        'namespaceId': namespaceId,
        'scale': 1,
        'dnsPolicy': 'ClusterFirst',
        'restartPolicy': 'Always',
        'labels': {},
        'containers': [
            {
                'initContainer': False,
                'restartCount': 0,
                'stdin': True,
                'stdinOnce': False,
                'tty': True,
                'type': 'container',
                'privileged': False,
                'allowPrivilegeEscalation': False,
                'readOnly': False,
                'runAsNonRoot': False,
                'namespaceId': namespaceId,
                'imagePullPolicy': 'Always',
                'environmentFrom': [
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'spec.nodeName', 'targetKey': 'MY_NODE_NAME'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'metadata.name', 'targetKey': 'MY_POD_NAME'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'metadata.namespace',
                     'targetKey': 'MY_POD_NAMESPACE'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'status.podIP', 'targetKey': 'MY_POD_IP'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'spec.serviceAccountName',
                     'targetKey': 'MY_POD_SERVICE_ACCOUNT'}
                ],
                'resources': {
                    'requests': {},
                    'limits': {}
                },
                'capAdd': [],
                'capDrop': [],
                'image': image,
                'ports': [
                    {'containerPort': ports[0], 'type': 'containerPort', 'kind': 'ClusterIP', 'protocol': 'TCP'},
                ],
                'environment': {
                    'BUILD_ID': BUILD_ID,
                    'BUILD_P': 'test',
                    'PORTS': ports[0],
                    'application_name': workload['artfactid'],
                    'defaultZone': defaultZone
                },
                # 'readinessProbe': {
                #     'failureThreshold': 3, 'initialDelaySeconds': 120, 'periodSeconds': 2,
                #     'successThreshold': 2, 'tcp': True, 'timeoutSeconds': 2, 'type': 'probe',
                #     'path': None, 'httpHeaders': None, 'command': None, 'port': ports[0]
                # },
                'command': [
                    'java',
                    '-Djava.security.egd=file:/dev/./urandom',
                    '-jar',
                    '/APP.jar ',
                    '--server.port=${PORTS}',
                    '--spring.cloud.nacos.discovery.server-addr=${defaultZone}'
                ],
                'name': workload['artfactid'],
                'volumeMounts': [
                    {'readOnly': False, 'type': 'volumeMount', 'mountPath': '/data/logs/bex/execs/', 'name': 'logs'},
                ]
            }
        ],
        'scheduling': {
            'node': {
                'requireAll':
                    [
                        'ENV_EnvIronMent = %s' % ENV_EnvIronMent
                    ]
            }
        },
        'deploymentConfig': {
            'minReadySeconds': 0,
            'type': 'deploymentConfig',
            'revisionHistoryLimit': 10,
            'strategy': 'RollingUpdate',
            'maxSurge': 1,
            'maxUnavailable': 0
        },
        'name': workload['artfactid'],
        'volumes': [
            {'type': 'volume', 'name': 'logs',
             'hostPath': {'type': 'hostPathVolumeSource', 'kind': None, 'path': '/data_docker/logs/bex/execs/'}},
        ]
    }
    return ymal_data

def _get_nginx_yaml(ENV_EnvIronMent):
    """
        获取最新的 yaml
    :param ARTIFACTID:
    :param BUILD_ID:
    :param ENV_EnvIronMent:
    :param Types:
    :return:
    """
    # 获取相应内容
    workload_artfactid = "%s-nginx" % (_get_namespaceId(ENV_EnvIronMent))
    namespaceId = "%s-base" % (_get_namespaceId(ENV_EnvIronMent))
    image = "baoku/dockeropenresty:entosc-1.15.8.2-3"
    ports = [
        80,
        443
    ]
    defaultZone = _get_Dsentry_eureka(ENV_EnvIronMent)
    ymal_data = {
        'hostIPC': False,
        'hostNetwork': False,
        'hostPID': False,
        'paused': False,
        'type': 'workload',
        'namespaceId': namespaceId,
        'scale': 1,
        'dnsPolicy': 'ClusterFirst',
        'restartPolicy': 'Always',
        'labels': {},
        'containers': [
            {
                'initContainer': False,
                'restartCount': 0,
                'stdin': True,
                'stdinOnce': False,
                'tty': True,
                'type': 'container',
                'privileged': False,
                'allowPrivilegeEscalation': False,
                'readOnly': False,
                'runAsNonRoot': False,
                'namespaceId': namespaceId,
                'imagePullPolicy': 'Always',
                'environmentFrom': [
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'spec.nodeName', 'targetKey': 'MY_NODE_NAME'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'metadata.name', 'targetKey': 'MY_POD_NAME'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'metadata.namespace',
                     'targetKey': 'MY_POD_NAMESPACE'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'status.podIP', 'targetKey': 'MY_POD_IP'},
                    {'source': 'field', 'sourceKey': None, 'sourceName': 'spec.serviceAccountName',
                     'targetKey': 'MY_POD_SERVICE_ACCOUNT'}
                ],
                'resources': {
                    'requests': {},
                    'limits': {}
                },
                'capAdd': [],
                'capDrop': [],
                'image': image,
                'ports': [
                    {'containerPort': ports[0], 'type': 'containerPort', 'kind': 'ClusterIP', 'protocol': 'TCP'},
                    {'containerPort': ports[1], 'type': 'containerPort', 'kind': 'ClusterIP', 'protocol': 'TCP'},
                ],
                'environment': {
                    'defaultZone': defaultZone,
                },
                'livenessProbe': {
                    'failureThreshold': 3, 'initialDelaySeconds': 20, 'periodSeconds': 2,
                    'successThreshold': 1, 'tcp': True, 'timeoutSeconds': 2, 'type': 'probe',
                    'path': None, 'httpHeaders': None, 'command': None, 'port': ports[0]
                },
                'name': workload_artfactid
            }
        ],
        'scheduling': {
            'node': {
                'requireAll':
                    [
                        'ENV_EnvIronMent = %s' % ENV_EnvIronMent
                    ]
            }
        },
        'deploymentConfig': {
            'minReadySeconds': 0,
            'type': 'deploymentConfig',
            'revisionHistoryLimit': 10,
            'strategy': 'RollingUpdate',
            'maxSurge': 1,
            'maxUnavailable': 0
        },
        'name': workload_artfactid,
    }
    return ymal_data




