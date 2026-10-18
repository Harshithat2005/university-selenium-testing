
pipeline {
    agent any

    tools {
        maven 'Maven-3.10'
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Harshithat2005/university-selenium-testing.git'
            }
        }

        stage('Run Selenium Tests') {
            steps {
                bat 'mvn clean test'
            }
        }
    }

    post {
        always {
            junit testResults: 'target/surefire-reports/*.xml',
                  allowEmptyResults: true
        }
        success {
            echo 'All Selenium tests passed!'
        }
        failure {
            echo 'Build failed. Check Console Output.'
        }
    }
}
