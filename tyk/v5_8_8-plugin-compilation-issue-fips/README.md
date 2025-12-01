# Tyk v5.8.8 (fips) - Plugin Compilation Issue

The error text:

```text
Could not load Go-plugin" error="plugin.Open(\"/opt/tyk-gateway/middleware/myplugin_v5.8.8_linux_amd64.so\"): 
plugin was built with a different version of package internal/goarch (previous failure)" 
mwPath=/opt/tyk-gateway/middleware/myplugin.so mwSymbolName=MyEntrypoint
```

## Reproducing

- Start the docker-compose-based environment via `make run`
- Wait until Tyk Gateway is fully started
- Check the logs of the gateway container. You should see the error mentioned above shortly after the startup.