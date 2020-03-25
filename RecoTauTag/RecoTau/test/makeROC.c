#include <TPad.h>
#include <TGraphErrors.h>
#include <TFile.h>
#include <TH2D.h>
#include <TCanvas.h>
#include <iostream>

void makeROC()
{
   TFile * f_sig = TFile::Open("./output_VBFHToTauTau.root");
   TFile * f_bkg = TFile::Open("./output_QCD_Pt-15To7000.root");

   // 7 working points
   TH2D *h_sig[7], *h_bkg[7];
   for (int i = 0; i < 7; ++i) {
      char buffersig[100];
      sprintf(buffersig, "rerunMVAIsolationOnMiniAOD_Phase2/eff2_%d", i);
      h_sig[i] = (TH2D*)f_sig->Get(buffersig);
      char bufferbkg[100];
      sprintf(bufferbkg, "rerunMVAIsolationOnMiniAOD_Phase2/fak2_%d", i);
      h_bkg[i] = (TH2D*)f_bkg->Get(bufferbkg);
   }
   
   // 6 regions
   TGraphErrors *g[6];
   const TString regions[6] = {"a", "b", "c", "d", "e", "f"};
   for (int i = 0; i < 6; ++i) {
      g[i] = new TGraphErrors(8);
      g[i]->SetName("g_"+TString::Itoa(i, 10));
      g[i]->SetTitle(regions[i]+";signal efficiency;background efficiency");
   }

   for (int i = 0; i < 7; ++i) { 
   
      double eval[6], eerr[6];
      eval[0] = h_sig[i]->GetBinContent(1, 1);
      eerr[0] =   h_sig[i]->GetBinError(1, 1);
      eval[1] = h_sig[i]->GetBinContent(2, 1);
      eerr[1] =   h_sig[i]->GetBinError(2, 1);
      eval[2] = h_sig[i]->GetBinContent(3, 1);
      eerr[2] =   h_sig[i]->GetBinError(3, 1);
      eval[3] = h_sig[i]->GetBinContent(1, 2);
      eerr[3] =   h_sig[i]->GetBinError(1, 2);
      eval[4] = h_sig[i]->GetBinContent(2, 2);
      eerr[4] =   h_sig[i]->GetBinError(2, 2);
      eval[5] = h_sig[i]->GetBinContent(3, 2);
      eerr[5] =   h_sig[i]->GetBinError(3, 2);

      double mval[6], merr[6];
      mval[0] = h_bkg[i]->GetBinContent(1, 1);
      merr[0] =   h_bkg[i]->GetBinError(1, 1);
      mval[1] = h_bkg[i]->GetBinContent(2, 1);
      merr[1] =   h_bkg[i]->GetBinError(2, 1);
      mval[2] = h_bkg[i]->GetBinContent(3, 1);
      merr[2] =   h_bkg[i]->GetBinError(3, 1);
      mval[3] = h_bkg[i]->GetBinContent(1, 2);
      merr[3] =   h_bkg[i]->GetBinError(1, 2);
      mval[4] = h_bkg[i]->GetBinContent(2, 2);
      merr[4] =   h_bkg[i]->GetBinError(2, 2);
      mval[5] = h_bkg[i]->GetBinContent(3, 2);
      merr[5] =   h_bkg[i]->GetBinError(3, 2);

      for (int j = 0; j < 6; ++j) {
         g[j]->SetPoint(i, eval[j], mval[j]);
         g[j]->SetPointError(i, eerr[j], merr[j]);
      }

   }

   for (int i = 0; i < 6; ++i) {
      g[i]->SetPoint(8, 0., 0.);
   }

   TCanvas * c = new TCanvas("c", "", 1200, 800);
   c->Divide(3, 2);
   for (int i = 0; i < 6; ++i) {
      TPad * p = (TPad*)c->cd(i+1);
      g[i]->GetXaxis()->SetRangeUser(0., 1.);
      g[i]->SetMarkerStyle(20);
      g[i]->Draw("APE");
      g[i]->SetMaximum(1.);
      g[i]->SetMinimum(0.0001);
      g[i]->GetXaxis()->SetRangeUser(0., 1.);
      p->SetLogy();
      p->Update();
      c->Update();
      g[i]->Draw("APE");
   }

}

