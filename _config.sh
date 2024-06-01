#########################################################
# Configuration
#########################################################
# Directory of the application code | allowed characters: a-zA-Z0-9-_
export SRC=app

# NOTE: The bucket terraform-state must already exist in the AWS account
#       This should be defined on the command line for the best re-usability
export TERRAFORM_STATE_BUCKET=ticket-scout-terraform-state
# Terraform state identifier (must be unique) | allowed characters: a-zA-Z0-9-_
export TERRAFORM_STATE_IDENT=ticket-scout-backend

# Application config
export APP_IDENT=ticket-scout # Used to identify the application in AWS resources | allowed characters: a-zA-Z0-9-_
export APP_TIMEOUT=60 # seconds
export APP_MEMORY=128 # MB

echo "${AUTH0_DOMAIN}:AUTH0_DOMAIN"