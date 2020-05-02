import connexion
from connexion.resolver import RestyResolver
import logging

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('api_v1.yaml', base_path='/v1', resolver=RestyResolver('controller.v1'))

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S',
                        level=logging.INFO)
    app.secret_key = 'my_super_secret_key'
    app.debug = True
    app.run(port=8080)
