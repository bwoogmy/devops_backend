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
        stage('Detect Version') {
        steps {
            script {
                env.TAG_NAME = sh(
                    script: "git describe --tags --exact-match 2>/dev/null || echo ''",
                    returnStdout: true
                ).trim()
                echo "Detected tag: ${env.TAG_NAME}"
                echo "Branch: ${env.BRANCH_NAME}"
                echo "Git commit: ${env.GIT_COMMIT}"
            }
        }
    }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running unit tests...'
                sh 'make unit-test'
            }
        }

        stage('Lint Chart') {
            steps {
                echo 'Linting Helm chart'
                sh 'make lint'
            }
        }
        
        stage('Build Image') {
            steps {
                script {
                    def imageTag = env.TAG_NAME ?: 'latest'
                    echo "Building image with tag: ${imageTag}"
                    sh "make build IMAGE_TAG=${imageTag}"
                }
            }
        }
        
        stage('Push to Registry') {
            when {
                expression { 
                    return env.TAG_NAME != null && env.TAG_NAME != '' && env.TAG_NAME.matches('v\\d+\\.\\d+\\.\\d+')
                }
            }
            steps {
                script {
                    def imageTag = env.TAG_NAME
                    
                    echo "Logging into GHCR"
                    sh '''
                        echo ${GHCR_CREDENTIALS_PSW} | docker login ghcr.io -u ${GHCR_CREDENTIALS_USR} --password-stdin
                    '''
                    
                    echo "Pushing image: ${imageTag}"
                    sh "make push IMAGE_TAG=${imageTag}"
                    
                    echo "Packaging and pushing Helm chart"
                    sh "make package-chart IMAGE_TAG=${imageTag}"
                    sh "make push-chart IMAGE_TAG=${imageTag}"
                    
                    echo "Tagging as latest"
                    sh """
                        docker tag ${IMAGE_NAME}:${imageTag} ${REGISTRY}/${IMAGE_NAME}:latest
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Update Flux Staging') {
            when {
                expression { 
                    return env.TAG_NAME != null && env.TAG_NAME != '' && env.TAG_NAME.matches('v\\d+\\.\\d+\\.\\d+')
                }
            }
            steps {
                script {
                    def chartVersion = env.TAG_NAME.replaceFirst(/^v/, '')
                    
                    withCredentials([usernamePassword(credentialsId: 'github-ghcr', usernameVariable: 'GIT_USERNAME', passwordVariable: 'GIT_PASSWORD')]) {
                        sh """
                            git config user.name "Jenkins CI"
                            git config user.email "jenkins@devops.local"
                            sed -i 's|version: .*|version: ${chartVersion}|' flux/staging/patches.yaml
                            git add flux/staging/patches.yaml
                            git commit -m "chore: bump staging to ${chartVersion}" || echo "No changes to commit"
                            
                            git push https://${GIT_USERNAME}:${GIT_PASSWORD}@github.com/bwoogmy/devops_backend.git HEAD:main || echo "Push failed or no changes"
                        """
                    }
                }
            }
        }
    }

    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
        always {
            sh 'docker logout ghcr.io || true'
        }
    }
}
