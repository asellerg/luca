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
import httplib2
import webapp2
from oauth2client.client import GoogleCredentials
from twilio import twiml

class MainHandler(webapp2.RequestHandler):
    def post(self):
        creds = GoogleCredentials.from_stream('client_secrets.json')
        http = creds.authorize(httplib2.Http())
        creds.refresh(http)
        r = twiml.Response()
        r.message(self.request.params.get('Body', None))
        self.response.headers['Content-Type'] = 'text/xml'
        self.response.write(str(r))

app = webapp2.WSGIApplication([('/', MainHandler)],
                              debug=True)
