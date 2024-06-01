#!/bin/bash

set -e

####################################################################################################
# Check if Docker is running
####################################################################################################
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

####################################################################################################
# Determine Flags
####################################################################################################
while getopts "d" opt; do
  case ${opt} in
    d)
       export FLAG_DESTROY=true
       ;;
    \?)
       echo "Invalid option: -$OPTARG" 1>&2
       exit 1
       ;;
  esac
done
shift $((OPTIND -1))

####################################################################################################
# Determine Environment
####################################################################################################
# If the provided environment is not one of the allowed values, exit the script
if [[ "${ENVIRONMENT}" != "staging" && "${ENVIRONMENT}" != "prod" ]]; then
    echo "Invalid environment: ${ENVIRONMENT}. Allowed values are 'staging', or 'prod'."
    exit 1
fi

echo "ENVIRONMENT: ${ENVIRONMENT}"
echo "FLAG_DESTROY: ${FLAG_DESTROY}"

####################################################################################################
# Load the configuration variables
####################################################################################################
source _config.sh

if [ -n "$ENVIRONMENT" ]; then
  # Modify the environment variables for this deployment
  export TERRAFORM_STATE_IDENT=${TERRAFORM_STATE_IDENT}-${ENVIRONMENT}
  export APP_IDENT="${APP_IDENT}-${ENVIRONMENT}"
fi

####################################################################################################
# Run Terraform
####################################################################################################
./_run_terraform.sh
