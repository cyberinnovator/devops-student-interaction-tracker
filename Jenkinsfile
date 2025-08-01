pipeline {
    agent any
    
    environment {
        // Docker Hub configuration
        DOCKER_IMAGE = 'dockerpilot17/student-interaction-tracker'
        DOCKER_TAG = "${env.BUILD_NUMBER}"
        DOCKER_LATEST = "${DOCKER_IMAGE}:latest"
        DOCKER_VERSIONED = "${DOCKER_IMAGE}:${DOCKER_TAG}"
        
        // Credentials (configure these in Jenkins)
        DOCKER_HUB_CREDENTIALS = credentials('c12afb4f-2011-4cdb-9c37-05fd7c4bf361')
        
        // Application configuration (same machine as Jenkins)
        EC2_APP_DIR = '/home/ubuntu/student-interaction-tracker'
        MONGO_URL = 'mongodb://user:password@db:27017/studentdb?authSource=admin'
        DB_NAME = 'studentdb'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo '🔍 Checking out source code...'
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    docker.build("${DOCKER_VERSIONED}")
                    docker.build("${DOCKER_LATEST}")
                }
            }
        }
        
        stage('Test') {
            steps {
                echo '🧪 Running tests...'
                script {
                    // Run MongoDB connection test
                    docker.image("${DOCKER_VERSIONED}").inside('-e MONGO_URL=mongodb://test-mongo:27017/ -e DB_NAME=testdb') {
                        sh '''
                            echo "Testing MongoDB connection..."
                            python3 test_mongodb.py || exit 1
                        '''
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                echo '📤 Pushing to Docker Hub...'
                script {
                    withCredentials([usernamePassword(credentialsId: "${DOCKER_HUB_CREDENTIALS}", usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh '''
                            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                            docker push ${DOCKER_VERSIONED}
                            docker push ${DOCKER_LATEST}
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to EC2') {
            steps {
                echo '🚀 Deploying to EC2...'
                sh '''
                    echo 'Pulling latest image...'
                    docker pull ${DOCKER_LATEST}
                    
                    echo 'Creating application directory...'
                    mkdir -p ${EC2_APP_DIR}
                    
                    echo 'Creating docker-compose.yml...'
                    cat > ${EC2_APP_DIR}/docker-compose.yml << 'EOF'
version: '3.8'
services:
  db:
    image: mongo:lts
    environment:
      MONGO_INITDB_ROOT_USERNAME: user
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: studentdb
    ports:
      - '27017:27017'
    volumes:
      - mongodata:/data/db
    restart: unless-stopped

  app:
    image: ${DOCKER_LATEST}
    depends_on:
      - db
    environment:
      MONGO_URL: ${MONGO_URL}
      DB_NAME: ${DB_NAME}
    restart: unless-stopped

volumes:
  mongodata:
EOF
                    
                    echo 'Stopping existing containers...'
                    cd ${EC2_APP_DIR}
                    docker-compose down || true
                    
                    echo 'Starting new containers...'
                    docker-compose up -d
                    
                    echo 'Waiting for services to be ready...'
                    sleep 30
                    
                    echo 'Checking container status...'
                    docker-compose ps
                    
                    echo 'Deployment completed successfully!'
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo '🏥 Performing health check...'
                sh '''
                    cd ${EC2_APP_DIR}
                    
                    echo 'Checking if containers are running...'
                    if docker-compose ps | grep -q 'Up'; then
                        echo '✅ Containers are running successfully'
                    else
                        echo '❌ Containers are not running properly'
                        docker-compose logs
                        exit 1
                    fi
                    
                    echo 'Checking MongoDB connection...'
                    docker-compose exec -T db mongosh --eval 'db.runCommand({ping: 1})' || {
                        echo '❌ MongoDB health check failed'
                        exit 1
                    }
                    
                    echo '✅ Health check passed'
                '''
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            sh 'docker system prune -f || true'
        }
        
        success {
            echo '🎉 Pipeline completed successfully!'
            script {
                // Send success notification (optional)
                // emailext subject: 'Pipeline Success: Student Interaction Tracker',
                //         body: 'The deployment pipeline completed successfully.',
                //         to: 'your-email@example.com'
            }
        }
        
        failure {
            echo '❌ Pipeline failed!'
            script {
                // Send failure notification (optional)
                // emailext subject: 'Pipeline Failed: Student Interaction Tracker',
                //         body: 'The deployment pipeline failed. Check Jenkins logs for details.',
                //         to: 'your-email@example.com'
            }
        }
    }
} 
