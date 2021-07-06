function ArrowDisabler(Glide, Components) {
    return {
        mount() {
            // Only in effect when rewinding is disabled
            if (Glide.settings.rewind) {
                return;
            }

            Glide.on(['mount.after', 'run'], () => {
                // Filter out arrows_control
                Components.Controls.items.forEach((controlItem) => {
                    const left = controlItem.querySelector(
                        '[data-glide-dir="<"]',
                    );

                    const right = controlItem.querySelector(
                        '[data-glide-dir=">"]',
                    );

                    // Set left arrow state
                    if (left) {
                        if (Glide.index === 0) {
                            left.setAttribute('disabled', ''); // Disable on first slide
                        } else {
                            left.removeAttribute('disabled'); // Enable on other slides
                        }
                    }

                    // Set right arrow state
                    if (right) {
                        // Glide.index is based on the active slide
                        // For bound: true, there will be no empty space & the last slide will never become active
                        // Hence add perView to correctly calculate the last slide
                        const lastSlideIndex = Glide.settings.bound
                            ? Glide.index + (Glide.settings.perView - 1)
                            : Glide.index;

                        if (lastSlideIndex === Components.Sizes.length - 1) {
                            right.setAttribute('disabled', ''); // Disable on last slide
                        } else {
                            right.removeAttribute('disabled'); // Disable on other slides
                        }
                    }
                });
            });
        },
    };
}

export default ArrowDisabler;
