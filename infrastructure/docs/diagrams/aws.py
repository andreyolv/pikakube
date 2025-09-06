from diagrams import Diagram, Cluster
from diagrams.aws.network import NATGateway, VPC
from diagrams.aws.compute import EKS
from diagrams.k8s.compute import Pod
from diagrams.generic.blank import Blank

with Diagram("AWS Architecture", show=False, outformat="png", direction="TB"):
    with Cluster("VPC\nCIDR: 10.0.0.0/16"):
        vpc_icon = VPC("VPC")

        nat_gateway = NATGateway("NAT Gateway")

        with Cluster("Private Subnet A\nCIDR:10.0.1.0/24\nAZ:a") as subnet_a:
            eks_cluster = EKS("EKS Cluster")
            pod = Pod("Pod")

            subnet_a_node = Blank("")
            subnet_a_node >> nat_gateway

        with Cluster("Private Subnet B\nCIDR:10.0.2.0/24\nAZ:b") as subnet_b:
            Blank("")

        with Cluster("Private Subnet C\nCIDR:10.0.3.0/24\nAZ:c") as subnet_c:
            Blank("")