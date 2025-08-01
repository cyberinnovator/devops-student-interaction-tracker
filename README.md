# Student Interaction Tracker - DevOps Deployment

A complete CI/CD pipeline for deploying a student voice tracking system using Docker, Jenkins, MongoDB, and AWS EC2.

## 🚀 **Deployment Architecture**

```mermaid
graph LR
    A[Developer] --> B[Git Repository]
    B --> C[Jenkins Pipeline]
    C --> D[Docker Build]
    D --> E[Docker Hub Registry]
    E --> F[AWS EC2 Instance]
    F --> G[MongoDB Container]
    F --> H[Application Container]
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#e3f2fd
    style F fill:#fff8e1
    style G fill:#fce4ec
    style H fill:#f1f8e9
```

## 🔄 **CI/CD Pipeline Flow**

```mermaid
flowchart TD
    A[Code Push] --> B[Git Webhook]
    B --> C[Jenkins Trigger]
    C --> D[Checkout Code]
    D --> E[Build Docker Image]
    E --> F[Run Tests]
    F --> G{Tests Pass?}
    G -->|Yes| H[Push to Docker Hub]
    G -->|No| I[Build Failed]
    H --> J[Deploy to EC2]
    J --> K[Health Check]
    K --> L{Health OK?}
    L -->|Yes| M[Deployment Success]
    L -->|No| N[Rollback]
    
    style A fill:#e8f5e8
    style M fill:#c8e6c9
    style I fill:#ffcdd2
    style N fill:#ffcdd2
```

## 🏗️ **System Architecture**

```mermaid
graph TB
    subgraph "AWS EC2 Instance"
        subgraph "Docker Containers"
            A[Application Container<br/>Python 3.10]
            B[MongoDB Container<br/>MongoDB LTS]
        end
        
        C[Jenkins Server]
        D[Docker Engine]
    end
    
    subgraph "External Services"
        E[Git Repository]
        F[Docker Hub Registry]
    end
    
    A --> B
    C --> D
    D --> A
    D --> B
    E --> C
    F --> D
    
    style A fill:#e1f5fe
    style B fill:#f3e5f5
    style C fill:#fff3e0
    style D fill:#e8f5e8
    style E fill:#e3f2fd
    style F fill:#fff8e1
```

## 🏗️ **Technology Stack**

- **Containerization**: Docker & Docker Compose
- **CI/CD**: Jenkins Pipeline
- **Database**: MongoDB (NoSQL)
- **Cloud**: AWS EC2
- **Registry**: Docker Hub
- **Language**: Python 3.10

## 📋 **Prerequisites**

- AWS EC2 instance (Ubuntu 22.04 LTS)
- Jenkins server (installed on EC2)
- Docker Hub account
- Git repository

## 🛠️ **Quick Start**

### 1. **Clone and Setup**
```bash
git clone <your-repository-url>
cd student-interaction-tracker
```

### 2. **Local Testing**
```bash
# Test Docker build
docker build -t student-interaction-tracker .

# Test with Docker Compose
docker-compose up --build
```

### 3. **Deploy to Production**
```bash
# Push code to trigger Jenkins pipeline
git add .
git commit -m "Update application"
git push origin main
```

## 🔧 **Jenkins Pipeline Configuration**

### **Pipeline Stages:**
```mermaid
graph LR
    A[Checkout] --> B[Build]
    B --> C[Test]
    C --> D[Push]
    D --> E[Deploy]
    E --> F[Health Check]
    
    style A fill:#e8f5e8
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e1f5fe
    style F fill:#f1f8e9
```

1. **Checkout** - Pull code from Git
2. **Build** - Create Docker image
3. **Test** - Run MongoDB connection tests
4. **Push** - Upload to Docker Hub
5. **Deploy** - Deploy to EC2
6. **Health Check** - Verify deployment

### **Jenkins Setup:**
1. Install Jenkins on EC2
2. Install required plugins:
   - Docker Pipeline
   - Git Plugin
   - Pipeline
   - Credentials Binding
3. Configure credentials:
   - Docker Hub credentials (`docker-hub-credentials`)
4. Create pipeline job pointing to `Jenkinsfile`

## 🐳 **Docker Configuration**

### **Dockerfile**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python3", "main.py"]
```

### **Docker Compose**
```yaml
version: '3.8'
services:
  db:
    image: mongo:lts
    environment:
      MONGO_INITDB_ROOT_USERNAME: user
      MONGO_INITDB_ROOT_PASSWORD: password
      MONGO_INITDB_DATABASE: studentdb
    volumes:
      - mongodata:/data/db

  app:
    image: dockerpilot17/student-interaction-tracker:latest
    depends_on:
      - db
    environment:
      MONGO_URL: mongodb://user:password@db:27017/studentdb?authSource=admin
      DB_NAME: studentdb
```

## 📊 **Database Migration**

### **From SQLite to MongoDB**
The application has been migrated from SQLite to MongoDB for better scalability:

```mermaid
graph LR
    A[SQLite Database] --> B[Migration Script]
    B --> C[MongoDB Collections]
    
    subgraph "Data Structure"
        D[Students Collection]
        E[Teachers Collection]
    end
    
    C --> D
    C --> E
    
    style A fill:#ffcdd2
    style B fill:#fff3e0
    style C fill:#c8e6c9
    style D fill:#e1f5fe
    style E fill:#f3e5f5
```

- **Migration Script**: `migrate_to_mongodb.py`
- **Database Operations**: `db.py` (MongoDB implementation)
- **Test Script**: `test_mongodb.py`

### **Data Structure**
```javascript
// Students Collection
{
  "roll_no": "string",
  "embedding_path": "string", 
  "time": "number"
}

// Teachers Collection
{
  "teacher_id": "string",
  "embedding_path": "string"
}
```

## 🔄 **Deployment Process**

### **Automated Deployment**
```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Git as Git Repository
    participant Jenkins as Jenkins
    participant Docker as Docker Hub
    participant EC2 as AWS EC2
    participant App as Application
    participant DB as MongoDB

    Dev->>Git: Push Code
    Git->>Jenkins: Webhook Trigger
    Jenkins->>Jenkins: Build Docker Image
    Jenkins->>Docker: Push Image
    Jenkins->>EC2: Deploy
    EC2->>App: Start Container
    App->>DB: Connect to MongoDB
    Jenkins->>EC2: Health Check
    EC2->>Jenkins: Status Report
```

1. **Code Push** triggers Jenkins pipeline
2. **Jenkins** builds Docker image
3. **Docker Hub** stores the image
4. **EC2** pulls and runs the image
5. **MongoDB** stores application data
6. **Health checks** verify deployment

### **Manual Deployment**
```bash
# On EC2 instance
./deploy.sh deploy
```

## 📁 **Project Structure**

```
student-interaction-tracker/
├── main.py                 # Main application
├── db.py                   # MongoDB operations
├── embedding.py            # Voice embedding processing
├── diarization.py          # Speaker diarization
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Container orchestration
├── Jenkinsfile             # CI/CD pipeline
├── deploy.sh               # Deployment script
├── requirements.txt        # Python dependencies
├── test_mongodb.py         # Database tests
├── migrate_to_mongodb.py   # Data migration
└── README.md               # This file
```

## 🔍 **Monitoring & Maintenance**

### **Health Checks**
```bash
# Check container status
docker-compose ps

# View application logs
docker-compose logs -f app

# Check database connection
docker-compose exec db mongosh --eval "db.runCommand({ping: 1})"
```

### **Backup & Recovery**
```bash
# Create backup
./deploy.sh backup

# Rollback deployment
./deploy.sh rollback
```

## 🚨 **Troubleshooting**

### **Common Issues**

1. **Docker Permission Issues**
   ```bash
   sudo usermod -aG docker jenkins
   sudo systemctl restart jenkins
   ```

2. **MongoDB Connection Issues**
   ```bash
   docker-compose logs db
   docker-compose restart db
   ```

3. **Jenkins Build Failures**
   - Check Jenkins console output
   - Verify Docker Hub credentials
   - Ensure Git repository is accessible

### **Logs Location**
- **Application**: `docker-compose logs app`
- **Database**: `docker-compose logs db`
- **Jenkins**: `/var/log/jenkins/jenkins.log`

## 🔐 **Security Considerations**

- MongoDB authentication enabled
- Docker containers run with limited privileges
- Environment variables for sensitive data
- Regular security updates

## 📈 **Scaling Options**

### **Horizontal Scaling**
```mermaid
graph TB
    subgraph "Load Balancer"
        LB[Application Load Balancer]
    end
    
    subgraph "EC2 Instances"
        EC1[EC2 Instance 1]
        EC2[EC2 Instance 2]
        EC3[EC2 Instance 3]
    end
    
    subgraph "Database"
        DB1[MongoDB Primary]
        DB2[MongoDB Secondary]
        DB3[MongoDB Secondary]
    end
    
    LB --> EC1
    LB --> EC2
    LB --> EC3
    EC1 --> DB1
    EC2 --> DB1
    EC3 --> DB1
    DB1 --> DB2
    DB1 --> DB3
    
    style LB fill:#e3f2fd
    style EC1 fill:#e8f5e8
    style EC2 fill:#e8f5e8
    style EC3 fill:#e8f5e8
    style DB1 fill:#f3e5f5
    style DB2 fill:#f3e5f5
    style DB3 fill:#f3e5f5
```

- Multiple EC2 instances behind load balancer
- MongoDB replica set for high availability
- Docker Swarm or Kubernetes for orchestration

### **Vertical Scaling**
- Larger EC2 instance types
- MongoDB Atlas for managed database
- Enhanced monitoring and alerting

## 🤝 **Contributing**

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test locally with Docker
5. Push and create pull request

## 📞 **Support**

- **Repository**: [GitHub Repository URL]
- **Docker Hub**: [dockerpilot17/student-interaction-tracker]
- **Issues**: Create GitHub issue for bugs/features

---

**Deployed By**: [Your Name]  
**Last Updated**: [Date]  
**Version**: 1.0
