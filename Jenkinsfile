pipeline {
    agent {
        kubernetes {
        yaml """
            apiVersion: v1
            kind: Pod
            metadata:
            labels:
                some-label: helm
            spec:
            containers:
            - name: helm
                image: "alpine/helm:3.14.0"
                command:
                - cat
                tty: true
            """
        }
  }
        

    environment {
        CHART_NAME = "flask-postgres-chart"
        CHART_VERSION = "0.1.${BUILD_NUMBER}"  // Auto versioning
        REPO_DIR = "/my-helm-repo"   // Update as per your system
        REPO_URL = "http://127.0.0.1:8879"
        RELEASE_NAME = "flask-app"
    }

    stages {
        stage('Update Chart Version') {
            steps {
                script {
                    sh """
                    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
                    sed -i 's/^version:.*/version: ${CHART_VERSION}/' ${CHART_NAME}/Chart.yaml
                    """
                }
            }
        }

        stage('Helm Package') {
            steps {
                sh "helm package ${CHART_NAME} --destination ${REPO_DIR}"
            }
        }

        stage('Update Repo Index') {
            steps {
                sh "helm repo index ${REPO_DIR} --url ${REPO_URL}"
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh "helm repo add myrepo ${REPO_URL} || true"
                sh "helm repo update"
                sh """
                    helm upgrade --install ${RELEASE_NAME} \
                    myrepo/${CHART_NAME} \
                    --version ${CHART_VERSION}
                """
            }
        }
    }

    post {
        success {
            echo "Deployed version ${CHART_VERSION} of ${CHART_NAME} successfully."
        }
        failure {
            echo "Deployment failed."
        }
    }
}
