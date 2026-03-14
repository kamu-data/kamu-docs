export const Term = ({ t, id }) => {
  const anchor = id ? id : t.toLowerCase().replace(/\s+/g, "-");
  const link = `/glossary#${anchor}`;

  return <a class="glossary-term" href={link}>{t}</a>;
};


export const Schema = ({ t, id }) => {
  const anchor = id ? id : t.toLowerCase().replace(/\s+/g, "-");
  const link = `/reference#${anchor}`;

  return <a class="schema-object" href={link}>{t}</a>;
};


export const YouTube = ({ id }) => {
  const src = `https://www.youtube.com/embed/${id}`;

  return <iframe
    className="w-full aspect-video rounded-xl"
    src={src}
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen
  ></iframe>;
};


export const YouTubeList = ({ id }) => {
  const src = `https://www.youtube.com/embed/videoseries?list=${id}`;

  return <iframe
    className="w-full aspect-video rounded-xl"
    src={src}
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen
  ></iframe>;
};
