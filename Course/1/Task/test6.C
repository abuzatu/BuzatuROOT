#include "TH1F.h"
#include "TCanvas.h"

void change_color(TH1F* h, int color)
{
  h->SetLineColor(color);
}

int main()
{
  int color=2;
  TH1F* h = new TH1F("hist","hist",10,0,100);
  h->Fill(23,3);
  h->Fill(44,6);
  h->Fill(67,2);
  change_color(h,color);
  TCanvas* c = new TCanvas("c","c",600,400);
  h->Draw();
  c->Print("./histogram6.pdf");
  return 0;
}
