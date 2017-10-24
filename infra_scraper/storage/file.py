
from .base import BaseStorage
import os
import glob
import yaml
import logging

logger = logging.getLogger(__name__)


class FileStorage(BaseStorage):

    def __init__(self, **kwargs):
        super(FileStorage, self).__init__(**kwargs)
        self.storage_dir = kwargs.get('storage_dir', '/tmp/scraper')
        try:
            os.stat(self.storage_dir)
        except Exception:
            os.mkdir(self.storage_dir)

    def _storage_dir_exist(self, name):
        try:
            os.stat(self._get_storage_dir(name))
        except Exception:
            os.mkdir(self._get_storage_dir(name))

    def _get_storage_dir(self, name):
        return os.path.join(self.storage_dir, name)

    def _get_last_timestamp(self, name):
        sinks = glob.glob('{}/*.yaml'.format(self._get_storage_dir(name)))
        last_sink = max(sinks, key=os.path.getctime)
        return last_sink.split('/')[-1].replace('.yaml', '')

    def save_data(self, name, data):
        self._storage_dir_exist(name)
        filename = '{}/{}.yaml'.format(self._get_storage_dir(name),
                                       data['timestamp'])
        with open(filename, 'w') as outfile:
            yaml.safe_dump(data, outfile, default_flow_style=False)
        self.last_timestamp = data['timestamp']

    def load_data(self, name):
        data = None
        if self.last_timestamp is None:
            self.last_timestamp = self._get_last_timestamp(name)
        filename = '{}/{}.yaml'.format(self._get_storage_dir(name),
                                       self.last_timestamp)
        with open(filename, 'r') as stream:
            try:
                data = yaml.load(stream)
            except yaml.YAMLError as exception:
                logger.error(exception)
        return data
