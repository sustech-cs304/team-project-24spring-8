pipeline {
    agent any
        stages{
            stage('Automated test') {
            steps{
                dir('backend') {
                    sh 'pytest'
                    }
            }
        }
            stage('Building image') {
            steps{
                script {
                    sh 'docker build -t myapp-frontend:latest -f frontend/Dockerfile ./frontend'
                    sh 'docker build -t myapp-backend:latest -f backend/Dockerfile ./backend'
                }
            }
        }
        // Uploading Docker images into Docker Hub
            stage('Upload image') {
            steps{
                withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
                    sh "docker login -u ${DOCKERHUB_USERNAME} -p ${DOCKERHUB_PASSWORD}"

                    sh "docker tag myapp-backend:latest ${DOCKERHUB_USERNAME}/myapp-backend:latest"
                    
                    sh"docker push ${DOCKERHUB_USERNAME}/myapp-backend:latest"

                    sh"docker tag myapp-frontend:latest ${DOCKERHUB_USERNAME}/myapp-frontend:latest"
                    sh"docker push ${DOCKERHUB_USERNAME}/myapp-frontend:latest"

                }
            }
        }
    }
}
