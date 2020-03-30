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
process.rerunDiscriminationByIsolationMVAPhase2raw = patDiscriminationByIsolationMVArun2v1raw.clone(
    PATTauProducer = cms.InputTag('slimmedTaus'),
    Prediscriminants = noPrediscriminants,
    loadMVAfromDB = cms.bool(True),
    #loadMVAfromDB = cms.bool(False),
    #inputFileName = cms.FileInPath("gbrDiscriminationByIsolationMVAPhase2.root"),
    mvaName = cms.string("RecoTauTag_tauIdMVAIsoPhase2"),
    mvaOpt = cms.string("Phase2"),
    verbosity = cms.int32(0)
)

process.rerunDiscriminationByIsolationMVAPhase2VVLoose = patDiscriminationByIsolationMVArun2v1Loose.clone(
    PATTauProducer = cms.InputTag('slimmedTaus'),
    Prediscriminants = noPrediscriminants,
    toMultiplex = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2raw'),
    key = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2raw:category'),
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

process.rerunDiscriminationByIsolationMVAPhase2VLoose = process.rerunDiscriminationByIsolationMVAPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVAPhase2VLoose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff90")
process.rerunDiscriminationByIsolationMVAPhase2Loose = process.rerunDiscriminationByIsolationMVAPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVAPhase2Loose.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff80")
process.rerunDiscriminationByIsolationMVAPhase2Medium = process.rerunDiscriminationByIsolationMVAPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVAPhase2Medium.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff70")
process.rerunDiscriminationByIsolationMVAPhase2Tight = process.rerunDiscriminationByIsolationMVAPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVAPhase2Tight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff60")
process.rerunDiscriminationByIsolationMVAPhase2VTight = process.rerunDiscriminationByIsolationMVAPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVAPhase2VTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff50")
process.rerunDiscriminationByIsolationMVAPhase2VVTight = process.rerunDiscriminationByIsolationMVAPhase2VVLoose.clone()
process.rerunDiscriminationByIsolationMVAPhase2VVTight.mapping[0].cut = cms.string("RecoTauTag_tauIdMVAIsoPhase2_WPEff40")

process.rerunMvaIsolation2Seq_Phase2 = cms.Sequence(
    process.rerunDiscriminationByIsolationMVAPhase2raw
    * process.rerunDiscriminationByIsolationMVAPhase2VVLoose
    * process.rerunDiscriminationByIsolationMVAPhase2VLoose
    * process.rerunDiscriminationByIsolationMVAPhase2Loose
    * process.rerunDiscriminationByIsolationMVAPhase2Medium
    * process.rerunDiscriminationByIsolationMVAPhase2Tight
    * process.rerunDiscriminationByIsolationMVAPhase2VTight
    * process.rerunDiscriminationByIsolationMVAPhase2VVTight
)

# embed new id's into tau
embedID = cms.EDProducer("PATTauIDEmbedder",
    src = cms.InputTag('slimmedTaus'),
    tauIDSources = cms.PSet(
        byIsolationMVAPhase2raw = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2raw'),
        byVVLooseIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2VVLoose'),
        byVLooseIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2VLoose'),
        byLooseIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2Loose'),
        byMediumIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2Medium'),
        byTightIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2Tight'),
        byVTightIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2VTight'),
        byVVTightIsolationMVAPhase2New = cms.InputTag('rerunDiscriminationByIsolationMVAPhase2VVTight'),
    ),
)
setattr(process, "newTauIDsEmbedded", embedID)

## added for mvaIsolation on miniAOD testing
#process.out = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string(filetag+'_miniaod.root'),
#    ## save only events passing the full path
#    SelectEvents = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
#    ## save PAT output; you need a '*' to unpack the list of commands
#    ##'patEventContent'
#    outputCommands = cms.untracked.vstring(
#        'drop *',
#        'keep *_newTauIDsEmbedded_*_*',
#        'keep *_prunedGenParticles_*_*'
#    )
#)

#process.genVisTauProducer = cms.EDProducer("GenVisTauProducer",
#    genParticleCollection = cms.InputTag("prunedGenParticles")
#)

process.rerunMVAIsolationOnMiniAOD_Phase2 = cms.EDAnalyzer(
    'rerunMVAIsolationOnMiniAOD_Phase2',
    genJetCollection = cms.InputTag("slimmedGenJets"), #comment out to run on data
    #genVisTauCollection = cms.InputTag("genVisTauProducer:genVisTaus"), #comment out if running on data
    genParticleCollection  = cms.InputTag("prunedGenParticles") #comment out to run on data
)

process.p = cms.Path(
    process.rerunMvaIsolation2Seq_Phase2
    *process.newTauIDsEmbedded
    #*process.genVisTauProducer
    *process.rerunMVAIsolationOnMiniAOD_Phase2
)

#process.outpath = cms.EndPath(process.out)

