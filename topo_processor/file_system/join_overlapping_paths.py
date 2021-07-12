import difflib


def join_overlapping_paths(path_one: str, path_two: str) -> str:
    """This function take two paths which overlap and combines
    them into the one full path. For example:
    path_one: 's3://bucket/folder'
    path_two: 'bucket/folder/file'
    return: s3://bucket/folder/file'
    """
    sm = difflib.SequenceMatcher(None, path_one, path_two)
    _, part_two_index, size = sm.get_matching_blocks()[0]
    if part_two_index == 0:
        part_one, part_two = (path_one, path_two)
    else:
        part_one, part_two = (path_two, path_one)
    return part_one + part_two[size:]
