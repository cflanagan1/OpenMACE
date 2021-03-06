import numpy as np
import scipy as sp
import scipy.spatial
import sys, json
from matplotlib import path
import matplotlib.pyplot as pl
from geoLocation import Location
from planPath import planPath
from AircraftComModule import AircraftHandler

eps = sys.float_info.epsilon

#Ken added
def sortWesternPoints(locationArray):
    newlonLocation = []
    lonArray = []
    for i in range(0, len(locationArray), 1):
        location = locationArray[i]
        lonArray.append(location[1])
    newlonLocation = sorted(lonArray)

    arrayOrderSorted = []
    for i in range(0, len(newlonLocation), 1):
        for j in range(0, len(locationArray), 1):
            position = locationArray[j]
            if newlonLocation[i] == position[1]:
                arrayOrderSorted.append(j)
                break

    returnArraySorted = []
    #build a new array with the points
    for i in range(0, len(arrayOrderSorted), 1):
        returnArraySorted.append(locationArray[arrayOrderSorted[i]])

    return returnArraySorted

# Function to determine minimum bounding box of the points given in coords:
def minimum_bounding_box(coords):
    min_x = 100000 # start with something much higher than expected min
    min_y = 100000
    max_x = -100000 # start with something much lower than expected max
    max_y = -100000

    for item in coords:
        if item[0] < min_x:
            min_x = item[0]

        if item[0] > max_x:
            max_x = item[0]

        if item[1] < min_y:
            min_y = item[1]

        if item[1] > max_y:
            max_y = item[1]

    return [min_x, max_x, min_y, max_y]


def in_box(hotSpots, bounding_box):
    return np.logical_and(np.logical_and(bounding_box[0] <= hotSpots[:, 0],
                                         hotSpots[:, 0] <= bounding_box[1]),
                          np.logical_and(bounding_box[2] <= hotSpots[:, 1],
                                         hotSpots[:, 1] <= bounding_box[3]))


def voronoi(hotSpots, bounding_box):
    # Select towers inside the bounding box
    i = in_box(hotSpots, bounding_box)
    # Mirror points
    points_center = hotSpots[i, :]
    points_left = np.copy(points_center)
    points_left[:, 0] = bounding_box[0] - (points_left[:, 0] - bounding_box[0])
    points_right = np.copy(points_center)
    points_right[:, 0] = bounding_box[1] + (bounding_box[1] - points_right[:, 0])
    points_down = np.copy(points_center)
    points_down[:, 1] = bounding_box[2] - (points_down[:, 1] - bounding_box[2])
    points_up = np.copy(points_center)
    points_up[:, 1] = bounding_box[3] + (bounding_box[3] - points_up[:, 1])
    points = np.append(points_center,
                       np.append(np.append(points_left,
                                           points_right,
                                           axis=0),
                                 np.append(points_down,
                                           points_up,
                                           axis=0),
                                 axis=0),
                       axis=0)
    # Compute Voronoi
    vor = sp.spatial.Voronoi(points)
    # Filter regions
    regions = []
    for region in vor.regions:
        flag = True
        for index in region:
            if index == -1:
                flag = False
                break
            else:
                x = vor.vertices[index, 0]
                y = vor.vertices[index, 1]
                if not(bounding_box[0] - eps <= x and x <= bounding_box[1] + eps and
                       bounding_box[2] - eps <= y and y <= bounding_box[3] + eps):
                    flag = False
                    break
        if region != [] and flag:
            regions.append(region)
    vor.filtered_points = points_center
    vor.filtered_regions = regions
    return vor

def centroid_region(vertices):
    # Polygon's signed area
    A = 0
    # Centroid's x
    C_x = 0
    # Centroid's y
    C_y = 0
    for i in range(0, len(vertices) - 1):
        s = (vertices[i, 0] * vertices[i + 1, 1] - vertices[i + 1, 0] * vertices[i, 1])
        A = A + s
        C_x = C_x + (vertices[i, 0] + vertices[i + 1, 0]) * s
        C_y = C_y + (vertices[i, 1] + vertices[i + 1, 1]) * s
    A = 0.5 * A
    C_x = (1.0 / (6.0 * A)) * C_x
    C_y = (1.0 / (6.0 * A)) * C_y
    return np.array([[C_x, C_y]])


# Read in arguments:
#argboundaryVertices = np.asarray(json.loads(sys.argv[1]))
#arghotSpots = np.asarray(json.loads(sys.argv[2]))

argboundaryVertices = np.array([[37.886928977295476, -76.81533336639404], [37.890527558618025, -76.81533336639404], [37.890527558618025, -76.80932521820068], [37.886928977295476, -76.80932521820068], [37.886928977295476, -76.81533336639404]])
arghotSpotsIn = np.array([[37.88865631827983, -77.8123185634613]])

#Ken added
arghotSpots = sortWesternPoints(arghotSpotsIn)

# Find bottom left point of boundary:
originPoint = Location(argboundaryVertices[0][0], argboundaryVertices[0][1])

# Find X/Y distance from bottom left point to all other points:
xyBoundary =[]
for point in argboundaryVertices:
    tmpPoint = Location(point[0], point[1])
    xComp, yComp = originPoint.getXYFromPoint(tmpPoint)
    xyBoundary.append([xComp, yComp])
xyBoundaryArray = np.asarray(xyBoundary)

xyHotSpots =[]
for point in arghotSpots:
    tmpPoint = Location(point[0], point[1])
    xComp, yComp = originPoint.getXYFromPoint(tmpPoint)
    xyHotSpots.append([xComp, yComp])
xyHotSpotsArray = np.asarray(xyHotSpots)
# X/Y distance to each point is the X/Y coordinates of each point now.

# Normalize based on the transformed points:
temp_bounding_box = minimum_bounding_box(xyBoundaryArray)
normFactor_x = float(temp_bounding_box[1] - temp_bounding_box[0]) #this should always be positive based on the math
normFactor_y = float(temp_bounding_box[3] - temp_bounding_box[2])

normedBoundary = []
for point in xyBoundaryArray:
    bnormX = float((point[0]-temp_bounding_box[0])/normFactor_x)
    bnormY = float((point[1]-temp_bounding_box[2])/normFactor_y)
    normedBoundary.append([bnormX, bnormY])
boundaryVerticesNormalized = np.array(normedBoundary)

normedHotSpots = []
for hotPoints in xyHotSpotsArray:
    normX = float((hotPoints[0]-temp_bounding_box[0])/normFactor_x)
    normY = float((hotPoints[1]-temp_bounding_box[2])/normFactor_y)
    normedHotSpots.append([normX, normY])
hotSpotsNormalized = np.array(normedHotSpots)
# END NORMALIZE

# print "Normalize results:"
# print boundaryVerticesNormalized
# print hotSpotsNormalized


# Plan paths:
# **** Start main script **** #
validatePointsPath = path.Path(boundaryVerticesNormalized)

for i in xrange(0,len(hotSpotsNormalized)):
    if validatePointsPath.contains_point(hotSpotsNormalized[i]) == False:
        sys.exit("One of the selected points of interest is either on or not contained in the boundary: " + str(hotSpotsNormalized[i]))


bounding_box = minimum_bounding_box(boundaryVerticesNormalized)
vor = voronoi(hotSpotsNormalized, bounding_box)

fig = pl.figure()
ax = fig.gca()
# Plot initial points
ax.plot(vor.filtered_points[:, 0], vor.filtered_points[:, 1], 'go', markerSize=10)
# Plot ridges points
planningRegions = []
planningHotSpots = []
for region in vor.filtered_regions:
    vertices = vor.vertices[region, :]
    ax.plot(vertices[:, 0], vertices[:, 1], 'bo')
    planningRegions.append(vertices)
    regionPath = path.Path(vertices)
    for point in hotSpotsNormalized:
        if regionPath.contains_point((point[0], point[1])):
            planningHotSpots.append(point)

# Plot ridges
for region in vor.filtered_regions:
    vertices = vor.vertices[region + [region[0]], :]
    ax.plot(vertices[:, 0], vertices[:, 1], 'k-')

# Compute and plot centroids
centroids = []
for region in vor.filtered_regions:
    vertices = vor.vertices[region + [region[0]], :]
    centroid = centroid_region(vertices)
    centroids.append(list(centroid[0, :]))
    # ax.plot(centroid[:, 0], centroid[:, 1], 'c.')


# Plot boundary supplied:
ax.plot(xyBoundaryArray[:, 0], xyBoundaryArray[:, 1], 'b-')

ax.set_xlim([bounding_box[0] - 1, bounding_box[1] + 1])
ax.set_ylim([bounding_box[2] - 1, bounding_box[3] + 1])
# ax.set_xlim([temp_bounding_box[0] - 1, temp_bounding_box[1] + 1])
# ax.set_ylim([temp_bounding_box[2] - 1, temp_bounding_box[3] + 1])



# Plan the path based on the boundaries:
vehiclePaths = []
vehiclePathsNormalized = []
vehiclePathsLatLon = []
pVal = 0.5
gridSpacing = 0.25
for i in xrange(0, len(planningRegions)):
    tmpWaypoints = planPath(planningRegions[i], "NorthSouth", gridSpacing, planningHotSpots[i], pVal)
    unNormalizedPoints = []
    transformedPoints = []
    for point in tmpWaypoints:
        # Un-normalize first:
        newX = point[0]*normFactor_x + temp_bounding_box[0]
        newY = point[1]*normFactor_y + temp_bounding_box[2]
        unNormalizedPoints.append([newY, newX])
        # Transform to lat/lon:
        distance, bearing = originPoint.getDistanceBearingFromXY([newX, newY])
        lat, lon = originPoint.getLatLonFromDistanceBearing(distance, bearing)
        transformedPoints.append([lat, lon])
    vehiclePaths.append(unNormalizedPoints)
    vehiclePathsNormalized.append(tmpWaypoints)
    vehiclePathsLatLon.append(transformedPoints)

print vehiclePathsLatLon  # THIS IS WHAT SHOULD BE PLOTTED ON LEAFLET MAP

for path in vehiclePathsNormalized:
     ax.plot(np.array(path)[:,0], np.array(path)[:,1], 'r-')

pl.title('pVal: ' + str(pVal) + " / " + "gridSpacing: " + str(gridSpacing), fontsize=20)
pl.show()

# Done generating the appropriate points...lets now pass them on
#newObject = AircraftHandler(vehiclePathsLatLon, 20)
#newObject.runCommand()