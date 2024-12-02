import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';
import { TwitterApi } from 'twitter-api-v2';
import { WikimediaFile } from '../types';
import { getFileDetails, getImage, fitImageToConstraint, toBuffer } from './';

let twitterClient: TwitterApi | undefined;

const getTwitterClient = async (): Promise<TwitterApi> => {
  if (!twitterClient) {
    const ssmClient = new SSMClient({});
    const [apiKey, apiSecret, accessToken, accessSecret] = await Promise.all([
      ssmClient.send(
        new GetParameterCommand({
          Name: '/wikimedia_bot/twitter/api_key',
        })
      ),
      ssmClient.send(
        new GetParameterCommand({
          Name: '/wikimedia_bot/twitter/api_key_secret',
        })
      ),
      ssmClient.send(
        new GetParameterCommand({
          Name: '/wikimedia_bot/twitter/access_token',
        })
      ),
      ssmClient.send(
        new GetParameterCommand({
          Name: '/wikimedia_bot/twitter/access_token_secret',
        })
      ),
    ]);

    if (
      !apiKey.Parameter?.Value ||
      !apiSecret.Parameter?.Value ||
      !accessToken.Parameter?.Value ||
      !accessSecret.Parameter?.Value
    ) {
      throw new Error('twitter credentials not found in ssm');
    }

    twitterClient = new TwitterApi({
      appKey: apiKey.Parameter.Value,
      appSecret: apiSecret.Parameter.Value,
      accessToken: accessToken.Parameter.Value,
      accessSecret: accessSecret.Parameter.Value,
    });
  }
  return twitterClient;
};

export const post = async (file: WikimediaFile): Promise<void> => {
  try {
    const twitter = await getTwitterClient();
    const details = await getFileDetails(file.title);
    const image = await getImage(details.url);
    const resizedImage = await fitImageToConstraint(image, 2048);
    const imageBuffer = await toBuffer(resizedImage);

    const mediaId = await twitter.v1.uploadMedia(imageBuffer, {
      mimeType: 'image/jpeg',
    });

    await twitter.v1.createMediaMetadata(mediaId, {
      alt_text: { text: details.descriptionurl },
    });

    await twitter.v2.tweet('', {
      media: { media_ids: [mediaId] },
    });
  } catch (e) {
    console.error('error posting to twitter:', e);
    throw e;
  }
};
