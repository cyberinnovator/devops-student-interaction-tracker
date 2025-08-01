#!/bin/bash

# deploy.sh - Deployment script for Student Interaction Tracker
# This script can be run on EC2 to deploy the application

set -e  # Exit on any error

# Configuration
APP_NAME="student-interaction-tracker"
DOCKER_IMAGE="dockerpilot17/student-interaction-tracker:latest"
APP_DIR="/home/ec2-user/${APP_NAME}"
BACKUP_DIR="/home/ec2-user/backups"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   error "This script should not be run as root"
   exit 1
fi

# Function to check if Docker is installed
check_docker() {
    log "Checking Docker installation..."
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed. Installing Docker..."
        sudo apt-get update
        sudo apt-get install -y docker.io docker-compose
        sudo usermod -aG docker $USER
        success "Docker installed successfully"
        warning "Please log out and log back in for Docker group changes to take effect"
        exit 1
    fi
    success "Docker is installed"
}

# Function to create backup
create_backup() {
    log "Creating backup of current deployment..."
    mkdir -p "$BACKUP_DIR"
    if [ -d "$APP_DIR" ]; then
        tar -czf "$BACKUP_DIR/backup-$(date +%Y%m%d-%H%M%S).tar.gz" -C "$(dirname $APP_DIR)" "$(basename $APP_DIR)"
        success "Backup created successfully"
    else
        warning "No existing deployment found to backup"
    fi
}

# Function to pull latest image
pull_image() {
    log "Pulling latest Docker image..."
    docker pull "$DOCKER_IMAGE"
    success "Latest image pulled successfully"
}

# Function to create docker-compose.yml
create_docker_compose() {
    log "Creating docker-compose.yml..."
    mkdir -p "$APP_DIR"
    
    cat > "$APP_DIR/docker-compose.yml" << EOF
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
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.runCommand({ping: 1})"]
      interval: 30s
      timeout: 10s
      retries: 3

  app:
    image: ${DOCKER_IMAGE}
    depends_on:
      db:
        condition: service_healthy
    environment:
      MONGO_URL: mongodb://user:password@db:27017/studentdb?authSource=admin
      DB_NAME: studentdb
    restart: unless-stopped
    volumes:
      - ./embeddings:/app/embeddings
    healthcheck:
      test: ["CMD", "python3", "-c", "import pymongo; pymongo.MongoClient('mongodb://user:password@db:27017/studentdb?authSource=admin')"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  mongodata:
EOF
    success "docker-compose.yml created successfully"
}

# Function to stop existing containers
stop_containers() {
    log "Stopping existing containers..."
    if [ -f "$APP_DIR/docker-compose.yml" ]; then
        cd "$APP_DIR"
        docker-compose down || true
        success "Existing containers stopped"
    else
        warning "No existing docker-compose.yml found"
    fi
}

# Function to start containers
start_containers() {
    log "Starting containers..."
    cd "$APP_DIR"
    docker-compose up -d
    success "Containers started successfully"
}

# Function to wait for services to be ready
wait_for_services() {
    log "Waiting for services to be ready..."
    sleep 30
    
    # Check if containers are running
    if docker-compose ps | grep -q "Up"; then
        success "All containers are running"
    else
        error "Some containers failed to start"
        docker-compose logs
        exit 1
    fi
}

# Function to perform health check
health_check() {
    log "Performing health check..."
    
    # Check MongoDB
    if docker-compose exec -T db mongosh --eval "db.runCommand({ping: 1})" > /dev/null 2>&1; then
        success "MongoDB health check passed"
    else
        error "MongoDB health check failed"
        return 1
    fi
    
    # Check application
    if docker-compose ps app | grep -q "Up"; then
        success "Application health check passed"
    else
        error "Application health check failed"
        return 1
    fi
}

# Function to show deployment status
show_status() {
    log "Deployment Status:"
    cd "$APP_DIR"
    docker-compose ps
    echo ""
    log "Container logs (last 10 lines):"
    docker-compose logs --tail=10
}

# Function to rollback
rollback() {
    log "Rolling back to previous version..."
    if [ -f "$APP_DIR/docker-compose.yml" ]; then
        cd "$APP_DIR"
        docker-compose down
    fi
    
    # Find the most recent backup
    LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/backup-*.tar.gz 2>/dev/null | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        log "Restoring from backup: $LATEST_BACKUP"
        tar -xzf "$LATEST_BACKUP" -C "$(dirname $APP_DIR)"
        cd "$APP_DIR"
        docker-compose up -d
        success "Rollback completed successfully"
    else
        error "No backup found for rollback"
        exit 1
    fi
}

# Main deployment function
deploy() {
    log "Starting deployment of $APP_NAME..."
    
    check_docker
    create_backup
    pull_image
    create_docker_compose
    stop_containers
    start_containers
    wait_for_services
    health_check
    show_status
    
    success "Deployment completed successfully!"
}

# Parse command line arguments
case "$1" in
    deploy)
        deploy
        ;;
    rollback)
        rollback
        ;;
    status)
        show_status
        ;;
    health)
        health_check
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|status|health}"
        echo ""
        echo "Commands:"
        echo "  deploy   - Deploy the application"
        echo "  rollback - Rollback to previous version"
        echo "  status   - Show deployment status"
        echo "  health   - Perform health check"
        exit 1
        ;;
esac 