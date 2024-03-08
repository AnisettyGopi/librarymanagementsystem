pipeline {

  environment {
    dockerimagename = "anisettygopi/flask"
    dockerImage = ""
  }

  agent any

  stages {

    stage('Checkout Source') {
      steps {
        git 'https://github.com/AnisettyGopi/librarymanagementsystem.git'
      }
    }

    stage('Build image') {
      steps{
        script {
          dockerImage = docker.build dockerimagename
        }
      }
    }

    stage('Pushing Image') {
      environment {
               registryCredential = 'dockerhublogin'
           }
      steps{
        script {
          docker.withRegistry( 'https://registry.hub.docker.com', registryCredential ) {
            dockerImage.push("lms")
          }
        }
      }
    }

    stage('Deploying App to Kubernetes') {
      steps {
        sh "echo deploying"
      }
    }

  }

}