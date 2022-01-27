#!/bin/bash

# ./produceData.sh
# $1 label "ref" or "test"
# $2 procModifier 

echo "label " $1
echo "procModifiers " $2

source /cvmfs/cms.cern.ch/cmsset_default.sh
echo $PWD
eval `scramv1 runtime -sh`
if [[ -n $2 ]] #if not empty
then
  cmsDriver.py hgcal_tpg_validation -n 50 + \
  --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW + \
  --conditions auto:phase2_realistic + \
  --beamspot HLLHC14TeV + \
  --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation + \
  --geometry Extended2026D49 --era Phase2C9 --procModifiers $2 + \
  --inputCommands "keep *","drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT","drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT","drop l1tEMTFHit2016s_simEmtfDigis__HLT","drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT","drop l1tEMTFTrack2016s_simEmtfDigis__HLT" + \
  --filein file:/data_CMS_upgrade/becheva/data_jenkins/003F2BA9-0D02-5A43-A53F-4161E513BFA6.root + \
  --no_output + \
  --customise_commands "process.MessageLogger.files.out_$1 = dict(); process.Timing = cms.Service('Timing', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service('SimpleMemoryCheck', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
else
  cmsDriver.py hgcal_tpg_validation -n 50 + \
  --mc --eventcontent FEVTDEBUG --datatier GEN-SIM-DIGI-RAW + \
  --conditions auto:phase2_realistic + \
  --beamspot HLLHC14TeV + \
  --step USER:Validation/HGCalValidation/hgcalRunEmulatorValidationTPG_cff.hgcalTPGRunEmulatorValidation + \
  --geometry Extended2026D49 --era Phase2C9 + \
  --inputCommands "keep *","drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT","drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT","drop l1tEMTFHit2016s_simEmtfDigis__HLT","drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT","drop l1tEMTFTrack2016s_simEmtfDigis__HLT" + \
  --filein file:/data_CMS_upgrade/becheva/data_jenkins/003F2BA9-0D02-5A43-A53F-4161E513BFA6.root + \
  --no_output + \
  --customise_commands "process.MessageLogger.files.out_$1 = dict(); process.Timing = cms.Service('Timing', summaryOnly = cms.untracked.bool(False), useJobReport = cms.untracked.bool(True)); process.SimpleMemoryCheck = cms.Service('SimpleMemoryCheck', ignoreTotal = cms.untracked.int32(1)); process.schedule = cms.Schedule(process.user_step)"
fi
