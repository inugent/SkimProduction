import FWCore.ParameterSet.Config as cms

# stolen from: https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATTools#MET_Systematics_Tools
def metUncertainty(process):
    process.load("PhysicsTools.PatAlgos.patSequences_cff")
    #process.MetSequence += process.type0PFMEtCorrection
    #process.MetSequence += process.patPFMETtype0Corr
    #from PhysicsTools.PatAlgos.patTemplate_cfg import *
    #from PhysicsTools.PatAlgos.tools.coreTools import *
    from PhysicsTools.PatAlgos.tools.jetTools import switchJetCollection
    #from PhysicsTools.PatAlgos.tools.metTools import *
    switchJetCollection(
                        process,
                        cms.InputTag('ak5PFJets'),
                        doJTA = True,
                        doBTagging = False,
                        jetCorrLabel = ('AK5PF',cms.vstring(['L1FastJet','L2Relative','L3Absolute'])),
                        doType1MET = False,
                        doJetID = True,
                        jetIdLabel = "ak5",
                        outputModules = [] # no PAT output module
                        )
    from PhysicsTools.PatUtils.tools.metUncertaintyTools import runMEtUncertainties
    runMEtUncertainties(process)

