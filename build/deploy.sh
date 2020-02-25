#!/bin/bash

# Uncomment below if you have multiple aws profiles configured
export AWS_PROFILE=myawsaccount

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
                          --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

#$(jq -r 'to_entries[] | "\(.key)=\(.value)"' buildfiles/config.json)
