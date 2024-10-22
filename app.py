#!/usr/bin/env python3
import os

import aws_cdk as cdk

from image_rekognition_app.image_rekognition_app_stack import ImageRekognitionAppStack
#from image_rekognition_app.multi_account_pipeline_stack import MultiAccountPipelineStack

app = cdk.App()
ImageRekognitionAppStack(app, "ImageRekognitionAppStackv2")

# MultiAccountPipelineStack(app, "MultiAccountPipelineStack", 
#     env={'account':'886436951561', 'region':'us-east-2'}
# ) 

app.synth()
