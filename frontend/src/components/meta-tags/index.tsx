import React from "react";

import Head from "next/head";
import { useRouter } from "next/router";

import messages from "~/locale";
import { useCurrentLanguage } from "~/locale/context";

type Props = {
  title?: React.ReactNode | string | null;
  description?: string;
  useDefaultSocialCard?: boolean;
  useNewSocialCard?: boolean;
};

const getSocialCardURL = (
  asPath: string,
  useDefaultSocialCard: boolean,
  useNewSocialCard: boolean,
  locale: string,
) => {
  if (useDefaultSocialCard) {
    return `${process.env.NEXT_PUBLIC_SOCIAL_CARD_SERVICE}?url=${process.env.NEXT_PUBLIC_SITE_URL}en/social`;
  }

  if (useNewSocialCard) {
    return `${process.env.NEXT_PUBLIC_SITE_URL}api/${locale}/${asPath.substring(
      1,
    )}/social-card`;
  }

  return `${process.env.NEXT_PUBLIC_SOCIAL_CARD_SERVICE}?url=${
    process.env.NEXT_PUBLIC_SITE_URL
  }${asPath.substr(1)}/social`;
};

export const MetaTags = ({
  title,
  description,
  useDefaultSocialCard = true,
  useNewSocialCard = false,
  children,
}: React.PropsWithChildren<Props>) => {
  const language = useCurrentLanguage();
  const { asPath, locale } = useRouter();
  const socialCard = getSocialCardURL(
    asPath,
    useDefaultSocialCard,
    useNewSocialCard,
    locale,
  );

  const titleTemplate = messages[language].titleTemplate;

  description = description || messages[language].description;

  const titleContent = titleTemplate.replace(
    "%s",
    title ? title.toString() : "",
  );

  return (
    <Head>
      <title>{titleTemplate.replace("%s", title.toString())}</title>

      <meta name="title" content={titleContent} />
      <meta name="description" content={description} />

      <meta property="og:type" content="website" />
      <meta property="og:title" content={titleContent} />
      <meta property="og:description" content={description} />
      <meta property="og:image" content={socialCard} />

      <meta property="twitter:card" content="summary_large_image" />
      <meta property="twitter:title" content={titleContent} />
      <meta property="twitter:description" content={description} />
      <meta property="twitter:image" content={socialCard} />

      {children}
    </Head>
  );
};
