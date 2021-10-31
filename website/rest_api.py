from flask_restful import Resource, fields, marshal_with
from .models import PlateAppearance


resource_fields = {
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


class PitcherData(Resource):
    @marshal_with(resource_fields)
    def get(self, league, player_id):
        pitch_data = PlateAppearance.query.filter_by(pitcherID=player_id, league=league).all()
        return pitch_data


class HitterData(Resource):
    @marshal_with(resource_fields)
    def get(self, league, player_id):
        pitch_data = PlateAppearance.query.filter_by(hitterID=player_id, league=league).all()
        return pitch_data


def add_resources(api):
    api.add_resource(PitcherData, '/plateappearances/pitching/<string:league>/<int:player_id>')
    api.add_resource(HitterData, '/plateappearances/batting/<string:league>/<int:player_id>')
