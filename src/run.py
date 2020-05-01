import connexion
from connexion.resolver import RestyResolver

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api_v1.yaml', base_path='/v1', resolver=RestyResolver('controller'))


if __name__ == '__main__':
    app.secret_key = 'my_super_secret_key'
    app.debug = True
    app.run(port=8080)
