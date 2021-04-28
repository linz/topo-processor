import s3fs

fs = s3fs.S3FileSystem(anon=False)

print(fs.ls("megantestbucket/"))
print(fs.ls("/home/bcheng/"))
