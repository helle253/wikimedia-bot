cd venv/lib/python3.10/site-packages
zip -r9 ${OLDPWD}/lambda.zip .
cd $OLDPWD
zip -g lambda.zip lambda_function.py 
zip -rg lambda.zip ./aws_helpers 
# aws lambda update-function-code --function-name wikimedia-bot --zip-file fileb://lambda.zip
