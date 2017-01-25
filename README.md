lmdo
=========

*A simple CLI tool for developing microservices using AWS Lambda function (python2.7) and managing logistic of AWS resources*


Purpose
-------

The existing open source tool sets such as
[Apex](https://github.com/apex/apex) and
[Serverless](https://github.com/serverless/serverless) have all sorts
of limitations and too many abstractions. I understand tools are often opinionated but flexibility should be allowed. 

lmdo allows:
- Use cloud formation templates
- Use swagger for API Gateway
- Individually managing AWS resources
- Manage life cycles of AWS Lambda functions
- Bridge Django framework
- Tail Cloudwatch logs

Usage
-----

Installation

    $ sudo pip install lmdo

Create skeleton
    
    $ lmdo tpl

Package and upload Lambda function to S3

    $ lmdo lm

Create/Update CloudFormation and create Lambda function

    $ lmdo cf

Create/update API gateway and deploy stage

    $ lmdo api

Deploy the service in one step
    
    $ lmdo deploy

Delete the service and associated AWS assets

    $ lmdo destroy


Initiation
-----
To initiate your project
    $ lmdo init <project_name>
This will create a project folder and the sample lmdo.yml configuration file for you.

Note: Apart from the init command, all other lmdo commands need to be run at the same directory of the lmdo.yml file

To get a boiler plate from somewhere in github, run below command:
    $ lmdo bp fetch <url>
The boiler plate will then be copied from github to your current location without all the git folders or files

AWS Cloudformation
-----
To use cloudformation, you need to create a folder named 'cloudformation' in your project folder, so it looks like:
    <your-project>/cloudformation

The cloudformation template can be in any of .yml, .json or .template format as per AWS requirements. However, there has to be 
one master template and named `main.*` regardless you are using single template or nested stacks. 

If using nested stacks, you must provide S3 bucket in your lmdo.yml file under 'CloudformationBucket' as per AWS requirements.

For single template, if no S3 bucket provided, the template will be loaded from your local. 

If there are parameters, all parameters with their values must be provided in the file named 'params.json'. This file however 
won't be uploaded to S3 under all scenarios for security reasons.

If 'StackName' is provided in lmdo.yml, it'll be used to create the stack. Otherwise lmdo will use <user>-<stage>-<service-name>-service
to name your stack

AWS Lambda
-----
You can create standard lambda function and or use a bridging lambda function provided by lmdo to connect to your django app. Lmdo allows you to create any number of lambda functions.

1. Standard Python Lambda function
The invokable lambda function file needs to be placed on the top level of the project folder. The 'requirements.txt' file and 'vendored' folder is required under the project folder as well. All the pip installations will be installed in the 'vendored' folder.
Add below lines at the beginning of your lambda function file so all your modules can be found by AWS Lambda runtime:
import os
import sys

sys.path.append('/var/task')
file_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(file_path, "./"))
sys.path.append(os.path.join(file_path, "./vendored"))

To configure your lambda, enter an entry under 'Lambda' in your lmdo.yml:

    - S3Bucket: lambda.bucket.name        # mandatory, the bucket to load your package to
      Type: default                       # Optional, other types is django
      FunctionName: superman              # mandatory, the actual function name in AWS will have the format of <user>-<stage>-<service-name>-<FunctionName>
      Handler: handler.fly                # mandatory, define the handler function
      MemorySize: 128                     # optional, default to 128
      RoleArn: roleName                   # Either provide a role arn or assume role policy doc, the RolePolicyDocument takes preccedent
      RolePolicyDocument: path/to/policy  # Assume role Policy
      Runtime: python2.7                  # optional default to 'python2.7'
      Timeout: 180                        # optional default to 180
      VpcConfig:                          # optional, Lambda VPC configuration
          SecurityGroupIds:
              - string
              - string
          SubnetIds:
              - string
              - string
      EnvironmentVariables:              # optional, runtime environment variable
          MYSQL_HOST: localhost
          MYSQL_PASSWORD: secret
          MYSQL_USERNAME: admin
          MYSQL_DATABASE: lmdo
 
2. Django app
Same as standard lambda function, lmdo requires 'requirements.txt' file and 'vendored' folder for dependencies.

To config, add below entry in 'Lambda':

    - S3Bucket: lambda.bucket.name        # mandatory
      Type: django                        # Other types
      DisableApiGateway: False            # Optional, if set to True, the apigateway for Django app won't be created
      ApiBasePath: /path                  # Mandatory if apigateway to be created. Base resource path for django app
      FunctionName: superman              # mandatory
      MemorySize: 128                     # optional, default to 128
      RoleArn: roleName                   # Either provide a role arn or assume role policy doc, the RolePolicyDocument takes preccedent
      RolePolicyDocument: path/to/policy  # Assume role Policy
      Runtime: python2.7                  # optional default to 'python2.7'
      Timeout: 180                        # optional default to 180
      VpcConfig:                          # optional
          SecurityGroupIds:
              - string
              - string
          SubnetIds:
              - string
      EnvironmentVariables:                       # mandatory
          DJANGO_SETTINGS_MODULE: mysite.settings # mandatory
 

To deploy all the functions, run

    $ lmdo lm (create|update|delete)

To only deploy one function, run
    
    $ lmdo lm (create|update|delete) --function-name=blah



AWS API Gateway
-----
1. Standard API Gateway
Swagger template is used to create API Gateway, you will need to create a folder named 'swagger' under your project folder and name your swagger template as 'apigateway.json'.

In your swagger template, please name your version as '$version' and your title as '$title' so that Lmdo can update it during creation using the value of 'ApiGatewayName' in your lmdo.yml.

2. WSGI(Django) API
Lmdo automatically create a API Gateway resource if you have Django Lambda function configured using proxy. 

There will only be one API gateway created. Django api will be appended as part of the resource

You can create or delete a stage by running

    $ lmdo api create-stage <from_stage> <to_stage>
    or 
    $ lmdo api delete-stage <from_stage>

AWS S3
-----
Lmdo offers a simple command line to upload your local static asset into a S3 bucket. All you need to do is to configure 'AssetS3Bucket' and 'AseetDirectory' in your lmdo.yml, then run

    $ lmdo s3 sync

    
AWS Cloudwatch Logs
-----
You can tail any AWS cloudwatch group logs by running:

    $ lmdo logs tail <log_group_name> [-f | --follow] [--day=<int>] [--start-date=<datetime>] [--end-date=<datetime>]

--day value defines how many days ago the logs need to be retrieved or you specify a start date and/or end date for the log entries using format 'YYYY-MM-DD'

You can also tail logs of your lambda function in your project by running:

    $ lmdo logs tail function <function_name> [-f | --follow] [--day=<int>] [--start-date=<datetime>] [--end-date=<datetime>]

The <function_name> is the name you configure in your lmdo.yml

One step deploy
------
Alternatively, you can deploy and delete your entire service by running

    $ lmdo deloy 
    or
    $ lmdo destroy


