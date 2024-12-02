import axios from 'axios';
import { addWeeks, subSeconds } from 'date-fns';

const WIKIMEDIA_API = 'https://commons.wikimedia.org/w/api.php';

interface WikimediaFile {
  pageid: number;
  title: string;
}

interface WikimediaFileDetails {
  url: string;
  descriptionurl: string;
}

const randomTime = (
  start: Date = new Date(2011, 2, 8, 13),
  end: Date = subSeconds(new Date(), addWeeks(new Date(), 4).getTime())
): Date => {
  const delta = end.getTime() - start.getTime();
  const randomSecond = Math.floor(Math.random() * delta);
  return new Date(start.getTime() + randomSecond);
};

const makeRequest = async (params: Record<string, any>) => {
  const { data } = await axios.get(WIKIMEDIA_API, { params });
  if ('error' in data) {
    throw new Error(JSON.stringify(data.error));
  }
  if ('warnings' in data) {
    console.warn(data.warnings);
  }
  if ('query' in data) {
    return data;
  }
  throw new Error('something went wrong!');
};

const findNonPostedImage = (results: WikimediaFile[]): WikimediaFile => {
  return results[0]; // in the future we could check if it's been posted
};

export const getRandomImage = async (): Promise<WikimediaFile> => {
  const request = {
    action: 'query',
    format: 'json',
    list: 'categorymembers',
    cmtype: 'file',
    cmtitle: 'Category:Quality_images',
    cmstart: randomTime(),
    cmsort: 'timestamp',
    cmdir: 'ascending',
  };

  let lastContinue = {};
  while (true) {
    const req = { ...request, ...lastContinue };
    const result = await makeRequest(req);

    if ('query' in result) {
      const results = result.query.categorymembers;
      const freshResult = findNonPostedImage(results);
      if (freshResult) {
        return freshResult;
      }
    }
    lastContinue = result.continue;
  }
};

export const getFileDetails = async (
  fileTitle: string
): Promise<WikimediaFileDetails> => {
  const request = {
    action: 'query',
    format: 'json',
    titles: fileTitle,
    prop: 'imageinfo',
    iiprop: 'url',
  };

  const { data } = await axios.get(WIKIMEDIA_API, { params: request });
  const resultList = Object.values(data.query.pages);
  console.log(resultList);
  return (resultList[0] as any).imageinfo[0];
};
