

import FWCore.ParameterSet.Config as cms

import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt



process = cms.Process("AOD")

process.load('Configuration/StandardSequences/Services_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration.StandardSequences.GeometryExtended_cff')
#process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')




#process.GlobalTag.globaltag = 'START42_V11::All'
process.GlobalTag.globaltag = 'GR_P_V22::All'

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

#HLT_Photon15_TrackIso_L1R
process.load("Configuration.StandardSequences.EndOfProcess_cff")
#process.load("RecoTauTag.Configuration.FixedConeHighEffPFTaus_cfi")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.categories.append('InputTrackSelector')
process.MessageLogger.categories.append('KinematicTauProducer')
process.MessageLogger.categories.append('KinematicTauSkim')
process.MessageLogger.debugModules = cms.untracked.vstring('KinematicTauProducer', 'KinematicTauSkim')
process.MessageLogger.cerr = cms.untracked.PSet(
     threshold = cms.untracked.string('DEBUG'),
     FwkReport = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     InputTrackSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     KinematicTauProducer = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     KinematicTauSkim = cms.untracked.PSet(limit = cms.untracked.int32(-1))
)



process.source = cms.Source("PoolSource",
	fileNames = cms.untracked.vstring(
    'file:///home/home2/institut_3b/cherepanov/work/CMSSW_4_2_0/src/Ztautau/TauXPromptReco172_798.root'),
#    'file:///home/home2/institut_3b/cherepanov/work/CMSSW_4_2_0/src/Ztautau/SkimmingEff/BA94F49F-A29C-E011-A212-E0CB4EA0A908.root'),
    )


numberOfEvents = 500
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numberOfEvents)
)

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)





process.load("CommonTools.PrimVtxSelector.PrimVtxSelector_cfi")
process.load("RecoTauTag.KinematicTau.InputTrackSelector_cfi")
process.load("RecoTauTag.KinematicTau.ThreeProngInputSelector_cfi")
process.load("RecoTauTag.KinematicTau.kinematictau_cfi")
process.load("RecoTauTag.KinematicTau.kinematictauAdvanced_cfi")
process.load("RecoTauTag.KinematicTau.KinematicTauSkim_cfi")
process.load("TriggerFilter.Filter.triggerFilter_cfi")
process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")


process.load("SkimmingTools.EventCounter.countInput_cfi")
process.load("SkimmingTools.EventCounter.countTriggerPassed_cfi")
process.load("SkimmingTools.EventCounter.countKinFitPassed_cfi")
process.load("TauDataFormat.TauNtuple.tauntuple_cfi")




process.filter_1 = hlt.triggerResultsFilter.clone(
    hltResults = cms.InputTag( "TriggerResults", "", "HLT" ),
    triggerConditions =  ( 'HLT_IsoMu15_LooseIsoPFTau15_v8', ), #  data TauPlusX PromtReco-6
#    triggerConditions =  ( 'HLT_IsoMu12_LooseIsoPFTau10_v2', ),  #  trigger MC  DY sample 
    l1tResults = '',
    throw = False
    )


process.schedule = cms.Schedule()


process.KinFitSkim  = cms.Path(process.CountInputEvents*process.filter_1*process.CountTriggerPassedEvents*process.PrimVtxSelector*process.InputTrackSelector*process.ThreeProngInputSelector*process.KinematicTauProducer*process.KinematicTauSkim*process.CountKinFitPassedEvents*process.DetailedProducer*process.NtupleMaker)
#process.Ntuple      = cms.Path(process.NtupleMaker)
#process.skim_QualityTau = cms.Path(process.PrimVtxSelector*process.InputTrackSelector*process.ThreeProngInputSelector*process.KinematicTauProducer*process.KinematicTauSkim)

#process.schedule.append(process.TriggerSkim)
process.schedule.append(process.KinFitSkim)
#process.schedule.append(process.Ntuple)

#process.schedule.append(process.endjob_step)
#process.schedule.append(process.out_step)





#process.schedule.append(process.out_step)
#process.schedule.append(process.endjob_step)
