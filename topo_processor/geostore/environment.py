import boto3


def is_production() -> bool:
    try:
        arn_assumed = boto3.client("sts").get_caller_identity().get("Arn")
        if arn_assumed:
            if "nonprod" in arn_assumed:
                return False
            else:
                return True
        else:
            raise Exception("AWS assumed role could not be retrieved.")
    except Exception as e:
        raise Exception("An issue has occured while trying to get the AWS identity", e)
