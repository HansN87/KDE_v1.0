#include <stdio.h>
#include <vector>
#include <stdlib.h>

#include "TMath.h"

#include "AbsPhaseSpace.hh"
#include "AbsDensity.hh"
#include "FactorisedDensityPointSource.hh"

#include "Logger.hh"

FactorisedDensityPointSource::FactorisedDensityPointSource(const char* pdfName, 
                                     AbsPhaseSpace* thePhaseSpace, AbsDensity* sigmaEnergyPDF, Double_t const_scale) : AbsDensity(pdfName) {

  init(thePhaseSpace, sigmaEnergyPDF, const_scale); 
}


FactorisedDensityPointSource::~FactorisedDensityPointSource() {

}

void FactorisedDensityPointSource::init(AbsPhaseSpace* thePhaseSpace, AbsDensity* sigmaEnergyPDF, Double_t const_scale) {

  _const_scale = const_scale;

  m_phaseSpace = thePhaseSpace;  
  m_sigmaEnergyPDF = sigmaEnergyPDF;

  
  Logger::print(0,"%20.20s INFO: Creating factorised density of sigmaEnergy KDE and PS spatial term (Rayleigh in Log10(Psi) space))\n", m_name); 

  UInt_t sumDim = 0; 
  sumDim += m_sigmaEnergyPDF->phaseSpace()->dimensionality(); 

  if(sumDim != 2) {
	  Logger::print(2,"%20.20s ERROR: Dimensionality of Log10Sigma - Log10Energy PDF should be 2\n", m_name);
	  abort();
  }

  sumDim += 1;

  m_dim = m_phaseSpace->dimensionality(); 
  if (m_dim != 3) {
    Logger::print(2,"%20.20s ERROR: Dimensionalities of the combined PhaseSpace should be 3\n", m_name);
    abort(); 
  }

}

Double_t FactorisedDensityPointSource::density(std::vector<Double_t> &x) {  

  /* expect log10_Psi, log10_Sigma, log10_E
   */

  if (x.size() != m_dim) {
    Logger::print(2,"%20.20s ERROR: Dimensionality of vector (%d) does not correspond to phase space definition (%d)\n", 
       m_name, (UInt_t)x.size(), m_dim);
    abort(); 
  }
  
  Double_t prod = 1.;

  // first element is log10_Psi
  int idx_psi = 0;
  int idx_sigma = 1;
  int idx_E = 2;

  Double_t logPsi = x[idx_psi];
  Double_t logSigma = x[idx_sigma]; 
  Double_t logE = x[idx_E];

  // eval 2D PDF
  std::vector<Double_t> x_eval(2);
  x_eval[0] = logSigma; // log10 Sigma
  x_eval[1] = logE; // log10 Energy

  prod *= m_sigmaEnergyPDF->density(x_eval); 

  // eval Rayleigh PDF in log space and add arbitrary constant
  Double_t term1 = TMath::Power(10., 2.0 * logPsi);
  Double_t term2 = TMath::Power(10., 2.0 * logSigma);

  
  prod *= (term1 / term2 * TMath::Exp(-0.5 * term1 / term2) + _const_scale) * TMath::Log(10) ;

  // need to fix the 3D PDF norm to Meerkat convention 
  Double_t low = m_phaseSpace->lowerLimit(idx_psi);
  Double_t high = m_phaseSpace->upperLimit(idx_psi);
  prod *= (high-low);



   
  return prod; 

}
