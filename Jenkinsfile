pipeline {
    agent any

    environment {
        IMAGE_NAME = "aceest-fitness"
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
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
                    "${PYTHON}" -m pip install --upgrade pip
                    "${PIP}" install -r requirements.txt
                """
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 syntax check...'
                bat """
                    call venv\\Scripts\\activate.bat
                    "${PIP}" install flake8
                    venv\\Scripts\\flake8.exe app.py --select=E9,F63,F7,F82 --show-source --statistics
                """
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running Pytest unit tests...'
                bat """
                    call venv\\Scripts\\activate.bat
                    venv\\Scripts\\pytest.exe tests/ -v --tb=short
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