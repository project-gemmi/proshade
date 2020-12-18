##############################################
##############################################
#   \file advancedAccess_symmetry.py
#   \brief This code demonstrates the usage of the ProSHADE tool in the advanced mode.
#
#   This file shows a fast demonstration of how the advanced access interfacte can be used to compute the
#   symmetry of a particular structure and how the results can be obtained. This file does not contain all
#   the explanations and possible settings, for complete documentation, please see the advancedAccess.py
#   file instead.
#
#   Copyright by Michal Tykac and individual contributors. All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#   1) Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#   2) Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#   3) Neither the name of Michal Tykac nor the names of this code's contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#   This software is provided by the copyright holders and contributors "as is" and any express or implied warranties, including, but not limitted to, the implied warranties of merchantibility and fitness for a particular purpose are disclaimed. In     no event shall the copyright owner or the contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limitted to, procurement of substitute goods or services, loss of use, data     or profits, or business interuption) however caused and on any theory of liability, whether in contract, strict liability or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility     of such damage.
#
#   \author    Michal Tykac
#   \author    Garib N. Murshudov
#   \version   0.7.5.0
#   \date      DEC 2020
##############################################
##############################################


### System modules
import sys
import numpy

### Import ProSHADE from non-system folder (local installation assumed)
sys.path.append                               ( "/Users/mysak/BioCEV/proshade/experimental/install/python2" )
import proshade

### Create the settings object
pSet                                          = proshade.ProSHADE_settings ( proshade.Symmetry )

### Further useful settings
pSet.setSymmetryRotFunPeaks                   ( True );                              ## Should the new angle-axis space symmetry detection be used?
pSet.setBicubicInterpolationSearch            ( True );                              ## Should bi-cubic interpolation between peak grid indices be done?
pSet.setMaxSymmetryFold                       ( 30 );                                ## The maximum prime number fold that will be searched for.
pSet.verbose                                  = 1
pSet.forceP1                                  = True;                                ## Should PDB files be forced to have P1 spacegroup?
pSet.removeWaters                             = True;                                ## Should PDB files have their water molecules removed?
pSet.firstModelOnly                           = True;                                ## Should PDB files have only their first model used, or should ProSHADE use all models?
pSet.setProgressiveSphereMapping              ( True );                              ## Should smaller spheres be less sampled? It is considerably faster, but may sacrifice some (little) accuracy.
pSet.setMapResolutionChange                   ( True );                              ## Should maps be re-sample to the computation resolution using reciprocal-space re-sampling?
pSet.setMapResolutionChangeTriLinear          ( False );                             ## Should maps be re-sample to the computation resolution using real-space tri-linear interpolation?
pSet.setPeakNeighboursNumber                  ( 1 );                                 ## Numer of points in each direction which needs to be lower in order for the central point to be considered a peak.
pSet.setPeakNaiveNoIQR                        ( -999.9 );                            ## Peak searching threshold for too low peaks in number of inter-quartile ranges from median of the non-peak point values.
pSet.setMissingPeakThreshold                  ( 0.3 );                               ## Fraction of peaks that can be missing for missing axis search to be initiated.
pSet.setAxisComparisonThreshold               ( 0.1 );                               ## The dot product difference within which two axes are considered the same.
pSet.setMinimumPeakForAxis                    ( 0.3 );                               ## The minimum peak height for axis to be used.
#pSet.setRequestedSymmetry                     ( "C" );                               ## Which symmetry type (C,D,T,O or I) is requested to be detected? If none, then leave empty
#pSet.setRequestedFold                         ( 6 );                                 ## For C and D symmetries, which symmetry fold is requested to be detected? If none, leave 0.
pSet.setMapCentering                          ( True );                              ## Move structure COM to the centre of map box?
pSet.setExtraSpace                            ( 10.0 );                              ## Extra space in Angs to be added when creating internap map representation. This helps avoid map effects from other cells.
pSet.setResolution                            ( 6.0 );                               ## The resolution to which the calculations will be done. NOTE: Not necessarily the resolution of the structure!

### Create the structure object
pStruct                                       = proshade.ProSHADE_data ( pSet )

### Read in the structure
pStruct.readInStructure                       ( "./emd_6324.map", 0, pSet ) # This example uses EMD 6324 (PDB 3JA7)

### Process map
pStruct.processInternalMap                    ( pSet )

### Map to spheres
pStruct.mapToSpheres                          ( pSet )

### Compute spherical harmonics
pStruct.computeSphericalHarmonics             ( pSet )

### Compute self-rotation function
pStruct.getRotationFunction                   ( pSet )

### Detect recommended symmetry
pStruct.detectSymmetryInStructurePython       ( pSet )
recSymmetryType                               = pStruct.getRecommendedSymmetryType ( pSet )
recSymmetryFold                               = pStruct.getRecommendedSymmetryFold ( pSet )
recSymmetryAxes                               = proshade.getRecommendedSymmetryAxesPython ( pStruct, pSet )

### Print results
print ( "Detected " + str( recSymmetryType ) + "-" + str( recSymmetryFold ) + " symetry." )
print ( "Fold      x         y         z       Angle     Height" )
for iter in range ( 0, len( recSymmetryAxes ) ):
     print ( "  %s    %+1.3f    %+1.3f    %+1.3f    %+1.3f    %+1.4f" % ( recSymmetryAxes[iter][0], recSymmetryAxes[iter][1], recSymmetryAxes[iter][2], recSymmetryAxes[iter][3], recSymmetryAxes[iter][4], recSymmetryAxes[iter][5] ) )

### Expected output
#   Detected D-12 symetry.
#   Fold      x         y         z       Angle     Height
#     12    -0.007    +0.004    +1.000    +0.524    +0.7031
#      2    +0.788    +0.616    +0.007    +3.142    +0.4261

### Get list of all cyclic axes detected
allCAxes                                      = proshade.getAllDetectedSymmetryAxes ( pStruct, pSet )
print ( "Found a total of " + str( len ( allCAxes ) ) + " cyclic point groups." )

### Expected output
#   Found a total of 10 cyclic point groups.

### Get indices of which C axes form any detected non-C symmetry
allNonCAxesIndices                            = proshade.getNonCSymmetryAxesIndices ( pSet )
print ( "Found a total of " + str( len ( allNonCAxesIndices["D"] ) ) + " dihedral point groups." )

### Expected output
#   Found a total of 26 dihedral point groups.

#  NOTE: To get all the point group elements, one needs to supply the list of all cyclic point groups which comprise the
#        requested point group. This is relatively simple for T, O and I symmetries, as such a list is already produced by
#        ProSHADE - see the following examples:
#
#        allGroupElements = proshade.getAllGroupElements ( pSet, pStruct, allNonCAxesIndices['T'], "T" )
#        allGroupElements = proshade.getAllGroupElements ( pSet, pStruct, allNonCAxesIndices['O'], "O" )
#        allGroupElements = proshade.getAllGroupElements ( pSet, pStruct, allNonCAxesIndices['I'], "I" )
#
#        For cyclic point groups, this is also simple, as one can select the required >index< from the allCs variable and use
#        NOTE: The [] around index is required, as the function expects an array (list) and not an int!
#
#        allGroupElements = proshade.getAllGroupElements ( pSet, pStruct, [index], "C" )
#
#        The only problem comes when D is to be used, as ProSHADE gives a vector (list) of all combinations (also as vector/list) of cyclic point groups which form the
#        D point groups. Therefore, to select the recommended D point group from this list, a search needs to be done. This is shown in the following code.

### Define isclose() for comparing floats
def isclose(a, b, rel_tol=1e-06, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

### Find the indices of the best dihedral combination
bestDCombination                              = []
for dIt in range ( 0, len ( allNonCAxesIndices['D'] ) ):
    firstMatch = False
    secondMatch = False
    for recIt in range ( 0, len( recSymmetryAxes ) ):
        if ( isclose ( allCAxes[allNonCAxesIndices['D'][dIt][0]][1], recSymmetryAxes[0][1] ) ) and \
           ( isclose ( allCAxes[allNonCAxesIndices['D'][dIt][0]][2], recSymmetryAxes[0][2] ) ) and \
           ( isclose ( allCAxes[allNonCAxesIndices['D'][dIt][0]][3], recSymmetryAxes[0][3] ) ):
            firstMatch = True
            
        if ( isclose ( allCAxes[allNonCAxesIndices['D'][dIt][1]][1], recSymmetryAxes[1][1] ) ) and \
           ( isclose ( allCAxes[allNonCAxesIndices['D'][dIt][1]][2], recSymmetryAxes[1][2] ) ) and \
           ( isclose ( allCAxes[allNonCAxesIndices['D'][dIt][1]][3], recSymmetryAxes[1][3] ) ):
            secondMatch = True
            
    if firstMatch and secondMatch:
        bestDCombination.append               ( allNonCAxesIndices['D'][dIt][0] )
        bestDCombination.append               ( allNonCAxesIndices['D'][dIt][1] )
        
### Get the group elements for the best dihedral group
allGroupElements                              = proshade.getAllGroupElements ( pSet, pStruct, bestDCombination, "D" )

### Print the first non-identity element
print ( "Found a total of " + str( len ( allGroupElements ) ) + " group " + str( bestDCombination ) + " elements." )
print ( "The first non-identity element is:" )
print ( "  %+1.3f    %+1.3f    %+1.3f " % ( allGroupElements[1][0][0], allGroupElements[1][0][1], allGroupElements[1][0][2] ) )
print ( "  %+1.3f    %+1.3f    %+1.3f " % ( allGroupElements[1][1][0], allGroupElements[1][1][1], allGroupElements[1][1][2] ) )
print ( "  %+1.3f    %+1.3f    %+1.3f " % ( allGroupElements[1][2][0], allGroupElements[1][2][1], allGroupElements[1][2][2] ) )

### Expected output
#   Found a total of 24 group [0, 9] elements.
#   The first non-identity element is:
#     +0.866    -0.500    +0.001 
#     +0.500    +0.866    +0.004 
#     -0.003    -0.003    +1.000 

### Release C++ pointers
del pStruct
del pSet

### Done
