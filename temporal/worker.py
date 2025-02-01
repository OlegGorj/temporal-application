from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    # import sentry_sdk
    from temporalio import activity, workflow
    from temporalio.client import Client
    from temporalio.worker import Worker
    from config import config

    import asyncio
    from dataclasses import dataclass
    from datetime import timedelta
    import concurrent.futures
    import logging
    import os


workflow.logging.basicConfig(level=workflow.logging.DEBUG)

async def main():
    """
    Main function to start the Temporal Worker
    """
    attrs = vars(config.temporal_workflow_config)
    logging.debug(", ".join("%s: %s" % item for item in attrs.items()))

    _appcode_onboard_config = config.temporal_workflow_config.get_workflow_config("appcode_onboard_worker")
    try:
        _namespace = _appcode_onboard_config["namespace"]
        if not _namespace:  # set to default namespace if not provided
            _namespace = config.temporal_config.TEMPORAL_NAMESPACE

        _task_queue = _appcode_onboard_config["task_queue"]

        _max_concurrent_activities = _appcode_onboard_config["max_concurrent_activities"]
        if not _max_concurrent_activities:
            _max_concurrent_activities = 5

        client = await Client.connect(
            f"{config.temporal_config.TEMPORAL_SERVER_HOST}:{config.temporal_config.TEMPORAL_SERVER_PORT}",
            namespace=_namespace,
            tls=config.temporal_config.TEMPORAL_TLS_ENABLED,
        )
        worker = Worker(
            client,
            task_queue=_task_queue,
            workflows=[
            ],
            activities=[
            ],
            debug_mode=True,
            activity_executor=concurrent.futures.ThreadPoolExecutor(
                max_workers=_max_concurrent_activities
            ),
            max_concurrent_activities=_max_concurrent_activities,
        )
        await worker.run()

    except Exception as e:
        raise e


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

