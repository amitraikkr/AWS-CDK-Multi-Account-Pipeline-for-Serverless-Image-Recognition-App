#!/usr/bin/env python3
import os

import aws_cdk as cdk

from image_rekognition_app.image_rekognition_app_stack import ImageRekognitionAppStack

app = cdk.App()
ImageRekognitionAppStack(app, "ImageRekognitionAppStackv2")

app.synth()
