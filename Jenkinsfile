pipeline {
    agent any

    environment {
        PYTHON = "C:\\Users\\srivi.DESKTOP-L6OI7G9\\AppData\\Local\\Python\\bin\\python.exe"
        PIP = "C:\\Users\\srivi.DESKTOP-L6OI7G9\\AppData\\Local\\Python\\bin\\pip.exe"
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
                bat """
                    "${PYTHON}" -m venv venv
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\pip.exe install -r requirements.txt
                    venv\\Scripts\\pip.exe install flake8
                """
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 syntax check...'
                bat """
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python.exe -m flake8 app.py --select=E9,F63,F7,F82 --show-source --statistics
                """
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running Pytest unit tests...'
                bat """
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\python.exe -m pytest tests/ -v --tb=short
                """
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