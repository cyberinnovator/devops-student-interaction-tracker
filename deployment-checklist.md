# Deployment Checklist - Student Interaction Tracker

Use this checklist to ensure all components are properly configured for the CI/CD pipeline.

## ✅ Pre-Deployment Setup

### Docker Hub Setup
- [ ] Create Docker Hub account
- [ ] Create repository: `yourdockerhubusername/student-interaction-tracker`
- [ ] Generate access token with push permissions
- [ ] Test Docker login locally

### AWS EC2 Setup
- [ ] Launch EC2 instance (Ubuntu 22.04 LTS)
- [ ] Configure security groups (SSH: 22, HTTP: 80, HTTPS: 443)
- [ ] Create/download SSH key pair
- [ ] Test SSH connection to EC2
- [ ] Install Docker and Docker Compose on EC2
- [ ] Add user to docker group on EC2
- [ ] Copy `deploy.sh` to EC2 and make executable

### Jenkins Setup
- [ ] Install Jenkins server
- [ ] Complete initial Jenkins setup
- [ ] Install required plugins:
  - [ ] Docker Pipeline
  - [ ] SSH Agent
  - [ ] Credentials Binding
  - [ ] Pipeline
  - [ ] Git
  - [ ] Email Extension (optional)
- [ ] Configure Jenkins credentials:
  - [ ] Docker Hub credentials (`docker-hub-credentials`)
  - [ ] EC2 SSH key (`ec2-ssh-key`)
- [ ] Add Jenkins user to docker group
- [ ] Restart Jenkins

## ✅ Configuration Files

### Update Jenkinsfile
- [ ] Replace `yourdockerhubusername` with your Docker Hub username
- [ ] Replace `your-ec2-public-dns` with your EC2 public DNS
- [ ] Verify all environment variables are correct
- [ ] Test Jenkinsfile syntax

### Update deploy.sh
- [ ] Replace `yourdockerhubusername` with your Docker Hub username
- [ ] Verify APP_DIR path is correct for your EC2 setup
- [ ] Test deploy.sh script on EC2

### Environment Variables
- [ ] Verify MONGO_URL is correct
- [ ] Verify DB_NAME is correct
- [ ] Test MongoDB connection

## ✅ Pipeline Configuration

### Jenkins Pipeline
- [ ] Create new pipeline: `student-interaction-tracker`
- [ ] Configure Git repository URL
- [ ] Set branch specifier (e.g., `*/main`)
- [ ] Configure build triggers (Poll SCM: `H/5 * * * *`)
- [ ] Set pipeline definition to "Pipeline script from SCM"
- [ ] Set script path to `Jenkinsfile`

### Git Repository
- [ ] Push all files to Git repository:
  - [ ] Jenkinsfile
  - [ ] Dockerfile
  - [ ] docker-compose.yml
  - [ ] deploy.sh
  - [ ] All Python files
  - [ ] requirements.txt
  - [ ] README.md
- [ ] Verify Jenkins can access the repository

## ✅ Testing

### Local Testing
- [ ] Test Docker build locally: `docker build -t test-image .`
- [ ] Test docker-compose locally: `docker-compose up --build`
- [ ] Test MongoDB connection locally
- [ ] Run test script: `python3 test_mongodb.py`

### Jenkins Testing
- [ ] Run manual build in Jenkins
- [ ] Check each stage:
  - [ ] Checkout stage
  - [ ] Build Docker Image stage
  - [ ] Test stage
  - [ ] Push to Docker Hub stage
  - [ ] Deploy to EC2 stage
  - [ ] Health Check stage
- [ ] Verify no errors in console output

### EC2 Testing
- [ ] Test deployment script: `./deploy.sh status`
- [ ] Test health check: `./deploy.sh health`
- [ ] Verify containers are running: `docker-compose ps`
- [ ] Check application logs: `docker-compose logs -f`

## ✅ Production Readiness

### Security
- [ ] Change default MongoDB credentials
- [ ] Configure firewall rules
- [ ] Set up SSL/HTTPS (if web interface)
- [ ] Review security group settings
- [ ] Enable CloudWatch monitoring

### Monitoring
- [ ] Set up application logging
- [ ] Configure log rotation
- [ ] Set up basic monitoring
- [ ] Test backup procedures

### Documentation
- [ ] Update README.md with deployment instructions
- [ ] Document troubleshooting procedures
- [ ] Create runbook for common issues
- [ ] Document rollback procedures

## ✅ Final Verification

### End-to-End Test
- [ ] Make a code change
- [ ] Push to Git repository
- [ ] Verify Jenkins pipeline triggers automatically
- [ ] Monitor pipeline execution
- [ ] Verify deployment to EC2
- [ ] Test application functionality
- [ ] Verify data persistence in MongoDB

### Performance Test
- [ ] Test application under load
- [ ] Monitor resource usage
- [ ] Verify auto-restart functionality
- [ ] Test backup and restore procedures

## 🚨 Troubleshooting Checklist

### Common Issues
- [ ] Docker permission issues resolved
- [ ] SSH connection issues resolved
- [ ] MongoDB connection issues resolved
- [ ] Jenkins credential issues resolved
- [ ] Network connectivity issues resolved

### Emergency Procedures
- [ ] Know how to rollback deployment
- [ ] Know how to access EC2 instance
- [ ] Know how to check application logs
- [ ] Know how to restart services
- [ ] Have backup procedures tested

## 📋 Maintenance Tasks

### Regular Maintenance
- [ ] Monitor Jenkins disk space
- [ ] Clean up old Docker images
- [ ] Update system packages
- [ ] Review security updates
- [ ] Test backup procedures

### Monthly Tasks
- [ ] Review application logs
- [ ] Check resource usage trends
- [ ] Update documentation
- [ ] Review security settings
- [ ] Test disaster recovery procedures

---

## 🎯 Success Criteria

Your deployment is successful when:

1. ✅ Code push triggers automatic Jenkins build
2. ✅ Jenkins builds Docker image successfully
3. ✅ Docker image is pushed to Docker Hub
4. ✅ Application deploys to EC2 automatically
5. ✅ Application is accessible and functional
6. ✅ MongoDB data persists across deployments
7. ✅ Health checks pass consistently
8. ✅ Rollback procedures work when needed

## 📞 Support Information

- **Jenkins URL**: `http://your-jenkins-url:8080`
- **EC2 Public DNS**: `your-ec2-public-dns`
- **Docker Hub Repository**: `yourdockerhubusername/student-interaction-tracker`
- **Git Repository**: `your-git-repo-url`

---

**Last Updated**: [Date]
**Deployed By**: [Your Name]
**Version**: 1.0 