export const Term = ({ t, id }) => {
  const anchor = id ? id : t.toLowerCase().replace(/\s+/g, "-");
  const link = `/general/glossary#${anchor}`;

  return <a class="glossary-term" href={link}>{t}</a>;
};


export const Schema = ({ t, id }) => {
  const anchor = id ? id : t.toLowerCase().replace(/\s+/g, "-");
  const link = `/odf/schemas#${anchor}`;

  return <a class="schema-object" href={link}>{t}</a>;
};


export const Diagram = ({ src, alt }) => {
  return <div style={{display: "flex", "flex-direction": "column", "align-items": "center"}}>
    <img src={src} alt={alt} style={{background: "#dddddd", "margin-bottom": 0}}/>
    <span>{alt}</span>
  </div>;
};


export const YouTube = ({ id, width }) => {
  const src = `https://www.youtube.com/embed/${id}`;

  return <iframe
    className="w-full aspect-video rounded-xl"
    src={src}
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
    allowFullScreen
    width={width}
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
