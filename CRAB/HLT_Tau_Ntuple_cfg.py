

import FWCore.ParameterSet.Config as cms

import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt



process = cms.Process("AOD")

process.load('Configuration/StandardSequences/Services_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration.StandardSequences.GeometryExtended_cff')
#process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')



<globaltag>

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

#HLT_Photon15_TrackIso_L1R
process.load("Configuration.StandardSequences.EndOfProcess_cff")
#process.load("RecoTauTag.Configuration.FixedConeHighEffPFTaus_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")



process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
    'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/data/Run2011A/TauPlusX/AOD/08Nov2011-v1/0001/28F4BD62-2416-E111-922D-00261894395C.root'),
    )


numberOfEvents = 500
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numberOfEvents)
)

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)





process.load("CommonTools.PrimVtxSelector.PrimVtxSelector_cfi")


process.load("RecoTauTag.KinematicTau.KinematicFitSequences_cff")
process.load("RecoTauTag.KinematicTau.KinematicTauPostProcessing_cfi")


process.load('Configuration.StandardSequences.EDMtoMEAtJobEnd_cff')
process.load("Validation.Configuration.postValidation_cff")

process.schedule = cms.Schedule()

process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.EDMtoMEAtJobEnd_cff')
process.load('RecoTauTag.KinematicTau.KinematicTauPostProcessing_cfi')
process.load('RecoTauTag.KinematicTau.Tau_JAKID_Filter_cfi')
process.load('DQMServices.Components.MEtoEDMConverter_cfi')

process.dqmSaver.convention = 'Offline'
process.dqmSaver.saveByRun = cms.untracked.int32(-1)
process.dqmSaver.saveAtJobEnd = cms.untracked.bool(True)
process.dqmSaver.forceRunNumber = cms.untracked.int32(1)
process.dqmSaver.workflow = "/KinematicFitSequencewithDQM/VAL/RECO"
#process.DQMStore.verbose=1


process.load("TriggerFilter.Filter.triggerFilter_cfi")
process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
process.load("SkimmingTools.EventCounter.countInput_cfi")
process.load("SkimmingTools.EventCounter.countTriggerPassed_cfi")
process.load("SkimmingTools.EventCounter.countKinFitPassed_cfi")
process.load("SkimmingTools.SkimmingCuts.cuts_cfi")
process.load("TauDataFormat.TauNtuple.tauntuple_cfi")
process.load("TauDataFormat.TauNtuple.eventCounter_cfi")


process.endjob_step = cms.Path(process.endOfProcess)



###### New HPS
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
###### New HPS


process.filter_1 = hlt.triggerResultsFilter.clone(
    hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
#    triggerConditions =  ( 'HLT_IsoMu15_LooseIsoPFTau15_v8', ), #  data TauPlusX PromtReco-6
    triggerConditions =  ( 'HLT_IsoMu12_LooseIsoPFTau10_v2', ),  #  trigger MC  DY sample 
    l1tResults = '',
    throw = False
    )

process.EvntCounterA.DataMCType = cms.untracked.string("<DataType>");
process.EvntCounterB.DataMCType = cms.untracked.string("<DataType>");

process.NtupleMaker.PUInputFile = cms.untracked.string("$CMSSW_BASE/src/data/Lumi_190456_208686MCandData.root");

process.schedule = cms.Schedule()

process.KinFitSkim  = cms.Path(process.EvntCounterA*process.CountInputEvents*process.TrigFilter*process.TrigFilterInfo*process.CountTriggerPassedEvents*process.KinematicFitSequencewithSkim*process.CountKinFitPassedEvents*process.EvntCounterB*process.recoTauClassicHPSSequence*process.PreselectionCuts*process.NtupleMaker)



process.schedule.append(process.KinFitSkim)



