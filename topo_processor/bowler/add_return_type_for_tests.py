from bowler import Query


def main():
    (Query().select_function("test_upload_local").add_argument("auto_param", '"default_value"', positional=True).execute())
