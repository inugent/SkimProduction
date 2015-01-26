import FWCore.ParameterSet.Config as cms
import os
import re
import socket
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt
import FWCore.ParameterSet.VarParsing as VarParsing

process = cms.Process("TauNtupleProcess")

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

### read in command line arguments
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideAboutPythonConfigFile#Passing_Command_Line_Arguments_T
options = VarParsing.VarParsing()
options.register ('inputFiles', '', options.multiplicity.list, options.varType.string, "List of input files.")
options.register ('maxEvents', 500, options.multiplicity.singleton, options.varType.int, "Number of events to process.")
options.register ('runOnGrid', 0, options.multiplicity.singleton, options.varType.int, "Whether execution happens on Grid (0: local)")
# default values
options.inputFiles ='/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/000260A0-4286-E211-89DC-0030487F1F23.root',\
                    '/store/data/Run2012D/TauPlusX/AOD/22Jan2013-v1/20000/0085A19F-9187-E211-9305-0025901D484C.root'
options.maxEvents = 500

# parse command line arguments
options.parseArguments()

# MET uncertainty tool
# needs to go before everything else for some reason...
if not ("<DataType>" == "Data") and not ("embedded" in "<DataType>"):
    from SkimProduction.CRAB.metUncertaintyTool_cff import metUncertainty
    metUncertainty(process)

# load full CMSSW reconstruction config, needed for btagging
process.load("Configuration.StandardSequences.Reconstruction_cff")

############ Electrons
# electron isolation
from CommonTools.ParticleFlow.Tools.pfIsolation import setupPFElectronIso
process.eleIso = setupPFElectronIso(process, 'gsfElectrons')
process.eleIsoSequence = cms.Sequence(process.pfParticleSelectionSequence
                                      * process.eleIso)
# Electron momentum regression
from SkimProduction.CRAB.eleMomentumRegression_cff import eleMomentumRegression
eleMomentumRegression(process, "<datasetpath>", "<DataType>")

############ Jets
# Jet energy corrections to use:
JetCorrection = "ak5PFL1FastL2L3"
if "<DataType>" == "Data" or "embedded" in "<DataType>":
    JetCorrection += "Residual"
process.ak5PFJetsCorr = cms.EDProducer('PFJetCorrectionProducer',
                                       src = cms.InputTag("ak5PFJets"),
                                       correctors = cms.vstring(JetCorrection) # NOTE: use "ak5PFL1FastL2L3" for MC / "ak5PFL1FastL2L3Residual" for Data
                                       )

# load PUJetID
process.load("RecoJets.JetProducers.PileupJetID_cfi")
process.pileupJetIdProducer.jets = "ak5PFJetsCorr"
process.pileupJetIdProducer.residualsTxt = cms.FileInPath("RecoJets/JetProducers/data/mva_JetID_v1.weights.xml")

# b-tagging on PFJets
from SkimProduction.CRAB.bTaggingOnPFJets_cff import runBTaggingOnPFJets
runBTaggingOnPFJets(process)

process.JetSequence = cms.Sequence(process.ak5PFJetsCorr
                    * process.pileupJetIdProducer
                    * process.bTagOnPFJetSequence)

# jet flavour
if not ("<DataType>" == "Data") and not ("embedded" in "<DataType>"):
    from SkimProduction.CRAB.jetFlavour_cff import jetFlavour
    jetFlavour(process)

############ MET
from SkimProduction.CRAB.metCorrections_cff import applyMetCorrections
applyMetCorrections(process, "<DataType>", JetCorrection)

# default MVA MET
process.load('JetMETCorrections.Configuration.JetCorrectionProducers_cff')
process.load('RecoMET.METPUSubtraction.mvaPFMET_leptons_cff')
process.pfMEtMVA.srcLeptons = cms.VInputTag("isomuons","isoelectrons","isotaus") # load default lepton selection (H2Tau) for MVA-MET
process.pfMEtMVA.srcCorrJets = cms.InputTag("ak5PFJetsCorr")

#  custom MVA-MET for mu+tau analyses
from SkimProduction.CRAB.mvaMET_MuTau_cff import mvaMET_MuTau
mvaMET_MuTau(process)

# choose weight files for MVA-MET
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/MVAMet#Recommended_files_for_53X_Type1
# these weights are using Type0+Type1 corrections and the non-unity response training
weightFiles = cms.PSet(
        U     = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmet_53_Sep2013_type1.root'),
        DPhi  = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
        CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
        CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_53_Dec2012.root')
    )
process.pfMEtMVA.inputFileNames = weightFiles
process.pfMetMVAMuTau.inputFileNames = weightFiles

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
                                      * process.pfMEtMVAsequence # default MVA-MET sequence
                                      * process.MVAMETMuTauSequence # custom MVA-MET MuTau sequence
                                      )

dopatmet = True

if dopatmet:
    from SkimProduction.CRAB.runPatMET_cff import runPatMET
    runPatMET(process)
    process.MetSequence += process.runPatMetSequence

############ Taus
# load new HPS config
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

############ user config
process.source = cms.Source("PoolSource",
                            fileNames = cms.untracked.vstring(options.inputFiles)                  
                            )

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
    )

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('ProductNotFound')
    )

# runOnGrid has to be set to "1" (i.e. True) for GRID submission
if options.runOnGrid:
    base = 'src'
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000
else:
    base = os.path.relpath(os.environ.get('CMSSW_BASE'))+'/src'
    process.MessageLogger.cerr.FwkReport.reportEvery = 10

####################### TauNtuple ######################
from SkimProduction.CRAB.tauNtupleSetup_cff import setupTauNtuple
setupTauNtuple(process, base, "<Pile_Up_File>", "<DataType>", dopatmet)

# apply event and object preselections for Ntuple creation
from SkimProduction.CRAB.tauNtuplePreselection_cff import eventPreselection, objectPreselection
eventPreselection(process,"<PRESELECTION>")
objectPreselection(process)

# define and run path
process.schedule = cms.Schedule()

if "embedded" in "<DataType>":
    process.TauNtupleSkim  = cms.Path(process.EvntCounterA
                                  * process.metFilters
                                  * process.eleRegressionEnergy
                                  * process.calibratedElectrons
                                  * process.firstLevelPreselection
                                  * process.CountTriggerPassedEvents
                                  * process.recoTauClassicHPSSequence
                                  * process.eleIsoSequence
                                  * process.JetSequence
                                  * process.MetSequence
                                  * process.secondLevelPreselection
                                  * process.EvntCounterB
                                  * process.NtupleMaker)
elif "<DataType>" == "Data":
    process.TauNtupleSkim  = cms.Path(process.EvntCounterA
                                  * process.metFilters
                                  * process.eleRegressionEnergy
                                  * process.calibratedElectrons
                                  * process.MultiTrigFilter
                                  * process.firstLevelPreselection
                                  * process.CountTriggerPassedEvents
                                  * process.recoTauClassicHPSSequence
                                  * process.eleIsoSequence
                                  * process.JetSequence
                                  * process.MetSequence
                                  * process.secondLevelPreselection
                                  * process.EvntCounterB
                                  * process.NtupleMaker)
else:
    process.TauNtupleSkim  = cms.Path(process.EvntCounterA
                                  * process.metFilters
                                  * process.eleRegressionEnergy
                                  * process.calibratedElectrons
                                  * process.MultiTrigFilter
                                  * process.firstLevelPreselection
                                  * process.CountTriggerPassedEvents
                                  * process.recoTauClassicHPSSequence
                                  * process.eleIsoSequence
                                  * process.JetSequence
                                  * process.MetSequence
                                  * process.secondLevelPreselection
                                  * process.EvntCounterB
                                  * process.patDefaultSequence #for MET uncertainties. Needs to be called after all other sequences.
                                  * process.NtupleMaker)



process.schedule.append(process.TauNtupleSkim)



