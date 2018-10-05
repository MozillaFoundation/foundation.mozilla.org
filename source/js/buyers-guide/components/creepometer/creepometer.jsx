import React from 'react';

export default class Creepometer extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isHandleGrabbed: false,
      handleOffset: 0
    };

    this.handleWidth = 70;
    this.faceCount = 40; // Number of face frames
    this.framePath = `/_images/buyers-guide/faces/`;

    this.slideStart = this.slideStart.bind(this);
    this.slideMove = this.slideMove.bind(this);
    this.slideStop = this.slideStop.bind(this);

    this.setSliderRef = element => {
      this.sliderElement = element;
    };

    // Preload images
    for (let i = 1; i <= this.faceCount; i++) {
      let img = document.createElement(`img`);

      img.src = `${this.framePath}${i}.png`;
    }
  }

  slideStart(e) {
    if (e.nativeEvent.target.className === `handle`) {
      this.setState({
        isHandleGrabbed: true
      });
    }
  }

  slideMove(e) {
    if (this.state.isHandleGrabbed) {
      let clientX = e.nativeEvent.clientX;
      let sliderLeftEdgeX = this.sliderElement.getBoundingClientRect().left;
      let offset = Math.floor(clientX - sliderLeftEdgeX);

      this.setState({
        handleOffset: offset
      });
    }
  }

  slideStop() {
    this.setState({
      isHandleGrabbed: false
    });
  }

  render() {
    let handleX = this.state.handleOffset - this.handleWidth / 2;
    let frameChoice = Math.floor(this.faceCount / 2);

    // Don't let handle overflow slider's left side
    handleX = handleX < 0 ? 0 : handleX;

    if (this.sliderElement) {
      // Don't let handle overflow slider's right side
      if (handleX > this.sliderElement.scrollWidth - this.handleWidth) {
        handleX = this.sliderElement.scrollWidth - this.handleWidth;
      }

      frameChoice = Math.floor(handleX / this.sliderElement.scrollWidth * this.faceCount) + 1;
    }

    let faceImgSrc = `${this.framePath}${frameChoice}.png`;

    return (
      <div className="slider" ref={this.setSliderRef} onMouseLeave={this.slideStop} onMouseMove={this.slideMove} onMouseDown={this.slideStart} onMouseUp={this.slideStop}>
        <div className="handle" style={{background: `url("${faceImgSrc}") 0 0 / contain, #f2b946`, left: `${handleX}px`}}></div>
      </div>
    );
  }
}
