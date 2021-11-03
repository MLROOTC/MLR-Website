from flask_restful import Resource, fields, marshal_with
from .models import PlateAppearance, Player, GameData

pa_resource_fields = {
    'paID': fields.Integer,
    'league': fields.String,
    'season': fields.Integer,
    'session': fields.Integer,
    'gameID': fields.Integer,
    'inning': fields.String,
    'inningID': fields.Integer,
    'playNumber': fields.Integer,
    'outs': fields.Integer,
    'obc': fields.Integer,
    'awayScore': fields.Integer,
    'homeScore': fields.Integer,
    'pitcherTeam': fields.String,
    'pitcherName': fields.String,
    'pitcherID': fields.Integer,
    'hitterTeam': fields.String,
    'hitterName': fields.String,
    'hitterID': fields.Integer,
    'pitch': fields.Integer,
    'swing': fields.Integer,
    'diff': fields.Integer,
    'exactResult': fields.String,
    'oldResult': fields.String,
    'resultAtNeutral': fields.String,
    'resultAllNeutral': fields.String,
    'rbi': fields.Integer,
    'run': fields.Boolean,
    'batterWPA': fields.String,
    'pitcherWPA': fields.String,
    'pr3B': fields.Integer,
    'pr2B': fields.Integer,
    'pr1B': fields.Integer,
    'prAB': fields.Integer
}
player_resource_fields = {
    'playerID': fields.Integer,
    'playerName': fields.String,
    'Team': fields.String,
    'batType': fields.String,
    'pitchType': fields.String,
    'pitchBonus': fields.String,
    'hand': fields.String,
    'priPos': fields.String,
    'secPos': fields.String,
    'tertPos': fields.String,
    'redditName': fields.String,
    'discordName': fields.String,
    'discordID': fields.Integer,
    'status': fields.Integer,
    'posValue': fields.Integer
}


class PitcherData(Resource):
    @marshal_with(pa_resource_fields)
    def get(self, league, player_id):
        pitch_data = PlateAppearance.query.filter_by(pitcherID=player_id, league=league).all()
        return pitch_data


class HitterData(Resource):
    @marshal_with(pa_resource_fields)
    def get(self, league, player_id):
        pitch_data = PlateAppearance.query.filter_by(hitterID=player_id, league=league).all()
        return pitch_data


class AllPlateAppearances(Resource):
    @marshal_with(pa_resource_fields)
    def get(self):
        return PlateAppearance.query.all()


class PlateAppearnacesByLeague(Resource):
    @marshal_with(pa_resource_fields)
    def get(self, league):
        return PlateAppearance.query.filter_by(league=league).all()


class AllPlayers(Resource):
    @marshal_with(player_resource_fields)
    def get(self):
        return Player.query.all()


class PlayerID(Resource):
    @marshal_with(player_resource_fields)
    def get(self, playerID):
        return Player.query.filter_by(playerID=playerID).first()


class PlayerName(Resource):
    @marshal_with(player_resource_fields)
    def get(self, player_name):
        return Player.query.filter_by(playerName=player_name).first()


def add_resources(api):
    api.add_resource(PitcherData, '/api/plateappearances/pitching/<string:league>/<int:player_id>')
    api.add_resource(HitterData, '/api/plateappearances/batting/<string:league>/<int:player_id>')
    api.add_resource(AllPlateAppearances, '/api/plateappearances')
    api.add_resource(PlateAppearnacesByLeague, '/api/plateappearances/<string:league>')
    api.add_resource(AllPlayers, '/api/players')
    api.add_resource(PlayerID, '/api/players/id/<int:playerID>')
    api.add_resource(PlayerName, '/api/players/name/<string:player_name>')
