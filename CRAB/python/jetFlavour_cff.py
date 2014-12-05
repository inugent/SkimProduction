import FWCore.ParameterSet.Config as cms

# https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookBTagging#BtagMCTools
def jetFlavour(process):
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
    
    # get gen jets without neutrinos
    from RecoJets.Configuration.GenJetParticles_cff import genParticlesForJetsNoNu
    process.genParticlesForJetsNoNu = genParticlesForJetsNoNu

    from RecoJets.JetProducers.ak5GenJets_cfi import ak5GenJets
    process.ak5GenJetsNoNu = ak5GenJets.clone( src = cms.InputTag("genParticlesForJetsNoNu") )
    
    process.JetSequence += process.genParticlesForJetsNoNu
    process.JetSequence += process.ak5GenJetsNoNu