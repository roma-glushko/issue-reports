package main

import (
	"net/http"

	"github.com/TykTechnologies/tyk/log"
)

var logger = log.Get().WithField("prefix", "inject_headers")

func init() {
	logger.Info("inject headers plugin initialized")
}

func InjectHeaders(rw http.ResponseWriter, r *http.Request) { //nolint:all
	logger.Debug("inject headers middleware running")
}
