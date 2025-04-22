pipeline {
    agent {
        label 'llrgrhgtrig.in2p3.fr'
    }
    environment {
        LABEL_TEST='test'
        LABEL_REF='ref'
        CONFIG_SUBSET = 'default_multi_subset'
    }
    options {
        skipDefaultCheckout()
        buildDiscarder logRotator(artifactDaysToKeepStr: '7', artifactNumToKeepStr: '', daysToKeepStr: '', numToKeepStr: '')
    }
    stages {
        stage('Set environment variables'){
            steps{
                sh '''
                set +x
                echo '==> Set environment variables'
                exec >> log_Jenkins
                if [ -f "log_Jenkins" ]; then
                    echo "Remove the last created log_Jenkins."
                    rm log_Jenkins
                else 
                    echo "log_Jenkins does not exist."
                fi 
                echo '==> Set environment variables'
                '''
                script{
                    String s = env.JOB_NAME
                    String[] elements = s.split("/")
                    String job_name = elements[-2]
                    println(job_name);
                    switch(job_name){
                       case 'HGC TPG CMSSW Validation':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_MAIN
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_MAIN
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_MAIN
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_MAIN
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_PROD
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Automatic Validation - TEST':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_TEST
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_TEST
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_TEST
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Automatic Validation - TEST ebecheva':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_EB
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_EB
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_EB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_EB
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Automatic Validation - TEST jbsauvan':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_JB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_JB
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_JB
                            env.BRANCH_HGCTPGVAL=env.HGCTPG_BRANCH_VAL_JB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_JB
                            env.JOB_FLAG=0
                            break
                        case 'HGC TPG Validation Validation':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_MAIN
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_MAIN
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_VALTEST
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CODE_TEST
                            env.JOB_FLAG=1
                            break
                        case 'HGC TPG Dev Validation - ebecheva':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_EB
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_EB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_EB
                            env.JOB_FLAG=1
                            break
                        case 'HGC TPG Validation - org':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_EB_org
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_EB
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_EB
                            env.JOB_FLAG=1
                            break
                        case 'CMSSW Dev Validation - org':
                            env.EMAIL_TO=env.HGCTPG_EMAIL_TO_EB
                            env.BASE_REMOTE=env.HGCTPG_BASE_REMOTE_EB_org
                            env.REMOTE_HGCTPGVAL=env.BASE_REMOTE
                            env.DATA_DIR=env.HGCTPG_DATA_DIR_EB
                            env.BRANCH_HGCTPGVAL='Jenkins-feature-modularJenkinsfile'
                            env.WEBPAGES_VAL=env.HGCTPG_WEBPAGES_VAL_CMSSW_TEST_EB
                            env.JOB_FLAG=0    
                        default: 
                            println("The job name is unknown"); 
                            break
                    }
                    
                    if (env.JOB_FLAG=='1'){
                        
                        env.BRANCH_HGCTPGVAL=env.CHANGE_BRANCH
                        env.CHANGE_TARGET_HGCTPGVAL=env.CHANGE_TARGET
                        
                        if (env.CHANGE_FORK){
                            env.REMOTE_HGCTPGVAL = env.CHANGE_FORK
                        }
                        else {
                            env.REMOTE_HGCTPGVAL = env.BASE_REMOTE
                        }
                    }
                    
                    println(env.REMOTE_HGCTPGVAL)
                    println(env.BRANCH_HGCTPGVAL)
                    
                    
                    println(env.BASE_REMOTE)
                    println(env.DATA_DIR)
                    println(env.CHANGE_TARGET)
                    println(env.CHANGE_BRANCH)
                    println(env.CHANGE_URL)
                    println(env.CHANGE_FORK)
                }
            }  
        }
        stage('Initialize'){
            stages{
                stage('Install automatic validation package HGCTPGValidation') {
                    steps {
                        sh '''
                        set +x
                        echo '==> Install automatic validation package HGCTPGValidation. ============================'
                        exec >> log_Jenkins
                        echo '==> Install automatic validation package HGCTPGValidation. ============================'
                        uname -a
                        whoami
                        pwd
                        ls -l
                        if [ -d "./HGCTPGValidation" ] 
                        then
                            rm -rf HGCTPGValidation
                        fi
                        git clone -b ${BRANCH_HGCTPGVAL} https://github.com/${REMOTE_HGCTPGVAL}/HGCTPGValidation HGCTPGValidation
                        source HGCTPGValidation/env_install.sh
                        pip install attrs
                        ls -lrt ..
                        echo '   '
                        '''
                    }
                }
                stage('Clean the working environment'){
                    steps{
                        sh '''
                        ./HGCTPGValidation/scripts/clean_environment.sh ${DATA_DIR} PR$CHANGE_ID
                        mkdir test_dir
                        '''
                    }
                }
                stage('Set CMSSW environment variables'){
                    steps{
                        script{
                            sh '''
                            set +x
                            echo 'echo ==> Set CMSSW environment variables. ============================'
                            exec >> log_Jenkins
                            echo 'echo ==> Set CMSSW environment variables. ============================'
                            '''
                            try {
                                def set_var = load './HGCTPGValidation/scripts/set_CMSSW_env_variables.groovy'
                                set_var.run(env.JOB_FLAG, env.CHANGE_FORK, env.BASE_REMOTE)
                            } catch (e) {
                                echo "Error during loading or execution: ${e}"
                            }
                            println("The environment variables are:")
                            
                            echo "The variables are:"
                            echo "JOB_FLAG: ${JOB_FLAG}"
                            echo "CHANGE_BRANCH: ${CHANGE_BRANCH}"
                            echo "CHANGE_TARGET: ${CHANGE_TARGET}"
                            echo "REF_RELEASE: ${REF_RELEASE}"
                            echo "TEST_RELEASE: ${TEST_RELEASE}"
                            echo "SCRAM_ARCH: ${SCRAM_ARCH}"
                            echo "BASE_REMOTE: ${BASE_REMOTE}"
                            echo "REMOTE: ${REMOTE}"
                        }
                        sh '''
                        set +x
                        exec >> log_Jenkins
                        echo '  '
                        '''
                    }
                }
            }
        }
        stage('Install CMSSW Test release'){
            steps {
                sh '''
                ./HGCTPGValidation/scripts/installCMSSW_global.sh $SCRAM_ARCH $REF_RELEASE $REMOTE $BASE_REMOTE $CHANGE_BRANCH $CHANGE_TARGET ${LABEL_TEST}
                echo '     '
                '''
            }
        }
        stage('Quality Checks'){
            steps{
                sh '''
                ./HGCTPGValidation/scripts/quality_checks.sh ${REF_RELEASE} ${LABEL_TEST}
                '''
            }
        }
        stage('Compare with CMSSW Ref Release'){
            stages{
                stage('Install Ref Release'){
                    steps {
                        sh '''
                        ./HGCTPGValidation/scripts/installCMSSW_global.sh $SCRAM_ARCH $REF_RELEASE $BASE_REMOTE $BASE_REMOTE $CHANGE_TARGET $CHANGE_TARGET ${LABEL_REF}
                        echo '      '
                        '''
                    }
                }
                stage('Produce Ref'){
                    steps {
                        sh '''
                        set +x
                        echo '===> Produce reference data.'
                        exec >> log_Jenkins
                        echo '===> Produce reference data.'
                        pwd
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_REF}
                        echo '      '
                        '''
                    }
                }
                stage('Produce Test'){
                    steps {
                        sh '''
                        set +x
                        echo '===> Produce test data.'
                        exec >> log_Jenkins
                        echo '===> Produce test data.'
                        pwd
                        cd test_dir/${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src
                        module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/
                        module purge
                        module load python/3.9.9
                        python --version
                        echo ' CONFIG_SUBSET = ' ${CONFIG_SUBSET}
                        echo 'LABEL_TEST = ' ${LABEL_TEST}
                        echo 'SCRAM_ARCH = ' ${SCRAM_ARCH}
                        python ../../../HGCTPGValidation/scripts/produceData_multiconfiguration.py --subsetconfig ${CONFIG_SUBSET} --label ${LABEL_TEST}
                        echo '      '
                        '''
                    }
                }
                stage('Display') {
                    steps {
                        sh '''
                        set +x
                        echo '==> Display ======================='
                        exec >> log_Jenkins
                        echo '==> Display ======================='
                        cd test_dir
                        source ../HGCTPGValidation/env_install.sh
                        echo $PWD
                        python ../HGCTPGValidation/scripts/displayHistos.py --subsetconfig ${CONFIG_SUBSET} --refdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_REF}/src --testdir ${REF_RELEASE}_HGCalTPGValidation_${LABEL_TEST}/src --datadir ${DATA_DIR} --prnumber $CHANGE_ID --prtitle "$CHANGE_TITLE (from $CHANGE_AUTHOR, $CHANGE_URL)"
                        echo '      '
                        '''
                    }
                }
            }
        }
        stage('Geom Check') {
            steps {
                echo '==> Geom Check'
                script{
                    try{
                        sh'./HGCTPGValidation/scripts/geom_check.sh ${TEST_RELEASE} ${LABEL_TEST}'
                    } catch (e){
                        error("An error occured in Geom testing stage: ${e}")
                    }
                }
            }
        }
    }
    post {
        always {
            script{
                if ( env.JOB_FLAG=='1' ) {    
                    env.CHANGE_BRANCH = env.BRANCH_HGCTPGVAL
                    env.CHANGE_TARGET = env.CHANGE_TARGET_HGCTPGVAL
                    println( "Validation of the validation: Set the original name of CHANGE_BRANCH => " + env.CHANGE_BRANCH )
                }
                
                def message = ""
                if (currentBuild.result == 'SUCCESS') {
                    message = "The validation checks have passed." + "<br>" + "The comparison histograms are available [here](${env.WEBPAGES_VAL}list_config.php?pr=/PR$CHANGE_ID)"
                } else if (currentBuild.result == 'FAILURE') {
                    message = "Some of the validation checks have failed." + "<br>" + "More details can be found [here](${env.CHANGE_URL}/checks)"
                
                }
                
                withEnv(["MESSAGE=${message}","url=${env.CHANGE_URL}"]) {
                    // Generate a token, the command "set +x" is mandatory
                    sh '''
                        ./HGCTPGValidation/scripts/write_toGitHub.sh "$url" "$MESSAGE"
                    '''
                }
            }
            archiveArtifacts artifacts: 'log_Jenkins, test_dir/**/src/test_triggergeom.root', fingerprint: true
        }
        success {
            echo 'The job finished successfully.'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job succeded: ${currentBuild.fullDisplayName}",
                 body:  "The job finished successfully. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} \n\n and ${env.CHANGE_URL} to view the results.  \n\n The validation histograms are available at ${env.WEBPAGES_VAL}list_config.php?pr=/PR$CHANGE_ID \n\n"
        }
        failure {
            echo 'Job failed'
            mail to: "${EMAIL_TO}",
                 subject: "Jenkins job failed: ${currentBuild.fullDisplayName}",
                 body: "The compilation or the build steps failed. \n\n Pull request: ${env.BRANCH_NAME} build number: #${env.BUILD_NUMBER} \n\n Title: ${env.CHANGE_TITLE} \n\n Author of the PR: ${env.CHANGE_AUTHOR} \n\n Target branch: ${env.CHANGE_TARGET} \n\n Feature branch: ${env.CHANGE_BRANCH} \n\n Check console output at ${env.BUILD_URL} \n\n and ${env.CHANGE_URL} to view the results.  \n\n The validation histograms are available at ${env.WEBPAGES_VAL} \n\n"
        }
    }
}
