#!/usr/bin/env python3

import os
import sys
sys.path.append('..')
import warnings
import unittest
import email_scraper

class TestGetEmail(unittest.TestCase):
	def test_scrape_emails(self):
		'''Verify that lineup emails can be obtained via gmail API'''
		warnings.filterwarnings("ignore", category=ResourceWarning)
		query_string = 'to:baseball.cbssports.com subject:lineup'
		test_emails = email_scraper.scrape_emails(
			query_string,
			'../credentials.json',
			max_results=1
		)
		self.assertTrue(len(test_emails) > 0)
		for email in test_emails:
			self.assertTrue('lineup' in 'lineup')


if __name__ == '__main__':
	unittest.main()