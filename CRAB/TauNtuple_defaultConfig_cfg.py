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

# load full CMSSW reconstruction config, needed for btagging
process.load("Configuration.StandardSequences.Reconstruction_cff")

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

# b-tagging on PFJets (taken from https://twiki.cern.ch/twiki/pub/CMS/BtvTutorialHandsOn/runBtagExample1SV.py.txt)
#process.load('RecoBTag.Configuration.RecoBTag_cff')
process.MyAk5PFJetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
   process.j2tParametersVX,
   jets = cms.InputTag("ak5PFJetsCorr")
)
process.MyImpactParameterPFTagInfos = process.impactParameterTagInfos.clone(
  jetTracks = "MyAk5PFJetTracksAssociatorAtVertex"
)
process.MySecondaryVertexTagInfos = process.secondaryVertexTagInfos.clone(
  trackIPTagInfos = cms.InputTag("MyImpactParameterPFTagInfos"),
)
process.MyCombinedSecondaryVertexBJetTags  = process.combinedSecondaryVertexBJetTags.clone(
  tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"),
                           cms.InputTag("MySecondaryVertexTagInfos"))
)

process.JetSequence = cms.Sequence(process.ak5PFJetsCorr
                    * process.pileupJetIdProducer
                    * process.MyAk5PFJetTracksAssociatorAtVertex
                    * process.MyImpactParameterPFTagInfos
                    * process.MySecondaryVertexTagInfos
                    * process.MyCombinedSecondaryVertexBJetTags)

# jet flavour (https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookBTagging#BtagMCTools)
if not "<DataType>" == "Data":
    process.load("PhysicsTools.JetMCAlgos.CaloJetsMCFlavour_cfi")
    process.PFAK5byRef = process.AK5byRef.clone(
                                                jets = cms.InputTag("ak5PFJetsCorr")
                                                )
    process.PFAK5byValAlgo = process.AK5byValAlgo.clone(
                                                        srcByReference = cms.InputTag("PFAK5byRef")
                                                        )
    process.JetSequence += process.myPartons
    process.JetSequence += process.PFAK5byRef
    process.JetSequence += process.PFAK5byValAlgo


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


debugging = False
#debugging = True
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

### Electron momentum regression ###
process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                  calibratedElectrons = cms.PSet(
                                                                                 initialSeed = cms.untracked.uint32(1),
                                                                                 engineName = cms.untracked.string("TRandom3")
                                                                                 ),
                                                  )
process.load("EgammaAnalysis.ElectronTools.calibratedElectrons_cfi")
if "<DataType>" == "Data":
    process.calibratedElectrons.isMC = cms.bool(False)
    process.calibratedElectrons.inputDataset = cms.string("22Jan2013ReReco")
else:
    process.calibratedElectrons.isMC = cms.bool(True)
    process.calibratedElectrons.inputDataset = cms.string("Summer12_LegacyPaper")
process.calibratedElectrons.updateEnergyError = cms.bool(True)
process.calibratedElectrons.correctionsType = cms.int32(2)
process.calibratedElectrons.combinationType = cms.int32(3)
process.calibratedElectrons.applyLinearityCorrection = cms.bool(True)

process.load('EgammaAnalysis.ElectronTools.electronRegressionEnergyProducer_cfi')
process.eleRegressionEnergy.inputElectronsTag = cms.InputTag('gsfElectrons')
process.eleRegressionEnergy.inputCollectionType = cms.uint32(0)
process.eleRegressionEnergy.useRecHitCollections = cms.bool(True)
process.eleRegressionEnergy.produceValueMaps = cms.bool(True)
process.eleRegressionEnergy.regressionInputFile = cms.string("EgammaAnalysis/ElectronTools/data/eleEnergyRegWeights_WithSubClusters_VApr15.root")
process.eleRegressionEnergy.energyRegressionType = cms.uint32(2)

process.NtupleMaker.pfelectrons = cms.InputTag("calibratedElectrons","calibratedGsfElectrons","")
####################################


process.schedule = cms.Schedule()

process.NtupleMaker.doTrack= cms.untracked.bool(False)

#hlt modules
process.NtupleMaker.useFilterModules = cms.vstring("hltOverlapFilterIsoMu17LooseIsoPFTau20","hltL3crIsoL1sMu14erORMu16erL1f0L2f14QL3f17QL3crIsoRhoFiltered0p15", # HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v
                                                   "hltOverlapFilterIsoMu18LooseIsoPFTau20","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f18QL3crIsoFiltered10", # HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v
                                                   "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoRhoFiltered0p15","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoFiltered10", # HLT_IsoMu24_eta2p1_v
                                                   "hltL3crIsoL1sMu16L1f0L2f16QL3f24QL3crIsoRhoFiltered0p15", # HLT_IsoMu24_v
                                                   "hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltL1Mu12EG7L3MuFiltered17", # HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL
                                                   "hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8","hltL1MuOpenEG12L3Filtered8", # HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL
                                                   "hltEle8CaloIdLCaloIsoVLPixelMatchFilter", # HLT_Ele8_CaloIdL_CaloIsoVL_v
                                                   "hltEle8CaloIdTTrkIdVLDphiFilter", # HLT_Ele8_CaloIdT_TrkIdVL_v
                                                   "hltEle8TightIdLooseIsoTrackIsoFilter", # HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v
                                                   "hltL3fL1sMu3L3Filtered8", # HLT_Mu8_v
                                                   "hltL3fL1sMu7L3Filtered12", # HLT_Mu12_v
                                                   "hltL3fL1sMu12L3Filtered17", # HLT_Mu17_v
                                                   "hltDiMuonGlb17Glb8DzFiltered0p2","hltL3fL1DoubleMu10MuOpenOR3p5L1f0L2f10L3Filtered17","hltL3fL1DoubleMu10MuOpenL1f0L2f10L3Filtered17","hltDiMuonMu17Mu8DzFiltered0p2","hltL3pfL1DoubleMu10MuOpenOR3p5L1f0L2pf0L3PreFiltered8","hltL3pfL1DoubleMu10MuOpenL1f0L2pf0L3PreFiltered8" # HLT_Mu17_Mu8_v
                                                   "hltEle17TightIdLooseIsoEle8TightIdLooseIsoTrackIsoDZ", # HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v
                                                   "hltEle27WP80TrackIsoFilter" # HLT_Ele27_WP80_v
                                                   )

#hlt paths
process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v", # for mu+tau analyses
                                                  "HLT_IsoMu24_eta2p1_v","HLT_IsoMu24_v", # for claudia and possible trigger efficiency measurements
                                                  "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL", # for e+mu analysis
                                                  "HLT_Ele8_CaloIdL_CaloIsoVL_v","HLT_Ele8_CaloIdT_TrkIdVL_v","HLT_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v", # for electron fake rate measurements
                                                  "HLT_Mu8_v","HLT_Mu12_v","HLT_Mu17_v", # for muon fakerate measurements
                                                  "HLT_Mu17_Mu8_v","HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Ele27_WP80_v" # for trigger efficiency measurements
                                                  )

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
    
# object selection cuts
process.NtupleMaker.MuonPtCut = cms.double(3.0)
process.NtupleMaker.MuonEtaCut = cms.double(2.5)
process.NtupleMaker.TauPtCut = cms.double(18.0)
process.NtupleMaker.TauEtaCut = cms.double(2.4)
process.NtupleMaker.ElectronPtCut = cms.double(8.0)
process.NtupleMaker.ElectronEtaCut = cms.double(2.5)
process.NtupleMaker.JetPtCut = cms.double(10.0)
process.NtupleMaker.JetEtaCut = cms.double(4.7)
    
process.TauNtupleSkim  = cms.Path(process.EvntCounterA
				                  * process.metFilters
                                  * process.eleRegressionEnergy
                                  * process.calibratedElectrons
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



