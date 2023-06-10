from boto3 import client
from datetime import datetime
import os

class DynamoDBWrapper:
  def __init__(self, table_name=os.getenv("TABLE_NAME")):
    self.table_name = table_name
    self.client = client('dynamodb')

  def record_post_to_table(self, file_id: int, title: str) -> None:
    """
    Returns:
        None
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    self.client.put_item(
      TableName=self.table_name,
      Item={
        "file_id": { 'S': str(file_id) },
        "title": { 'S': title },
        "posted_at": { 'S': formatted_time }
      }
    )

  def is_already_posted(self, file_id: int) -> bool:
    """
    Returns:
        bool
    """
    response = self.client.get_item(
      TableName=self.table_name,
      Key={
        'file_id': {
          'S': str(file_id),
        }
      }
    )

    # If there is a matching item, this field is present.
    # If there is no matching item, this field is absent.
    return 'Item' in response;
