# -*- coding: utf-8 -*-
import MySQLdb, datetime, math
import config

class Score(object):
	
	def __init__(self, now, row):
		super(Score, self).__init__()
		self.now = now
		self.row = row

	def grow(self, days):
		return math.log(days)

	def decay(self, days):
		exponent = -1 * (days/config.Scoring.half_life)
		return math.pow(2, exponent)/2

	def vote(self):
		db = MySQLdb.connect(host=config.DB.host, user=config.DB.user, passwd=config.DB.password, db=config.DB.db)
		cur = db.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM '+ config.DB.table_vote +' WHERE report_id = %s', self.row['report_id'])

		vote_score = 0

		for x in xrange(0, cur.rowcount):
			row = self.cur.fetchone()
			days = (self.now() - row['added_at']).days
			vote_score += self.decay(days)

		return vote_score

	def inform(self):
		db = MySQLdb.connect(host=config.DB.host, user=config.DB.user, passwd=config.DB.password, db=config.DB.db)
		cur = db.cursor(MySQLdb.cursors.DictCursor)
		cur.execute('SELECT * FROM '+ config.DB.table_inform +' WHERE report_id = %s', self.row['report_id'])

		inform_score = 0

		for x in xrange(0, cur.rowcount):
			row = self.cur.fetchone()
			days = (self.now() - row['added_at']).days
			inform_score += self.decay(days)

		return inform_score

	def day(self):
		days = (self.now() - self.row['added_at']).days + 1
		return self.grow(days)

	def calculate(self):

		score = config.Scoring.day*self.day() + config.Scoring.vote*self.vote() + config.Scoring.inform*self.inform()

		return score