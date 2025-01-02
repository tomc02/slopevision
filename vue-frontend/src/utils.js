export const isVideo = (url) => {
  return /(mp4|webm|ogg)/i.test(url); // Matches common video extensions anywhere in the URL
};

