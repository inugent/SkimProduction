import FWCore.ParameterSet.Config as cms

def applyMetCorrections(process, datatype, jetCorrection):
    # load recommended met filters
    process.load("RecoMET.METFilters.metFilters_cff")
    # produce corrected MET collections (RECO)
    process.load("JetMETCorrections.Type1MET.correctionTermsCaloMet_cff")
    process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType1Type2_cff")
    process.corrPfMetType1.jetCorrLabel = cms.string(jetCorrection)
    
    process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0PFCandidate_cff")
    process.load("JetMETCorrections.Type1MET.correctionTermsPfMetType0RecoTrack_cff")
    process.load("JetMETCorrections.Type1MET.correctionTermsPfMetShiftXY_cff")
    if datatype == "Data" or "embedded" in datatype:
        process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_data
    else:
        process.corrPfMetShiftXY.parameter = process.pfMEtSysShiftCorrParameters_2012runABCDvsNvtx_mc
    process.load("JetMETCorrections.Type1MET.correctedMet_cff")