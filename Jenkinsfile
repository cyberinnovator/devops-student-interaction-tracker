pipeline {
    agent any

    environment {
        IMAGE_NAME = 'vedantpatil/devops-student-tracker'
        IMAGE_TAG = 'latest'
        DOCKERHUB_CREDENTIALS = credentials('c12afb4f-2011-4cdb-9c37-05fd7c4bf361')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/cyberinnovator/devops-student-interaction-tracker.git', branch: 'main'
            }
        }

        stage('Debug: Print requirements.txt') {
            steps {
                sh 'cat requirements.txt'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build --no-cache -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'c12afb4f-2011-4cdb-9c37-05fd7c4bf361') {
                        sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    sh "docker-compose down || true"
                    sh "docker-compose up -d"
                }
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline executed successfully!'
        }
        failure {
            echo '❌ Pipeline failed. Check the console output for errors.'
        }
    }
}
