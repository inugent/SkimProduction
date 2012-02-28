

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
process.MessageLogger.categories.append('InputTrackSelector')
process.MessageLogger.categories.append('KinematicTauBasicProducer')
process.MessageLogger.categories.append('KinematicTauSkim')
process.MessageLogger.debugModules = cms.untracked.vstring('KinematicTauBasicProducer', 'KinematicTauSkim')
process.MessageLogger.cerr = cms.untracked.PSet(
     threshold = cms.untracked.string('DEBUG'),
     FwkReport = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     DEBUG = cms.untracked.PSet(limit = cms.untracked.int32(0)),
     InputTrackSelector = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     KinematicTauBasicProducer = cms.untracked.PSet(limit = cms.untracked.int32(-1)),
     KinematicTauSkim = cms.untracked.PSet(limit = cms.untracked.int32(-1))
)



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
process.load("RecoTauTag.KinematicTau.InputTrackSelector_cfi")
process.load("RecoTauTag.KinematicTau.ThreeProngInputSelector_cff")
process.load("RecoTauTag.KinematicTau.ThreeProngInputSelector_Step2_cfi")
process.load("RecoTauTag.KinematicTau.ThreeProngInputSelector_Step1_cfi")
process.load("RecoTauTag.KinematicTau.kinematictau_cfi")
process.load("RecoTauTag.KinematicTau.kinematictauAdvanced_cfi")
process.load("RecoTauTag.KinematicTau.KinematicTauSkim_cfi")
process.load("TriggerFilter.Filter.triggerFilter_cfi")
process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")


process.load("SkimmingTools.EventCounter.countInput_cfi")
process.load("SkimmingTools.EventCounter.countTriggerPassed_cfi")
process.load("SkimmingTools.EventCounter.countKinFitPassed_cfi")
process.load("TauDataFormat.TauNtuple.tauntuple_cfi")
process.load("TauDataFormat.TauNtuple.eventCounter_cfi")


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

process.NtupleMaker.PUInputFile = cms.untracked.string("$CMSSW_BASE/src/data/Lumi_160404_180252_andMC_Flat_Tail.root");

process.schedule = cms.Schedule()

process.KinFitSkim  = cms.Path(process.EvntCounterA*process.CountInputEvents*process.TrigFilter*process.CountTriggerPassedEvents*process.PrimVtxSelector*process.InputTrackSelector*process.ThreeProngInputSelector*process.KinematicTauBasicProducer*process.KinematicTauSkim*process.CountKinFitPassedEvents*process.KinematicTauProducer*process.EvntCounterB*process.NtupleMaker)

process.schedule.append(process.KinFitSkim)



