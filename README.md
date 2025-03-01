# k8s-project

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