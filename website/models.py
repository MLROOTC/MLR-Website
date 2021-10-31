from . import db


class BattingTypes(db.Model):
    __tablename__ = 'battingTypes'
    type = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    rangeHR = db.Column(db.Integer)
    range3B = db.Column(db.Integer)
    range2B = db.Column(db.Integer)
    range1B = db.Column(db.Integer)
    rangeBB = db.Column(db.Integer)
    rangeFO = db.Column(db.Integer)
    rangeK = db.Column(db.Integer)
    rangePO = db.Column(db.Integer)
    rangeRGO = db.Column(db.Integer)
    rangeLGO = db.Column(db.Integer)


class GameData(db.Model):
    __tablename__ = 'gameData'
    league = db.Column(db.String(255))
    season = db.Column(db.Integer)
    session = db.Column(db.Integer)
    gameID = db.Column(db.Integer)
    sheetID = db.Column(db.String(255), primary_key=True)
    threadURL = db.Column(db.String(255))
    umpires = db.Column(db.String(255))
    awayTeam = db.Column(db.String(255))
    homeTeam = db.Column(db.String(255))
    awayScore = db.Column(db.Integer)
    homeScore = db.Column(db.Integer)
    inning = db.Column(db.String(255))
    outs = db.Column(db.Integer)
    obc = db.Column(db.Integer)
    complete = db.Column(db.Boolean)
    winningPitcher = db.Column(db.Integer)
    losingPitcher = db.Column(db.Integer)
    save = db.Column(db.Integer)
    potg = db.Column(db.Integer)


class HandBonus(db.Model):
    __tablename__ = 'handBonuses'
    type = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    rangeHR = db.Column(db.Integer)
    range3B = db.Column(db.Integer)
    range2B = db.Column(db.Integer)
    range1B = db.Column(db.Integer)
    rangeBB = db.Column(db.Integer)
    rangeFO = db.Column(db.Integer)
    rangeK = db.Column(db.Integer)
    rangePO = db.Column(db.Integer)
    rangeRGO = db.Column(db.Integer)
    rangeLGO = db.Column(db.Integer)


class Parks(db.Model):
    __tablename__ = 'parkFactors'
    team = db.Column(db.String(3), primary_key=True)
    parkName = db.Column(db.String(255))
    rangeHR = db.Column(db.Float)
    range3B = db.Column(db.Float)
    range2B = db.Column(db.Float)
    range1B = db.Column(db.Float)
    rangeBB = db.Column(db.Float)


class PitchingTypes(db.Model):
    __tablename__ = 'pitchingTypes'
    type = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    rangeHR = db.Column(db.Integer)
    range3B = db.Column(db.Integer)
    range2B = db.Column(db.Integer)
    range1B = db.Column(db.Integer)
    rangeBB = db.Column(db.Integer)
    rangeFO = db.Column(db.Integer)
    rangeK = db.Column(db.Integer)
    rangePO = db.Column(db.Integer)
    rangeRGO = db.Column(db.Integer)
    rangeLGO = db.Column(db.Integer)


class PlateAppearance(db.Model):
    __tablename__ = 'PALogs'
    paID = db.Column(db.Integer, primary_key=True)
    league = db.Column(db.String(255))
    season = db.Column(db.Integer)
    session = db.Column(db.Integer)
    gameID = db.Column(db.Integer)
    inning = db.Column(db.String(255))
    inningID = db.Column(db.Integer)
    playNumber = db.Column(db.Integer)
    outs = db.Column(db.Integer)
    obc = db.Column(db.Integer)
    awayScore = db.Column(db.Integer)
    homeScore = db.Column(db.Integer)
    pitcherTeam = db.Column(db.String(255))
    pitcherName = db.Column(db.String(255))
    pitcherID = db.Column(db.Integer)
    hitterTeam = db.Column(db.String(255))
    hitterName = db.Column(db.String(255))
    hitterID = db.Column(db.Integer)
    pitch = db.Column(db.Integer)
    swing = db.Column(db.Integer)
    diff = db.Column(db.Integer)
    exactResult = db.Column(db.String(255))
    oldResult = db.Column(db.String(255))
    resultAtNeutral = db.Column(db.String(255))
    resultAllNeutral = db.Column(db.String(255))
    rbi = db.Column(db.Integer)
    run = db.Column(db.Boolean)
    batterWPA = db.Column(db.String(255))
    pitcherWPA = db.Column(db.String(255))
    pr3B = db.Column(db.Integer)
    pr2B = db.Column(db.Integer)
    pr1B = db.Column(db.Integer)
    prAB = db.Column(db.Integer)


class Player(db.Model):
    __tablename__ = 'playerData'
    playerID = db.Column(db.Integer, primary_key=True)
    playerName = db.Column(db.String(255))
    Team = db.Column(db.String(4))
    batType = db.Column(db.String(2))
    pitchType = db.Column(db.String(2))
    pitchBonus = db.Column(db.String(1))
    hand = db.Column(db.String(5))
    priPos = db.Column(db.String(2))
    secPos = db.Column(db.String(2))
    tertPos = db.Column(db.String(2))
    redditName = db.Column(db.String(255))
    discordName = db.Column(db.String(255))
    discordID = db.Column(db.Integer)
    status = db.Column(db.Integer)
    posValue = db.Column(db.Integer)


class SeasonData(db.Model):
    __tablename__ = 'seasonData'
    league = db.Column(db.String(255), primary_key=True)
    season = db.Column(db.Integer)
    session = db.Column(db.Integer)


class TeamData(db.Model):
    __tablename__ = 'teamData'
    name = db.Column(db.String(255))
    abb = db.Column(db.String(3), primary_key=True)
    color = db.Column(db.String(6))
    logo_url = db.Column(db.String(1000))
    webhook_url = db.Column(db.String(1000))
    league = db.Column(db.String(4))
    division = db.Column(db.String(255))
    gm = db.Column(db.Integer)
    cogm = db.Column(db.Integer)
    captain1 = db.Column(db.Integer)
    captain2 = db.Column(db.Integer)
    captain3 = db.Column(db.Integer)
    awards1 = db.Column(db.Integer)
    awards2 = db.Column(db.Integer)
    committee1 = db.Column(db.Integer)
    committee2 = db.Column(db.Integer)
    affiliate = db.Column(db.String(255))
