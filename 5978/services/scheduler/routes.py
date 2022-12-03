import logging
import uuid

from fastapi import Request, Response, status, APIRouter
from kubernetes_asyncio import client
from kubernetes_asyncio.client import models
from kubernetes_asyncio.client.api_client import ApiClient

from services.scheduler.config import Config

logger = logging.getLogger(__name__)

config = Config()
router = APIRouter()


async def create_worker_deployment(
        namespace: str,
        name: str,
        image: str,
        port: int = 8802,
) -> models.v1_deployment.V1Deployment:
    labels: dict[str, str] = {
        'app.kubernetes.io/component': 'worker',
        'app.kubernetes.io/part-of': 'sample5978',
    }

    container = client.V1Container(
        name="worker",
        image=image,
        ports=[
            client.V1ContainerPort(container_port=port),
        ],
        resources=client.V1ResourceRequirements(
            requests={"cpu": "100m", "memory": "200Mi"},
            limits={"cpu": "500m", "memory": "500Mi"},
        ),
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


@router.post("/worker/")
async def start_worker(
    request: Request,
) -> Response:
    await deploy_worker(
        namespace=config.namespace,
        worker_image=config.worker_image,
        worker_id=str(uuid.uuid4()),
    )

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.delete("/worker/{worker_id}/")
async def stop_worker(
    request: Request,
    worker_id: str,
) -> Response:
    await stop_worker(
        namespace=config.namespace,
        worker_id=worker_id,
    )

    return Response(status_code=status.HTTP_202_ACCEPTED)
