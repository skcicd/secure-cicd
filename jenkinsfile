pipeline {
    agent any
    
    stages {
        stage('Build') {
            steps {
                echo "Building for ${env.BRANCH_NAME}"
                // Common build steps
            }
        }
        
        stage('Test') {
                steps {
                    // Run on all branches
                    echo "Running unit tests for branch  ${env.BRANCH_NAME}"
                }

        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                // Production deployment steps
                echo "Deploying, branch: ${env.BRANCH_NAME}"
            }
        }
    }
}