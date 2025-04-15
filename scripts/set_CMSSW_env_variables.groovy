// set_CMSSW_env_variables.groovy

// This script is used in the Jenkinsfile pipeline, in the stage 'Set CMSSW environment variables'
// Usage:
// def set_var = load './HGCTPGValidation/scripts/set_CMSSW_env_variables.groovy'
// set_var.run(env.JOB_FLAG, env.CHANGE_FORK, env.BASE_REMOTE)

def run(String JOB_FLAG, String CHANGE_FORK, String BASE_REMOTE) {
    println('Input variables in the run function')
    println("${JOB_FLAG}")
    println("${CHANGE_FORK}")
    println("${BASE_REMOTE}")
    
    if ( JOB_FLAG == '0' ){
        env.REF_RELEASE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/extractReleaseName.sh ${CHANGE_TARGET}').trim()
        env.SCRAM_ARCH = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/getScramArch.sh ${REF_RELEASE}').trim()
        env.TEST_RELEASE = env.REF_RELEASE
                                
        // Checks if the CHANGE_BRANCH comes from the BASE_REMMOTE or from the FORK
        if ( CHANGE_FORK ){
            env.REMOTE = ${CHANGE_FORK}
        }
        else {
            env.REMOTE = ${BASE_REMOTE}
        }
            println(env.REF_RELEASE)
            println(env.SCRAM_ARCH)
            println(env.TEST_RELEASE)
            println(env.REMOTE)
    }
    else {
            env.REF_BRANCH = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/; module purge; module load python/3.9.9; python ./HGCTPGValidation/scripts/get_cmsswRefBranch.py').trim()
            env.REF_RELEASE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/extractReleaseName.sh ${REF_BRANCH}').trim()
            env.SCRAM_ARCH = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; source ./HGCTPGValidation/scripts/getScramArch.sh ${REF_RELEASE}').trim()
            env.BASE_REMOTE = sh(returnStdout: true, script: 'set +x exec >> log_Jenkins; module use /opt/exp_soft/vo.llr.in2p3.fr/modulefiles_el7/; module purge; module load python/3.9.9; python ./HGCTPGValidation/scripts/get_remoteParam.py').trim()
            env.CHANGE_BRANCH = env.REF_BRANCH
            env.CHANGE_TARGET = env.REF_BRANCH
            env.REMOTE = env.BASE_REMOTE
            env.TEST_RELEASE = env.REF_RELEASE
                                
            println(env.REF_BRANCH)
            println(env.REF_RELEASE)
            println(env.TEST_RELEASE)
            println(env.SCRAM_ARCH)
            println(env.BASE_REMOTE)
            println(env.CHANGE_BRANCH)
            println(env.CHANGE_TARGET)
            println(env.REMOTE)
    }
}

return this
