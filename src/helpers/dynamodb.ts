import {
  DynamoDBClient,
  PutItemCommand,
  GetItemCommand,
} from '@aws-sdk/client-dynamodb';
import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';

export class DynamoDBWrapper {
  private dynamoClient: DynamoDBClient;
  private ssmClient: SSMClient;
  private tableName: string | undefined;

  constructor() {
    this.dynamoClient = new DynamoDBClient({});
    this.ssmClient = new SSMClient({});
  }

  private async getTableName(): Promise<string> {
    if (!this.tableName) {
      const command = new GetParameterCommand({
        Name: '/wikimedia_bot/table_name',
      });
      const response = await this.ssmClient.send(command);
      this.tableName = response.Parameter?.Value;
      if (!this.tableName) throw new Error('table name not found in ssm');
    }
    return this.tableName;
  }

  async recordPostToTable(fileId: number, title: string): Promise<void> {
    const tableName = await this.getTableName();
    const command = new PutItemCommand({
      TableName: tableName,
      Item: {
        file_id: { S: fileId.toString() },
        title: { S: title },
        posted_at: { S: new Date().toISOString() },
      },
    });

    await this.dynamoClient.send(command);
  }

  async isAlreadyPosted(fileId: number): Promise<boolean> {
    const tableName = await this.getTableName();
    const command = new GetItemCommand({
      TableName: tableName,
      Key: {
        file_id: { S: fileId.toString() },
      },
    });

    const response = await this.dynamoClient.send(command);
    return !!response.Item;
  }
}
