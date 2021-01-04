### k8s权限配置
    
    kubectl create role pod-watch --verb=get,list,watch --resource=pods
    kubectl create clusterrole pod-watch-clusterrole --verb=get,list,watch --resource=pods
    kubectl create serviceaccount pod-watch-account -n jacoco
    kubectl create clusterrolebinding pod-watch-binding --clusterrole=pod-watch-clusterrole --serviceaccount=jacoco:pod-watch-account
    