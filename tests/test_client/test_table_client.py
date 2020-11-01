import pytest
from quickbase_client.client import request_factory
from quickbase_client.client.table_client import QuickBaseTableClient


class TestQuickBaseTableClient(object):

    @pytest.mark.parametrize('http_method,url,cls_method,kwargs', [
        ('GET', '/apps/abcdefg', 'get_app', {}),
        ('GET', '/tables?appId=abcdefg', 'get_tables_for_app', {}),
        ('GET', '/tables/aaaaaa?appId=abcdefg', 'get_table', {}),
        ('GET', '/fields?tableId=aaaaaa', 'get_fields_for_table', {}),
        ('GET', '/fields/6?tableId=aaaaaa', 'get_field', {'field': 6}),
        ('GET', '/reports?tableId=aaaaaa', 'get_reports_for_table', {}),
        ('GET', '/reports/1?tableId=aaaaaa', 'get_report', {'report': 1}),
        ('POST', '/reports/1/run?tableId=aaaaaa', 'run_report', {'report': 1}),
    ])
    def test_makes_api_request_to_correct_url(
            self, requests_mock, debugs_table, http_method, url, cls_method, kwargs):
        client = QuickBaseTableClient(debugs_table, user_token='doesnotmatter')
        mock_json = {'foo': 'bar'}
        requests_mock.request(http_method, f'https://api.quickbase.com/v1{url}', json=mock_json)
        resp = getattr(client, cls_method)(**kwargs)
        assert resp.ok
        assert resp.json() == mock_json

    @pytest.mark.parametrize('header,val', [
        ('Content-Type', 'application/json'),
        ('Authorization', 'QB-USER-TOKEN myusertoken'),
        ('QB-Realm-Hostname', 'dicorp.quickbase.com')])
    def test_request_includes_proper_headers(self, monkeypatch, debugs_table, header, val):
        client = QuickBaseTableClient(debugs_table, user_token='myusertoken')
        monkeypatch.setattr(request_factory.requests, 'request',
                            lambda *args_, **kwargs_: (args_, kwargs_))
        args, kwargs = client.get_table()
        headers = kwargs['headers']
        assert header in headers
        assert headers[header] == val
