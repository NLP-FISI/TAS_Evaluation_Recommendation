pipeline {
    agent any

    tools {
        jdk 'JDK17'
        maven 'Maven3'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-token',
                    url: 'https://github.com/NLP-FISI/TAS_Evaluation_Recommendation.git'
            }
        }

        stage('Build') {
            steps {
                sh 'mvn clean package -DskipTests'
            }
        }

        stage('Test') {
            steps {
                sh 'mvn test'
            }
        }

        stage('Quality Analysis') {
            steps {
                echo 'Running SonarQube analysis...'
                // Aquí puedes agregar la integración con Sonar más adelante
            }
        }
    }
}
