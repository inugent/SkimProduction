import FWCore.ParameterSet.Config as cms

# MVA-MET specific for H->mu+tau channel
# definitions taken from https://ekptrac.physik.uni-karlsruhe.de/trac/Kappa/browser/Producers/python/KMET_cff.py
def mvaMET_MuTau(process):
    from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector
    process.goodOfflinePrimaryVertices = cms.EDFilter("PrimaryVertexObjectFilter",
        filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0) ),
        src=cms.InputTag('offlinePrimaryVertices')
    )
    # Muons (definition stolen from Roger)
    process.mvaMETMuons = cms.EDFilter("MuonSelector",
        src = cms.InputTag('muons'),
        cut = cms.string(
            "abs(eta)<2.1 & pt>15"                                      +
            ## muon ID
            "& isTrackerMuon"                                           +
            "& isPFMuon"                                                +
            "& globalTrack.isNonnull"                                   +
            "& innerTrack.hitPattern.numberOfValidPixelHits    >  0"    +
            "& innerTrack.normalizedChi2                       < 10"    +
            "& numberOfMatches                                 >  0"    +
            "& innerTrack.hitPattern.numberOfValidTrackerHits  >  5"    +
            "& globalTrack.hitPattern.numberOfValidHits        >  0"    +
            "& abs(innerTrack().dxy)                           <2.0"    +
            ## muon isolation (w/o deltaBeta, therefore weaker selection criteria)
            "& (pfIsolationR03.sumChargedHadronPt+pfIsolationR03.sumNeutralHadronEt+pfIsolationR03.sumPhotonEt)/pt < 0.3"
        ),
        filter = cms.bool(False)
    )
    # Taus for Mu+Tau channel (definition stolen from Roger)
    process.mvaMETTausMT = cms.EDFilter("PFTauSelector",
        src = cms.InputTag('hpsPFTauProducer'),
        BooleanOperator = cms.string("and"),
        discriminators = cms.VPSet(              
            cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByDecayModeFinding"                       ), selectionCut=cms.double(0.5)),
            cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits" ), selectionCut=cms.double(0.5)),
            cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByLooseElectronRejection"                 ), selectionCut=cms.double(0.5)),
            cms.PSet( discriminator=cms.InputTag("hpsPFTauDiscriminationByTightMuonRejection"                     ), selectionCut=cms.double(0.5)) 
            ),
        cut = cms.string("abs(eta) < 2.3 && pt > 20.0 "),
        filter = cms.bool(False)
    )
    # define MVA-Met producer (for Mu+Tau)
    from RecoJets.JetProducers.PileupJetIDParams_cfi import JetIdParams
    process.pfMetMVAMuTau = cms.EDProducer("PFMETProducerMVA",
        srcCorrJets     = cms.InputTag('ak5PFJetsCorr'),
        srcUncorrJets   = cms.InputTag('ak5PFJets'),
        srcPFCandidates = cms.InputTag('particleFlow'),
        srcVertices     = cms.InputTag('goodOfflinePrimaryVertices'),
        srcLeptons      = cms.VInputTag("mvaMETMuons"    , "mvaMETTausMT"),
        minNumLeptons   = cms.int32(0),
        srcRho          = cms.InputTag('kt6PFJets','rho'),
        globalThreshold = cms.double(-1.),#pfMet.globalThreshold,
        minCorrJetPt    = cms.double(-1.),
        inputFileNames  = cms.PSet(
            U = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmet_53_June2013_type1.root'),
            DPhi = cms.FileInPath('RecoMET/METPUSubtraction/data/gbrmetphi_53_June2013_type1.root'),
            CovU1 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru1cov_53_Dec2012.root'),
            CovU2 = cms.FileInPath('RecoMET/METPUSubtraction/data/gbru2cov_53_Dec2012.root')  
        ),
        loadMVAfromDB   = cms.bool(False),
        is42            = cms.bool(False), # CV: set this flag to true if you are running mvaPFMET in CMSSW_4_2_x                           
        corrector       = cms.string("ak5PFL1Fastjet"),
        useType1        = cms.bool(True),
        useOld42        = cms.bool(False),
        dZcut           = cms.double(0.1),
        impactParTkThreshold = cms.double(0.),
        tmvaWeights     = cms.string("RecoJets/JetProducers/data/TMVAClassificationCategory_JetID_MET_53X_Dec2012.weights.xml"),
        tmvaMethod      = cms.string("JetID"),
        version         = cms.int32(-1),
        cutBased        = cms.bool(False),                      
        tmvaVariables   = cms.vstring(
            "nvtx",
            "jetPt",
            "jetEta",
            "jetPhi",
            "dZ",
            "beta",
            "betaStar",
            "nCharged",
            "nNeutrals",
            "dR2Mean",
            "ptD",
            "frac01",
            "frac02",
            "frac03",
            "frac04",
            "frac05",
            ),
        tmvaSpectators  = cms.vstring(),
        JetIdParams     = JetIdParams,
        verbosity       = cms.int32(0)
    )
    
    process.MVAMETMuTauSequence = cms.Sequence( process.goodOfflinePrimaryVertices
    											* process.mvaMETMuons
                                          		* process.mvaMETTausMT
                                         		* process.pfMetMVAMuTau
                                         		)
