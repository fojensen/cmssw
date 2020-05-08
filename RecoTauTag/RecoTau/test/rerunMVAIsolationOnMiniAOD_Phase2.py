import FWCore.ParameterSet.Config as cms

process = cms.Process("rerunMVAIsolationOnMiniAODPhase2")

process.load('Configuration.Geometry.GeometryExtended2026D41Reco_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_upgrade2023_realistic_v2')
process.load("Configuration.StandardSequences.MagneticField_cff")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10000)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'/store/mc/PhaseIIMTDTDRAutumn18MiniAOD/QCD_Pt-15To7000_TuneCP5_Flat_14TeV-pythia8/MINIAODSIM/PU200_103X_upgrade2023_realistic_v2-v1/40000/FFE6B9AD-6109-FA47-9273-24C908EC90EE.root',
        '/store/mc/PhaseIIMTDTDRAutumn18MiniAOD/VBFHToTauTau_M125_14TeV_powheg_pythia8_correctedGridpack/MINIAODSIM/PU200_103X_upgrade2023_realistic_v2-v1/120000/2AD029AA-54C4-3D44-B934-24F19454A6FD.root',
    )
)

process.TFileService = cms.Service("TFileService",
    #fileName = cms.string('output_QCD_Phase2.root')
    fileName = cms.string('output_VBFHToTauTau_Phase2.root')
)

from RecoTauTag.RecoTau.TauDiscriminatorTools import noPrediscriminants
### Load PoolDBESSource with mapping to payloads
process.load('RecoTauTag.Configuration.loadRecoTauTagMVAsFromPrepDB_cfi')

from RecoTauTag.RecoTau.PATTauDiscriminationByMVAIsolationRun2_cff import *
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2raw = patDiscriminationByIsolationMVArun2v1raw.clone(
    PATTauProducer = cms.InputTag('slimmedTaus'),
    Prediscriminants = noPrediscriminants,
    loadMVAfromDB = cms.bool(True),
    #loadMVAfromDB = cms.bool(False),
    #inputFileName = cms.FileInPath("gbrDiscriminationByIsolationMVAPhase2.root"),
    mvaName = cms.string("RecoTauTag_tauIdMVAIsoPhase2"),
    mvaOpt = cms.string("kDBnewDMwLTwGJPhase2"),
    verbosity = cms.int32(0)
)

process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose = patDiscriminationByIsolationMVArun2v1Loose.clone(
    PATTauProducer = cms.InputTag('slimmedTaus'),
    Prediscriminants = noPrediscriminants,
    toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2raw'),
    key = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2raw:category'),
    loadMVAfromDB = cms.bool(True),
    #loadMVAfromDB = cms.bool(False),
    #inputFileName = cms.FileInPath("wpDiscriminationByIsolationMVAPhase2_tauIdMVAIsoPhase2.root"),
    mvaOutput_normalization = cms.string("RecoTauTag_tauIdMVAIsoPhase2_mvaOutput_normalization"),
    mapping = cms.VPSet(
        cms.PSet(
            category = cms.uint32(0),
            cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff95"),
            variable = cms.string("pt"),
        )
    )
)

process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VLoose = process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VLoose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff90")
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Loose = process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff80")
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Medium = process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff70")
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Tight = process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff60")
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VTight = process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff50")
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVTight = process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff40")

process.rerunMvaIsolation2Seq_Phase2 = cms.Sequence(
    process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2raw
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VLoose
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Loose
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Medium
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Tight
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VTight
    * process.rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVTight
)

# embed new id's into tau
embedID = cms.EDProducer("PATTauIDEmbedder",
    src = cms.InputTag('slimmedTaus'),
    tauIDSources = cms.PSet(
        byIsolationMVADBnewDMwLTPhase2raw = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2raw'),
        byVVLooseIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVLoose'),
        byVLooseIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VLoose'),
        byLooseIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Loose'),
        byMediumIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Medium'),
        byTightIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2Tight'),
        byVTightIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VTight'),
        byVVTightIsolationMVADBnewDMwLTPhase2 = cms.InputTag('rerunDiscriminationByIsolationMVADBnewDMwLTPhase2VVTight'),
    ),
)
setattr(process, "newTauIDsEmbedded", embedID)

process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
process.tauGenJets.GenParticles = "prunedGenParticles"

process.rerunMVAIsolationOnMiniAOD_Phase2 = cms.EDAnalyzer(
    'rerunMVAIsolationOnMiniAOD_Phase2',
    genJetCollection = cms.InputTag("slimmedGenJets"), #comment out to run on data
    genVisTauCollection = cms.InputTag("tauGenJets"), #comment out to run data
)

process.p = cms.Path(
    process.rerunMvaIsolation2Seq_Phase2
    *process.newTauIDsEmbedded
    *process.tauGenJets
    *process.rerunMVAIsolationOnMiniAOD_Phase2
)

#process.outpath = cms.EndPath(process.out)

