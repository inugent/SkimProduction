import FWCore.ParameterSet.Config as cms

def runPatMET(process):
    from PhysicsTools.PatAlgos.producersLayer1.metProducer_cfi import patMETs
    process.patPfMetT0rt = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0rt'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0rtT1 = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0rtT1'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0pc = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0pc'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0pcT1 = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0pcT1'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0rtTxy = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0rtTxy'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0rtT1Txy = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0rtT1Txy'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0pcTxy = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0pcTxy'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT0pcT1Txy = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT0pcT1Txy'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT1 = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT1'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patPfMetT1Txy = patMETs.clone(
                                 metSource=cms.InputTag('pfMetT1Txy'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patCaloMetT1 = patMETs.clone(
                                 metSource=cms.InputTag('caloMetT1'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patCaloMetT1T2 = patMETs.clone(
                                 metSource=cms.InputTag('caloMetT1T2'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patMet = patMETs.clone(
                                 metSource=cms.InputTag('pfMet'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patMVAMet = patMETs.clone(
                                 metSource=cms.InputTag('pfMEtMVA'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    process.patMVAMetMuTau = patMETs.clone(
                                 metSource=cms.InputTag('pfMetMVAMuTau'),
                                 addMuonCorrections=cms.bool(False),
                                 addGenMET=cms.bool(False)
                                 )
    
    process.runPatMetSequence = cms.Sequence(     
                                          process.patPfMetT0rt
                                        * process.patPfMetT0rtT1
                                        * process.patPfMetT0pc
                                        * process.patPfMetT0pcT1
                                        * process.patPfMetT0rtTxy
                                        * process.patPfMetT0rtT1Txy
                                        * process.patPfMetT0pcTxy
                                        * process.patPfMetT0pcT1Txy
                                        * process.patPfMetT1
                                        * process.patPfMetT1Txy
                                        * process.patCaloMetT1
                                        * process.patCaloMetT1T2
                                        * process.patMet
                                        * process.patMVAMet
                                        * process.patMVAMetMuTau
                                        )
