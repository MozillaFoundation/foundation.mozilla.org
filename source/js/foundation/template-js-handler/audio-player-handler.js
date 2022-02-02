/**
 * Adding play/pause/seek functionality to the Audio Player component.
 */

const audioBlockHandler = () => {
  let pageAudioBlocks = document.querySelectorAll("#audio-player");

  if (!pageAudioBlocks) {
    return;
  }

  // Used to return times in seconds.
  const calculateTime = (secs) => {
    const minutes = Math.floor(secs / 60);
    const seconds = Math.floor(secs % 60);
    const returnedSeconds = seconds < 10 ? `0${seconds}` : `${seconds}`;
    return `${minutes}:${returnedSeconds}`;
  };

  for (const audioPlayer of pageAudioBlocks) {
    const audio = audioPlayer.querySelector("audio.embedded-audio");
    const pauseButton = audioPlayer.querySelector(
      ".btn-audio-control.btn-pause"
    );
    const playButton = audioPlayer.querySelector(".btn-audio-control.btn-play");
    const durationContainer = audioPlayer.querySelector("#duration");
    const currentTimeContainer = audioPlayer.querySelector("#current-time");
    const seekSlider = audioPlayer.querySelector("#seek-slider");

    seekSlider.value = 0;

    // Adding pause/play functionality to button.
    if (audio && pauseButton && playButton) {
      const HIDE = `d-none`;

      const showPauseButton = () => {
        playButton.classList.add(HIDE);
        pauseButton.classList.remove(HIDE);
      };

      const showPlayButton = () => {
        pauseButton.classList.add(HIDE);
        playButton.classList.remove(HIDE);
      };

      pauseButton.addEventListener(`click`, () => {
        audio.pause();
      });

      playButton.addEventListener(`click`, () => {
        audio.play();
      });

      audio.addEventListener(`pause`, () => {
        showPlayButton();
      });

      audio.addEventListener(`playing`, () => {
        showPauseButton();
      });
      showPlayButton();
    }

    // Setting maximum value for slider based on track length.
    const setSliderMax = () => {
      seekSlider.max = Math.floor(audio.duration);
    };

    // Updating progress bar when user drags on Chrome/Safari
    const updateProgressBar = () => {
      seekSlider.style.setProperty(
        "--seek-before-width",
        (seekSlider.value / seekSlider.max) * 100 + "%"
      );
    };

    // Based on the audio duration, update the tracks total length. (0:00/x:xx <- )
    const displayTrackDuration = () => {
      durationContainer.textContent = calculateTime(audio.duration);
    };

    // Updating current track time and progress bar as user slides.
    seekSlider.addEventListener("input", () => {
      currentTimeContainer.textContent = calculateTime(seekSlider.value);
      updateProgressBar();
    });

    // Updating track position when user selects a time.
    seekSlider.addEventListener("change", () => {
      audio.currentTime = seekSlider.value;
    });

    // Updating current time on progress bar and time as track plays.
    audio.addEventListener("timeupdate", () => {
      seekSlider.value = Math.floor(audio.currentTime);
      updateProgressBar();
      currentTimeContainer.textContent = calculateTime(
        Math.floor(audio.currentTime)
      );
    });

    // If metadata is loaded, set information. If not, wait until it is, and then set info.
    if (audio.readyState > 0) {
      displayTrackDuration();
      setSliderMax();
    } else {
      audio.addEventListener("loadedmetadata", () => {
        displayTrackDuration();
        setSliderMax();
      });
    }
  }
};

/**
 * Bind handlers to audio player
 */
export default () => {
  audioBlockHandler();
};
