import FWCore.ParameterSet.Config as cms
import hashlib

def eleMomentumRegression(process, datasetpath, datatype):
    # generate hash from datasetpath and form unique but constant seed for each sample
    # !!! WARNING: seed is still dependent on job splitting !!!
    to_hash = datasetpath
    hash_input = to_hash.split("=")[1].strip()
    generate_hash = hashlib.md5(hash_input)
    seed = abs(int(str(int(generate_hash.hexdigest(),16))[0:9])) # crab expects uint32 -> only up to 9 digits of hash can be safely used
    
    process.RandomNumberGeneratorService = cms.Service("RandomNumberGeneratorService",
                                                       calibratedElectrons = cms.PSet(
                                                       initialSeed = cms.untracked.uint32(seed),
                                                       engineName = cms.untracked.string("TRandom3")
                                                                                     ),
                                                      )
    process.load("EgammaAnalysis.ElectronTools.calibratedElectrons_cfi")
    if datatype == "Data" or "embedded" in datatype:
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
