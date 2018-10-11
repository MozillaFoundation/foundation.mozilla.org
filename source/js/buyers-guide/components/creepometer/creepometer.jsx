import React from 'react';

export default class Creepometer extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isHandleGrabbed: false,
      handleOffset: 0
    };

    this.handleWidth = 70; // px
    this.faceCount = 40; // Number of face frames
    this.encodedStepCount = 100; // Upper range of values to be recorded
    this.framePath = `/_images/buyers-guide/faces/`;

    this.slideStart = this.slideStart.bind(this);
    this.slideMove = this.slideMove.bind(this);
    this.slideStop = this.slideStop.bind(this);

    this.setSliderRef = element => {
      this.sliderElement = element;
    };
  }

  componentDidMount() {
    // Slight delay because Firefox is too dang fast
    setTimeout(() => {
      // Set initial position
      this.setState({
        handleOffset: Math.floor(this.props.initialValue / this.encodedStepCount * this.sliderElement.scrollWidth),
        encodedValue: this.props.initialValue
      });
    }, 100);
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
        handleOffset: offset,
        encodedValue: Math.floor(offset / this.sliderElement.scrollWidth * this.encodedStepCount)
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

    let pxOffset = this.handleWidth * this.faceCount - this.handleWidth * frameChoice; // offset position for spritesheet

    return (
      <div class="creepometer">
        <div className="slider" ref={this.setSliderRef} onMouseLeave={this.slideStop} onMouseMove={this.slideMove} onMouseDown={this.slideStart} onMouseUp={this.slideStop}>
          <div className="h6-heading copy copy-left">Not creepy</div>
          <div className="handle" style={{background: `url("${this.framePath}sprite-resized-64-colors.png") 0 ${pxOffset}px / 70px auto, #f2b946`, left: `${handleX}px`}}></div>
          <div className="h6-heading copy copy-right">Super creepy</div>
        </div>
      </div>
    );
  }
}
