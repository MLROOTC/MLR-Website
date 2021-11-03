from flask import Blueprint, render_template, request, flash
from .models import GameData, TeamData, Parks, Player, PlateAppearance, BattingTypes, PitchingTypes, HandBonus, SeasonData
from .calculator import calculate_diff, calculate_ranges, calculate_result, calculate_hitting_stats, calculate_pitching_stats

views = Blueprint('views', __name__)


@views.route('/calculator', methods=["GET", "POST"])
def calculator():
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    player_list = Player.query.order_by(Player.playerName.asc()).all()
    batting_types = BattingTypes.query.order_by(BattingTypes.name.asc()).all()
    pitching_types = PitchingTypes.query.order_by(PitchingTypes.name.asc()).all()
    hand_bonus_list = HandBonus.query.order_by(HandBonus.name.asc()).all()
    park_list = Parks.query.order_by(Parks.team.asc()).all()

    # Initial Values
    result_string = ''
    batting_type = ''
    pitching_type = ''
    hand_bonus = ''
    park_name = ''
    pitcher_placeholder_value = ''
    pitcher_placeholder_name = 'Select Pitcher...'
    batter_placeholder_value = ''
    batter_placeholder_name = 'Select Batter...'
    pitching_type_placeholder_value = ''
    pitching_type_placeholder_name = 'Select Pitching Type...'
    batting_type_placeholder_value = ''
    batting_type_placeholder_name = 'Select Batting Type...'
    park_placeholder_value = ''
    park_placeholder_name = 'Select Park...'
    player_tab_active = ' show active'
    type_tab_active = ''
    player_tab_button_active = ' active'
    type_tab_button_active = ''
    batting_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    pitching_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    hand_bonus_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    park_factor_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    infield_in_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    total_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    stacked_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

    if request.method == "POST":
        data = request.form

        pitcher_id = data['pitcher_name']
        batter_id = data['batter_name']
        pitching_type = data['pitcher_type']
        batting_type = data['batter_type']
        hand_bonus = data['hand_bonus']
        park_name = data['park_name']
        infield_in = data['infield_in']
        pitch = data['pitch_input']
        swing = data['swing_input']

        if pitch and swing:
            if pitch.isnumeric() and swing.isnumeric():
                diff = calculate_diff(int(pitch), int(swing))
                result = calculate_result(total_ranges, diff)
                result_string = 'Swing: %s\nPitch: %s\nDiff: %s -> %s' % (pitch, swing, diff, result)
            else:
                flash('Swing and pitch must be integers', category='error')

        if pitching_type:
            pt = PitchingTypes.query.filter_by(type=pitching_type).first()
            pitching_type_placeholder_value = pitching_type
            pitching_type_placeholder_name = pt.name
            player_tab_active = ''
            type_tab_active = ' show active'
            player_tab_button_active = ''
            type_tab_button_active = 'active'
            pitcher_placeholder_value = ''
            pitcher_placeholder_name = 'Select Pitcher...'
            batter_placeholder_value = ''
            batter_placeholder_name = 'Select Batter...'
            pitcher_id = None
            batter_id = None
        else:
            player_tab_active = ' show active'
            type_tab_active = ''
            player_tab_button_active = 'active'
            type_tab_button_active = ''
            pitching_type_placeholder_value = ''
            pitching_type_placeholder_name = 'Select Pitching Type...'
            batting_type_placeholder_value = ''
            batting_type_placeholder_name = 'Select Batting Type...'

        if batting_type:
            bt = BattingTypes.query.filter_by(type=batting_type).first()
            batting_type_placeholder_value = batting_type
            batting_type_placeholder_name = bt.name

        if pitcher_id:
            pitcher = Player.query.filter_by(playerID=int(pitcher_id)).first()
            pitcher_placeholder_value = pitcher.playerID
            pitcher_placeholder_name = pitcher.playerName
            pitching_type = pitcher.pitchType
            if not pitching_type:
                pitching_type = 'POS'

        if batter_id:
            batter = Player.query.filter_by(playerID=int(batter_id)).first()
            batter_placeholder_value = batter.playerID
            batter_placeholder_name = batter.playerName
            batting_type = batter.batType
            if not batting_type:
                batting_type = 'P'

        if park_name:
            park = Parks.query.filter_by(team=park_name).first()
            park_placeholder_value = park_name
            park_placeholder_name = park.parkName
            park_factor_ranges = (park.rangeHR, park.range3B, park.range2B, park.range1B, park.rangeBB)
            park_name = park.parkName
        else:
            park_factor_ranges = (1.0, 1.0, 1.0, 1.0, 1.0)

        if batter_id and pitcher_id:
            if batter.hand == pitcher.hand:
                hand_bonus = pitcher.pitchBonus
            else:
                hand_bonus = ''

        if pitching_type:
            pitching_type = PitchingTypes.query.filter_by(type=pitching_type).first()
            pitching_ranges = (pitching_type.rangeHR, pitching_type.range3B, pitching_type.range2B, pitching_type.range1B, pitching_type.rangeBB, pitching_type.rangeFO, pitching_type.rangeK, pitching_type.rangePO, pitching_type.rangeRGO, pitching_type.rangeLGO)
            pitching_type = pitching_type.name

        if batting_type:
            batting_type = BattingTypes.query.filter_by(type=batting_type).first()
            batting_ranges = (batting_type.rangeHR, batting_type.range3B, batting_type.range2B, batting_type.range1B, batting_type.rangeBB, batting_type.rangeFO, batting_type.rangeK, batting_type.rangePO, batting_type.rangeRGO, batting_type.rangeLGO)
            batting_type = batting_type.name

        if hand_bonus:
            hand_bonus = HandBonus.query.filter_by(type=hand_bonus).first()
            hand_bonus_ranges = (hand_bonus.rangeHR, hand_bonus.range3B, hand_bonus.range2B, hand_bonus.range1B, hand_bonus.rangeBB, hand_bonus.rangeFO, hand_bonus.rangeK, hand_bonus.rangePO, hand_bonus.rangeRGO, hand_bonus.rangeLGO)
            hand_bonus = hand_bonus.name

        if infield_in == 'true':
            infield_in_ranges = (0, 0, 0, 18, 0, 0, 0, 0, -9, -9)

        park_factor_ranges, total_ranges, stacked_ranges = calculate_ranges(pitching_ranges, batting_ranges, hand_bonus_ranges, park_factor_ranges, infield_in_ranges)

    return render_template('calculator.html',
                           player_tab_active=player_tab_active,
                           type_tab_active=type_tab_active,
                           player_tab_button_active=player_tab_button_active,
                           type_tab_button_active=type_tab_button_active,
                           player_list=player_list,
                           batting_types=batting_types,
                           pitching_types=pitching_types,
                           hand_bonus_list=hand_bonus_list,
                           park_list=park_list,
                           pitcher_placeholder_name=pitcher_placeholder_name,
                           pitcher_placeholder_value=pitcher_placeholder_value,
                           batter_placeholder_name=batter_placeholder_name,
                           batter_placeholder_value=batter_placeholder_value,
                           pitching_type_placeholder_value=pitching_type_placeholder_value,
                           pitching_type_placeholder_name=pitching_type_placeholder_name,
                           batting_type_placeholder_name=batting_type_placeholder_name,
                           batting_type_placeholder_value=batting_type_placeholder_value,
                           park_placeholder_name=park_placeholder_name,
                           park_placeholder_value=park_placeholder_value,
                           batting_type=batting_type,
                           pitching_type=pitching_type,
                           hand_bonus=hand_bonus,
                           park_name=park_name,
                           batting_ranges=batting_ranges,
                           pitching_ranges=pitching_ranges,
                           pitching_bonus_ranges=hand_bonus_ranges,
                           park_factor_ranges=park_factor_ranges,
                           infield_in_ranges=infield_in_ranges,
                           total_ranges=total_ranges,
                           stacked_ranges=stacked_ranges,
                           result_string=result_string)


@views.route('/games')
def games():
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    return render_template('games.html')


@views.route('/')
def home():
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    mlr_season = SeasonData.query.filter_by(league='mlr').first()
    game_data = GameData.query.filter_by(league='mlr', season=mlr_season.season, session=mlr_season.session).all()
    return render_template('home.html', games=game_data)


@views.route('/player/<playerID>')
def player(playerID):
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    session = PlateAppearance.query.session
    season = SeasonData.query.filter_by(league='mlr').first()
    player_data = Player.query.filter_by(playerID=playerID).first()
    bt = BattingTypes.query.filter_by(type=player_data.batType).first()
    pt = PitchingTypes.query.filter_by(type=player_data.pitchType).first()
    pb = HandBonus.query.filter_by(type=player_data.pitchBonus).first()
    team_data = TeamData.query.filter_by(abb=player_data.Team).first()
    mlr_pitching = PlateAppearance.query.filter_by(pitcherID=playerID, league='mlr').all()
    mlr_batting = PlateAppearance.query.filter_by(hitterID=playerID, league='mlr').all()
    milr_pitching = PlateAppearance.query.filter_by(pitcherID=playerID, league='milr').all()
    milr_batting = PlateAppearance.query.filter_by(hitterID=playerID, league='milr').all()

    mlr_batting_seasons = PlateAppearance.query.with_entities(PlateAppearance.season).filter_by(hitterID=playerID, league='mlr').distinct().all()
    mlr_pitching_seasons = PlateAppearance.query.with_entities(PlateAppearance.season).filter_by(pitcherID=playerID, league='mlr').distinct().all()
    milr_batting_seasons = PlateAppearance.query.with_entities(PlateAppearance.season).filter_by(hitterID=playerID, league='milr').distinct().all()
    milr_pitching_seasons = PlateAppearance.query.with_entities(PlateAppearance.season).filter_by(pitcherID=playerID, league='milr').distinct().all()

    mlr_batting_stats = []
    for season in mlr_batting_seasons:
        if len(season) == 1:
            season = season[0]
            plate_appearances = PlateAppearance.query.filter(PlateAppearance.hitterID == playerID,
                                                             PlateAppearance.league == 'mlr',
                                                             PlateAppearance.season == season,
                                                             PlateAppearance.session >= 1,
                                                             PlateAppearance.session <= 16
                                                             ).all()
            season_stats = calculate_hitting_stats(plate_appearances)
            if season_stats:
                mlr_batting_stats.append(season_stats)

    mlr_pitching_stats = []
    for season in mlr_pitching_seasons:
        if len(season) == 1:
            season = season[0]
            plate_appearances = PlateAppearance.query.filter(PlateAppearance.pitcherID == playerID,
                                                             PlateAppearance.league == 'mlr',
                                                             PlateAppearance.season == season,
                                                             PlateAppearance.session >= 1,
                                                             PlateAppearance.session <= 16
                                                             ).all()
            season_stats = calculate_pitching_stats(plate_appearances)
            if season_stats:
                mlr_pitching_stats.append(season_stats)

    milr_batting_stats = []
    for season in milr_batting_seasons:
        if len(season) == 1:
            season = season[0]
            plate_appearances = PlateAppearance.query.filter(PlateAppearance.hitterID == playerID,
                                                             PlateAppearance.league == 'milr',
                                                             PlateAppearance.season == season,
                                                             PlateAppearance.session >= 1,
                                                             PlateAppearance.session <= 14
                                                             ).all()
            season_stats = calculate_hitting_stats(plate_appearances)
            if season_stats:
                milr_batting_stats.append(season_stats)

    milr_pitching_stats = []
    for season in milr_pitching_seasons:
        if len(season) == 1:
            season = season[0]
            plate_appearances = PlateAppearance.query.filter(PlateAppearance.pitcherID == playerID,
                                                             PlateAppearance.league == 'milr',
                                                             PlateAppearance.season == season,
                                                             PlateAppearance.session >= 1,
                                                             PlateAppearance.session <= 14
                                                             ).all()
            season_stats = calculate_pitching_stats(plate_appearances)
            if season_stats:
                milr_pitching_stats.append(season_stats)

    return render_template('player.html', player=player_data, team=team_data, mlr_batting_stats=mlr_batting_stats, milr_batting_stats=milr_batting_stats, mlr_pitching_stats=mlr_pitching_stats, milr_pitching_stats=milr_pitching_stats, mlr_pitching=mlr_pitching, mlr_batting=mlr_batting, milr_pitching=milr_pitching, milr_batting=milr_batting, bt=bt, pt=pt, pb=pb)


@views.route('/players')
def players():
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    player_data = Player.query.order_by(Player.playerID.asc()).all()
    return render_template('players.html', players=player_data)


@views.route('/team/<team_abb>')
def team(team_abb):
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    team_data = TeamData.query.filter_by(abb=team_abb).first()
    park_data = Parks.query.filter_by(team=team_abb).first()
    if team_data.league == 'mlr':
        player_data = Player.query.filter_by(Team=team_abb).order_by(Player.posValue.asc(), Player.playerName.asc()).all()
    else:
        if team_abb == 'FAP':
            player_data = Player.query.filter_by(Team='', status=1).order_by(Player.posValue.asc()).all()
        else:
            mlr_teams = TeamData.query.filter_by(affiliate=team_abb).all()
            player_data = []
            for affiliate in mlr_teams:
                roster = Player.query.filter_by(Team=affiliate.abb).all()
                player_data += roster
            player_data.sort(key=lambda x: x.playerName)

    gm = Player.query.filter_by(playerName=team_data.gm).first()
    cogm = Player.query.filter_by(playerName=team_data.cogm).first()
    captain1 = Player.query.filter_by(playerName=team_data.captain1).first()
    captain2 = Player.query.filter_by(playerName=team_data.captain2).first()
    captain3 = Player.query.filter_by(playerName=team_data.captain3).first()
    committee1 = Player.query.filter_by(playerName=team_data.committee1).first()
    committee2 = Player.query.filter_by(playerName=team_data.committee2).first()
    awards1 = Player.query.filter_by(playerName=team_data.awards1).first()
    awards2 = Player.query.filter_by(playerName=team_data.awards2).first()

    return render_template('team.html', team=team_data, park=park_data, roster=player_data, gm=gm, cogm=cogm, captain1=captain1, captain2=captain2, captain3=captain3, committee1=committee1, committee2=committee2, awards1=awards1, awards2=awards2)


@views.route('/teamcalc', methods=["GET", "POST"])
def team_calc():
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    player_list = Player.query.order_by(Player.playerName.asc()).all()
    team_list = TeamData.query.filter_by(league='mlr').all()
    park_list = Parks.query.all()
    title = ''
    subtitle = ''
    roster_ranges = []
    if request.method == "POST":
        data = request.form

        if data['pitcher']:
            pitcher = Player.query.filter_by(playerID=data['pitcher']).first()
        else:
            flash('Please select a pitcher', category='error')
            return render_template('teamcalc.html', players=player_list, teams=team_list, parks=park_list)
        if data['team']:
            batting_team = TeamData.query.filter_by(abb=data['team']).first()
        else:
            flash('Please select a team', category='error')
            return render_template('teamcalc.html', players=player_list, teams=team_list, parks=park_list)
        if data['park']:
            park = Parks.query.filter_by(team=data['park']).first()
        else:
            flash('Please select a park', category='error')
            return render_template('teamcalc.html', players=player_list, teams=team_list, parks=park_list)

        roster = Player.query.filter_by(Team=batting_team.abb).order_by(Player.posValue).all()
        pitcher_type = pitcher.pitchType

        if pitcher_type:
            pitcher_type = PitchingTypes.query.filter_by(type=pitcher.pitchType).first()
            pitcher_bonus_type = HandBonus.query.filter_by(type=pitcher.pitchBonus).first()
            pitcher_bonus_ranges = (pitcher_bonus_type.rangeHR, pitcher_bonus_type.range3B, pitcher_bonus_type.range2B, pitcher_bonus_type.range1B, pitcher_bonus_type.rangeBB, pitcher_bonus_type.rangeFO,pitcher_bonus_type.rangeK, pitcher_bonus_type.rangePO, pitcher_bonus_type.rangeRGO,pitcher_bonus_type.rangeLGO)
        else:
            pitcher_type = PitchingTypes.query.filter_by(type='POS').first()
            pitcher_bonus_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        pitcher_ranges = (pitcher_type.rangeHR, pitcher_type.range3B, pitcher_type.range2B, pitcher_type.range1B, pitcher_type.rangeBB, pitcher_type.rangeFO, pitcher_type.rangeK, pitcher_type.rangePO, pitcher_type.rangeRGO, pitcher_type.rangeLGO)
        if park:
            park_ranges = (park.rangeHR, park.range3B, park.range2B, park.range1B, park.rangeBB)
        else:
            park_ranges = (1.0, 1.0, 1.0, 1.0, 1.0)
        blank_ranges = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        roster_ranges = []
        title = '%s vs. %s' % (pitcher.playerName, batting_team.name)
        subtitle = '%s | %s - %s' % (pitcher_type.name, park.parkName, park_ranges)
        for batter in roster:
            if batter.priPos == 'P':
                batter_type = BattingTypes.query.filter_by(type='P').first()
            elif batter.batType:
                batter_type = BattingTypes.query.filter_by(type=batter.batType).first()
            else:
                batter_type = BattingTypes.query.filter_by(type='P').first()
            batter_ranges = (batter_type.rangeHR, batter_type.range3B, batter_type.range2B, batter_type.range1B, batter_type.rangeBB, batter_type.rangeFO, batter_type.rangeK, batter_type.rangePO, batter_type.rangeRGO, batter_type.rangeLGO)
            if pitcher.hand == batter.hand:
                data1, range_totals, data3 = calculate_ranges(pitcher_ranges, batter_ranges, pitcher_bonus_ranges, park_ranges, blank_ranges)
            else:
                data1, range_totals, data3 = calculate_ranges(pitcher_ranges, batter_ranges, blank_ranges, park_ranges, blank_ranges)
            total = 0
            stacked_ranges = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            for i in range(len(range_totals)):
                stacked_ranges[i] = (total+range_totals[i]-1)
                total += range_totals[i]
            roster_ranges.append([batter.playerID, batter.playerName, batter.priPos, batter.secPos, batter.tertPos, batter_type.type, batter.hand] + stacked_ranges)
    return render_template('teamcalc.html', players=player_list, teams=team_list, parks=park_list, title=title, subtitle=subtitle, roster_ranges=roster_ranges)


@views.route('/teams')
def teams():
    flash('Note - this website is currently in beta. We will be accepting bug reports and user feedback at a later date.', category='error')
    ale = TeamData.query.filter_by(league='mlr', division='ALE').order_by(TeamData.name.asc()).all()
    alc = TeamData.query.filter_by(league='mlr', division='ALC').order_by(TeamData.name.asc()).all()
    alw = TeamData.query.filter_by(league='mlr', division='ALW').order_by(TeamData.name.asc()).all()
    nle = TeamData.query.filter_by(league='mlr', division='NLE').order_by(TeamData.name.asc()).all()
    nlc = TeamData.query.filter_by(league='mlr', division='NLC').order_by(TeamData.name.asc()).all()
    nlw = TeamData.query.filter_by(league='mlr', division='NLW').order_by(TeamData.name.asc()).all()
    ind = TeamData.query.filter_by(league='milr', division='IND').order_by(TeamData.name.asc()).all()
    dia = TeamData.query.filter_by(league='milr', division='DIA').order_by(TeamData.name.asc()).all()
    twi = TeamData.query.filter_by(league='milr', division='TWI').order_by(TeamData.name.asc()).all()
    wld = TeamData.query.filter_by(league='milr', division='WLD').order_by(TeamData.name.asc()).all()

    return render_template('teams.html', ale=ale, alc=alc, alw=alw, nle=nle, nlc=nlc, nlw=nlw, ind=ind, dia=dia, twi=twi, wld=wld)


@views.route('/api')
def api():
    return render_template('api.html')
