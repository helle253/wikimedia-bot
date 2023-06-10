### Virtualenv install
```bash
  python -m pip install --user virtualenv
  source ./bin/venv/bin/activate
```
### serverless install
```bash
  npm install -g serverless
```
### Configuring AWS Credentials
TODO

### Deploying
```bash
  aws configure --profile $PROFILE_IN_CREDENTIALS_FILE
  export ACCOUNT_ID=$ACCOUNT_ID_TO_DEPLOY_TO
  serverless deploy
```
