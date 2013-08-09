import FWCore.ParameterSet.Config as cms
import os
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt

process = cms.Process("AOD")

process.load('Configuration/StandardSequences/Services_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

<globaltag>
#process.GlobalTag.globaltag = 'START52_V9::All'

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

process.load("Configuration.StandardSequences.EndOfProcess_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")


process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    #'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0000/D2E4D132-3D97-E111-88B2-003048673FC0.root'),
    'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/data/Run2012A/TauPlusX/AOD/13Jul2012-v1/0000/76C17B7B-98D7-E111-B500-20CF3027A639.root'),
                            )

numberOfEvents = 5000
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(numberOfEvents)
    )

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
    )

####################### TauNtuple ######################
process.load("TauDataFormat.TauNtuple.triggerFilter_cfi")
process.load("TauDataFormat.TauNtuple.cuts_cfi")
process.load("TauDataFormat.TauNtuple.tauntuple_cfi")
process.load("TauDataFormat.TauNtuple.eventCounter_cfi")
#process.EvntCounterA.DataMCType = cms.untracked.string("Data")
#process.EvntCounterB.DataMCType = cms.untracked.string("Data")
process.EvntCounterA.DataMCType = cms.untracked.string("<DataType>")
process.EvntCounterB.DataMCType = cms.untracked.string("<DataType>")
process.CountTriggerPassedEvents = process.EvntCounterB.clone()
process.CountTriggerPassedEvents.CounterType = cms.untracked.string("CountTriggerPassedEvents")
process.CountKinFitPassedEvents = process.EvntCounterB.clone()
process.CountKinFitPassedEvents.CounterType = cms.untracked.string("CountKinFitPassedEvents")

####################### Jet corrections ######################
process.load("JetMETCorrections.Configuration.JetCorrectionServicesAllAlgos_cff")
process.load("JetMETCorrections.Configuration.DefaultJEC_cff")

# this should load the correction service and the corresponding producers
# one producer is e.g. ak5PFJetsL1FastL2L3 (recommendated for MC) and ak5PFJetsL1FastL2L3Residual  (recommendated for data)
# run one of these to create a new branch which contains the corrected jets

if "<DataType>" == "Data":
    jetCorrectionProducer = process.ak5PFJetsL1FastL2L3Residual
    process.NtupleMaker.pfjets = cms.InputTag('ak5PFJetsL1FastL2L3Residual')
else:
    jetCorrectionProducer = process.ak5PFJetsL1FastL2L3
    process.NtupleMaker.pfjets = cms.InputTag('ak5PFJetsL1FastL2L3')
                        
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

#debugging = True
debugging = False
if debugging:
    base = os.path.relpath(os.environ.get('CMSSW_BASE'))+'/src'
else:
    base = 'src'
    
process.NtupleMaker.PUInputFile = cms.untracked.string(base+'/data/<Pile_Up_File>')
#process.NtupleMaker.PUInputFile = cms.untracked.string(base+'/data/Lumi_190456_208686MC_PU_S10_andData.root')
process.NtupleMaker.EleMVAWeights1 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat1.weights.xml')
process.NtupleMaker.EleMVAWeights2 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat2.weights.xml')
process.NtupleMaker.EleMVAWeights3 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat3.weights.xml')
process.NtupleMaker.EleMVAWeights4 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat4.weights.xml')
process.NtupleMaker.EleMVAWeights5 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat5.weights.xml')
process.NtupleMaker.EleMVAWeights6 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat6.weights.xml')
process.NtupleMaker.ElectronMVAPtCut = cms.double(10.0);

process.schedule = cms.Schedule()

process.NtupleMaker.doTrack= cms.untracked.bool(False)

process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu24_eta2p1_v","HLT_Mu17_Ele8_CaloIdL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdL",
"HLT_Mu8_Ele17_CaloIdT_CaloIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL")

process.TauNutpleSkim  = cms.Path(process.EvntCounterA*process.MultiTrigFilter*process.MuonPreselectionCuts*process.CountTriggerPassedEvents*process.PFTau*process.PreselectionCuts*jetCorrectionProducer*process.type0PFMEtCorrection*process.producePFMETCorrections*process.EvntCounterB*process.NtupleMaker)
process.schedule.append(process.TauNutpleSkim)



