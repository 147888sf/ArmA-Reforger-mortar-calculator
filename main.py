from database import mortars
import bisect

def find_closest_keys(distances, target_dist):
    sorted_dists = sorted(distances.keys())
    if not sorted_dists:
        return None, None
    
    index = bisect.bisect_left(sorted_dists, target_dist)
    
    if index == 0:
        if target_dist < sorted_dists[0]:
            return None, None
        return sorted_dists[0], sorted_dists[0]
    if index == len(sorted_dists):
        if target_dist > sorted_dists[-1]:
            return None, None
        return sorted_dists[-1], sorted_dists[-1]
    
    low = sorted_dists[index - 1]
    high = sorted_dists[index]
    
    return low, high

def interpolate(low_dist, high_dist, target_dist, low_value, high_value):
    if low_dist == high_dist:
        return low_value
    ratio = (target_dist - low_dist) / (high_dist - low_dist)
    return low_value + (high_value - low_value) * ratio

# Selecting mortar
mortar_keys = list(mortars.keys())
for i, x in enumerate(mortar_keys):
    print(f'{i+1}: {x}')

while True:
    try:
        mortar_number = int(input('Enter mortar number: ')) - 1
        mortar = mortars[mortar_keys[mortar_number]]
        break
    except:
        pass

# Selecting ammo type
shell_keys = list(mortar.keys())
for i, x in enumerate(shell_keys):
    print(f'{i+1}: {x}')

while True:
    try:
        shell_number = int(input('Enter shell number: ')) - 1
        shell = mortar[shell_keys[shell_number]]
        break
    except:
        pass

# Entering target dist and elevation difference
while True:
    try:
        tdist = int(input('Enter target dist: '))
        break
    except:
        pass

while True:
    try:
        mortar_elevation = int(input('Enter mortar altitude: '))
        break
    except:
        pass

while True:
    try:
        target_elevation = int(input('Enter target altitude: '))
        break
    except:
        pass

alt_difference = mortar_elevation - target_elevation

for ring_amount in shell:
    try:
        low_dist, high_dist = find_closest_keys(shell[ring_amount]['Dists'], tdist)
        if low_dist is None or high_dist is None:
            continue
        
        dispersion = shell[ring_amount]['Dispersion']
        
        low_mils = shell[ring_amount]['Dists'][low_dist][0]
        high_mils = shell[ring_amount]['Dists'][high_dist][0]
        low_time = shell[ring_amount]['Dists'][low_dist][1]
        high_time = shell[ring_amount]['Dists'][high_dist][1]
        low_mils_per_100m = shell[ring_amount]['Dists'][low_dist][2]
        high_mils_per_100m = shell[ring_amount]['Dists'][high_dist][2]

        mils = interpolate(low_dist, high_dist, tdist, low_mils, high_mils)
        time = interpolate(low_dist, high_dist, tdist, low_time, high_time)
        mils_per_100m = interpolate(low_dist, high_dist, tdist, low_mils_per_100m, high_mils_per_100m)
        mils_per_1m = mils_per_100m/100
        mils_compensation_altitude = alt_difference*mils_per_1m

        mils += mils_compensation_altitude

        print(f'Ring amount: {ring_amount}; Dispersion: {dispersion}m; Elevation: {round(mils)}mils; Time in flight: {round(time, 2)}s')
    except Exception as e:
        print(f'Error processing ring amount {ring_amount}: {e}')