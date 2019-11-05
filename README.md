# rancher python api and jenkins
用于 jenkins 直接调用并生成 相应api

```bash
# 最新插件
pip3 install git+https://github.com/rancher/client-python.git@master
```

```Bash
python3 /data/base/rancher_python/index.py -ARTIFACTID ${ARTIFACTID} -BUILD_ID ${BUILD_ID}_${GIT_COMMIT} -ENV_EnvIronMent ${ENV_EnvIronMent} -Types xcauto_java -delete true
# 测试命令
python3 ./index.py -ARTIFACTID bex-user -BUILD_ID 3_68077a5b991da5aec531d93b4a5c566b8d7dfdad -ENV_EnvIronMent TEST -Types bex -delete true
```