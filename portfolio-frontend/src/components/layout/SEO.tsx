interface SEOProps {
  title: string;
  description: string;
  image?: string;
  url?: string;
  type?: 'website' | 'article';
  twitterHandle?: string;
}

export function SEO({ title, description, image, url, type = 'website', twitterHandle }: SEOProps) {
  const siteName = 'ED | Portfolio';
  const fullTitle = `${title} | ${siteName}`;
  const siteUrl = url || 'https://portfolio-edu444477.vercel.app';
  const ogImage = image || '/og-default.png';

  return (
    <>
      <title>{fullTitle}</title>
      <meta name="description" content={description} />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <link rel="canonical" href={siteUrl} />

      <meta property="og:type" content={type} />
      <meta property="og:url" content={siteUrl} />
      <meta property="og:title" content={fullTitle} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:site_name" content={siteName} />

      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:url" content={siteUrl} />
      <meta name="twitter:title" content={fullTitle} />
      <meta name="twitter:description" content={description} />
      <meta name="twitter:image" content={ogImage} />
      {twitterHandle && <meta name="twitter:creator" content={twitterHandle} />}

      <meta name="theme-color" content="#0ea5e9" />
      <meta name="color-scheme" content="light dark" />
    </>
  );
}