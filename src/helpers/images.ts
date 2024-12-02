import sharp from 'sharp';
import axios from 'axios';

const resizeOnHeight = async (
  img: sharp.Sharp,
  maxHeight: number
): Promise<sharp.Sharp> => {
  const metadata = await img.metadata();
  if (!metadata.height || !metadata.width)
    throw new Error('invalid image metadata');

  const ratio = maxHeight / metadata.height;
  const newWidth = Math.floor(metadata.width * ratio);

  return img.resize(newWidth, maxHeight);
};

const resizeOnWidth = async (
  img: sharp.Sharp,
  maxWidth: number
): Promise<sharp.Sharp> => {
  const metadata = await img.metadata();
  if (!metadata.height || !metadata.width)
    throw new Error('invalid image metadata');

  const ratio = maxWidth / metadata.width;
  const newHeight = Math.floor(metadata.height * ratio);

  return img.resize(maxWidth, newHeight);
};

export const fitImageToConstraint = async (
  image: sharp.Sharp,
  constraint = 4096
): Promise<sharp.Sharp> => {
  const metadata = await image.metadata();
  if (!metadata.height || !metadata.width)
    throw new Error('invalid image metadata');

  if (metadata.height > constraint && metadata.height > metadata.width) {
    return resizeOnHeight(image, constraint);
  } else if (metadata.width > constraint) {
    return resizeOnWidth(image, constraint);
  }
  return image;
};

export const getImage = async (url: string): Promise<sharp.Sharp> => {
  const headers = { 'User-Agent': 'Wikimedia Bot' };
  const response = await axios.get(url, {
    headers,
    responseType: 'arraybuffer',
  });

  console.log(`downloading ${url}`);

  if (response.status !== 200) {
    throw new Error('something went wrong downloading the file!');
  }

  return sharp(response.data);
};

export const toBlob = async (image: sharp.Sharp): Promise<Blob> => {
  const metadata = await image.metadata();
  const format = metadata.format || 'jpeg';
  const buffer = await image.toBuffer();
  return new Blob([buffer], { type: `image/${format}` });
};

export const toBuffer = async (image: sharp.Sharp): Promise<Buffer> => {
  const metadata = await image.metadata();
  const format = metadata.format || 'jpeg';
  console.log(format);
  return image.toBuffer();
};
