# Issue #5978

Link: https://github.com/tilt-dev/tilt/issues/5978

## Reproducing

In order to reproduce the code reloading issue, you need to:

- Run `make cluster-start` (make sure you have k3d installed)
- Run `tilt up` to deploy the environment. Wait until the scheduler pod is ready
- Run `curl --location --request POST 'localhost:8801/worker/5479/'` to create a new worker deployment
- Edit any of `service/*` files. I was adding a dummy comment to `services/scheduler/config.py`
- Inspect the content of scheduler's copy of the file you have edited. The edition should be applied. 
  Now do the same with the worker pod. You will see that the change was not applied there. This is how you can miss an update.