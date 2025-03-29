module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = var.cluster_name
  cluster_version = var.cluster_version

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  cluster_endpoint_public_access = true

  eks_managed_node_groups = {
    for name, group in var.node_groups : name => {
      desired_size = group.desired_size
      min_size     = group.min_size
      max_size     = group.max_size

      instance_types = group.instance_types

      labels = {
        Environment = var.environment
      }

      taints = []
    }
  }

  tags = var.tags
}

# Add EKS cluster security group rules
resource "aws_security_group_rule" "eks_cluster_ingress" {
  type                     = "ingress"
  from_port               = 443
  to_port                 = 443
  protocol                = "tcp"
  cidr_blocks             = ["0.0.0.0/0"]
  security_group_id       = module.eks.cluster_security_group_id
  description            = "Allow inbound HTTPS traffic"
}

# Add EKS node group security group rules
resource "aws_security_group_rule" "eks_node_ingress" {
  type                     = "ingress"
  from_port               = 30000
  to_port                 = 32767
  protocol                = "tcp"
  cidr_blocks             = ["0.0.0.0/0"]
  security_group_id       = module.eks.node_security_group_id
  description            = "Allow inbound NodePort traffic"
} 