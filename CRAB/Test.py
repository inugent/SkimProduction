
import FWCore.ParameterSet.Config as cms
import os
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt


process = cms.Process("AOD")

process.load('Configuration/StandardSequences/Services_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

#<globaltag>
process.GlobalTag.globaltag = 'START52_V9::All'

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

#HLT_Photon15_TrackIso_L1R
process.load("Configuration.StandardSequences.EndOfProcess_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")


process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    #'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0000/D2E4D132-3D97-E111-88B2-003048673FC0.root'),
    'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/data/Run2012A/TauPlusX/AOD/13Jul2012-v1/0000/76C17B7B-98D7-E111-B500-20CF3027A639.root'),
                            
                            )

numberOfEvents = 500
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numberOfEvents)
)

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
)

####################### TauNtuple ######################
process.load("TriggerFilter.Filter.triggerFilter_cfi")
process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
process.load("SkimmingTools.SkimmingCuts.cuts_cfi")
process.load("TauDataFormat.TauNtuple.tauntuple_cfi")
process.load("TauDataFormat.TauNtuple.eventCounter_cfi")
process.EvntCounterA.DataMCType = cms.untracked.string("Data")#("<DataType>")
process.EvntCounterB.DataMCType = cms.untracked.string("Data")#("<DataType>")
process.CountTriggerPassedEvents = process.EvntCounterB.clone()
process.CountTriggerPassedEvents.CounterType = cms.untracked.string("CountTriggerPassedEvents")
process.CountKinFitPassedEvents = process.EvntCounterB.clone()
process.CountKinFitPassedEvents.CounterType = cms.untracked.string("CountKinFitPassedEvents")

####################### MET corrections ######################
process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
process.pfJetMETcorr.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")
process.load("JetMETCorrections.Type1MET.pfMETCorrections_cff")
process.load("JetMETCorrections.Type1MET.pfMETCorrectionType0_cfi")
process.pfType1CorrectedMet.applyType0Corrections = cms.bool(False)
process.pfType1CorrectedMet.srcType1Corrections = cms.VInputTag(
    cms.InputTag('pfMETcorrType0'),
    cms.InputTag('pfJetMETcorr', 'type1')        
)

####################### MET corrections ######################
process.endjob_step = cms.Path(process.endOfProcess)

###### New HPS
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")
###### New HPS

debugging = True
#debugging = False
if debugging:
    base = os.path.relpath(os.environ.get('CMSSW_BASE'))+'/src'
else:
    base = 'src'
    
process.NtupleMaker.PUInputFile = cms.untracked.string(base+'/data/Lumi_190456_208686MC_PU_S10_andData.root') #pu_whole2012.root');
process.NtupleMaker.EleMVAWeights1 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat1.weights.xml')
process.NtupleMaker.EleMVAWeights2 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat2.weights.xml')
process.NtupleMaker.EleMVAWeights3 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat3.weights.xml')
process.NtupleMaker.EleMVAWeights4 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat4.weights.xml')
process.NtupleMaker.EleMVAWeights5 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat5.weights.xml')
process.NtupleMaker.EleMVAWeights6 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat6.weights.xml')
process.NtupleMaker.ElectronMVAPtCut = cms.double(28.0);
process.NtupleMaker.PFTauTIPTag = cms.InputTag("hpsPFTauTransverseImpactParameters")

process.schedule = cms.Schedule()

process.TauNutpleSkim  = cms.Path(process.EvntCounterA*process.MultiTrigFilter*process.TrigFilterInfo*process.MuonPreselectionCuts*process.CountTriggerPassedEvents*process.PFTau*process.PreselectionCuts*process.type0PFMEtCorrection*process.producePFMETCorrections*process.EvntCounterB*process.NtupleMaker)
#process.recoTauClassicHPSSequence
process.schedule.append(process.TauNutpleSkim)



