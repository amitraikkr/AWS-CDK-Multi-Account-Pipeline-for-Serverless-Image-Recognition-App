from aws_cdk import (
    Stack,
    pipelines,
    aws_secretsmanager as secretsmanager,
    aws_s3 as s3,
    aws_kms as kms,
    aws_iam as iam,
    SecretValue,
    Environment,
    Stage,
)
from constructs import Construct
from image_rekognition_app.image_rekognition_app_stack import ImageRekognitionAppStack
from aws_cdk.aws_codebuild import BuildEnvironment, LinuxBuildImage, ComputeType


class MultiAccountPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Fetch GitHub token from AWS Secrets Manager
        github_secret = secretsmanager.Secret.from_secret_name_v2(
            scope=self,
            id="github_secret",
            secret_name="github-token"  # Ensure this matches your secret name
        )

        # Define the CodeBuild environment for the pipeline
        code_build_options = pipelines.CodeBuildOptions(
            build_environment=BuildEnvironment(
                build_image=LinuxBuildImage.STANDARD_5_0,
                compute_type=ComputeType.SMALL,
            )
        )

        # Source Stage (GitHub)
        source_output = pipelines.CodePipelineSource.git_hub(
            repo_string="amitraikkr/AWS-CDK-Multi-Account-Pipeline-for-Serverless-Image-Recognition-App",
            branch="main",
            authentication=github_secret.secret_value_from_json("github-token")
        )

        # Define the pipeline with crossAccountKeys enabled
        pipeline = pipelines.CodePipeline(self, "Pipeline",
            synth=pipelines.ShellStep("Synth",
                input=source_output,
                commands=[
                    "npm install -g aws-cdk",
                    "pip install -r requirements.txt",
                    "cdk synth"
                ],
                primary_output_directory="cdk.out",
            ),
            code_build_defaults=code_build_options,
            docker_enabled_for_synth=True,
            cross_account_keys=True,  # Enable cross-account artifact encryption
        )

        # Define the application stage for Dev
        dev_stage = pipeline.add_stage(
            DeployStage(self, "DeployToDev",
                env=Environment(account='886436951561', region='us-east-2')  # Dev account ID and region
            )
        )

        # Define the Prod Stage
        prod_stage = pipeline.add_stage(
            DeployStage(self, "DeployToProd",
                env=Environment(account='741448924184', region='us-east-2')  # Prod account ID and region
            )
        )


class DeployStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Define your application stack to be deployed in this stage (for example, Image Rekognition App)
        app_stack = ImageRekognitionAppStack(self, "ImageRekognitionAppStack")