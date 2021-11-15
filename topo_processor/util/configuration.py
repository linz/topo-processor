from dotenv import dotenv_values

configuration = dotenv_values(".env")

lds_cache_bucket = configuration["LDS_CACHE_BUCKET"]
lds_cache_read_role = configuration["LDS_CACHE_READ_ROLE"]
lds_cache_local_tmp_folder = configuration["LDS_CACHE_LOCAL_TMP_FOLDER"]
