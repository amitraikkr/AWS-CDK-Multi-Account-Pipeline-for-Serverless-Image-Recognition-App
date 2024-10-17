<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AWS CDK Multi-Account Pipeline for Serverless Image Recognition</title>
</head>
<body>

<h1>AWS CDK Multi-Account Pipeline for Serverless Image Recognition with Lambda, S3, and Rekognition</h1>

<p>
This repository provides a comprehensive guide to setting up a multi-account CI/CD pipeline using 
<a href="https://aws.amazon.com/cdk/" target="_blank">AWS CDK</a> for deploying a serverless image recognition 
application. The project automates infrastructure deployments across <strong>development</strong> and 
<strong>production</strong> environments, ensuring consistency and scalability using AWS services such as Lambda, S3, Rekognition, 
DynamoDB, and CodePipeline.
</p>

<h2>Project Overview</h2>
<p>
The goal of this project is to showcase how to build a <strong>multi-account CI/CD pipeline</strong> using 
AWS CDK to manage and deploy resources for an <strong>image recognition</strong> application. 
The pipeline integrates with GitHub for source control and deploys Lambda functions, S3 buckets, 
and DynamoDB tables for processing images using AWS Rekognition.
</p>

<h2>Key Features</h2>
<ul>
  <li>Fully automated CI/CD pipeline using AWS CodePipeline and CodeBuild.</li>
  <li>Serverless image recognition leveraging AWS Rekognition for detecting objects and labels in images.</li>
  <li>Multi-account setup with deployments to both development and production environments.</li>
  <li>Cross-account role management for secure deployments between accounts.</li>
  <li>GitHub integration for source control and continuous deployment.</li>
</ul>

<h2>Architecture Overview</h2>
<p>The following AWS services are used in this project:</p>
<ul>
  <li><strong>AWS Lambda:</strong> Processes images by calling AWS Rekognition for label detection.</li>
  <li><strong>Amazon S3:</strong> Stores the uploaded images and triggers Lambda functions on object creation.</li>
  <li><strong>Amazon Rekognition:</strong> Performs image analysis and detects objects or labels in images.</li>
  <li><strong>Amazon DynamoDB:</strong> Stores the results of the image analysis, such as detected labels.</li>
  <li><strong>AWS CodePipeline:</strong> Manages the CI/CD pipeline for deploying infrastructure and Lambda code.</li>
  <li><strong>AWS CodeBuild:</strong> Builds the application and synthesizes the CDK app for deployment.</li>
</ul>

<h2>Pre-requisites</h2>
<ul>
  <li>AWS account with sufficient privileges to create and manage resources.</li>
  <li>CDK toolkit installed (<code>npm install -g aws-cdk</code>).</li>
  <li>AWS CLI configured on your machine.</li>
  <li>GitHub account for repository integration.</li>
</ul>

<h2>Installation Instructions</h2>
<ol>
  <li>Clone the repository to your local machine:</li>
  <pre><code>git clone https://github.com/YourGitHubUsername/YourRepositoryName.git</code></pre>
  
  <li>Install dependencies for Lambda function (if needed):</li>
  <pre><code>cd lambda && npm install</code></pre>
  
  <li>Install project dependencies:</li>
  <pre><code>npm install</code></pre>

  <li>Configure AWS credentials:</li>
  <pre><code>aws configure</code></pre>

  <li>Deploy the resources in your development account:</li>
  <pre><code>cdk deploy</code></pre>
</ol>

<h2>Usage</h2>
<ol>
  <li>Upload an image to the S3 bucket created by the stack.</li>
  <li>Lambda function is triggered to process the image using Rekognition.</li>
  <li>Results are stored in DynamoDB, and you can query the detected labels and objects.</li>
</ol>

<h2>Contributing</h2>
<p>Contributions are welcome! Please fork this repository and submit a pull request with your improvements.</p>

<h2>Follow Me</h2>
<p>
For more content like this, follow me on:
<ul>
  <li><a href="https://medium.com/@amitraikkr" target="_blank">Medium</a></li>
  <li><a href="www.linkedin.com/in/amitraikkr" target="_blank">LinkedIn</a></li>
</ul>
</p>

</body>
</html>