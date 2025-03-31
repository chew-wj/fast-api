variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-southeast-1"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "my-eks-cluster"
}

variable "cluster_version" {
  description = "Kubernetes version to use for the EKS cluster"
  type        = string
  default     = "1.27"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "availability_zones" {
  description = "List of availability zones"
  type        = list(string)
  default     = ["ap-southeast-1a", "ap-southeast-1b", "ap-southeast-1c"]
}

variable "node_groups" {
  description = "Map of node groups to create"
  type = map(object({
    desired_size = number
    min_size     = number
    max_size     = number
    instance_types = list(string)
  }))
  default = {
    general = {
      desired_size    = 2
      min_size        = 1
      max_size        = 4
      instance_types  = ["t3.medium"]
    }
  }
}

variable "tags" {
  description = "A map of tags to add to all resources"
  type        = map(string)
  default = {
    Environment = "dev"
    Terraform   = "true"
  }
}

variable "acm_certificate_arn" {
  description = "ARN of ACM certificate to use with ALB"
  type        = string
  default     = ""  # Replace with your certificate ARN
}

variable "waf_rate_limit" {
  description = "Rate limit for WAF rules (requests per 5 minutes per IP)"
  type        = number
  default     = 2000
}

variable "enable_shield_advanced" {
  description = "Enable AWS Shield Advanced protection"
  type        = bool
  default     = false
} 