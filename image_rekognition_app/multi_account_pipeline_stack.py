from aws_cdk import (
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_codebuild as codebuild,
    aws_iam as iam,
    pipelines,
    Stack,
    SecretValue
)
from constructs import Construct

class MultiAccountPipelineStack(Stack):
    def __init__(self, scope: Constriuct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.GitHubSourceAction(
            action_name="GitHub_Source",
            owner="amitraikkr760@gmail.com",
            repo="",
            oauth_token=ScretValue.secrets_manager("github-token"),
            output=source_output,
            branch="main"
        )

        build_project = codebuild.PipelineProject(self, "BuildProject",
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged=True
            ),
            build_spec=codebuild.BuildSpec.from_source_filename('buildspec.yml')
        )

        build_output = codepipeline.Artifact()
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_output,
            outputs=[build_output]
        )

        pipeline = codepipeline.Pipeline(self, "Pipeline",
            stages=[
                codepipeline.stageProps(
                    stage_name="Source",
                    action=[source_action]
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[build_action]
                )
            ]
        )

        dev_stage = pipelines.CdkStage(self, "DeployToDeveloper",
            stack_name="DevStack",
            env={'account':"DEV_ACCOUNT", 'region':'us-east-2'}
        )

        prod_stage = pipelines.CdkStage(self, "DeployToProduction",
            stack_name="ProdStack",
            env={'account':'PROD_ACCOUNT', 'region':'us-east-2'}
        )

        pipeline.add_stage(dev_stage)
        pipeline.add_stage(prod_stage)

        pipeline.add_to_role_policy(iam.PolicyStatement(
            action=["sts:AssumeRole"],
            resources=["arn:aws:iam::PROD_ACCOUNT:role/CrossAccountRoleForDev"]
        ))