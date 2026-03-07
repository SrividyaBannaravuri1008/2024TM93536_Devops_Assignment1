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
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Lint') {
            steps {
                echo 'Running flake8 syntax check...'
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 app.py --select=E9,F63,F7,F82 --show-source --statistics
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                echo 'Running Pytest unit tests...'
                sh '''
                    . venv/bin/activate
                    python -m pytest tests/ -v --tb=short --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Docker Build') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Docker Test') {
            steps {
                echo 'Running tests inside Docker container...'
                sh """
                    docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} \
                        python -m pytest tests/ -v --tb=short
                """
            }
        }

    }

    post {
        success {
            echo "BUILD SUCCESS - ACEest image ${IMAGE_NAME}:${IMAGE_TAG} is ready."
        }
        failure {
            echo "BUILD FAILED - Check the logs above."
        }
        always {
            echo 'Cleaning up workspace...'
            sh 'rm -rf venv || true'
        }
    }
}
