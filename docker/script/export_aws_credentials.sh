#!/usr/bin/sh

PROFILE=${1:-personal}
REGION=${2:-us-west-2}

export AWS_ACCESS_KEY_ID=$(cat ~/.aws/credentials | grep -A 2 ${PROFILE} | sed '2q;d' | cut -d = -f 2 | tr -d '[:space:]' )
export AWS_SECRET_ACCESS_KEY=$(cat ~/.aws/credentials | grep -A 2 ${PROFILE} | sed '3q;d' | cut -d = -f 2 | tr -d '[:space:]' )
export AWS_DEFAULT_REGION=$REGION