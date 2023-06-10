### Virtualenv install
```bash
  python -m pip install --user virtualenv
  python -m venv .venv
  source ./.venv/bin/activate
```
### serverless install
```bash
  npm install -g serverless
```
### Configuring AWS Credentials
See [AWS Docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for details

### Deploying
```bash
  aws configure --profile $PROFILE_IN_CREDENTIALS_FILE
  export ACCOUNT_ID=$ACCOUNT_ID_TO_DEPLOY_TO
  serverless deploy
```
