



def create_k8s_cluster_mock_log():
    post_log(f'eksctl version 0.194.0 🚀', run_id=port_env_context["runId"])
    post_log(f'using region us-east-1 🌍', run_id=port_env_context["runId"])
    post_log(f'setting availability zones to [us-east-1a us-east-1b] 🌐', run_id=port_env_context["runId"])
    post_log(f'subnets for us-east-1a - public:192.168.0.0/19 private:192.168.64.0/19 🏙️',
             run_id=port_env_context["runId"])
    post_log(f'subnets for us-east-1b - public:192.168.32.0/19 private:192.168.96.0/19 🌆',
             run_id=port_env_context["runId"])
    post_log(f'nodegroup "ng-598412f9" will use "" [AmazonLinux2/1.30] 🐧', run_id=port_env_context["runId"])
    post_log(f'using Kubernetes version 1.30 🧑‍💻', run_id=port_env_context["runId"])
    post_log(f'creating EKS cluster "{cluster_name}" in "us-east-1" region with managed nodes 🎉',
             run_id=port_env_context["runId"])
    post_log(f'will create 2 separate CloudFormation stacks for cluster itself and the initial managed nodegroup 📦',
             run_id=port_env_context["runId"])
    post_log(
        f'if you encounter any issues, check CloudFormation console or try "eksctl utils describe-stacks --region=us-east-1 --cluster={cluster_name}" 🛠️',
        run_id=port_env_context["runId"])
    post_log(
        f'Kubernetes API endpoint access will use default of {{publicAccess=true, privateAccess=false}} for cluster "{cluster_name}" in "us-east-1" 🌐',
        run_id=port_env_context["runId"])
    post_log(f'CloudWatch logging will not be enabled for cluster "{cluster_name}" in "us-east-1" 📉',
             run_id=port_env_context["runId"])
    post_log(
        f'you can enable it with "eksctl utils update-cluster-logging --enable-types={{SPECIFY-YOUR-LOG-TYPES-HERE (e.g. all)}} --region=us-east-1 --cluster={cluster_name}" 🔧',
        run_id=port_env_context["runId"])
    post_log(f'default addons coredns, vpc-cni, kube-proxy were not specified, will install them as EKS addons 🛠️',
             run_id=port_env_context["runId"])
    post_log(f'building cluster stack "eksctl-{cluster_name}-cluster" 🏗️', run_id=port_env_context["runId"])
    post_log(f'deploying stack "eksctl-{cluster_name}-cluster" 📤', run_id=port_env_context["runId"])
    post_log(f'waiting for CloudFormation stack "eksctl-{cluster_name}-cluster" ⏳', run_id=port_env_context["runId"])
    post_log(f'creating addon ➕', run_id=port_env_context["runId"])
    post_log(f'successfully created addon ✅', run_id=port_env_context["runId"])
    post_log(
        f'recommended policies were found for "vpc-cni" addon, but since OIDC is disabled on the cluster, eksctl cannot configure the requested permissions 🚨',
        run_id=port_env_context["runId"])
    post_log(f'creating addon ➕', run_id=port_env_context["runId"])
    post_log(f'successfully created addon ✅', run_id=port_env_context["runId"])
    post_log(f'building managed nodegroup stack "eksctl-{cluster_name}-nodegroup-ng-598412f9" 🏗️',
             run_id=port_env_context["runId"])
    post_log(f'deploying stack "eksctl-{cluster_name}-nodegroup-ng-598412f9" 📤', run_id=port_env_context["runId"])
    post_log(f'waiting for CloudFormation stack "eksctl-{cluster_name}-nodegroup-ng-598412f9" ⏳',
             run_id=port_env_context["runId"])
    post_log(f'waiting for the control plane to become ready 🔄', run_id=port_env_context["runId"])
    post_log(f'saved kubeconfig as "/home/dan/.kube/config" 📄', run_id=port_env_context["runId"])
    post_log(f'all EKS cluster resources for "{cluster_name}" have been created 🎉', run_id=port_env_context["runId"])
    post_log(f'created 1 managed nodegroup(s) in cluster "{cluster_name}" ✅', run_id=port_env_context["runId"])
    post_log(f'nodegroup "ng-598412f9" has 3 node(s) 🖥️', run_id=port_env_context["runId"])
    post_log(f'node "ip-192-168-15-185.ec2.internal" is ready ✅', run_id=port_env_context["runId"])
    post_log(f'node "ip-192-168-23-133.ec2.internal" is ready ✅', run_id=port_env_context["runId"])
    post_log(f'node "ip-192-168-63-179.ec2.internal" is ready ✅', run_id=port_env_context["runId"])
    post_log(f'waiting for at least 2 node(s) to become ready in "ng-598412f9" ⏳', run_id=port_env_context["runId"])
    post_log(f'kubectl command should work with "/home/dan/.kube/config", try "kubectl get nodes" 🖥️',
             run_id=port_env_context["runId"])
    post_log(f'EKS cluster "{cluster_name}" in "us-east-1" region is ready 🎉', run_id=port_env_context["runId"])



