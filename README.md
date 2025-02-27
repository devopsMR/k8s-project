# k8s-project

# Commands to retrieve the URLs for accessing the services:

    # For accessing the consumer metrics service
    minikube service consumer-metrics-service -n k8s-project --url
    
    # For accessing the RabbitMQ NodePort service
    minikube service rabbitmq-nodeport -n k8s-project --url
