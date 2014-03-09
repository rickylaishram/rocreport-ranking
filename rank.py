#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb, datetime, math
import score, config

class Database(object):
	def __init__(self):
		super(Database, self).__init__()
		self.db = MySQLdb.connect(host=config.DB.host, user=config.DB.user, passwd=config.DB.password, db=config.DB.db)
		self.cur = self.db.cursor(MySQLdb.cursors.DictCursor)
		self.now = datetime.datetime.now


	def updateRanks(self):
		#self.cur.execute('''SELECT report.report_id, report.added_at, COUNT(DISTINCT vote.report_id) AS vote_count, COUNT(DISTINCT inform.report_id) AS inform_count FROM report LEFT JOIN vote ON vote.report_id = report.report_id LEFT JOIN inform On inform.report_id = report.report_id WHERE report.closed <> 1 GROUP BY report.report_id''')
		self.cur.execute('SELECT * FROM '+ config.DB.table_report +' WHERE closed <> 1')

		scores = []

		for x in xrange(0, self.cur.rowcount):
			row = self.cur.fetchone()
			s = score.Score(self.now, row)
			points = s.calculate()

			scores.append({'report_id': row['report_id'], 'score': points})
		return scores

	def saveRanks(self, scores):
		for item in scores:
			self.cur.execute('UPDATE '+config.DB.table_report+' SET score = %s WHERE report_id = %s', (item['score'], int(item['report_id'])))
		self.db.commit()
		self.db.close()

if __name__ == '__main__':
	d = Database();
	scores = d.updateRanks();
	d.saveRanks(scores)
	#print scores



