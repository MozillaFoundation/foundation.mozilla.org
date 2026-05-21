/**
 * Entry point for the Gallery Hub page experience.
 *
 * The modules are initialized separately so the page-level vertical carousel,
 * modal overlays, and per-project media slideshows can evolve independently.
 *
 * @module galleryHubPage
 */

import { initGalleryHubOverlay } from "../../components/gallery_hub/overlay";
import { initGalleryHubFilterPanel } from "../../components/gallery_hub/filter_panel";
import { initGalleryHubProjectCarousel } from "../../components/gallery_hub/project_carousel";
import { initGalleryHubSlideshows } from "../../components/gallery_hub/slideshow";

initGalleryHubProjectCarousel();
initGalleryHubFilterPanel();
initGalleryHubOverlay();
initGalleryHubSlideshows();
