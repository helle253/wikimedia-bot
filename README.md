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

### DynamoDB
You'll need a dynamoDB table to run this bot - configure it and record the table name in parameter store under `/wikimedia_bot/table_name`
### Parameter Store
The following parameter store keys need to be populated:
- /wikimedia_bot/mastodon_access_key
- /wikimedia_bot/mastodon_base_url
- /wikimedia_bot/table_name


### Deploying
```bash
  aws configure --profile $PROFILE_IN_CREDENTIALS_FILE
  export ACCOUNT_ID=$ACCOUNT_ID_TO_DEPLOY_TO
  serverless deploy
```
