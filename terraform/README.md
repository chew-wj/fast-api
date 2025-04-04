# AWS EKS Infrastructure with Terraform

This directory contains Terraform configurations to set up an AWS EKS cluster with networking components.

## Prerequisites

- Terraform >= 1.0.0
- AWS CLI configured with appropriate credentials
- kubectl installed
- AWS account with appropriate permissions

## Usage

1. Configure your AWS credentials:
   ```bash
   aws configure
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review the planned changes:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

5. Configure kubectl to use the new cluster:
   ```bash
   aws eks update-kubeconfig --region <region> --name <cluster-name>
   ```

## Important Notes

- State file is configured to be stored in S3 (uncomment and configure the backend block in main.tf)
- Default region is set to us-west-2 (modify in variables.tf if needed)
- Node groups are configured with t3.medium instances by default

## Security Considerations

- The EKS cluster endpoint is publicly accessible
- Node groups are placed in private subnets
- Security groups are configured to allow necessary traffic
- Consider enabling encryption at rest for the EKS cluster
- Review and adjust security group rules based on your requirements

## Cost Considerations

- NAT Gateway usage will incur costs
- EKS cluster costs will be charged per hour
- Node group instances will be charged based on the selected instance types
- Consider using spot instances for non-production workloads

## Maintenance

- Regularly update the Kubernetes version
- Monitor and adjust node group sizes based on workload
- Keep Terraform and provider versions up to date
- Review and update security group rules as needed 