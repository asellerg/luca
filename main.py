#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os

import httplib2
from twilio import twiml
import webapp2
import apiclient
import oauth2client

SPREADSHEET_ID = '1-q5cnvS4dSZ8_IuFS9rx097GKF4NsBb5YxBpJqa9c9I'
DISCOVERY_URL = 'https://sheets.googleapis.com/$discovery/rest?version=v4'


class MainHandler(webapp2.RequestHandler):
    def post(self):
        creds = oauth2client.client.GoogleCredentials.from_stream(
            os.path.join(os.path.dirname(__file__), 'client_secrets.json'))
        http = creds.authorize(httplib2.Http())
        creds.refresh(http)
        service = apiclient.discovery.build('sheets', 'v4', http=http,
                                            discoveryServiceUrl=DISCOVERY_URL)
        r = twiml.Response()
        self.response.headers['Content-Type'] = 'text/xml'

        # Bail out if number is unauthorized.
        with open('whitelist.txt') as f:
            whitelist = f.read().splitlines()
            if self.request.params.get('From', None) not in whitelist:
                r.message('Unauthorized number.')
                self.response.write(str(r))
                return

        # Parse the text message.
        body = self.request.params.get('Body', None)
        if body is not None:
            result = service.spreadsheets().values().append(
                     spreadsheetId=SPREADSHEET_ID, range='A5',
                     insertDataOption='OVERWRITE',
                     valueInputOption='USER_ENTERED',
                     body={
                         'range': 'A5',
                         'majorDimension': 'ROWS',
                         'values': [
                             body.split(','),
                         ],
                     }).execute()
            updates = result.get('updates', [])
            r.message(str(updates))
            self.response.write(str(r))

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
