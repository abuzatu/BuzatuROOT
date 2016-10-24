#include "HelperROOT.h"

void change_colour_of_histogram(TH1F* h, int colour)
{
  h->SetLineColor(colour);
}
