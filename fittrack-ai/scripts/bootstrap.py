"""Create local development configuration without overwriting existing secrets."""
from pathlib import Path
import secrets
root=Path(__file__).resolve().parents[1]
def write_once(path,content):
 if path.exists():print('Existing configuration preserved:',path.relative_to(root));return
 path.write_text(content);path.chmod(0o600);print('Created:',path.relative_to(root))
if __name__=='__main__':
 write_once(root/'.env',''.join(f'{key}={secrets.token_urlsafe(48)}\n' for key in ['DATABASE_PASSWORD','JWT_SECRET','MODEL_SERVICE_TOKEN']))
 write_once(root/'apps/android/.env','EXPO_PUBLIC_API_URL=http://10.0.2.2:8080\n')
 print('Next: docker compose up --build -d; then run npm ci and npx expo run:android in apps/android.')
