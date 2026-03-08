pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Pulling latest code from GitHub...'
                checkout scm
            }
        }

        stage('Environment Setup') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '''
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 syntax check...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    pip install flake8
                    flake8 app.py --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running Pytest unit tests...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -m pytest tests/ -v --tb=short
                '''
            }
        }

    }

    post {
        success {
            echo "BUILD SUCCESS - ACEest pipeline completed successfully."
        }
        failure {
            echo "BUILD FAILED - Check the logs above."
        }
        always {
            echo 'Cleaning up workspace...'
            bat 'if exist venv rmdir /s /q venv'
        }
    }
}