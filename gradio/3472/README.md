# Issue #3472

Link: https://github.com/gradio-app/gradio/issues/3472

## Reproducing

- Spin up the example via `make up`. Make sure all containers have been started successfully and green
- Head over to `http://localhost:8080/subpath/ID/app/ID/`

### Actual Behavior

The gradio page is broken. The app tries to:
- access its configuration endpoint on `http://localhost:8080/config` (doesn't respect the subpath)
- access its CSS assets like `http://localhost:8080/assets/index-DQ_Hu8W_.css` (doesn't respect the subpath)

### Expected Behavior

Gradio loads without errors on serving from a subpath.