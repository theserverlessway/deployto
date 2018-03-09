# DeployTo

Simple Deployment Tool for AWS Services that is integrated with CloudFormation.

Deploying to AWS, especially during development, is often a hassle. Having to remember or copy together the names of your resources
and running various awscli (or other tools) commands is not productive.

DeployTo tries to solve this by doing two things:

1. Integrate with CloudFormation so you tell deployto the name of the resource in your CF template and it will figure out the actual name
2. Give you output that actually tells you whats happening during longer deployments, e.g. when deploying to ElasticBeanstalk

At the moment Lambda is supported as a deployment target, but more are to come in the future.

## Install

You can install DeployTo either through pip:

```
pip install deployto
```

or through whalebrew:

```
whalebrew install theserverlessway/deployto
```

## Deployment to Lambda

DeployTo requires you to put your deployment config into a config file. You can have several config files in your repo and just hand different ones to DeployTo depending on what you want to deploy

Following are all options available for Lambda deployment

```
stack: teststack # The stack to read CloudFormation resources from
service: lambda # The service to deploy to
paths:  # The paths to include in the ZipFile, more info in the packaging config below
 - 'code:'
s3: false # If you want to push the zipfile to an S3 Bucket before deploying (will create and remove the bucket automatically)
functions: # Limit which functions to deploy to with CF LogicalIds. By default deploys to all functions in the stack
  - LambdaFunction
publish: true # If a new version should be published for each function
```

If you name the config file `deployto.yml` it will be picked up automatically, otherwise you have to use the `-c` option:

```
deployto
deployto -c backend.yaml
```

## Packaging config

The `paths` config allows you to set which files or folders should be included where to in the zipfile. With DeployTo you can pick and choose from different paths and combine them together into a zipfile easily.

This makes it unnecessary for your team to copy together files and dependencies into a separate `build` folder and then zip that up. Simply tell DeployTo where to find which files and folders and it will zip it up in memory and deploy to Lambda.

The basic format for including files or folders is `FROM_PATH:TO_PATH`. When `FROM_PATH` is a file the `TO_PATH` will be treated as a file as well, unless it is empty. Following are a few examples how to include files and folders into DeployTo.

### Examples

Include the code folder (and put it into `code` in the zipfile as well)
```
paths:
 - code
```

Include the code folder but rename it to `other`

```
paths:
 - code:other
```

Include the `code` folders content in the root of the zipfile. As we're using `:` as a separator you have to put the path config between `''` otherwise it will be interpreted as yaml.

```
paths:
 - 'code:'
```

Include only one file from the code folder

```
paths:
 - 'code/index.py'
```

Include only one file from the code folder and rename it to another folder

```
paths:
 - 'code/index.py:other/events.py'
```

Include one file from the code folder put it in the root

```
paths:
 - 'code/index.py:'
```