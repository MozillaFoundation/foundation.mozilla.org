/**
 * Adding play/pause functionality to the optional Article Page hero video section.
 */

 const articleHeroVideoHandler = () => {
    let articlePageHero = document.querySelector(".article-hero");
  
    if (!articlePageHero) {
      return;
    }
  
    let video = articlePageHero.querySelector("video.hero-video");
    let pauseButton = articlePageHero.querySelector(".btn-pause");
    let playButton = articlePageHero.querySelector(".btn-play");
  
    function toggleVideo() {
        video.paused ? video.play() : video.pause();     
    }



    if (video && pauseButton && playButton) {
      const HIDE = `tw-hidden`;
  
      const showPauseButton = () => {
        playButton.classList.add(HIDE);
        pauseButton.classList.remove(HIDE);
      };
  
      const showPlayButton = () => {
        pauseButton.classList.add(HIDE);
        playButton.classList.remove(HIDE);
      };

      video.addEventListener(`click`, () => {
        toggleVideo();
     });
  
      pauseButton.addEventListener(`click`, () => {
        toggleVideo();
      });
  
      playButton.addEventListener(`click`, () => {
        toggleVideo();
      });
  
      video.addEventListener(`pause`, () => {
        showPlayButton();
      });
  
      video.addEventListener(`playing`, () => {
        showPauseButton();
      });
  
      video.play();
    }
  };
  
  /**
   * Bind handlers to article hero video
   */
  export default () => {
    articleHeroVideoHandler();
  };
  