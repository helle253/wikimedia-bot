### Configuring AWS Credentials

See [AWS Docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) for details

### DynamoDB

You'll need a dynamoDB table to run this bot - configure it and record the table name in parameter store under `/wikimedia_bot/table_name`

### Parameter Store

The following parameter store keys need to be populated:

- /wikimedia_bot/mastodon/access_key
- /wikimedia_bot/mastodon/base_url
- /wikimedia_bot/twitter/api_key
- /wikimedia_bot/twitter/api_key_secret
- /wikimedia_bot/twitter/access_token
- /wikimedia_bot/twitter/access_token_secret
- /wikimedia_bot/table_name

### Twitter Setup

You'll have to create a Twitter Project and generate API keys and access tokens. See [Twitter Docs](https://developer.twitter.com/en/docs/authentication/oauth-1-0a) for details.

### Mastodon Setup

Create a new Mastodon App, with read/write privileges. See [Mastodon Docs](https://docs.joinmastodon.org/methods/apps/) for details.

### OIDC

To configure automated deployments, you will also need to configure Github secrets for the AWS_DEPLOY_ROLE.

see [Github Docs](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services) for details about setting up your own OIDC.
