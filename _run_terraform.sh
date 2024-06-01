# NOTE: Do not call this directly - it is called indirectly from ./deploy_single_env.sh or ./deploy.sh

#########################################################
# Create code hash
#########################################################
export CODE_HASH_FILE=${SRC}_code_hash.txt
docker run -v $(pwd):/workdir -w /workdir alpine sh -c \
  "apk add --no-cache findutils coreutils && find ./requirements.txt ./Dockerfile ./${SRC} -type f \( -name '*.py' -o -name 'Dockerfile' -o -name 'requirements.txt' \) -not -path '*/.*' -exec md5sum {} \\; | sort | md5sum | cut -d ' ' -f1 > terraform/${CODE_HASH_FILE}"

#########################################################
# Generate the backend.tf file
#########################################################

cd terraform
rm -fR .terraform
rm -fR .terraform.lock.hcl
cat > backend.tf << EOF
terraform {
  backend "s3" {
    bucket = "${TERRAFORM_STATE_BUCKET}"
    key    = "terraform-${TERRAFORM_STATE_IDENT}.tfstate"
    region = "us-east-1"
  }
}
EOF

#########################################################
# Generate the remote_backend.tf file for access
# to the shared infrastructure elements
#########################################################

#cat > remote_backend.tf << EOF
# data "terraform_remote_state" "core" {
#   backend = "s3"
#   config = {
#     bucket = "${TERRAFORM_STATE_BUCKET}"
#     key    = "terraform.tfstate"
#     region = "us-east-1"
#   }
# }
#EOF

#########################################################
# Run Terraform
#########################################################
export TF_VAR_environment=${ENVIRONMENT}
export TF_VAR_src=${SRC}
export TF_VAR_app_ident=${APP_IDENT}
export TF_VAR_code_hash_file=${CODE_HASH_FILE}
export TF_VAR_app_timeout=${APP_TIMEOUT}
export TF_VAR_app_memory=${APP_MEMORY}
export TF_VAR_api_stage_name=${ENVIRONMENT}
#export TF_VAR_api_domain=${API_DOMAIN}
#export TF_VAR_api_root_domain=${API_ROOT_DOMAIN}

# Initialize terraform
terraform init

if [ "$FLAG_DESTROY" = true ] ; then
    echo "Destroying resources..."
    terraform destroy -auto-approve
else
    echo "Creating resources..."
    terraform apply -auto-approve
fi
