import React from "react";
import { getText } from "../petition/locales";

const PulseProfile = ({ profile }) => {
  const profileUrl = "https://www.mozillapulse.org/profile/";
  return (
    <div className="tw-grid tw-grid-cols-4 tw-gap-x-3 tw-gap-y-2 tw-border-t tw-border-black">
      {/* Image */}
      <a
        href={`https://www.mozillapulse.org/profile/${profile.profile_id}`}
        className="tw-block tw-col-span-1 tw-relative tw-min-h-[160px] tw-h-[100%] tw-w-full tw-overflow-hidden"
      >
        <img
          src={
            profile.thumbnail
              ? profile.thumbnail
              : "/static/_images/fellowships/headshot/placeholder.jpg"
          }
          className="tw-w-auto tw-h-full tw-absolute tw-left-50 tw-top-50 tw-min-w-full tw-object-cover"
          alt="Headshot"
        />
      </a>

      {/* Right card  */}
      <div className="tw-col-start-2 tw-col-span-3 tw-flex tw-flex-col">
        {/* Card top */}
        <div className="tw-flex tw-flex-row tw-justify-between tw-items-start tw-mt-2">
          <a
            className="tw-text-lg tw-mb-1 tw-font-sans tw-font-normal tw-text-black"
            href={`${profileUrl}${profile.profile_id}`}
          >
            {profile.name}
          </a>

          {/* Social Icons */}
          <div className="tw-flex tw-flex-row tw-space-x-2 tw-mt-[7px]">
            {profile.twitter && (
              <a className="hover:tw-no-underline" href={profile.twitter}>
                <i className="twitter twitter-glyph small" />
              </a>
            )}
            {profile.linkedin && (
              <a className="hover:tw-no-underline" href={profile.linkedin}>
                <i className="linkedIn linkedIn-glyph small" />
              </a>
            )}
          </div>
        </div>

        {/* Profile Location */}
        {profile.location && (
          <p className="tw-flex-row tw-flex tw-items-center tw-justify-start tw-text-sm tw-my-0">
            <img
              className="tw-w-[12px] tw-h-[12px] tw-block tw-mr-1 body-small"
              src="/static/_images/glyphs/map-marker-icon-dark.svg"
              alt=""
            />
            {profile.location}
          </p>
        )}

        {/* Short bio block */}
        {profile.user_bio && (
          <p className="tw-text-gray-60 tw-text-sm medium:tw-text-[15px] my-2">
            {profile.user_bio}
          </p>
        )}

        {profile.program_type && (
          <div className="tw-flex tw-flex-wrap tw-mt-auto">
            <span className="tw-text-black tw-text-sm tw-font-bold first:tw-ml-0 tw-ml-2">
              {profile.program_type}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default PulseProfile;
