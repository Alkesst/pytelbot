@Library('jenkings') _

pipeline {
    agent none
    stages {
        stage('Preparation & Build') {
            agent {
                label 'docker-qemu'
            }

            environment {
                img = null
                img8 = null
            }

            stages {
                stage('Checks') {
                  agent {
                    docker {
                      label 'docker'
                      image 'python:3.7-buster'
                      args '-e HOME=$WORKSPACE -e PATH=$PATH:$WORKSPACE/.local/bin'
                    }
                  }

                  steps {
                    script {
                      sh 'pip install --user -r requirements.txt'
                      // Checks that every file can be compiled (aka checks for syntax errors)
                      sh 'find main.py pytel_bot -type f -name \'*.py\' | xargs -n1 python3 -m py_compile'
                    }
                  }
                }
                
                stage('Build Image') {
                    when { expression { BRANCH_NAME ==~ /master|dev/ } }
                    steps {
                        script {
                            img = docker.build('alkesst/pytelbot:armv7', '--pull -f Dockerfile-armv7 .')
                            img8 = docker.build('alkesst/pytelbot:armv8', '--pull -f Dockerfile-armv8 .')
                        }
                    }
                }

                stage('Push dev image') {
                    when { branch 'dev' }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'alkesst_dockerhub') {
                                img.push('armv7-dev')
                                img8.push('armv8-dev')
                            }
                        }
                    }
                }

                stage('Push image') {
                    when { branch 'master' }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'alkesst_dockerhub') {
                                img.push('armv7')
                                img8.push('armv8')
                            }
                        }
                    }
                }
            }
        }

        stage('Deployment'){
            agent {
                node {
                    label 'majorcadevs'
                }
            }
            when { branch 'master' }
            steps {
                sshagent(credentials : ['casita-rpi']) {
                    script {
                        sh 'ssh -o StrictHostKeyChecking=no -p 1223 -l ubuntu casita.melchor9000.me "cd ./docker/pytelbot && docker-compose pull bot && docker-compose up -d bot"'
                    }
                }
            }
        }
    }
}
