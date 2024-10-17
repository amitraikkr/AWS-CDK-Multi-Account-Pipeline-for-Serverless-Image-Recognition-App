from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    aws_s3 as s3,
    aws_iam as iam,
    aws_s3_notifications as s3n,
    RemovalPolicy,
    Duration
)
from constructs import Construct

class ImageRekognitionAppStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the S3 bucket with BlockPublicAccess disabled (or configured to allow specific policies)
        bucket = s3.Bucket(self, "ImageBucket",
            versioned= True,
            removal_policy= RemovalPolicy.DESTROY,
            bucket_name="imagerekognitionbucket",
            auto_delete_objects= True
        )

        # Add necessary permissions to the bucket policy (allowing public policies but being careful with public access)
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                actions=["s3:PutObject", "s3:GetObject"],
                resources=[f"{bucket.bucket_arn}/*"],
                principals=[iam.AccountPrincipal("886436951561")]  # Update this if you need to restrict access to specific roles
            )
        )

        # Create the DynamoDB table to store Rekognition results
        table = dynamodb.Table(self, "RekognitionResults",
            partition_key=dynamodb.Attribute(
                name= "ImageID", 
                type= dynamodb.AttributeType.STRING
            ),
            removal_policy=RemovalPolicy.DESTROY,
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )

        
        # Define the Lambda function
        rekognition_lambda = _lambda.Function(self, "RekognitionLambda",
            runtime=_lambda.Runtime.NODEJS_18_X,
            handler="rekognition.handler",
            code=_lambda.Code.from_asset("lambda"),
            memory_size=1024,
            timeout=Duration.seconds(300),
            environment={
                "TABLE_NAME": table.table_name,
                "BUCKET_NAME": bucket.bucket_name
                }
        )

        # Grant the Lambda function read/write access to the S3 bucket
        bucket.grant_read_write(rekognition_lambda)

        # Add necessary IAM policies for the Lambda function to use Rekognition
        rekognition_lambda.add_to_role_policy(
            iam.PolicyStatement(
                actions=["rekognition:DetectLabels"],
                resources=["*"]  # You can restrict this to specific resources if needed
            )
        )

        # Grant the Lambda function full access to the DynamoDB table
        table.grant_full_access(rekognition_lambda)

        # Add an event notification to trigger the Lambda function when an object is created in the S3 bucket
        bucket.add_event_notification(
            s3.EventType.OBJECT_CREATED, 
            s3n.LambdaDestination(rekognition_lambda)
        )

