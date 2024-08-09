from boto3 import dynamodb
from datetime import datetime
from boto3.dynamodb.conditions import Key
import os

class DynamoDBWrapper:
  def __init__(self, table_name=os.getenv('TABLE_NAME')):
    self.table_name = table_name
    self.table = dynamodb.Table(table_name)

  def record_post_to_table(self, file_id: int, title: str) -> None:
    '''
    Returns:
        None
    '''
    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    self.table.put_item(
      Item={
        'file_id': str(file_id),
        'title': title,
        'posted_at': formatted_time
      }
    )

  def is_already_posted(self, file_id: int) -> bool:
    '''
    Returns:
        bool
    '''
    response = self.table.query(KeyConditionExpression=Key('file_id').eq(file_id))

    return len(response['Items']) != 0
