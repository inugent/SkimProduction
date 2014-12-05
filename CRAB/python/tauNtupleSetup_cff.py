import FWCore.ParameterSet.Config as cms

def setupTauNtuple(process, base, puFile, datatype, dopatmet):
    process.load("TauDataFormat.TauNtuple.triggerFilter_cfi")
    process.load("TauDataFormat.TauNtuple.cuts_cfi")
    process.load("TauDataFormat.TauNtuple.tauntuple_cfi")
    process.load("TauDataFormat.TauNtuple.eventCounter_cfi")
    #process.EvntCounterA.DataMCType = cms.untracked.string("Data")
    #process.EvntCounterB.DataMCType = cms.untracked.string("Data")
    process.EvntCounterA.DataMCType = cms.untracked.string(datatype)
    process.EvntCounterB.DataMCType = cms.untracked.string(datatype)
    process.CountTriggerPassedEvents = process.EvntCounterB.clone()
    process.CountTriggerPassedEvents.CounterType = cms.untracked.string("CountTriggerPassedEvents")
    process.CountKinFitPassedEvents = process.EvntCounterB.clone()
    process.CountKinFitPassedEvents.CounterType = cms.untracked.string("CountKinFitPassedEvents")
    
    process.NtupleMaker.doPatJets = cms.untracked.bool(False)
    process.NtupleMaker.doPatMET = cms.untracked.bool(dopatmet)
    process.NtupleMaker.doMVAMET = cms.untracked.bool(True)
    
    ## change Pileup histograms to use
    process.NtupleMaker.PUInputFile= cms.untracked.string("$CMSSW_BASE/src/data/Lumi_OfficialAndHtautau.root")
    process.NtupleMaker.PUInputHistoMC    = cms.untracked.string("official_MC_Summer12")
    process.NtupleMaker.PUInputHistoData  = cms.untracked.string("official_h_190456_20868")
    process.NtupleMaker.PUInputHistoData_p5  = cms.untracked.string("official_h_190456_20868_p5")
    process.NtupleMaker.PUInputHistoData_m5  = cms.untracked.string("official_h_190456_20868_m5")
    process.NtupleMaker.PUInputHistoMCFineBins = cms.untracked.string("htautau_mc_pileup")
    process.NtupleMaker.PUInputHistoDataFineBins = cms.untracked.string("htautau_data_pileup")
    
    process.NtupleMaker.PUInputFile = cms.untracked.string(base+'/data/'+puFile)
    
    # use electrons from electron momentum regression
    process.NtupleMaker.pfelectrons = cms.InputTag("calibratedElectrons","calibratedGsfElectrons","")
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
    
    # JEC uncertainty files
    process.NtupleMaker.JECuncData = cms.untracked.string(base+'/data/JECuncertaintyData.txt')
    process.NtupleMaker.JECuncMC = cms.untracked.string(base+'/data/JECuncertaintyMC.txt')
    
    process.NtupleMaker.doTrack= cms.untracked.bool(False)
    
    if "embedded" in datatype:
        process.NtupleMaker.Embedded = cms.untracked.bool(True);
    else:
        process.NtupleMaker.Embedded = cms.untracked.bool(False);
    