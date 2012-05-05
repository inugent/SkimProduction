

import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.triggerResultsFilter_cfi as hlt

process = cms.Process("AOD")

############################################
#
# configure
doDebugOutput = True
myjets = "goodPatJets" #"selectedPatJets"
myBtag = "TCHEM"
runOnMC=True
DataType = "<DataType>"
if DataType == "Data":
    runOnMC=False
############################################

process.load('Configuration/StandardSequences/Services_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration.StandardSequences.GeometryExtended_cff')
#process.load('Configuration.StandardSequences.GeometryDB_cff')
process.load('Configuration/StandardSequences/FrontierConditions_GlobalTag_cff')

# global tag
<globaltag>

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load("Configuration.EventContent.EventContent_cff")
process.load('HLTrigger.Configuration.HLT_GRun_cff')

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("RecoTauTag.Configuration.RecoPFTauTag_cff")

#HLT_Photon15_TrackIso_L1R
process.load("Configuration.StandardSequences.EndOfProcess_cff")
#process.load("RecoTauTag.Configuration.FixedConeHighEffPFTaus_cfi")
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

removeMCMatching(process, ['All'])

# Jet energy corrections to use:
#inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute', 'L2L3Residual'])
inputJetCorrLabel = ('AK5PF', ['L1Offset', 'L2Relative', 'L3Absolute'])
process.patJetCorrFactors.useRho=False

# add pf met
addPfMET(process, 'PF')

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

# Apply loose PF jet ID
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.goodPatJets = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                   filterParams = pfJetIDSelector.clone(),
                                   src = cms.InputTag("selectedPatJets"),
                                   filter = cms.bool(True)
                                   )


# Taus are currently broken in 4.1.x
removeSpecificPATObjects( process, ['Taus'] )
process.patDefaultSequence.remove( process.patTaus )

# Select jets
process.selectedPatJets.cut = cms.string('pt > 25')

#from PhysicsTools.PatUtils.metUncertaintyTools import runMEtUncertainties
#runMEtUncertainties(process)
######################################################
#
# Add Bjets
#
#process.bTagCorr = cms.EDProducer("BTagSFEventWeight",
#                          jets  = cms.InputTag(myjets),   ## jet collection (after jet selection, before b-tagging)
#                          bTagAlgo = cms.string(myBtag),  ## name of b tag algorithm
#                          sysVar   = cms.string(""),                  ## bTagSFUp, bTagSFDown, misTagSFUp, misTagSFDown possible;
#                          ## bTagSFShapeUpPt, bTagSFShapeDownPt, bTagSFShapeUpEta, bTagSFShapeDownEta,
#                          ## everything else: no systematic variation is made
#                          shapeVarPtThreshold  = cms.double(65.),     ## pt threshold which divides up/down variations during bTagSFShapeUp/DownPt
#                          shapeVarEtaThreshold = cms.double(0.7),     ## eta threshold which divides up/down variations during bTagSFShapeUp/DownEta
#                          uncertaintySFb = cms.double(-1),            ## uncertainty of SFb (0.05 means 5%); if set to <0, the values from the b-tag DB are taken
#                          shapeDistortionFactor = cms.double(1.),     ## for shape uncertainty calculation (fraction of normalisation uncertainty)
#                          verbose  = cms.int32( 0),                   ## set to 1 if terminal text output is desired
#                          filename = cms.string("input/default.root"),                   ## if filename != "", the efficiencies are read from histos
#                          ## provided in that file
#                          dir=cms.string("bTagEff")
#                          )
#process.HHCorr=bTagCorr.clone(bTagAlgo= cms.string('SSVHEM'),dir="analyzeBTagEfficiency")

######################################################
#
# Now setup rest of the code
#


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


process.EvntCounterA.DataMCType = cms.untracked.string(DataType);
process.EvntCounterB.DataMCType = cms.untracked.string(DataType);
process.MultiTrigFilter.useTriggers = cms.vstring("IsoMu24","IsoPFTau35_Trk20_MET")
process.KinematicTauSkim.discriminators = cms.vstring("PFRecoTauDiscriminationByKinematicFit","PFRecoTauDiscriminationByKinematicFitQuality")
process.NtupleMaker.PUInputFile = cms.untracked.string("$CMSSW_BASE/src/data/Lumi_160404_180252_andMC_Flat_Tail.root")
process.NtupleMaker.doPatJets = cms.untracked.bool(True)
process.NtupleMaker.srcPatJets = cms.untracked.string(myjets)
#process.NtupleMaker.doPatMET = cms.untracked.bool(True)
process.NtupleMaker.srcPatMET = cms.untracked.string("patMETsPF")


####################################################################
#
# Filters
#

#process.primaryVertexFilter = cms.EDFilter("GoodVertexFilter",
#                                           vertexCollection = cms.InputTag('offlinePrimaryVertices'),
#                                           minimumNDOF = cms.uint32(4) ,
#                                           maxAbsZ = cms.double(24),
#                                           maxd0 = cms.double(2)
#                                           )
process.goodVertices= cms.EDFilter("VertexSelector",
                                   filter = cms.bool(True),
                                   src = cms.InputTag("offlinePrimaryVertices"),
                                   cut = cms.string("!isFake && ndof > 4 && abs(z) <= 24 && position.rho < 2")
                                   )


process.load('RecoMET.METAnalyzers.CSCHaloFilter_cfi')
#process.load('CommonTools/RecoAlgos/HBHENoiseFilter_cfi') # for data only below
process.load("RecoMET.METFilters.hcalLaserEventFilter_cfi")

process.load('RecoMET.METFilters.EcalDeadCellTriggerPrimitiveFilter_cfi')
# The section below is for the filter on Boundary Energy. Available in AOD in CMSSW>44x
process.load('RecoMET.METFilters.EcalDeadCellBoundaryEnergyFilter_cfi')
process.EcalDeadCellBoundaryEnergyFilter.taggingMode = cms.bool(False)
process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEB=cms.untracked.double(10)
process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyDeadCellsEE=cms.untracked.double(10)
process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEB=cms.untracked.double(100)
process.EcalDeadCellBoundaryEnergyFilter.cutBoundEnergyGapEE=cms.untracked.double(100)
process.EcalDeadCellBoundaryEnergyFilter.enableGap=cms.untracked.bool(False)
process.EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEB = cms.vint32(12,14)
process.EcalDeadCellBoundaryEnergyFilter.limitDeadCellToChannelStatusEE = cms.vint32(12,14)
# End of Boundary Energy filter configuration

# The line below is the default recommendation
process.load('JetMETCorrections.Configuration.DefaultJEC_cff')
process.load('RecoMET.METFilters.trackingFailureFilter_cfi')
process.trackingFailureFilter.JetSource = cms.InputTag('ak5PFJetsL2L3Residual')

##################################################################################



process.schedule = cms.Schedule()

if runOnMC != True:
    
    process.noscraping = cms.EDFilter("FilterOutScraping",
                                      applyfilter = cms.untracked.bool(True),
                                      debugOn = cms.untracked.bool(True),
                                      numtrack = cms.untracked.uint32(10),
                                      thresh = cms.untracked.double(0.25)
                                      )
    
    process.HBHENoiseFilter = cms.EDFilter('HBHENoiseFilter',
                                           noiselabel = cms.InputTag('hcalnoise','','RECO'),
                                           minRatio = cms.double(-999),
                                           maxRatio = cms.double(999),
                                           minHPDHits = cms.int32(17),
                                           minRBXHits = cms.int32(999),
                                           minHPDNoOtherHits = cms.int32(10),
                                           minZeros = cms.int32(10),
                                           minHighEHitTime = cms.double(-9999.0),
                                           maxHighEHitTime = cms.double(9999.0),
                                           maxRBXEMF = cms.double(-999.0),
                                           minNumIsolatedNoiseChannels = cms.int32(9999),
                                           minIsolatedNoiseSumE = cms.double(9999),
                                           minIsolatedNoiseSumEt = cms.double(9999),
                                           useTS4TS5 = cms.bool(True)
                                           )

    process.KinFitSkim  = cms.Path(process.EvntCounterA*process.MultiTrigFilter*process.TrigFilterInfo*process.goodVertices*process.noscraping*process.HBHENoiseFilter*process.PFTau*process.PrimVtxSelector*process.InputTrackSelector*process.ThreeProngInputSelector*process.KinematicTauBasicProducer*process.KinematicTauSkim*process.KinematicTauProducer*process.CSCTightHaloFilter*process.hcalLaserEventFilter*process.EcalDeadCellTriggerPrimitiveFilter*process.ak5PFJetsL2L3Residual*process.trackingFailureFilter*process.patDefaultSequence*process.goodPatJets*process.EvntCounterB*process.NtupleMaker)

else:
    process.KinFitSkim  = cms.Path(process.EvntCounterA*process.MultiTrigFilter*process.TrigFilterInfo*process.goodVertices*process.PFTau*process.PrimVtxSelector*process.InputTrackSelector*process.ThreeProngInputSelector*process.KinematicTauBasicProducer*process.KinematicTauSkim*process.KinematicTauProducer*process.CSCTightHaloFilter*process.hcalLaserEventFilter*process.EcalDeadCellTriggerPrimitiveFilter*process.ak5PFJetsL2L3Residual*process.trackingFailureFilter*process.patDefaultSequence*process.goodPatJets*process.EvntCounterB*process.NtupleMaker)
    
process.schedule.append(process.KinFitSkim)
#if doDebugOutput :
#    process.debugOutput = cms.OutputModule("PoolOutputModule",
#                                           outputCommands = cms.untracked.vstring('keep *'),
#                                           fileName = cms.untracked.string('TauNtupleDebugOutput.root'),
#                                           )
#    process.out_step = cms.EndPath(process.debugOutput)
#    
#    process.schedule.append(process.out_step)
