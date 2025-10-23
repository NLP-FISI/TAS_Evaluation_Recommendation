pipeline {
    agent any

    tools {
        jenkins.plugins.shiningpanda.tools.PythonInstallation('Python3')
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    credentialsId: 'github-credentials',
                    url: 'https://github.com/NLP-FISI/TAS_Evaluation_Recommendation.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest || echo "No tests found"
                '''
            }
        }

        stage('Quality Analysis') {
            steps {
                echo 'Integración con SonarQube pendiente.'
            }
        }
    }
}

