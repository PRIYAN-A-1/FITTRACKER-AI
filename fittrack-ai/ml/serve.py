"""Module-safe entry point; run from repository root: python -m ml.serve."""
import os
from ml.service import Runtime,server
if __name__=='__main__':
 runtime=Runtime(os.getenv('MODEL_DIR','ml/models/food101'));http=server(os.getenv('MODEL_HOST','127.0.0.1'),int(os.getenv('MODEL_PORT','8090')),os.environ.get('MODEL_SERVICE_TOKEN',''),runtime);http.serve_forever()
