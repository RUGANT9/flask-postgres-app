pipeline {
    agent any

    environment {
        CHART_NAME = "flask-postgres-chart"
        CHART_VERSION = "0.1.${BUILD_NUMBER}"  // Auto versioning
        REPO_DIR = "/var/www/html/helm-repo"   // Update as per your system
        REPO_URL = "http://127.0.0.1:8879"
        RELEASE_NAME = "flask-app"
    }

    stages {
        stage('Update Chart Version') {
            steps {
                script {
                    sh "sed -i '' 's/^version:.*/version: ${CHART_VERSION}/' ${CHART_NAME}/Chart.yaml"
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
                sh "helm repo add localrepo ${REPO_URL} || true"
                sh "helm repo update"
                sh """
                    helm upgrade --install ${RELEASE_NAME} \
                    localrepo/${CHART_NAME} \
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
