import boto3
from botocore.client import Config
import zipfile
import mimetypes
import StringIO

def lambda_handler(event, context):
    s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
    
    build_bucket = s3.Bucket('kiranbuild.sgaslabs.net')
    portfolio_bucket = s3.Bucket('kiran.sgaslabs.net')
    
    #build_bucket.download_file('portfolio.zip', '/tmp/portfolio.zip')
    portfolio_zip = StringIO.StringIO()
    build_bucket.download_fileobj('kiranbuild.zip', portfolio_zip)

    with zipfile.ZipFile(portfolio_zip) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType':mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
            
    return 'Hello Guru'