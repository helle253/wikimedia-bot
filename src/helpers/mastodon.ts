import { SSMClient, GetParameterCommand } from '@aws-sdk/client-ssm';
import { createRestAPIClient } from 'masto';
import { WikimediaFile } from '../types';
import { getFileDetails, getImage, fitImageToConstraint, toBlob } from './';

type Mastodon = ReturnType<typeof createRestAPIClient>;

let mastodonClient: Mastodon | undefined;

const getMastodonClient = async (): Promise<Mastodon> => {
  if (!mastodonClient) {
    const ssmClient = new SSMClient({});
    const [accessKey, baseUrl] = await Promise.all([
      ssmClient.send(
        new GetParameterCommand({
          Name: '/wikimedia_bot/mastodon/access_key',
        })
      ),
      ssmClient.send(
        new GetParameterCommand({
          Name: '/wikimedia_bot/mastodon/base_url',
        })
      ),
    ]);

    if (!accessKey.Parameter?.Value || !baseUrl.Parameter?.Value) {
      throw new Error('mastodon credentials not found in ssm');
    }

    mastodonClient = createRestAPIClient({
      accessToken: accessKey.Parameter.Value,
      url: baseUrl.Parameter.Value,
    });
  }
  return mastodonClient;
};

export const post = async (file: WikimediaFile): Promise<void> => {
  try {
    const mastodon = await getMastodonClient();
    const details = await getFileDetails(file.title);
    const image = await getImage(details.url);
    const resizedImage = await fitImageToConstraint(image, 4096);
    const imageBlob = await toBlob(resizedImage);

    const mediaResponse = (await mastodon.v1.media.create({
      file: imageBlob,
      description: details.descriptionurl,
    })) as any;

    await mastodon.v1.statuses.create({
      status: '',
      mediaIds: [mediaResponse.data.id],
    });
  } catch (e) {
    console.error('error posting to mastodon:', e);
    throw e;
  }
};
