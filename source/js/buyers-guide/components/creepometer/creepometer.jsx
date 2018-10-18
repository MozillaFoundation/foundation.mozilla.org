import React from 'react';

export default class Creepometer extends React.Component {
  constructor(props) {
    super(props);

    this.faceCount = 40; // Number of face frames
    this.faceHeight = 70; // pixel height for one frame
    this.framePath = `/_images/buyers-guide/faces/`;

    this.state = {
      dragging: false,
      percentage: 50,
      value: 50
    };

    this.setupDocumentListeners();
  }

  setupDocumentListeners() {
    this.moveListener = (function(evt) {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideMove(evt);
    }).bind(this);

    this.releaseListener = (function(evt) {
      evt.preventDefault();
      evt.stopPropagation();
      this.slideReleased(evt);
      this.removeDocumentListeners();
    }).bind(this);
  }

  addDocumentListeners() {
    document.addEventListener('mousemove', this.moveListener, true);
    document.addEventListener('touchmove', this.moveListener, true);
    document.addEventListener('mouseup', this.releaseListener, true);
    document.addEventListener('touchstart', this.releaseListener, true);
  }

  removeDocumentListeners() {
    document.removeEventListener('mousemove', this.moveListener, true);
    document.removeEventListener('touchmove', this.moveListener, true);
    document.removeEventListener('mouseup', this.releaseListener, true);
    document.removeEventListener('touchstart', this.releaseListener, true);
  }

  slideStart(e) {
    if (e.target === this.handle) {
      this.setState({
        parentBBox: this.sliderElement.getBoundingClientRect(),
        dragging: true
      });
      // The "move" and "release" events have to be handled at
      // the document level, because the events can be generated
      // "nowhere near the React-managed DOM node".
      this.addDocumentListeners();
    }
  }

  slideReleased() {
    this.setState({
      dragging: false
    });
  }

  slideMove(e) {
    if (this.state.dragging) {
      let x = e.clientX, bbox = this.state.parentBBox, percentage, value;

      if (e.touches){
        x = e.touches[0].clientX;
      }

      // cap the position:
      if (x > bbox.right) {
        x = bbox.right;
      } else if (x < bbox.left) {
        x = bbox.left;
      }


      // compute the handle offset
      percentage = Math.round(100 * (x - bbox.left) / bbox.width);
      value = percentage ? percentage : 1;

      console.log(bbox.left, x, bbox.right, percentage);

      this.setState({
        percentage,
        value
      }, () => {
        if (this.props.onChange) {
          this.props.onChange(value);
        }
      });
    }
  }

  render() {
    let frameOffset = Math.round(this.state.percentage * (this.faceCount-1)/100);

    let handleOpts = {
      ref: e => (this.handle=e),
      style: {
        background: `url("${this.framePath}sprite-resized-64-colors.png"), #f2b946`,
        backgroundSize: `70px`,
        backgroundPositionX: 0,
        backgroundPositionY: `-${frameOffset * this.faceHeight}px`,
        backgroundRepeat: `no-repeat`,
        left: `${this.state.value}%`
      },
      onMouseDown: evt => this.slideStart(evt),
      onTouchStart: evt => this.slideStart(evt)
    };

    return (
      <div className="creepometer">
        <div className="slider-container p-2">
          <div className="slider" ref={e => (this.sliderElement=e)}>
            <div className="h6-heading copy copy-left">Not creepy</div>
            <div className="handle" {...handleOpts}></div>
            <div className="h6-heading copy copy-right">Super creepy</div>
          </div>
        </div>
      </div>
    );
  }
}
