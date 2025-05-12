# AWS EC2 Start-Stop Lambda Function

A serverless AWS Lambda function to automatically start or stop EC2 instances based on tags.

## Overview

This project provides a simple AWS Lambda function that can be used to start stopped instances and stop running instances based on a specified tag (`auto-start-stop: yes`). This is useful for cost optimization, especially for development or test environments that don't need to run 24/7.

## Features

- Automatically start EC2 instances that are in a stopped state
- Automatically stop EC2 instances that are in a running state
- Target specific instances using AWS tags
- Easily deployable as an AWS Lambda function

## Prerequisites

- Python 3.8 or higher
- AWS account with appropriate permissions
- Boto3 (AWS SDK for Python)
- For development: pytest and pytest-cov

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/aws-start-stop.git
   cd aws-start-stop
   ```

2. Install dependencies:
   ```bash
   pip install boto3 pytest pytest-cov
   ```

## Testing

This project uses unit tests to ensure functionality and maintain code quality. We also use code coverage reporting to ensure comprehensive test coverage.

### Running Tests

To run basic tests:

```bash
python -m unittest test_unit.py
```

### Running Tests with Coverage

For test execution with coverage reporting:

```bash
# Run tests with coverage
python -m coverage run --source=startstopec2 -m unittest test_unit.py

# Generate terminal coverage report
python -m coverage report -m

# Generate XML coverage report for SonarQube
python -m coverage xml
```

### Integrating with SonarQube

The project includes a `sonar-project.properties` file for SonarQube integration. To use SonarQube for code quality analysis:

1. Make sure SonarQube is installed and running
2. Run tests with coverage as described above
3. Run the SonarQube scanner:
   ```bash
   sonar-scanner
   ```

The configuration in `sonar-project.properties` specifies:
- Project identification
- Source code location
- Path to coverage reports
- Exclusions for test files

### Jenkins CI/CD Integration

To automate testing and code coverage in Jenkins, you can use the following Jenkinsfile (Groovy) example:

```groovy
pipeline {
    agent {
        // Specify the execution environment
        docker {
            image 'python:3.10'
        }
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh 'pip install boto3 pytest pytest-cov'
                sh 'pip install -r requirements.txt || true'
            }
        }
        
        stage('Test') {
            steps {
                // Run tests with coverage
                sh 'python -m coverage run --source=startstopec2 -m unittest test_unit.py'
                // Generate coverage reports
                sh 'python -m coverage xml'
                sh 'python -m coverage report -m'
            }
        }
        
        stage('SonarQube Analysis') {
            environment {
                // Define SonarQube environment variables if needed
                SONAR_HOST_URL = 'http://your-sonarqube-server:9000'
            }
            steps {
                // Use the SonarQube Scanner Jenkins plugin
                withSonarQubeEnv('SonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                // Wait for quality gate response
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'  // Only deploy from main branch
            }
            steps {
                // Add deployment steps for AWS Lambda
                echo 'Deploying to AWS Lambda...'
                // Example: use AWS CLI or Serverless Framework to deploy
                // sh 'aws lambda update-function-code --function-name aws-start-stop --zip-file fileb://deployment.zip'
            }
        }
    }
    
    post {
        always {
            // Publish test results
            junit allowEmptyResults: true, testResults: '**/test-results/*.xml'
            
            // Publish coverage reports in Jenkins
            publishCoverage adapters: [coberturaAdapter('coverage.xml')], 
                            sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
            
            // Clean workspace
            cleanWs()
        }
    }
}

## Function Usage

To use the Lambda function in your AWS environment:

1. Deploy the `startstopec2.py` file as an AWS Lambda function
2. Set up appropriate IAM permissions for EC2 actions
3. Tag your EC2 instances with `auto-start-stop: yes` to include them in the automation
4. Set up a CloudWatch Events trigger to run the function on your desired schedule

## Additional CI/CD Integration Examples

### GitHub Actions Workflow

Create a file `.github/workflows/python-test.yml` with the following content:

```yaml
name: Python Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install boto3 pytest pytest-cov
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        
    - name: Test with coverage
      run: |
        python -m coverage run --source=startstopec2 -m unittest test_unit.py
        python -m coverage xml
        python -m coverage report -m
        
    - name: SonarCloud Scan
      uses: SonarSource/sonarcloud-github-action@master
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

### GitLab CI Configuration

Create a file `.gitlab-ci.yml` with the following content:

```yaml
image: python:3.10

stages:
  - test
  - quality

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

cache:
  paths:
    - .pip-cache/

test:
  stage: test
  script:
    - pip install boto3 pytest pytest-cov
    - if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - python -m coverage run --source=startstopec2 -m unittest test_unit.py
    - python -m coverage xml
    - python -m coverage report -m
  artifacts:
    paths:
      - coverage.xml
    expire_in: 1 day

sonarqube-check:
  stage: quality
  image: 
    name: sonarsource/sonar-scanner-cli:latest
    entrypoint: [""]
  dependencies:
    - test
  script:
    - sonar-scanner -Dsonar.projectKey=${CI_PROJECT_NAME} -Dsonar.qualitygate.wait=true
  only:
    - main
    - merge_requests
```

## Contributing

Contributions to improve the function or expand its capabilities are welcome. Please ensure that:

1. Your code passes all tests
2. You maintain or improve the current code coverage
3. You update documentation as needed

## License

[Specify your license here]