from typing import Optional

from kubernetes_asyncio import client
from kubernetes_asyncio.client.api_client import ApiClient


async def create_worker_deployment(
    namespace: str,
    name: str,
    image: str,
    port: int = 8802,
    env: Optional[dict[str, str]] = None,
) -> client.V1Deployment:
    labels: dict[str, str] = {
        "app.kubernetes.io/component": "worker",
        "app.kubernetes.io/part-of": "sample5978",
    }

    env_vars: list[client.V1EnvVar] = (
        [
            client.V1EnvVar(
                name=name,
                value=value,
            )
            for name, value in env.items()
        ]
        if env
        else None
    )

    container = client.V1Container(
        name="worker",
        image=image,
        command=["python", "-m", "services.worker.main"],
        ports=[
            client.V1ContainerPort(container_port=port),
        ],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "200Mi"},
            limits={"cpu": "500m", "memory": "500Mi"},
        ),
        env=env_vars,
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels=labels),
        spec=client.V1PodSpec(containers=[container]),
    )

    spec = client.V1DeploymentSpec(
        replicas=1,
        template=template,
        selector={
            "matchLabels": labels,
        },
    )

    return client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(
            name=name,
            namespace=namespace,
            labels=labels,
        ),
        spec=spec,
    )


async def deploy_worker(namespace: str, worker_image: str, worker_id: str) -> None:
    async with ApiClient() as api_client:
        apps_api = client.AppsV1Api(api_client)

        deployment = await create_worker_deployment(
            namespace=namespace,
            name=f"worker-{worker_id}",
            image=worker_image,
            env={
                "WORKER_ID": worker_id,
                "WORKER_IMAGE": worker_image,
            },
        )

        apps_api.create_namespaced_deployment(
            namespace=namespace,
            body=deployment,
        )


async def stop_worker(namespace: str, worker_id: str) -> None:
    async with ApiClient() as api_client:
        apps_api = client.AppsV1Api(api_client)

        apps_api.delete_namespaced_deployment(
            namespace=namespace,
            name=f"worker-{worker_id}",
            body=client.V1DeleteOptions(
                propagation_policy="Background",
                grace_period_seconds=5,
            ),
        )
