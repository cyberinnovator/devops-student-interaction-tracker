# Jenkins Setup Guide for Student Interaction Tracker

This guide will help you set up Jenkins for the CI/CD pipeline of the Student Interaction Tracker project.

## Prerequisites

- Jenkins server (local or cloud)
- Docker Hub account
- AWS EC2 instance
- SSH access to EC2

## Step 1: Install Jenkins

### Option A: Local Jenkins Installation

```bash
# Install Java
sudo apt update
sudo apt install openjdk-11-jdk

# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install jenkins

# Start Jenkins
sudo systemctl start jenkins
sudo systemctl enable jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### Option B: Jenkins on EC2

```bash
# Launch EC2 instance with Ubuntu 22.04 LTS
# Security Group: Allow SSH (22) and HTTP (8080)

# Connect to EC2 and install Jenkins
ssh -i your-key.pem ubuntu@your-ec2-public-dns

# Follow the same installation steps as Option A
```

## Step 2: Initial Jenkins Setup

1. **Access Jenkins**: Open `http://your-jenkins-url:8080`
2. **Install suggested plugins** when prompted
3. **Create admin user** and complete setup

## Step 3: Install Required Plugins

Go to **Manage Jenkins** → **Manage Plugins** → **Available** and install:

### Essential Plugins
- [x] **Docker Pipeline** - For Docker operations
- [x] **SSH Agent** - For SSH connections to EC2
- [x] **Credentials Binding** - For secure credential management
- [x] **Pipeline** - For Jenkinsfile support
- [x] **Git** - For Git integration
- [x] **Email Extension** - For email notifications (optional)

### Installation Steps
1. Go to **Manage Jenkins** → **Manage Plugins**
2. Click **Available** tab
3. Search for each plugin and check the box
4. Click **Install without restart**
5. Restart Jenkins when prompted

## Step 4: Configure Credentials

Go to **Manage Jenkins** → **Manage Credentials** → **System** → **Global credentials** → **Add Credentials**

### 1. Docker Hub Credentials
- **Kind**: Username with password
- **Scope**: Global
- **Username**: Your Docker Hub username
- **Password**: Your Docker Hub access token
- **ID**: `docker-hub-credentials`
- **Description**: Docker Hub credentials for pushing images

### 2. EC2 SSH Key
- **Kind**: SSH Username with private key
- **Scope**: Global
- **ID**: `ec2-ssh-key`
- **Description**: SSH key for EC2 deployment
- **Username**: `ec2-user` (or `ubuntu` for Ubuntu instances)
- **Private Key**: Enter directly or from file (your EC2 private key)

## Step 5: Configure Jenkins Environment

### 1. Set up Docker
```bash
# On Jenkins server
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 2. Configure Git (if needed)
```bash
# Set up Git user
git config --global user.name "Jenkins"
git config --global user.email "jenkins@your-domain.com"
```

## Step 6: Create Jenkins Pipeline

### 1. Create New Pipeline
1. Go to **Dashboard** → **New Item**
2. Enter **Item name**: `student-interaction-tracker`
3. Select **Pipeline**
4. Click **OK**

### 2. Configure Pipeline
1. **General**:
   - Check **GitHub project** (if using GitHub)
   - Enter project URL: `https://github.com/yourusername/student-interaction-tracker`

2. **Build Triggers**:
   - Check **Poll SCM** for automatic builds
   - Schedule: `H/5 * * * *` (every 5 minutes)

3. **Pipeline**:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: Your Git repository URL
   - **Credentials**: Add your Git credentials if private repo
   - **Branch Specifier**: `*/main` (or your main branch)
   - **Script Path**: `Jenkinsfile`

4. **Save** the configuration

## Step 7: Update Jenkinsfile Configuration

Before running the pipeline, update the `Jenkinsfile` with your specific values:

```groovy
environment {
    // Update these values
    DOCKER_IMAGE = 'yourdockerhubusername/student-interaction-tracker'
    EC2_HOST = 'ec2-user@your-ec2-public-dns'
    // ... other configurations
}
```

## Step 8: Test the Pipeline

### 1. Manual Build
1. Go to your pipeline
2. Click **Build Now**
3. Monitor the build progress
4. Check console output for any errors

### 2. Common Issues and Solutions

#### Docker Permission Issues
```bash
# Add jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

#### SSH Connection Issues
- Verify EC2 security group allows SSH
- Check SSH key permissions: `chmod 400 your-key.pem`
- Test SSH connection manually first

#### Docker Hub Authentication Issues
- Verify Docker Hub credentials
- Check if access token has push permissions
- Test Docker login manually

## Step 9: Set up EC2 Instance

### 1. Launch EC2 Instance
- **AMI**: Ubuntu 22.04 LTS
- **Instance Type**: t2.micro (free tier) or larger
- **Security Group**: Allow SSH (22), HTTP (80), HTTPS (443)

### 2. Install Docker on EC2
```bash
# Connect to EC2
ssh -i your-key.pem ec2-user@your-ec2-public-dns

# Install Docker
sudo apt update
sudo apt install -y docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and log back in
exit
ssh -i your-key.pem ec2-user@your-ec2-public-dns

# Verify Docker installation
docker --version
docker-compose --version
```

### 3. Copy Deployment Script
```bash
# Copy deploy.sh to EC2
scp -i your-key.pem deploy.sh ec2-user@your-ec2-public-dns:~/

# Make it executable
chmod +x deploy.sh
```

## Step 10: Monitor and Maintain

### 1. Jenkins Monitoring
- **Build History**: Monitor build success/failure rates
- **Console Output**: Check logs for issues
- **Disk Space**: Monitor Jenkins workspace size

### 2. EC2 Monitoring
- **Container Status**: `docker-compose ps`
- **Logs**: `docker-compose logs -f`
- **Resource Usage**: `htop`, `df -h`

### 3. Backup Strategy
- **Jenkins**: Backup Jenkins home directory
- **EC2**: Use the backup feature in deploy.sh
- **MongoDB**: Regular database backups

## Troubleshooting

### Jenkins Issues
```bash
# Check Jenkins status
sudo systemctl status jenkins

# View Jenkins logs
sudo tail -f /var/log/jenkins/jenkins.log

# Restart Jenkins
sudo systemctl restart jenkins
```

### Docker Issues
```bash
# Check Docker status
sudo systemctl status docker

# Clean up Docker
docker system prune -f
docker volume prune -f
```

### Pipeline Issues
- Check console output for specific error messages
- Verify all credentials are configured correctly
- Test each stage manually if needed

## Security Considerations

1. **Jenkins Security**:
   - Use HTTPS for Jenkins
   - Configure authentication
   - Regular security updates

2. **EC2 Security**:
   - Use security groups
   - Regular system updates
   - Monitor access logs

3. **Docker Security**:
   - Use non-root user in containers
   - Regular image updates
   - Scan images for vulnerabilities

## Next Steps

Once the basic pipeline is working:

1. **Add Testing**: Unit tests, integration tests
2. **Add Notifications**: Email, Slack notifications
3. **Add Monitoring**: Application monitoring, alerting
4. **Add Security**: Vulnerability scanning, secrets management
5. **Add Backup**: Automated backup procedures

---

## Quick Reference Commands

```bash
# Jenkins
sudo systemctl status jenkins
sudo systemctl restart jenkins
sudo cat /var/lib/jenkins/secrets/initialAdminPassword

# Docker
docker ps
docker-compose ps
docker system prune -f

# EC2
ssh -i your-key.pem ec2-user@your-ec2-public-dns
./deploy.sh status
./deploy.sh health
``` 