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
            }

            stages {
                stage('Build Image') {
                    steps {
                        script {
                            img = docker.build('alkesst/pytelbot:armv7', '--pull -f Dockerfile-armv7 .')
                        }
                    }
                }

                stage('Push dev image') {
                    when { branch 'dev' }
                    steps {
                        script {
                            docker.withRegistry('https://registry.hub.docker.com', 'alkesst_dockerhub') {
                                img.push('armv7-dev')
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
                        sh 'ssh -o StrictHostKeyChecking=no -p 1223 -l pi casita.melchor9000.me "cd /home/pi/docker/pytelbot && docker-compose pull bot && docker-compose up -d bot"'
                    }
                }
            }
        }
    }

    post {
        success { 
            telegramSend 'Chavales, `s e l f` se ha actualizado\n\n@alkesst @melchor629', '-1001104881568'
        }
        failure {
            telegramSend 'Oh no, [build log](' + env.BUILD_URL + ')... @alkesst @melchor629', '-1001104881568'
        }
    }
}
