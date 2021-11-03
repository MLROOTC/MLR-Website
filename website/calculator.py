import math

all_result_types = ['HR', '3B', '2B', '1B', 'BB', 'FO', 'K', 'PO', 'RGO', 'LGO',
                    'BUNT 1B', 'BUNT SAC', 'BUNT K', 'BUNT GO', 'BUNT DP',
                    'STEAL 2B', 'STEAL 3B', 'STEAL HOME', 'MSTEAL 3B', 'MSTEAL HOME',
                    'CS 2B', 'CS 3B', 'CS HOME', 'CMS 3B', 'CMS HOME',
                    'SAC', 'AUTO K', 'AUTO BB', 'IBB']
out_types = ['FO', 'K', 'PO', 'RGO', 'LGO', 'BUNT SAC', 'BUNT K', 'BUNT GO', 'BUNT DP', 'CS 2B', 'CS 3B', 'CS HOME', 'CMS 3B', 'CMS HOME', 'SAC', 'AUTO K']
hit_types = ['HR', '3B', '2B', '1B']
not_pa_types = ['STEAL 2B', 'STEAL 3B', 'STEAL HOME', 'MSTEAL 3B', 'MSTEAL HOME',
                'CS 2B', 'CS 3B', 'CS HOME', 'CMS 3B', 'CMS HOME', 'AUTO BB', 'IBB']
not_ab_types = ['STEAL 2B', 'STEAL 3B', 'STEAL HOME', 'MSTEAL 3B', 'MSTEAL HOME',
                'CS 2B', 'CS 3B', 'CS HOME', 'CMS 3B', 'CMS HOME',
                'AUTO BB', 'IBB', 'BB', 'SAC', 'BUNT SAC']
steal_types = ['STEAL 2B', 'STEAL 3B', 'STEAL HOME', 'MSTEAL 3B', 'MSTEAL HOME']
steal_attempt_types = ['STEAL 2B', 'STEAL 3B', 'STEAL HOME', 'MSTEAL 3B', 'MSTEAL HOME',
                       'CS 2B', 'CS 3B', 'CS HOME', 'CMS 3B', 'CMS HOME']
caught_stealing_types = ['CS 2B', 'CS 3B', 'CS HOME', 'CMS 3B', 'CMS HOME']
double_play_obc = [1, 4, 5, 7]
triple_play_obc = [4, 7]
double_play_results = ['RGO', 'LGO', 'BUNT DP']
triple_play_results = ['RGO', 'LGO']


def calculate_diff(pitch, swing):
    diff = abs(swing - pitch)
    if diff > 500:
        if swing > 500:
            return abs(1000 - swing + pitch)
        else:
            return abs(1000 - pitch + swing)
    return diff


def calculate_ranges(pitching_ranges, batting_ranges, hand_bonus_ranges, park_ranges, infield_in_ranges):
    range_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    stacked_ranges = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    index = 0
    offset = 0
    total = 0

    # Base Match-up
    for i in range(len(range_totals)):
        range_totals[i] = pitching_ranges[i] + batting_ranges[i] + hand_bonus_ranges[i]

    # Park Factors
    neutral_ranges = range_totals.copy()
    for i in range(len(park_ranges)):
        range_totals[i] = round(float(range_totals[i] * park_ranges[i]))
        offset += range_totals[i] - neutral_ranges[i]
    while offset != 0:
        if offset > 0:
            range_totals[index + 5] = range_totals[index + 5] - 1
            offset -= 1
        elif offset < 0:
            range_totals[index + 5] = range_totals[index + 5] + 1
            offset += 1
        index += 1
        if index >= 5:
            index = 0

    park_ranges = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(range_totals)):
        park_ranges[i] = range_totals[i] - neutral_ranges[i]

    # Add Infield In
    for i in range(len(range_totals)):
        range_totals[i] += infield_in_ranges[i]

    # Stack the ranges
    for i in range(len(range_totals)):
        stacked_ranges[i] = '%s - %s' % (total, total+range_totals[i]-1)
        total += range_totals[i]

    return park_ranges, range_totals, stacked_ranges


def calculate_result(ranges, diff):
    result_types = ['HR', '3B', '2B', '1B', 'BB', 'FO', 'K', 'PO', 'RGO', 'LGO']
    total = 0
    for i in range(len(ranges)):
        total += ranges[i]
        if diff <= total:
            return result_types[i]
    return


def calculate_hitting_stats(plate_appearances):
    if not plate_appearances:
        return None
    season = 0
    hits = 0
    walks = 0
    pas = 0
    at_bats = 0
    runs = 0
    rbi = 0
    hrs = 0
    sb = 0
    sa = 0
    total_bases = 0
    total_diff = 0
    for pa in plate_appearances:
        if pa.exactResult:
            result = pa.exactResult.upper()
        elif pa.oldResult:
            result = pa.oldResult.upper()
        else:
            continue
        if result in hit_types:
            hits += 1
            if result == 'HR':
                hrs += 1
                total_bases += 4
            if result == '3B':
                total_bases += 3
            if result == '2B':
                total_bases += 2
            if result == '1B':
                total_bases += 1
        if result == 'BB':
            walks += 1
        if result in steal_types:
            sb += 1
        if result in steal_attempt_types:
            sa += 1
        if result not in not_pa_types:
            pas += 1
            if pa.diff:
                total_diff += pa.diff
        if result not in not_ab_types:
            at_bats += 1
        if pa.rbi:
            rbi += pa.rbi
        if pa.run:
            runs += 1
        season = pa.season
    if at_bats > 0:
        ba = hits / at_bats
        slg = total_bases / at_bats
    else:
        ba = 0.0
        slg = 0.0
    if pas > 0:
        obc = (hits + walks) / pas
        dpa = total_diff / pas
    else:
        obc = 0.0
        dpa = 500.0
    ops = obc + slg
    stats = {'season': season,
             'avg': round(ba, 3),
             'obp': round(obc, 3),
             'slg': round(slg, 3),
             'ops': round(ops, 3),
             'dpa': round(dpa, 3),
             'runs': runs,
             'rbi': rbi,
             'hrs': hrs,
             'hits': hits,
             'sa': sa,
             'sb': sb,
             'pa': pas,
             'ab': at_bats
             }
    return stats


def calculate_pitching_stats(plate_appearances):
    if not plate_appearances:
        return None
    total_outs = 0
    total_runs = 0
    total_diff = 0
    hits = 0
    walks = 0
    flyouts = 0
    strikeouts = 0
    double_plays = 0
    double_play_opps = 0
    bf = 0
    sa = 0
    cs = 0
    for pa in plate_appearances:
        if pa.exactResult:
            result = pa.exactResult.upper()
        elif pa.oldResult:
            result = pa.oldResult.upper()
        else:
            continue
        if result in out_types:
            if pa.outs == 0 and pa.obc in triple_play_obc:
                double_play_opps += 1
                if result in triple_play_results and pa.diff >= 496:
                    total_outs += 3
                    double_plays += 1
            elif pa.outs < 2 and pa.obc in double_play_obc:
                double_play_opps += 1
                if result in double_play_results:
                    total_outs += 2
                    double_plays += 1
            elif result in out_types:
                total_outs += 1
        if result in steal_attempt_types:
            sa += 1
        if result in caught_stealing_types:
            cs += 1
        if result in hit_types:
            hits += 1
        if result == 'BB' or result == 'AUTO BB':
            walks += 1
        if result == 'FO' or result == 'SAC':
            flyouts += 1
        if result == 'K' or result == 'BUNT K':
            strikeouts += 1
        if result not in not_pa_types:
            bf += 1
            if pa.diff:
                total_diff += pa.diff
        if pa.run:
            total_runs += 1
        season = pa.season
    ip_string = '%s.%s' % (math.floor(total_outs / 3), total_outs % 3)
    ip_float = total_outs / 3
    if ip_float > 0:
        era = 6 * (total_runs / ip_float)
        whip = (walks + hits) / ip_float
    else:
        era = 0.0
        whip = 0.0
    if bf > 0:
        dbf = total_diff / bf
    else:
        dbf = 0.0
    if sa > 0:
        cs_pct = cs / sa
    else:
        cs_pct = 0.0
    if double_play_opps > 0:
        dp_pct = double_plays / double_play_opps
    else:
        dp_pct = 0.0
    return {
        'season': season,
        'ip': ip_string,
        'era': round(era, 3),
        'whip': round(whip, 3),
        'hits': hits,
        'flyouts': flyouts,
        'strikeouts': strikeouts,
        'dp': double_plays,
        'dp_pct': round(dp_pct, 3),
        'cs': cs,
        'cs_pct': round(cs_pct, 3),
        'runs': total_runs,
        'bf': bf,
        'dbf': round(dbf, 3)
    }
