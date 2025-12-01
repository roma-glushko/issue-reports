ARG TYK_VERSION=v5.8.8
ARG TYK_PLUGIN_COMPILER_VERSION=v5.8.8

FROM datarobotdev/mirror_tykio_tyk-plugin-compiler-ee:${TYK_PLUGIN_COMPILER_VERSION} AS plugin-build-stage

COPY plugins /go/src/plugins

WORKDIR /plugin-source/

ENV GOEXPERIMENT=boringcrypto \
    GOOS=linux \
    GOARCH=amd64

RUN set -e && for d in $(find /go/src/plugins/ -mindepth 1 -maxdepth 1 -type d); do \
    dir_name=$(basename "$d"); \
    cd "$d"; \
    cp *.go go.mod go.sum /plugin-source/; \
    /build.sh "$dir_name.so" "_$(date +%s)"; \
    cp /plugin-source/*.so /go/src/plugins/; \
    rm /plugin-source/*.*; \
    cd ../; \
done

FROM datarobotdev/mirror_tykio_tyk-gateway-fips:${TYK_VERSION} AS runtime-stage

COPY --from=plugin-build-stage /go/src/plugins/*.so /opt/tyk-gateway/middleware
COPY api.json /opt/tyk-gateway/apps/

ENV TYK_GW_HASHKEYFUNCTION=sha256

WORKDIR /opt/tyk-gateway/

ENTRYPOINT ["/opt/tyk-gateway/tyk"]

CMD ["--conf=/opt/tyk-gateway/tyk.conf"]
