from rama import read
from rama.models.source import SourcePosition
from rama.models.coordinates import SpaceFrame
from rama.models.photdmalt import PhotometryFilter

parser = read('simple.vot.xml')

print(parser)

print('SpaceFrame:')
space_frames = parser.find_instances(SpaceFrame)
for sf in space_frames:
    print(sf.space_ref_frame)
    
print('\nSourcePosition:')
source_positions = parser.find_instances(SourcePosition)
for pos in source_positions:
    print (pos.coord)
    print (pos.coord.frame)
    print (pos.coord.ra.degree)
    print (type(pos.coord.frame))
    
print('\nPhotometryFilter:')
phot_filters = parser.find_instances(PhotometryFilter)
for pf in phot_filters:
    print(pf.name)
    print('   TransmissionPoint:')
    if pf.transmission_point is not None:
        for tp in pf.transmission_point:
            print(tp.spectral)
            print(tp.spectral_error)

print('\nDone')

