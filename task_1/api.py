

from flask import Flask, jsonify
from flask_restx import Api, Resource, fields
from pnl_calculations import compute_pnl
from datetime import datetime
from DB import load_data_as_dataframe

# Initialize Flask app
app = Flask(__name__)
api = Api(app, version='1.0', title='Energy Trading API', description='Energy Trading PnL API')

# Define Swagger model for PnL response
pnl_model = api.model('PnLResponse', {
    'strategy': fields.String(required=True, description='The strategy ID'),
    'value': fields.Float(required=True, description='The calculated PnL value'),
    'unit': fields.String(required=True, description='The unit of value', example='euro'),
    'capture_time': fields.String(required=True, description='Timestamp of the calculation', example='2023-01-16T08:15:46Z')
})

# Define PnL resource
@api.route('/pnl/<string:strategy_id>')
class PnL(Resource):
    @api.doc(description="Returns the PnL of the given strategy")
    @api.marshal_with(pnl_model)  # Serialize the response using the defined model
    def get(self, strategy_id):
        """
        Get the PnL for a specific strategy.
        """
        df = load_data_as_dataframe()
        pnl_value = compute_pnl(strategy_id, df)
        
        if pnl_value == 0.0:
            return {"strategy": strategy_id, "value": pnl_value, "unit": "euro", "capture_time": datetime.utcnow().isoformat()}

        return {"strategy": strategy_id, "value": pnl_value, "unit": "euro", "capture_time": datetime.utcnow().isoformat()}

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
