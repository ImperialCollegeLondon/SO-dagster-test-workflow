import os

from dagster import FilesystemIOManager, graph, op, repository, schedule
from dagster_docker import docker_executor

VALUE = int(os.environ["WORKFLOW_VAR"])

@op
def hello() -> int:
    return VALUE


@op
def goodbye(foo):
    if foo != VALUE:
        raise Exception("Bad io manager")
    return foo * 2


@graph
def my_graph():
    goodbye(hello())


my_job = my_graph.to_job(name="my_job_2")

my_step_isolated_job = my_graph.to_job(
    name="my_step_isolated_job",
    executor_def=docker_executor,
    resource_defs={"io_manager": FilesystemIOManager(base_dir="/tmp/io_manager_storage")},
)


@schedule(cron_schedule="* * * * *", job=my_job, execution_timezone="US/Central")
def my_schedule(_context):
    return {}


@repository
def deploy_docker_repository():
    return [my_job, my_step_isolated_job, my_schedule]
