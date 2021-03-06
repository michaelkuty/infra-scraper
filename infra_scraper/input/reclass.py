# -*- coding: utf-8 -*-

from infra_scraper.input.saltstack import SaltStackInput
from infra_scraper.utils import setup_logger

logger = setup_logger('input.reclass')


class SaltReclassInput(SaltStackInput):

    RESOURCE_MAP = {
        'salt_high_state': {
            'resource': 'high_state',
            'client': '',
            'name': 'High State',
            'icon': 'fa:cube',
        },
        'salt_job': {
            'resource': 'job',
            'client': '',
            'name': 'Job',
            'icon': 'fa:clock-o',
        },
        'salt_node': {
            'resource': 'node',
            'client': '',
            'name': 'Node',
            'icon': 'fa:server',
        },
        'salt_service': {
            'resource': 'service',
            'name': 'Service',
            'icon': 'fa:podcast',
        },
        'salt_user': {
            'resource': 'user',
            'name': 'User',
            'icon': 'fa:user',
        },
    }

    def __init__(self, **kwargs):
        super(SaltReclassInput, self).__init__(**kwargs)
        self.kind = 'reclass'

    def _create_relations(self):
        for resource_id, resource in self.resources.get('salt_job', {}).items():
            for minion_id, result in resource['metadata'].get('Result', {}).items():
                self._scrape_relation(
                    'salt_job-salt_node',
                    resource_id,
                    minion_id)

    def scrape_all_resources(self):
        self.scrape_nodes()
        self.scrape_resources()
        self.scrape_jobs()
#        self.scrape_services()

    def scrape_nodes(self):
        response = self.api.low([{
            'client': 'local',
            'expr_form': 'compound',
            'tgt': 'I@salt:master',
            'fun': 'reclass.inventory'
        }]).get('return')[0]
        for minion_id, minion in response.items():
            for node_id, node in minion.items():
                self._scrape_resource(node_id,
                                      node_id,
                                      'salt_node', None,
                                      metadata=node)

    def scrape_resources(self):
        response = self.api.low([{
            'client': 'local',
            'expr_form': 'compound',
            'tgt': 'I@salt:master',
            'fun': 'reclass.graph_data'
        }]).get('return')[0]
        for minion_id, minion in response.items():
            for service in minion['graph']:
                service_id = '{}|{}'.format(service['host'],
                                            service['service'])
                self._scrape_resource(service_id,
                                      service['service'],
                                      'salt_service', None,
                                      metadata=service)
                self._scrape_relation(
                    'salt_service-salt_host',
                    service_id,
                    service['host'])
                for rel in service['relations']:
                    if rel['host'] not in self.resources['salt_node']:
                        self._scrape_resource(rel['host'],
                                              rel['host'],
                                              'salt_node', None,
                                              metadata={})
                    rel_service_id = '{}|{}'.format(rel['host'],
                                                    rel['service'])
                    if rel_service_id not in self.resources['salt_service']:
                        self._scrape_resource(rel_service_id,
                                              rel['service'],
                                              'salt_service', None,
                                              metadata={})
                        self._scrape_relation(
                            'salt_service-salt_host',
                            rel_service_id,
                            rel['host'])
                    self._scrape_relation(
                        'salt_service-salt_service',
                        service_id,
                        rel_service_id)

    def scrape_jobs(self):
        response = self.api.low([{
            'client': 'runner',
            'fun': 'jobs.list_jobs',
            'arg': "search_function='[\"state.apply\", \"state.sls\"]'"
        }]).get('return')[0]
        for job_id, job in response.items():
            if job['Function'] in ['state.apply', 'state.sls']:
                result = self.api.lookup_jid(job_id).get('return')[0]
                job['Result'] = result
                self._scrape_resource(job_id,
                                      job['Function'],
                                      'salt_job', None, metadata=job)
