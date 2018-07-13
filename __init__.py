# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import urllib2
import random
import string
import boto
import boto.s3.connection
from boto.s3.key import Key

class KronosDataCollector(octoprint.plugin.SettingsPlugin,
                             octoprint.plugin.EventHandlerPlugin,
                             octoprint.plugin.TemplatePlugin,
                             octoprint.plugin.RestartNeedingPlugin):

    def get_settings_defaults(self):
        return dict(enabled=True)

    def get_template_configs(self):
        return [
            dict(type='settings', custom_bindings=False, template='fail_data_template.jinja2')
        ]
	def get_update_information(self):
        return dict(
            kronos_data_collector=dict(
                displayName="Kronos Data Collector",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="MrBreadWater",
                repo="project-kronos-data-collector",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/MrBreadWater/project-kronos-data-collector/archive/{target_version}.zip"
            )
        )
		
    @property
    def enablePlugin(self):
        return self._settings.get_boolean(['enablePlugin'])

    def on_event(self, event, payload):
        from octoprint.events import Events
        if event == Events.MOVIE_DONE:
            self.upload_timelapse(payload)
		if event == Events.PRINT_CANCELLED
			self.upload_picture()
	def upload_picture(self):
		if enablePlugin():
			random_filename = str(''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(32)])) + 'jpg'
			urllib.urlretrieve ("http://localhost:8080/?action=snapshot", random_filename)
			self._logger.info('Uploading image to S3 Sever...')
			upload_file(random_filename, random_filename, pic = True)
			os.remove(random_filename)
    def upload_timelapse(self, payload):
		if enablePlugin():
			path = payload['movie']
			file_name = payload['movie_basename']
			upload_file(path, file_name, pic = False)
		   
			#if delete:
            #import os
            #self._logger.info('Deleting %s from local disk...' % file_name)
            #os.remove(path)
            #self._logger.info('Deleted %s from local disk.' % file_name)


	def upload_file(file, filename, pic = True)
		
		self._logger.info('Uploading %s to S3 Server...' % file_name)
		if pic = False:	
			try:

				conn = boto.s3.connect_to_region('us-west-1',
				aws_access_key_id = 'AKIAJJ4BJOQSV5MGQHIQ',
				aws_secret_access_key = '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',
				# host = 's3-website-us-east-1.amazonaws.com',
				# is_secure=True,               # uncomment if you are not using ssl
				calling_format = boto.s3.connection.OrdinaryCallingFormat(),
				)

				bucket = conn.get_bucket('3dprintdetectionuploads')
				key_name = filename + '.mpg'
				UpPath = 'prints/' #Directory Under which file should get upload
				full_key_name = os.path.join(UpPath, key_name)
				k = bucket.new_key(full_key_name)
				k.set_contents_from_filename(file)
				self._logger.info('Uploaded %s to S3 Server!' % file_name)
			except Exception as e: 
				self._logger.info(str(e))
				self._logger.info("error")
		elif pic = True:
			try:

				conn = boto.s3.connect_to_region('us-west-1',
				aws_access_key_id = 'AKIAJJ4BJOQSV5MGQHIQ',
				aws_secret_access_key = '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',
				# host = 's3-website-us-east-1.amazonaws.com',
				# is_secure=True,               # uncomment if you are not using ssl
				calling_format = boto.s3.connection.OrdinaryCallingFormat(),
				)

				bucket = conn.get_bucket('3dprintdetectionuploads')
				key_name = filename + '.jpg'
				UpPath = 'print_pics/' #Directory Under which file should get upload
				full_key_name = os.path.join(UpPath, key_name)
				k = bucket.new_key(full_key_name)
				k.set_contents_from_filename(key_name)
				self._logger.info('Uploaded %s to S3 Server!' % file_name)
			except Exception as e: 
				self._logger.info(str(e))
				self._logger.info("error")
			
__plugin_name__ = "Kronos Data Collector"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = KronosDataCollector()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
