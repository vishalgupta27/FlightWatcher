from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app import  app

#
# class FlightDetails(db.Model):
#     __tablename__ = "flight_details"
#     id = db.Column(db.Integer, primary_key=True)
#     flightName = db.Column(db.String(100))
#     airlineName = db.Column(db.String(100))
#     arrivalTime = db.Column(db.DateTime, default=False)
#     departureTime = db.Column(db.DateTime, default=False)
#     status = db.Column(db.String(100))
#     futurePrediction = db.Column(db.String(100))
#     isWatchlist = db.Column(db.Boolean, default=False)
#     watchlist = db.relationship("Watchlist", back_populates="flight_details")
#
#     def __init__(self, flightName, airlineName, arrivalTime, departureTime, status, futurePrediction,
#                  isWatchlist=False):
#         self.flightName = flightName
#         self.airlineName = airlineName
#         self.arrivalTime = arrivalTime
#         self.departureTime = departureTime
#         self.status = status
#         self.futurePrediction = futurePrediction
#         self.isWatchlist = isWatchlist
#
#
# class Watchlist(db.Model):
#     __tablename__ = "watchlist"
#     id = db.Column(db.Integer, primary_key=True)
#
#     flightDetailsId = db.Column(db.Integer, ForeignKey('flight_details.id'))
#     flight_details = relationship('FlightDetails', back_populates='watchlist')

# with app.app_context():
#     db.create_all()
