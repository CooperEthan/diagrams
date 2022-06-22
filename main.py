from diagrams import Cluster, Diagram
from diagrams.aws.compute import ECS
from diagrams.aws.database import Elasticache, RDS
from diagrams.aws.network import ELB
from diagrams.aws.network import Route53
from diagrams.aws.storage import SimpleStorageServiceS3Bucket
from diagrams.aws.compute import Lambda
from diagrams.aws.network import CloudFront
from diagrams.aws.database import Dynamodb


with Diagram("Clustered Web Services", show=False):
    dns = Route53("dns")
    lb = ELB("elb")

    with Cluster("Services"):
        svc_group = [ECS("Web1"),
                     ECS("Web2"),
                     ECS("Web3")]

    with Cluster("op_db"):
        db_op = RDS("op_db")
    with Cluster("pmp_db"):
        db_pmp = RDS("pmp_db")
    with Cluster("core"):
        db_core = RDS("core")

    with Cluster("CDN"):
        cdn = CloudFront("CDN")

    with Cluster("s3"):
        static = SimpleStorageServiceS3Bucket("static_files")

    with Cluster("Auth_lambda"):
        auth_lambda = Lambda("Auth_lambda")

    with Cluster("dynamodb"):
        dynamodb = Dynamodb("dynamodb_auth_table")

    redis1 = Elasticache("redis")
    redis2 = Elasticache("redis")

    dns >> cdn
    cdn >> static
    cdn >> lb >> svc_group
    cdn >> auth_lambda
    auth_lambda >> dynamodb
    # dynamodb >> auth_lambda
    # auth_lambda >> cdn
    cdn >> dns
    svc_group >> redis1
    svc_group >> redis2
    redis1 >> db_op
    redis2 >> db_pmp
    redis1 >> db_core



