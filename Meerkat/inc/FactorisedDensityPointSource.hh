#ifndef FACTORISED_DENSITY_POINTSOURCE
#define FACTORISED_DENSITY_POINTSOURCE

#include "AbsDensity.hh"
#include "AbsPhaseSpace.hh"



#include "TMath.h"

#include <vector>

/// This class generates the joint pdf in 3D from a 2D KDE (log Sigma, log E) and 
/// a rayleigh spatial term in log Psi (1D conditional PDF f(log Psi | log Sigma)

class FactorisedDensityPointSource : public AbsDensity {

  public: 
  
    //! Constructor of factorised density of an arbitrary number of density components
    /*! 
      \param [in] pdfName PDF name
      \param [in] thePhaseSpace phase space. Dimensionality of the phase space should be equal to 3
      \param [in] sigmaEnergyPDF KDE. a 2D KDE that takes log Sigma as first argument
      			and log E as second argument
      \param [in] const_scale - value of the constant to be added to the rayleigh pdf
     			(allows heavy tails to be estimated in second 3D KDE using this as approx) 
    */ 
    FactorisedDensityPointSource(const char* pdfName, 
                      AbsPhaseSpace* thePhaseSpace, AbsDensity* sigmaEnergyPDF, Double_t const_scale=0.3);

    //! Destructor
    virtual ~FactorisedDensityPointSource(); 

    //! Calculate PDF value at the given point
    /*! 
        \param [in] x the point at which to calculate the PDF
        \return PDF value
    */
    Double_t density(std::vector<Double_t> &x);

    //! Return phase space definition for this PDF
    /*!
       \return PDF phase space
    */
    AbsPhaseSpace* phaseSpace() { return m_phaseSpace; }
    
  private: 
    
    //! Common initialise function used by all constructors. 
    /*! 
      \param [in] thePhaseSpace phase space
      \param [in] sigmaEnergyPDF : 2D KDE
      \param [in] const_scale : constant to be added to rayleigh
    */ 
    void init(AbsPhaseSpace* thePhaseSpace, 
              AbsDensity* sigmaEnergyPDF, Double_t const_scale);
  
    //! Reference to phase space
    AbsPhaseSpace* m_phaseSpace; 
    
    //! 2D KDE density
    AbsDensity* m_sigmaEnergyPDF; 

    //! value of constant to be added to rayleigh
    Double_t _const_scale;
    
    //! Cached dimensionality of the phase space
    UInt_t m_dim; 

}; 

#endif
