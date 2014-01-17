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

############ Jets #############
# Jet energy corrections to use:
JetCorrection = "ak5PFL1FastL2L3"
if "<DataType>" == "Data":
    JetCorrection += "Residual"
process.ak5PFJetsCorr = cms.EDProducer('PFJetCorrectionProducer',
                                       src = cms.InputTag("ak5PFJets"),
                                       correctors = cms.vstring(JetCorrection) # NOTE: use "ak5PFL1FastL2L3" for MC / "ak5PFL1FastL2L3Residual" for Data
                                       )

# load PUJetID
process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdProducer.jets = "ak5PFJetsCorr"
process.pileupJetIdProducer.residualsTxt = cms.FileInPath("RecoJets/JetProducers/data/mva_JetID_v1.weights.xml")

process.JetSequence(process.ak5PFJetsCorr
                    * process.pileupJetIdProducer)

############ MET #############
# load recommended met filters
process.load("RecoMET.METFilters.metFilters_cff")
# produce corrected MET collections (RECO)
process.load("JetMETCorrections.Type1MET.correctionTermsCaloMet_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")
process.corrPfMetType1.jetCorrLabel = cms.string(JetCorrection)

process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0RecoTrack_cff")
process.load("JetMETCorrections.Type1MET.correctionTermsPfMetShiftXY_cff")
if "<DataType>" == "Data":
    process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data
else:
    process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc
process.load("JetMETCorrections.Type1MET.correctedMet_cff")


# compute MVA MET
process.load('JetMETCorrections.Configuration.JetCorrectionProducers_cff')
process.load('RecoMET.METPUSubtraction.mvaPFMET_leptons_cff')
process.load('RecoMET.METPUSubtraction.noPileUpPFMET_cff')
#Specify the leptons
process.pfMEtMVA.srcLeptons = cms.VInputTag("isomuons","isoelectrons","isotaus") # load default lepton selection (H2Tau) for MVA-MET
process.pfMEtMVA.srcCorrJets = cms.InputTag("ak5PFJetsCorr")

process.MetSequence = cms.Sequence(process.correctionTermsPfMetType1Type2
                                      * process.correctionTermsPfMetType0RecoTrack
                                      * process.correctionTermsPfMetType0PFCandidate
                                      * process.correctionTermsPfMetShiftXY
                                      * process.correctionTermsCaloMet
                                      * process.pfMetT0rt
                                      * process.pfMetT0rtT1
                                      * process.pfMetT0pc
                                      * process.pfMetT0pcT1
                                      * process.pfMetT0rtTxy
                                      * process.pfMetT0rtT1Txy
                                      * process.pfMetT0pcTxy
                                      * process.pfMetT0pcT1Txy
                                      * process.pfMetT1
                                      * process.pfMetT1Txy
                                      * process.caloMetT1
                                      * process.caloMetT1T2
                                      * process.pfMEtMVAsequence)

###############

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

process.NtupleMaker.doPatJets = cms.untracked.bool(False)
process.NtupleMaker.doPatMET = cms.untracked.bool(False)
process.NtupleMaker.doMVAMET = cms.untracked.bool(True)
                        
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
process.NtupleMaker.EleMVATrigNoIPWeights1 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat1.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights2 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat2.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights3 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat3.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights4 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat4.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights5 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat5.weights.xml')
process.NtupleMaker.EleMVATrigNoIPWeights6 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigNoIPV0_2012_Cat6.weights.xml')
# weight files for non triggering MVA
process.NtupleMaker.EleMVANonTrigWeights1 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_NonTrigV0_Cat1.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights2 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_NonTrigV0_Cat2.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights3 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_NonTrigV0_Cat3.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights4 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_NonTrigV0_Cat4.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights5 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_NonTrigV0_Cat5.weights.xml')
process.NtupleMaker.EleMVANonTrigWeights6 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_NonTrigV0_Cat6.weights.xml')
# weight files for triggering MVA w/ IP
process.NtupleMaker.EleMVATrigWeights1 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat1.weights.xml')
process.NtupleMaker.EleMVATrigWeights2 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat2.weights.xml')
process.NtupleMaker.EleMVATrigWeights3 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat3.weights.xml')
process.NtupleMaker.EleMVATrigWeights4 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat4.weights.xml')
process.NtupleMaker.EleMVATrigWeights5 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat5.weights.xml')
process.NtupleMaker.EleMVATrigWeights6 = cms.untracked.string(base+'/EgammaAnalysis/ElectronTools/data/Electrons_BDTG_TrigV0_Cat6.weights.xml')


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

# choose preselection to apply
if "<PRESELECTION>" == "DoubleMu":
    firstLevelPreselection = process.MuonPreselectionCuts
    secondLevelPreselection = process.DoubleMuPreselectionCuts
elif "<PRESELECTION>" == "DoubleEle":
    firstLevelPreselection = process.ElePreselectionCuts
    secondLevelPreselection = process.DoubleElePreselectionCuts
elif "<PRESELECTION>" == "MuJet":
    firstLevelPreselection = process.MuonPreselectionCuts
    secondLevelPreselection = process.MuJetPreselectionCuts
else:
    firstLevelPreselection = process.MuonPreselectionCuts
    secondLevelPreselection = process.PreselectionCuts
    
process.TauNtupleSkim  = cms.Path(process.EvntCounterA
				                  * process.metFilters
                                  * process.MultiTrigFilter
                                  * firstLevelPreselection
                                  * process.CountTriggerPassedEvents
                                  * process.recoTauClassicHPSSequence
                                  * process.JetSequence
                                  * process.MetSequence
                                  * secondLevelPreselection
                                  * process.EvntCounterB
                                  * process.NtupleMaker)



process.schedule.append(process.TauNtupleSkim)



