import FWCore.ParameterSet.Config as cms
import os
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt

process = cms.Process("TauNTuple")

process.load('Configuration/StandardSequences/Services_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

#<globaltag>
process.GlobalTag.globaltag = 'START52_V9::All'

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

######################################################
#
# load Pat
#
from PhysicsTools.PatAlgos.patTemplate_cfg import *
from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.metTools import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.pfTools import *

removeMCMatching(process, ['All'])

# Jet energy corrections to use:
if "<DataType>" == "Data":
    inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
else:
    inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute'])
process.patJetCorrFactors.useRho=False

# Add PF jets
switchJetCollection(process,cms.InputTag('ak5PFJets'),
                    doJTA        = True,
                    doBTagging   = True,
                    jetCorrLabel = inputJetCorrLabel,
                    doType1MET   = True,
                    genJetCollection=cms.InputTag("ak5GenJets"),
                    doJetID      = True
                    )
process.patJets.addTagInfos = True
process.patJets.tagInfoSources  = cms.VInputTag(
    cms.InputTag("secondaryVertexTagInfosAOD"),
    )


# load the PU JetID sequence
#process.load("CMGTools.External.pujetidsequence_cff") # should not be needed, is done below with MVA MET

# Select jets
process.selectedPatJets.cut = cms.string('pt > 18')

############ MET #############
# add pf met
switchToPFMET(process, input=cms.InputTag('pfMet')) #this adds uncorrected MET collection labelled "patMETs"

# produce corrected MET collections (RECO)
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")
if "<DataType>" == "Data":
    process.corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3Residual")
else:
    process.corrPfMetType1.jetCorrLabel = cms.string("ak5PFL1FastL2L3")

process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")
process.load("JetMETCorrections.Type1MET.correctedMet_cff")

# produce PAT MET collections
from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs
process.patPfMetT0pcT1 = patMETs.clone(
    metSource = cms.InputTag('pfMetT0pcT1'),
    addMuonCorrections = cms.bool(False),
    addGenMET    = cms.bool(False)
)
process.patPfMetT1 = patMETs.clone(
    metSource = cms.InputTag('pfMetT1'),
    addMuonCorrections = cms.bool(False),
    addGenMET    = cms.bool(False)
)

# compute PUJetID and MVA MET
process.load('JetMETCorrections.METPUSubtraction.mvaPFMET_leptons_cff')
process.pfMEtMVA.srcLeptons = cms.VInputTag("isomuons","isoelectrons","isotaus") # load default lepton selection (H2Tau) for MVA-MET
if "<DataType>" == "Data":
    process.calibratedAK5PFJetsForPFMEtMVA.correctors = cms.vstring("ak5PFL1FastL2L3Residual")
else:
    process.calibratedAK5PFJetsForPFMEtMVA.correctors = cms.string("ak5PFL1FastL2L3")
process.PUJetMVAMetSequence = cms.Sequence( process.pfMEtMVAsequence * process.pileupJetIdProducer)

process.JetMetSequence = cms.Sequence(process.correctionTermsPfMetType1Type2
                                      * process.correctionTermsPfMetType0PFCandidate
                                      * process.pfMetT0pcT1 
                                      * process.pfMetT1
                                      * process.patPfMetT0pcT1
                                      * process.patPfMetT1
                                      * process.PUJetMVAMetSequence)

#from PhysicsTools.PatUtils.metUncertaintyTools import runMEtUncertainties
#runMEtUncertainties(process)

####### done with setting up PAT
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(
    #'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/mc/Summer12/DYJetsToLL_M-50_TuneZ2Star_8TeV-madgraph-tarball/AODSIM/PU_S7_START52_V9-v2/0000/D2E4D132-3D97-E111-88B2-003048673FC0.root'),
    #'file://dcap://grid-dcap.physik.rwth-aachen.de/pnfs/physik.rwth-aachen.de/cms/store/data/Run2012A/TauPlusX/AOD/13Jul2012-v1/0000/76C17B7B-98D7-E111-B500-20CF3027A639.root'),
                                    '/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/000260A0-4286-E211-89DC-0030487F1F23.root',
                                    '/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/0085A19F-9187-E211-9305-0025901D484C.root',
                                    '/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/00DF9FCD-8986-E211-B337-0025901D4936.root',
                                    '/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/022E5139-5287-E211-9024-0030487F164D.root',
                                    '/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/023184C4-F487-E211-AC7C-0025904B144E.root')
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
process.NtupleMaker.ElectronMVAPtCut = cms.double(28.0);

# set Ntuple to run on PAT jets
process.NtupleMaker.doPatJets = cms.untracked.bool(True)
process.NtupleMaker.srcPatJets = cms.untracked.string("selectedPatJets")
process.NtupleMaker.doPatMET = cms.untracked.bool(True)
process.NtupleMaker.srcPatMET = cms.untracked.string("patMETsPF")

process.schedule = cms.Schedule()

process.NtupleMaker.doTrack= cms.untracked.bool(False)

process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu24_eta2p1_v","HLT_Mu17_Ele8_CaloIdL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdL",
"HLT_Mu8_Ele17_CaloIdT_CaloIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL")

process.TauNutpleSkim  = cms.Path(process.EvntCounterA
                                  * process.MultiTrigFilter
                                  * process.MuonPreselectionCuts
                                  * process.CountTriggerPassedEvents
                                  * process.patDefaultSequence
                                  * process.JetMetSequence
                                  * process.PFTau
                                  * process.PreselectionCuts
                                  * process.EvntCounterB
                                  * process.NtupleMaker)
process.schedule.append(process.TauNutpleSkim)



