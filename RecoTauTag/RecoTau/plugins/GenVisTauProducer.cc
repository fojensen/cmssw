// system include files
#include <memory>
// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
// new includes
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/Math/interface/LorentzVector.h"
typedef math::PtEtaPhiMLorentzVectorD PolarLorentzVector;
#include <TTree.h>
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

class GenVisTauProducer : public edm::EDProducer {
public:
	explicit GenVisTauProducer(const edm::ParameterSet&);
private:
   void produce(edm::Event&, const edm::EventSetup&) override;
   edm::EDGetTokenT<std::vector<reco::GenParticle>> genParticleTok_;
   TTree * tree;
   int nGenTaus;
   double pt[10], eta[10], phi[10], mass[10];
   int pdgId[10];
};

GenVisTauProducer::GenVisTauProducer(const edm::ParameterSet& iConfig)
{
   edm::InputTag genParticleTag_ = iConfig.getParameter<edm::InputTag>("genParticleCollection");
   genParticleTok_ = consumes<std::vector<reco::GenParticle>>(genParticleTag_);
   produces<pat::CompositeCandidateCollection>("genTaus");
   produces<pat::CompositeCandidateCollection>("genVisTaus");
   produces<pat::CompositeCandidateCollection>("genInvTaus");
   edm::Service<TFileService> fs;
   tree = fs->make<TTree>("tree", "tree");
   tree->Branch("nGenTaus", &nGenTaus, "nGenTaus/I");
   tree->Branch("pt", pt, "pt[nGenTaus]/D");
   tree->Branch("eta", eta, "eta[nGenTaus]/D");
   tree->Branch("phi", phi, "phi[nGenTaus]/D");
   tree->Branch("mass", mass, "mass[nGenTaus]/D");
   tree->Branch("pdgId", pdgId, "pdgId[nGenTaus]/I");
}

void GenVisTauProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   auto genTaus = std::make_unique<pat::CompositeCandidateCollection>();
   auto genVisTaus = std::make_unique<pat::CompositeCandidateCollection>();
   auto genInvTaus = std::make_unique<pat::CompositeCandidateCollection>();

   nGenTaus = 0;

   edm::Handle<std::vector<reco::GenParticle>> genParticles;
   iEvent.getByToken(genParticleTok_, genParticles);
    
   for (auto i = genParticles->begin(); i != genParticles->end(); ++i) {
      if (i->isLastCopy() && std::abs(i->pdgId())==15) {

         pat::CompositeCandidate tau;
         tau.addDaughter(*i);
         tau.setP4(i->polarP4());
         genTaus->push_back(tau);

         pat::CompositeCandidate tauvis;
         PolarLorentzVector tauvis_(0., 0., 0., 0.);
         tauvis.setPdgId(15);

         pat::CompositeCandidate tauinv;
         PolarLorentzVector tauinv_(0., 0., 0., 0.);

         for (auto j = genParticles->begin(); j != genParticles->end(); ++j) {
            if (j->mother()) {
               if (j->mother()->pt()==i->pt()) {
                  const int id = std::abs(j->pdgId());
                  const bool idInv = id==12||id==14||id==16;
                  bool idVis = id==11||id==13||id==22||id==211||id==111||id==321;
                  idVis = idVis || 323; // hack
                  if (idInv) {
                     tauinv.addDaughter(*j);
                     tauinv_ += j->polarP4();
                     if (id==12) tauvis.setPdgId(11);
                     if (id==14) tauvis.setPdgId(13);
                  }
                  if (idVis) {
                     tauvis.addDaughter(*j);
                     tauvis_ += j->polarP4();
                  }
                 
               }
            }
         }
       
         tauinv.setP4(tauinv_);
         tauvis.setP4(tauvis_);
   
         pt[nGenTaus] = tauvis.pt();
         eta[nGenTaus] = tauvis.eta();
         phi[nGenTaus] = tauvis.phi();
         mass[nGenTaus] = tauvis.mass();
         pdgId[nGenTaus] = tauvis.pdgId();
         ++nGenTaus;
 
         genInvTaus->push_back(tauinv);
         genVisTaus->push_back(tauvis);
      }
   }

   tree->Fill();
   iEvent.put(std::move(genTaus), std::string("genTaus"));
   iEvent.put(std::move(genVisTaus), std::string("genVisTaus"));
   iEvent.put(std::move(genInvTaus), std::string("genInvTaus"));

}

//define this as a plug-in
DEFINE_FWK_MODULE(GenVisTauProducer);

