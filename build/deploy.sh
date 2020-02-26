#!/bin/bash

export AWS_PROFILE=myawsaccount

CONFIG_PATH=s3://anitaernszt-website/deployment/dev-config.json

aws s3 cp $CONFIG_PATH tmp/deploy-cfg.json

# CHANGE THIS BUCKET
S3_BUCKET=anitaernszt-website
INPUT_FILE=schemas/mysite-SAM.yaml
OUTPUT_FILE=compiled-schema.yaml
STACK_NAME=mywebsite-api

# remove any old compiled schemas
rm -f $OUTPUT_FILE

aws cloudformation package --template-file $INPUT_FILE \
                           --output-template-file $OUTPUT_FILE \
                           --s3-bucket $S3_BUCKET

aws cloudformation deploy --template-file $OUTPUT_FILE \
                          --stack-name $STACK_NAME \
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
                          --parameter-overrides $(jq -r 'to_entries[] | "\(.key)=\(.value)"' tmp/deploy-cfg.json)
