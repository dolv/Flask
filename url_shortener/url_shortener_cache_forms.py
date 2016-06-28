from __init__ import app
from flask_testing import TestCase
class url_shortener_cache_Test(TestCase):
    def create_app(self):
        app.config.from_object('settings_for_testing')
        return app

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        self.app.testing = True


    def test_index_get(self):
        from flask import template_rendered
        from contextlib import contextmanager

        @contextmanager
        def captured_templates(app):
            recorded = []

            def record(sender, template, context, **extra):
                recorded.append((template, context))

            template_rendered.connect(record, app)
            try:
                yield recorded
            finally:
                template_rendered.disconnect(record, app)

        with captured_templates(app) as templates:
            rv = self.app.get('/')
            self.assertEqual(rv.status_code, 200)
            assert len(templates) == 1
            template, context = templates[0]
            assert template.name == 'index.html'

    def test_index_post(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

        response = self.app.post('/',
                                 data=dict(
                                     url='http://example.com/',
                                     follow_redirects=True)
                                 )
        self.assertEqual(response.status_code, 200)


        response = self.app.post('/',
                                 data={'url': 'mailto:admin@google.com'})
        self.assertEqual(response.status_code, 200)
        #self.assertContains(response, 'http')
        assert b'http' in response.data
        #self.assertContains(response, 'https')
        assert b'https' in response.data
        #self.assertContains(response, 'ftp')
        assert b'ftp' in response.data

    def test_redirect(self):
        response = self.app.get('/randomnonsense/')
        self.assertRedirects(response, '/')

if __name__ == "__main__":
    app.run()
