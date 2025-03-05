import React from "react";
import { getText } from "../petition/locales";

const PulseProfile = ({ profile }) => {
  return (
    <div className="tw-grid tw-grid-cols-4 tw-gap-x-6 tw-gap-y-4 tw-border-t tw-border-black">
      {/* Image */}
      <div className="tw-block tw-col-span-1 tw-relative tw-min-h-[160px] tw-h-full tw-w-full tw-overflow-hidden">
        <img
          src={
            profile.thumbnail
              ? profile.thumbnail
              : "/static/legacy/_images/fellowships/headshot/placeholder.jpg"
          }
          className="tw-w-auto tw-h-full tw-absolute tw-left-50 tw-top-50 tw-min-w-full tw-object-cover"
          alt="Headshot"
        />
      </div>

      {/* Right card  */}
      <div className="tw-col-start-2 tw-col-span-3 tw-flex tw-flex-col">
        {/* Card top */}
        <div className="tw-flex tw-flex-row tw-justify-between tw-items-start tw-mt-4">
          <div className="tw-text-lg tw-mb-2 tw-font-sans tw-font-normal tw-text-black">
            {profile.name}
          </div>

          {/* Social Icons */}
          <div className="tw-flex tw-flex-row tw-space-x-4 tw-mt-[7px]">
            {profile.twitter && (
              <a className="hover:tw-no-underline" href={profile.twitter}>
                <i className="twitter tw-twitter-glyph" />
              </a>
            )}
            {profile.linkedin && (
              <a className="hover:tw-no-underline" href={profile.linkedin}>
                <i className="linkedIn tw-linkedin-glyph" />
              </a>
            )}
          </div>
        </div>

        {/* Profile Location */}
        {profile.location && (
          <p className="tw-flex-row tw-flex tw-items-center tw-justify-start tw-text-sm tw-my-0">
            <img
              className="tw-w-6 tw-h-6 tw-block tw-mr-2 tw-body-small"
              src="/static/legacy/_images/glyphs/map-marker-icon-dark.svg"
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
            <span className="tw-text-black tw-text-sm tw-font-bold first:tw-ml-0 tw-ml-4">
              {profile.program_type}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

export default PulseProfile;
