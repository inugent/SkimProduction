import FWCore.ParameterSet.Config as cms

# b-tagging on PFJets 
# taken from https://twiki.cern.ch/twiki/pub/CMS/BtvTutorialHandsOn/runBtagExample1SV.py.txt)
def runBTaggingOnPFJets(process):
    process.MyAk5PFJetTracksAssociatorAtVertex = cms.EDProducer("JetTracksAssociatorAtVertex",
        process.j2tParametersVX,
        jets = cms.InputTag("ak5PFJetsCorr")
    )
    process.MyImpactParameterPFTagInfos = process.impactParameterTagInfos.clone(
        jetTracks = "MyAk5PFJetTracksAssociatorAtVertex"
    )
    process.MySecondaryVertexTagInfos = process.secondaryVertexTagInfos.clone(
        trackIPTagInfos = cms.InputTag("MyImpactParameterPFTagInfos")
    )
    process.MyCombinedSecondaryVertexBJetTags  = process.combinedSecondaryVertexBJetTags.clone(
        tagInfos = cms.VInputTag(cms.InputTag("MyImpactParameterPFTagInfos"),
                                 cms.InputTag("MySecondaryVertexTagInfos"))
    )
    
    process.bTagOnPFJetSequence = cms.Sequence(
                          process.MyAk5PFJetTracksAssociatorAtVertex
                        * process.MyImpactParameterPFTagInfos
                        * process.MySecondaryVertexTagInfos
                        * process.MyCombinedSecondaryVertexBJetTags)
