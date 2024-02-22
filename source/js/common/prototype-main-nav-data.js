const SVG_CLASS_ATTR = `class="tw-inline-block tw-mb-2 tw-mr-2"`;
const SVG = {
  award: `<svg ${SVG_CLASS_ATTR} width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg"><g stroke="#595CF3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 11.25A5.25 5.25 0 1 0 9 .75a5.25 5.25 0 0 0 0 10.5z"/><path d="M6.157 10.418L5.25 17.25 9 15l3.75 2.25-.908-6.84"/></g></svg>`,
  "dollar-sign": `<svg ${SVG_CLASS_ATTR} width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg"><g stroke="#595CF3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M9 .75v16.5M12.75 3.75H7.125a2.625 2.625 0 0 0 0 5.25h3.75a2.625 2.625 0 0 1 0 5.25H4.5"/></g></svg>`,
  headphones: `<svg ${SVG_CLASS_ATTR} width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg"><g stroke="#595CF3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M2.25 13.5V9a6.75 6.75 0 0 1 13.5 0v4.5"/><path d="M15.75 14.25a1.5 1.5 0 0 1-1.5 1.5h-.75a1.5 1.5 0 0 1-1.5-1.5V12a1.5 1.5 0 0 1 1.5-1.5h2.25v3.75zm-13.5 0a1.5 1.5 0 0 0 1.5 1.5h.75a1.5 1.5 0 0 0 1.5-1.5V12a1.5 1.5 0 0 0-1.5-1.5H2.25v3.75z"/></g></svg>`,
  "refresh-ccw": `<svg ${SVG_CLASS_ATTR} width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg"><g stroke="#595CF3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M.75 3v4.5h4.5M17.25 15v-4.5h-4.5"/><path d="M15.367 6.752A6.75 6.75 0 0 0 4.23 4.232L.75 7.502m16.5 3l-3.48 3.27a6.75 6.75 0 0 1-11.137-2.52"/></g></svg>`,
  users: `<svg ${SVG_CLASS_ATTR} width="18" height="18" fill="none" xmlns="http://www.w3.org/2000/svg"><g stroke="#595CF3" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12.75 15.75v-1.5a3 3 0 0 0-3-3h-6a3 3 0 0 0-3 3v1.5M6.75 8.25a3 3 0 1 0 0-6 3 3 0 0 0 0 6zM17.25 15.75v-1.5A3 3 0 0 0 15 11.348M12 2.348a3 3 0 0 1 0 5.812"/></g></svg>`,
};

let navData = {
  navItems: [
    {
      name: "Who we are",
      url: "/en/who-we-are/",
      class: "",
      dropdown: [
        {
          type: "intro",
          title: "About Us",
          description:
            "Mozilla is a global nonprofit dedicated to keeping the Internet a public resource that is open and accessible to all.",
          class: "",
        },
        {
          type: "link",
          title: "Approach",
          links: [
            {
              title: "Strategy",
              url: "/en/who-we-are/strategy/",
            },
            {
              title: "Leadership",
              url: "/en/who-we-are/leadership/",
            },
          ],
          class: "",
        },
        {
          type: "link",
          title: "Legal",
          links: [
            {
              title: "Public Records",
              url: "/en/who-we-are/public-records/",
            },
            {
              title: "Licensing",
              url: "/en/who-we-are/licensing/",
            },
          ],
          class: "",
        },
      ],
    },
    {
      name: "What we do",
      url: "/en/what-we-do/",
      class: "",
      bigCta: {
        text: "Learn more about what we do →",
        link: "/en/what-we-do/",
      },
      dropdown: [
        {
          type: "link",
          title: "Connect People",
          links: [
            {
              title: "Fellowships & Awards",
            },
            {
              title: "Data Futures Lab",
              url: "/en/data-futures-lab/",
              description: "Explore Approaches To Data Stewardship",
            },
            {
              title: "Responsible Computing",
              url: "/en/responsible-computing-challenge/",
              description:
                "A grant opportunity that empowers computing students",
            },
            {
              title: "Mozilla Festival",
              url: "https://www.mozillafestival.org/",
              description:
                "Where passionate individuals unite to build a better internet.",
              external: true,
            },
          ],
          class: "",
        },
        {
          type: "link",
          title: "Rally Communities",
          links: [
            {
              title: "Campaigns",
              url: "/en/campaigns/",
            },
            {
              title: "Common Voice",
              url: "/en/common-voice/",
              description:
                "An initiative to help teach machines how real people speak.",
            },
            {
              title: "IRL Podcast",
              url: "https://irlpodcast.org/",
              external: true,
              description:
                "A podcast covering the intersection between online life and real life",
            },
          ],
          class: "",
        },
        {
          type: "link",
          title: "Influence Policies",
          links: [
            {
              title: "YouTube Regrets",
              url: "/en/youtube/",
              description: "Investigating Youtube’s harmful recommendations",
            },
            {
              title: "*Privacy Not Included",
              url: "https://privacynotincluded.org/",
              external: true,
              description:
                "A buyers guide that helps you shop smart when it comes to privacy.",
            },
          ],
        },
        {
          type: "link",
          title: "Research & Analysis",
          links: [
            {
              title: "Trustworthy AI Research",
              url: "/en/insights/trustworthy-ai-whitepaper/",
              description:
                "Challenges, opportunities, and accountability in the AI era",
            },
            {
              title: "Internet Health Report",
              url: "https://internethealthreport.org/",
              external: true,
              description:
                "Research on issues impacting a healthy internet & possible solutions",
            },
          ],
        },
      ],
    },
    {
      name: "What you can do",
      url: "/en/what-you-can-do/",
      class: "",
      dropdown: [
        {
          type: "intro",
          title: "Get Involved",
          description:
            "From donating funds or data, to signing a petition, to applying to become a volunteer or fellow there are many ways to get involved with the community.",
          class: "",
        },
        {
          type: "link",
          title: "Act",
          links: [
            {
              title: "Sign a Petition",
              url: "/en/campaigns/",
            },
            {
              title: "Download YouTube Regrets Reporter",
              url: "/en/youtube/regretsreporter/",
              description:
                "Help monitor the harm of YouTube’s algorithm by reporting strange recommendations",
            },
            {
              title: "Donate Your Voice to Common Voice",
              url: "https://commonvoice.mozilla.org/",
              description:
                "Contribute to a growing voice dataset base that encompasses the underrepresented",
              external: true,
            },
          ],
          class: "",
        },
        {
          type: "link",
          title: "Learn",
          links: [
            {
              title: "Explore our Research Hub",
              url: "/en/research/",
            },
            {
              title: "Listen to our IRL Podcast",
              url: "https://irlpodcast.org/",
              description:
                "IRL is a podcast covering the intersection between online life and real life",
              external: true,
            },
            {
              title: "Learn about the privacy of internet connected products",
              url: "https://privacynotincluded.org/",
              description: "Read About *Privacy Not Included",
              external: true,
            },
            {
              title: "Explore Mozilla Festival",
              url: "https://www.mozillafestival.org/",
              description:
                "MozFest is a gathering where passionate individuals unite to build a better internet.",
              external: true,
            },
          ],
          class: "",
        },
        {
          type: "featured",
          title: "Donate",
          links: [
            {
              title: "Make a Donation",
              url: "/en/donate/",
              icon: SVG["dollar-sign"],
            },
            {
              title: "Ways to Give",
              url: "/en/what-you-can-do/#ways-to-give",
              icon: SVG["users"],
            },
          ],
        },
      ],
    },
    {
      name: "Funding",
      url: "/en/what-we-fund/",
      class: "",
      dropdown: [
        {
          type: "intro",
          title: "Apply for Funding",
          content: {
            description:
              "The Mozilla Foundation provides funding and resources to individuals, groups, and organizations aligned with creating a more human-centered internet.",
            button: {
              text: "Learn more →",
              url: "/en/what-we-fund/",
            },
          },
          class: "",
        },
        {
          type: "link",
          title: "Opportunities",
          links: [
            {
              title: "Fellowships",
              url: "/en/what-we-fund/fellowships/",
              description:
                "A program empowering leaders to carry out work that ensures the internet remains a force for good.",
            },
            {
              title: "Awards",
              url: "/en/what-we-fund/awards/",
            },
          ],
        },
        {
          type: "link",
          title: "Community Impact",
          links: [
            {
              title: "Alumni",
              url: "/en/what-we-fund/alumni/",
              description:
                "Program Alumni, community connections and opportunities",
            },
            {
              title: "Collaborative Funds",
              url: "/en/what-we-fund/funding-collaboratives/",
              description:
                "An ecosystem of donors working together to have a broader and more meaningful impact.",
            },
          ],
        },
      ],
    },
    {
      name: "Blog",
      url: "/en/blog/",
      class: "",
      bigCta: {
        text: "See all blog posts →",
        link: "/en/blog/",
      },
      dropdown: [
        {
          type: "posts",
          title: "Featured Posts",
          desktopColSpan: 2,
          links: [
            {
              category: "Advocacy",
              title: "Ring Rethinks Police Partnerships",
              description:
                "Amazon Ring will no longer allow law enforcement to request users’ doorbell footage through the associated Neighbors app. This is a positive development for millions of Ring users in the U.S. — and the tens of millions of others who appear in Ring record…",
            },
            {
              category: "Mozilla Festival",
              title:
                "Be a part of creating MozFest House 2024 in the Netherlands",
              url: "https://www.mozillafestival.org/",
              description:
                "We are looking for passionate individuals to help co-design the 2024 MozFest House in the Netherlands. This is your opportunity to share your ideas and make a real impact. Applications close Jan 31, 2024.",
              external: true,
            },
            {
              category: "Advocacy",
              title: "TikTok Quickly Goes From Funny Memes To Depressing Teens",
              description:
                "TikTok has users of all ages, including young users. How quickly does a young person on TikTok start to see depression-related content? The answer isn’t great.",
            },
          ],
        },
        {
          type: "featured",
          title: "Popular Topics",
          links: [
            {
              title: "Advocacy",
              url: "/en/blog/topic/advocacy/",
              icon: SVG["users"],
            },
            {
              title: "Fellowship & Awards",
              url: "/en/blog/topic/fellowships-awards/",
              icon: SVG["award"],
            },
            {
              title: "Common Voice",
              url: "/en/blog/topic/common-voice/",
              icon: SVG["headphones"],
            },
            {
              title: "Insights",
              url: "/en/blog/topic/insights/",
              icon: SVG["refresh-ccw"],
            },
          ],
        },
      ],
    },
  ],
};

navData.primaryNavLookUp = {};

navData.navItems.forEach((navItem) => {
  let dropdown = navItem.dropdown;
  let totalDesktopColumnSpan = 0;

  navData.primaryNavLookUp[navItem.url] = navItem.name;

  if (dropdown.length == 0) {
    return;
  }

  dropdown.forEach((section) => {
    if (!section.desktopColSpan) {
      section.desktopColSpan = 1;
    }
    totalDesktopColumnSpan += section.desktopColSpan;

    section.links?.map((item) => {
      navData.primaryNavLookUp[item.url] = navItem.name;
    });
  });

  navItem.totalDesktopColumnSpan = totalDesktopColumnSpan;
});

export default navData;
