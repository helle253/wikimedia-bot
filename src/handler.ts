import {
  DynamoDBWrapper,
  getRandomImage,
  postToMastodon,
  postToTwitter,
} from './helpers';

const dynamodb = new DynamoDBWrapper();

const post = async (file: { pageid: number; title: string }) => {
  await Promise.all([postToMastodon(file), postToTwitter(file)]);
};

export const handler = async (_event: any, _context: any): Promise<void> => {
  const file = await getRandomImage();
  await dynamodb.recordPostToTable(file.pageid, file.title);
  await post(file);
};
