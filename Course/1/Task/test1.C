{
  TH1F* h = new TH1F("hist","hist",10,0,100);
  h->Fill(23,3);
  h->Fill(44,6);
  h->Fill(67,2);
  TCanvas* c = new TCanvas("c","c",600,400);
  h->Draw();
  c->Print("./histogram1.pdf");
}
