// pipeline {
//     agent any
//     stages {
//         stage('Build') {
//             steps {
//                 sh 'mvn -B -DskipTests clean package'
//             }
//         }
//         stage('pmd') {
//             steps {
//                 sh 'mvn pmd:pmd'
//             }
//         }
//         stage('Generate Javadoc') {
//             steps {
//                 sh 'mvn site --fail-never'
//             }
//         }
        
//     }
//     post {
//             always {
//                 archiveArtifacts artifacts: '**/target/site/**', fingerprint: true
//                 archiveArtifacts artifacts: '**/target/**/*.jar', fingerprint: true
//                 archiveArtifacts artifacts: '**/target/**/*.war', fingerprint: true
//             }
//         }
// }

pipeline {
    agent any
        stages{
            stage('Automated test') {
            steps{
                dir('backend') {
                        sh 'pwd'
                        
                        // Run uvicorn in the background and save its PID
                        sh 'uvicorn main:app --port 8001 & echo $! > uvicorn.pid'
                        sleep 10
                    }
                    sh 'newman run se.postman_collection.json -e token.postman_environment.json --reporters html,cli --reporter-html-export output.html'
            }
        }
            stage('Building image') {
            steps{
                sh 'docker-compose build'
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
        // stage('Run containers'){
        //     steps{
        //         withCredentials([usernamePassword(credentialsId: 'dockerhub_credentials', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
        //             sh "docker run -d -p 8082:8080 ${DOCKERHUB_USERNAME}/teedy"
        //         }
        //     }
        // }
    }
}
