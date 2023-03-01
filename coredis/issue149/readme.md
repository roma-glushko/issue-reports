# Issue #149

Link: https://github.com/alisaifee/coredis/issues/149

## Reproducing

In order to reproduce the code reloading issue, you need to:

- start a new cluster and deploy the example there (make sure docker is up and running):

```sh
make cluster-start start
```

Open up Tilt UI and make sure all services have been successfully deployed

- Open the cluster in k9s and try to restart redis instances one by one and see whether heartbear and tracker are still working.
  At some point, either heartbeat or tracker (or both of them) will hang up and won't be able to recover by themselves even though the cluster will get healthy in short time.