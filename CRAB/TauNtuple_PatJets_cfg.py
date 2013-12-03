import FWCore.ParameterSet.Config as cms
import os
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt

process = cms.Process("TauNTuple")

process.load('Configuration/StandardSequences/Services_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.StandardSequences.GeometryDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")

<globaltag>
#process.GlobalTag.globaltag = 'START52_V9::All'

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")

######################################################
#
# load Pat
process.load("PhysicsTools.PatAlgos.patSequences_cff")
from PhysicsTools.PatAlgos.tools.coreTools import removeMCMatching
from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection
from PhysicsTools.PatAlgos.tools.pfTools import switchToPFMET

removeMCMatching(process, outputModules=[])

# Jet energy corrections to use:
if "<DataType>" == "Data":
    inputJetCorrLabel = ('AK5PF', ['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
else:
    inputJetCorrLabel = ('AK5PF', ['L1FastJet', 'L2Relative', 'L3Absolute'])
#process.patJetCorrFactors.useRho=False

# Add PF jets
switchJetCollection(process,cms.InputTag('ak5PFJets'),
                    doJTA        = True,
                    doBTagging   = True,
                    jetCorrLabel = inputJetCorrLabel,
                    doType1MET   = True,
                    genJetCollection=cms.InputTag("ak5GenJets"),
                    doJetID      = True,
                    outputModules= []
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
switchToPFMET(process, input=cms.InputTag('pfMet')) #this adds uncorrected MET collection labeled "patMETs"

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

# PUJetID following the instructions given here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJetID
process.load("CMGTools.External.pujetidsequence_cff")
#process.puJetId.algos = cms.VPSet(full_53x,cutbased,PhilV1)

# to use MVA-MET + PUJetID, uncomment the 2 sections below
'''# compute PUJetID (https://twiki.cern.ch/twiki/bin/view/CMS/HiggsToTauTauWorkingSummer2013#MVA_JET_Id)
from RecoJets.JetProducers.PileupJetID_cfi import *
stdalgos = cms.VPSet(full_53x,cutbased,PhilV1)
process.puJetMva = cms.EDProducer('PileupJetIdProducer',
    produceJetIds = cms.bool(True),
    jetids = cms.InputTag(""),
    runMvas = cms.bool(True),
    jets = cms.InputTag("ak5PFJets"),
    vertexes = cms.InputTag("offlinePrimaryVertices"),
    algos = cms.VPSet(stdalgos),
    rho     = cms.InputTag("kt6PFJets","rho"),
    jec     = cms.string("AK5PF"),
    applyJec = cms.bool(True),
    inputIsCorrected = cms.bool(False),
    residualsFromTxt = cms.bool(False),
    residualsTxt     = cms.FileInPath("RecoJets/JetProducers/data/dummy.txt"),
)'''

# compute MVA MET
'''process.load('JetMETCorrections.METPUSubtraction.mvaPFMET_leptons_cff')
process.pfMEtMVA.srcLeptons = cms.VInputTag("isomuons","isoelectrons","isotaus") # load default lepton selection (H2Tau) for MVA-MET
if "<DataType>" == "Data":
    process.calibratedAK5PFJetsForPFMEtMVA.correctors = cms.vstring("ak5PFL1FastL2L3Residual")
else:
    process.calibratedAK5PFJetsForPFMEtMVA.correctors = cms.string("ak5PFL1FastL2L3")
process.patPfMetMVA = patMETs.clone(
    metSource = cms.InputTag('pfMEtMVA'),
    addMuonCorrections = cms.bool(False),
    addGenMET    = cms.bool(False)
)
process.PUJetMVAMetSequence = cms.Sequence( process.pfMEtMVAsequence * process.puJetMva * process.patPfMetMVA)
'''
process.JetMetSequence = cms.Sequence(process.correctionTermsPfMetType1Type2
                                      * process.correctionTermsPfMetType0PFCandidate
                                      * process.pfMetT0pcT1 
                                      * process.pfMetT1
                                      * process.patPfMetT0pcT1
                                      * process.patPfMetT1
                                      * process.puJetIdSqeuence) # use this to run PUJetID alone
                                      #* process.PUJetMVAMetSequence) # use this for MVA-MET + PUJetID

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
# weight files for triggering MVA w/o IP
process.NtupleMaker.EleMVATrigNoIPWeights1 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat1.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights2 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat2.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights3 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat3.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights4 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat4.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights5 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat5.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights6 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigNoIPV0_2012_Cat6.weights.xml')
# weight files for non triggering MVA
process.NtupleMaker.EleMVANonTrigWeights1 = cms.untracked.string(base+'/data/Electrons_BDTG_NonTrigV0_Cat1.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights2 = cms.untracked.string(base+'/data/Electrons_BDTG_NonTrigV0_Cat2.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights3 = cms.untracked.string(base+'/data/Electrons_BDTG_NonTrigV0_Cat3.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights4 = cms.untracked.string(base+'/data/Electrons_BDTG_NonTrigV0_Cat4.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights5 = cms.untracked.string(base+'/data/Electrons_BDTG_NonTrigV0_Cat5.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights6 = cms.untracked.string(base+'/data/Electrons_BDTG_NonTrigV0_Cat6.weights.xml')
# weight files for triggering MVA w/ IP
process.NtupleMaker.EleMVATrigWeights1 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigV0_Cat1.weights.xml')
process.NtupleMaker.EleMVATrigWeights2 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigV0_Cat2.weights.xml')
process.NtupleMaker.EleMVATrigWeights3 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigV0_Cat3.weights.xml')
process.NtupleMaker.EleMVATrigWeights4 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigV0_Cat4.weights.xml')
process.NtupleMaker.EleMVATrigWeights5 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigV0_Cat5.weights.xml')
process.NtupleMaker.EleMVATrigWeights6 = cms.untracked.string(base+'/data/Electrons_BDTG_TrigV0_Cat6.weights.xml')

# set Ntuple to run on PAT jets
process.NtupleMaker.doPatJets = cms.untracked.bool(True)
process.NtupleMaker.srcPatJets = cms.untracked.string("selectedPatJets")
process.NtupleMaker.doPatMET = cms.untracked.bool(True)
process.NtupleMaker.doMVAMET = cms.untracked.bool(False)

process.schedule = cms.Schedule()

process.NtupleMaker.doTrack= cms.untracked.bool(False)

#hlt modules
process.NtupleMaker.useFilterModules = cms.vstring("hltOverlapFilterIsoMu17LooseIsoPFTau20","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f18QL3crIsoFiltered10","hltL1Mu12EG7L3MuFiltered17","hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8","hltL1MuOpenEG12L3Filtered8","hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltMu8Ele17dZFilter","hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltMu17Ele8dZFilter","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoRhoFiltered0p15","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoFiltered10","hltL3fL1sMu12L3Filtered17","hltEle17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltEle8CaloIdLCaloIsoVLPixelMatchFilter","hltEle8CaloIdTTrkIdVLDphiFilter","hltL3fL1sMu3L3Filtered8","hltL3crIsoL1sMu16L1f0L2f16QL3f24QL3crIsoRhoFiltered0p15","hltL3crIsoL1sMu16L1f0L2f16QL3f30QL3crIsoRhoFiltered0p15","hltL3fL1sMu16L1f0L2f16QL3Filtered40Q","hltL3fL1sMu16Eta2p1L1f0L2f16QL3Filtered40Q","hltL3fL1sMu7L3Filtered12","hltEle27CaloIdLCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltL3fL1DoubleMu10MuOpenOR3p5L1f0L2f10L3Filtered17","hltL3fL1DoubleMu10MuOpenL1f0L2f10L3Filtered17","hltEle17TightIdLooseIsoEle8TightIdLooseIsoTrackIsoDZ","hltEle8TightIdLooseIsoTrackIsoFilter","hltEle25CaloIdVTCaloIsoTTrkIdTTrkIsoTCentralPFNoPUJet30EleCleaned","hltEleBLifetimeL3PFNoPUFilterSingleTop","hltEle27WP80TrackIsoFilter")

#hlt paths
if "<DataType>" == "Data":
    process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu24_eta2p1_v","HLT_Mu17_Ele8_CaloIdL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu17_v","HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_QuadJet80_v","HLT_Ele8_CaloIdL_CaloIsoVL_v","HLT_Ele8_CaloIdT_TrkIdVL_v","HLT_Mu8_v","HLT_IsoMu24_v","HLT_IsoMu30_v","HLT_Mu40_v","HLT_Mu40_eta2p1_v","HLT_Mu12_v","HLT_Ele27_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Mu17_Mu8_v","HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFNoPUJet30_v","HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFNoPUJet30_BTagIPIter_v","HLT_Ele27_WP80_v")
elif "<DataType>" == "dy_ll" or "<DataType>" == "dy_ee" or "<DataType>" == "dy_mumu" or "<DataType>" == "dy_tautau":
    process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu24_eta2p1_v","HLT_Mu17_Ele8_CaloIdL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu17_v","HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_IsoMu24_v","HLT_IsoMu30_v","HLT_Mu40_v","HLT_Mu40_eta2p1_v","HLT_Mu12_v","HLT_Ele27_CaloIdL_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Mu17_Mu8_v","HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFNoPUJet30_v","HLT_Ele25_CaloIdVT_CaloIsoT_TrkIdT_TrkIsoT_CentralPFNoPUJet30_BTagIPIter_v","HLT_Ele27_WP80_v")
else:
    process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu24_eta2p1_v","HLT_Mu17_Ele8_CaloIdL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL","HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL")    


process.TauNtupleSkim  = cms.Path(process.EvntCounterA
                                  * process.MultiTrigFilter
                                  * process.MuonPreselectionCuts
                                  * process.CountTriggerPassedEvents
                                  * process.recoTauClassicHPSSequence
                                  * process.patDefaultSequence
                                  * process.JetMetSequence
                                  * process.PreselectionCuts
                                  * process.EvntCounterB
                                  * process.NtupleMaker)
process.schedule.append(process.TauNtupleSkim)



