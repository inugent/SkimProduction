import FWCore.ParameterSet.Config as cms

def eventPreselection(process, preselection):
    # choose preselection to apply
    if preselection == "DoubleMu":
        process.firstLevelPreselection = process.MuonPreselectionCuts
        process.secondLevelPreselection = process.DoubleMuPreselectionCuts
    elif preselection == "DoubleEle":
        process.firstLevelPreselection = process.ElePreselectionCuts
        process.secondLevelPreselection = process.DoubleElePreselectionCuts
    elif preselection == "EMuTvariable":
        process.firstLevelPreselection = process.MuOrElePreselectionCuts
        process.secondLevelPreselection = process.EMuTvariablePreselectionCuts
    else:
        process.firstLevelPreselection = process.MuonPreselectionCuts
        process.secondLevelPreselection = process.PreselectionCuts
    
    # HLT paths to use
    process.MultiTrigFilter.useTriggers = cms.vstring("HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v","HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v", # for mu+tau analyses
                                                      "HLT_IsoMu24_eta2p1_v", # for claudia and possible trigger efficiency measurements
                                                      "HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL","HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL", # for e+mu analysis
                                                      "HLT_Mu17_Mu8_v","HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v","HLT_Ele27_WP80_v" # for trigger efficiency measurements
                                                      )
    # HLT modules in used HLT paths
    process.NtupleMaker.useFilterModules = cms.vstring("hltOverlapFilterIsoMu17LooseIsoPFTau20","hltL3crIsoL1sMu14erORMu16erL1f0L2f14QL3f17QL3crIsoRhoFiltered0p15", # HLT_IsoMu17_eta2p1_LooseIsoPFTau20_v
                                                       "hltOverlapFilterIsoMu18LooseIsoPFTau20","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f18QL3crIsoFiltered10", # HLT_IsoMu18_eta2p1_LooseIsoPFTau20_v
                                                       "hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoRhoFiltered0p15","hltL3crIsoL1sMu16Eta2p1L1f0L2f16QL3f24QL3crIsoFiltered10", # HLT_IsoMu24_eta2p1_v
                                                       "hltMu17Ele8CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltL1Mu12EG7L3MuFiltered17", # HLT_Mu17_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL
                                                       "hltMu8Ele17CaloIdTCaloIsoVLTrkIdVLTrkIsoVLTrackIsoFilter","hltL1sL1Mu3p5EG12ORL1MuOpenEG12L3Filtered8","hltL1MuOpenEG12L3Filtered8", # HLT_Mu8_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL
                                                       "hltDiMuonGlb17Glb8DzFiltered0p2","hltL3fL1DoubleMu10MuOpenOR3p5L1f0L2f10L3Filtered17","hltL3fL1DoubleMu10MuOpenL1f0L2f10L3Filtered17","hltDiMuonMu17Mu8DzFiltered0p2","hltL3pfL1DoubleMu10MuOpenOR3p5L1f0L2pf0L3PreFiltered8","hltL3pfL1DoubleMu10MuOpenL1f0L2pf0L3PreFiltered8" # HLT_Mu17_Mu8_v
                                                       "hltEle17TightIdLooseIsoEle8TightIdLooseIsoTrackIsoDZ", # HLT_Ele17_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_Ele8_CaloIdT_CaloIsoVL_TrkIdVL_TrkIsoVL_v
                                                       "hltEle27WP80TrackIsoFilter" # HLT_Ele27_WP80_v
                                                       )
    


def objectPreselection(process):
    # object selection cuts
    process.NtupleMaker.MuonPtCut = cms.double(3.0)
    process.NtupleMaker.MuonEtaCut = cms.double(2.5)
    process.NtupleMaker.TauPtCut = cms.double(18.0)
    process.NtupleMaker.TauEtaCut = cms.double(2.4)
    process.NtupleMaker.ElectronPtCut = cms.double(8.0)
    process.NtupleMaker.ElectronEtaCut = cms.double(2.5)
    process.NtupleMaker.JetPtCut = cms.double(10.0)
    process.NtupleMaker.JetEtaCut = cms.double(5.2)