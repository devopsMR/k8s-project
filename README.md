# k8s-project

## Project Structure

```plaintext
k8s-project/
├── bundle/
│   ├── app.py          # Python code for the application logic
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile      # Dockerfile to containerize the Python application
├── ci-cd/
│   ├── Jenkinsfile     # CI/CD pipeline configuration for Jenkins
├── deployment/
│   ├── helm-charts/my-apps    # Helm charts for deploying the application
│   │   ├── Chart.yaml  # Helm chart metadata - rabbitmq dependencies
│   │   ├── values.yaml # Helm configuration values
│   │   └── templates/  # Kubernetes resource templates
│   │       ├── deployment_consumer.yml # Kubernetes Deployment configuration
│   │       └── service_consumer.yml    # Kubernetes Service configuration
│   │       └── deployment_producer.yml # Kubernetes Deployment configuration
│   ├── k8s-manifests/ # Static Kubernetes manifests (alternative to Helm)
│       ├── deployment.yaml # Static Kubernetes Deployment configuration
│       ├── service.yaml    # Static Kubernetes Service configuration
```

### Explanation

1. **bundle/**
    - Contains the application code (`consumer.py & producer.py`) and its dependencies (`requirements.txt`).
    - A `Dockerfile` for each application.

2. **ci-cd/**
    - Contains the `Jenkinsfile`, which defines the Continuous Integration and Continuous Deployment (CI/CD) pipeline.
      

3. **deployment/**
    - **helm-charts**: Contains Helm templates to deploy the application. `Chart.yaml` provides metadata, `values.yaml`
      stores variable values, and the `templates/` folder contains Kubernetes resource templates.
    - **k8s-manifests**: Contains static Kubernetes YAML files as an alternative to Helm for directly managing
      application deployment in Kubernetes.

## Commands to retrieve the URLs for accessing the services:

### For accessing the consumer metrics service
```bash
minikube service consumer-metrics-service -n k8s-project --url
```

### For accessing the RabbitMQ NodePort service
```bash
minikube service rabbitmq-nodeport -n k8s-project --url
```
## Jenkins install and commands
### install command
```bash
brew install jenkins-lts 
```
### add access to kubectl and helm
```bash
vi /opt/homebrew/Cellar/jenkins-lts/2.492.1/homebrew.mxcl.jenkins-lts.plist
    <key>EnvironmentVariables</key>
    <dict>
      <key>PATH</key>
      <string>/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin/:/Applications/Docker.app/Contents/Resources/bin/:/Users/michaelrosenbaum/Library/Group\ Containers/group.com.docker/Applications/Docker.app/Contents/Resources/bin</string>
    </dict>
```
### start jenkins
```bash
brew services start  jenkins-lts 
localhost:8080
```
## Helm Commands 
### Helm install command
```bash
helm install myhelm ./my-apps --namespace k8s-project
```
### Helm uninstall command
```bash
helm uninstall myhelm --namespace k8s-project
```