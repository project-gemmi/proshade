##############################################
##############################################
#   \file directAccess.py
#   \brief This code demonstrates the usage of the ProSHADE tool in the advanced mode.
#
#   This file should be the main source of wisdom when it comes to using ProSHADE in
#   Python in the advanced access mode. It demonstrates how many of the possible
#   tasks can be done, albeit one would not expect to be doing them all in one run...
#
#   Therefore, this should serve more as a "cook-book" rather than executable file. Generally,
#   the procedures shown here include creating the settings and structure objects, both from
#   file and from already existing Python array. It also shows how the map can be processed,
#   mapped onto spheres and how spherical harmonics are obtained, including how they can be
#   directly accessed from Python.
#
#   Moreover, structure re-boxing is shown, as well as the distances computation. The file also
#   demonstrates how the rotation function can be computed and how the E matrices, SO(3) coeff-
#   icients and the self-rotation map can be accessed, followed by a demonstration of how the
#   symmetry detection is called and results read.
#
#   Finally, the file shows and explains how the map overlay can be completed from Python, including
#   computation of the rotation function, access to it programatically and the same for the translation
#   function. Direct access to the optimal rotation Euler angles and rotation matrix is shown, as well
#   as direct access to the optimal translation vector.
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

##############################################
### Import modules
### =====================
###
### This is where Python modules are loaded.
###

### System modules
import sys
import numpy

### Import ProSHADE from non-system folder (local installation assumed)
sys.path.append                               ( "/Users/mysak/BioCEV/proshade/development/install/python3" )
import proshade

##############################################
### Create the ProSHADE_settings object
### ===================================
###
### This object contains all the settings that
### will be used throughout the ProSHADE exection.
### Therefore, the user should NOT change any
### of these settings once structures are read,
### as these values are assumend not the be
### changing throughout the run, except by the
### functions themselves.
###
### If you are running a different structure for
### a different purpose, please create a new
### settings object.
###

### Create the object
pSet                                          = proshade.ProSHADE_settings ()

### Set settings values
pSet.task                                     = proshade.Distances
pSet.verbose                                  = 1
pSet.rotationUncertainty                      = 5.0
pSet.moveToCOM                                = True
pSet.setMapResolutionChange                   ( False )

##############################################
### Create ProSHADE_structure object
### ================================
###
### This object is the basis of the advanced
### access interface. Most of the processing
### and computation functions are callable from
### this object. Each structure (map or co-ords)
### will need its own object. Also, these are
### pointers in C++ and so not deleting them
### before Python code termination will cause
### memory error message.
###
pStruct                                       = proshade.ProSHADE_data ( pSet )

##############################################
### Read in structure
### =================
###
### This function reads in a molecular structure
### from a file. It uses CCP4MAP library for
### reading in maps and MMDB2 for reading in
### PDB (and MTZ) files. It takes three arguments:
###
### 1) String: The path and filename of the structure to be read.
### 2) Int: The order of the structure. This is used to distinguish
###         multiple file outputs. Please used different value for each read in structure.
### 3) ProSHADE_settings*: The settings object with all values required for the reading in.
###
### If the function fails, it will exit proshade and
### print error message explaining what happened.
###
### At this point, the following variables are
### meaningfully (in Python access meaning) filled in:
###
### string pStruct.fileName                   //!< This is the original file from which the data were obtained.
### float  pStruct.xDimSize                   //!< This is the size of the map cell x dimension in Angstroms.
### float  pStruct.yDimSize                   //!< This is the size of the map cell y dimension in Angstroms.
### float  pStruct.zDimSize                   //!< This is the size of the map cell z dimension in Angstroms.
### float  pStruct.aAngle                     //!< This is the angle a of the map cell in degrees.
### float  pStruct.bAngle                     //!< This is the angle b of the map cell in degrees.
### float  pStruct.cAngle                     //!< This is the angle c of the map cell in degrees.
### int    pStruct.xDimIndices                //!< This is the size of the map cell x dimension in indices.
### int    pStruct.yDimIndices                //!< This is the size of the map cell y dimension in indices.
### int    pStruct.zDimIndices                //!< This is the size of the map cell z dimension in indices.
### int    pStruct.xGridIndices               //!< As far as I know, this is identical to the xDimIndices.
### int    pStruct.yGridIndices               //!< As far as I know, this is identical to the yDimIndices.
### int    pStruct.zGridIndices               //!< As far as I know, this is identical to the zDimIndices.
### int    pStruct.xAxisOrder                 //!< This is the order of the x axis.
### int    pStruct.yAxisOrder                 //!< This is the order of the y axis.
### int    pStruct.zAxisOrder                 //!< This is the order of the z axis.
### int    pStruct.xAxisOrigin                //!< This is the origin position along the x axis.
### int    pStruct.yAxisOrigin                //!< This is the origin position along the y axis.
### int    pStruct.zAxisOrigin                //!< This is the origin position along the z axis.
### int    pStruct.xFrom                      //!< This is the starting index along the x axis.
### int    pStruct.yFrom                      //!< This is the starting index along the y axis.
### int    pStruct.zFrom                      //!< This is the starting index along the z axis.
### int    pStruct.xTo                        //!< This is the final index along the x axis.
### int    pStruct.yTo                        //!< This is the final index along the y axis.
### int    pStruct.zTo                        //!< This is the final index along the z axis.
###
### Please note that if you change any of these,
### then things may stop making any sense. So,
### only change things if you know enough about
### the underlying code or if you are prepared
### to experiment and possibly get crazy results.
###
pStruct.readInStructure                       ( "/Users/mysak/LMB/proshade/exp/demo/C3.pdb", 0, pSet )

##############################################
### Create ProSHADE_structure object from map
### =========================================
###
### An alternative approach to creating the
### ProSHADE_data object is not to use a structure
### saved on the drive, but instead to supply all
### the required information as well as the map.
###
### This allows the user to obtain the map from
### any source they like, but it requires them
### to know the map information and how it should
### be supplied. In this case, the ProSHADE_data
### constructure takes the following arguments:
###
### ProSHADE_settings - object                //!< This object contains all the settings for further processing.
### structureName     - string                //!< A string to be used in naming any outout files from this structure.
### inputMap          - 1D float array        //!< Array containing the map values.
### xDimAngs          - float                 //!< The size of x dimension in Angstroms.
### yDimAngs          - float                 //!< The size of y dimension in Angstroms.
### zDimAngs          - float                 //!< The size of z dimension in Angstroms.
### xDimInds          - int                   //!< The size of x dimension in terms of number of indices.
### yDimInds          - int                   //!< The size of y dimension in terms of number of indices.
### zDimInds          - int                   //!< The size of z dimension in terms of number of indices.
### xFrom             - int                   //!< The initial index position along x axis.
### yFrom             - int                   //!< The initial index position along y axis.
### zFrom             - int                   //!< The initial index position along z axis.
### xTo               - int                   //!< The last index position along x axis.
### yTo               - int                   //!< The last index position along y axis.
### zTo               - int                   //!< The last index position along z axis.
### ord               - int                   //!< The order of the struct object in ProSHADE processing - important for multiple objects processing outputs.
###
### NOTE: There are two main conditions that need
### to be fullfilled for the constructor call to
### work. 1) The map dimensions needs to be the
### same as the x/y/zDimInds variables and 2)
### x/y/zTo - x/y/zFrom + 1 = x/y/zDimInds
###
### NOTE2: This function makes a lot of assumptions
### (all angles are 90 degrees, axis grids are
### equal to indices, axis order is XYZ and axis
### origin is the first index in all dimensions).
### If any of these are not true, the user is required
### to change the appropriate internal values after
### this function has returned the object.
###

#### Release the previous object
del pStruct

### Set example values
xDimIndices                                   = 100
yDimIndices                                   = 120
zDimIndices                                   = 60
xDimAngstroms                                 = xDimIndices * 1.3
yDimAngstroms                                 = yDimIndices * 1.3
zDimAngstroms                                 = zDimIndices * 1.3
xFrom                                         = int ( -xDimIndices/2 )
yFrom                                         = int ( -yDimIndices/2 )
zFrom                                         = int ( -zDimIndices/2 )
xTo                                           = int ( (xDimIndices/2)-1 )
yTo                                           = int ( (yDimIndices/2)-1 )
zTo                                           = int ( (zDimIndices/2)-1 )
ord                                           = 0

### Create example map (this will be a ball in the middle of the map)
testMap = numpy.empty ( [ ( xDimIndices * yDimIndices * zDimIndices ) ] )
for xIt in range( 0, xDimIndices ):
    for yIt in range( 0, yDimIndices ):
        for zIt in range( 0, zDimIndices ):
            ind = zIt + zDimIndices * ( yIt + yDimIndices * xIt )
            testMap[ind] = 1.0 / ( numpy.sqrt( numpy.power ( (xDimIndices/2) - xIt, 2.0 ) + numpy.power ( (yDimIndices/2) - yIt, 2.0 ) + numpy.power ( (zDimIndices/2) - zIt, 2.0 ) ) + 0.01 )

### Create the ProSHADE_data object without structure file on drive
pStruct                                       = proshade.ProSHADE_data ( pSet, "python_map_test", testMap, xDimAngstroms, yDimAngstroms, zDimAngstroms, xDimIndices, yDimIndices, zDimIndices, xFrom, yFrom, zFrom, xTo, yTo, zTo, ord )

### Should we ever need to use 3D map instead of 1D
### map, there is no way of passing 3D maps using SWIG
### and numpy (as far as I know). However, 3D map can
### be converted to 1D map using the ProSHADE supplied
### function. Be aware, this takes some time as python
### is not the master of for loops...

testMap3D = numpy.empty ( ( xDimIndices, yDimIndices, zDimIndices ) )
for xIt in range( 0, xDimIndices ):
    for yIt in range( 0, yDimIndices ):
        for zIt in range( 0, zDimIndices ):
            testMap3D[xIt][yIt][zIt] = 1.0 / ( numpy.sqrt( numpy.power ( (xDimIndices/2) - xIt, 2.0 ) + numpy.power ( (yDimIndices/2) - yIt, 2.0 ) + numpy.power ( (zDimIndices/2) - zIt, 2.0 ) ) + 0.01 )

pStruct2                                      = proshade.ProSHADE_data ( pSet, "python_map_test", proshade.convert3Dto1DArray ( testMap3D ), xDimAngstroms, yDimAngstroms, zDimAngstroms, xDimIndices, yDimIndices, zDimIndices, xFrom, yFrom, zFrom, xTo, yTo, zTo, ord )

del pStruct2

##############################################
### Write the internal map to disk
### ==============================
###
### This function writes the current internal
### map in CCP4 MAP format into a file given as
### its only argument. It uses all the internal
### values in the ProSHADE_data structure, so
### the user is responsible for these not being
### changed/or still making sense.
###
pStruct.writeMap                              ( "initialMap.map" )

##############################################
### Get internal map representation
### ===============================
###
### These functions returns the current (not only
### initial) internal map density values as a
### Numpy array. There is a 1D version returning
### a simple 1D numpy array, which can be indexed
### as [ z + pStruct.zDimIndices * ( y + pStruct.yDimIndices * x ) ].
### Obtaining this array is very fast, as it can
### be read directly from ProSHADE.
###
### Alternatively, there is a 3D version, which is,
### however, rather slow (approx 0.5 second for average
### sized map). The reason is that it requires
### looping through the 1D array and assigning the
### values to correct 3D array locations, which
### Python does not excel at.
###
### These functions can be called at any time on
### the ProSHADE_data object to get the current
### internal map representation.
###
initialMapArray1D                             = proshade.getMapPython1D ( pStruct )
initialMapArray3D                             = proshade.getMapPython3D ( pStruct )

##############################################
### Manipulate map and make ProSHADE accept it
### ==========================================
###
### This is an example snippet code, which changes
### the ProSHADE map in a simple way (feel free to
### change as you like) and then gives this new map
### to ProSHADE to replace the old map. This allows
### for the user to change/supply maps to ProSHADE
### in different than the standard ProSHADE reading
### it in format.
###
### NOTE: If you change the map dimensions, YOU are
### responsible for changing ALL the ProSHADE_data
### structure variables accordingly. Also, in this
### case, you must call the setNewMapPython() function
### instead of the simpler setMapPython() function.
### If you fail to do this, memory access problem are
### likely. Consider yourself warned! :-).
###

### Simple map manipulation
initialMapArray1D                             = initialMapArray1D / 2.0
proshade.setMapPython1D                       ( pStruct, initialMapArray1D )

initialMapArray3D                             = initialMapArray3D * 2.0
proshade.setMapPython3D                       ( pStruct, initialMapArray3D )

### With map dimensions changes
# Change map by removing last 3 y-axis indices
newMapArr1D                                   = numpy.empty ( ( pStruct.xDimIndices * ( pStruct.yDimIndices - 3 ) * pStruct.zDimIndices ) )
newMapArr3D                                   = numpy.empty ( [ pStruct.xDimIndices,  ( pStruct.yDimIndices - 3 ),  pStruct.zDimIndices ] )
for xIt in range( 0, pStruct.xDimIndices ):
    for yIt in range( 0, pStruct.yDimIndices ):
        for zIt in range( 0, pStruct.zDimIndices ):
            if yIt >= ( pStruct.yDimIndices - 3 ):
                continue
            arrPos                            = zIt + pStruct.zDimIndices * ( yIt  + pStruct.yDimIndices * xIt );
            newMapPos                         = zIt + pStruct.zDimIndices * ( yIt  + (pStruct.yDimIndices-3) * xIt );
            newMapArr1D[newMapPos]            = initialMapArray1D[arrPos] * 2
            newMapArr3D[xIt][yIt][zIt]        = initialMapArray1D[arrPos] / 2

# Now change the ProSHADE_data structure appropriately
pStruct.yDimSize                              = pStruct.yDimSize - ( ( pStruct.yDimSize / pStruct.yDimIndices ) * 3 )
pStruct.yDimIndices                           = pStruct.yDimIndices - 3
pStruct.yGridIndices                          = pStruct.yDimIndices
pStruct.yTo                                   = pStruct.yTo - 3

# And now make ProSHADE change the internal map completely
proshade.setNewMapPython1D                    ( pStruct, newMapArr1D )
proshade.setNewMapPython3D                    ( pStruct, newMapArr3D )

##############################################
### Process internal map
### ====================
###
### This function is where all the initial map
### manipulation happens. If requested (i.e. set
### in the settings object), it can do the following
### modifications of the internal map:
###
### 1) Map invertion: This switches all XYZ positions
###    to -X-Y-Z positions.
### 2) Map normalisation: This changes all density to
###    have mean zero and standard deviation one.
### 3) Map masking: Here, the map is blurred by a factor
###    and then a threshold is computed from the blurred
###    map. All passing points are left, non-passing points
###    become zeroes.
### 4) Map centering: The map will be moved to have its
###    centre of mass at the co-ordinate a/2, b/2, c/2.
### 5) Add extra space: This will add specified number of
###    Angstroms before and after the data along all
###    dimensions. This is useful to avoid unwanted inter-
###    actions from periodic cells.
### 6) Removing phase information: If you want molecular
###    replacement type of search instead, this option is
###    available.
###
### NOTE: All of these modifications can be done on PDB
### originating internal maps as well.
###
### NOTE2: This basically completes the map manipulation
### task - using the already described settings options,
### running the processInternalMap() function and getting
### the internal map into Python means that anything that
### can be done using the ProSHADE Map Manipulation task
### can also be done in Python using this code :-).
###
pStruct.processInternalMap                    ( pSet )

##############################################
### Map re-boxing
### =============
###
### This is the first task to be discussed as
### such. In the re-boxing functionality, the
### user first needs to determine the boundaries
### from which the new, re-boxed map should be
### created and then he needs to create a new
### empty structure, finally having it filled
### from the original structure using the already
### defined boundaries. The following three
### steps will accomplish just that using the
### ProSHADE map masking approach, but the user
### is free to change the bounds or determine his
### own boundaries, if he so pleases.
###

##############################################
### Determine new boundaries from mask (or custom)
### ==============================================
###
### If the user requires ProSHADE to determine
### new boundaries based on the ProSHADE masking
### procedure (and using the settings object
### values), the following function does just that.
###
### NOTE: Second parameter of the function is always
### 6. This is required from the Swig/Numpy/C++
### interface, just do not change the number.
###
### NOTE2: If the user wants to supply his own
### boundaries, this step can be skipped. Just
### make sure your custom boundaries are in the
### numpy.ndarray format, have length of 6 and
### dtype = int32. Also, the 6 numbers have
### meaning as follows:
###
###    [0] = min X-axis index
###    [1] = max X-axis index
###    [2] = min Y-axis index
###    [3] = max Y-axis index
###    [4] = min Z-axis index
###    [5] = max Z-axis index
###
minimalBounds                                 = pStruct.getReBoxBoundariesPy ( pSet, 6 )

print(minimalBounds)
# Expected output: [  6 109   4 127   6  69]

##############################################
### Create new structure to hold the new map
### ========================================
###
### Create a new structure, which will have the
### re-boxed map and values. This is so that the
### re-boxing would not be done in place.
###
reBoxStr                                      = proshade.ProSHADE_data ( pSet )

##############################################
### Set the re-boxed structure values and map
### =========================================
###
### Fill the new structure with the calling
### structure's map values in the boudaries
### supplied and set all of its required fields
### as well. The syntax of the call is that the
### calling structure is the one which is the
### source of map, while the second argument
### structure is the empty one.
###
pStruct.createNewMapFromBoundsPy              ( pSet, reBoxStr, minimalBounds )

##############################################
### Map internal map to spheres
### ===========================
###
### This function does the automatic spherical
### harmonics settings determination (unless
### these are already set in the settings object)
### and then it creates the required number of
### concentric spheres, finally mapping the inter-
### nal map onto the spheres using tri-linear
### interpolation.
###
### This will fill the following variables properly
###
### int           pStruct.noSpheres           //!< The number of spheres with map projected onto them.
### _float_list   pStruct.spherePos           //!< Vector of sphere radii from the centre of the map.
###                                           // To access this from Python, I recommend spPos = numpy.array ( pStruct.spherePos )
###                                           // To change from Python (should you need to), I recommend pStruct.spherePos[0] = X where is the new value
###
pStruct.mapToSpheres                          ( pSet )

##############################################
### Compute spherical harmonics
### ===========================
###
### This function takes the shells with the mapped
### data and proceeds to compute the spherical
### harmonics for each of them. This may take some
### time depending on the bandwidth and number of
### shells.
###
pStruct.computeSphericalHarmonics             ( pSet )

##############################################
### Accessing spherical harmonics
### =============================
###
### In order to access the spherical harmonics
### values for each sphere, please use the
### following function. It returns a complex
### type 2D numpy array with rows being shells
### and columns being the spherical harmonics
### values.
###
### To gain access to a particular band-order
### spherical harmonics value, please use the
### pStruct.sphericalHarmonicsIndex() function
### provided. This function takes three arguments:
###
### 1) order: This is signed int order (i.e. order
###           is from -band to band) requested.
### 2) band: The band requested.
### 3) shell: The shell for which to get the value.
###
### NOTE: The sphericalHarmonics variable is 2D
### array with shell index as the row - therefore
### the shell index needs to be given twice, once
### as the first index of sphericalHarmonics and
### secondly to the sphericalHarmonicsIndex()
### function.
###
sphericalHarmonics                            = proshade.getSphericalHarmonics ( pStruct )
Shell3Band4OrderMin2Value                     = sphericalHarmonics[3][ pStruct.sphericalHarmonicsIndex ( -2, 4, 3 ) ] # Order -2, band 4, shell 3.

print ( Shell3Band4OrderMin2Value )
# Expected output: (-0.0001720168888943213-0.0003544294668826651j)

##############################################
### Computing distances between two structures
### ==========================================
###
### In order to compute shape distances between
### two structures, two structures need to exist
### :-). Therefore, one more structure is created
### here and then both these structures are
### supplied to the three functions, i.e.
### proshade.computeEnergyLevelsDescriptor(),
### proshade.computeTraceSigmaDescriptor() and
### proshade.computeRotationunctionDescriptor().
###

### Create a second structure to have someting to compute distances to
pStruct_distTo                                = proshade.ProSHADE_data ( pSet )
pStruct_distTo.readInStructure                ( "/Users/mysak/LMB/proshade/exp/demo/testMap2.map", 1, pSet )
pStruct_distTo.processInternalMap             ( pSet )
pStruct_distTo.mapToSpheres                   ( pSet )
pStruct_distTo.computeSphericalHarmonics      ( pSet )

### Get the three descriptors
energyLevelsDescriptor                        = proshade.computeEnergyLevelsDescriptor    ( pStruct, pStruct_distTo, pSet )
traceSigmaDescriptor                          = proshade.computeTraceSigmaDescriptor      ( pStruct, pStruct_distTo, pSet )
fullRotationFunctionDescriptor                = proshade.computeRotationunctionDescriptor ( pStruct, pStruct_distTo, pSet )

print ( energyLevelsDescriptor )
# Expected output: 0.1020146560089361
print ( traceSigmaDescriptor )
# Expected output: 0.2692465414316738
print ( fullRotationFunctionDescriptor )
# Expected output: 0.24597629414455538

##############################################
### Delete the C++ pointer
### ======================
###
del pStruct_distTo

##############################################
### Computing self-rotation function
### ================================
###
### This function computes the self-rotation
### function by firstly computing and normalising
### the E matrices, then combining these into
### the SO(3) coefficients and finally calcula-
### ting the inverse SO(3) Fourier Transform
### (SOFT) from them. It therefore needs to be
### called before any symmetry detection can be
### attempted.
###
pStruct.getRotationFunction                   ( pSet )

##############################################
### Accessing E Matrices
### ====================
###
### ProSHADE allows access to the E matrices
### ( Integral _0 ^rMAX ( c^lm * c*^lm ) of
### the structure combination. These are
### returned as a 3D Numpy array with indices
### band of the E matrix, order1 of the E matrix
### and order2 of the E matrix. Note that because
### indices need to go from zero, the order of indexing
### goes like, for example, this:
###
### BAND = 2 || ORDER = -2  || INDEX [2][0]
### BAND = 2 || ORDER = -1  || INDEX [2][1]
### BAND = 2 || ORDER =  0  || INDEX [2][2]
### BAND = 2 || ORDER =  1  || INDEX [2][3]
### BAND = 2 || ORDER =  2  || INDEX [2][4]
### i.e. order index = ORDER + BAND
###
### NOTE: As Numpy arrays have single shape, the
### lower bands (which will have less orders)
### are padded with zeroes to have the same length
### as the largest band. This leads to a large
### redundancy of zeroes and makes the E matrix
### retrieval slow. If anyone needs to call this
### function frequently, please let me know and
### we can have a look as to how to improve this.
###
eMat                                          = proshade.getEMatrix( pStruct )
Band4OrderOneMin2OrderTwo3EMatrixValue        = eMat[4][2][7] # Band = 4, Order1 = -2 and Order2 = 3

print ( Band4OrderOneMin2OrderTwo3EMatrixValue )
# Expected output: (0.0004427206790703917+0.002131158008544593j)

##############################################
### Accessing SO(3) coefficients
### ============================
###
### ProSHADE also allows access to the SO(3)
### coefficients computed by normalising the E
### matrix values and dealing with the signs.
### The inverse SO(3) Fourier Transform (SOFT)
### of these values then results in the rotation
### function. The complete complex array of
### these values can be accessed as shown,
### however, the organisation of the array is
### done by the SOFT library and reflects
### internal value symmetries. Therefore, to
### access a specific value, please use the
### so3CoeffsArrayIndex() function as shown.
###
so3Coeffs                                     = proshade.getSO3Coeffs( pStruct )
so3CoeffsOrderOneMin1OrderTwo3Band5           = so3Coeffs[5][3][-1] # Accessing SO(3) coefficient value order1 = -1; order2 = 3, band = 5

print ( so3CoeffsOrderOneMin1OrderTwo3Band5 )
# Expected output: (0.0013320362162576496+0.001950971054873568j)

##############################################
### Accessing self-rotation function
### ================================
###
### ProSHADE also gives access to the self -
### rotation function as shown next. The function
### can be accessed as a 1D array as well as a 3D
### array, albeit the 3D array access is slower.
### The 1D array is ordered with X being the fastest
### axis, while Z being the slowest axis (same indexing
### as the ProSHADE internal map, but with different
### dimensions), that is a xyz position can be accessed as
### [ z + int ( pStruct.getMaxBand() * 2.0 ) * ( y + int ( pStruct.getMaxBand() * 2.0 ) * x ) ].
###
### The returned 3D array has dimensions 2 *
### bandwidth. Please note that the indices have
### nothing to do with the angle values, if you
### want to know the Euler angle values for a
### particular index, you need to convert it
### yourself. Alternatively (and a recommended
### approach is), you can use the
### getRotationMatrixFromEulerIndices() function
### also demonstrated here.
###
selfRotationFunction1D                        = proshade.getRotationFunction1D ( pStruct )
rotFnAlpha10Beta11Gamma7_1D                   = selfRotationFunction1D[ 7 + int ( pStruct.getMaxBand() * 2.0 ) * ( 11 + int ( pStruct.getMaxBand() * 2.0 ) * 10 ) ]# Accessing rotation function value for indices alpha = 10, beta = 11 and gamma = 7
rotMat                                        = proshade.getRotationMatrixFromRotFunIndices ( pStruct, 10, 11, 7 ) # Accessing rotation matrix for indices alpha = 10, beta = 11 and gamma = 7

print ( rotMat )
# Expected output: [[-0.04402094  0.96917621 -0.24240388]
# Expected output:  [-0.93713158  0.04402094  0.34618861]
# Expected output:  [ 0.34618861  0.24240388  0.90630779]]

selfRotationFunction3D                        = proshade.getRotationFunction3D ( pStruct )
rotFnAlpha10Beta11Gamma7_3D                   = selfRotationFunction3D[10][11][7] # Accessing rotation function value for indices alpha = 10, beta = 11 and gamma = 7
rotMat                                        = proshade.getRotationMatrixFromRotFunIndices ( pStruct, 10, 11, 7 ) # Accessing rotation matrix for indices alpha = 10, beta = 11 and gamma = 7

print ( rotMat )
# Expected output: [[-0.04402094  0.96917621 -0.24240388]
# Expected output:  [-0.93713158  0.04402094  0.34618861]
# Expected output:  [ 0.34618861  0.24240388  0.90630779]]


##############################################
### Run symmetry detection
### ======================
###
### Once the self-rotation computation is done
### (does not need getting it into python), the
### symmetry detection algorithm can be run as
### shown. Once the detectSymmetryInStructurePython()
### function is complete, the detected symmetry
### values can be obtained as demonstrated.
###

### Detect symmetry
pStruct.detectSymmetryInStructurePython       ( pSet )
symmetryType                                  = pStruct.getRecommendedSymmetryType ( pSet )
symmetryFold                                  = pStruct.getRecommendedSymmetryFold ( pSet )
symmetryAxes                                  = proshade.getRecommendedSymmetryAxesPython ( pStruct, pSet )

### Print results
print ( "Detected " + str( symmetryType ) + "-" + str( symmetryFold ) + " symetry." )
# Expected output: Detected C-4 symetry.
print ( "Fold      x         y         z       Angle     Height" )
for iter in range ( 0, len( symmetryAxes ) ):
     print ( "  %s    %+1.3f    %+1.3f    %+1.3f    %+1.3f    %+1.4f" % ( symmetryAxes[iter][0], symmetryAxes[iter][1], symmetryAxes[iter][2], symmetryAxes[iter][3], symmetryAxes[iter][4], symmetryAxes[iter][5] ) )
     
# Expected output: Fold      x         y         z       Angle     Height
# Expected output:   4    +0.257    +0.948    +0.186    +1.571    +0.0853

##############################################
### Get more symmetry results
### =========================
###
### Once the symmetry detection has been run,
### it is now possible to access more detailed
### results. These include the list of all
### detected cyclic point groups, a list of indices
### of these cyclic point groups which form any
### particular non-cyclic point group as well as
### list of all group elements for any point group
### comprised from detected cyclic point groups. For
### more details, please see the advancedAccess_symmetry.py
### file.
###

allCAxes                                      = proshade.getAllDetectedSymmetryAxes ( pStruct, pSet )

print ( "Found a total of " + str( len ( allCAxes ) ) + " cyclic point groups." )
# Expected output: Found a total of 1 cyclic point groups.

allNonCAxesIndices                            = proshade.getNonCSymmetryAxesIndices ( pSet )

print ( "Found a total of " + str( len ( allNonCAxesIndices["D"] ) ) + " dihedral point groups." )
# Expected output: Found a total of 0 dihedral point groups.

allGroupElements = proshade.getAllGroupElements ( pSet, pStruct, [0], "C" )

print ( "Found a total of " + str( len ( allGroupElements ) ) + " elements for the cyclic group C-" + str( int ( allCAxes[0][0] ) ) )
# Expected output: Found a total of 4 elements for the cyclic group C-4

print ( allGroupElements[1] )
# Expected output: [[ 0.06592191  0.05739252  0.99581337]
# Expected output:  [ 0.429437    0.89880204 -0.08039392]
# Expected output:  [-0.90029     0.43311134  0.03460428]]

##############################################
### Delete the C++ pointers
### =======================
###
del reBoxStr
del pStruct
del pSet

##############################################
### Computing the map overlay
### =========================
###
### As the overlay code does require the phase
### to be removed for optimal rotation compu-
### tation, most of the already demonstrated
### functions will need to be called again.
### However, they will not be described in much
### detail, as the descriptions are above.
###
### More specifically to the overlay computation,
### the user here should know how ProSHADE does
### this in order to call the functions properly.
### If you do not want to know the details, I
### suggest using the simpleAccess files instead,
### as they are almost as fast and do not require
### any internal knowledge (albeit they do not have
### as much flexibility as the advancedAccess)
###
### Therefore, the overlay mode is divided into two
### separate steps. Firstly, the phase is removed
### from the two internal maps and the resulting
### Patterson maps are subjected to the spherical
### harmonics decomposition. This makes sure the
### centering is precise, while it still allows
### for computing the rotation function (from the
### spherical harmonics values and inverse SOFT
### transform). The highest peak of the rotation
### function then gives the global optimal rotation
### angles.
###
### Then, all the internal data are released and the
### two structures are read again, this time with
### phase. The moving structure then has the optimal
### rotation applied (it must be retained from the
### phase-less step); now, the translation function
### can be computed for two optimally rotated structures.
### The results from the translation function then
### form the optimal translation vector. To do this,
### please follow the next section.
###

##############################################
### Create new settings object
### ==========================
###

### Create the object
pSet                                          = proshade.ProSHADE_settings ()

### Set settings values
pSet.task                                     = proshade.OverlayMap
pSet.verbose                                  = 4
pSet.requestedResolution                      = 8.0;
pSet.usePhase                                 = False;
pSet.changeMapResolution                      = True;
pSet.maskMap                                  = False;
pSet.moveToCOM                                = False;
pSet.normaliseMap                             = False;
pSet.reBoxMap                                 = False;

##############################################
### Create structure objects (phase-less)
### =====================================
###
pSet.usePhase                                 = False;
pStruct_static                                = proshade.ProSHADE_data ( pSet )
pStruct_moving                                = proshade.ProSHADE_data ( pSet )

### Read in the structures
pStruct_static.readInStructure                ( "/Users/mysak/BioCEV/proshade/00_GeneralTests/04_MapOverlay/test1.map", 0, pSet )
pStruct_moving.readInStructure                ( "/Users/mysak/BioCEV/proshade/00_GeneralTests/04_MapOverlay/test1_rotTrs.map", 1, pSet )

### Get spherical harmonics for both structures
pStruct_static.processInternalMap             ( pSet )
pStruct_moving.processInternalMap             ( pSet )

pStruct_static.mapToSpheres                   ( pSet )
pStruct_moving.mapToSpheres                   ( pSet )

pStruct_static.computeSphericalHarmonics      ( pSet )
pStruct_moving.computeSphericalHarmonics      ( pSet )

##############################################
### Create structure objects (phase-less)
### =====================================
###
### This is the first step not already described
### above. Albeit this step is similar to the
### symmetry detection self-rotation function,
### here the symmetry function is computed by
### combining the spherical harmonics coefficients
### from two different structures rather than from
### the same structure. The combination then results
### in the SO(3) group coefficients, which can be
### converted to the rotation function by the
### Fourier transform on the SO(3) group.
###
pStruct_moving.getOverlayRotationFunction     ( pSet, pStruct_static )

##############################################
### Acceasing rotation function and etc.
### ====================================
###
### Similarly to the self-rotation function used
### by the symmetry detection part above, ProSHADE
### allows access to the rotation function (as well
### as the E matrices and the SO(3) coefficients)
### using the same function as above. The only
### caveat that the user needs to be aware of is
### that these values are always saved in the
### moving structure class and never in the static
### structure class (static can be compared to
### multiple moving without the need for new
### static class).
###
rotationFunction1D                            = proshade.getRotationFunction1D ( pStruct_moving )
rotFnAlpha10Beta11Gamma7_1D                   = rotationFunction1D[ 7 + int ( pStruct_moving.getMaxBand() * 2.0 ) * ( 11 + int ( pStruct_moving.getMaxBand() * 2.0 ) * 10 ) ]# Accessing rotation function value for indices alpha = 10, beta = 11 and gamma = 7
rotMat                                        = proshade.getRotationMatrixFromRotFunIndices ( pStruct_moving, 10, 11, 7 ) # Accessing rotation matrix for indices alpha = 10, beta = 11 and gamma = 7

print ( rotMat )
# Expected output: [[-8.41253533e-01  5.40640817e-01 -1.85506948e-16]
# Expected output:  [-4.08589068e-01 -6.35776999e-01  6.54860734e-01]
# Expected output:  [ 3.54044443e-01  5.50903906e-01  7.55749574e-01]]

rotationFunction3D                            = proshade.getRotationFunction3D ( pStruct_moving )
rotFnAlpha10Beta11Gamma7_3D                   = rotationFunction3D[10][11][7] # Accessing rotation function value for indices alpha = 10, beta = 11 and gamma = 7
rotMat                                        = proshade.getRotationMatrixFromRotFunIndices ( pStruct_moving, 10, 11, 7 ) # Accessing rotation matrix for indices alpha = 10, beta = 11 and gamma = 7

print ( rotMat )
# Expected output: [[-8.41253533e-01  5.40640817e-01 -1.85506948e-16]
# Expected output:  [-4.08589068e-01 -6.35776999e-01  6.54860734e-01]
# Expected output:  [ 3.54044443e-01  5.50903906e-01  7.55749574e-01]]

##############################################
### Finding optimal rotation
### ========================
###
### Finally, once the rotation function is available,
### the optimal rotation Euler angles (ZXZ form) can
### be obtained as shown. Technically, this is done
### by finding the highest peak in the rotation map
### and then finding the Euler angles from its co-
### ordinates, but I assume this will be faster in
### C++ rather than in Python.
###
### NOTE: The output of the optimalRotationAngles()
### function is of the type proshade._double_list,
### which is a wrapper for the std::vector < proshade_double >
### type. This means that from Python the values can
### be accessed, but operations such as + or print
### will not work on it. Numpy functions, however,
### should work fine, or it can be simply converted
### to any other array-like type. The rotation matrix,
### on the other hand, is a numpy array with shape ( 3, 3 ).
###
optimalRotationAngles                         = pStruct_moving.getBestRotationMapPeaksEulerAngles ( pSet )
optimalRotationMatrix                         = proshade.getRotationMatrixFromEulerZXZ ( optimalRotationAngles )

print ( optimalRotationMatrix )
# Expected output: [[ 0.87256445 -0.4329139  -0.22631136]
# Expected output:  [-0.4332374  -0.47176062 -0.76795005]
# Expected output:  [ 0.22569146  0.76813246 -0.59919604]]

##############################################
### Delete the phase-less data
### ==========================
###
### As described above for the Overlay procedure,
### this is what needs to be done.
###
del pStruct_static
del pStruct_moving

##############################################
### Changing the settings
### =====================
###
### As described above for the Overlay procedure,
### this is what needs to be done - otherwise the
### translation cannot be obtained in the real
### space. Also, the map changing is required.
###
pSet.usePhase                                 = True
pSet.changeMapResolution                      = True

##############################################
### Read in the structures with phase
### =================================
###
### As described above for the Overlay procedure,
### this is what needs to be done. However, this
### time, the spherical harmonics decomposition
### is required only for the moving structure.
###

### Create objects
pStruct_static                                = proshade.ProSHADE_data ( pSet )
pStruct_moving                                = proshade.ProSHADE_data ( pSet )

### Read in the structures
pStruct_static.readInStructure                ( "/Users/mysak/BioCEV/proshade/00_GeneralTests/04_MapOverlay/test1.map", 0, pSet )
pStruct_moving.readInStructure                ( "/Users/mysak/BioCEV/proshade/00_GeneralTests/04_MapOverlay/test1_higherRotTrs.map", 1, pSet )

### Get spherical harmonics for moving structures
pStruct_static.processInternalMap             ( pSet )

pStruct_moving.processInternalMap             ( pSet )
pStruct_moving.mapToSpheres                   ( pSet )
pStruct_moving.computeSphericalHarmonics      ( pSet )

##############################################
### Rotate map
### ==========
###
### This function does the map rotation. In ProSHADE,
### this is done by computing the spherical harmonics,
### computing the Wigner D matrices for the required
### rotation (in Euler ZXZ angles) and then multi-
### plying the coefficients. This results in spherical
### harmonics coefficients of a rotated structure,
### which can subsequently be converted to the structure
### itself by inverse spherical harmonics decomposition
### calculation. This approach, however, uses interpolation
### to get the Cartesian map positions, so the resulting
### map tends to be blurry. It also introduces some artefacts,
### and as a results, the user us discouraged from using
### such maps directly. They are good enough to get the
### translation map in the next steps, but they are not
### good enough for further processing by ProSHADE or
### any other software. The recommended approach to computing
### the rotated map from the optimal angles (or rotation
### matrix) is to use EMDA.
###
### Nonetheless, if the user so desires, the rotated map
### can be obtained and processed as any other map and as
### described above.
###
pStruct_moving.rotateMap                      ( pSet, -optimalRotationAngles[0], optimalRotationAngles[1], -optimalRotationAngles[2] )

##############################################
### Zero padd the maps
### ==================
###
### The following code adds zeroes to both maps so that
### they will have the same dimensions (which will,
### in turn, be the maximum dimensions of the two
### structures). This is required for the Fourier
### coefficients used to compute the translation
### map to be of the same orders.
###
pStruct_static.zeroPaddToDims                 ( int ( numpy.max ( [ pStruct_static.getXDim(), pStruct_moving.getXDim() ] ) ),
                                                int ( numpy.max ( [ pStruct_static.getYDim(), pStruct_moving.getYDim() ] ) ),
                                                int ( numpy.max ( [ pStruct_static.getZDim(), pStruct_moving.getZDim() ] ) ) )
pStruct_moving.zeroPaddToDims                 ( int ( numpy.max ( [ pStruct_static.getXDim(), pStruct_moving.getXDim() ] ) ),
                                                int ( numpy.max ( [ pStruct_static.getYDim(), pStruct_moving.getYDim() ] ) ),
                                                int ( numpy.max ( [ pStruct_static.getZDim(), pStruct_moving.getZDim() ] ) ) )
                                                
##############################################
### Computing translation map
### =========================
###
### The following function takes the two structures
### and computes the translation function, which it
### then saves into the movings (calling) structure.
###
### NOTE: This function will fail if the two structures
### do not have the same dimensions and sampling, so
### for this reason it is required that the settings
### option for re-sampling the internal map to the
### same resolution and using the zero-padding above
### are used.
###
pStruct_moving.computeTranslationMap          ( pStruct_static )

##############################################
### Accessing the translation function
### ==================================
###
### The translation function can also be accessed
### from ProSHADE. This can again be done using the
### fast 1D version, which has the same indexing as
### the 1D internal map and the 1D rotation function,
### that is: [ z + int ( pStruct.getZDim() ) * ( y + int ( pStruct.getYDim() ) * x ) ].
###
### Alternatively, the 3D array can be obtained as
### shown below, with the same caveat as before,
### specifically that this is slow.
###
### The highest value of this translation function
### is the optimal global overlay translation
### vector for the two structures used to produce
### it.
###
translationMap1D = proshade.getTranslationFunction1D ( pStruct_moving )
translationMap3D = proshade.getTranslationFunction3D ( pStruct_moving )

print ( translationMap3D[1][2][3] )
# Expected output: (101.35688753123377-6.084559434255484e-15j)

##############################################
### Obtaining the optimal translation
### =================================
###
### The optimal translation vector is obtained
### from the translation map co-ordinates with
### the highest value. As this search should be
### faster in C++, such function is provided by
### ProSHADE as below.
###
### NOTE: The output of the getBestTranslationMapPeaksAngstrom()
### function is of the type proshade._double_list,
### which is a wrapper for the std::vector < proshade_double >
### type. This means that from Python the values can
### be accessed, but operations such as + or print
### will not work on it. Numpy functions, however,
### should work fine, or it can be simply converted
### to any other array-like type.
###
optimalTranslationVector                      = pStruct_moving.getBestTranslationMapPeaksAngstrom ( pStruct_static )

print ( optimalTranslationVector[0] )
# Expected output: 4.0

##############################################
### Translating the map
### ===================
###
### Although it is not recommended to use the
### internal ProSHADE maps directly (see the
### Rotate map section), or at least not the
### rotated maps, ProSHADE does have a function
### for translating the internal map by a given
### number of Angstroms along the three axes.
###
### The function can be used as shown, in this
### case to move the moving map, what can be
### useful for the visually confirming the ProSHADE
### values are correct. The resulting internal
### moved map can, of course, be accessed as
### before.
###
pStruct_moving.translateMap                   ( pSet, optimalTranslationVector[0], optimalTranslationVector[1], optimalTranslationVector[2] )

##############################################
### Clean up!
### =========
###
del pStruct_static
del pStruct_moving

##############################################
### Done
### ====
###
print ( "The end." )
