pipeline {
    agent {
        label 'docker'
    }
    
    environment {
        REGISTRY = 'ghcr.io/bwoogmy'
        IMAGE_NAME = 'devops-backend'
        GHCR_CREDENTIALS = credentials('github-ghcr')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                echo '🧪 Running unit tests...'
                sh 'make unit-test'
            }
        }
        
        stage('Build & Push') {
            when {
                tag pattern: "v\\d+\\.\\d+\\.\\d+", comparator: "REGEXP"
            }
            steps {
                script {
                    def imageTag = env.TAG_NAME
                    
                    echo "🔨 Building image with tag: ${imageTag}"
                    sh "make build IMAGE_TAG=${imageTag}"
                    
                    echo "🔐 Logging into GHCR..."
                    sh '''
                        echo ${GHCR_CREDENTIALS_PSW} | docker login ghcr.io -u ${GHCR_CREDENTIALS_USR} --password-stdin
                    '''
                    
                    echo "📦 Pushing image..."
                    sh "make push IMAGE_TAG=${imageTag}"
                    
                    echo "📦 Packaging and pushing Helm chart..."
                    sh "make package-chart IMAGE_TAG=${imageTag}"
                    sh "make push-chart IMAGE_TAG=${imageTag}"
                    
                    echo "📝 Updating Chart.yaml..."
                    sh "make update-chart-version IMAGE_TAG=${imageTag}"
                    
                    echo "🏷️ Tagging as latest..."
                    sh """
                        docker tag ${IMAGE_NAME}:${imageTag} ${REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline completed successfully!'
        }
        failure {
            echo '❌ Pipeline failed!'
        }
        always {
            sh 'docker logout ghcr.io || true'
        }
    }
}
