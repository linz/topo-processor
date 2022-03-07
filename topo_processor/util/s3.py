
import boto3

from linz_logger import get_log




def bucket_name_from_path(path: str) -> str:
    path_parts = path.replace("s3://", "").split("/")
    return path_parts.pop(0)


def bucket_name_from_stack(stack_name: str) -> str:
    get_log().debug("stack_name", stack_name=stack_name)
    session = boto3.Session()
    cloudformation = session.resource('cloudformation')
    stack = cloudformation.Stack(stack_name)

    try:
        for output in stack.outputs:
            if output["OutputKey"] == "TempBucketName":
                get_log().debug("bucket_name", bucket_name=output["OutputValue"])
                return output["OutputValue"]
    except Exception as e:
        get_log().error("bucket_name_not_found", stackName=stack_name, error=e)
        raise e



def is_s3_path(path: str) -> bool:
    if path.startswith("s3://"):
        return True
    return False
