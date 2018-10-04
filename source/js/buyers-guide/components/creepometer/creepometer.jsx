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

    this.slideStart = this.slideStart.bind(this);
    this.slideMove = this.slideMove.bind(this);
    this.slideStop = this.slideStop.bind(this);

    this.setSliderRef = element => {
      this.sliderElement = element;
    };

  }

  slideStart() {
    console.log(`slideStart`);
    this.setState({
      isHandleGrabbed: true
    });
  }

  slideMove(e) {
    if (this.state.isHandleGrabbed && e.nativeEvent.target.className === `slider`) {
      this.setState({
        handleOffset: e.nativeEvent.offsetX
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
      console.log(frameChoice);
    }

    // let frameChoice = this.state.handleOffset /
    let faceImgSrc = `/_images/buyers-guide/faces/${frameChoice}.png`;

    return (
      <div className="slider" ref={this.setSliderRef} onMouseLeave={this.slideStop} onMouseMove={this.slideMove} onMouseDown={this.slideStart} onMouseUp={this.slideStop}>
        <div className="handle" style={{background: `url("${faceImgSrc}") 0 0 / contain, #f2b946`, left: `${handleX}px`}}></div>
      </div>
    );
  }
}
