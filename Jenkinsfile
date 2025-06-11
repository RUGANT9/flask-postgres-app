pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask-app"
        IMAGE_TAG = "${BUILD_NUMBER}"
        CHART_NAME = "flask-postgres-chart"
        CHART_VERSION = "0.1.${BUILD_NUMBER}"
        REPO_DIR = "/my-helm-repo"       // Path to your local repo folder
        REPO_URL = "http://127.0.0.1:8879" // If you're hosting via `python3 -m http.server`
        RELEASE_NAME = "flask-app"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Update Chart Version + Image Tag') {
            steps {
                sh """
                  sed -i 's/^version:.*/version: ${CHART_VERSION}/' ${CHART_NAME}/Chart.yaml
                  sed -i 's/^  tag:.*/  tag: "${IMAGE_TAG}"/' ${CHART_NAME}/values.yaml
                """
            }
        }

        stage('Package Helm Chart') {
            steps {
                sh "helm package ${CHART_NAME} --destination ${REPO_DIR}"
            }
        }

        stage('Update Helm Repo Index') {
            steps {
                sh "helm repo index ${REPO_DIR} --url ${REPO_URL}"
            }
        }

        stage('Deploy from Local Helm Repo') {
            steps {
                sh """
                  helm repo add localrepo ${REPO_URL} || true
                  helm repo update
                  helm upgrade --install ${RELEASE_NAME} \
                    localrepo/${CHART_NAME} \
                    --version ${CHART_VERSION}
                """
            }
        }
    }

    post {
        success {
            echo "✅ Deployed version ${CHART_VERSION} of ${CHART_NAME} from local Helm repo."
        }
        failure {
            echo "❌ CI/CD failed."
        }
    }
}
