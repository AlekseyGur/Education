# Если kustomization (https://github.com/kubernetes-sigs/kustomize) не установлен, то выполняем последовательно:

kubectl apply -f namespace.yaml
kubectl apply -f deployment.yaml
kubectl apply -f rbac.yaml 
kubectl apply -f replicaset.yaml
kubectl apply -f pod.yaml 
